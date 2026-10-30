# STAGE II · Zara Fashion · renders based on the 3D model (ChatGPT kit)

Prepared by Claude, 30 October 2026. ChatGPT turns each 3D view into a photograph (A) and adds one closer moment in the same room (B): 46 images, then a PDF.

The same kit as a phone-friendly page, with every 3D frame and a copy button for each message: https://claude.ai/artifact/UiLPeUuXQQxeE37SSBNapE (private to the owner).

## কীভাবে ব্যবহার করবেন

1. ChatGPT-এ নতুন চ্যাট খুলুন। নিচের **বার্তা 0 (শুরু)** কপি করে পাঠান। এই বার্তার সাথে কোনো ছবি লাগবে না।
2. প্রতিটা স্টপের জন্য:
   - সেই স্টপের 3D ছবিটা (`refs/stopNN_ref.jpg`) ChatGPT-তে attach করুন।
   - সাথে ওই স্টপের বার্তাটা paste করুন।
   - ChatGPT দুটো ছবি দেবে: A আর B।
3. 23টা স্টপ শেষ হলে **শেষ বার্তা (PDF)** পাঠান।

3D ছবি না দেখলে ChatGPT 3D-এর মতো ছবি বানাতে পারে না। আগের PDF আমাদের 3D-এর সাথে মেলেনি এই কারণেই। তাই প্রতিটা স্টপের সাথে ছবি দিতেই হবে।

The 23 frames come from the same build as the live 3D (`109aec2`).
Each frame is at `refs/stopNN_ref.jpg` in this folder, or at `https://raw.githubusercontent.com/i-m-r-a-n/Practice01/3306380a4b4bfa2e2d506c98635d0b09ef7fa2da/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/qa/bel-20261030/presentation/photoshoot/refs/stopNN_ref.jpg`.

## Message 0 · setup (send once, no image)

```text
You are the best architectural and editorial photoshoot director and composition designer in the world.

We will make 46 photorealistic renders of the ground-floor concept of STAGE II Knitting Apparel Ltd. / Zara Fashion, a knitwear (RMG) factory in Bangladesh. Use only this branding (STAGE II · Zara Fashion) and invent no other brand or project name. The concept: knitwear made from earth fibres and recycled fabric, with Bengal craft as its signature. Every render is BASED ON OUR 3D MODEL. In each next message I attach one view from the 3D model and ask for two images:

A = THE SAME VIEW, MADE REAL. Edit the attached 3D image into a photograph. Keep the exact camera angle and framing, and keep the walls, glass, ceiling beams, lights, doors, furniture and objects in the same places. Change only the look: real materials, real light and a few people. Do not move, add or remove architecture. Do not add windows, outdoor views or extra plants.
B = A CLOSER MOMENT IN THE SAME ROOM. The same room, materials and light as A, with a closer camera (lens given) and one human moment.

Every image: landscape 1536 x 1024. It looks like a real professional photograph: full-frame camera, straight verticals, soft natural shadows, real textures. Colours are vibrant but true: indigo, terracotta, jute gold, leaf green, rice white. Never an illustration, a 3D render or a collage.

The same fictional people in every image where they appear:
- Buyer A: European woman, about 55, short silver bob, tortoiseshell glasses, navy linen blazer over an ivory knit top.
- Buyer B: Black European man, about 35, close-cropped hair, short beard, light grey merino crew-neck, olive chinos, black sketchbook.
- Buyer C: European woman, about 40, dark curly shoulder-length hair, sage-green linen shirt dress, small notebook.
- Host 1: Bangladeshi woman, about 30, deep green salwar kameez, cream dupatta, neat low bun.
- Host 2: Bangladeshi man, about 40, light blue shirt, charcoal trousers, rimless glasses.
People never look at the camera. They are warm, respectful and natural, with correct hands.

Rules for every image:
- No readable text, letters, numbers or logos anywhere. The text and logos in the 3D are placeholders: make those signs, cards, screens and boards blank.
- No certification marks, QR codes, prices or charts with figures.
- No flames: lanterns and stoves glow electrically. No candles.
- No solar panels, gardens or outdoor landscapes.
- Never show prayer rooms or washrooms.
- No Chakma or Marma people, dress or patterns.

Name the images S01A, S01B ... S23A, S23B. After each pair, tell me in one line what you kept from the 3D and what you could not keep. Keep the caption I give with each stop: at the end you will put all 46 images and their captions into a PDF.

Reply only "Ready". I will then send stop 01 with its 3D image.
```

## Stop 01 · The whole floor (attach `refs/stop01_ref.jpg`)

```text
Stop 01 · The whole floor. Attached: our 3D view of this stop.

A (the same view, made real): Turn this 3D cutaway into a photograph of a museum-quality 1:50 architectural model of the same floor, roof off, in exactly this layout and from this angle: every room, glass partitions as clear acrylic, miniature furniture, tiny knitwear forms, terracotta, jute and indigo details, tiny trees. It stands on a walnut plinth against a deep green background, in soft studio light. No people.

B (a closer moment): 50 mm. The same model on its plinth in a reception lounge. The three buyers and Host 1 lean over it, and Host 1 traces the visit route with a slim bamboo pointer. The model is sharp in the lower third.

Caption for the PDF: A knitwear factory whose fabric comes from the earth and from what was already made, with Bengal craft as its signature: a concept for the approved STAGE II ground floor. The pilot comes first; option A rooms are a possible later phase.
```

## Stop 02 · Arrival gallery (attach `refs/stop02_ref.jpg`)

```text
Stop 02 · Arrival gallery. Attached: our 3D view of this stop.

A (the same view, made real): Keep the slatted oak brand wall, the check-in desk faced with handmade terracotta tiles, the monitor, the two wooden doors on the left, the glass partition with the hanging handloom on the right, and the white beams and black linear lights. The logo board becomes a blank panel. In the free space at the front left, add a banyan bonsai on a granite plinth and three granite stones. People: Host 1 greets the three buyers as they arrive, her hand on her heart. Warm light.

B (a closer moment): 85 mm. Buyer B's fingertips trace the relief of a terracotta plaque of a doel bird on the lobby wall while Host 1 explains. Grazing light makes the clay texture crisp.

Caption for the PDF: A banyan bonsai on granite by the glass gate, three stones, handmade terracotta on the check-in desk and terracotta plaques by a rural artist (to be commissioned).
```

## Stop 03 · Reception and Bengali tea (attach `refs/stop03_ref.jpg`)

```text
Stop 03 · Reception and Bengali tea. Attached: our 3D view of this stop.

A (the same view, made real): Keep the reception desk, the slatted wall, the dark double doors, the green armchairs, the sofa, the round table, the handloom panels on the right wall and the ring pendant. The logo becomes blank. Add a clay teapot and small clay cups on a wooden tray on the table. On the console at the left, add an oak rail with an ektara, a dotara and a banshi, and a dhol. People: the buyers sit while Host 2 pours tea from the clay pot.

B (a closer moment): 85 mm. Buyer A holds an unglazed clay cup of milky tea with soft steam, smiling. The instruments are softly blurred behind.

Caption for the PDF: Tea in clay, rural instruments above the console, handloom on the walls, a small fig tree and ghritokumari.
```

## Stop 04 · Earth and Sun passage (attach `refs/stop04_ref.jpg`)

```text
Stop 04 · Earth and Sun passage. Attached: our 3D view of this stop.

A (the same view, made real): Keep the corridor. On the left: the low wall of handmade terracotta tiles with clay bowls on its ledge, and glass above it with the office beyond out of focus. On the right: the Sun wall. Make it a softly backlit panel of simple icons and flowing lines, with no words or numbers. People: the three buyers walk towards the camera with Host 1, who points at the Sun wall.

B (a closer moment): 100 mm, along the oak ledge. Four clay bowls hold raw cotton, golden jute fibre, a multicolour tuft of recycled fibre and natural indigo. Buyer C lifts a pinch of jute.

Caption for the PDF: The Sun wall tells the energy story with grid and backup included (a concept, not live data); the earth wall holds the raw side of the fabric story: cotton, jute, recycled fibre and indigo, beside clay.
```

## Stop 05 · Fabric from the earth, and from waste (attach `refs/stop05_ref.jpg`)

```text
Stop 05 · Fabric from the earth, and from waste. Attached: our 3D view of this stop.

A (the same view, made real): Keep the four dress forms in knitwear on the long low plinth, with their small fibre dishes and cards (cards blank). Keep the deep green garment bays with knitwear on brass rails, the blue-and-white natural indigo cloths swagged under the ceiling, the large terracotta kolshi in the right foreground and the track lights. People: the buyers stand mid-room with Host 2 at the first form.

B (a closer moment): 50 mm. Buyer B feels the knit of the oatmeal cardigan on a form while Host 1 holds up the dish of colour-sorted fibre from its foot. Buyer C writes in her notebook.

Caption for the PDF: The approved knitwear stays. Each form and bay shows where its fabric could come from: cotton, a jute and cotton blend (research), cutting waste sorted by colour and spun again, and used garments taken back. Illustrative until records arrive.
```

## Stop 06 · Second life in the bays (attach `refs/stop06_ref.jpg`)

```text
Stop 06 · Second life in the bays. Attached: our 3D view of this stop.

A (the same view, made real): Keep the forms, the green bays, the hanging knitwear and the shelves. At the foot of the bays, make these real: small jute sacks of fabric offcuts sorted by colour, yarn cones in the same colours, and a wooden crate of folded used T-shirts. People: Buyer A crouches to compare a yarn cone with its sack, and Host 1 kneels beside her.

B (a closer moment): 85 mm. Host 1 and Buyer A hold a grey jersey T-shirt whose tear is mended in red kantha running stitch. The stitch is razor sharp.

Caption for the PDF: Jute sacks of offcuts sorted by colour and the yarn spun from them, a take-back crate and a T-shirt mended in kantha stitch, under the approved garments.
```

## Stop 07 · The jhut river (attach `refs/stop07_ref.jpg`)

```text
Stop 07 · The jhut river. Attached: our 3D view of this stop.

A (the same view, made real): Keep the table with the sewing machine and the patchwork river of colourful jersey offcuts running off it across the floor. Keep the dress forms on the plinth, the green bays and the yarn cones in the right foreground. The brand board at the back becomes blank. Make the patchwork real fabric: jersey and rib with visible seams. People: the three buyers stand at the river's end, and one bends to look.

B (a closer moment): 35 mm, camera at floor level. The patchwork is sharp in the foreground, rising to the sewing machine. Buyer B crouches and runs his hand over it.

Caption for the PDF: A sewing machine and a river of patchwork pieced from cutting waste, running off the table and across the floor, under natural indigo cloths. An installation; makers to be credited.
```

## Stop 08 · Option A · the Green Uthan (attach `refs/stop08_ref.jpg`)

```text
Stop 08 · Option A · the Green Uthan (option A, a possible later phase). Attached: our 3D view of this stop.

A (the same view, made real): Keep the courtyard: the terracotta brick bot-tola seat around the white column, the bamboo canopy with kula and dala trays, the painted bamboo posts with lanterns (electric glow), the small trees, the alpana on the floor, the jute carpet, the bamboo chair in front and the ceiling baffles. People: the buyers sit on the bot-tola, chatting with Host 1.

B (a closer moment): 35 mm, looking up from the seat. The kula and dala form layered silhouettes, with warm light through the woven bamboo. Skeins of indigo and undyed yarn and small clay pots hang from the canopy. Buyer C looks up.

Caption for the PDF: A possible later phase, only if the merchandising team moves: a Bengali courtyard around the column, a bot-tola seat, small trees under grow lights, kula and dala over a bamboo canopy, alpana, electric hurricane-form lanterns and natural indigo yarn.
```

## Stop 09 · Option A · artisan corner (attach `refs/stop09_ref.jpg`)

```text
Stop 09 · Option A · artisan corner (option A, a possible later phase). Attached: our 3D view of this stop.

A (the same view, made real): Keep the room: the shelves with painted pots, the baskets, the tables, the kantha frame on the low table and the basket pendant. REMOVE the back-strap loom and its strap (consent rule) and put a sitalpati mat there. People: an older Bangladeshi woman embroiders at the nakshi kantha frame, and a man shapes a cane basket. Two buyers sit on low stools at their level, listening, while Host 1 translates.

B (a closer moment): 100 mm macro. The embroiderer's hands pull red thread through a lotus-and-fish kantha motif while a buyer's finger points at the motif.

Caption for the PDF: Demonstrations by invitation, never as a spectacle: nakshi kantha, cane, painted shokher hari pots, tepa putul dolls and drums. Chakma and Marma work only with the weavers' consent.
```

## Stop 10 · Option A · circular knitwear studio (attach `refs/stop10_ref.jpg`)

```text
Stop 10 · Option A · circular knitwear studio (option A, a possible later phase). Attached: our 3D view of this stop.

A (the same view, made real): Keep the bamboo canopy with its trays and lanterns, the bot-tola, the bonsai and small trees, the alpana rug, the tables with yarn cones, the live-edge mending table and the basket lamps. Make these real: offcuts sorted into colour piles on the sorting table, jute sacks, bamboo rails of knitwear and woven jute take-back bins. People: the buyers move between the stations with Host 2.

B (a closer moment): 50 mm, at the live-edge mending table under a basket lamp. A Bangladeshi embroiderer (a woman, about 35) guides Buyer B's first kantha running stitch on a sweater elbow.

Caption for the PDF: Wear, remake, repair and return around the Uthan: knitwear on bamboo rails, cutting waste sorted by colour, kantha mending and take-back bins. Illustrative.
```

## Stop 11 · Option A · craft corner (attach `refs/stop11_ref.jpg`)

```text
Stop 11 · Option A · craft corner (option A, a possible later phase). Attached: our 3D view of this stop.

A (the same view, made real): Keep the bamboo trellis with the gamchha, kantha, kula, round baskets and framed painting, the large nakshi kantha on the left wall, the cane bowl chair, the bamboo armchair, the round sitalpati, the jute pouf, the snake plant and the rail of T-shirts. People: Buyer A sits in the cane chair, laughing, while Host 1 shows her a mathal (the farmer's palm-leaf hat).

B (a closer moment): 85 mm still life. A low bamboo shelf holds painted shokher hari pots (white ground; red, yellow and black fish and flowers), tepa putul clay dolls, a dholak and a khol. Buyer B's hand lifts a tepa putul.

Caption for the PDF: A bamboo trellis with a gamchha, a kantha, a kula and a painting by a rural artist (to be commissioned), a cane bowl chair, a jute pouf and bamboo armchairs. Makers to be identified, paid and credited.
```

## Stop 12 · Option A · design academy (attach `refs/stop12_ref.jpg`)

```text
Stop 12 · Option A · design academy (option A, a possible later phase). Attached: our 3D view of this stop.

A (the same view, made real): Keep the glass suite, the rows of wooden tables and woven chairs, the screen at the end and the linear lights. People: about 16 young Bangladeshi design students, men and women, at the tables (never more than 20 seats). At the front, a tutor demonstrates at a bench with a sewing machine, and the screen shows a close-up picture of a stitch (no text). The three buyers watch from the back.

B (a closer moment): 50 mm. Buyer B and a student stand at a pin-up board, discussing a pinned knit cardigan sketch and swatches (drawings only).

Caption for the PDF: A possible later phase, only if the accounts team moves: 20 seats inside the existing glass suite, a demonstration bench with a sewing machine and a tutor room. The fire engineer sets the capacity.
```

## Stop 13 · The making line (attach `refs/stop13_ref.jpg`)

```text
Stop 13 · The making line. Attached: our 3D view of this stop.

A (the same view, made real): Keep the long white wall with the oak ledge and its six groups of objects (cotton bolls, yarn cones, knit fabric, cut panels, a test swatch, finished T-shirts), and the glass corridor on the left. Make the title band and all the step cards blank (no letters). People: the buyers walk along the line with Host 2, who points at the first step, the cotton.

B (a closer moment): 100 mm along the ledge, from the yarn cones to the knit fabric, shallow focus. Buyer B stretches a piece of jersey between his hands.

Caption for the PDF: At the entrance to the design wing: one T-shirt in six steps, from fibre to yarn, knit fabric, cut and sew, test, and wear and return. Illustrative objects; real samples and records replace them.
```

## Stop 14 · The labs behind the glass (attach `refs/stop14_ref.jpg`)

```text
Stop 14 · The labs behind the glass. Attached: our 3D view of this stop.

A (the same view, made real): Keep the lab bench with its terrazzo top and white cabinets, the test items on it (papers, swatch cards, a small device, a round cutter, swatches) and the large interior window. The room beyond the window is softly out of focus. People: a lab technician (a Bangladeshi woman, about 30, white lab coat, hair tied back) cuts a circular fabric sample with a round cutter while Buyer C and Host 1 watch.

B (a closer moment): 85 mm. An open, empty logbook beside a circular knit sample on a precision balance (display turned away), a grey scale card and swatches with stitched marks. The technician's hand places the sample.

Caption for the PDF: A fabric lab with an empty durability log (no results until tests are done), the fibre library with product passport cards next door, and remake and repair in the sample room.
```

## Stop 15 · CAD · knitwear development (attach `refs/stop15_ref.jpg`)

```text
Stop 15 · CAD · knitwear development. Attached: our 3D view of this stop.

A (the same view, made real): Keep the desks with dual monitors, the big pattern table on the right, the wall screen, the linear pendants and the dark floor. The monitors and the wall screen show line drawings of a knit cardigan (no text). People: a pattern maker (a Bangladeshi man, about 30) works at the monitors, Buyer B leans in and points at the neckline, and Host 2 stands at the pattern table.

B (a closer moment): 50 mm, top-down onto the pattern table. A knit cardigan lies flat beside brown-paper pattern pieces, a tape measure, pencils, a yarn cone and swatches. Two pairs of hands adjust a piece.

Caption for the PDF: The approved CAD room: one illustrative knit cardigan from flats to pattern, grading and marker. In the concept every style also carries a product passport.
```

## Stop 16 · Academy annex (pilot) (attach `refs/stop16_ref.jpg`)

```text
Stop 16 · Academy annex (pilot). Attached: our 3D view of this stop.

A (the same view, made real): Keep the table with the green chairs, the pin board of swatches on the left wall, the whiteboard (blank), the green sofa lounge and the plant. People: exactly six trainees (factory staff, Bangladeshi, men and women) sit around the table with knit swatches, yarn cones and a mending kit. A trainer stands, and the buyers sit in from the lounge sofa.

B (a closer moment): 85 mm. A young woman trainee shows Buyer A a swatch she has just mended in kantha stitch. Pride and warmth.

Caption for the PDF: The pilot academy before any room changes: a class of six learning fibre, knit and repair, and a wall of student work.
```

## Stop 17 · The tong · tea in clay (attach `refs/stop17_ref.jpg`)

```text
Stop 17 · The tong · tea in clay. Attached: our 3D view of this stop.

A (the same view, made real): Keep the tea cart with its two green spoked wheels and canopy, the painted kettles hanging, the lantern, the kettle on the clay stove, the cups and jars, the wood-slice stools, and the fridge and pantry on the right. Paint the canopy in rickshaw-art flowers and borders with NO letters. The lantern and stove are electric (no flame). People: a tea maker in a neat apron pours tea from height into clay cups while the buyers and factory staff sit together on the stools, laughing.

B (a closer moment): 50 mm. Buyer B and a sample-room operator (a Bangladeshi woman in work clothes) touch clay cups in a toast, both laughing. The painted canopy and the lantern are soft behind.

Caption for the PDF: Staff and artisan dining with a Bengali tea stall: a cart front on two wheels, tea in clay cups, an electric lantern in the hurricane form (no kerosene indoors) and wood-slice stools.
```

## Stop 18 · Collaborative studio (attach `refs/stop18_ref.jpg`)

```text
Stop 18 · Collaborative studio. Attached: our 3D view of this stop.

A (the same view, made real): Keep the long sample-review table with grey chairs, the garment rail on the right wall, the windows on the right, the desks and the green living wall at the far end. Soft daylight comes through the windows (sheer blinds, no outdoor view) and falls across the table, which is laid with knit samples and swatches. People: the buyers and the design team (4 to 5 people) are in a review.

B (a closer moment): 50 mm, backlit. Buyer A holds a knit swatch up to the window light to read its structure, with Host 1 beside her.

Caption for the PDF: The only room with daylight: the approved sample-review table, and a small fig tree by the window.
```

## Stop 19 · The sunning shelf (attach `refs/stop19_ref.jpg`)

```text
Stop 19 · The sunning shelf. Attached: our 3D view of this stop.

A (the same view, made real): Keep the oak shelf on its stone base under the large window, the three bonsai and the small plant in pots, the fig tree in the terracotta pot on the left and the desk edge. The window gets soft daylight through a sheer blind (no outdoor view). People: Host 1 explains to Buyer C that the trees take turns here for daylight.

B (a closer moment): 100 mm macro. The banyan bonsai's aerial roots and small leaves catch the sun, with tulsi leaves soft behind and a fingertip near a leaf.

Caption for the PDF: Bonsai and tulsi take turns in the daylight of window W10.
```

## Stop 20 · The living wall (attach `refs/stop20_ref.jpg`)

```text
Stop 20 · The living wall. Attached: our 3D view of this stop.

A (the same view, made real): Keep the sage-green wall with eight organic wooden ring niches glowing warm from within, holding snake plant, trailing money plant and peace lily. Keep the two small fig trees, the desks with monitors in front and the swatch wall on the left. People: one buyer stands before the wall, small in the frame.

B (a closer moment): 85 mm, at an angle along the wall. The backlit edge of a niche, the white flowers of the peace lily and the trailing money plant, with Buyer B and Host 2 talking behind.

Caption for the PDF: At the north end of the studio: organic wooden niches with a warm backlight, snake plant, money plant and peace lily, and a small fig tree either side. No medical claim.
```

## Stop 21 · The records room (attach `refs/stop21_ref.jpg`)

```text
Stop 21 · The records room. Attached: our 3D view of this stop.

A (the same view, made real): Keep the table with the row of green box files, the framed board on the wall (rows of blank lines, no text), the chairs, the white cabinets and the pendant. People: Buyer C reviews an open, almost empty folder with a compliance officer (a Bangladeshi woman, about 30, navy salwar kameez).

B (a closer moment): 50 mm. The compliance officer hands a plain kraft folder to Buyer C. The focus is on the hands and the folder, with the box files soft behind.

Caption for the PDF: The originals behind every claim, fibre origins and recycled content first. Until documents arrive, every line of the Open Record reads none yet, to prepare or to be collected.
```

## Stop 22 · Negotiation suite (attach `refs/stop22_ref.jpg`)

```text
Stop 22 · Negotiation suite. Attached: our 3D view of this stop.

A (the same view, made real): Keep the long boardroom table and black chairs, the wooden slat walls, the green ceiling panels, the screen at the end (dark), the painting, and the glass wall on the right with the knitwear forms beyond. Make these real: a small clay cup at every place, a clay jug and knitwear review trays. Add a bonsai on a jute-wrapped stand by the screen. People: the three buyers and two Bangladeshi factory directors in a warm discussion.

B (a closer moment): 50 mm. Buyer A and a factory director examine a knit sample together, both smiling, with clay cups in the foreground. No papers being signed.

Caption for the PDF: The visit ends here: tea in clay at every place, the approved knitwear review trays, a bonsai in the corner.
```

## Stop 23 · Designed for a Solar-Powered Future (attach `refs/stop23_ref.jpg`)

```text
Stop 23 · Designed for a Solar-Powered Future. Attached: our 3D view of this stop.

A (the same view, made real): As at stop 01: turn this 3D cutaway into a photograph of the same 1:50 architectural model from this opposite angle. Light it with one warm, low side light like late sun, with long shadows, against a deep green background. No people and no solar panels.

B (a closer moment): 35 mm, in the arrival gallery of stop 02 (use your S02A image as the room). The buyers leave through the glass gate into soft, bright light. Buyer A turns back to wave, and Host 1 and Host 2 see them off with their hands on their hearts.

Caption for the PDF: Every claim on this floor waits for its evidence: fibre origins, recycled shares, durability tests, makers, water reports and measured energy. Next: the full export and order centre once HR moves.
```

## Last message · the PDF (send after stop 23)

```text
Now build the PDF from all 46 images.
- A4 landscape, 26 pages, English digits 0-9 only. Background #F7F3EA, text #1F3A2E, accent #B5532D. Images as JPEG quality 85 at full size; the PDF stays under 40 MB.
- Page 1, cover: S07A full page. Title "STAGE II · Zara Fashion". Subtitle "The ground floor, reimagined: a buyer's visit in 46 pictures". Line: "Knitwear from the earth and from recycled fabric, with Bengal craft · a concept for the STAGE II ground floor · October 2026".
- Page 2: "How to read this book: this book follows one buyer team through the 23 stops of the guided tour of our 3D proposal. Each stop has two pictures: A, the room as the 3D model shows it, made real; B, a moment in it. Stops 8 to 12 show option A, a possible later phase." Then a list of the 23 stops.
- Pages 3 to 25, one page per stop:
  - "STOP 05 / 23", the stop title and the caption I gave;
  - images A and B side by side, with "A · The room" and "B · The moment" under them;
  - stops 8 to 12 get a small tag "Option A · possible later phase".
- Page 26, closing: "What these pictures are: AI-generated concept visualisations based on the 3D model of the approved STAGE II ground floor. They are not photographs. Every person in them is fictional. What is still to be proven: fibre origins, recycled shares and their certificates; durability and colourfastness tests by an accredited laboratory; laboratory reports for the drinking water and for clay glazes; the names of the makers, artists, embroiderers, growers and stone sources, each to be identified, paid and credited; and measured energy data. Chakma and Marma work is shown only with the communities' consent. The plan: the owner chose the pilot first (option C); the option A rooms (stops 8 to 12) are a possible later phase."
- Footer on every page: "AI concept visualisation based on the 3D model · not a photograph · people are fictional · fibre origins, recycled shares, tests, makers and energy data are still to be verified".
- If you cannot reach your images from Python, tell me and I will upload them.
```
