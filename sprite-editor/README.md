# Free Market Wildlife Sprite Editor

A dependency-free pixel editor at `/sprite-editor/`. Run the repository dev server and open that path. The normal project build includes it. No game runtime or save code is imported.

Choose a canvas preset, select a Critz palette bank and draw. Every stored cell is one native pixel, with either full opacity or full transparency. Tools: pencil, eraser, flood fill, eyedropper, line, rectangle and pan. Integer zoom, X mirror, pixel grid, vertical centerline, numbered horizontal guides, clean preview, undo/redo, and previous/next onion skin support review. Grid cell lines appear at ≥4×; ten-row guides appear at ≥3×, with fifty-row labels at lower zoom to remain readable. Maximum zoom is bounded by overlay memory.

## Workspace

The editor fills the browser window. The canvas gets the remaining space while the right panels scroll independently. Drag the dividers beside the drawing tools and inspector to change their widths. Expand Animation, then drag its top divider to change its height. Dividers also support arrow keys, Shift for larger steps and double-click to reset their size.

Use **Tools**, **Animation** and **Panels** to show or hide each dock; click any inspector section heading to collapse it. Animation starts collapsed and pauses when collapsed. **Focus** hides all docks and restores the previous arrangement on a second click. **Reset layout** restores the defaults. Layout preferences have their own local storage key, separate from sprites and game saves. Fit zoom follows viewport changes until you choose a manual zoom. On narrow screens, Panels opens a drawer; selecting a color or positioning a reference returns to the canvas.

Guide labels count upward from Y=0 at the bottom. Exported pixel rows still use standard top-left image coordinates.

## Canvas sizes

| Preset | Pixels |
| --- | --- |
| Standard character | 32 × 64 |
| Battle front / back | 128 × 128 |
| Small overworld / item | 32 × 32 |
| Large overworld | 64 × 64 |
| Party icon | 64 × 64 |
| Base environment tile | 16 × 16 |
| Map block | 32 × 32 |
| Rock / small prop | 32 × 32 |
| Building | 160 × 160 starting workspace; editable in 32px blocks |
| Screen | 480 × 320 |
| Custom | 1–480px per axis |

The building starting size is a convenience, not an exact universal Emerald building measurement. Canvas dimensions do not certify anatomy, silhouette, timing or approved art. The tool creates blank canvases; it does not generate artwork or advance art-review gates.

## Palette and art rules

`palettes.json` now provides the user's **32-slot Wildlife palette**: transparent slot 00 and 31 named opaque colors for tropical creatures, water, wood/soil, foliage and hardware/stone. All 31 can coexist in a character project. Swatches show the supplied slot, name and hex value. Selecting transparent paints transparent pixels. Imported PNGs quantize to these exact colors and threshold alpha at 128. [ART_BIBLE](../docs/ART_BIBLE.md) records the full specification; palette selection does not approve artwork.

Earlier Critz banks remain compatibility data only, hidden from the palette selector. Existing projects keep their original indexed pixels and colors; new brush swatches use Wildlife. Opening or restoring a project never silently recolors it. The picker can still select a preserved old pixel. Arbitrary colors outside the new or known legacy palettes remain invalid project data.

Mirror X mirrors paint, including color, and is an authoring aid—not proof of anatomical-mask symmetry. Document source revision/frame, semantic annotations, target measurements and deviations in Art notes. A separate annotated 1×/2× Hero comparison and independent part-mask proof still need to be authored for a formal character review. The editor does not automatically derive those annotations.

## References

Load a local PNG, JPEG, WebP or GIF (first decoded still). Reference scale offers **1×, 2× and Free**. Small native references start at 2×; larger images automatically open in Free with the whole source fitted inside the canvas and centered, above the artwork. Fit inside canvas can be used any time. This fits storage dimensions, not measured anatomical bounds.

In **Free**, click **Move / resize**, drag anywhere on the drawing canvas to move the guide, and drag its corner/edge handles to resize. Click **Done positioning**, press Escape, or choose a drawing tool to return to drawing. Keep proportions is enabled initially; unlock it to stretch width and height independently. Numeric display dimensions and offsets provide precise adjustments. Focused handles also support arrow keys (Shift for ten pixels). Geometry snaps to native canvas pixels. Free display dimensions are bounded to 1–2048 per axis; references accept up to 16 million source pixels / 20 MB.

Drag on the bounded source thumbnail or edit crop coordinates to select a pose. Cropping remains in original-image coordinates; in Free it automatically refits the selected crop. Cropping is non-destructive. Exact top-left RGB background removal is optional.

**Average covered pixels** integrates the source area covered by each output pixel, weighted by alpha, preventing transparent RGB from darkening edges. It averages in source sRGB space; it does not recover lost original pixels or infer sprite anatomy. **Nearest pixel** instead samples each output cell's source center. Resizing uses a responsive nearest preview while dragging, then settles to the selected algorithm on release. Movement reuses cached pixels. Both appear on the native grid with nearest-neighbor display; sampling affects references only and never quantizes or changes artwork. Fixed 1×/2× modes preserve source sampling.

Reference images remain in browser memory; reload them after opening/reloading a project. They are excluded from artwork PNG/GIF, project/copy data, autosave and checked-in assets. No bundled Pokémon image is shipped.

## Odd-width reference workshop

After adding a reference, choose **Fix odd width / symmetry…**. An odd-width image has a middle column; an even-width canvas has a centerline between columns. Choose **Duplicate center column · +1 px** (for example 31 → 32) or **Remove center column · −1 px** (33 → 32). Preview both grids before applying. Every other column retains its exact RGBA values; no averaging or forced mirroring occurs. Existing asymmetry remains. Adding transparent padding alone would not solve the anatomical center-column mismatch.

The workshop starts with the selected crop's dimensions when within its 480px limit. For an enlarged screenshot, enter the actual native grid first; **Use source size** and **Use shown size** are shortcuts. Nearest sampling constructs that working grid; it cannot infer an unknown original grid or recover lost detail. Correction then operates exactly on that grid.

**Use corrected reference** replaces only the temporary reference and centers its even width on the canvas centerline. A reference that fits stays at 1×; oversized results are reduced with nearest pixels and an even displayed width. The preview explains that reduction. The canvas must have an even width. Already-even images can be centered without changing their grid. **Restore original reference** restores the original image, crop and settings, including after repeated corrections. Cancel changes nothing. The corrected reference remains excluded from artwork, saves and exports.

## Animation and files

Add blank frames, duplicate, rename, reorder, delete, adjust holds and play. Up to 64 frames and two million total pixels. Timing uses the Art Bible clock `280896 / 16777216` seconds per tick. Default holds are 8 ticks; users can author run holds 5/3/5/3. The app does not infer pose construction or generate in-betweens. Playback pauses on blur and does not accrue hidden-tab time.

- **Save/Open project:** `.fmw.json` retains all indexed frames, exact palette, names, notes and tick durations. Open/import/new/clear are undoable within a bounded history.
- **Autosave:** one local draft at `fmw.sprite-editor.v1`, separate from game saves. Download projects to keep multiple sprites, make durable backups, or move between devices. Reference images are intentionally not persisted. Storage failures show a save-download message.
- **Frame PNG:** exact native transparent artwork only.
- **Sprite sheet PNG:** row-major frames, at most 4096px per row; filename reports column count. Last row may contain empty cells. Project JSON preserves exact frame count/timing.
- **Animated GIF:** loops with exact indexed colors and binary alpha; delays round cumulatively to centiseconds, minimum 20ms per frame for common viewer compatibility. Exact sub-centisecond timing remains in project JSON.
- **Copy for ChatGPT / Exact pixel data:** lossless JSON with color table, top-left coordinates, per-row `[colorIndex, runLength]` pairs, bounds, names, notes and durations. A selectable-text fallback works when clipboard access is unavailable. No network or AI service is required.
- **Import PNG/sheet:** image dimensions must be whole multiples of the current canvas; replaces frames with row-major slices, quantized to the selected Critz bank. Undo restores prior art. Use project JSON for lossless timing round trips.

## Checks

`node --test tests/sprite-editor.test.mjs` checks preset dimensions, bank provenance, drawing primitives, lossless data reconstruction and project validation; creates a GIF fixture for independent decoding. `tests/reference-pixels.test.mjs` verifies fitting, anchored resizing, fractional area sampling, transparency and crop boundaries. `tests/reference-editor-browser.mjs` checks large-image fitting, move/resize/crop, numeric and keyboard controls, desktop/mobile layouts and touch without painting. `tests/sprite-editor-browser.mjs` uses Playwright/Chromium with isolated synthetic storage to exercise editing, references, exports, save/reload, animation, all sizes, responsive layout and touch. Supply `CODEX_PRIMARY_RUNTIME_NODE_MODULES` and `CHROMIUM_EXECUTABLE` when using a bundled runtime. `CRITZ_EDITOR_URL` can point to a built local server.

`tests/symmetry.test.mjs` checks exact column conversion, transparency, immutable sources, invalid input and even-centered placement. `tests/sprite-workspace-browser.mjs` verifies screen fit, dock resizing/collapse, layout persistence, reference-only symmetry correction and restore, screenshot grids, playback collapse and mobile drawers in isolated browser contexts.
