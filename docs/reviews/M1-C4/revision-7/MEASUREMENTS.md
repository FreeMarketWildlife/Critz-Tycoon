# R7 measurements and reference registration

Native coordinates use top-left origin and half-open bounds. Review grids use bottom-left origin: native edge row `r` appears at height `Y = 64-r`. Native cell row `r` occupies review heights `[63-r,64-r]`. Hair/headwear-inclusive bounds are not skull measurements.

## Reference basis and doubled targets

Pinned source basis remains pret/pokeemerald revision `5eff78649e7170a877b961ef0b3da13b81a16038`, Brendan walking frame 0, front idle. Source PNG SHA-256: `f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1`. This is source inspection, not emulator observation.

The user's refined Brendan screenshot is a **separate comparison source**. Its R5 reconstruction is retained unchanged: 32×64 frame, 26×42 painted bounds `[3,20,29,62]`, 13 opaque colors. Screenshot SHA-256: `e1ca0c743d27b40ac411ff32a9094e3b4abb3f0c9e889d7c3cade2042992c8f9`. Do not label this reconstruction an untouched ROM sprite or use its hat peak to measure a hidden skull.

| Feature | Native Emerald basis | Doubled target / actual R7 |
| --- | --- | --- |
| Storage frame | 16×32 | 32×64, all four |
| Frame anchor | (8,32) | (16,64), review (16,0) |
| Eye rectangle | 1×2 | 2×4, all four |
| Eye bounds | x=6 and 9; native rows 19–20 | `[12,38,14,42]`, `[18,38,20,42]`; review Y=22–26 |
| Last painted idle foot row | 30 | Doubled rows 60–61; all four end at native edge 62, review Y=2 |
| Brendan full opaque bounds, including headwear | 14×21 (ledger) | Derived 28×42, **not a bare-head silhouette requirement** |
| Supplied refined Brendan bounds | Separate screenshot reconstruction | 26×42; target for comparison, not a claim of identical Hero costumes |
| Skull crown / bare-head hairline | Hidden by reference headwear | Unresolved; symmetric cranium guide is an original inference |

Brendan's central hat-to-face boundary at native row 36 corresponds to review Y=28. It is **not** the hairline required for these uncovered heads. The R6 instruction that shortened them to meet it is revoked.

## Actual source registration

Complete concept reference: 738×248, SHA-256 `5cf9265179561a25429e1e7347cec5c52d41e858b404b5c71dd21fe58764ab15`. Each figure uses **5.25 source pixels per native pixel in both axes**. Source foot edge 239 maps to native edge 62. Source frame-origin Y is −86.5. Each source center maps to native x=16. No part is scaled separately.

| Design | Source crop [left,top,right,bottom] | Source center X | Source frame-origin X | Native painted bounds | Review crown height |
| --- | --- | --- | --- | --- | --- |
| A rounded afro | [15,25,145,243] | 79.5 | −4.5 | [4,24,28,62], 24×38 | Y=40 |
| B flat-top | [205,25,334,243] | 270 | 186 | [4,23,28,62], 24×39 | Y=41 |
| C short twists | [393,25,525,243] | 459.25 | 375.25 | [4,24,28,62], 24×38 | Y=40 |
| D cornrows | [585,25,714,243] | 649.75 | 565.75 | [4,25,28,62], 24×37 | Y=39 |

The common scale preserves each complete design's source head/body proportions; eye boxes are then cleaned to the common target. Native contours below row 37 use paired source coverage. Upper hair silhouettes and color patterns may differ left/right. The underlying symmetric ellipse guide spans approximately x=6–26 and native y=25.5–45.5; it is inferred construction, not independently measured anatomy beneath hair.

Source-relative hands, sleeves, neck, torso and shoes are retained together during registration. Their region labels in the editable sources are inspection zones, not claims that exact Emerald garment or bone boundaries were measured. The Hero silhouettes are two pixels narrower overall than this Brendan reconstruction; preserving the user's supplied designs takes precedence over inventing wider garments to force identical alpha masks. The actual overlay and final five-grid comparison make this difference visible.

All measured coordinates and output hashes are reproducible from the indexed sources and recorded in `validation.json`. Visual acceptance remains unresolved until the user's review; technical correctness alone is not approval.
