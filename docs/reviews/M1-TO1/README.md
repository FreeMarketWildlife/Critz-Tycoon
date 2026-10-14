# M1.TO1 — Overnight technical optimization

Technical implementation and checks are complete. Parent deployment review is pending. No Sites operation was performed; these changes are not yet on the phone game. Existing link: https://critz-tycoon.freemarketwildlife.chatgpt.site . Main was clean at `ee2a3cf67ead72385b64170003addf9c28fd9442`, newer than the delegated `7d73a6c` checkpoint. The later commits contain static Hero review; accepted gameplay Hero remains unchanged. Commit/push evidence is in [checkpoint.json](checkpoint.json).

## Measured result

| Measurement | Before | After | Scope |
| --- | ---: | ---: | --- |
| Game ready | 25.70s | 10.83s | Median of three fresh Chrome contexts; local production preview, uncached, **uncompressed**, 1.6Mbps download / 80ms latency |
| Map Studio ready | 24.10s | 13.43s | Same conditions and sample count |
| Game startup decoded resources | 4,794,510 bytes | 1,955,198 bytes | First cold sample; 59.2% reduction |
| Editor startup decoded resources | 4,482,544 bytes | 2,492,722 bytes | First cold sample; 44.4% reduction |
| Synthetic lake cold draw | 566.1ms | 134.3ms | One draw, 520 wet cells in a64×48 map; same host/480×320 camera; 4.2× faster |
| Moving sand shoreline phase | 3.3ms | 0.4ms | Median of32 first-loop phase draws on that lake |
| Shoreline canvas allocation over one loop | 89,686,016 bytes | 15,220,736 bytes | Sum of allocated bitmap area×4 over32 phases, including the bank; 83.0% less allocation, **not total browser RAM** |
| Warm grass lake drawImage calls | 527 | 157 | Same viewport and source pixels; 70.2% less image submission |
| Twelve large-map pan events | 518.6ms | 0.2ms | Median of three synchronous batches on128×128; old editor with the same current renderer isolates viewport work |
| Map redraws for those twelve pan events | 196,608 tile image calls | 0 | Existing bitmap is retained; no content edit |
| Six zoom button actions | 315.1ms /98,304 tile image calls | 0.5ms /0 calls | Same128×128 fixture |
| Idle editor rAF callbacks | 19 | 0 | Observed over300ms; no battery measurement |

Desktop Chrome155 on this Mac,390×844 emulation, no CPU throttle. Hosted compression/routing and physical-phone hardware differ; these timings do not claim the hosted phone game became10.83s. Sub-millisecond timings are diagnostic; operation counts, byte counts and equality proofs provide the more stable evidence. [Baseline samples](baseline-performance.json) · [Final samples](performance.json) · [Pan/zoom samples](editor-view.json).

## What changed and why

The contact manifest dominated cold transfer at2.66MB and contained thousands of editor-only tile/assembly records. Production now loads a331,625-byte runtime subset for play and a784,267-byte catalogue only for authoring. Catalogue entries share repeated B metadata on the wire and expand losslessly. **The original complete atlas.json download stays at its existing URL**, with identical parsed data. All83 authored asset JSON files are compacted in the build; source files remain intact. A generated production URL module selects the runtime subset; source previews retain the complete authored manifest. Independent atlas, tree, soil, water/cloud/prop and home requests now start together, preserving the existing all-art-ready/error barrier. Request counts increase69→72 for the game and50→54 for the editor, while transferred data falls substantially.

The coast compiler repeatedly visited every tap of a radius-six disk across a large field. Row prefix counts implement the exact same binary circular morphology with fewer operations. Interior bank pixels beyond the existing boundary distance avoid unnecessary style lookup. A warm camera now submits only water cells that can overlap its viewport, including the16px registered south projection; adventure passes its actual camera bounds too.

Moving wash formerly allocated a full lake-sized canvas for each phase and retained eight, causing repeated allocation on every loop. It now packs only eligible shoreline tiles, reuses all32 phases for the measured lake and caps phase bitmap storage at16MiB **per water component** (at least one frame). For this fixture, retained phase bitmap area is12,582,912 bytes versus21,102,592 bytes for eight old full-field phases; the89.7MB number above is allocation across a loop, not retained memory. Boundary masks, colors, loop timing, reflections and bank pixels stay exact.

Each direction now tracks its keyboard keys and pointer IDs independently. Releasing a finger or alias key cannot cancel a different held source. The editor restores the previous held direction when a newer source releases. Menus, blur and visibility still clear all owners. Editor playtests use foreground time for walking, hops and landing/arrival delays; hidden tests freeze and resume their committed action without catch-up or retained input. Static authoring no longer schedules an empty frame loop.

Pan, zoom, Fit and viewport layout updates reuse the rendered map bitmap. Painting, overlays, project changes and map changes still repaint. Canceling a pan restores its original transform; transformed picking and undo remain correct. Large-map **content edits still redraw the full map**; partial repaint is future optimization, not part of this checkpoint.

## Verification

- 289 unit tests pass, up from the verified282-test opening baseline. New checks prove exact disk morphology independently across borders/holes/radii, preserved bank pixels, complete metadata reconstruction, build data/pixel preservation, independent input ownership and immediate blocked release at all32 phases.
- 72 runtime modules syntax-check; standard checks, whitespace checks and the build pass. The builder verifies all30 canonical MIDI assets.
- 204 browser groups across18 production suites pass, using isolated Chrome contexts and synthetic storage. Coverage includes both named-player/loan story paths, surviving rescues/25-gallon gift, care and Critter workflows, old primary/backup bytes, quota rollback, menus/dialogue, phone framing, map links/resize/selection/paste/undo/redo, native overlap/fences, water and stair traversal. Group counts include overlapping coverage across suites.
- 640 composites match the opening renderer exactly across all32 phases, day/night, moving/still sand, mixed depths, raw overrides, reflections and two clipped viewports. All32 packed wash frames separately match the full native mask. Pixel comparison uses an explicit CPU readback context to avoid Chrome's changing GPU readback heuristic; existing renderers also retain nearest-neighbor sampling.
- The complete-coast browser suite independently checks all4,070 colored native transition references against the compositor.
- The package verifier checked3,113 files before final documentation receipts:3,027 byte-exact files,83 JSON files with equal parsed data and three explicitly generated delivery files. [Runtime/source hashes](runtime-proof.json) retain1,797 non-documentation paths for the parent's rebuilt-package comparison. Protected state/world/movement/grid migration/overworld modules and approved Hero PNG equal the opening commit byte-for-byte. Hero PNG SHA-256: `0099dd331ae2c2d995663328e52763e8b10b1df0d36854d59676ee0ac52f7883`.

The broader run exposed stale harness assumptions, recorded in [regression-results.json](regression-results.json): obsolete stair direction/rail coordinates, the already-superseded32-tick release expectation, a comparison against a clock that legitimately advanced before pausing, the moved Options title route, a broad notice selector and the old seven-command menu count. Those checks now follow existing behavior without changing movement/story/save code. A large pretty-JSON fill timeout was avoided using the editor's canonical RLE export; pan/zoom checks then passed. All initial failures have passing corrected runs; no test was skipped to obtain the result.

[Unit/check summary](unit-checks.json) · [Functional/native checks](technical-checks.json) · [Resolved browser results](regression-results.json) · [Town phone capture](phone-town.png) · [Large-map phone capture](large-map-phone.png) · [Playtest capture](phone-playtest.png). Town and large-map captures were inspected; no new art or visual/feel gate acceptance is claimed.

## Reproduction and handoff

Run `npm test`, `npm run check`, `npm run build`, then `node scripts/verify-build.mjs`. Start a dedicated preview with `PORT=5221 npm run preview`. Point `TEST_URL` at that preview and run `node tests/production-browser.mjs`; `TEST_OUTPUT_DIR` redirects evidence. The runner uses available bundled Playwright and Chrome, sequential suites and fresh profiles. `node tests/performance-browser.mjs` reproduces the controlled startup/lake diagnostic. Neither runner accesses a real user's browser storage.

Parent's next action: review this technical checkpoint, rebuild the committed source, compare the non-documentation hashes, then publish the exact tested build through the existing Sites project with its current audience and saves. Verify successful deployment and return the existing phone URL. No deployment authorization is inferred from push success.

Remaining measurement limits: physical iPhone/Safari touch/backgrounding, audible speaker output, hosted compression/ready timings and total JS/GPU memory have not been measured. Very large connected bodies still allocate bounded full-field morphology arrays and a bank canvas; the wash cap is per component, not an app-wide heap cap. No creative features, asset redesign, accepted-map edits, save-key changes, new roster/world content or milestone self-approval are included.
