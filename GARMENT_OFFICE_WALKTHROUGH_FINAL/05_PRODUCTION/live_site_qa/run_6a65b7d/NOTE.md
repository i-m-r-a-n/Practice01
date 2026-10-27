# Live site check, 27 Oct 2026 09:16 UTC (15:16 Dhaka)

health: variant baked-light, assetCommit ddf99ee, frontendCommit 6a65b7d. Chromium (software GPU), 1280 x 720.
- `live_now_overview.jpg`: the building shell (walls, floors, ceilings) is offset from the furniture.
- `live_now_reception.jpg`: Rooms -> Reception shows one wall filling the screen.
Cause: the baked GLB stores COLOR_0 interleaved with POSITION and NORMAL (24-byte stride, 16-bit); the live code adds the
light floor to every element of the interleaved array, which moves positions and normals. Fix posted on issue #12.
