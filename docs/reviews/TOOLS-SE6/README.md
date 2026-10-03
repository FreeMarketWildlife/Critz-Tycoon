# TOOLS.SE6 — Zoom anywhere

Published source `74eaa8d2f8409851dfee48bce4ffeff433d3359d`, committed on main and pushed with remote SHA verified. [Deployment receipt](deployment.json). Existing owner-only audience preserved. [Editor](https://critz-tycoon.freemarketwildlife.chatgpt.site/sprite-editor/), header revision **06**. Includes previously published reference centering and crop fixes.

## Behavior

Wheel zoom anchors the native pixel beneath the pointer; ordinary wheel and Ctrl/Command-wheel work. Keyboard +/− uses the hovered point. The +/− and 1× buttons preserve the current view center. Space-drag or Pan moves the view, including from blank workspace. Fit recenters the full canvas. Zoom remains integer and memory-bounded.

The previous viewport-ratio formula ignored the centered canvas offset, and button zoom supplied no anchor. The fix measures actual canvas geometry before and after scaling and compensates scroll. A scroll plane provides room around every edge. Intended anchor coordinates persist across repeated zoom events so rounded browser scroll offsets cannot accumulate visible drift.

## Verification

All 60 unit tests and 49 isolated Chromium browser scenarios passed with zero runtime errors. [Zoom tests](zoom-browser-report.json), [editor](browser-report.json), [reference](reference-browser-report.json), [workspace](workspace-browser-report.json), [centering and crop](symmetry-sides-report.json). All test state is synthetic and isolated from the user's browser.

New tests verify all canvas quadrants across repeated zoom in/out and overflowing sizes, panned-center button/native zoom, keyboard/Ctrl-wheel, Space-drag and blank-space pan without artwork changes, Fit recentering, exact painted-cell coordinates after zoom and phone-size layout. Anchor tolerance is 1.1 CSS pixels, accounting for browser scroll rounding. Existing suites also passed after the scroll-plane change.

All 585 tested build files matched the publication archive by SHA-256; the helper-added hosting manifest was identical. [Hashes](tested-build-sha256.json). [Desktop layout](workspace-1366.png) visually inspected; [mobile zoom](zoom-390.png).

Clean release excludes unrelated unfinished game/art changes; all opening unrelated file hashes were verified unchanged and shared status/plan edits were staged separately. No art, palette, animation, saves, exports or gameplay data changed. No artwork acceptance is inferred. Native touch drawing and reference transforms remain covered by existing tests; the new zoom behavior is wheel/keyboard based, not a two-finger canvas pinch implementation.

Next action: refresh to revision 06, scroll over a chosen point to zoom, Space-drag to pan, or Fit to recenter.
