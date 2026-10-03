# M1.C4 R8 — Native pixel-cluster redraw

**Front idle review; visual acceptance pending.** The user requested actual pixel art retaining the four supplied designs and hairstyles, shown at native size with Brendan. Each original sprite is 32×64. The five-character strip is **160×64 at 1×**, with no resized artwork, overlay or grid baked into it.

[Five-character native lineup — Brendan first](/Users/tanoshi/.codex/visualizations/2026/10/03/hero-revision-8/five-characters-native.png). The reference-bearing strip stays outside the project/build. [Original four-character native strip](four-heroes-native.png) stays in the review packet. Order: afro/teal, flat-top/gold vest, twists/red stripes, cornrows/blue jacket and olive shorts.

## Actual pixel authoring

`draw.mjs` authors integer pixel runs and rectangles directly into four empty 32×64 indexed matrices. It draws symmetric anatomical layers, then separately draws the four hairstyles, clothing seams, face/hair shading clusters and compact shoes. The original-character drawing code reads no screenshot, sampled transfer or R7 sprite. It performs no resampling, area averaging, quantization, dithering, filtering or automatic palette extraction. Sharp only encodes the raw pixels. Optional Brendan input is read solely to place his unchanged reconstruction beside the four originals.

The R7 overlay was used visually to retain proportions, not used as an output texture. R8 replaces near-duplicate sampled colors with 15–16 intentional colors per sprite and groups highlights/shadows by material. The Sprite Editor's separate Wildlife bank remains unchanged. These are proposed review palettes, not retroactive global palette approval or an assertion that 2× resolution increases hardware color limits.

| Asset | Native PNG | Editable indexed source | Painted bounds | Opaque colors |
| --- | --- | --- | --- | --- |
| A rounded afro / teal raglan | [PNG](a-afro.png) | [JSON](a-afro.json) | 24×38 | 16 |
| B flat-top / gold vest | [PNG](b-flat-top.png) | [JSON](b-flat-top.json) | 24×39 | 16 |
| C hanging twists / striped shirt | [PNG](c-twists.png) | [JSON](c-twists.json) | 24×38 | 16 |
| D cornrows / blue jacket | [PNG](d-cornrows.png) | [JSON](d-cornrows.json) | 24×37 | 15 |

## Measured scaffold and design choices

Reference basis remains the pinned Brendan south-idle annotation in [REFERENCE_MEASUREMENTS](../../../REFERENCE_MEASUREMENTS.md): frame 16×32 → 32×64; eyes 1×2 → 2×4; reference eyes x=6/9, y=19–20 → boxes `[12,38,14,42]` and `[18,38,20,42]`; final source foot row 30 → target rows 60–61; anchor `(8,32)` → `(16,64)`. These targets were stated before this redraw. Source revision is `5eff78649e7170a877b961ef0b3da13b81a16038`; no new emulator observation is claimed.

All four have those eye rectangles, anchor and last painted row 61. Actual bounds are `[4,24,28,62]`, `[4,23,28,62]`, `[4,24,28,62]`, `[4,25,28,62]`. The supplied refined Brendan reconstruction is separately sourced, unchanged at `[3,20,29,62]` (26×42). Original clothing/head silhouettes are not claimed identical to his. The four design heights are retained from the useful R7 reference alignment; no skull is extended to his hat tip or flattened to his hat edge. Hidden anatomy is original construction, not a verified measurement beneath his hat.

Authoring masks identify skull, ears, eyes, neck, torso, sleeves, hands, hips, legs and feet separately from hair. These masks describe the constructed layers, including occluded regions; they are not recovered biological anatomy. Corresponding anatomical masks mirror exactly. Hair silhouettes and illumination may differ left/right. Final body alpha below row 37 is also mirrored. One-pixel corner decisions are allowed; final clusters are not constrained to doubled 2×2 blocks.

## Verification and delivery

Independent PNG decoding checks **8,192 original native pixels and all 10,240 five-strip pixels**, exact palette/source agreement, binary alpha, connected silhouettes, bounds, eye boxes, mask symmetry, foot alignment and unchanged Brendan pixels. See [validation.json](validation.json). The native lineup and a private nearest-neighbor inspection were visually reviewed. The enlargement is QA only and is not the requested deliverable. Technical checks are not user approval.

Rebuild with Node and Sharp installed at `CODEX_PRIMARY_RUNTIME_NODE_MODULES`:

```sh
node docs/reviews/M1-C4/revision-8/draw.mjs EXTERNAL_REFERENCE_DIRECTORY
python3 docs/reviews/M1-C4/revision-8/verify.py EXTERNAL_REFERENCE_DIRECTORY
```

The optional external directory contains the preserved `brendan-reference.json`; reference pixels may not be written inside the project. Omitting it builds only the four original sprites and their native strip. Verification requires Python/Pillow plus that directory. No reference comparison, source screenshot, generated cache or QA enlargement enters the game build.

ART_BIBLE now clearly separates reference alignment from pixel art authoring, removes the current transfer recipe and honors this native-size presentation override. AGENTS already points there and is unchanged. This is review-only: no animation, runtime asset replacement, collision/save work or deployment. Unrelated workspace changes are preserved. Commit/push evidence is recorded in PROJECT_STATUS. Next action is visual review of the native stills before further animation work.
