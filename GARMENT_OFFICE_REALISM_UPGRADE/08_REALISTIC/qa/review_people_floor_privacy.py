"""Audit actual exported, visible posed people geometry without changing assets.

Floor tests use referenced shoe vertices and exact source finish heights. Privacy
tests use conservative horizontal convex hulls of all referenced visible meshes;
a separated hull proves the enclosed rendered triangles are separated too.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

from review_people_paths import point_in, segments_distance

QA = Path(__file__).parent
ROOT = QA.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(points, polygon):
    result = np.zeros(len(points), dtype=bool)
    x, z = points[:, 0], points[:, 1]
    for (ax, az), (bx, bz) in zip(polygon, polygon[1:] + polygon[:1]):
        if az != bz:
            result ^= ((az > z) != (bz > z)) & (x < (bx - ax) * (z - az) / (bz - az) + ax)
    return result


def hull(points):
    points = sorted(set(map(tuple, points)))
    if len(points) <= 1:
        return points
    def cross(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    low, high = [], []
    for p in points:
        while len(low) >= 2 and cross(low[-2], low[-1], p) <= 0:
            low.pop()
        low.append(p)
    for p in reversed(points):
        while len(high) >= 2 and cross(high[-2], high[-1], p) <= 0:
            high.pop()
        high.append(p)
    return low[:-1] + high[:-1]


def polygon_distance(a, b):
    if any(point_in(p, b) for p in a) or any(point_in(p, a) for p in b):
        return 0
    return min(segments_distance(p, q, r, s)
               for p, q in zip(a, a[1:] + a[:1])
               for r, s in zip(b, b[1:] + b[:1]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    manifest_path = args.export / "export-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    floor_path = QA / "props-independent/source-floor-heights.json"
    floors = json.loads(floor_path.read_text())["surfaces"]
    meta_path = ROOT / "GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json"
    rooms = {r["zone"]: r["polygon_xz"] for r in json.loads(meta_path.read_text())["rooms"]}
    empty = {z: rooms[z] for z in manifest["people_manifest"]["emptyZones"]}
    records, privacy = [], []
    verified_hashes = 0
    for snapshot in manifest["snapshots"]:
        for item in snapshot["actors"]:
            path = args.export / item["file"]
            if sha(path) != item["sha256"]:
                raise RuntimeError("Export checksum changed: " + str(path))
            verified_hashes += 1
            with gzip.open(path, "rt") as stream:
                actor = json.load(stream)
            all_vertices, shoes = [], []
            for mesh in actor["meshes"]:
                if not mesh["effectivelyVisible"]:
                    raise RuntimeError("Unexpected hidden mesh in export")
                vertices = np.array(mesh["vertices"], dtype=np.float64)[np.unique(mesh["indices"])]
                all_vertices.append(vertices)
                if "shoe" in mesh["name"].lower():
                    shoes.append(vertices)
            all_vertices = np.concatenate(all_vertices)
            if not shoes:
                raise RuntimeError("No visible shoe mesh: " + actor["id"])
            shoes = np.concatenate(shoes)
            heights = np.full(len(shoes), -np.inf)
            sources = np.full(len(shoes), -1, dtype=np.int32)
            for i, floor in enumerate(floors):
                mask = inside(shoes[:, [0, 2]], floor["polygon_xz_m"]) & (floor["topY"] > heights)
                heights[mask], sources[mask] = floor["topY"], i
            if not np.all(np.isfinite(heights)):
                raise RuntimeError("Shoe outside measured floor footprints: " + actor["id"])
            clearance = shoes[:, 1] - heights
            minimum = int(np.argmin(clearance))
            feet = {}
            left = np.array(actor["bones"]["foot_L"])
            right = np.array(actor["bones"]["foot_R"])
            left_mask = np.linalg.norm(shoes - left, axis=1) <= np.linalg.norm(shoes - right, axis=1)
            for side, mask in [("left", left_mask), ("right", ~left_mask)]:
                feet[side] = {"minimum_clearance_m": float(np.min(clearance[mask])), "referenced_vertices": int(np.sum(mask))}
            definition = actor["definition"]
            records.append({
                "id": actor["id"], "seconds": snapshot["seconds"], "zone": definition["zone"],
                "outfit": definition["outfit"], "pose": definition["pose"], "task": definition["task"],
                "seated": bool(definition.get("seated")), "walking": bool(definition.get("path")),
                "minimum_clearance_m": float(clearance[minimum]),
                "deepest_point_xyz": shoes[minimum].tolist(), "support_source": floors[sources[minimum]]["source_object"],
                "support_top_y_m": float(heights[minimum]),
                "shoe_vertices_below_surface_by_more_than_2mm": int(np.sum(clearance < -.002)),
                "feet": feet, "penetration_check_passed": bool(clearance[minimum] >= -.002),
                "standing_or_seated_grounded_check_passed": None if definition.get("path") else all(abs(f["minimum_clearance_m"]) <= .01 for f in feet.values()),
            })
            actor_hull = hull(all_vertices[:, [0, 2]])
            distances = {zone: polygon_distance(actor_hull, polygon) for zone, polygon in empty.items()}
            privacy.append({"id": actor["id"], "seconds": snapshot["seconds"],
                            "visible_mesh_count": len(actor["meshes"]), "hull_vertex_count": len(actor_hull),
                            "minimum_hull_to_empty_zone_m": min(distances.values()),
                            "closest_empty_zone": min(distances, key=distances.get),
                            "hull_separated_from_all_empty_zones": all(d > 1e-9 for d in distances.values())})
    per_actor = []
    for identity in sorted({r["id"] for r in records}):
        rows = [r for r in records if r["id"] == identity]
        worst = min(rows, key=lambda r: r["minimum_clearance_m"])
        per_actor.append({k: worst[k] for k in ["id", "zone", "outfit", "pose", "seated", "walking", "seconds", "minimum_clearance_m", "support_source", "deepest_point_xyz"]})
    result = {
        "status": "failed" if any(not r["penetration_check_passed"] for r in records) else "sampled-floor-pass",
        "scope": "Actual runtime-deformed visible LOD0 shoe vertices against measured source horizontal finish/rug tops; all visible mesh projected hulls against eight empty-zone polygons.",
        "source_hashes": {str(manifest_path): sha(manifest_path), str(floor_path.relative_to(ROOT)): sha(floor_path), str(meta_path.relative_to(ROOT)): sha(meta_path)},
        "loaded_people_source_hashes": manifest["sources"],
        "verified_export_files": verified_hashes, "actor_count": len(per_actor),
        "floor_snapshot_passed": sum(r["penetration_check_passed"] for r in records), "floor_snapshot_total": len(records),
        "actors_with_penetration_more_than_2mm": sum(r["minimum_clearance_m"] < -.002 for r in per_actor),
        "maximum_floor_penetration_m": max(0, -min(r["minimum_clearance_m"] for r in records)),
        "empty_zone_hull_passed": sum(r["hull_separated_from_all_empty_zones"] for r in privacy),
        "empty_zone_hull_total": len(privacy), "per_actor_worst": per_actor,
        "floor_snapshots": records, "empty_zone_snapshots": privacy,
        "limitations": [
            "Finite actual animation snapshots, not proof of every time in a continuous animation cycle.",
            "Rug tops use source rectangular footprints; no failure located near a rug border should be accepted without exact triangle follow-up.",
            "Used shoe vertices can demonstrate penetration; no all-mesh floor collision or physiological gait certification is claimed.",
            "Empty-zone convex hull separation is conservative and covers every displayed triangle at each exported time, including hand props, but does not alone cover every time or every path location.",
            "Furniture, hair/eye intersections, rendered realism and mutual visitor/actor interaction remain separate reviews.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(json.dumps({k: result[k] for k in ["status", "verified_export_files", "actor_count", "floor_snapshot_passed", "floor_snapshot_total", "actors_with_penetration_more_than_2mm", "maximum_floor_penetration_m", "empty_zone_hull_passed", "empty_zone_hull_total"]}))


if __name__ == "__main__":
    main()
