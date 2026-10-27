"""Lightweight alternate-manifest startup check; no camera/room atlas requested."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from browser_walk_route import launch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--url", default="http://127.0.0.1:8783/realistic/?stage=5&welcome=0&post=0&materials=0&probes=0&scale=0.25&lighting=./lighting-v2/manifest.json")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {"status": "running", "url": args.url, "page_errors": [], "console_errors": [], "responses": [], "scope": "Alternate-manifest startup applies exactly six named fallback repairs. No room-selection, frameCamera or atlas-loading API invoked. Not a new controller or visual acceptance."}
    with sync_playwright() as p:
        browser = launch(p, "chromium")
        page = browser.new_page(viewport={"width": 640, "height": 360})
        page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
        page.on("console", lambda m: report["console_errors"].append(m.text) if m.type == "error" else None)
        def response(r):
            name = urlparse(r.url).path.rsplit("/", 1)[-1]
            if name in ["app.js", "manifest.json", "doorway-repairs.glb"]:
                body = r.body()
                report["responses"].append({"url": r.url, "status": r.status, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
        page.on("response", response)
        try:
            page.goto(args.url, wait_until="domcontentloaded", timeout=240000)
            page.wait_for_function("window.__viewer?.ready === true", timeout=600000)
            report["state"] = page.evaluate("({repairs:__viewer.repairs,errors:__viewer.errors,lighting:__viewer.api.lighting(),features:__viewer.features,gpu:__viewer.api.gpuInfo()})")
            expected = {"NI01 frame above PW01", "NI03 frame above PW01", "NI04 frame above PW05", "NI07 frame above PW06", "NI08 frame above PW07", "NI10 frame above PW07"}
            repairs = report["state"]["repairs"]
            report["passed"] = repairs["state"] == "applied" and len(repairs["objects"]) == 6 and set(repairs["objects"]) == expected and not report["state"]["errors"] and not report["page_errors"] and not report["console_errors"]
            report["status"] = "passed" if report["passed"] else "failed"
        except Exception as e:
            report["status"], report["exception"] = "failed", str(e)
            raise
        finally:
            args.output.write_text(json.dumps(report, indent=2))
            browser.close()
    print(json.dumps({"status": report["status"], "repairs": report["state"]["repairs"], "errors": report["state"]["errors"]}))
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
