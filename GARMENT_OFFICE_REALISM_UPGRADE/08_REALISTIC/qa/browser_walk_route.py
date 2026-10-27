"""Replay the saved route through the actual browser movement controller.

One initial verified spawn is allowed. Every later position comes from the
viewer's real acceleration/substep/collision function, never a teleport.
This is automated controller evidence, not a manual walk or a Mac FPS test.
"""
import argparse
import gzip
import hashlib
import json
import os
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

QA = Path(__file__).parent
ROOT = QA.parents[2]


def launch(playwright, name):
    if name == "firefox":
        return playwright.firefox.launch(
            executable_path="/workspace/tools/playwright/firefox-1538/firefox/firefox", headless=False, timeout=30000,
            env={**os.environ, "DISPLAY": ":88", "LD_LIBRARY_PATH": "/workspace/tools/browser-libs/usr/lib/x86_64-linux-gnu", "LIBGL_ALWAYS_SOFTWARE": "1", "MOZ_DISABLE_CONTENT_SANDBOX": "1", "MOZ_DISABLE_RDD_SANDBOX": "1", "MOZ_DISABLE_GPU_SANDBOX": "1", "XDG_CACHE_HOME": "/tmp/office-firefox-cache", "XDG_CONFIG_HOME": "/tmp/office-firefox-config"},
            firefox_user_prefs={"security.sandbox.content.level": 0, "gfx.webrender.software": True, "webgl.force-enabled": True},
        )
    if name == "webkit":
        return playwright.webkit.launch(
            executable_path="/workspace/tools/playwright/webkit-with-local-libs.sh", headless=True, timeout=30000,
            env={**os.environ, "LIBGL_ALWAYS_SOFTWARE": "1", "WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS": "1", "XDG_CACHE_HOME": "/tmp/office-webkit-cache", "XDG_CONFIG_HOME": "/tmp/office-webkit-config"},
        )
    return playwright.chromium.launch(executable_path="/usr/bin/chromium", headless=True, args=["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8783/realistic/?stage=5&welcome=0&ao=0&shadows=0&scale=0.25")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], default="chromium")
    parser.add_argument("--people", choices=["unchanged", "on", "off"], default="unchanged")
    parser.add_argument("--screenshots", action="store_true", help="Render the reached room endpoints; never substitutes reference cameras.")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    witness_file = QA / "walk-route-witness.json"
    witness = json.loads(witness_file.read_text())
    report = {
        "status": "running", "url": args.url, "browser_requested": args.browser, "people_requested": args.people,
        "route_sha256": hashlib.sha256(witness_file.read_bytes()).hexdigest(), "route_m": witness["total_route_m"],
        "scope": "One initial verified spawn, then actual browser movement-controller steps. No intermediate camera-position assignment. Real rendering only at requested checkpoints.",
        "limitations": ["Automated proportional movement inputs, not a manual keyboard/mouse walkthrough.", "Linux software rendering, not MacBook FPS, hardware, Safari or accessibility evidence.", "Inherited raster radius is 0.15m; this is not a human-body clearance certification.", "No new atlas or visual-quality pass is inferred from movement checks."],
        "legs": [], "console_errors": [], "page_errors": [], "source_responses": [],
    }

    def save():
        (output / "walk-report.json").write_text(json.dumps(report, indent=2))

    with sync_playwright() as playwright:
        browser = launch(playwright, args.browser)
        context = browser.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        page = context.new_page()
        page.on("pageerror", lambda error: report["page_errors"].append(str(error)))
        page.on("console", lambda msg: report["console_errors"].append(msg.text) if msg.type == "error" else None)

        def record_response(response):
            filename = urlparse(response.url).path.rsplit("/", 1)[-1]
            if response.request.resource_type == "document" or filename in ["app.js", "manifest.json", "people-layer.js", "people-manifest.json", "poses.json"]:
                try:
                    body = response.body()
                    report["source_responses"].append({"url": response.url, "status": response.status, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
                except Exception as error:
                    report.setdefault("source_capture_errors", []).append(str(error))
        page.on("response", record_response)
        started = time.monotonic()
        try:
            page.goto(args.url, wait_until="domcontentloaded", timeout=240000)
            page.wait_for_function("window.__viewer?.ready && typeof __viewer.api?.setWalkQAStart === 'function' && typeof __viewer.api?.stepWalkQA === 'function'", timeout=600000)
            report["ready_seconds_local"] = round(time.monotonic() - started, 3)
            report["browser_version"] = browser.version
            report["gpu"] = page.evaluate("__viewer.api.gpuInfo()")
            if args.browser == "webkit":
                report["gpu_caveat"] = "Playwright WebKit on Debian with software GL. Privacy-masked Apple GPU renderer strings are not evidence of Apple hardware or macOS Safari."
            if args.people != "unchanged":
                page.evaluate("""async enabled => {
                    if (!__viewer.api.setPeopleEnabled || !__viewer.api.peopleStats) throw new Error('People state APIs are required for an occupied-state claim');
                    await __viewer.api.setPeopleEnabled(enabled);
                    const state=__viewer.api.peopleStats();
                    if(state.enabled!==enabled || (enabled && (!state.loaded || state.total<25)))throw new Error('People assets/count are not ready for requested walk');
                }""", args.people == "on")
            report["people_initial"] = page.evaluate("__viewer.api.peopleStats?.() || null")
            report["preflight"] = page.evaluate("""witness => {
                const bad = [];
                for (const leg of witness.legs) for (let i = 0; i < leg.points_xz.length; i++) {
                    const [x,z] = leg.points_xz[i];
                    if (__viewer.api.blocked(x,z)) bad.push({from:leg.from,to:leg.to,index:i,x,z});
                }
                return {blockedPoints:bad.length,firstBlocked:bad.slice(0,20)};
            }""", witness)
            first = witness["waypoints"][0]["xz"]
            report["initial_spawn"] = page.evaluate("p => __viewer.api.setWalkQAStart(p[0],p[1])", first)
            report["spawn_assignments"] = 1
            for leg_index, leg in enumerate(witness["legs"]):
                result = page.evaluate("""leg => {
                    const api = __viewer.api, dt = 1/60, trace = [];
                    const result = {from:leg.from,to:leg.to,requestedMetres:leg.length_m,goalsReached:0,inputs:0,trace,failures:[],maxStepMetres:0,maxEyeError:0};
                    let state = api.stepWalkQA({forward:0,strafe:0,yaw:0,dt:0});
                    let elapsed = 0;
                    const record = (next, previous) => {
                        const [x,y,z]=next.position, p=previous.position;
                        const movement = Math.hypot(x-p[0],z-p[2]);
                        result.maxStepMetres = Math.max(result.maxStepMetres,movement);
                        result.maxEyeError = Math.max(result.maxEyeError,Math.abs(y-1.6));
                        if (next.startCount !== 1) result.failures.push({reason:'unexpected extra spawn',state:next});
                        if (next.blocked || api.blocked(x,z)) result.failures.push({reason:'endpoint in collision',state:next});
                        if (Math.abs(y-1.6)>1e-9) result.failures.push({reason:'eye-height drift',state:next});
                        if (movement > 1.4*dt + 1e-6) result.failures.push({reason:'movement exceeds configured walking speed',movement});
                        const count = Math.max(1,Math.ceil(movement/.005));
                        for (let j=1;j<=count;j++) {
                            const f=j/count;
                            if (api.blocked(p[0]+f*(x-p[0]),p[2]+f*(z-p[2]))) {
                                result.failures.push({reason:'conservative between-step chord touches blocked space',point:[p[0]+f*(x-p[0]),p[2]+f*(z-p[2])]}); break;
                            }
                        }
                        trace.push({t:elapsed,position:next.position,velocity:next.velocity,collisions:next.collisions,room:next.room});
                    };
                    for (let i=1;i<leg.points_xz.length;i++) {
                        const target=leg.points_xz[i];
                        let stuck=0, reached=false;
                        for (let attempt=0;attempt<600;attempt++) {
                            const dx=target[0]-state.position[0],dz=target[1]-state.position[2],distance=Math.hypot(dx,dz);
                            if(distance<.012){reached=true;break;}
                            const yaw=Math.atan2(-dx,-dz),forward=Math.min(1,distance*5);
                            const previous=state;
                            state=api.stepWalkQA({forward,strafe:0,yaw,dt,fast:false});
                            elapsed+=dt;result.inputs++;
                            record(state,previous);
                            if(result.failures.length)break;
                            const movement=Math.hypot(state.position[0]-previous.position[0],state.position[2]-previous.position[2]);
                            stuck=movement<1e-6?stuck+1:0;
                            if(stuck>=240){result.failures.push({reason:'movement blocked for four simulated seconds',target,position:state.position,collisions:state.collisions});break;}
                        }
                        if(!reached&&!result.failures.length)result.failures.push({reason:'controller failed to converge on route point',index:i,target,position:state.position});
                        if(result.failures.length)break;
                        result.goalsReached++;
                    }
                    result.finalState=state;result.simulatedSeconds=elapsed;
                    result.passed=result.failures.length===0 && result.goalsReached===leg.points_xz.length-1 && state.room===leg.to;
                    if(!result.passed&&!result.failures.length)result.failures.push({reason:'wrong final room',expected:leg.to,actual:state.room});
                    return result;
                }""", leg)
                trace = result.pop("trace")
                trace_name = f"trace-{leg_index + 1:02d}-{leg['from']}-{leg['to']}.json.gz"
                with gzip.open(output / trace_name, "wt") as stream:
                    json.dump(trace, stream, separators=(",", ":"))
                result["trace_file"] = trace_name
                result["trace_sha256"] = hashlib.sha256((output / trace_name).read_bytes()).hexdigest()
                report["legs"].append(result)
                save()
                print(json.dumps({k: result[k] for k in ["from", "to", "passed", "goalsReached", "inputs", "failures"]}), flush=True)
                if args.screenshots or not result["passed"]:
                    page.evaluate("() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
                    page.screenshot(path=str(output / f"walk-{leg_index + 1:02d}-{leg['to']}.png"), timeout=300000)
                if not result["passed"]:
                    break
            if len(report["legs"]) == len(witness["legs"]) and all(leg["passed"] for leg in report["legs"]):
                report["release_and_collision_probe"] = page.evaluate("""() => {
                    const api=__viewer.api,dt=1/60;
                    const initial=api.stepWalkQA({forward:0,strafe:0,yaw:0,dt:0});
                    const start=initial.position.slice();
                    let state=initial,blockedSamples=0,maxEyeError=0;
                    for(let i=0;i<90;i++){
                        state=api.stepWalkQA({forward:0,strafe:0,yaw:0,dt});
                        if(state.blocked)blockedSamples++;
                        maxEyeError=Math.max(maxEyeError,Math.abs(state.position[1]-1.6));
                    }
                    const release={initialVelocity:initial.velocity,finalVelocity:state.velocity,coastMetres:Math.hypot(state.position[0]-start[0],state.position[2]-start[2]),simulatedSeconds:1.5};
                    release.passed=Math.hypot(...state.velocity)<.001 && blockedSamples===0 && maxEyeError<1e-9;
                    const origin=state.position.slice(),directions=[[1,0],[-1,0],[0,1],[0,-1]];
                    const obstacles=[];
                    for(const [dx,dz] of directions)for(let d=.02;d<=2;d+=.02){
                        if(api.blocked(origin[0]+dx*d,origin[2]+dz*d)){if(d>=.12)obstacles.push({dx,dz,d,x:origin[0]+dx*d,z:origin[2]+dz*d});break;}
                    }
                    obstacles.sort((a,b)=>a.d-b.d);
                    if(!obstacles.length)return {release,obstacle:{passed:false,reason:'No suitable nearby blocked probe found'},passed:false};
                    const obstacle=obstacles[0],yaw=Math.atan2(-obstacle.dx,-obstacle.dz),beforeCollisions=state.collisions;
                    for(let i=0;i<180;i++){
                        state=api.stepWalkQA({forward:1,strafe:0,yaw,dt});
                        if(state.blocked)blockedSamples++;
                        maxEyeError=Math.max(maxEyeError,Math.abs(state.position[1]-1.6));
                    }
                    const travelled=Math.hypot(state.position[0]-origin[0],state.position[2]-origin[2]);
                    const probe={target:obstacle,travelledMetres:travelled,requestedUnobstructedMetres:4.2,collisionsAdded:state.collisions-beforeCollisions,position:state.position,blockedSamples,maxEyeError,scope:'Nearest actual grid/floor blocker; not an exhaustive fixture collision proof.'};
                    probe.passed=state.collisions>beforeCollisions && !state.blocked && blockedSamples===0 && travelled<obstacle.d+.03 && maxEyeError<1e-9 && state.startCount===1;
                    for(let i=0;i<90;i++)state=api.stepWalkQA({forward:0,strafe:0,yaw,dt});
                    return {release,obstacle:probe,finalState:state,passed:release.passed&&probe.passed};
                }""")
            report["final_state"] = page.evaluate("({walk:__viewer.api.walkState(),viewer:__viewer.api.state(),people:__viewer.api.peopleStats?.()||null,viewer_errors:__viewer.errors||[]})")
            report["status"] = "passed" if len(report["legs"]) == len(witness["legs"]) and all(leg["passed"] for leg in report["legs"]) and report.get("release_and_collision_probe", {}).get("passed") and not report["page_errors"] and not report["console_errors"] else "failed"
        except Exception as error:
            report["status"] = "failed"
            report["exception"] = str(error)
            raise
        finally:
            report["wall_seconds"] = round(time.monotonic() - started, 3)
            save()
            browser.close()
    print(json.dumps({"status":report["status"],"completed_legs":sum(leg["passed"] for leg in report["legs"]),"total_legs":len(witness["legs"]),"output":str(output)}))
    if report["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
