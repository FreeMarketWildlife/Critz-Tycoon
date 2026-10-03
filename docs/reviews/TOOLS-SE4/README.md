# TOOLS.SE4 — Four center-side treatments

Published source `76931028c0d991ffb7c209cd34c3d0efba47718b`, committed on main and pushed with remote SHA verified. [Deployment receipt](deployment.json). Existing owner-only audience preserved. [Editor](https://critz-tycoon.freemarketwildlife.chatgpt.site/sprite-editor/).

## Fix

The previous workshop bypassed the treatment on an even input width; centering an already centered image could leave the viewport unchanged. Replaced that shortcut with four operations that always edit a column: remove left/right and add left/right. Odd grids select the immediate neighbors of the middle column; even grids select the central pair. Add copies that column toward center. The exact chosen column is highlighted and numbered in the dialog.

Apply constructs a fresh reference canvas, resets crop and sampling cache, shows it above artwork, restores zero opacity to 30%, and triggers viewport rendering. Other opacity values are retained. Mobile apply reveals the canvas. Restore reinstates the original image and settings and invalidates its cached samples, fixing stale-image restoration.

## Verified release

The clean committed release excludes unrelated dirty game/art work. All 60 unit tests and 36 isolated Chromium browser scenarios passed with zero runtime errors. [New viewport pixel checks](symmetry-sides-report.json), [workspace](workspace-browser-report.json), [reference](reference-browser-report.json), [editor](browser-report.json). Tests use synthetic fixtures and isolated storage.

Actual canvas RGBA is checked for all four operations on odd/even source widths, repeated operations, exact restore, hidden/zero-opacity/behind references, and mobile apply. Art/project data is verified unchanged. Existing regression tests cover export isolation, animation, save compatibility, references, palette, sizing and touch. [Applied viewport](applied-reference.png) and [mobile treatment](mobile-treatment.png) are synthetic QA images; mobile preview was visually inspected.

All 565 tested build files exactly match the publication archive by SHA-256. The only helper-added static file is a byte-identical hosting manifest. [Build hashes](tested-build-sha256.json).

## Limits

An even input becomes odd after one single-column operation; the dialog explains its half-pixel center mismatch on an even canvas and placement stays on whole native pixels. Oversized results use disclosed nearest sampling. Screenshot grids must be supplied by the user; no source-grid or anatomical inference is claimed. References remain temporary and excluded from artwork, project/export and game saves. No art acceptance or gameplay changes. All unrelated opening file hashes were preserved; shared status/plan changes were staged separately.

Next action: refresh the editor, reload the reference, choose a treatment and click Center this image.
