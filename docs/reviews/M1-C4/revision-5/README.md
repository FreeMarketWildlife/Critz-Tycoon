# M1.C4 revision 5 — Brendan beside four unchanged Heroes

User requested an exact reconstruction of the supplied enlarged Brendan reference beside the four R4 candidates to diagnose why they look different. No new Hero drawing, animation or art acceptance is implied.

The reference-containing PNGs and recovered indexed reference are intentionally outside the project because the build copies `docs/`. They remain review-only and cannot enter the game deployment:

- [Detailed five-character grid](/Users/tanoshi/.codex/visualizations/2026/10/03/hero-brendan-comparison/five-character-detail-grid.png)
- [Full-frame five-character grid](/Users/tanoshi/.codex/visualizations/2026/10/03/hero-brendan-comparison/five-character-grid.png)
- [Recovered 32×64 reference PNG](/Users/tanoshi/.codex/visualizations/2026/10/03/hero-brendan-comparison/brendan-reference-32x64.png)

These local links are machine-specific; `compare.py` reproduces the outputs from the user screenshot and existing R4 JSON files. Usage: `python compare.py /absolute/path/to/screenshot.png /absolute/external/output/directory`. Pillow and macOS Arial fonts are required. The script rejects output directories inside the repository. No reference-colored pixels are embedded in the committed source or report.

## Recovery and alignment

The 454×768 screenshot has cell boundaries every 16 screen pixels, with mapped 32×64 frame origin (-18,-311). Every recovered cell uses the center color; all nine samples in each 3×3 center region match exactly (11,340 sample checks). The flat pixel pattern contains 13 opaque colors and occupies [3,20,29,62], or 26×42. Screenshot edge interpolation is discarded; it is not native sprite shading. This is exact recovery of the displayed logical cells/colors, not byte-for-byte reproduction of screenshot blur, and not a claim that this refined Brendan version is an untouched Emerald ROM sprite. Native cells outside the cropped screenshot are transparent padding.

Measurements shown before composition: supplied Brendan 26×42, R4 A/C 28×42, B/D 26×42, all in 32×64 frames. No second doubling is applied to this already refined reference. All five use 12 screen pixels per native cell, x=16 centerline, numbered ten-row Y guides and final painted foot row 61. The detail view omits empty rows 0–19 equally for all figures; original row coordinates remain labeled. The full view includes all 64 rows. Brendan's original asymmetries remain unchanged.

All four Hero RGBA arrays match their R4 PNGs exactly (8,192 cells). Every displayed cell center across both plates matches the relevant source or transparent-background color (17,280 checks). See [validation.json](validation.json). Both plates were inspected. The reference-containing images are local review artifacts only; the game is unchanged and needs no deployment.

## What the aligned view reveals

- The reference's continuous central exposed face starts at row 36; A/B/D open that area around rows 30–31. The eyes still occupy rows 38–41. These candidates add approximately five rows of forehead above the same eyes, changing the facial read even when total painted height matches. C's locks partly obscure the same underlying tall skull scaffold.
- Brendan's pointed headwear silhouette reaches its top with very little width, while A–D carry much more filled mass across the upper rows. Equal top and bottom extrema do not mean equal head mass or equivalent anatomical landmarks. A hat peak must not be treated as skull height.
- The supplied reference has strong dark separation at the neck and between torso/arms, plus stepped clothing clusters. The candidates' broad rectangular shirt planes and weaker separation make them look flatter and more like front-facing dolls. This is a visual diagnosis, not an assertion about the original artist's process.

The next correction must compare exposed-face/hairline landmarks, occupied row widths, arm attachment/overlap and body separation against the chosen reference. Do not use symmetry and an overall bounding box as evidence that the style matches. The current request only adds the reference comparison; all four candidate drawings remain untouched.
