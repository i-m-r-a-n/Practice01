"""Exercise occupied movement using real viewer substeps, not position animation.

Each scenario gets one fresh page and one verified initial visitor spawn. People
off/on supplies a static-geometry counterfactual; no collision bypass is used.
Requires accepted, integrated People APIs and deliberately fails if unavailable.
"""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from browser_walk_route import launch

QA = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8783/realistic/?stage=5&welcome=0&post=0&materials=0&probes=0&scale=0.25&lighting=./lighting-v2/manifest.json")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], default="chromium")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--scenario", action="append", choices=["stationary_actor", "walking_actor_yields", "enable_occupied_anchor"], help="Run only selected bounded scenarios.")
    parser.add_argument("--expected-people", type=int, default=35)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {"status": "running", "browser": args.browser, "url": args.url, "scenarios": [], "page_errors": [], "console_errors": [], "source_responses": [], "limitations": ["Linux software rendering, not native Mac FPS or Safari evidence.", "Capsule/segment collision checks are runtime movement evidence, separate from actual skinned-mesh furniture contact review.", "Authored walker trajectories do not necessarily produce actor/actor encounters; absence of overlaps does not prove an unexercised avoidance branch."]}
    with sync_playwright() as p:
        browser = launch(p, args.browser)
        try:
            for scenario in args.scenario or ["stationary_actor", "walking_actor_yields", "enable_occupied_anchor"]:
                page = browser.new_page(viewport={"width": 640, "height": 360})
                page.on("pageerror", lambda e: report["page_errors"].append(str(e)))
                page.on("console", lambda m: report["console_errors"].append(m.text) if m.type == "error" else None)
                def response(r):
                    name = urlparse(r.url).path.rsplit("/", 1)[-1]
                    if name in ["app.js", "people-manifest.json", "poses.json", "people-layer.js"]:
                        try:
                            body = r.body()
                            entry = {"url": r.url, "status": r.status, "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}
                            if entry not in report["source_responses"]:
                                report["source_responses"].append(entry)
                        except Exception as e:
                            report.setdefault("source_capture_errors", []).append(str(e))
                page.on("response", response)
                page.goto(args.url, wait_until="domcontentloaded", timeout=240000)
                page.wait_for_function("window.__viewer?.ready && !!__viewer.api.peopleDiagnostics", timeout=600000)
                report["gpu"] = page.evaluate("__viewer.api.gpuInfo()")
                result = page.evaluate("""async ({scenario,expected}) => {
                    const api=__viewer.api, trace=[], check=(ok,message)=>{if(!ok)throw new Error(message)};
                    await api.setPeopleEnabled(true);
                    check(api.peopleStats().loaded && api.peopleStats().enabled && api.peopleStats().total===expected,'People not accepted/loaded/enabled or unexpected actor count');
                    const diagnostics=()=>api.peopleDiagnostics();
                    const find=id=>diagnostics().find(a=>a.id===id);
                    const position=a=>a.position;
                    const step=input=>api.stepWalkQA({forward:0,strafe:0,yaw:0,dt:1/60,...input});
                    let actor=find(scenario==='walking_actor_yields'?'office-person-33':'office-person-02');
                    check(actor,'Required reviewed actor absent');
                    const id=actor.id,initial=position(actor).slice(),r=actor.radius;
                    check(Number.isFinite(r),'Missing actual actor radius diagnostic');
                    await api.setPeopleEnabled(false);
                    let start;
                    if(scenario==='stationary_actor'){
                        for(let i=0;i<32&&!start;i++){
                            const angle=i*Math.PI/16,dx=Math.cos(angle),dz=Math.sin(angle),candidate=[initial[0]+dx*1.1,initial[2]+dz*1.1];
                            let clear=true;
                            for(let j=0;j<=44;j++)if(api.blocked(initial[0]+dx*j*.025,initial[2]+dz*j*.025)){clear=false;break;}
                            if(clear)start=candidate;
                        }
                        check(start,'No static-free approach to standing actor; no synthetic fixture bypass attempted');
                        await api.setPeopleEnabled(true);
                        api.setWalkQAStart(start[0],start[1]);
                        const yaw=Math.atan2(start[0]-initial[0],start[1]-initial[2]);
                        let state=step({dt:0}),minimum=Infinity;
                        const before=state.collisions;
                        for(let i=0;i<240;i++){
                            state=step({forward:1,yaw});actor=find(id);
                            const a=position(actor),d=Math.hypot(state.position[0]-a[0],state.position[2]-a[2]);
                            minimum=Math.min(minimum,d);trace.push({i,position:state.position,actor:a,distance:d,collisions:state.collisions});
                            check(d>=r+.15-1e-5,'Visitor entered stationary actor capsule');
                            check(!state.blocked,'Visitor endpoint is blocked');
                            check(state.startCount===1,'Unexpected extra spawn');
                        }
                        check(state.collisions>before,'Actor blocker was not exercised');
                        check(minimum<.9,'Visitor stopped too far away to attribute blocking to the intended actor');
                        return {scenario,id,passed:true,initialActor:initial,initialVisitor:start,minimumCenterDistance:minimum,combinedRadii:r+.15,collisionsAdded:state.collisions-before,final:state,trace};
                    }
                    if(scenario==='walking_actor_yields'){
                        // The authored person33 path is east-west in Z33; obtain its
                        // actual manifest rather than assigning a new actor route.
                        const manifest=await fetch(new URL('./people/people-manifest.json',location.href)).then(r=>{check(r.ok,'People manifest unavailable');return r.json()});
                        const def=manifest.actors.find(a=>a.id===id),path=def.path;
                        check(path?.length>=2,'Authored walker path missing');
                        let dx=path[1][0]-path[0][0],dz=path[1][1]-path[0][1],length=Math.hypot(dx,dz);dx/=length;dz/=length;
                        start=[initial[0]+dx*1.3,initial[2]+dz*1.3];
                        check(!api.blocked(...start),'Stationary visitor probe lies in static geometry');
                        await api.setPeopleEnabled(true);
                        api.setWalkQAStart(...start);
                        let state=step({dt:0}),minimum=Infinity,maxActorAdvance=0,previous=initial,nearStoppedFrames=0;
                        for(let i=0;i<1200;i++){
                            // A large input dt also exercises the shared controller's
                            // finite substeps and the actor callback, not one teleport.
                            state=step({dt:i===300?.25:1/60});actor=find(id);
                            const a=position(actor),d=Math.hypot(state.position[0]-a[0],state.position[2]-a[2]);
                            minimum=Math.min(minimum,d);maxActorAdvance=Math.max(maxActorAdvance,Math.hypot(a[0]-initial[0],a[2]-initial[2]));
                            if(d<1 && Math.hypot(a[0]-previous[0],a[2]-previous[2])<1e-6)nearStoppedFrames++;
                            trace.push({i,visitor:state.position,actor:a,distance:d,moving:actor.moving});previous=a.slice();
                            check(d>=r+.15-1e-5,'Moving actor entered stationary visitor capsule');
                            check(Math.hypot(state.position[0]-start[0],state.position[2]-start[1])<1e-9,'Zero-input visitor drift');
                            check(state.startCount===1,'Unexpected extra spawn');
                        }
                        check(maxActorAdvance>.2,'Walker did not advance during real zero-input substeps');
                        check(nearStoppedFrames>120,'No sustained actor yield near stationary visitor was observed');
                        return {scenario,id,passed:true,minimumCenterDistance:minimum,combinedRadii:r+.15,maxActorAdvance,nearStoppedFrames,final:state,trace};
                    }
                    start=[initial[0],initial[2]];
                    check(!api.blocked(...start),'Actor anchor is not free in static-only counterfactual');
                    api.setWalkQAStart(...start);
                    await api.setPeopleEnabled(true);
                    actor=find(id);
                    check(actor.hiddenForVisitor===true,'Enabling at occupied anchor did not separate actor from visitor');
                    check(!api.blocked(...start),'Visitor trapped by newly enabled actor');
                    return {scenario,id,passed:true,visitor:start,actor,stats:api.peopleStats(),trace};
                }""", {"scenario": scenario, "expected": args.expected_people})
                trace = result.pop("trace")
                (args.output / (scenario + "-trace.json")).write_text(json.dumps(trace, separators=(",", ":")))
                result["viewer_errors"] = page.evaluate("__viewer.errors||[]")
                report["scenarios"].append(result)
                (args.output / "collision-report.json").write_text(json.dumps(report, indent=2))
                page.close()
                print(json.dumps({"scenario": scenario, "passed": result["passed"]}), flush=True)
            report["status"] = "passed" if all(x["passed"] for x in report["scenarios"]) and not report["page_errors"] and not report["console_errors"] else "failed"
        except Exception as e:
            report["status"], report["exception"] = "failed", str(e)
            raise
        finally:
            (args.output / "collision-report.json").write_text(json.dumps(report, indent=2))
            browser.close()


if __name__ == "__main__":
    main()
