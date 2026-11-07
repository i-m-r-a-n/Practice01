# Woven Earth: prompts for AI images made from the 3D renders

The owner's book "Woven Earth" is an AI render brief. These prompts let ChatGPT (or another image model) make photoreal AI concept images of the six views the brief asks for. Each prompt pairs with one render of this 3D model as its base image.

## How to use them

1. Open the render named under the view (on the images page, or in `concept-images/`) and download it at full size.
2. Attach it to a new ChatGPT image request.
3. Paste the shared rules, then the view's own prompt.
4. Label the result as an AI concept image. If it shows people, say they are fictional. It is not a photograph.
5. Compare it with the render before using it. If anything moved or was added, ask for the correction prompt at the end.

## Shared rules (paste first, every time)

```
Use the attached image as the geometric ground truth. It is a render of the 3D model of the ZF Zara Fashion
Stage II arrival gallery and reception. Make a photoreal editorial interior photograph of exactly this view.

Geometry lock: keep the camera, column grid, steel beams, ceiling height, glazing, doors, check-in desk, brand
wall and its sign, corridors, floor boundaries and circulation exactly as shown. Do not add, move or remove any
opening, column, desk, sign or light fitting.

The design is "Woven Earth / The Woven Threshold": serene, modern Bangladeshi industrial interior; gallery-grade,
quietly monumental; not bohemian, not ethnic-themed, not luxury hotel.
- The hero: six shallow handwoven swags hung on a laminated-bamboo frame with straight bamboo culms, black steel
  drop rods and cotton tapes. Strips of cleaned textile offcuts (jhut) with natural jute and cotton, interlaced by
  thin weft rows, with hemmed ends. Ecru and sand, with one accent block per swag (forest olive, dusty indigo,
  charcoal indigo, a very small amount of clay). One restrained rhythm, not a rainbow. Believable folded hems,
  weave irregularity, precise anchoring. Lowest point 2.30 m.
- One hand-pressed terracotta wall with raised diamonds in a half-drop repeat (Jamdani logic), lit by a linear
  wall-washer.
- One salvaged-hardwood bench on laminated-bamboo trestles (through-tenons, hardwood wedges, dowels), a light
  bamboo stool with a cane seat.
- One real fig tree in a terracotta planter by the entrance glass.
- Terrazzo floor as shown; off-white plaster; matte black metal; clear glass.

Lighting: daylight only from the existing entrance glass; soft daylight plus linear light at 3000-3500 K; two
narrow spots on the textile; no glowing fabric, no theatrical light pools.
Photography: 28-35 mm rectilinear look, verticals straight, restrained saturation, no people.

Negative: no imaginary openings, shifted columns, floating furniture, low fabric across exits, fake equipment,
duplicate doors, extra desks, random signs, fake certifications or QR codes, overscaled bonsai, glossy CGI, HDR,
fog, bloom, fisheye, warped letters, folk props, boho styling, hyper-luxury marble, clutter, plastic bamboo,
pastiche.

Before you output, check the image against the attached render: every wall, opening, beam, desk and sign must
be where it is in the render. Fix any difference first.
```

## The six views

| # | View | Base image |
|---|---|---|
| 1 | The arrival camera, before and after | `render_CAM_03_Entrance_Lobby.jpg` (after); the before is `model/render_CAM_03_Entrance_Lobby.jpg` |
| 2 | A reverse view towards the entrance | `render_BEL_CAM_WOVEN_REVERSE.jpg` |
| 3 | An eye-level close view of the woven installation and its fixings | `render_BEL_CAM_WOVEN_CLOSE.jpg` |
| 4 | A 50 mm detail of the bench and bamboo connection | `render_BEL_CAM_WOVEN_BENCH.jpg` |
| 5 | Reception and brand wall | `render_CAM_01_Reception_A.jpg` |
| 6 | A night lighting check | `render_CAM_03_Entrance_Lobby_night.jpg` |

### Prompts for each view (paste after the shared rules)

1. **The arrival camera:** "The first view on entry: the woven swags fill the upper right, framed by the steel beam and the brand wall. Keep the 19 mm framing of the base image."
2. **Reverse view:** "Looking back towards the glass entrance from the reception door: the swags overhead, the fig tree in the entrance daylight, the exit sign visible below the swags."
3. **Close view:** "Looking up at the swags and their fixings at eye level: the culms through the rails, the steel saddles and drop rods, the cotton tapes, the weave and the hems sharp. One strip carries a small kantha repair in indigo running stitch."
4. **Bench detail:** "A 50 mm detail at seat height: the end grain and checks of the salvaged slab, a butterfly key across one check, the bamboo through-tenon split by a hardwood wedge, the dowels. The terracotta wall softly behind."
5. **Reception:** "The approved reception desk and its brand wall as they are; tea in clay cups on the coffee table; on the console, one oak tray of raw cotton, jute fibre, folded offcuts sorted by colour, recycled yarn and a knit swatch."
6. **Night check:** "The same arrival view at night: no daylight; the glass is dark; only the linear lights, the brand-wall spots, the two narrow spots on the swags and the terracotta wall-washer light the room. Calm, not theatrical."

## Correction prompt (from the brief)

```
Reduce decorative density by 30%. Keep the woven installation as the only hero element. Restore the original
architecture exactly from the attached render. Remove any added doors, columns, desks, signs, plants or props.
```

## Honesty

- An AI image is a concept visualisation. Its details can differ from the 3D.
- It proves no material, maker, source, test or certificate.
- The makers, weavers, fabricator, suppliers, fibre sources and fire tests are all still to be identified.
- The design still needs architect and engineer review, local fire and building compliance, and real contractor quotations.
