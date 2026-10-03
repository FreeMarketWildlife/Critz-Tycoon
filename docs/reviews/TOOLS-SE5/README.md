# TOOLS.SE5 — Visible reference edits and reference-only crop

Published source `58c6ede10542f3850a94d537ad99e10685e7d642`, committed on main and pushed with remote SHA verified. [Deployment receipt](deployment.json). Existing owner-only audience preserved. [Editor](https://critz-tycoon.freemarketwildlife.chatgpt.site/sprite-editor/), header revision **05**.

## Reproduced failure and correction

A 320×434 repeated-column reference, edited in original source pixels to 321×434 and then reduced to 32×43, produced zero changed display channels. The prior implementation changed source pixels but could erase that change during its second resize. Prior regression coverage used small native images and missed this failure. This is a reproduced class of failure, not an inspection of the user's exact image; no existing user browser tab was available. Sites metadata was checked and real browser storage was not accessed.

Reduced references now initialize the workshop from displayed dimensions and use the reference's current sampling method to construct the working grid. Treatment then changes a whole canvas pixel column. Applying creates a new temporary image and places it at 1:1, with no automatic resize afterward. An oversized edge is clipped, disclosed in the preview. Explicit source-size work stays at that size too. A visible applied-size receipt confirms replacement. Original-reference restoration is preserved.

## Reference crop

The user explicitly requested reference-only cropping. **Crop reference** opens a larger drag preview with exact original-image X/Y/Width/Height, Apply/Cancel and Full image reset. Changes are staged until Apply; the full current source is retained for recropping. Applying fits the selected source region into the viewport and reveals the canvas on mobile. Sprite dimensions, animation frames, palette and painted pixels do not change.

## Verified release

All 60 unit tests and 42 isolated Chromium browser scenarios pass with zero runtime errors. [Column/crop checks](symmetry-sides-report.json), [workspace](workspace-browser-report.json), [reference](reference-browser-report.json), [editor](browser-report.json). Synthetic fixtures and isolated browser contexts were used. All four side treatments are checked against actual viewport RGBA for a large reduced image; corrected dimensions cannot be silently refitted. Crop tests cover staged cancellation, numeric input/validation, exact pointer source coordinates, restoration, crop-to-symmetry, desktop and mobile. Existing regressions cover native edits, animation, exports, palette, save compatibility and touch.

All 575 tested build files matched the archive by SHA-256. The packaging helper's added hosting manifest was also identical. [Build hashes](tested-build-sha256.json). [Large reference workshop](large-grid-preview.png), [crop desktop](reference-crop.png), [crop mobile](reference-crop-mobile.png) were visually inspected.

The release came from a clean main copy excluding unfinished game/art work. Opening unrelated file hashes were verified unchanged; shared status/plan edits were staged independently. No gameplay change, original-reference asset shipment or art approval is claimed. References remain temporary and excluded from sprite exports/saves. Working grids remain limited to 480px per axis and do not infer original screenshot anatomy or lost detail.

Next action: refresh to editor 05, reload the reference, use Crop reference if needed, then apply a center treatment.
