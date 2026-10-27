# Reception: four frozen actors — contact acceptance

**Pass for static geometry only.** Actual final browser-deformed meshes for actors01–04 have zero approved-furniture triangle contacts, zero badge/skin intersections and zero book/skin-or-clothing intersections. The book underside is1.98006mm above the highest lap surface within its footprint.

Accepted source lock: manifest `d1ee7c8d88b22216aaea9c07283bc1c392ef9eae43359d4038ce3e734d349b7a`; poses `16bb2498fd8b86fe8dcc57e27b606aee4d48dba8dcaee10b110fda66e65f8fc3`. Full runtime/model hashes are in [the acceptance JSON](reception-static4-contact-acceptance.json).

Evidence: [same-source furniture clearance](reception-static4-final2-furniture-contacts.json), [book/badge clearance](reception-static4-final2-prop-contacts.json), [floor/privacy review](../reception-static-contact-final2/floor-privacy-review.json), and [unchanged prior actors](../reception-static-contact-final2/previous-candidate-preservation.json). The baseline reviewer also verified that all four remain identical after ten updates totalling0.5s.

Exported posed coordinates are rounded to1micrometre; the triangle separation tolerance is0.1micrometre. Approximately0.5mm sole offsets and the1.98mm lap gap are deliberate visual tolerances. These are frozen poses, not a physical contact, continuous handover or moving-character proof. No approved room/furniture geometry moved. Integrated visual quality and target-Mac performance remain separate checks.
