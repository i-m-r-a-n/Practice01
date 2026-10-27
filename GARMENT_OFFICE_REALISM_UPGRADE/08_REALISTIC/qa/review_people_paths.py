"""Independent count/privacy/path audit, explicitly separate from body contacts."""
import base64
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).parent
PEOPLE = QA.parent / "people"
ASSETS = ROOT / "GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS"


def point_in(p, poly):
    x, z = p
    hit = False
    for (ax, az), (bx, bz) in zip(poly, poly[1:] + poly[:1]):
        if (az > z) != (bz > z) and x < (bx - ax) * (z - az) / (bz - az) + ax:
            hit = not hit
    return hit


def point_segment(p, a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]
    length = dx * dx + dz * dz
    t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / length)) if length else 0
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dz)


def segments_distance(a, b, c, d):
    def cross(p, q, r):
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    if cross(a, b, c) * cross(a, b, d) < 0 and cross(c, d, a) * cross(c, d, b) < 0:
        return 0
    return min(point_segment(a, c, d), point_segment(b, c, d), point_segment(c, a, b), point_segment(d, a, b))


def main():
    sources = [PEOPLE / "people-manifest.json", PEOPLE / "people-layer.js", ASSETS / "office_web_metadata.json", ASSETS / "walk_grid.json"]
    manifest = json.loads(sources[0].read_text())
    metadata = json.loads(sources[2].read_text())
    grid = json.loads(sources[3].read_text())
    bits = base64.b64decode(grid["blocked_bits_base64"])
    rooms = {r["zone"]: r for r in metadata["rooms"]}
    empty = {zone: rooms[zone]["polygon_xz"] for zone in manifest["emptyZones"]}
    checks = []
    def check(name, passed, detail=None):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})
    def grid_blocked(x, z):
        col = math.floor((x - grid["origin_xz"][0]) / grid["res"])
        row = math.floor((z - grid["origin_xz"][1]) / grid["res"])
        if col < 0 or row < 0 or col >= grid["cols"] or row >= grid["rows"]:
            return True
        index = row * grid["cols"] + col
        return bool(bits[index >> 3] & (1 << (index & 7)))
    actors = manifest["actors"]
    check("25 to40 illustrative actors with uniqueIDs", 25 <= len(actors) <= 40 and manifest["count"] == len(actors) and len({a["id"] for a in actors}) == len(actors))
    check("fictional metadata and visible disclosure text supplied", all(a.get("fictional") is True for a in actors) and "illustrative" in manifest["note"].lower())
    check("all eight reserved empty zones declared", set(empty) == {"Z23", "Z24", "Z25", "Z26", "Z27", "Z28", "Z29", "Z34"})
    for name, asset in manifest["assets"].items():
        actual = hashlib.sha256((PEOPLE / asset["file"]).read_bytes()).hexdigest()
        check("asset source hash " + name, actual == asset["sha256"], actual)
    samples = 0
    for actor in actors:
        identity = actor["id"]
        anchor = [actor["position"][0], actor["position"][2]]
        path = actor.get("path") or [anchor]
        segments = list(zip(path, path[1:])) or [(anchor, anchor)]
        minimum = math.inf
        offending = []
        for zone, polygon in empty.items():
            for a, b in segments:
                distance = 0 if point_in(a, polygon) or point_in(b, polygon) else min(segments_distance(a, b, c, d) for c, d in zip(polygon, polygon[1:] + polygon[:1]))
                minimum = min(minimum, distance)
                if distance < actor["radius"] - 1e-9:
                    offending.append(zone)
        check(identity + " entire authored capsule path avoids empty rooms", not offending and actor["zone"] not in empty, {"minimum_centerline_to_empty_room_m": minimum, "declared_radius_m": actor["radius"], "offending": sorted(set(offending))})
        if actor.get("path"):
            violations = []
            grow = max(0, actor["radius"] - grid["walker_radius_m"])
            for a, b in segments:
                n = max(1, math.ceil(math.dist(a, b) / .02))
                for i in range(n + 1):
                    x, z = a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n
                    samples += 1
                    # Denser independent circle than the runtime's four growth probes.
                    for j in range(24):
                        angle = 2 * math.pi * j / 24
                        if grid_blocked(x + grow * math.cos(angle), z + grow * math.sin(angle)):
                            violations.append([round(x, 5), round(z, 5)])
                            break
            check(identity + " sampled grown-grid path", not violations, {"violations": violations[:10]})
    result = {
        "scope": "Independent actor count, asset lock and whole authored-path privacy/capsule audit. Actual posed body vertices, contacts and visitor interaction are separate tests.",
        "source_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        "checks": checks, "passed": sum(c["passed"] for c in checks), "total": len(checks), "path_sample_count": samples,
        "limitations": ["Capsule radius is a runtime model, not proof that animated hands, clothes or feet remain inside it.", "Grid sampling is not a continuous source-triangle collision proof.", "The disclosure text is checked in data here; actual visibility is verified in screenshots/UI separately."],
    }
    (QA / "people-path-independent-review.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({k: result[k] for k in ["passed", "total", "path_sample_count"]}))
    if result["passed"] != result["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
