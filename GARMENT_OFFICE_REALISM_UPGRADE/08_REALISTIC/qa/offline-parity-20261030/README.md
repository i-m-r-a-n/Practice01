# Six-room offline interior parity repair — 30 October 2026

The cumulative offline ZIP now contains the six-room interior release actually served by `/realistic/`: source `d5939f9ef3928340908459efc440259df0d34b6d`. No Worker deployment was made. Claude's prepared Lobby/CAD source at `533d698…` and separate proposals are excluded.

The previous `realistic-design_studio/Design_Studio_Realistic_Offline.zip` was still the older package: 73,034,188 bytes, SHA256 `8c86264151392b77087556c5d20fdc4b56be7b3c7e8024a2d73b3d50af98893a`. Its config was 1,842 bytes; the live interior config is 4,698 bytes. The old package is preserved.

## Deliverable

- [New ZIP and manifest](../../../../GARMENT_OFFICE_WALKTHROUGH_FINAL/09_MAC_OFFLINE_TOUR/realistic-six_room_interiors/)
- ZIP: 73,868,332 bytes; SHA256 `6b3cf6aa1d8dfb810d6d7ff671dd7047e3933f29fee11095767aae28334416c3`.
- Extract the complete folder, keep its files together, and open `Office_Realistic_Tour.html` in Firefox on the target Mac. Target-Mac acceptance remains outstanding; see the limitations below.

## What changed

The package is rebuilt from the deployed `viewer/dist` bytes, not a newly rebuilt or undeployed viewer. The builder accepts `--source-commit` and checks bundled inputs against that immutable Git source. Its manifest now records the source commit, all 3 viewer dist hashes, packed assets, stills, and generated package-file hashes. A wrong-source negative check rejects the old release SHA.

The first actual package load exposed an inherited dependency omission: the new release fetches `textures/pbr2k/ktx2/Terrazzo019M/basecolor.ktx2`, but the old packager only collected codec textures. It returned HTTP 404 and the finish refinement failed. The builder now also includes literal texture-resource URLs referenced by the shipped bundle. The final package includes the terrazzo albedo and PBR index, without adding the unused full PBR texture collection. Viewer code and design remain byte-identical to the deployed source.

## Evidence

- [Live source comparison](live-source-parity.json): public page, `app.js`, and config matched the pinned dist exactly. An initial Python urllib request returned 403; ordinary curl using inherited proxy/TLS succeeded.
- [Final static parity](parity-final.json): 23 packed assets, inline app, 43 camera stills, and 62 generated files checked; ZIP round trip exact. Source model SHA256 `06f13e5311f4f78008a15ab8b7d97c3284d52411cf22c231d522d2c26ed196c3`.
- [Wrong-source rejection](wrong-source-rejected.json): packaging against `bcb92b0…` fails on the first differing input.
- [Final runtime check](chromium-loopback-final/report.json): Linux Chromium, software WebGL, 1440×900, Internet requests blocked by the test. All 6 cameras rendered, terrazzo finish loaded, 27 frozen illustrative figures and People off/on worked. No page, console, viewer or HTTP errors; no failed/external requests or missing offline resources. Ready including finish completion: 30.617 seconds in this executor, not a MacBook or WAN benchmark.
- [Initial failed runtime check](chromium-loopback/report.json): preserved evidence of the missing texture. The test's initial list/count assertion error was also corrected; neither failure is presented as a pass.
- [Final live read-only check](final-live-readonly.json): live source still `d5939f9…`; original `/` SHA256 remains `ff75beb54b3134b3e1eee7d29d0f6016ed1bf5895777c715f3815ebe3dcd2675`. No live mutation or rollback occurred.

The final screenshots were opened and visually inspected: Reception's textile panels/rug and terrazzo, Experience's knit forms/textile baffles, Boardroom's kantha panel/pads, MD's panel/rug, Merchandising's proposed finish/samples, and Studio's cloth board are present. This establishes package rendering, not new design approval or a new contact-clearance audit of inherited people.

| Camera | Actual offline-resource capture |
| --- | --- |
| Reception CAM_01 | [PNG](chromium-loopback-final/CAM_01_Reception_A.png) |
| Boardroom CAM_09 | [PNG](chromium-loopback-final/CAM_09_Boardroom_A.png) |
| Experience CAM_04 | [PNG](chromium-loopback-final/CAM_04_Experience_Centre_A.png) |
| MD Office CAM_07 | [PNG](chromium-loopback-final/CAM_07_MD_Office_A.png) |
| Merchandising CAM_34 | [PNG](chromium-loopback-final/CAM_34_Merchandising_Sample_Hub.png) |
| Design Studio CAM_14 | [PNG](chromium-loopback-final/CAM_14_Design_Studio_B.png) |

[Six existing same-camera before/after comparisons](existing-comparisons.md) are linked separately, with their original provenance.

## Limits

- Chromium direct `file://` navigation is blocked by administrator policy: [failure](chromium-file/report.json). The successful runtime test uses loopback HTTP with the same offline HTML/JS packs, and is explicitly not a file-protocol pass.
- Existing Firefox Nightly cannot finish launching in this executor: sandbox `/proc/self/uid_map: EROFS`, plus a headless framebuffer failure. Both [headless](firefox/result.json) and [existing-Xvfb headed](firefox/headed-result.json) diagnostics are retained. No browser policy was bypassed.
- Native MacBook Firefox, Chrome, Safari, direct double-click operation, GPU memory and frame rate remain untested. No 30/60 fps claim is made.

## Reproduce

From a checkout containing the deployed source inputs:

```sh
python3 GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/deploy/package_offline.py Six_Room_Interiors --source-commit d5939f9ef3928340908459efc440259df0d34b6d --staging /tmp/office-offline-parity
python3 GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/qa/check_offline_parity.py /tmp/office-offline-parity/Six_Room_Interiors_Realistic_Offline GARMENT_OFFICE_WALKTHROUGH_FINAL/09_MAC_OFFLINE_TOUR/realistic-six_room_interiors/Six_Room_Interiors_Realistic_Offline.zip /tmp/office-offline-parity-result.json
python3 GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/qa/check_offline_six_rooms.py /tmp/office-offline-parity/Six_Room_Interiors_Realistic_Offline /tmp/office-offline-runtime --protocol http
```

ZIP timestamps can differ on regeneration; verify the newly generated ZIP hash and its manifest rather than assuming this release's ZIP hash will repeat.
