#!/usr/bin/env python3
"""Turn the Shakwat factory room screenshots into photorealistic images with OpenAI's image model.

Usage:
  python3 gpt_realistic.py --images DIR --out DIR [--select roomview|best3|all] [--limit N]
                           [--quality low|medium|high] [--model NAME] [--dry-run]

- DIR holds the screenshots named like 01_Z01_centre_000deg.jpg (as produced by capture_rooms.js).
- Output goes to OUT/<NN room name>/<same file name>.png, one folder per room, matching the Drive folders.
- Safe to run twice: an image whose output already exists is skipped.
- Every call is logged to OUT/ledger.jsonl (file, model, quality, seconds, status).
- The API key is read from OPENAI_API_KEY. It is never printed.
"""
import argparse, base64, json, os, re, sys, time
from pathlib import Path

import requests

API = "https://api.openai.com/v1"
HERE = Path(__file__).resolve().parent

PROMPT = (
    "This is a screenshot of a 3D model of an office interior (a concept design). "
    "Turn it into a photorealistic architectural interior photograph of the same room. "
    "Keep exactly the same camera position, angle and framing. Keep the same room layout, walls, "
    "doors, windows, glass partitions, ceiling beams, furniture, its positions and sizes, colours, "
    "materials, artwork and any logos or signage text exactly as shown. "
    "Do not add, remove or move any object. Do not add people. "
    "Only improve realism: real material textures (wood grain, fabric weave, terrazzo, metal, glass "
    "reflections), natural soft daylight combined with the light fittings that are visible, soft "
    "realistic shadows and ambient occlusion, accurate white balance, and the look of a professional "
    "interior photo taken with a full-frame camera."
)

PREFERENCE = ["00_room_view", "corner_1", "corner_2", "corner_3", "corner_4",
              "centre_000deg", "centre_090deg", "centre_180deg", "centre_270deg",
              "centre_045deg", "centre_135deg", "centre_225deg", "centre_315deg"]


def room_names():
    rooms = json.loads((HERE / "rooms.json").read_text(encoding="utf8"))
    return {r["zone"]: f"{r['order']:02d} {r['name']}" for r in rooms}


def pick(files, mode):
    by_room = {}
    for f in sorted(files):
        m = re.match(r"^(\d\d)_(Z\d\d)_(.+)\.jpg$", f.name)
        if m:
            by_room.setdefault(m.group(2), []).append((m.group(3), f))
    out = []
    for zone, items in by_room.items():
        if mode == "all":
            out += [(zone, f) for _, f in items]
            continue
        n = 1 if mode == "roomview" else 3
        ranked = sorted(items, key=lambda it: PREFERENCE.index(it[0]) if it[0] in PREFERENCE else 99)
        out += [(zone, f) for _, f in ranked[:n]]
    return out


def headers():
    key = os.environ.get("OPENAI_API_KEY")
    # A Network secret added by the cloud proxy also works: send a placeholder, the proxy replaces it.
    return {"Authorization": f"Bearer {key or 'sk-placeholder'}"}


def newest_image_model():
    r = requests.get(f"{API}/models", headers=headers(), timeout=60)
    if r.status_code == 401:
        sys.exit("OpenAI answered 401: the API key is missing or wrong. Add OPENAI_API_KEY to the environment.")
    r.raise_for_status()
    ids = [m["id"] for m in r.json().get("data", []) if m["id"].startswith("gpt-image")]
    if not ids:
        sys.exit("No gpt-image model is available for this API key.")
    full = [i for i in ids if "mini" not in i] or ids

    def ver(i):
        nums = re.findall(r"\d+(?:\.\d+)?", i)
        return float(nums[0]) if nums else 0.0
    return sorted(full, key=lambda i: (ver(i), len(i)))[-1]


def edit(model, src, quality):
    data = {"model": model, "prompt": PROMPT, "size": "1536x1024", "quality": quality, "n": "1"}
    with_fidelity = dict(data, input_fidelity="high")
    for attempt in range(4):
        for payload in (with_fidelity, data):
            with open(src, "rb") as fh:
                r = requests.post(f"{API}/images/edits", headers=headers(),
                                  files={"image": (src.name, fh, "image/jpeg")}, data=payload, timeout=600)
            if r.status_code == 400 and "input_fidelity" in r.text:
                continue  # this model does not take input_fidelity: retry without it
            break
        if r.status_code in (429, 500, 502, 503, 504):
            time.sleep(10 * (attempt + 1))
            continue
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:400]}")
        return base64.b64decode(r.json()["data"][0]["b64_json"]), r.json().get("usage")
    raise RuntimeError(f"gave up after retries: HTTP {r.status_code}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--select", default="roomview", choices=["roomview", "best3", "all"])
    ap.add_argument("--quality", default="high", choices=["low", "medium", "high"])
    ap.add_argument("--limit", type=int, default=0, help="stop after this many new images (0 = no limit)")
    ap.add_argument("--model", default="")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    names = room_names()
    jobs = pick(list(a.images.glob("*.jpg")), a.select)
    todo = [(z, f, a.out / names.get(z, z) / (f.stem + ".png")) for z, f in jobs]
    todo = [t for t in todo if not t[2].exists()]
    if a.limit:
        todo = todo[:a.limit]
    print(f"selected {len(jobs)} images, {len(todo)} still to generate (mode {a.select}, quality {a.quality})")
    if a.dry_run:
        for z, f, o in todo:
            print(f"  {f.name}  ->  {o.relative_to(a.out)}")
        return

    model = a.model or newest_image_model()
    print("model:", model)
    a.out.mkdir(parents=True, exist_ok=True)
    ledger = a.out / "ledger.jsonl"
    ok = fail = 0
    for i, (z, f, o) in enumerate(todo, 1):
        t0 = time.time()
        try:
            png, usage = edit(model, f, a.quality)
            o.parent.mkdir(parents=True, exist_ok=True)
            o.write_bytes(png)
            ok += 1
            status = "ok"
        except Exception as e:  # keep going; the ledger records the failure
            fail += 1
            usage, status = None, f"error: {e}"
        with ledger.open("a", encoding="utf8") as lf:
            lf.write(json.dumps({"file": f.name, "out": str(o.relative_to(a.out)), "model": model,
                                 "quality": a.quality, "seconds": round(time.time() - t0, 1),
                                 "usage": usage, "status": status}) + "\n")
        print(f"[{i}/{len(todo)}] {f.name}: {status}")
        if status.startswith("error: HTTP 401") or status.startswith("error: HTTP 403"):
            sys.exit("Stopping: the API refused the key.")
    print(f"done: {ok} new, {fail} failed. Output: {a.out}")


if __name__ == "__main__":
    main()
