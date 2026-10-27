"""Export actual browser-deformed LOD0 people meshes for independent contact QA.

No pose or character placement is invented here. The runtime supplies all poses;
getVertexPosition applies its actual morphs and skinning before world transforms.
Large audit exports live outside the Git repository; only their manifest is small.
"""
import argparse
import gzip
import hashlib
import json
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from browser_walk_route import launch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8770/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/people/review/office-preview.html")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--preflight", action="store_true", help="Export current manifest actors only at t0 before a longer-cycle review.")
    parser.add_argument("--maximum-actors", type=int, help="Fail before exporting if a reduced-scope manifest contains more actors than expected.")
    parser.add_argument("--freeze-check", action="store_true", help="With preflight, export again after ten real runtime updates to verify frozen geometry.")
    args = parser.parse_args()
    output = args.output.resolve()
    if (output / "export-manifest.json").exists():
        raise RuntimeError("Existing audit export preserved; choose a new output directory")
    output.mkdir(parents=True, exist_ok=True)
    report = {"status": "running", "url": args.url, "sources": [], "snapshots": [], "errors": [], "scope": "Actual runtime posed LOD0 world vertices/indices plus hand props. All actors at0/3/6/9seconds; moving actors additionally at0.35/0.75/1.3seconds. No rendering/material realism or Mac performance claim."}
    if args.preflight:
        report["scope"] = "Actual runtime posed visible LOD0 world vertices/indices plus hand props; current manifest actors at t0. Preflight, not full cycle, rendered realism or Mac performance acceptance."
        if args.freeze_check:
            report["scope"] += " A second export follows ten actual runtime updates totalling0.5seconds, to test frozen geometry."

    def save():
        (output / "export-manifest.json").write_text(json.dumps(report, indent=2))

    with sync_playwright() as playwright:
        browser = launch(playwright, "chromium")
        page = browser.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        page.on("pageerror", lambda error: report["errors"].append(str(error)))

        def source_seen(response):
            name = urlparse(response.url).path.rsplit("/", 1)[-1]
            if name in ["people-layer.js", "people-manifest.json", "poses.json"] or name.endswith(".glb"):
                try:
                    body = response.body()
                    report["sources"].append({"url": response.url, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
                except Exception as error:
                    report.setdefault("source_capture_errors", []).append({"url": response.url, "error": str(error)})
        page.on("response", source_seen)
        started = time.monotonic()
        try:
            page.goto(args.url, wait_until="domcontentloaded", timeout=240000)
            page.wait_for_function("window.ready === true && !!window.people?.group", timeout=600000)
            page.evaluate("window.frozen=true")
            report["browser"] = browser.version
            report["people_manifest"] = page.evaluate("window.people.manifest")
            if args.maximum_actors is not None and len(report["people_manifest"]["actors"]) > args.maximum_actors:
                raise RuntimeError("People manifest exceeds the explicitly bounded actor scope")
            page.evaluate("""() => {
                const Vec = camera.position.constructor;
                window.__contactExport = id => {
                    const def=people.manifest.actors.find(a=>a.id===id);
                    const pivot=people.group.children.find(a=>a.name===id+'_placement');
                    if(!def||!pivot)throw new Error('Actor missing: '+id);
                    people.group.updateMatrixWorld(true);
                    pivot.traverse(o=>{if(o.isSkinnedMesh)o.skeleton.update()});
                    const meshes=[],bones={},hiddenMeshes=[];
                    pivot.traverse(o=>{
                        if(o.isBone && /^(root|pelvis|upperleg01_[LR]|lowerleg01_[LR]|foot_[LR]|toe[0-9_]*[LR]|wrist_[LR])$/.test(o.name))bones[o.name]=o.getWorldPosition(new Vec()).toArray();
                        if(!o.isMesh||o.userData.peopleLOD===1)return;
                        let visible=true,parent=o;while(parent){if(!parent.visible)visible=false;parent=parent.parent;}
                        if(!visible){hiddenMeshes.push(o.name);return;}
                        const v=new Vec(),count=o.geometry.attributes.position.count,vertices=[];
                        for(let i=0;i<count;i++){
                            o.getVertexPosition(i,v);o.localToWorld(v);
                            const a=v.toArray().map(x=>Math.round(x*1e6)/1e6);vertices.push(a);
                        }
                        const allIndices=o.geometry.index?Array.from(o.geometry.index.array):Array.from({length:count},(_,i)=>i);
                        const range=o.geometry.drawRange,indices=allIndices.slice(range.start,Number.isFinite(range.count)?range.start+range.count:undefined);
                        const low=[Infinity,Infinity,Infinity],high=[-Infinity,-Infinity,-Infinity];
                        for(const index of new Set(indices)){const a=vertices[index];for(let j=0;j<3;j++){low[j]=Math.min(low[j],a[j]);high[j]=Math.max(high[j],a[j])}}
                        meshes.push({name:o.name,visible:true,effectivelyVisible:true,skinned:!!o.isSkinnedMesh,materials:(Array.isArray(o.material)?o.material:[o.material]).map(m=>m.name),vertices,indices,bounds:{min:low,max:high}});
                    });
                    return {id,definition:def,actualPosition:pivot.position.toArray(),actualYaw:pivot.rotation.y,bones,meshes,hiddenMeshes};
                };
            }""")
            elapsed = 0
            schedule = [(0, True)] if args.preflight else [(0, True), (.35, False), (.75, False), (1.3, False), (3, True), (6, True), (9, True)]
            if args.preflight and args.freeze_check:
                schedule.append((.5, True))
            for target, all_actors in schedule:
                remaining = target - elapsed
                page.evaluate("""seconds => {
                    let remaining=seconds;
                    while(remaining>1e-10){const dt=Math.min(.05,remaining);people.update(dt,{quality:'high'});remaining-=dt;}
                    people.update(0,{quality:'high'}); // all actors evaluated nearby at actual high-detail LOD
                    people.group.updateMatrixWorld(true);
                }""", remaining)
                elapsed = target
                actors = report["people_manifest"]["actors"]
                if not all_actors:
                    actors = [a for a in actors if a.get("path")]
                entry = {"seconds": target, "all_actors": all_actors, "actors": [], "runtime_stats": page.evaluate("people.stats()")}
                subdir = output / ("t" + str(target).replace(".", "_"))
                subdir.mkdir(exist_ok=True)
                for actor in actors:
                    geometry = page.evaluate("id => __contactExport(id)", actor["id"])
                    target_file = subdir / (actor["id"] + ".json.gz")
                    with gzip.open(target_file, "wt", compresslevel=3) as stream:
                        json.dump(geometry, stream, separators=(",", ":"))
                    entry["actors"].append({"id": actor["id"], "file": str(target_file.relative_to(output)), "sha256": hashlib.sha256(target_file.read_bytes()).hexdigest(), "meshes": len(geometry["meshes"]), "vertices": sum(len(m["vertices"]) for m in geometry["meshes"]), "minimum_vertex_y": min(m["bounds"]["min"][1] for m in geometry["meshes"])})
                report["snapshots"].append(entry)
                save()
                print(json.dumps({"seconds": target, "actors": len(entry["actors"])}), flush=True)
            report["status"] = "exported"
            if args.preflight and args.freeze_check:
                comparisons = []
                for first, second in zip(report["snapshots"][0]["actors"], report["snapshots"][1]["actors"]):
                    with gzip.open(output / first["file"], "rt") as stream:
                        a = json.load(stream)
                    with gzip.open(output / second["file"], "rt") as stream:
                        b = json.load(stream)
                    comparisons.append({"id": first["id"], "all_exported_fields_identical": a == b})
                report["frozen_geometry"] = {"checks": comparisons, "passed": all(c["all_exported_fields_identical"] for c in comparisons)}
        except Exception as error:
            report["status"] = "failed"
            report["failure"] = str(error)
            raise
        finally:
            report["wall_seconds"] = round(time.monotonic() - started, 3)
            save()
            browser.close()
    print(json.dumps({"status": report["status"], "snapshots": len(report["snapshots"]), "output": str(output)}))


if __name__ == "__main__":
    main()
