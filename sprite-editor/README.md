## Supplied default and Play/Pause — 27 October 2026

Fresh Dummy Creator workspaces now use Phil’s exact pasted project in `assets/phil-default-20261027.json` (SHA256 `043d230c1eb241db65fbc6d62f68b474618e08d7f541b97a7fecf7629f0419a4`):12unique drawings,29timed slots, activeEastslot1. South/West/North each have8slots; East retains the5supplied slots. All labels, IDs, sequence order and stored durations are preserved. The previous22October asset remains available as `labels=phil-supplied-20261022`.

The right mobile hotbar has a Play/Pause toggle below Pick. It plays every stored sequence slot, including repeated drawings, in the current direction. Pause freezes the displayed drawing; stepping or editing also pauses. Desktop Play/Pause uses the same player. The view-only relaxed loop is800ms in each direction, preserving relative holds. This is a slower review cadence than current gameplay’s32simulation-tick (~535.77ms) normal gait from `src/movement.js`; no game movement or stored project timing is changed and no missing poses are invented.

Existing autosaves still load first without startup writes. The dedicated `labels=phil-supplied-20261027` link opens this supplied project under a separate draft key so older edits remain available through their original links. Copy/Download retain the complete current project. This changes the editor default, not accepted gameplay artwork.

## Previous supplied default — 22 October 2026 (historical)

Dummy Creator without a labels query, and the existing `labels=phil-walk-draft-20261017` link, now seed empty workspaces from `assets/phil-default-20261022.json`. This is Phil’s exact 65,252-byte supplied v2 project, SHA256 `1a1891a3a3c4bd75bf4942a5458c9efc8ea0e373c229ff63e11e6fa734112105`: 12 cels, 32 sequence references, all four directions and original durations/selection. No artwork or IDs are inferred or rewritten. The canonical region seed remains registration/part metadata only.

The existing dataset identity and autosave key are retained. Valid existing v1/v2 autosaves load first; v1 uses the tested exact-label unique-cel migration. No default is written to storage on startup. Existing drafts are never automatically replaced by the new asset. Copy/Download preserve the complete current project; users may explicitly import a backup. Restore starting layout remains an undoable active-drawing operation and updates linked slots, not a whole-project reset.

All prior assets remain byte-exact. **Original rough walk** opens `labels=phil-walk-original-20261017` under a separate autosave key, while `phil-south-20261017` and `phil-20261016` retain their original behavior. Ordinary drawing mode still starts its own workspace; this default is for Dummy Creator only.

# Free Market Wildlife Sprite Editor

## Right-side canvas hotbar (M1.DUI3)

Phones/tablets have a vertical hotbar beside the canvas: **Move / Pencil / Eyedropper / Forward one frame / Backward one frame / Reference visibility / Dummy visibility**. Selecting the drawing slot activates its current tool; tapping it again opens Pencil, Fill, Line and Erase. Move pans the canvas. Eyedropper samples a dummy pixel's part and exact anatomical side, then returns to Pencil; reference RGB is not converted into label IDs. Show the dummy before sampling it. Fill replaces the connected region of the same exact label ID; Line previews until release; each action uses one Undo and the current mirroring/side rules. Forward and Back step through unique drawings in the current direction, wrapping at either end and skipping repeated animation slots. Animation order and timing are unchanged. Visibility buttons stay synchronized with View-tab checkboxes and do not alter labels. Short landscape rails scroll vertically to keep44px+ targets reachable. Desktop retains its existing docks.

## Phone and tablet workspace (M1.DUI2)

Dummy Creator opens on **Canvas**, with tools and settings tucked into **Draw / Frames / View / File** tabs. Undo, Redo, Copy and zoom stay within reach. Draw contains directions, brush/erase/pan, Mirror, part and anatomical-side selection. Frames contains stepping, playback, frame actions and sharing. View contains guides, layers and reference controls. File contains import, backups, source information and Help. Done, Canvas, or Escape closes a panel; selecting a facing or part button returns to drawing.

The canvas fills the available dynamic viewport, including phone/tablet rotation and safe-area padding. Phones use a scrollable bottom panel; tablets use a side panel and refit the canvas beside it. Narrow landscape uses a side overlay. Compact mode applies through1100px wide and through1400px on coarse-pointer tablets; desktop docks return above those limits. Panels start closed on entry even if desktop dock preferences were saved. The same live controls move between layouts; artwork, project data, timing, storage keys, undo history and desktop layout preferences do not migrate or reset.

## Dummy Creator — completed south, rough walking setup and direct Copy (M1.DC2)

Open `/sprite-editor/?mode=dummy-creator&labels=phil-walk-draft-20261017`. Four visible **South / West / East / North** buttons choose the track. **ROUGH labels are prefilled for Phil to correct**:12unique editable poses across32timed reference slots. The actual completed714-cell south passing pose is reused exactly; other poses are estimates, not approved anatomy or artwork. Region Labels remain the dummy; no RD1 raster is rendered. No NPC/game artwork is installed.

### Correct repeated frames once

Version2 projects store2048-cell label arrays once in named `cels`; timeline frames refer to `celId`. Repeated sequence slots can reference the same editable pose **within that view**. Legacy migration shares only complete identical editable-label arrays, never merely similar reference images. Editing any repeat updates every linked slot, with one Undo. The Shared pose caption lists affected slots. **Reuse pose** adds a linked hold. **Duplicate** creates an independent copy. **Make independent** detaches just that slot. Frame order/name/reference/hold remain per slot. East is a distinct mirrored view with anatomical left/right IDs remapped, never linked to West.

The completed south original is available separately at `?mode=dummy-creator&labels=phil-south-20261017` and through **Download completed south original**. The full attachment is byte-exact22,997bytes, SHA256 `f88b094cf73ff272aaa629cfcc8ef1a9f02f6d01989d11b4e20a6ca3411736d7`:version1,32×64,28parts, four single-frame tracks,714marked south cells, other views740cells. No labels/colors/geometry in that original are creatively changed. The earlier740-cell preset remains at `labels=phil-20261016`. Each dataset has a separate autosave key; opening an update does not overwrite another draft.

### Real walking references

Expand **Reference** above the canvas for selectable slots, previous/next, independent playback, opacity and integer X/Y overlay offsets/reset. Offsets change only the overlay view, never label coordinates or project registration. All frames use32×64 canvas and bottom-center anchor(16,64).

- **South:** actual supplied fan-refined GIF, exact4× block extraction into32×48,+16Y registration; eight100ms slots A,A,P,P,C,C,P,P; no observed idle.
- **West/North/East:** actual original Emerald Brendan16×32, enlarged nearest-neighbor2×; raw PNG palette, **not** the fan artist’s refined2× frames. Frame layout and animation declarations are verified at `5eff78649e7170a877b961ef0b3da13b81a16038`:North5,1,6,1;West7,2,8,2;East West horizontally flipped. Each source command holds8updates; the UI divides it into two identical4-update slots without changing pixels/order/total535.7666ms gait. This preserves the existing eight reference-index slots.

`scripts/extract-emerald-directions.py` verifies source hashes/declarations and extracts original references. `scripts/build-rough-walk-labels.py` makes explicitly rough source-anchored semantic maps, retaining Phil’s exact anchor. Hat-covered scalp, near/far limb ownership and clothing/pack-occluded body divisions remain proposals for manual correction. North has no eyes; profiles have only the visible eye. No hidden limbs are added merely to fill categories. No imagegen estimates are used.

### One click Copy and safe projects

**Copy project** calls the Clipboard API directly from one trusted click/tap. A Copied confirmation appears only after success, with no dialog. If denied/unavailable, a clearly identified manual fallback contains the entire captured project and Select all; no success is claimed. Download backup/Import preserve all poses, links, timings and identities. Brush strokes and structural edits support Undo/Redo. Version1 projects migrate losslessly into shared cels only for complete identical editable-label arrays within the same direction; every slot name/order/hold/reference is preserved. Intentional version2 cel identities stay separate. Legacy correction imports edit the active drawing and its linked slots. Old explicit anatomical IDs stay stable even when crossing the screen center.

All categories retain left/right/center machine identities and related saturated annotation colors. Front Auto assigns screen-left to character-right; Back Auto reverses that. Profiles require an explicit anatomical side. Mirror writes opposite anatomical IDs and groups edits into one Undo. Two-finger navigation cancels tentative paint. Integer zoom/pan remain available; frame tools/reference controls collapse on portrait phones.

Projects use `fmw.sprite-editor.dummy-creator.v1:<seedId>:<datasetId>`; old body-region/default/supplied drafts remain recoverable and untouched. Layout is separate; game and ordinary sprite save keys are never migrated. Version2 uses1–128poses and1–32frames per direction, up to2MB JSON; fractional source holds are supported. Download backups to move devices. Physical phone testing is distinct from browser portrait QA.

## Reference and colors (revision 08)

- **Reference → Copy reference** paints the positioned/cropped reference onto the active frame with full opacity and exact sampled colors. Transparent cells preserve existing artwork. Other frames are unchanged; Undo restores the edit. The overlay hides afterward. Copy uses the entire reference footprint, independent of drawing locks.
- **Reference preset → Basic character skeleton** loads the user's exact template as a normal reference, ready to position, crop or copy. Upload remains available for your own images.
- **Eyedropper (I / Alt-click)** samples the visible layer, artwork only, or reference only. Faded guide opacity never dulls its sampled RGB. After picking, Pencil is ready to draw.
- **Colors** offers 14 palette collections plus a custom color picker/hex field. Use color selects the new color. Switching palettes preserves existing pixels. Colors in this sprite shows your used colors; more than 256 swatches are available through the eyedropper.
- **Two-finger scrolling pans** horizontally and vertically. Pinch or Ctrl/Command-scroll zooms at the pointer; +/−, Fit, and Space-drag remain available. Ordinary scroll now pans instead of zooming.

The latest user instruction permits exact RGB beyond Wildlife and removes the editor's old 31-color limit. PNG, projects and exact data remain lossless. GIF compacts unused indexes; when artwork uses more than 255 opaque colors, only that GIF is reduced and the export message says so. Existing PNG import still snaps to the selected palette; use Copy reference for exact colors. Palette changes and this tooling update do not approve or recolor gameplay art.

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


### Dummy Creator workspace (M1.DUI1)

Direction arrows are in the right Parts/Layers inspector, immediately above Parts. On a phone, use the panel icon to open that drawer; choosing a direction or part returns to the canvas. Plus adds a blank frame, overlapping pages duplicate independently, and the trash icon deletes the selected frame. All icon controls have accessible names and hover tooltips. The timeline retains the imported frame timing automatically; there is no millisecond/speed input. Copy remains a one-click full-project clipboard write with a manual fallback only on failure. Existing drafts, shared-pose links, undo and backups retain their formats/keys.
