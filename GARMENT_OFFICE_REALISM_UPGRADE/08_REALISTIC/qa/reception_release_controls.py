"""Bounded Reception release UI smoke: original controls plus four frozen people."""
import argparse
import hashlib
import json
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from browser_walk_route import launch


def check_walk_controls(page, check):
    """The original touch pad is intentionally absent for a fine pointer."""
    detail = page.evaluate("""() => {
        const inspect = id => {
            const e = document.getElementById(id), style = getComputedStyle(e);
            return {hiddenClass:e.classList.contains('hidden'),display:style.display,visibility:style.visibility};
        };
        return {mode:__viewer.api.state().mode,viewport:[innerWidth,innerHeight],
            coarsePointer:matchMedia('(pointer: coarse)').matches,
            finePointer:matchMedia('(pointer: fine)').matches,pad:inspect('pad'),minimap:inspect('minimap')};
    }""")
    detail["pad"]["visible"] = page.locator("#pad").is_visible()
    detail["minimap"]["visible"] = page.locator("#minimap").is_visible()
    check("original pointer-specific walk pad and desktop minimap behavior",
          detail["mode"] == "walk" and detail["viewport"][0] > 860
          and detail["pad"]["visible"] == detail["coarsePointer"]
          and detail["minimap"]["visible"], detail)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", required=True)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--browser", choices=["chromium", "firefox", "webkit"], default="chromium")
    p.add_argument("--walk-controls-only", action="store_true", help="Rerun only the corrected pointer-specific pad/minimap check.")
    args = p.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {"status": "running", "url": args.url, "checks": [], "sources": [], "page_errors": [], "console_errors": [], "scope": "Reception only: real original UI buttons/search/photo/help/tour start-stop/walk, People on/off, bounded keys. No full-floor tour, native Mac FPS or file:// acceptance."}
    def save():
        (args.output / "controls-report.json").write_text(json.dumps(report, indent=2))
    def check(name, passed, detail=None):
        report["checks"].append({"name": name, "passed": bool(passed), "detail": detail})
        save()
    with sync_playwright() as playwright:
        browser = launch(playwright, args.browser)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
        page.on("console", lambda m: report["console_errors"].append(m.text) if m.type == "error" else None)
        def response(r):
            if r.request.resource_type == "document" or urlparse(r.url).path.rsplit("/", 1)[-1] in ["app.js", "style.css", "people-manifest.json", "poses.json", "manifest.json"]:
                try:
                    body = r.body()
                    report["sources"].append({"url": r.url, "status": r.status, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)})
                except Exception as e:
                    report.setdefault("source_capture_errors", []).append(str(e))
        page.on("response", response)
        started = time.monotonic()
        try:
            page.goto(args.url, wait_until="domcontentloaded", timeout=240000)
            page.wait_for_function("window.__viewer?.ready && __viewer.api.peopleStats().loaded", timeout=600000)
            report["browser"] = browser.version
            report["gpu"] = page.evaluate("__viewer.api.gpuInfo()")
            if args.walk_controls_only:
                report["scope"] = "Reception only: corrected original pointer-specific walk pad/minimap assertion at 1280x720. Previous passing controls are not rerun. No native Mac FPS claim."
                if not page.locator("#side").evaluate("e=>e.classList.contains('open')"):
                    page.click("#mRooms")
                page.fill("#search", "Z02")
                page.click('#roomList .room[data-zone="Z02"]')
                page.wait_for_function("__viewer.api.state().room==='Z02' && !__viewer.api.state().flying", timeout=300000)
                if page.locator("#side").evaluate("e=>e.classList.contains('open')"):
                    page.click("#sideClose")
                page.click("#bWalkHere")
                page.wait_for_function("__viewer.api.state().mode==='walk' && !__viewer.api.state().flying", timeout=300000)
                check_walk_controls(page, check)
                report["viewer_errors"] = page.evaluate("__viewer.errors")
                report["status"] = "passed" if all(c["passed"] for c in report["checks"]) and not report["page_errors"] and not report["console_errors"] and not report["viewer_errors"] else "failed"
                print(json.dumps({"status": report["status"], "checks": len(report["checks"]), "failed": [x for x in report["checks"] if not x["passed"]]}))
                return
            ids = ["mTour", "mOverview", "mRooms", "mWalk", "mHelp", "mFull", "search", "bPhoto", "bWalkHere", "bBack", "vReset", "vIso", "vTop", "vCeil", "vLabels", "tPrev", "tPlay", "tNext", "tPhoto", "tStop", "minimap", "photoClose", "vQuality"]
            present = page.evaluate("ids => ids.filter(id=>!!document.getElementById(id))", ids)
            check("original control elements retained", present == ids, present)
            check("People control visible", page.locator("#mPeople").is_visible())
            if page.evaluate("__viewer.api.peopleStats().enabled"):
                page.click("#mPeople")
            page.wait_for_function("!__viewer.api.peopleStats().enabled")
            check("real People button turns layer off", page.get_attribute("#mPeople", "aria-pressed") == "false")
            page.click("#mPeople")
            page.wait_for_function("__viewer.api.peopleStats().enabled && __viewer.api.peopleStats().total===4")
            check("real People button enables exactly four", page.get_attribute("#mPeople", "aria-pressed") == "true", page.evaluate("__viewer.api.peopleStats()"))
            check("illustrative disclosure is visible", page.locator("#peopleNote").is_visible() and "illustrative" in page.locator("#peopleNote").inner_text().lower())
            if not page.locator("#side").evaluate("e=>e.classList.contains('open')"):
                page.click("#mRooms")
            page.fill("#search", "Z02")
            check("original room search finds Reception only", page.locator("#roomList .room").count() == 1 and page.locator("#roomList .room").get_attribute("data-zone") == "Z02")
            page.click('#roomList .room[data-zone="Z02"]')
            page.wait_for_function("__viewer.api.state().room==='Z02' && !__viewer.api.state().flying", timeout=300000)
            check("actual room-list click reaches Reception", page.evaluate("__viewer.api.state()" )["room"] == "Z02")
            if page.locator("#side").evaluate("e=>e.classList.contains('open')"):
                page.click("#sideClose")
            page.click("#bPhoto")
            page.wait_for_function("__viewer.api.state().photo==='CAM_01_Reception_A' && document.getElementById('photoImg').complete && document.getElementById('photoImg').naturalWidth>0", timeout=120000)
            check("original photo control opens exact Reception Cycles still", True, page.get_attribute("#photoImg", "src"))
            page.click("#photoClose")
            page.wait_for_function("!__viewer.api.state().photo")
            check("Back to3D closes offline Cycles still", True)
            before = page.evaluate("__viewer.api.peopleDiagnostics().map(a=>({id:a.id,position:a.position,bones:a.bones}))")
            page.wait_for_timeout(750)
            after = page.evaluate("__viewer.api.peopleDiagnostics().map(a=>({id:a.id,position:a.position,bones:a.bones}))")
            check("four people remain frozen during normal RAF", len(before) == 4 and before == after)
            page.screenshot(path=str(args.output / "reception-ui.png"), timeout=300000)
            page.click("#mHelp")
            check("original Help dialog opens", page.locator("#welcome").is_visible())
            page.click("#wClose")
            page.click("#mTour")
            page.wait_for_function("!!__viewer.api.state().tour", timeout=120000)
            page.click("#tPlay")
            check("original guided-tour Pause works", page.evaluate("__viewer.api.state().tour.playing") is False)
            page.click("#tStop")
            check("original End tour works", page.evaluate("!__viewer.api.state().tour"))
            # Return to Reception with the existing room-list UI; never test a
            # different room or run the full guided tour in this bounded smoke.
            page.click("#mRooms")
            page.fill("#search", "Z02")
            page.click('#roomList .room[data-zone="Z02"]')
            page.wait_for_function("__viewer.api.state().room==='Z02' && !__viewer.api.state().flying", timeout=300000)
            if page.locator("#side").evaluate("e=>e.classList.contains('open')"):
                page.click("#sideClose")
            page.click("#bWalkHere")
            page.wait_for_function("__viewer.api.state().mode==='walk' && !__viewer.api.state().flying", timeout=300000)
            origin = page.evaluate("__viewer.api.walkState().position")
            check("Walk from here keeps1.6m eye on free floor", abs(origin[1] - 1.6) < 1e-9 and not page.evaluate("p=>__viewer.api.blocked(p[0],p[2])", origin))
            page.keyboard.down("KeyW")
            page.wait_for_timeout(500)
            page.keyboard.up("KeyW")
            page.wait_for_function("Math.hypot(...__viewer.api.walkState().velocity)<.003", timeout=120000)
            movement = page.evaluate("p=>{const n=__viewer.api.walkState().position;return Math.hypot(n[0]-p[0],n[2]-p[2])}", origin)
            check("real W input moves and release brakes", movement > .02, {"distance_m": movement, "state": page.evaluate("__viewer.api.walkState()")})
            check_walk_controls(page, check)
            page.keyboard.press("Escape")
            page.wait_for_function("__viewer.api.state().mode==='overview'", timeout=120000)
            check("Escape returns to overview", True)
            report["software_render_timing"] = page.evaluate("""async () => {
                const samples=[];
                for(let i=0;i<5;i++){const t=performance.now();await __viewer.api.frameCamera('CAM_01_Reception_A');samples.push(performance.now()-t);}
                const sorted=samples.slice().sort((a,b)=>a-b);
                return {samples_ms:samples,median_ms:sorted[2],scope:'Five repeated exact-camera frame requests on Linux software WebGL; includes framing and two RAF waits. This is not display FPS, MacBook performance or WAN loading.',stats:__viewer.api.renderStats()};
            }""")
            report["viewer_errors"] = page.evaluate("__viewer.errors")
            report["gpu_memory_estimate"] = page.evaluate("__viewer.api.gpuMemoryEstimate?.()||null")
            report["status"] = "passed" if all(c["passed"] for c in report["checks"]) and not report["page_errors"] and not report["console_errors"] and not report["viewer_errors"] else "failed"
        except Exception as e:
            report["status"], report["exception"] = "failed", str(e)
            raise
        finally:
            report["wall_seconds"] = round(time.monotonic() - started, 3)
            save()
            browser.close()
    print(json.dumps({"status": report["status"], "checks": len(report["checks"]), "failed": [x for x in report["checks"] if not x["passed"]]}))


if __name__ == "__main__":
    main()
