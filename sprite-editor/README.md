# Free Market Wildlife Sprite Editor

A dependency-free pixel editor at `/sprite-editor/`. Run the repository dev server and open that path. The normal project build includes it. No game runtime or save code is imported.

Choose a canvas preset, select a Critz palette bank and draw. Every stored cell is one native pixel, with either full opacity or full transparency. Tools: pencil, eraser, flood fill, eyedropper, line, rectangle and pan. Integer zoom, X mirror, pixel grid, vertical centerline, numbered horizontal guides, clean preview, undo/redo, and previous/next onion skin support review. Grid cell lines appear at ≥4×; ten-row guides appear at ≥3×, with fifty-row labels at lower zoom to remain readable. Maximum zoom is bounded by overlay memory.

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

`palettes.json` mirrors editable original Critz sources with source paths. The Art Bible has **no approved global 32-color palette**: its policy is at most 15 opaque colors plus transparency per character and explicit environment banks. The editor supplies current Hero revision-3 colors, Mom/Kaid/Nugget banks and environment banks. All remain proposed artwork palettes. Standard and battle-character projects enforce a project-wide 15-color limit; other presets can combine the original banks. Selecting a bank changes available brushes without recoloring existing art. Imported PNGs explicitly quantize to the selected bank and threshold alpha at 128. Opened JSON projects must use recognized bank colors; arbitrary colors are rejected.

Mirror X mirrors paint, including color, and is an authoring aid—not proof of anatomical-mask symmetry. Document source revision/frame, semantic annotations, target measurements and deviations in Art notes. A separate annotated 1×/2× Hero comparison and independent part-mask proof still need to be authored for a formal character review. The editor does not automatically derive those annotations.

## References

Load a local PNG, JPEG, WebP or GIF (first decoded still). Drag over its thumbnail or enter crop coordinates. Set integer 1×–4× scale, integer offsets, opacity and above/behind positioning. Optional background removal keys the exact RGB at the whole reference image's top-left corner. No fuzzy removal or palette sampling from references occurs. All reference images remain in browser memory; reload them after opening/reloading a project. Reference art is never included in artwork exports, copy data, autosave or checked-in assets. No bundled Pokémon image is shipped.

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

`node --test tests/sprite-editor.test.mjs` checks preset dimensions, bank provenance, drawing primitives, lossless data reconstruction and project validation; creates a GIF fixture for independent decoding. `tests/sprite-editor-browser.mjs` uses Playwright/Chromium with isolated synthetic storage to exercise editing, references, exports, save/reload, animation, all sizes, responsive layout and touch. Supply `CODEX_PRIMARY_RUNTIME_NODE_MODULES` and `CHROMIUM_EXECUTABLE` when using a bundled runtime. `CRITZ_EDITOR_URL` can point to a built local server.
