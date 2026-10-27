"""Actual browser input smoke: UI entry, physical key events, mouse and Escape.

Complements the long controller replay; it never uses the QA spawn/step hooks.
"""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from browser_walk_route import launch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8783/realistic/?stage=5&welcome=0&ao=0&shadows=0&post=0&materials=0&probes=0&scale=0.25")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], default="chromium")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {"status": "running", "url": args.url, "checks": [], "page_errors": [], "console_errors": [], "source_responses": [], "scope": "Real UI click, keyboard and mouse events; no QA movement or spawn hook invoked. Linux software rendering; no FPS or Mac hardware claim."}

    def save():
        (output / "controls-report.json").write_text(json.dumps(report, indent=2))

    def check(name, passed, detail=None):
        report["checks"].append({"name": name, "passed": bool(passed), "detail": detail})
        save()

    with sync_playwright() as playwright:
        browser = launch(playwright, args.browser)
        page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        page.on("pageerror", lambda error: report["page_errors"].append(str(error)))
        page.on("console", lambda msg: report["console_errors"].append(msg.text) if msg.type == "error" else None)

        def response_seen(response):
            name = urlparse(response.url).path.rsplit("/", 1)[-1]
            if response.request.resource_type == "document" or name == "app.js":
                body = response.body()
                report["source_responses"].append({"url": response.url, "status": response.status, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
        page.on("response", response_seen)
        started = time.monotonic()
        try:
            page.goto(args.url, wait_until="domcontentloaded", timeout=240000)
            page.wait_for_function("window.__viewer?.ready && typeof __viewer.api?.lookState === 'function'", timeout=600000)
            report["browser"] = browser.version
            report["gpu"] = page.evaluate("__viewer.api.gpuInfo()")
            report["render_state"] = page.evaluate("__viewer.api.renderStats()")
            if args.browser == "webkit":
                report["gpu_caveat"] = "Playwright WebKit on Debian software GL, not native macOS Safari. Apple GPU renderer name is privacy-masked."
            page.click("#mWalk", timeout=120000)
            page.wait_for_function("__viewer.api.state().mode === 'walk' && !__viewer.api.state().flying", timeout=300000)
            initial = page.evaluate("({viewer:__viewer.api.state(),walk:__viewer.api.walkState(),look:__viewer.api.lookState(),blocked:__viewer.api.blocked(...[__viewer.api.state().pos[0],__viewer.api.state().pos[2]])})")
            report["initial"] = initial
            check("normal UI entry spawns on free floor", not initial["blocked"], initial["walk"]["position"])
            check("normal walk eye height is 1.60m", abs(initial["walk"]["position"][1] - 1.6) < 1e-9)
            origin = initial["walk"]["position"]
            moved = False
            page.keyboard.down("KeyW")
            try:
                page.wait_for_function("p => {const n=__viewer.api.walkState().position;return Math.hypot(n[0]-p[0],n[2]-p[2])>.35}", arg=origin, timeout=120000)
                moved = True
            finally:
                page.keyboard.up("KeyW")
            page.wait_for_function("Math.hypot(...__viewer.api.walkState().velocity)<.003", timeout=120000)
            after_key = page.evaluate("({walk:__viewer.api.walkState(),viewer:__viewer.api.state(),blocked:__viewer.api.blocked(__viewer.api.walkState().position[0],__viewer.api.walkState().position[2])})")
            check("real W key moves forward", moved, {"from": origin, "to": after_key["walk"]["position"]})
            check("key release brakes to rest on free floor", not after_key["blocked"] and sum(v*v for v in after_key["walk"]["velocity"]) < .003**2, after_key["walk"])
            before_look = page.evaluate("__viewer.api.lookState()")
            page.mouse.click(640, 340)
            page.wait_for_timeout(300)
            locked = page.evaluate("__viewer.api.lookState().pointerLocked")
            report["pointer_lock_acquired"] = locked
            if locked:
                page.mouse.move(700, 370, steps=3)
            else:
                page.mouse.move(640, 340)
                page.mouse.down()
                page.mouse.move(700, 370, steps=3)
                page.mouse.up()
            page.wait_for_function("p => {const n=__viewer.api.lookState();return Math.abs(n.yaw-p.yaw)+Math.abs(n.pitch-p.pitch)>.02}", arg=before_look, timeout=30000)
            after_look = page.evaluate("__viewer.api.lookState()")
            check("real mouse changes first-person look", abs(after_look["yaw"] - before_look["yaw"]) + abs(after_look["pitch"] - before_look["pitch"]) > .02, {"before": before_look, "after": after_look, "input_mode": "pointer lock" if locked else "drag fallback"})
            page.keyboard.press("Escape")
            page.wait_for_timeout(600)
            escaped = page.evaluate("({viewer:__viewer.api.state(),look:__viewer.api.lookState()})")
            check("one Escape leaves walking and releases mouse", escaped["viewer"]["mode"] == "overview" and not escaped["look"]["pointerLocked"], escaped)
            check("no QA spawn used", page.evaluate("!__viewer.qaStartCount"))
            report["status"] = "passed" if all(c["passed"] for c in report["checks"]) and not report["page_errors"] and not report["console_errors"] else "failed"
        except Exception as error:
            report["status"] = "failed"
            report["exception"] = str(error)
            raise
        finally:
            report["wall_seconds"] = round(time.monotonic() - started, 3)
            save()
            browser.close()
    print(json.dumps({"status": report["status"], "checks": report["checks"], "errors": report["page_errors"] + report["console_errors"]}), flush=True)
    if report["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
