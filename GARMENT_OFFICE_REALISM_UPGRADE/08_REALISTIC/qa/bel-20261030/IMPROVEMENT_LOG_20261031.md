# Ten-hour improvement run: 31 Oct 2026, from 20:35 UTC

**The owner, 31 Oct:** "eirokom sundor kore banao and factory te jeno phone dea walk kora jai oi system koro next 10hours keep improving". In English: make it as beautiful as these images (12 ChatGPT images made from our 3D frames), and build a system to walk the factory with a phone. Keep improving for the next 10 hours.

**Scope:**
- Only the proposal route: `/stage2-concept/` (the old `/bengal-earth-lab/` redirects there).
- Every change sits behind route-config flags, so `/realistic/` and `/` stay unchanged.
- Deploys go through ChatGPT, with one tested Worker per deploy request on issue 12.
- Deploy request 4 (`743ffd8`: the new address and the walk arrows) is waiting.

## Plan

1. **Phone walking:**
   - the arrow pad also works as a joystick (slide in any direction, analog speed);
   - tap the floor to walk there;
   - "Look by moving the phone" (device orientation; iOS asks for permission);
   - a first-time help card on phones.
2. **The owner's images in the tour**, labelled honestly as AI concept images with fictional people:
   - 9 tour stops: 2, 3, 4, 8, 14, 15, 17, 20 and 22;
   - 3 room views: MD office, fibre library, sample room.
3. **A warmer, softer real-time look** on this route, compared against the images and the Cycles render.
4. **Cycles stills from the 3D itself** for the other stops, if time allows.
5. **Deploy package:** Worker, tests, deploy request and report.

## Progress

- 20:35 UTC: plan written.
- **21:54 UTC (commit `3f4ca1e`), phone walking done:**
  - A finger slides from one arrow to another to change direction. Taps between the arrows reach the model.
  - A tap on the floor (a click on a computer) walks there:
    - the view turns towards the point like a person;
    - the walk stops on arrival or when blocked;
    - a green ring marks the point;
    - the minimap walks there too.
  - "Look by moving the phone" works with device orientation; iOS asks for permission. Dragging still turns the view.
  - On phones, a first-time help card.
  - While walking on a phone, a one-line room card; tap the room name to open it. The view starts slightly down, so the floor ahead shows.
  - Computers drag to look; mouse capture is off on this route.
  - Taps are timed by input time, not frame time.
  - Checks: `bel_phone_walk_check.py` passes on phone and desktop (`after-phone-walk/`). The arrows check passes, and the 23-stop tour passes.
- **21:54 UTC (the same commit), the owner's images in the tour:**
  - 12 images in `concept-images/`, named by camera:
    - 9 tour stops: 2, 3, 4, 8, 14, 15, 17, 20 and 22;
    - 3 rooms: MD office Z12, fibre library Z15, sample room Z17.
  - The tour switch "Show concept images" starts on. Each image fades in at its stop.
  - The label reads "AI CONCEPT IMAGE · made from the 3D views · people are fictional · not a photograph".
  - A room card offers "Concept image".
  - On upright phones the image fits whole, above the tour card.
  - The footer now says the 3D has no people and the concept images show fictional people.
  - Checks: `bel_stills_check.py` passes on desktop and phone (`after-stills/`); all 12 images load. The 23-stop tour passes with the images on (`after-tour-play-stills/`).
- **From 22:05 UTC, renders from the 3D for the stops without an AI image:**
  - Each view is exported from the page (three.js GLTFExporter) and rendered in Blender 5.2 Cycles with the camera's own lens and shift.
  - Interior views are lit only by the 3D's real light fittings (`led_3000`, `led_3500`, bulbs, lanterns, niche lights). The web view's painted light pools are hidden and the self-lit helpers are switched off. A warm, soft fill stands in for light bouncing off the walls.
  - Stop 1 uses the whole-floor render (`render_CAM_ISO_SE.jpg`).
  - Batch 1: stops 5, 6, 7, 9, 10, 11 and 12. Batch 2: stops 13, 16, 18, 19, 21 and 23.
  - The renders get their own label ("RENDERED FROM THE 3D MODEL · … · no people"); the AI images keep theirs.
  - `concept-images/README.md` explains both kinds.
  - Batch 1 finished at 22:32 UTC: stops 5, 6, 7, 9, 10, 11 and 12, each 214 to 254 seconds.
  - 22:38 UTC: the leaves rendered grey, because Blender's importer drops three.js instance colours. The export now bakes them into vertex colours, so the trees, bonsai and tulsi are green, and the sorted offcuts keep their colours. Stop 10 is rendered again.
  - Batch 2 started at 22:39 UTC: stops 19, 10 (again), 13, 16, 18, 21 and 23, and stop 1 again (green trees).
  - The render tools and their README are in `qa/bel-20261030/cycles-render/`.
- **The welcome screen's Walk choice** has phone wording on touch screens. The link `?walk=1` starts walking straight away; this is useful to send to a phone.
- **About 22:45 UTC, the tour in images:**
  - It is one grid of every tour stop's image, in tour order. Each card shows its stop number, title and kind: gold for "AI concept image · fictional people", green for "Rendered from the 3D model · no people".
  - A note above the grid says what both kinds are, and that none of them is a photograph.
  - A tap on a card starts the tour at that stop, so the image leads straight into the 3D.
  - It opens from the toolbar ("Images"), as a fourth choice on the welcome card, with the key I, or with the link `?images=1` (useful to send to a phone).
  - Phones get two columns of 640 px copies of the images, about 48 KB each (`concept-images/thumbs/`, made by `viewer/make_concept_thumbs.py`).
  - Check: `bel_gallery_check.py`, desktop and phone.
- **While a phone walks, the footer note is one line;** a tap shows the whole note. This gives the view about 40 px more on a phone; a computer keeps the whole note. `bel_phone_walk_check.py` checks it.
- **About 22:50 UTC, phones held sideways** (844 × 390, 667 × 375):
  - Before, the two-row header, the stacked room card and arrows, and a two-line footer left the 3D only a thin band in the middle.
  - Now the header is one row and the footer is one line (a tap shows the whole note).
  - While walking, the room card sits at the left and the arrows under the right thumb.
  - The welcome card shows its four ways in two columns.
  - Check: `bel_landscape_check.py`.
- **Fixes:**
  - On a phone, the walk help card stayed over the tour when "Got it" was not pressed. It now leaves with walking and returns next time.
  - A stop image's alt text named the camera id. It now names the kind and the stop or room.
- **`run_checks.sh`** runs all the browser checks of this route one after another and saves their screenshots as JPEG.
- **23:07 UTC, renders done:** all 23 stops have an image: 9 AI images and 14 renders, plus the 3 room images. `qa/bel-20261030/stop-images-contact-sheet.jpg` shows them in tour order, and was sent to the owner.
- **Two layout fixes, found in the screenshots of the checks:**
  - **The cards of "Images":** the grid squeezed its rows and cut off each card's stop, title and kind. Now the rows keep whole cards and the grid scrolls; the check measures each card.
  - **A phone held sideways:** the image label ran under "Back to 3D", and the tour's concept note covered most of the image. Now the label wraps clear of the button on screens 641 to 1100 px wide, and the note is one line (a tap opens it).
- **23:20 to 23:52 UTC, checks on the final build** (`3d0e779`), in `after-1031c-*/`:
  - landscape, stills (26 of 26 images), arrows, gallery and the 23-stop tour passed on the first run;
  - phone walk failed only on a guessed 30 px limit for the one-line footer (it is 31 px). The check now measures one line from the computed style, and passed on a second run;
  - all 60 requested files exist at the commit.
- **23:58 UTC, deploy request 5** is on [issue 12](https://github.com/i-m-r-a-n/Practice01/issues/12#issuecomment-6550846984) and replaces requests 3 and 4:
  - Worker `97e778d`, 10,742 bytes, SHA-256 `2bbb5325…0062`, source `3d0e779`;
  - 64 + 41 Worker checks pass;
  - the raw bytes on GitHub match.

