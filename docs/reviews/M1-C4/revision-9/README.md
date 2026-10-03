# M1.C4 R9 — User-template idle assets

Four front-idle PNGs use the user's exact 32×64 RLE template for anatomy. The input contains one color-blocked symmetric skeleton, not four colored characters. Its frame, body silhouette from row 36 down, eye rectangles at x=12–13/18–19 and y=38–41, and two transparent foot rows are preserved. Hair is independently authored at native resolution. The user specifically requests one-pixel outlines; this overrides the older mixed-weight advice in ART_BIBLE.

[Native five-character comparison](/Users/tanoshi/.codex/visualizations/2026/10/03/hero-revision-9/five-idles-native.png) · [Countable grid, upward Y and x=16 symmetry](/Users/tanoshi/.codex/visualizations/2026/10/03/hero-revision-9/five-idles-grid.png). Brendan is unchanged and is excluded from the repository/build and asset pack.

## Deliverables

[Download idle asset pack](hero-idle-r9.zip). It contains all four PNGs, manifest, editable `.sprite.json` files and exact `.rle.json` exports. Open the `.sprite.json` files with the Sprite Editor's project-open action; RLE is the exact text exchange representation. The original user export is preserved separately in `art/source/hero-idle-r9/user-template.rle.json`.

| Design | Native PNG | Editor project | Painted size |
| --- | --- | --- | --- |
| A afro / teal-green raglan | [PNG](../../../../assets/review/hero-idle-r9/a-afro.png) | [Project](../../../../art/source/hero-idle-r9/a-afro.sprite.json) | 26×38 |
| B flat-top / gold vest | [PNG](../../../../assets/review/hero-idle-r9/b-flat-top.png) | [Project](../../../../art/source/hero-idle-r9/b-flat-top.sprite.json) | 26×39 |
| C twists / red stripes | [PNG](../../../../assets/review/hero-idle-r9/c-twists.png) | [Project](../../../../art/source/hero-idle-r9/c-twists.sprite.json) | 26×38 |
| D cornrows / blue jacket | [PNG](../../../../assets/review/hero-idle-r9/d-cornrows.png) | [Project](../../../../art/source/hero-idle-r9/d-cornrows.sprite.json) | 26×37 |

All retain the supplied Wildlife palette. Teal and shorts use that bank's teal-green/green families; the original screenshot's colors are not sampled. The input's thick internal dark bands are repainted as material or single-row contact seams. Anatomy uses the user's construction instead of R8's smaller silhouette. The frame is 32×64 with anchor `[16,64]`; last painted row is 61. This preserves the measured Emerald 1px idle padding at 2× and the 1×2 → 2×4 eye target. Pinned reference context remains in `docs/REFERENCE_MEASUREMENTS.md`; hidden skull geometry is the user's supplied construction, not a recovered Emerald bone measurement.

## Method and verification

`art/source/hero-idle-r9/build.mjs` decodes the actual RLE, paints integer pixels, exports using the editor's own `describe` function and validates each reopenable project with its `validateProject`. No screenshot transfer, resampling, smoothing or forced 2×2 authoring blocks. Per-character masks record the source body, hair and exterior outline. The outline is exactly one occupied-cell four-neighbor boundary layer, never a dilated stroke. Dark hair material and the required 2×4 eyes are not stroke-width measurements.

Independent Pillow verification compares all 8,192 native pixels with their source indices, RLE round-trip and positions in the comparison strip. All four have binary alpha, connected shapes, exact mirrored template/body silhouettes, unchanged eye positions, source-palette equality and one-layer boundary masks. See [validation](validation.json). Brendan's comparison pixels are unchanged. Native and gridded sheets were visually inspected. These integrity checks do not self-approve the art or imply animation readiness.

Rebuild with Node/Sharp (`CODEX_PRIMARY_RUNTIME_NODE_MODULES`) and Python/Pillow:

```sh
node art/source/hero-idle-r9/build.mjs EXTERNAL_REVIEW_DIRECTORY
python3 docs/reviews/M1-C4/revision-9/verify.py EXTERNAL_REVIEW_DIRECTORY
node docs/reviews/M1-C4/revision-9/present.mjs EXTERNAL_REVIEW_DIRECTORY
```

The optional external reference comparison uses the existing local Brendan reconstruction documented in R7/R8. The original-only build does not need it. Reference sprites stay outside the repository because build output includes docs/assets. No browser storage, saves or gameplay code changed.

These PNGs and stable-ID metadata are ready to consume as **front idle assets** after visual acceptance. Back/side poses and animation do not exist in this packet. Assets remain in the review namespace; no silent replacement of accepted gameplay art. ART_BIBLE records the new outline rule and source priority; AGENTS already delegates art direction there. No playable deployment is needed. Commit/push receipt and remaining work are recorded in PROJECT_STATUS. Next action: user reviews idle, then author animation when requested.
