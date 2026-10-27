"""Capture actual phase viewer frames through its documented review API.

This never fabricates an after image and never silently accepts a missing atlas
when --require-lightmaps is set. Run only after the relevant assets are ready.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
QA = Path(__file__).parent
KEYS = [
    "CAM_01_Reception_A", "CAM_04_Experience_Centre_A", "CAM_09_Boardroom_A",
    "CAM_07_MD_Office_A", "CAM_11_Merchandising_A", "CAM_13_Design_Studio_A",
]
HIDE = """#top,#side,#sideOpen,#info,#viewbar,#tourbar,#disclaimer,#labels,
#minimap,#walkhint,#pad,#dock,#welcome,#dissolve,#photo{display:none!important}"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8783/realistic/?welcome=0&ao=0&shadows=0")
    parser.add_argument("--phase", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cameras", choices=["key", "all"], default="key")
    parser.add_argument("--camera", action="append", help="Capture this named camera only; repeat for several.")
    parser.add_argument("--require-lightmaps", action="store_true")
    parser.add_argument("--people", choices=["on", "off", "unchanged"], default="unchanged")
    parser.add_argument("--expected-people", type=int, help="Exact count required for a bounded occupied capture, e.g.4 for the Reception release.")
    args = parser.parse_args()
    output = args.output.resolve()
    shots = output / "shots"
    shots.mkdir(parents=True, exist_ok=True)
    meta = json.loads((QA.parent / "revised-model/office_web_metadata.json").read_text())
    cameras = meta["cameras"] if args.cameras == "all" else [next(c for c in meta["cameras"] if c["name"] == name) for name in KEYS]
    if args.camera:
        cameras = [next(c for c in meta["cameras"] if c["name"] == name) for name in args.camera]
    report = {
        "phase": args.phase, "url": args.url, "viewport": [1280, 720],
        "people_requested": args.people, "require_lightmaps": args.require_lightmaps,
        "shots": [], "console_errors": [], "page_errors": [], "http_errors": [],
        "source_responses": [], "source_response_method": "Actual browser navigation/asset response bodies, not a later refetch", "status": "running",
        "scope": "Actual viewer frames; UI hidden through screenshot-only CSS. Original scene camera API, no synthetic edits.",
        "limits": ["Linux software-GPU capture, not a MacBook performance test", "Local load timing is not a 50 Mbps WAN benchmark"],
    }

    def save():
        (output / "capture.json").write_text(json.dumps(report, indent=2))

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/usr/bin/chromium", headless=True,
            args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"],
        )
        context = browser.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        page = context.new_page()
        page.on("pageerror", lambda error: report["page_errors"].append(str(error)))
        page.on("console", lambda msg: report["console_errors"].append(msg.text) if msg.type == "error" else None)
        def record_response(response):
            if response.status >= 400:
                report["http_errors"].append({"url": response.url, "status": response.status})
            filename = urlparse(response.url).path.rsplit("/", 1)[-1]
            if response.request.resource_type == "document" or filename in ["app.js", "manifest.json"]:
                try:
                    body = response.body()
                    report["source_responses"].append({"url": response.url, "status": response.status, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
                    if filename == "manifest.json" and "/lighting/" in response.url and response.status == 200:
                        (output / "lighting-manifest.json").write_bytes(body)
                except Exception as error:
                    report.setdefault("source_capture_errors", []).append({"url": response.url, "error": str(error)})
        page.on("response", record_response)
        started = time.monotonic()
        try:
            page.goto(args.url, wait_until="domcontentloaded", timeout=240000)
            page.wait_for_function("window.__viewer?.ready && typeof window.__viewer.api?.frameCamera === 'function'", timeout=600000)
            report["ready_seconds_local"] = round(time.monotonic() - started, 3)
            report["browser"] = browser.version
            report["gpu"] = page.evaluate("""() => {
                if (__viewer.api.gpuInfo) return __viewer.api.gpuInfo();
                const gl = document.querySelector('canvas').getContext('webgl2');
                const debug = gl?.getExtension('WEBGL_debug_renderer_info');
                return gl ? {version: gl.getParameter(gl.VERSION), renderer: gl.getParameter(debug ? debug.UNMASKED_RENDERER_WEBGL : gl.RENDERER), vendor: gl.getParameter(debug ? debug.UNMASKED_VENDOR_WEBGL : gl.VENDOR)} : {unavailable: true};
            }""")
            report["counts"] = page.evaluate("__viewer.counts")
            if args.people != "unchanged":
                page.evaluate("""async ({enabled,expected}) => {
                    if (!__viewer.api.setPeopleEnabled || !__viewer.api.peopleStats) throw new Error('People capture requires setPeopleEnabled and peopleStats APIs');
                    await __viewer.api.setPeopleEnabled(enabled);
                    const state=__viewer.api.peopleStats();
                    if(state.enabled!==enabled || (enabled && (!state.loaded || state.total<1 || (expected!==null && state.total!==expected))))throw new Error('People assets/count are not ready for requested capture');
                }""", {"enabled": args.people == "on", "expected": args.expected_people})
            page.add_style_tag(content=HIDE)
            for camera in cameras:
                result = page.evaluate("name => __viewer.api.frameCamera(name)", camera["name"])
                if args.require_lightmaps and (result.get("lighting") or {}).get("state") != "loaded":
                    raise RuntimeError(f"Refusing unbaked after capture for {camera['name']}: {result.get('lighting')}")
                page.evaluate("() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
                state = page.evaluate("""() => ({
                    viewer: __viewer.api.state(), stats: __viewer.api.renderStats(),
                    lighting: __viewer.api.lighting?.(), people: __viewer.api.peopleStats?.() || null,
                    viewer_errors: __viewer.errors || []
                })""")
                if args.require_lightmaps:
                    lighting_state = state.get("lighting") or {}
                    for shared in lighting_state.get("requiredShared", []):
                        if lighting_state.get("rooms", {}).get(shared, {}).get("state") != "loaded":
                            raise RuntimeError(f"Refusing after capture with missing required shared atlas: {shared}")
                if args.people != "unchanged" and state["people"]["enabled"] != (args.people == "on"):
                    raise RuntimeError("People state does not match requested capture state")
                filename = "after_" + camera["name"] + ".png"
                target = shots / filename
                page.screenshot(path=str(target), timeout=300000)
                report["shots"].append({"camera": camera["name"], "type": camera["type"], "frame_result": result, "state": state, "file": "shots/" + filename, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
                save()
                print(camera["name"], result.get("lighting"), flush=True)
            report["status"] = "captured"
        except Exception as error:
            report["status"] = "failed"
            report["failure"] = str(error)
            raise
        finally:
            report["seconds"] = round(time.monotonic() - started, 3)
            save()
            browser.close()
    print(json.dumps({"status": report["status"], "shots": len(report["shots"]), "console_errors": report["console_errors"], "page_errors": report["page_errors"], "http_errors": report["http_errors"]}), flush=True)


if __name__ == "__main__":
    main()
