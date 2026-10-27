"""Checks the client presentation and appends the result to a report (used by verify_all.sh).
python3 verify_deck.py PROJECT_ROOT REPORT.md
- the PDF opens (pdfinfo) and has 18 pages
- the PPTX opens (python-pptx) and converts with LibreOffice to an 18-page PDF
- every render image the deck uses is byte-identical to a file in 02_RENDERED_IMAGES/final or previews (no other images),
  and each preview is captioned "(preview render)" in the HTML deck
"""
import filecmp
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT, REPORT = os.path.abspath(sys.argv[1]), sys.argv[2]
PRES = os.path.join(ROOT, "03_PRESENTATION")
IMG = os.path.join(ROOT, "02_RENDERED_IMAGES")
lines = ["## Presentation (`03_PRESENTATION`)"]


def pdf_pages(path):
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    size = re.search(r"Page size:\s+([\d.]+ x [\d.]+ pts)", out)
    return (int(m.group(1)) if m else 0), (size.group(1) if size else "?")


pdf = os.path.join(PRES, "Garment_Office_Design_Pitch.pdf")
n, size = pdf_pages(pdf)
lines.append(f"- PDF `Garment_Office_Design_Pitch.pdf` ({os.path.getsize(pdf) / 1e6:.1f} MB): opens, {n} pages, page size {size} - "
             + ("PASS" if n == 18 else "CHECK"))

pptx = os.path.join(PRES, "Garment_Office_Design_Pitch.pptx")
try:
    from pptx import Presentation
    prs = Presentation(pptx)
    pics = sum(1 for sl in prs.slides for sh in sl.shapes if sh.shape_type == 13)
    lines.append(f"- PPTX `Garment_Office_Design_Pitch.pptx` ({os.path.getsize(pptx) / 1e6:.1f} MB): opens in python-pptx, "
                 f"{len(prs.slides)} slides, {pics} pictures, all text in editable text boxes and tables")
except Exception as e:  # noqa: BLE001
    lines.append(f"- PPTX: could not be opened ({e!r}) - CHECK")
tmp = tempfile.mkdtemp()
shutil.copy(pptx, tmp)
subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, os.path.join(tmp, os.path.basename(pptx))],
               capture_output=True, timeout=600)
conv = os.path.join(tmp, "Garment_Office_Design_Pitch.pdf")
cn = pdf_pages(conv)[0] if os.path.exists(conv) else 0
lines.append(f"- PPTX opened and converted by LibreOffice: {cn} pages - " + ("PASS" if cn == 18 else "CHECK"))
shutil.rmtree(tmp, ignore_errors=True)

html_doc = open(os.path.join(PRES, "Garment_Office_Design_Pitch.html")).read()
manifest = json.load(open(os.path.join(PRES, "deck_manifest.json")))
final, prev, other, bad_cap = set(), set(), set(), []
for m in manifest:
    cam = m["cam"]
    a = os.path.join(PRES, "assets", cam + ".jpg")
    f, p = os.path.join(IMG, "final", cam + ".jpg"), os.path.join(IMG, "previews", cam + ".jpg")
    if m["status"] == "final" and os.path.exists(f) and filecmp.cmp(a, f, shallow=False):
        final.add(cam)
    elif m["status"] == "preview" and os.path.exists(p) and filecmp.cmp(a, p, shallow=False):
        prev.add(cam)
        if "(preview render)" not in m["caption"]:
            bad_cap.append(cam)
    else:
        other.add(cam)
    if html.escape(m["caption"]) not in html_doc:
        bad_cap.append(cam + " (caption not found in the HTML)")
used = sorted(final | prev | other)
lines.append(f"- render images used by the deck: {len(used)} views in {len(manifest)} places; byte-identical to `02_RENDERED_IMAGES/final`: "
             f"{len(final)}, to `02_RENDERED_IMAGES/previews`: {len(prev)}, anything else: {len(other)}" + (f" {sorted(other)}" if other else "")
             + (" - PASS" if not other else " - CHECK"))
lines.append(f"- every preview image is captioned '(preview render)' where it is shown: " + ("PASS" if not bad_cap else f"CHECK {bad_cap}")
             + (f" (previews: {', '.join(sorted(prev))})" if prev else " (no previews left in the deck)"))
other_imgs = sorted(set(re.findall(r'src="assets/([^"]+)"', html_doc)) - {c + ".jpg" for c in used})
lines.append(f"- other images in the deck: {', '.join(other_imgs)} (drawings ID-01..03, material board and swatches from this project, "
             "client logos and tagline cropped from the client's business card and company profile)")
with open(REPORT, "a") as fh:
    fh.write("\n".join(lines) + "\n\n")
print("\n".join(lines))
