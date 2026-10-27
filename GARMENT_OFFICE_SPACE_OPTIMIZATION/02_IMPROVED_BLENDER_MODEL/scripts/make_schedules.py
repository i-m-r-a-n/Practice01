"""Room, furniture, material and lighting schedules (CSV + Markdown) from the model data.
python3 make_schedules.py OUT_DIR"""
import csv
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import office_layout as O  # noqa: E402
import survey as S  # noqa: E402

OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
os.makedirs(OUT, exist_ok=True)
SEAT_KEYS = {"bench3": 6, "bench2": 4, "bench_design": 4, "cad_desk": 1, "desk_single": 1, "exec_desk_md": 1, "exec_desk_dir": 1,
             "security_desk": 1, "reception_desk": 2}
FIN = {"fl_terrazzo": "TZ-01 terrazzo-look porcelain / terrazzo tile", "fl_herringbone": "WD-01 oak herringbone",
       "fl_carpet": "CP-01 charcoal carpet tile", "fl_carpet_green": "CP-02 green prayer carpet", "fl_oak_planks": "WD-02 oak-look plank",
       "fl_concrete": "PC-01 sealed light-grey concrete / epoxy", "fl_porcelain": "PT-01 matt porcelain tile"}


def write(name, header, rows, title, intro=""):
    with open(os.path.join(OUT, name + ".csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    with open(os.path.join(OUT, name + ".md"), "w") as f:
        f.write(f"# {title}\n\n{intro}\n\n| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n")
        for r in rows:
            f.write("| " + " | ".join(str(c).replace("\n", " ").replace("|", "/") for c in r) + " |\n")


def rooms():
    per_zone = defaultdict(Counter)
    for key, x, y, facing, zone, z, label in O.PLACEMENTS:
        per_zone[zone][key] += 1
    lights = Counter(l[5] for l in O.LIGHTS)
    rows, tot_area, tot_seats = [], 0, 0
    for coll, zid, label, pts, fin, ceiling in O.ZONES:
        a = S.poly_area_sft(pts)
        tot_area += a
        seats = sum(SEAT_KEYS.get(k, 0) * n for k, n in per_zone[zid].items())
        tot_seats += seats if zid not in ("Z01", "Z02") else 0
        main = ", ".join(f"{n} x {O.ASSETS[k][3].split(',')[0]}" if not k.startswith("cc0:") else f"{n} x {k[4:]} (CC0)"
                         for k, n in per_zone[zid].most_common(4))
        rows.append([zid, label.replace("\n", " - "), coll.replace("_", " "), round(a), round(a * 0.092903, 1), FIN[fin], ceiling,
                     seats or "", lights.get(zid, 0), main])
    rows.append(["", "TOTAL (fit-out zones, net)", "", round(tot_area), round(tot_area * 0.092903, 1), "", "", tot_seats, "", ""])
    write("room_schedule", ["zone", "room / function", "group", "area_sft", "area_m2", "floor finish", "ceiling", "work seats", "light fixtures", "main furniture"],
          rows, "Room schedule", "Areas are net floor areas of the fit-out zones measured from the model polygons (survey dimensions; room 8 width assumed). "
          "Work seats exclude reception/security counters.")
    return tot_seats


def furniture():
    cnt = Counter(p[0] for p in O.PLACEMENTS)
    zones = defaultdict(set)
    for key, x, y, facing, zone, z, label in O.PLACEMENTS:
        zones[key].add(zone)
    rows = []
    for key, n in sorted(cnt.items()):
        if key.startswith("cc0:"):
            rows.append([key[4:], f"{key[4:].replace('_', ' ')} (lounge seating)", n, "model size", "Poly Haven CC0 model", " ".join(sorted(zones[key]))])
            continue
        builder, kw, fp, desc = O.ASSETS[key]
        rows.append([key, desc, n, f"{round(fp[0] * 25.4)} x {round(fp[1] * 25.4)}", "procedural (parametric Blender model)", " ".join(sorted(zones[key]))])
    rows.append(["plants", "Indoor plants on planters (pachira, calathea) + desk succulents", sum(1 for p in O.PLACEMENTS if p[6] and p[6].startswith("PLANT:")),
                 "", "Poly Haven CC0 models", "various"])
    write("furniture_schedule", ["item", "description", "qty", "footprint_mm (w x d)", "3D source", "zones"], rows, "Furniture & equipment schedule",
          "Quantities are counted from the 3D model. Dimensions are typical commercial sizes; final selection by the client "
          "from local suppliers. Prices are not included (no budget data supplied).")


MATERIALS = [
    ("TZ-01", "Floor - visitor zone", "Terrazzo-look porcelain tile 600 x 600 mm (or cast terrazzo), honed, warm beige aggregate, 3 mm joints, R10", "fl_terrazzo", "Terrazzo019M (ambientCG, CC0)"),
    ("WD-01", "Floor - boardroom, executive suite", "Engineered oak herringbone, matt lacquer; lower-cost option: oak-look LVT herringbone", "fl_herringbone", "herringbone_parquet (Poly Haven, CC0)"),
    ("CP-01", "Floor - offices, CAD, audit", "Nylon carpet tile 500 x 500 mm, charcoal, quarter-turn installation", "fl_carpet", "Fabric030 (ambientCG, CC0)"),
    ("CP-02", "Floor - prayer rooms", "Prayer carpet, deep green, row (saf) lines, removable for cleaning", "fl_carpet_green", "Fabric030 tinted"),
    ("WD-02", "Floor - design studio, cafe, lounge", "Oak-look LVT / laminate plank, commercial grade", "fl_oak_planks", "laminate_floor_02 (Poly Haven, CC0)"),
    ("PC-01", "Floor - sample room, 3D lab, library, store", "Existing slab ground and sealed (light grey) or epoxy screed", "fl_concrete", "smooth_concrete_floor (Poly Haven, CC0), recoloured"),
    ("PT-01", "Floor + walls - washrooms, wudu, pantry", "Porcelain tile 600 x 600 mm floor (R11 in wet areas), 300 x 600 mm wall tile, marble look", "fl_porcelain", "Tiles040 (ambientCG, CC0)"),
    ("PA-01", "Walls", "Low-VOC acrylic emulsion, warm white (approx. RAL 9010)", "paint_white", "procedural"),
    ("PA-02", "Accent walls / display backs", "Deep green paint based on the client logo green (#26673D)", "paint_green", "procedural"),
    ("PA-03", "Exposed deck + beams (kept)", "Spray-applied matt warm white over existing steel deck and beams (fire-protection coating to be confirmed)", "steel_painted", "procedural"),
    ("WO-01", "Feature walls, joinery", "White-oak veneered MDF slats about 45 x 25 mm at 75 mm centres on black acoustic felt (fire-retardant)", "oak_slat", "white_oak_veneer (Poly Haven, CC0)"),
    ("WO-02", "Executive furniture, boardroom", "Smoked walnut veneer, matt lacquer", "walnut", "natural_walnut_veneer (Poly Haven, CC0), toned"),
    ("SS-01", "Counter tops", "Quartz / solid surface, terrazzo pattern, 20 mm", "terrazzo_counter", "Terrazzo019M"),
    ("GL-01", "Glass partitions", "12 mm toughened glass in slim matt-black anodised aluminium channels; manifestation bands at about 1000 / 1500 mm", "glass_clear + alu_black", "procedural"),
    ("MT-01", "Frames, legs, handles", "Matt black powder-coated steel / anodised aluminium", "alu_black / metal_black", "procedural"),
    ("MT-02", "Accents", "Brushed brass (rails, halo light, door pulls) - small doses", "brass", "procedural"),
    ("UP-01", "Upholstery", "Commercial woven fabric (sand, grey, brand green, charcoal), heavy-duty rub rating", "fab_*", "Fabric030 (ambientCG, CC0), tinted"),
    ("UP-02", "Executive / boardroom seating", "Black and cognac leather (or PU leather)", "leather_*", "leather_white (Poly Haven, CC0), tinted"),
    ("AC-01", "Acoustic", "PET felt panels / baffles 12 mm, grey + brand green, fire-rated", "felt_green / felt_grey", "Fabric034 (ambientCG, CC0), tinted"),
    ("BR-01", "Branding", "Client logos (from the client's business card / company profile) printed on white solid-surface or acrylic plates", "logo_*", "client artwork"),
]


def materials():
    write("material_schedule", ["code", "application", "specification concept", "Blender material", "texture source / licence"], MATERIALS,
          "Material & finish schedule", "Specification concepts for tendering; final products, fire ratings and colours to be approved with samples. "
          "Texture images in the model are CC0 (public domain) and only represent the finish.")


def lighting():
    groups = defaultdict(lambda: [0, set(), set()])
    for kind, x, y, z, kw, zone in O.LIGHTS:
        key = (kind, kw.get("L", kw.get("r", kw.get("beam", ""))), kw.get("temp", 3500 if kind != "track" else ""))
        g = groups[key]
        g[0] += 1
        g[1].add(zone or "circulation")
        g[2].add(S.DECK_H - 6 if kind == "down" else z)          # downlights sit on the deck (as built in build_model.py)
    desc = {"lin": "Suspended linear LED profile, direct/indirect, opal diffuser, matt black", "halo": "Brass ring (halo) pendant, LED",
            "down": "Surface cylinder downlight, matt black", "spot": "Track spot on 3-circuit track, adjustable, 24-40 deg",
            "track": "3-circuit track fixed to the beam soffit", "pendant_cc0": "Opal dome pendant (cafe)"}
    rows = []
    for (kind, size, temp), (n, zones, zs) in sorted(groups.items(), key=lambda kv: str(kv[0])):
        sz = f"{size} in" if size != "" else ""
        extra = {"lin": f", {sz} long", "halo": f", ring r {sz}", "down": f", wide beam about {size} deg" if size != "" else ", 60-80 deg"}
        rows.append([kind, desc[kind] + extra.get(kind, ""),
                     f"{temp} K" if temp else "", n, " / ".join(f"{z:g}" for z in sorted(zs)), " ".join(sorted(zones))])
    rows += [["AC", "VRF under-ceiling indoor unit (capacity by MEP engineer)", "", len(O.AC_UNITS), "fixed to deck", ""],
             ["SD", "Smoke detector (connect to the existing fire alarm system)", "", len(O.SMOKE_DETECTORS), "deck", ""],
             ["EX", "Exit sign with emergency battery", "", len(O.EXIT_SIGNS), "88 in", ""]]
    write("lighting_schedule", ["type", "description", "CCT", "qty", "mounting height (in AFF, bottom)", "zones"], rows, "Lighting & ceiling equipment schedule",
          "Concept: 4000 K task light in work areas, 3000-3500 K in visitor/executive areas, accent spots on product displays and brand walls. "
          "Lux levels and luminaire photometry to be verified by a lighting/electrical engineer (target about 500 lux on desks, 300 lux circulation).")


if __name__ == "__main__":
    seats = rooms()
    furniture()
    materials()
    lighting()
    print("schedules written; work seats", seats)
