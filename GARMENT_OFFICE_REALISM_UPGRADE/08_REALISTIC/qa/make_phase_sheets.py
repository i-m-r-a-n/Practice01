"""Compose real Cycles / baseline / after captures; never fill absent after frames."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).parent
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path, help="Phase capture directory containing capture.json and shots/")
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    folder = args.capture.resolve()
    report = json.loads((folder / "capture.json").read_text())
    if report["status"] != "captured":
        raise RuntimeError("Refusing to compose an incomplete or failed capture as a completed phase")
    meta = json.loads((ROOT / "GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json").read_text())
    cameras = {c["name"]: c for c in meta["cameras"]}
    destination = folder / "comparisons"
    destination.mkdir(exist_ok=True)
    title_font = ImageFont.truetype(FONT, 28)
    label_font = ImageFont.truetype(FONT, 21)
    foot_font = ImageFont.truetype(FONT, 19)
    metrics = {"phase": report["phase"], "capture_report_sha256": hashlib.sha256((folder / "capture.json").read_bytes()).hexdigest(), "sheets": []}
    sheets = []
    for shot in report["shots"]:
        name = shot["camera"]
        c = cameras[name]
        paths = [ROOT / c["render"]["file"], QA / "baseline/shots" / ("before_" + name + ".png"), folder / shot["file"]]
        for path in paths:
            if not path.exists():
                raise FileNotFoundError(path)
        images = []
        for path in paths:
            fit = ImageOps.contain(Image.open(path).convert("RGB"), (1280, 720), Image.Resampling.LANCZOS)
            image = Image.new("RGB", (1280, 720), (16, 21, 17))
            image.paste(fit, ((1280 - fit.width) // 2, (720 - fit.height) // 2))
            images.append(image)
        sheet = Image.new("RGB", (3904, 860), (244, 245, 246))
        draw = ImageDraw.Draw(sheet)
        draw.text((16, 12), f"{c['room']} | {name}", font=title_font, fill=(25, 35, 45))
        labels = ["Approved Cycles reference", "Current live WebGL — BEFORE", args.label]
        for index, (image, label) in enumerate(zip(images, labels)):
            x = 16 + index * 1296
            draw.text((x, 56), label, font=label_font, fill=(60, 70, 80))
            sheet.paste(image, (x, 96))
        draw.text((16, 827), "Actual Chromium / software-GPU captures. Visual concept review; MacBook performance and native Safari remain untested.", font=foot_font, fill=(70, 80, 90))
        target = destination / (name + ".jpg")
        sheet.save(target, quality=93)
        metrics["sheets"].append({"camera": name, "file": str(target.relative_to(folder)), "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "after_sha256": shot["sha256"]})
        sheets.append(sheet)
    width = 1952
    thumbs = [image.resize((width, 430), Image.Resampling.LANCZOS) for image in sheets]
    contact = Image.new("RGB", (width, 430 * len(thumbs)), (244, 245, 246))
    for index, image in enumerate(thumbs):
        contact.paste(image, (0, index * 430))
    contact.save(folder / "phase-comparison-contact.jpg", quality=91)
    (folder / "comparison-manifest.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps({"sheets": len(sheets), "folder": str(folder)}))


if __name__ == "__main__":
    main()
