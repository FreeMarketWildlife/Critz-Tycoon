# Construction and coordinate record

## Reference evidence shown before drawing

Pinned Emerald source: `pret/pokeemerald` at `5eff78649e7170a877b961ef0b3da13b81a16038`, Brendan `graphics/object_events/pics/people/brendan/walking.png`, frame 0 south idle. Source SHA-256 `f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1`. Reuse the earlier source measurements; this revision adds no emulator observation. The user's separately reconstructed refined Brendan screenshot has SHA-256 `e1ca0c743d27b40ac411ff32a9094e3b4abb3f0c9e889d7c3cade2042992c8f9` and is already a 32×64-scale example, so it is not doubled again.

| Feature | Pinned native reference → exact 2× basis | Supplied refined Brendan | New four candidates |
| --- | --- | --- | --- |
| Frame | 16×32 → 32×64 | 32×64 reconstructed frame | 32×64 each |
| Full opaque figure including headwear | 14×21 → 28×42 | 26×42 | 26×35 / 26×35 / 26×34 / 26×33; original hair replaces a hat, so equal total height is not required |
| Continuous central face begins | native row 18 → target row 36 | row 36 | baseline row 36; C's locks overlay selected pixels |
| Each eye | 1×2 → 2×4 | 2×4, rows 38–41 | 2×4, same rows/columns |
| Eye rectangles at 2× | [12,38,14,42], [18,38,20,42] | identical | identical |
| Face/ear band height | 5 → 10 | rows 36–45 | rows 36–45, original symmetric contours |
| Face/ear band width | 14 → 28 | 26 | 24; compact original ears, a recorded design difference |
| Chin/neck transition | reference bands end/start at 23 → 46 | rows 45–46 | rows 45–46 |
| Last idle foot row | row 30 → rows 60–61 | final row 61 | final row 61 |
| Ground anchor | (8,32) → (16,64) | placed at (16,64) | (16,64) |
| Hair/skull crown | **not recoverable beneath headwear** | pointed hat peak at row 20 is not skull evidence | skull scaffold top row 30; hair rows 27/27/28/29, labeled original choices |

Face, eyes, jaw/neck, foot and crown-status landmarks were shown in commentary before drawing. The user then corrected the grid convention; their earlier 36 estimate is not used as a fixed size. Previous annotated arm/torso windows remain reference evidence in revision 2, not commands to fill every pixel in those windows. R6 shares a symmetrical original face/body scaffold, downward-hanging arms, separate mirrored hands and compact feet; the source JSON stores both pre-hair anatomical part masks and final visible parts.

## Final review convention: height increases upward

All source coordinates above are top-down native PNG coordinates. Review **edge height** is `Y = 64 - nativeRow`. A PNG cell in row r occupies `[63-r,64-r]` in bottom-up review units. Do not confuse a height coordinate with a region's height.

| Landmark | Native coordinate | Displayed upward height |
| --- | --- | --- |
| Frame bottom / ground anchor | edge 64 | Y=0 |
| Foot bottom edge | edge 62 | Y=2 |
| Foot last painted row | row 61 | cell spans Y=2…3 |
| Neck edge | edge 46 | Y=18 |
| Face top edge | edge 36 | Y=28 |
| Eyes | rows 38…41 | region Y=22…26 |
| Original hidden skull scaffold top | edge 30 | Y=34; construction choice |
| A/B hair top | edge 27 | Y=37 |
| C hair top | edge 28 | Y=36 |
| D hair top | edge 29 | Y=35 |
| Frame top | edge 0 | Y=64 |

## Limits

No exact hidden skull/arm bone measurements are invented. Equal eye/face/body landmarks and silhouette symmetry do not certify visual similarity; the user reviews that. Hair/costume differences and compact original face/ear contours remain visible in the reference comparison. No artwork is self-approved.
