# Free Market Wildlife Sprite Editor

## Character construction and shading (revision 07)

Click **Skeleton → Start from skeleton** to edit the user's exact basic character model. This replaces the workspace and is undoable. **Use as guide** overlays the same model without changing artwork. Choose a region to highlight it, set opacity/layer, or open **Anatomy & shading map**. The semantic guide fits 32×64 frames; it is disabled at other canvas sizes.

- **Paint only selected region** restricts pencil, eraser, fill, line, box, shade and recolor to that fixed template mask. Left/right mean screen-left/right. Mirrored marks must independently pass the mask.
- **Protect template outline** preserves the template's dark contour/separation positions. **Paint only existing pixels** locks transparent cells. Controls are explicit and session-only; they do not silently modify imported artwork.
- **Shade (D) / Lighten (U)** steps through the selected palette ramp once per pixel per stroke. Other colors and transparent cells remain unchanged. Select the appropriate ramp under **Shading & recolor**; the head/body region selector chooses its matching ramp.
- **Replace with brush color** changes the chosen source color in the current frame or all animation frames, respecting paint limits. Undo restores the whole operation.
- **Clean** hides reference/skeleton/grid/onion overlays for an artwork-only view. Exports always contain artwork only. Hover over the canvas to read the template's anatomical region.
- **Import & export → Paste sprite data**, or **Open project**, now accepts the exact RLE copied to ChatGPT, including animation frames and exact palette values. Invalid input is rejected before changing the workspace. No pasted text is executed.

The skeleton is a construction model, not a finished outfit or a new approved game asset. Its head/torso shadows are distinct from its outline; pink/green/coral are anatomy labels. See the [Art Bible](../docs/ART_BIBLE.md) for measured interpretation and the limited Brendan comparison. All existing reference cropping, odd-width correction, freely positioned overlays, cursor zoom, animation and resizing/collapsing controls remain available.


A dependency-free pixel editor at `/sprite-editor/`. Run the repository dev server and open that path. The normal project build includes it. No game runtime or save code is imported.

Choose a canvas preset, select a Critz palette bank and draw. Every stored cell is one native pixel, with either full opacity or full transparency. Tools: pencil, eraser, flood fill, eyedropper, line, rectangle and pan. Integer zoom, X mirror, pixel grid, vertical centerline, numbered horizontal guides, clean preview, undo/redo, and previous/next onion skin support review. Grid cell lines appear at ≥4×; ten-row guides appear at ≥3×, with fifty-row labels at lower zoom to remain readable. Maximum zoom is bounded by overlay memory.

## Workspace

The editor fills the browser window. The canvas gets the remaining space while the right panels scroll independently. Drag the dividers beside the drawing tools and inspector to change their widths. Expand Animation, then drag its top divider to change its height. Dividers also support arrow keys, Shift for larger steps and double-click to reset their size.

Use **Tools**, **Animation** and **Panels** to show or hide each dock; click any inspector section heading to collapse it. Animation starts collapsed and pauses when collapsed. **Focus** hides all docks and restores the previous arrangement on a second click. **Reset layout** restores the defaults. Layout preferences have their own local storage key, separate from sprites and game saves. Scroll over any canvas point to zoom around the pointer, including Ctrl/Command-wheel. The +/− and 1× buttons preserve the center of the current view; keyboard +/− uses the hovered point when present. Hold Space and drag, or choose Pan, to move the view, including from empty space around the canvas. Fit recenters the complete canvas. Integer zoom preserves crisp native pixels. Fit zoom follows viewport changes until you choose a manual zoom. On narrow screens, Panels opens a drawer; selecting a color or positioning a reference returns to the canvas.

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

## Crop reference image

Click **Crop reference** for a large selection preview. Drag a rectangle, or enter exact X/Y/Width/Height in original-image pixels (top-left origin). **Apply crop** fits that region into the viewport; **Cancel** changes nothing. **Full image**, then Apply, restores the complete source. Cropping only changes the guide: sprite dimensions, painted pixels and animation frames are untouched. The original source stays available for further crops.

## Center-column reference workshop

After adding a reference, choose **Fix odd width / symmetry…**. Four treatments are available: **Remove left of center column**, **Remove right of center column**, **Add left of center column**, and **Add right of center column**. The selected source column is highlighted and its one-based number appears in the preview explanation.

For an odd grid, left/right means the immediate neighbors of the single middle column. For an even grid, it means the two columns beside the centerline. Add duplicates the selected column toward the center; remove deletes it. Every other column keeps its exact RGBA values. All four options perform an edit, even if the input width is already even. An odd width becomes even; an even width becomes odd. Existing asymmetric features remain.

When a large reference is reduced in the viewport, the workshop starts with its displayed dimensions and current sampling method. The column treatment therefore edits a real canvas pixel rather than a tiny source-image pixel. Small unscaled references use their source grid. For an enlarged screenshot, enter the actual native grid first; **Use source size** and **Use shown size** are shortcuts. The reference’s current sampling mode constructs the working grid; it cannot infer an unknown original grid or recover lost detail. Correction then operates exactly on that grid. Removing the only column or adding beyond 480px shows an error.

**Center this image** creates a new temporary reference image, replaces the viewport overlay immediately, resets the crop to the corrected image and shows it above the artwork. Zero opacity becomes 30%; other opacity values remain. The mobile inspector closes so the canvas is visible. The corrected image stays at exactly 1×: there is no fit/resampling after the column edit. If it extends past the canvas, that part is clipped rather than squeezed. The dialog explains this and the Reference panel shows an applied-size receipt. Pixel placement stays on the native grid: odd/even parity mismatches are centered to the nearest whole pixel, with the half-pixel axis difference disclosed rather than blurring the image.

**Restore original reference** restores the original image, crop, positioning, visibility, layer and opacity, even after repeated treatments. Cancel changes nothing. Corrections remain excluded from artwork, saves and exports; reload the original reference after a browser reload.

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

`tests/symmetry.test.mjs` checks all four side treatments on odd/even grids, transparency, immutable sources, invalid input and centered placement. `tests/sprite-workspace-browser.mjs` verifies screen fit, dock resizing/collapse, layout persistence, reference-only symmetry correction and restore, screenshot grids, playback collapse and mobile drawers in isolated browser contexts.

`tests/symmetry-sides-browser.mjs` asserts actual viewport RGBA after all four treatments for odd/even inputs, repeated edits, exact restoration, hidden/zero-opacity overlays and mobile apply.

`tests/sprite-zoom-browser.mjs` verifies cursor anchors across all quadrants and repeated zoom steps, button/keyboard anchors, panning without painting, exact drawing coordinates after zoom, Fit recentering and small-screen layouts.
