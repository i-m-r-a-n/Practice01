"""Independent artifact consistency check; does not execute the viewer movement."""
import base64
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).parent
ASSETS = ROOT / "GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS"


def main():
    witness_file = QA / "walk-route-witness.json"
    witness = json.loads(witness_file.read_text())
    grid_file = ASSETS / "walk_grid.json"
    meta_file = ASSETS / "office_web_metadata.json"
    grid = json.loads(grid_file.read_text())
    bits = base64.b64decode(grid["blocked_bits_base64"])
    ox, oz = grid["origin_xz"]
    checks = []

    def check(name, value, detail=None):
        checks.append({"name": name, "passed": bool(value), "detail": detail})

    def blocked(point):
        x, z = point
        col = math.floor((x - ox) / grid["res"])
        row = math.floor((z - oz) / grid["res"])
        if col < 0 or row < 0 or col >= grid["cols"] or row >= grid["rows"]:
            return True
        index = row * grid["cols"] + col
        return bool((bits[index >> 3] >> (index & 7)) & 1)

    for source in [grid_file, meta_file]:
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        check("source lock " + source.name, actual == witness["source_sha256"][source.name], actual)
    check("ten ordered destinations", [w["zone"] for w in witness["waypoints"]] == ["Z01", "Z02", "Z30", "Z08", "Z12", "Z07", "Z18", "Z20", "Z23", "Z25"])
    total = 0
    sample_count = 0
    for index, leg in enumerate(witness["legs"]):
        points = leg["points_xz"]
        label = f"{leg['from']} to {leg['to']}"
        check(label + " continuous endpoints", points[0] == witness["waypoints"][index]["xz"] and points[-1] == witness["waypoints"][index + 1]["xz"])
        check(label + " all authored centres free", not any(blocked(p) for p in points))
        distances = [math.dist(a, b) for a, b in zip(points, points[1:])]
        check(label + " four-connected increments", all(abs(d - grid["res"]) < 1e-8 and (abs(a[0] - b[0]) < 1e-8 or abs(a[1] - b[1]) < 1e-8) for a, b, d in zip(points, points[1:], distances)))
        length = sum(distances)
        total += length
        check(label + " recorded length", abs(length - leg["length_m"]) < 1e-7)
        bad = []
        for a, b in zip(points, points[1:]):
            for j in range(6):
                t = j / 5
                point = [a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])]
                sample_count += 1
                if blocked(point):
                    bad.append(point)
        check(label + " interpolation at 0.02m samples", not bad, {"blocked_samples": bad[:5]})
    check("total length", abs(total - witness["total_route_m"]) < 1e-7, round(total, 4))
    report = {
        "scope": "Independent check of the saved static witness against exact original grid bytes. No viewer, new props or people tested.",
        "witness_sha256": hashlib.sha256(witness_file.read_bytes()).hexdigest(),
        "checks": checks, "passed": sum(c["passed"] for c in checks), "total": len(checks),
        "sample_count": sample_count, "route_m": round(total, 4),
        "limitations": ["Raster collision uses inherited 0.15m walker radius; not a real body-clearance certification.", "Browser movement, acceleration, default spawning, dynamic people and new props remain separate checks."],
    }
    (QA / "walk-route-independent-review.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ["passed", "total", "sample_count", "route_m"]}))
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
