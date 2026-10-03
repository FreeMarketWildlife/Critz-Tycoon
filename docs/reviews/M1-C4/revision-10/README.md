# M1.C4 R10 — Preserve the selected orange-striped Hero

[Native 32×64 PNG](../../../../assets/review/hero-idle-r10/hero.png) · [Countable grid](hero-grid.png) · [Indexed source](../../../../art/source/hero-idle-r10/hero.sprite.json) · [Exact RLE](../../../../art/source/hero-idle-r10/hero.rle.json).

The user's selected screenshot matches the existing R7 twists native raster. R10 edits that raster locally; it does not regenerate the hair or use the flatter R8/R9 drawings. The latest skeleton image guides symmetric anatomy, eye alignment and padding, without overwriting the selected character's silhouette. No new image generation, screenshot resampling, palette reduction or global RGB mirroring is used.

The transparent frame is 32×64; painted bounds `[4,24,28,62]` are 24×38. All 698 occupied cells remain at their original positions. Native rows62–63 are empty. Eyes remain `[12,38,14,42]` and `[18,38,20,42]`, the recorded 2×4 reference target. Body alpha from row37 down is mirrored across x16. Hair and illumination retain the permitted reference asymmetry. The user's skeleton is construction guidance; hidden skull shape is not claimed to be measured from Emerald.

There are 201 recorded color edits, mainly converting the exterior to pure black. Every black pixel belongs to the one-cell four-neighbor exterior boundary; no solid 2×2 pure-black blocks exist. Existing dark body bands immediately inside the border are recolored as skin/fabric/shoe shadows. Hair inside the boundary and the orange/cream stripe colors remain exact. The result uses 28 colors with no imposed count. See `art/source/hero-idle-r10/changes.json` and `outline.json` for individual edits and the mask.

Independent checks cover all 2,048 decoded PNG pixels, exact source/RLE agreement, zero silhouette changes, unchanged non-outline hair pixels, paired body alpha, eye positions, two transparent bottom rows, connectedness, exact black boundary membership and absence of 2×2 black blocks. [Validation](validation.json). Native and gridded proofs were visually inspected; technical checks do not approve the art.

`hero.sprite.json` and RLE preserve a custom palette. They use the editor's data schema, but the current editor's palette allow-list may reject these custom colors; this task does not change that tool. Do not use its palette-snapping PNG import to reproduce this artwork exactly. The PNG and indexed source are authoritative. No claim of successful browser/editor import is made.

Rebuild using Node/Sharp (`CODEX_PRIMARY_RUNTIME_NODE_MODULES`) with `node art/source/hero-idle-r10/build.mjs`; verify using Python/Pillow with `python3 docs/reviews/M1-C4/revision-10/verify.py`. Original sources have stable metadata in `assets/review/hero-idle-r10/manifest.json`. No Brendan or other reference-game pixels are included in this asset.

Art Bible corrected to prioritize the selected appearance and unrestricted palette for this request. Front-idle review only, awaiting user visual acceptance; no animation, runtime integration, game saves or deployment changes. Unrelated work remains preserved. Commit/push receipt is in PROJECT_STATUS. Next action: review this selected still before animation.
