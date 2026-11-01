# Images shown at the tour stops and rooms of the proposal route

Each image belongs to one 3D view and is named after that view's camera. `viewer/make_bel_config.py` maps them into the route config under `conceptStills`. The page shows each image with the label of its kind.

| Kind | Files | Source | Label on the page |
|---|---|---|---|
| AI concept image | `<CAMERA>.jpg` (12) | The owner made them with ChatGPT from this route's 3D frames and sent them on 31 Oct 2026. | "AI CONCEPT IMAGE · made from the 3D views · people are fictional · not a photograph" |
| Render | `render_<CAMERA>.jpg` | Blender Cycles renders of this route's own 3D scene. They follow the exact geometry and camera, with simulated light and no people. The method is in `qa/bel-20261030/cycles-render/`. | "RENDERED FROM THE 3D MODEL · Blender Cycles, simulated light · no people · not a photograph" |

## Notes

- **The AI images are concept visualisations.** Their details can differ from the 3D, and the people in them are fictional.
- **Neither kind is a photograph or a record.** Neither proves any material, maker, test or data. The route's footer says so.
- **AI images by view:**
  - stops 2, 3, 4, 8, 14, 15, 17, 20 and 22;
  - the MD office (Z12), the fibre library (Z15) and the sample room (Z17).
- **Renders:** the other tour stops (1, 5, 6, 7, 9 to 13, 16, 18, 19, 21 and 23).
- **`model/`** holds renders of the same views as the AI images, made from the 3D model (`render_<CAMERA>.jpg`). At a stop with an AI image, the button "3D model view" swaps in the render, with the render label, so a visitor can see what the 3D really has. "AI concept image" swaps back.
- **`thumbs/`** holds 640 px copies, about 48 KB each, for the tour in images: the grid behind the page's "Images" button. `viewer/make_concept_thumbs.py` makes them; run it before `viewer/make_bel_config.py` whenever an image changes.
- **`qa/bel-20261030/stop_images_film.py`** makes a short film of the same images in tour order. Each shot has its stop number, title and kind label burned in.
