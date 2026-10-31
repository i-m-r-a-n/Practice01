# ChatGPT prompt: one photorealistic image per room

## কীভাবে চালাবেন
1. Drive-এ ছবি আপলোড পুরো শেষ হতে দিন। গ্যালারি পেজে সব রুম "শেষ" দেখাবে, ততক্ষণ পেজটা খোলা রাখুন।
2. ChatGPT খুলে Agent mode চালু করুন।
3. নিচের "PROMPT START" থেকে "PROMPT END" পর্যন্ত পুরো লেখাটা কপি করে পেস্ট করুন।
4. Google লগইন চাইলে নিজে নিয়ন্ত্রণ নিয়ে লগইন করুন, তারপর ChatGPT-কে চালিয়ে যেতে দিন।
5. প্রথম 2টা রুমের ছবি 3D ছবির সাথে মিলিয়ে দেখুন। ঠিক থাকলে বলুন "continue"।
6. Agent ছবি বানাতে বা আপলোড করতে না পারলে সাধারণ ChatGPT চ্যাটে কাজ করুন। রুমের ছবিটা আপলোড করুন, তারপর "RULES" অংশ আর সেই রুমের কার্ডটা পেস্ট করুন।

---

PROMPT START
# ROLE
You are the world's best architectural and interior photographer, working together with a top architectural visualisation artist. Your work is published in Architectural Digest, Dezeen and Frame and on the best architecture and interior design Instagram accounts. Every frame you deliver is calm, precise, beautifully lit and true to the design.

# PROJECT
The ground floor of a knitwear company's corporate headquarters and design development centre in Bangladesh. The design is a clean, modern office in oak, walnut, terrazzo, black steel and glass with deep-green accents, warmed by Bengali craft and earth materials: unglazed clay and terracotta, jute, bamboo and cane, handloom and kantha textiles, natural indigo and living plants. Each source picture is a screenshot of the approved 3D model. Your job is to show the client how each room will look after construction: a real photograph of the finished room, ready for a client presentation and Instagram.

# YOUR TASK (Agent mode)
Google Drive: "Imran — Main Folder" > "shakwat factory" (https://drive.google.com/drive/folders/1TG36-FQdR2pqX8w_s5Z-V0UxM4NmyK5G).
Each room has its own folder with 3D pictures. Save every result in the "chatgpt" folder: https://drive.google.com/drive/folders/1wz3ORRlypiBOW44hfKOoQuguP_bj3vjX

Work through the 34 rooms in the ROOM LIST, in order, one room at a time:
1. Open the room's source picture: use the direct link, or open the room folder and pick the file with exactly the given title. Use only that one file. Never use files whose title contains "photoreal CAM"; they show an older design.
2. Create ONE photorealistic image from it, following the RULES and the room card.
3. Run the SELF-CHECK. If any point fails, generate again (up to 3 tries). If it still fails, keep the best try and note the problem.
4. Upload the image to the "chatgpt" folder with exactly the file name given in the card ("Save as").
5. Write one short line: room number, file uploaded, any problem. Then continue with the next room.

If you cannot open Google Drive, cannot generate images, or cannot upload, stop and tell me exactly what is blocked. If uploading is impossible, give me each image as a download with the exact "Save as" file name.
When all rooms are done, give me a table: number, room, source file, uploaded file name, status or notes.

# RULES
LOCK - never change:
1. Camera: the same position, height, angle, field of view, framing and composition as the source. Same perspective and vanishing points. Vertical lines stay vertical.
2. Architecture: every wall, column, beam, ceiling element, door, window, glass partition, opening and stair stays in the same place, size and shape.
3. Contents: every piece of furniture, fitting, plant, object and artwork stays where it is, with the same count, size, shape, colour and material. Add nothing, remove nothing, move nothing.
4. The room card describes the whole room. Show only what is visible in the source picture; the card only helps you name materials and objects correctly. Never add an item from the card that is not in the picture.
5. Logos, brand walls, signage and printed panels stay exactly as in the picture. Never invent new words, numbers, logos, certificates or labels. If small text is unreadable in the picture, keep it as an unreadable print texture.
6. No people, no animals.

LIGHT - facts of this building:
- Only the Collaborative studio (room 19) has windows to the outside. There, use soft natural daylight from those windows together with the visible fittings.
- Every other room is lit only by its own visible fittings: pendants, downlights, track spots and linear lights. Do not add sunlight, sun beams, windows or outdoor views. Glass partitions look into neighbouring rooms, not outside.
- The courtyard studio (room 34) has no daylight; its plants grow under grow lights.
- The prayer rooms (rooms 26 and 28) have windows with roller blinds. Keep the blinds as shown, with soft even light and no sun beams.

IMPROVE - make it a real, beautiful photograph:
- Materials: true-to-life textures with fine detail: oak and walnut grain, fluted and slatted timber, terrazzo chips, porcelain tiles with fine grout lines, carpet-tile pile, felt, leather, linen and wool upholstery, handloom and kantha weave, unglazed terracotta and clay, jute, bamboo and cane, brushed brass, powder-coated black metal, clear glass with soft true reflections.
- Light: bright, clean editorial lighting; physically correct falloff from each fitting; soft contact shadows and ambient occlusion where objects meet floors and walls; correct white balance (neutral office white, warm 3000 K only where the card says so); balanced exposure with no blown highlights and no crushed shadows.
- Camera look: professional architectural interior photography with a full-frame camera and a tilt-shift lens, sharp from front to back, straight verticals, natural true colours, subtle real-world finish (fine fabric creases, slight natural wear). No heavy vignetting, no fisheye, no lens flare.
- Plants: living plants with natural leaves, real soil and real pots.
- Mood: premium, calm, spacious and functional, the kind of image a top architecture magazine would publish.

AVOID: CGI or video-game look, plastic-looking surfaces, cartoon colours, oversaturation, HDR halos, bent or warped straight lines, melted or merged objects, duplicated or missing furniture, garbled text, extra decoration, people, text overlays, watermarks or borders.

SPECIAL CASE: If the source is an aerial cut-away view looking down into the floor plan with no ceiling (room 29), keep it as a photorealistic architectural cut-away model view from the same high angle. Do not turn it into an eye-level photo.

OUTPUT: one landscape image, 3:2 (1536 x 1024), with the same composition as the source. No text, logo stamp, caption or border added to the image.

SELF-CHECK before every upload (compare with the source picture):
- Same framing and viewpoint?
- Same walls, doors, glass and ceiling elements?
- Same furniture, count and positions?
- Logos and signage unchanged, with no invented text?
- Nothing added (people, plants, decor, windows, sunlight)?
- Straight lines straight, and no warped or merged objects?
- Does it look like a real photograph and not a render?

# ROOM LIST
## 01. Arrival gallery
- Source: "Arrival gallery - room view.jpg" in the room folder https://drive.google.com/drive/folders/1VxzzfmWFL7VBKCIxiZ5vKGPNnwVsoZ-I (direct link: https://drive.google.com/file/d/1YnyEBjVcqVrYXkaUEchUw5ymGJicirBH/view)
- Save as: "01 Arrival gallery.png"
- What it is: Entrance and visitor check-in, the first impression of the building.
- Materials and light: Terrazzo floor. Exposed ceiling deck with white beams, black linear pendants, black track spots on the brand wall.
- Objects (show only those visible in the source): Check-in desk with a terracotta-brick front and walnut top; vertical oak-slat brand wall with the client logo panel and tagline; wooden doors in black frames; glass to the reception; the existing stair; handmade terracotta pieces on the desk; terracotta plaques on the wall; a banyan bonsai on a granite block by the glass gate; three natural stones.

## 02. Reception - tea lounge
- Source: "Reception - tea lounge - room view.jpg" in the room folder https://drive.google.com/drive/folders/106FVDniDoWFx6N-Q3ufaB_VyR7HtTn5G (direct link: https://drive.google.com/file/d/15te1PpuKa1h7ZxLxcEXtU9X2O0T911cd/view)
- Save as: "02 Reception - tea lounge.png"
- What it is: Reception counter and a visitors' tea lounge.
- Materials and light: Terrazzo floor. Suspended oak-slat ceiling raft with a brass halo pendant; black linear pendant; track spots.
- Objects (show only those visible in the source): Fluted-oak reception counter with a terrazzo ledge and a lower accessible section; logo plate on a fluted oak wall; lounge with a linen sofa, green armchairs, a round walnut table and a wool rug; tea in clay cups on wooden trays; rural instruments above the console (ektara, dotara, banshi, dhol); handloom textile hangings on the wall; a small fig tree and aloe vera in pots.

## 03. Earth & Sun passage
- Source: "Earth & Sun passage - corner 1.jpg" in the room folder https://drive.google.com/drive/folders/1G4GFf_qfwMrOqt3gNMiqG3gcipBWFkQI (direct link: https://drive.google.com/file/d/16bckaDil8xfMWqFZi4lfEDdM2dS27BgL/view)
- Save as: "03 Earth & Sun passage.png"
- What it is: Visitor passage between reception, experience centre and guest WCs, telling the earth-and-sun story.
- Materials and light: Terrazzo floor. Downlights.
- Objects (show only those visible in the source): A long wall of illustrated energy-story panels (sun, solar generation, use and storage, operations) under a wooden header; a terracotta-brick earth wall with clay bowls holding cotton, jute, recycled fibre and indigo; black-framed glass partitions looking into the neighbouring offices. Keep the panel text exactly as shown or as unreadable print; never invent numbers.

## 04. Guest WCs
- Source: "Guest WCs - angle 180.jpg" in the room folder https://drive.google.com/drive/folders/1lv5e26tagP8WNTILdrNpcREqwb_syk4v (direct link: https://drive.google.com/file/d/10Y9k3l68XV7j3VxXI6_7MakmEvDge7fp/view)
- Save as: "04 Guest WCs.png"
- What it is: Two guest WCs off the visitor passage.
- Materials and light: Large-format stone-look porcelain tiles on walls and floor. Linear light and downlights.
- Objects (show only those visible in the source): Vanity with a white vessel basin on a timber cabinet; wooden door in a black frame.

## 05. Negotiation suite
- Source: "Negotiation suite - room view.jpg" in the room folder https://drive.google.com/drive/folders/1g_UfoQILRzPcXzeRZbBxHcIxG2Bu1_FW (direct link: https://drive.google.com/file/d/1Q_ETvML7lw0GjurUIKhkiOEzxSrW3iDC/view)
- Save as: "05 Negotiation suite.png"
- What it is: The main negotiation and board room for buyers.
- Materials and light: Oak herringbone floor. Green felt ceiling rafts between the white beams; black linear pendants over the table.
- Objects (show only those visible in the source): Long walnut table with black leather chairs; large screen on an oak-slat media wall; walnut acoustic slats; glass wall to the experience centre; clay cups at every place and a clay jug; knitwear review trays; a bonsai in the corner by the screen; framed textile art.

## 06. Records room
- Source: "Records room - corner 1.jpg" in the room folder https://drive.google.com/drive/folders/1oBl9dy4D-4UQNghvGkSdsi4IlLzHmXdo (direct link: https://drive.google.com/file/d/1Ki7W6nIuEaH__8Xe-iH-vExG4EuGWaaQ/view)
- Save as: "06 Records room.png"
- What it is: Records room for the original documents behind every claim.
- Materials and light: Dark carpet tiles. Black linear pendant.
- Objects (show only those visible in the source): Meeting table for five with grey chairs; tall white document cabinets; green labelled box files on the table; a framed index board on the wall; black-framed glass partition to the open workspace.

## 07. Experience centre - fabric stories
- Source: "Experience centre - fabric stories - angle 045.jpg" in the room folder https://drive.google.com/drive/folders/1XN2lG9hDUwXFqBekt1hNDOTKghlymyRo (direct link: https://drive.google.com/file/d/18Xka4FQIwXZ52am6m0i0u9r8tvUHMLvh/view)
- Save as: "07 Experience centre - fabric stories.png"
- What it is: Experience centre where buyers see the knitwear and its fabric stories.
- Materials and light: Terrazzo floor. Black track lights fixed to the beams.
- Objects (show only those visible in the source): Brand-story wall with the client logos and tagline; garment display bays with deep-green backs, brass rails and LED shelves holding knitwear; dress forms; a sewing machine with patchwork pieced from cutting waste; long terrazzo display counter; natural indigo cloths suspended under the ceiling; jute sacks of colour-sorted offcuts, yarn cones and a clay water pot (kolshi).

## 08. Exec reception - tea point
- Source: "Exec reception - tea point - room view.jpg" in the room folder https://drive.google.com/drive/folders/14U_3zTNcER6R_Z2_i-goIXD32fgbIvru (direct link: https://drive.google.com/file/d/1oR0pxBp8YTcRLS6g9mIJEdCbvMXLwfOL/view)
- Save as: "08 Exec reception - tea point.png"
- What it is: Executive reception with the PA desk and a waiting corner.
- Materials and light: Oak herringbone floor. Black linear pendant.
- Objects (show only those visible in the source): PA desk with a monitor and office chair; executive waiting chairs with black cushions on timber frames; a potted plant; dark timber doors; black-framed glass partitions.

## 09. Director
- Source: "Director - room view.jpg" in the room folder https://drive.google.com/drive/folders/107ao2sOl9BOkOg6n-Mp0wlGOEmpcK4Tt (direct link: https://drive.google.com/file/d/13POw9nhr-FIj-JiyaELUh05f7AABIY0N/view)
- Save as: "09 Director.png"
- What it is: Director's office.
- Materials and light: Oak herringbone floor. Black linear pendant.
- Objects (show only those visible in the source): Dark timber director desk with monitor; low credenza; two visitor chairs; glass front onto the oak-lined executive corridor, with the managing director's office visible through the glass.

## 10. Managing Director
- Source: "Managing Director - room view.jpg" in the room folder https://drive.google.com/drive/folders/1S3oKxUUA8dhmMhb7JUdCF1zJj-FYL5Gw (direct link: https://drive.google.com/file/d/11pm5C139uv7mNK85laeywNFu3uerdZfL/view)
- Save as: "10 Managing Director.png"
- What it is: Managing Director's office.
- Materials and light: Oak herringbone floor. Oak-slat ceiling raft with a brass halo pendant.
- Objects (show only those visible in the source): Walnut desk with a leather pad and a cognac executive chair; walnut feature wall with the logo panel; lounge corner with a sofa, armchair, round coffee table and rug; framed textile art; a tall plant in a white pot; tea in clay cups.

## 11. Executive corridor
- Source: "Executive corridor - corner 2.jpg" in the room folder https://drive.google.com/drive/folders/1Nn6G7JBqLhtYsnLyoaub8QG3dfCsEA9v (direct link: https://drive.google.com/file/d/1GmKcRFF0aR1h0zouUOtlzQU8uyB5LfDw/view)
- Save as: "11 Executive corridor.png"
- What it is: Glass-fronted, oak-lined corridor linking the executive offices.
- Materials and light: Oak herringbone floor. Downlights.
- Objects (show only those visible in the source): Full-height oak wall lining on one side; black-framed glass on the other side, looking into the managing director's lounge.

## 12. Buyer project room - order desk
- Source: "Buyer project room - order desk - corner 4.jpg" in the room folder https://drive.google.com/drive/folders/1n_6Hb3EmFvY_RnqBHFEfXjrBVsL4Ggb8 (direct link: https://drive.google.com/file/d/1L1i6GCLKcb35EOfwmYPr-SSsqmOdLInL/view)
- Save as: "12 Buyer project room - order desk.png"
- What it is: Buyer project room, also the export and order desk.
- Materials and light: Dark carpet tiles. Black linear pendant.
- Objects (show only those visible in the source): Six-seat timber table with green upholstered chairs; wall-mounted project board; knit swatches on a tray; clay water jug and cups; order checklist papers; a potted plant; window to the open office; timber door.

## 13. Export & order centre (planned)
- Source: "Export & order centre (planned) - corner 4.jpg" in the room folder https://drive.google.com/drive/folders/1rrk5bkiDxNYVxybdVJKmLvxaw7qsGdCy (direct link: https://drive.google.com/file/d/1fd77VEu8tUH1ViSCeF_ksDbIrY4qSraI/view)
- Save as: "13 Export & order centre (planned).png"
- What it is: Planned export and order centre beside reception.
- Materials and light: Dark carpet tiles. Black linear pendants.
- Objects (show only those visible in the source): Four white desks with screens and black chairs; round timber meeting table with chairs; white storage cabinets; black-framed glass partitions; timber door.

## 14. Staff corridor
- Source: "Staff corridor - corner 2.jpg" in the room folder https://drive.google.com/drive/folders/19arwcO1aATxzL_nq08tM_WmlbEFR9C-N (direct link: https://drive.google.com/file/d/1-OfkpTHdWqBcTnB_lem8GMQDPA8d9jqS/view)
- Save as: "14 Staff corridor.png"
- What it is: Staff corridor from the lobby to HR and the offices.
- Materials and light: Terrazzo floor. Downlights.
- Objects (show only those visible in the source): Black-framed glass partitions on both sides, looking into a meeting room with green chairs and an open office.

## 15. CAD - knitwear development
- Source: "CAD - knitwear development - room view.jpg" in the room folder https://drive.google.com/drive/folders/1-2Q_rhRYGKDt83l2c0ZJFjozwsoFO8Ku (direct link: https://drive.google.com/file/d/12qdPJZ7kmxKHWe_zcmeq2hVKeZktakk2/view)
- Save as: "15 CAD - knitwear development.png"
- What it is: CAD and knitwear development room.
- Materials and light: Grey carpet tiles. Black linear pendants, neutral 4000 K light.
- Objects (show only those visible in the source): Three CAD workstations with two monitors each; large-format plotter; layout and digitiser table with paper patterns; brand-green felt pinboard with tech packs; interior window.

## 16. Fibre library
- Source: "Fibre library - corner 3.jpg" in the room folder https://drive.google.com/drive/folders/1y84O9fYsFpsa5t5LRR6UBKa93xdbLP0s (direct link: https://drive.google.com/file/d/1KAI7lhxpJyHCdxU426xZPXFybVZ799O1/view)
- Save as: "16 Fibre library.png"
- What it is: Fibre and fabric library with a colour-matching booth.
- Materials and light: Light concrete floor. Black linear pendants.
- Objects (show only those visible in the source): Timber shelving with fabric binders and books; low swatch shelving with labelled fibre boxes; garment rail; black D65 colour-viewing booth on a white review table; round stools; glass wall to the experience centre.

## 17. Fabric lab
- Source: "Fabric lab - corner 3.jpg" in the room folder https://drive.google.com/drive/folders/13hkWXqEd2QCTbSHEoCF0NYiucuBkLLrC (direct link: https://drive.google.com/file/d/13pyYLqhtUBzFAatrY44mW_YAbNCuD_0E/view)
- Save as: "17 Fabric lab.png"
- What it is: Fabric lab with 3D printers.
- Materials and light: Light concrete floor. Black linear pendants.
- Objects (show only those visible in the source): Four enclosed black-framed 3D printers on a bench over white cabinets; post-processing bench; desk with chair and monitor; interior window to the next room.

## 18. Sample room - remake and repair
- Source: "Sample room - remake and repair - corner 2.jpg" in the room folder https://drive.google.com/drive/folders/15e43WPvSAlnbB1zDkREo0XZ4CSIclu9y (direct link: https://drive.google.com/file/d/1DlnUhTw4zpN84d0I07NcUTg4FPnUKKcK/view)
- Save as: "18 Sample room - remake and repair.png"
- What it is: Sample room for remake and repair.
- Materials and light: Light concrete floor. Black linear pendants.
- Objects (show only those visible in the source): Pattern and cutting table with a kraft-paper T-shirt pattern and offcuts sorted by colour; a pieced patchwork panel; two sample sewing-machine stations; white dress forms on timber stands; garment rail; interior window.

## 19. Collaborative studio
- Source: "Collaborative studio - angle 000.jpg" in the room folder https://drive.google.com/drive/folders/1vzzrtbGGJixCV9wfWvKRC9R4rVj_Cy_w (direct link: https://drive.google.com/file/d/1fRxmAlcpdxk-xyc63nKh7RtF325EAaJ0/view)
- Save as: "19 Collaborative studio.png"
- What it is: Collaborative design studio, the only room with windows to the outside.
- Materials and light: Oak plank floor. Black linear pendants and track spots on the mood-board wall.
- Objects (show only those visible in the source): Creative workstations with monitors; long mood-board wall covered in fabric swatches; living wall of wooden plant niches with warm backlight (snake plant, money plant, peace lily); bonsai and a tulsi pot on the window shelf; small fig tree; clay pieces on the desks; east windows with roller blinds.

## 20. Sample & material store
- Source: "Sample & material store - corner 4.jpg" in the room folder https://drive.google.com/drive/folders/1jbHo7ABMKJ3mTpUJN2XRfEvjyWzfDP-P (direct link: https://drive.google.com/file/d/1m6tqU7U_NMZ-n5epFUSmNm4rC7S4_qUK/view)
- Save as: "20 Sample & material store.png"
- What it is: Sample and material store.
- Materials and light: Light concrete floor. Batten lights.
- Objects (show only those visible in the source): Tall timber shelving with sample boxes and folders along an aisle; door at the end.

## 21. Design wing - the making line
- Source: "Design wing - the making line - corner 1.jpg" in the room folder https://drive.google.com/drive/folders/1ASebQa_0ZbqL7U_bCTeR7hn9O4GCXGWs (direct link: https://drive.google.com/file/d/1IyEzuTFCoBK3Qi6_BGblr0haYh6NJLkd/view)
- Save as: "21 Design wing - the making line.png"
- What it is: Design-wing corridor with the making-line display.
- Materials and light: Terrazzo floor. Downlights.
- Objects (show only those visible in the source): A long wall shelf showing one T-shirt in six steps (fibre, yarn, knit fabric, cut and sew, testing, wear and return) with small labels under a wooden header; glass partitions to the labs. Keep the text exactly as shown or as unreadable print.

## 22. Staff & artisan dining
- Source: "Staff & artisan dining - room view.jpg" in the room folder https://drive.google.com/drive/folders/1_dOoKCTSfhAPiKE_09nAF8O1qOY0uL53 (direct link: https://drive.google.com/file/d/1QMbo9BuIx64oi60TxKLU6GnWcauxd_dL/view)
- Save as: "22 Staff & artisan dining.png"
- What it is: Staff and artisan dining with a Bengali tea stall.
- Materials and light: Oak plank floor. White dome pendants.
- Objects (show only those visible in the source): Two long cafe tables with green chairs and hogla reed runners; clay plates, cups and jugs; pantry counter with sink and refrigerator; a tea-stall cart front on two wheels with a painted canopy, painted kettles on jute cords and an electric lantern in the hurricane form; wood-slice stools; a potted plant.

## 23. Academy annex (pilot academy)
- Source: "Academy annex (pilot academy) - room view.jpg" in the room folder https://drive.google.com/drive/folders/1_nIXygu76t8zvfl6hYyMex6SZaqDPbI7
- Save as: "23 Academy annex (pilot academy).png"
- What it is: Pilot academy room for learning fibre, knit and repair.
- Materials and light: Oak plank floor. Brass halo pendant and black linear pendant.
- Objects (show only those visible in the source): Six-seat workshop table with green chairs, knit swatches, yarn cones and a mending kit; pinboard craft wall of student work; wall screen; green sofa with grey armchairs; a tall plant; glass wall.

## 24. North corridor
- Source: "North corridor - corner 3.jpg" in the room folder https://drive.google.com/drive/folders/1InMEVFG6pxAZT6RooIS45C5KUHZlTWLi
- Save as: "24 North corridor.png"
- What it is: North corridor to the staff dining, lounge and prayer rooms.
- Materials and light: Terrazzo floor. Downlights.
- Objects (show only those visible in the source): Long corridor with a black-framed glass wall into the staff dining, where pendants and tables with clay tableware are visible.

## 25. Hallway
- Source: "Hallway - angle 225.jpg" in the room folder https://drive.google.com/drive/folders/1pRAglS5iKtfiAZeCoigZTuiwvvsPcN02
- Save as: "25 Hallway.png"
- What it is: Staff hallway between the offices and the design wing.
- Materials and light: Terrazzo floor. Downlights.
- Objects (show only those visible in the source): Patterned privacy-glass panels in black frames above a white dado; opening at the far end.

## 26. Prayer room (male)
- Source: "Prayer room (male) - corner 4.jpg" in the room folder https://drive.google.com/drive/folders/1iv4u6Lr9Sg5i4K_bZBppz06lghdEt1SO
- Save as: "26 Prayer room (male).png"
- What it is: Men's prayer room.
- Materials and light: Green prayer carpet. Warm 3000 K downlights.
- Objects (show only those visible in the source): Timber book shelf; shoe rack; windows with roller blinds (keep the blinds as shown; soft even light, no sun beams).

## 27. Wudu (male)
- Source: "Wudu (male) - corner 2.jpg" in the room folder https://drive.google.com/drive/folders/1GryzFDAHeDSn0UoBhpE25itriG5YlknW
- Save as: "27 Wudu (male).png"
- What it is: Men's ablution (wudu) room.
- Materials and light: Stone-look porcelain tiles. Downlights.
- Objects (show only those visible in the source): Ablution bench with taps and round stools; timber door.

## 28. Prayer room (female)
- Source: "Prayer room (female) - corner 4.jpg" in the room folder https://drive.google.com/drive/folders/1Tg-sQyRnU-pfA15Qz3fT68dZJlp1TKpp
- Save as: "28 Prayer room (female).png"
- What it is: Women's prayer room.
- Materials and light: Green prayer carpet. Warm 3000 K downlights.
- Objects (show only those visible in the source): Timber book shelf; timber door; round wall fitting as shown.

## 29. Wudu (female)
- Source: "Wudu (female) - room view.jpg" in the room folder https://drive.google.com/drive/folders/1Hl2UkPOuEp_rK9cACZhNAjCGeWxqYU4R
- Save as: "29 Wudu (female).png"
- What it is: Women's ablution (wudu) room, shown from above.
- Materials and light: Stone-look porcelain tiles.
- Objects (show only those visible in the source): Ablution bench. This source is an aerial cut-away view: keep the high angle and every neighbouring room exactly as shown (see SPECIAL CASE).

## 30. Washroom (female)
- Source: "Washroom (female) - room view.jpg" in the room folder https://drive.google.com/drive/folders/157hrTdmL0R-M7FN8_iYDR2Hj4N7VHoKa
- Save as: "30 Washroom (female).png"
- What it is: Women's washroom.
- Materials and light: Stone-look porcelain tiles. Downlights and a linear mirror light.
- Objects (show only those visible in the source): Two WC cubicles with white partitions; long vanity with basins on a timber cabinet; timber door.

## 31. Washroom (male)
- Source: "Washroom (male) - room view.jpg" in the room folder https://drive.google.com/drive/folders/1lRQoCag2gsDdfnKorEO-sLP-sk3Y2wML
- Save as: "31 Washroom (male).png"
- What it is: Men's washroom.
- Materials and light: Stone-look porcelain tiles. Downlights.
- Objects (show only those visible in the source): Two WC cubicles with white partitions; two urinals; vanity with a basin on a timber cabinet.

## 32. Guest workspace WC
- Source: "Guest workspace WC - corner 3.jpg" in the room folder https://drive.google.com/drive/folders/15nAupcehvwZCzoAiB3snt1L-PlZXbpnD
- Save as: "32 Guest workspace WC.png"
- What it is: WC for the guest workspace.
- Materials and light: Stone-look porcelain tiles. Linear light.
- Objects (show only those visible in the source): Vanity with a white vessel basin on a timber cabinet; timber door in a black frame.

## 33. Design academy (later phase)
- Source: "Design academy (later phase) - angle 000.jpg" in the room folder https://drive.google.com/drive/folders/1OKtCqoSOeG4P8IhvRIEkf9nfkEmCzp7K
- Save as: "33 Design academy (later phase).png"
- What it is: Later phase: a design academy inside the existing glass suite.
- Materials and light: Carpet floor. Black linear pendants.
- Objects (show only those visible in the source): About 20 seats at timber tables with timber chairs; demonstration bench with a sewing machine; mobile screen; pin-up board; black-framed glass suite walls.

## 34. Green Uthan - circular knitwear studio (later phase)
- Source: "Green Uthan - circular knitwear studio (later phase) - room view.jpg" in the room folder https://drive.google.com/drive/folders/1bj0O5XnonRvTvQ8wquWRajZ0kRiZAIfK
- Save as: "34 Green Uthan - circular knitwear studio (later phase).png"
- What it is: Later phase: a Bengali courtyard and circular knitwear studio. No daylight here; plants live under grow lights.
- Materials and light: Carpet floor. Felt baffles between the beams; grow lights over the plants.
- Objects (show only those visible in the source): A courtyard around the column with a raised bot-tola seat; small fig trees and a bonsai; stone seats; an open bamboo canopy hung with woven kula and dala trays and clay pots; alpana floor art; electric lanterns in the hurricane form; knitwear on bamboo rails; colour-sorted offcuts; kantha textiles; take-back bins; artisan and craft corners with cane and bamboo furniture.

PROMPT END
