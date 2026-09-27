# M1.I2 — playable visual review

This deliverable replaces the normal game's exploration renderer and movement, rather than adding another gallery. The user authorized completing missing art and movement together on 2026-09-27; final art and feel acceptance remains pending. The title bar visibly says **VISUAL REVIEW BUILD**.

## Artwork and presentation

The shared [runtime PNG](../../../assets/playable/atlas.png) is 512×768 with 270 stable entries: 54 environment modules/props/buildings and 216 character frames (nine roles × four directions × walk/run × idle/two strides). B1/G1 are provisional Hero/opposite-gender rival defaults; their south walk-idle pixels are unchanged. Mom, Nugget, Kaid and existing NPC roles now have complete sheets. Kaid's sides are explicitly authored; spout/handle are not mirrored. Adults retain modest native scale differences from the Black child Hero and child rival/Kaid.

All eleven existing scenes use the new renderer: bedroom, downstairs, yard, Rootport, Critz, Vet, Drug Store, Bike Shop, Glow n’ Blow, Kaid's home and the rival's home. Native floors/walls, furniture, intact/night/broken tanks, doors/stairs, paths, fences, pond, trees and all eight exteriors are included. The runtime never imports the old prototype exploration renderer or rejected environment-v1 assets. Generic integer raster utility code contains no rejected artwork.

Exploration draws at 240×160 with 16 px cells, integer positions and direct camera tracking. CSS uses a uniform integer nearest-neighbor scale with letterboxing. The camera follows the player at (120,88) without easing, including at scene edges. Ground anchors and explicit depth sorting place actors behind/in front of furniture and separated tree canopies. Rescue clues draw as foreground effects. Map collision, NPC occupancy, interactions, spawns and warps remain explicit data independent from atlas rectangles.

The habitat View/photography canvas also has newly authored native pixel plants, substrate, logs and creatures; it retains the existing 400×200 snapshot format and camera/care semantics. See [TANK_RENDER.md](TANK_RENDER.md). Accessible DOM menus remain display-scale controls; primary direction/A/B/Run/Start controls are at least 44 CSS px. The 320 px, 390 px and landscape phone proofs use 1× exploration; desktop uses 2× in the current shell. This intentionally favors uniform pixels over filling every available pixel. Physical-device DPR/zoom still needs user review.

Native source is editable and reproducible in `art/source/playable-characters/` and `art/source/playable-environment/`; [ATLAS.md](ATLAS.md) describes packing and validation. The generated [supporting-character study](supporting-character-study.png) is an illustrative image-generation guide, not the shipped sheet or evidence of directional/frame correctness. Production exports were authored on the native pixel grid and validated separately. No reference-game sprite pixels are shipped.

## Motion contract and deliberate differences

`src/movement.js` uses the pinned Emerald source ledger: tick period 280896/16777216 seconds; walk 16 pixels/16 ticks; run 16 pixels/8 ticks; rest turn 8 ticks; ordinary blocked attempt 32 ticks; held input priority up/down/left/right. A committed cardinal step finishes after release, mid-step direction changes wait for its boundary, and gait phase continues across actions. Walk holds stride/idle 8/8; run 5/3; turn 4/4; blocked 16/16. It saves only completed cell coordinates.

These are source-derived rules, not an emulator-verified equivalence claim. First/last presented action frames and complete reference door/warp sequences remain unresolved. Critz deliberately allows Run indoors, uses A-triggered doors and existing 150 ms fades, static NPCs/cardinal adjacent interaction, and retains the purchased skateboard's 1.25× benefit through an integer 6/7/6/7/6-tick run cadence. There are no new routes, ledges, elevation rules or terrain mechanics. Existing habitat simulation runs on its separate clock.

Hidden pages freeze motion and discard elapsed hidden time/input. Menus/dialogue freeze committed actions until resumed; browser blur clears held input. Visible long frames process at most 8 ticks and drop surplus whole ticks, keeping only fractional remainder. That responsiveness policy is a Critz choice. Pending A waits until the committed step completes before looking up interactions/warps.

## Save preservation

The v1 save key and schema remain. `gridVersion:1` marks the coordinate convention; unmarked positions already represent tile units and are relocated to the nearest reachable integer cell in the connected authored spawn region. Every nonposition field is preserved. Unknown grid markers are rejected in favor of recovery slots. Before the first converted save, original primary and backup bytes are archived under the same key plus `.pre-grid` and `.pre-grid.backup`; archives are immutable. Failed archival/backup/primary writes report failure and preserve recoverability. Only isolated synthetic saves were used for tests.

## Evidence and acceptance

See [atlas-validation.json](atlas-validation.json), [environment-validation.json](environment-validation.json), [tank-validation.json](tank-validation.json), [visual-browser.json](visual-browser.json), and the domain/story/lifecycle reports recorded in PROJECT_STATUS. Native scene captures and portrait/landscape screenshots accompany this document. Checks establish implementation behavior and export integrity; they do not approve artwork or movement feel. Physical phone Safari and emulator frame capture were not performed. Final user visual/movement acceptance is the next review action after publishing.
