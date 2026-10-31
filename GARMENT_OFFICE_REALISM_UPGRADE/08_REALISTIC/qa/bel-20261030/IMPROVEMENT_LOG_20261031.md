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
- **About 22:40 UTC, phone walking done:**
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
- **About 23:10 UTC, the owner's images in the tour:**
  - 12 images in `concept-images/`, named by camera:
    - 9 tour stops: 2, 3, 4, 8, 14, 15, 17, 20 and 22;
    - 3 rooms: MD office Z12, fibre library Z15, sample room Z17.
  - The tour switch "Show concept images" starts on. Each image fades in at its stop.
  - The label reads "AI CONCEPT IMAGE · made from the 3D views · people are fictional · not a photograph".
  - A room card offers "Concept image".
  - On upright phones the image fits whole, above the tour card.
  - The footer now says the 3D has no people and the concept images show fictional people.
  - Checks: `bel_stills_check.py` passes on desktop and phone (`after-stills/`); all 12 images load. The 23-stop tour passes with the images on (`after-tour-play-stills/`).
