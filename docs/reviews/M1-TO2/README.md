# M1.TO2 — Technical review, interruptions and retained memory

Implementation and final checks are complete. Publication remains held for parent review. This follow-up opens from clean main `2b4723173d1f7c1ba2efe7b0438e7ef23144e6ab`; the first overnight optimization is already pushed in `3755a2f`. All edits in this second pass belong to this task. A temporary local execution disconnect interrupted the receipt, then execution recovered and final checks were rerun. No user files were reset or discarded. Runtime commit [`68aeb24`](https://github.com/FreeMarketWildlife/Critz-Tycoon/commit/68aeb2419019120fae1bc4543c7bd5157a68efef) is pushed to origin/main with matching remote SHA and a clean checkpoint. This final receipt is documentation only. [Verified checkpoint](checkpoint.json). [First-pass morning report](../M1-TO1/README.md).

The existing phone game remains **public version49**, from source `7d73a6c524217543dc83df11c5c646d1fd3fb683`: https://critz-tycoon.freemarketwildlife.chatgpt.site . Sites reads confirm its existing successful deployment and public audience. No source synchronization, version save, deployment or audience change was performed in either optimization pass. GitHub pushes do not update that game. [Publication evidence and concrete handoff path](hosting-path.json).

## Reproduced measurements

The baseline is the complete production build exported from pinned `ee2a3cf67ead72385b64170003addf9c28fd9442`, not intercepted current code. Three cold contexts per route/version alternate order against two local production servers. Chrome155.0.8059.40,390×844 touch emulation,80ms latency,200,000 bytes/s download and93,750 bytes/s upload; no CPU throttle. Both previews serve uncompressed files. [Raw repeatability samples](repeatability.json).

| Measurement | Baseline | First-pass checkpoint | Final confirmation |
| --- | ---: | ---: | ---: |
| Game ready | 25.718s median of3 | 11.152s median of3 | 11.157s, one cold sample |
| Map Studio ready | 24.072s median of3 | 13.422s median of3 | 13.425s, one cold sample |
| Game decoded startup resources | 4,794,510B | 1,955,198B | 1,956,477B |
| Editor decoded startup resources | 4,482,544B | 2,492,722B | 2,494,463B |
| Game/editor requests | 69/50 | 72/54 | 72/54 |

The reproduced cold reductions are56.6% for game readiness and44.2% for editor readiness. Small final-byte increases come from the interruption guards and diagnostics. [Final production module hashes and startup sample](final-startup.json). One cache-enabled navigation after an unmeasured warm-up is also recorded for each version/route. All resources still transfer bodies (`zeroTransferResources:0`); these previews provide no ETag, so this is repeat-navigation evidence, **not a warm HTTP-cache speedup**. Baseline game/editor repeats25.731s/24.058s; first-pass11.099s/13.407s.

The live host already gzip-compresses the old full contact JSON:83,492 encoded bytes versus2,662,783 decoded bytes, HTTP200, with revalidation headers. That read was made at06:33UTC on14 October. Local uncompressed timings therefore cannot predict an equal hosted savings or a physical iPhone readiness time. The published game has not changed.

## Review findings and fixes

1. **Uppercase WASD and modifier release.** Shift+D did not move; changing Shift/CapsLock between press and release could also leave a symbolic key owner stuck. Shared direction lookup handles case and uses the physical `event.code` for ownership, with normalized keys for synthetic events. Both adventure and Map Studio use it. Existing touch/key ownership still passes.
2. **Page lifecycle interruption.** A persisted `pagehide` event without a preceding hidden-document event left input and movement running. The old game step advanced1→25 ticks during400ms; editor9→33. Both now freeze their clock on pagehide, clear owners and reset timing on pageshow, finishing only the already committed tile. These are synthetic persisted lifecycle probes plus real navigation; physical OS suspension remains untested.
3. **Final completed edit lost on immediate navigation.** Editor autosave waited150ms, so a completed edit followed by navigation in the same browser task disappeared. Hidden/pagehide now cancels incomplete strokes first and flushes only a pending completed edit. No pending edit means no serialization or rewrite. Review sandboxes, unreadable recovery data and unloaded editors remain protected. Import, immediate navigation, subsequent edits, undo/redo and reload pass.
4. **Failed delivery rewriting saves.** A503 artwork load followed by retry triggered pagehide autosave despite the error. The first-pass raw game save changed; current raw bytes remain exact. Pre-ready game input and editor actions are guarded, and an unloaded editor cannot create/import a replacement draft. Recovery and untouched navigation preserve the original draft's raw trailing whitespace too. [Independent before/after load probe](loading-finding.json).
5. **Retained coast construction memory.** Shoreline points were per-pixel objects, while runtime drawings retained wet/signed construction fields after compiling their paths. Numeric triples now use `Float32Array`; signed distances already originate as Float32 values, so no precision is lost. Runtime caches retain only field dimensions after bank, boundary, fresh and deep paths are built. Authoring/review construction APIs continue to expose their complete fields. Diagnostic recompilation counts also reset to zero on unchanged warm draws.

[Original failure probes against first-pass2b47231](baseline-defects.json) · [Nine final interruption groups](interruption-checks.json) · [Cache mutation evidence](cache-checks.json).

## Memory and rendering evidence

Three fresh64×48 maps each contain the same520-cell sand lake. Each sample measures a cold draw and two complete32-phase loops, then forces Chrome garbage collection. Canvas tracking uses weak references so the instrument does not retain evicted canvases. JS heap and backing storage come from `Runtime.getHeapUsage`; bitmap bytes are alive canvas area×4. These quantities overlap browser internals and must not be added or presented as total process/GPU RAM.

| Measurement | Before | After | Scope |
| --- | ---: | ---: | --- |
| Cold draw | 527.4ms | 122.6ms | Final baseline/current medians of3;4.30× faster |
| Retained construction arrays | 3,297,280B | 0B | One659,456-pixel field, wet Uint8 + signed Float32 |
| Backing-storage growth | 3,594,804B | 297,524B | Typed points before/after field release; identical in all3 samples |
| JS heap growth | 1,308,168B | 280,904B | Median of3, first-pass object points versus typed points before field release |
| Final JS heap growth | — | 264,960B | Median of3 after field release; sample spread231,460–358,636B |
| Alive canvas bitmap estimate | 23,740,416B | 15,220,736B | Old baseline versus final; bank plus cached phases |
| New phase canvases on second loop | 32 /84,410,368B | 0 /0B | Every one of the3 samples |

The field release removes exactly3,297,280 backing bytes after the typed-point change. The typed points themselves add297,504 backing bytes while reducing object heap growth; this tradeoff is reported separately. No claim is made that packed points alone reduce every memory category. [Before typed/release](repeatability.json) · [Typed points, fields retained](typed-memory-before-release.json) · [Final released fields](released-memory.json).

Nine cache lifecycle mutations cover unchanged draws, distant dry edits, shore material changes, adding/removing raw overrides, resize with unchanged bounds, moving→still water and pool deletion. Each cached image equals a fresh immutable-map rendering; expected rebuild counts and zero retained construction arrays are asserted. All32 measured phases reuse identical canvases on the next loop. A fabricated large phase atlas exercises the16MiB **per-component** cap and retains six phases/15,728,640B. The bound is not an application-wide memory cap.

## Final verification

- **290 unit tests pass**, no skips/cancellations;72 runtime modules syntax-check. Standard checks, build and whitespace checks pass; the build verifies30 canonical MIDI files.
- **217 browser groups across20 suites pass** on the final production bytes:214 printed groups plus3 JSON editor-view checks. Group counts overlap between suites. The complete20-suite run was repeated after recovering the preview servers; all suites exit0. The transient connection-refused attempt was an unavailable local server, with no product-test failure hidden or skipped. [Aggregate results](regression-results.json).
- Final independent water checks retain **640 exact prior-renderer composites** and all32 packed native masks. The complete-coast suite verifies4,070 colored native references. Native paths include mixed water depths, moving/still sand, raw overrides, day/night, reflections and clipped viewports. [Final pixel evidence](technical-checks.json).
- The existing gameplay suites cover named-player and loan paths, surviving rescues/25-gallon gift, care, Critter earnings, primary/backup saves, quota rollback, phone framing, maps/links/selection/import/undo/resize, stair/fence traversal and long-session behavior. New navigation probes use only isolated synthetic storage.
- Complete package verification before these receipts checks3,125 files:3,039 byte-exact files,83 authored asset JSON files with equal parsed data, and three explicit generated delivery files. The final rebuilt package is checked again after documentation. [1,797 non-documentation production hashes](runtime-proof.json) identify exactly tested runtime, art, source-download and music bytes. All six measured modules equal the final benchmark hashes. State/world/movement/grid migration/overworld modules and approved Hero PNG remain byte-exact to opening `ee2a3cf`; Hero SHA256 `0099dd331ae2c2d995663328e52763e8b10b1df0d36854d59676ee0ac52f7883`. [Unit/protection summary](unit-checks.json).
- GitHub exact-SHA inspection at pushed `2b47231` returns zero statuses, zero check runs and zero Actions runs. “Pending” with no status rows is **not green CI**. There is no checked-in Actions workflow; local checks are the test evidence. The runtime SHA68aeb24 has also been rechecked: zero status rows, check runs and Actions runs. [CI inspection](ci.json).

Approved pixels, B contacts,32px cells,480×320 camera, Black child Hero, story, names, accepted maps and save keys remain intact. No creative features or artwork were changed, and no visual/feel gate is self-approved.

## Reproduction and remaining work

Run `npm test`, `npm run check`, `npm run build`, and `node scripts/verify-build.mjs`. Start a dedicated production preview using `PORT=5221 npm run preview`, then `TEST_URL=http://127.0.0.1:5221 TEST_OUTPUT_DIR=/tmp/critz-production node tests/production-browser.mjs`. Benchmark reproduction uses `tests/benchmark-repeatability-browser.mjs` with `BASELINE_URL` pointing at a separately served production build exported from `ee2a3cf`, and `TEST_URL` at current production. `STARTUP_SAMPLES`/`RENDER_SAMPLES` default to3. The exported baseline has no Git checkout/worktree and does not modify repository branches. Scripts accept bundled Playwright and Chrome path overrides.

Parent's exact next action: review this checkpoint, rebuild/verify source and non-documentation hashes, then synchronize the same source through the existing Sites source helper with a fresh ephemeral credential. The project is public; use the public saved-version/deployment path, preserve its audience and saves, verify deployment success and return the existing phone URL. Previously minted source credentials were never printed/persisted and have expired; no Site source push occurred. Do not infer a publication from the GitHub push.

Remaining limits: physical iPhone/Safari touch and suspension, hosted ready timing, audible output and total GPU/process memory are unmeasured. Large bodies still require temporary full fields during compilation and a retained bank bitmap; full-map content edits still repaint the whole map. These are justified next profiling targets, not unmeasured claims of improvement. A temporary task-scoped idle-sleep inhibitor supported recovery and is removed with the owned preview servers; no persistent Mac power setting was changed and no cause of the earlier disconnect is asserted. No implementation, test or GitHub-push blocker remains after the receipt; publication intentionally awaits parent review.
