# M1.C4 revision 7 — Trace the supplied designs at Brendan's scale

**Delivered for visual review; not approved game art.** The user rejected R6's flattened heads and requested five grids, with Brendan first and the actual four character references aligned over him. This pass transfers those references at one uniform whole-figure scale. It preserves the rounded afro, tall flat-top, hanging twists and curved cornrows, along with the four supplied outfits.

Primary local review: [Brendan and all four designs on five full grids](/Users/tanoshi/.codex/visualizations/2026/10/03/hero-revision-7/five-character-grid.png). Supporting evidence: [actual source references over a faint Brendan guide](/Users/tanoshi/.codex/visualizations/2026/10/03/hero-revision-7/reference-registration.png). These reference-colored plates stay outside the repository because the build copies documentation. They are local review artifacts, not deployed URLs.

Repository-safe review copies: [four gridded candidates](four-heroes-grid.png), [larger 2×2 grids](four-heroes-grid-2x2.png), [native and enlarged inspection](native-and-clean-check.png). Each cell is one native pixel at integer 12× enlargement, with a pink x=16 symmetry line and numbered horizontal guides every ten pixels. All 32×64 frame cells remain visible; Y=0 is at the bottom, Y=64 at the top. Native PNG rows still count downward.

## What changed and why

R4 used Brendan's hat peak as a skull/hair target. R6 then independently shortened the heads and mistook the bottom of his hat for every bare head's hairline. The resulting cornrows became a flat cap, and the supplied proportions were lost. Both rules are now revoked in ART_BIBLE. Hair, visible face, underlying cranium and headwear are distinct. A covered forehead cannot establish a bare head's hairline.

This is a **reference-traced native transfer**, not a new hand-drawn sprite or a byte-exact copy of a screenshot. The complete 738×248 four-design reference supplied at 9:09:44 PM is used because the latest zoom of the same concepts slightly crops the shoes. The latest supplied zoom was inspected to confirm hairstyle and outfit identities. The complete reference SHA-256 is `5cf9265179561a25429e1e7347cec5c52d41e858b404b5c71dd21fe58764ab15`.

The process removes the paper background, positions each complete source figure with the same scale in X and Y, samples coverage/colors into the native grid, and reduces each result to 24 opaque colors without dithering. Paired source coverage corrects body silhouette asymmetry below native row 37; the eyes are set to the same mirrored 2×4 boxes. Hair and shading are not RGB-mirrored. Small exterior paper-color remnants are cleaned using existing dark palette colors. No independent head, hair or limb scaling is applied. No image-generation model was used for this deterministic source transfer.

The exported PNGs have binary alpha and exact native pixels. Screenshot-derived color clusters still need artistic review; 24 colors here is a review method, not a new production palette approval. The editor's separate Wildlife palette is unchanged. The anatomical zone map is an inspection guide, not a recovered skeleton or a precise segmentation of every garment boundary. The symmetric cranium guide is inferred construction. Technical checks do not establish that the artwork is visually approved.

## Files and checks

| Design | Native PNG | Editable source | Painted bounds |
| --- | --- | --- | --- |
| A — afro, teal/cream raglan | [PNG](a-afro.png) | [JSON](a-afro.json) | 24×38 |
| B — flat-top, gold vest | [PNG](b-flat-top.png) | [JSON](b-flat-top.json) | 24×39 |
| C — twists, red/cream stripes | [PNG](c-twists.png) | [JSON](c-twists.json) | 24×38 |
| D — cornrows, blue jacket/olive shorts | [PNG](d-cornrows.png) | [JSON](d-cornrows.json) | 24×37 |

[Measurements and provenance](MEASUREMENTS.md) distinguish source facts from original construction. [Validation](validation.json) records 8,192 decoded native cells, 34,816 displayed grid cells and 3,456 paired anatomical-zone cells checked. All four have connected silhouettes, binary alpha, 24 opaque colors, mirrored body alpha below row 37, mirrored eye boxes, common feet/anchor alignment and uniform source transforms. Native exports equal the saved source transfers. Brendan's source pixels remain unchanged. Grid cell-center colors, upward major guides and symmetry lines match their native sources. Native, clean enlarged, five-grid and actual-reference-overlay images were visually inspected.

Rebuild with Python 3 and Pillow:

```sh
python3 docs/reviews/M1-C4/revision-7/build.py
python3 docs/reviews/M1-C4/revision-7/verify.py
```

Passing an external review directory as the final argument to both commands also rebuilds/checks the five-grid reference plate. That directory must contain `brendan-reference.json` and the four `*-reference-cutout.png` files. `trace-reference.py COMPLETE_REFERENCE EXTERNAL_DIRECTORY` reproduces source registration/transfers from the complete screenshot; the checked-in indexed JSONs are the authoritative editable native sources. Reference inputs and copied reference pixels must remain outside the project. No browser storage or game tests are needed for this static review-only change.

## Scope and handoff

Front idle only. No walking, back pose, roster expansion, save changes, runtime consumers or accepted gameplay artwork changes. AGENTS already points exclusively to ART_BIBLE for art direction and needs no further duplicate specifications. The requested corrections and mistakes are recorded there. Work is on `main`; task-related review/docs changes are committed and pushed, with the verified receipt in PROJECT_STATUS. Unrelated game/editor work is preserved. The playable build is unchanged and no deployment is required.

Next action is visual review of these five aligned figures; continue the selected still before animation. No artwork approval is inferred from delivery or validation.
