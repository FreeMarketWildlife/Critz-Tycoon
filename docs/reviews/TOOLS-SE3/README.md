# TOOLS.SE3 — Workspace and symmetry workshop

Published source: `f857aae22fb6e5225c1c8ed918e6e4b8fb0afb5a` on `main`; origin/main matched before release. [Deployment receipt](deployment.json). Existing owner-only audience preserved. [Editor](https://critz-tycoon.freemarketwildlife.chatgpt.site/sprite-editor/).

The editor now uses a window-sized workspace, resizable tool/inspector docks and animation area, collapsible panels, Focus and Reset layout. The odd-width workshop previews exact center-column duplication/removal and centers the corrected temporary reference. It retains an original-reference restore point and does not modify artwork.

## Verified release

A clean main release copy excluded pre-existing unfinished game/art work. Built with the project's build script. All **60 unit tests** and **30 isolated Chromium browser scenarios** passed, with zero runtime errors. Reports: [editor](browser-report.json), [reference](reference-browser-report.json), [workspace](workspace-browser-report.json). Test storage and images were synthetic, not the user's browser data.

The 543 tested build files matched the deployment archive byte-for-byte by SHA-256; the packaging helper also included a byte-identical hosting manifest. [Build hashes](tested-build-sha256.json). macOS metadata entries were excluded before publication.

Visual inspection covered desktop canvas priority and mobile symmetry previews. [1366×768 workspace](workspace-1366.png), [31→32 preview](symmetry-31-to-32.png), [mobile preview](symmetry-mobile-390.png). Desktop fit tests also cover 1280×720, 1440×900 and 1920×1080; mobile covers 320×568, 390×844 and 844×390.

## Limits and preservation

Dock borders resize docked panels, not floating operating-system windows. Layout persists separately from sprites/game saves. Animation starts collapsed and pauses when hidden. References still need reloading after a browser reload.

Center-column correction is exact on the chosen working grid. Enlarged screenshots require a known native grid; nearest sampling cannot infer it. Oversized corrected guides are shown smaller with an even display width; the dialog explains resampling. Existing asymmetry remains, and an even-width canvas is required. Reference changes do not enter project data, exports or artwork. No original game references are bundled, no art is approved and no gameplay data or review gates change.

The opening unrelated dirty file contents were verified unchanged; concurrent committed R7 review work was preserved. Next action: use the updated editor; existing artwork review remains with the user.
