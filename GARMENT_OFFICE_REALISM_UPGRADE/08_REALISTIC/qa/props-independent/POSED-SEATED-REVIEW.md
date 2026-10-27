# Seated activity contact review — rejected candidate

Actual browser-deformed LOD0 meshes were checked against exact approved source furniture triangles at0,3,6,9seconds:23 seated actors,92 actor snapshots. This review does not alter approved furniture or poses.

21 of23 seated actors have vertices more than15mm below the actual flat cushion-top footprint at every sampled time. Typical task-chair trousers enter35–37mm; Boardroom trousers enter42–43mm. Reception sofa actors03/04 have zero vertices in the15–65mm diagnostic slab after their forward correction; shallow cushion contact and foot/rug issues remain separate.

Actors01/14/16/20 additionally place resting skin geometry into seat slabs. The people author identified hanging resting hands, so a global pelvis lift alone would not solve those contacts. Actual mesh names and coordinates are recorded.

Typing poses cross desk front/top surfaces: e.g actor17 intersects F110 white tabletop and oak front edge; actor25 intersects the CAD desk. Raising wrist joints alone does not establish forearm/finger clearance. The sewing pose contacts its raised machine bed and table edge; work-plane heights are0.8255m and0.762m respectively.

Use `posed-seated-cycle-summary.json` for per-actor results and the four `posed-seated-contacts-t*.json` files for exact source/actor triangle examples and source/export hashes. `source-seat-footprints.json` supplies22 exact support footprints; `source-floor-heights.json` is supplied to the separate floor reviewer.

Four discrete samples cannot prove continuous operation. Triangle surface contacts include intentional hand/cushion contact and must be interpreted with the supplied coordinates. The15mm seat threshold is a visual QA threshold, not an ergonomic standard. Skin can be clothing-occluded even while enabled. This is not a completed visual or functional acceptance.
