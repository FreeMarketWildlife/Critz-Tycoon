# Critz M0 gameplay and save audit

Audit of playable baseline `191e3a6b7721d8193f47914c6f7afa1d50b70dbc`, 2026-09-24. Runtime and tests are unchanged; local main was fast-forwarded to the existing playable history before this audit. Paths/line numbers refer to that baseline. The user’s M0-only production-plan assignment supersedes the older next-feature suggestion at the end of `docs/GAME_VISION.md`; the established story/design itself remains authoritative.

## Repository discovery and baseline checks

- Repository: [FreeMarketWildlife/Critz-Tycoon](https://github.com/FreeMarketWildlife/Critz-Tycoon). Local folder initially had an unborn empty `main` with no remote.
- Remote `main`: initial README commit `9f14c4fbc4fc1e8ca4ca59c171488896c36f9dcc`.
- Existing remote `feature/playable-foundation`: `191e3a6b7721d8193f47914c6f7afa1d50b70dbc`, containing implementation commit `466c359` and hosting configuration. [PR #1](https://github.com/FreeMarketWildlife/Critz-Tycoon/pull/1) was open/unmerged with no reported checks/review decision at inspection. No other remote branches or PRs were found in the queried inventory.
- Added `origin`, fetched history, and fast-forwarded **local main** to the playable commit. Created no development branch/worktree. No remote push, merge API, PR closure or deployment was performed. Existing `.openai/hosting.json` is configuration evidence, not verification of a live published site.
- Before M0 edits there were no local changes. GAME_VISION's Git blob remains `a92234f4c79dc202cd8d9e8e5be372cde31270d7`, identical to the playable baseline. No save format or runtime edits are part of M0.

Fresh verification on this machine used bundled Node v24.19.0 (the ordinary shell has neither `node` nor `npm` on PATH), plus Playwright 1.62.1 and installed Google Chrome 153.0.8010.54. Executed the exact underlying package-script commands: all four `node --check` calls passed, `node --test tests/*.test.mjs` passed **10/10**, and `node scripts/build.mjs` produced `dist/` successfully. These are fresh results, not merely inherited QA claims.

`node tests/browser.mjs` passed **14/14 reported checkpoints**, no uncaught page errors, in an isolated browser context. It traversed the story/world using held keyboard input, posted a photo/simulated video and checked four viewport sizes. [Raw checkpoint report](verification/M0_BROWSER_BASELINE.json) preserves the runner's original messages; the reload message overstates its exact assertion coverage as explained below. Current capture `test-results/mobile-town.png` was visually inspected: external controller, prototype's small actors and large buildings, fractional display scale; it is **not** an approved Emerald-style sample. Generated captures/build output remain ignored. No physical Safari/device session or user save was used.

## Architecture and visual discrepancies

Plain ES modules: `state.js` owns domain/economy/persistence; `world.js` owns scene/entity geometry and navigation; `art.js` draws procedurally on Canvas; `main.js` binds story/UI/input/clocks. DOM menus and controller remain accessible independently of the raster. This separation is worth preserving, though visual object rectangles currently double as collision geometry.

| Foundation | Verified prototype | Target / staged action |
| --- | --- | --- |
| Exploration raster | `index.html:35`: 384×288,4:3; CSS `#viewport`4/3 | 240×160,3:2; prove M1/M2, integrate M4+. |
| Tile construction | `world.js:3`: 24px tiles; direct drawing with no reusable PNG tile atlas | Editable 8×8 sources and 16×16 metatiles; M1 draft assets, M3 pipeline. |
| Display scale | CSS world fills viewport; smoothing disabled for images but display can be fractional/downscaled | Integer preferred; documented phone tradeoff; external controller retained. |
| Pixel edges | Rectangles rounded, but Canvas ellipses/text/alpha overlays can create antialiasing or intermediate colors | Pixel-authored inspectable PNGs, explicit palettes and hard outlines; M1. |
| Characters | No frame sheet; same procedural body for children/adults, Kaid special branch; walk uses `sin(time*12)*2` leg shapes | Distinct approved child/adult silhouettes, directional poses and tick holds; M1/M2. `time*12` is angular phase, not 12 sprite frames/sec. |
| Movement | Continuous diagonal 3.15/5.2 tiles/sec; roughly 75.6/124.8 native prototype px/sec; axis slide; blocked input still animates | Cardinal committed 16px steps, reference cadence, turning/collision semantics; M2 harness before integration. |
| Clock | `main.js:1080`: variable rAF dt capped 0.05 sec; habitat separate 8-second accumulator | Fixed exploration ticks independent of render rate; retain habitat/pause/economy behavior. |
| Camera | `art.js:320`: center-on-player clamped to map size; rounded camera offset | Reference direct tracking plus padded borders; small-room and outdoor proof. |
| Occlusion | Furniture/NPC/player y-sorted; outdoor trees/buildings drawn before all actors | Explicit foreground and ground anchors; M2 occlusion test, M3 layers. |
| Appearance/data | Repeated renderer branches and literal furniture/building drawing; furniture bounds also collide | Assets/map layer data separate from collisions/warps/actions; M3. |
| Doors/interact | A-triggered nearest target within 1.65 tiles; scripted transition/spawns | Preserve reachable actions and controls; explicit approach/warp metadata and reviewed transition cadence. |
| Build pipeline | Copies HTML/CSS/src/icon only; server lacks PNG/JSON MIME entries | Add exported assets/maps and matching types in M3, not M0. |

No target behavior in this table is claimed implemented. Existing code-drawn art is retained as playable baseline until staged integration.

## Preservation contracts verified in code

- **Identity/opening:** player names Hero and rival (16-character limit); boy/girl selection implies the opposite rival gender (`src/main.js:133`, `:741`; `src/state.js:34`). Opening explicitly says every escapee survives and gives Mom remorse, affection, and support (`src/main.js:175`). Kaid’s name, 25-gallon birthday gift, optional interest-free $100 loan, and no forced repayment survive both branches (`src/state.js:89`; `src/main.js:217`, `:496`, `:894`). Child age and Hero’s Black identity are design requirements; art verification belongs to the art audit.
- **Rescues:** stable IDs are `gecko`, `snail`, `isopods`, `springtails`; Pebble and Button stay in separate Vet care, while 6 isopods and 12 springtails enter the starter tank. Rescue is idempotent; no animal deaths are simulated (`src/state.js:8`, `:102`, `:186`; `src/main.js:296`). Nugget gives notebook and a one-time $15 reward (`src/main.js:432`).
- **Economy/recoverability:** all money is cents; start $12; moss $3; litter (3) $1.50; medicine $20; skateboard $45; hide $6. Free misting/cleaning, one-time kit, and repeatable 2-litter foraging every 6 habitat hours remain available (`src/main.js:401`, `:762`, `:920`; `src/state.js:117`). Drug Store medication delivery is implemented; recurring medication deadlines/tank breakage are expressly future work (`src/main.js:337`, `:632`).
- **Tank interface:** first-level options are exactly **Manage / Stats / View** (`src/main.js:503`). Management affects causal conditions and inventory; Stats exposes births, zero deaths, history and causes; View produces PNG snapshots and six-second simulated video posts, with transparent scores and fictional revenue (`src/main.js:517`, `:529`, `:540`, `:558`; `src/state.js:284`). Captured post PNGs are saved artwork, so a visual update must preserve existing snapshots rather than reinterpret/re-render them.
- **Simulation:** deterministic `tick` advances one habitat hour; 8 active seconds per hour; night does not tick; nonlethal bounded populations; history 24, events 12, posts 12; age 0–4 post payouts credit only incremental revenue (`src/state.js:186`). Keep this domain logic separate from a future fixed exploration clock. Explore/tank/manage/stats/view/Critter are live, while dialogue, transitions, ordinary menus and background tabs pause. Observe adds 1 hour, Rest adds 8; no offline catch-up (`src/main.js:904`, `:1071`, `:1102`).

## Stable map and interaction identifiers

Scene IDs (also independently hardcoded in save validation, `src/state.js:354`):

| Scene ID | Display identity / entrance |
|---|---|
| `bedroom` | Your bedroom / named Hero’s room |
| `house` | Home · downstairs |
| `yard` | Home · the yard / HOME |
| `town` | Rootport |
| `critz` | Critz / CRITZ |
| `vet` | Vet / VET |
| `pharmacy` | Drug Store / DRUG STORE |
| `bike` | Bike Shop / BIKE SHOP |
| `glass` | Glow n’ Blow / GLOW N’ BLOW |
| `kaidHome` | Kaid’s home / KAID |
| `rivalHome` | Your rival’s home / RIVAL |

`src/world.js:134` is the scene source. Doors use IDs `stairs`, `exit`, `home`, `gate`; town building doors use their destination scene ID. Bedroom: `tank`, `sleep`, `desk`, `gecko`. House: `mom`, `snail`. Yard: `isopods`, `springtails`, `forage`. Town: `nugget`, `rival`, `kaid`, `route`, `townSign`. Shops: `shop-critz`, `shop-vet`, `shop-pharmacy`, `shop-bike`, `shop-glass`. Neighbor residents: `kaid`, `rivalMom`, `rivalDad`. `route` displays Forest route · Liarsville but remains inaccessible future content. IDs are map-local (e.g. multiple `exit`s), not globally unique; a reusable pipeline should use scene ID + entity ID. Preserve this identity mapping even if art/layout changes.

## Save migration requirements

- Keys are `critz-tycoon.save.v1` and `critz-tycoon.save.v1.backup`; schema is exactly `1`. `load` validates primary, then backup; no migration exists (`src/state.js:1`, `:370`, `:489`). A schema increment without a v1 reader would reject both valid legacy saves; changing the key without reading the old key would orphan them. A future migration must read both originals, validate/transform in memory, retain original raw snapshots, validate the result and write only after success. M0/M1 require no save change.
- Persisted position is `{x,y,facing}` in **fractional map tile units anchored at feet**, not pixel coordinates (`src/world.js:1`; `src/state.js:42`, `:100`). `TILE=24` only supplies rendering scale. Merely exporting 16-pixel art does not justify multiplying old coordinates by 24/16. A redesign to a new grid/layout needs an explicit per-scene conversion or documented nearest safe tile/landmark mapping for every saved position and every door spawn. Fractional starting coordinates, furniture extents, rescue points and door approaches are extensive.
- Global validation bounds are x 0–32 / y 0–27 regardless of scene, and do not check collision (`src/state.js:393`). Startup replaces a blocked loaded position with generic `[8,9.5]` without checking that fallback (`src/main.js:1156`). This is an existing convenience, **not** a reliable migration. New maps need named, proven-safe per-scene fallback anchors and a recovery notice where relocation is necessary. Transition return positions also derive from building rectangles (`src/world.js:311`), so they cannot silently keep old geometry.
- Carry through **all** progression: names/gender, stage, scene/player, money/debt/time, tank ownership and entire tank, rescued/visited and other flags, inventory, notebook entries, posts (images/scores/IDs/age/revenue), nextPostId and lifetimeEarned. Optional fields not initialized in `createState` include `storyBeat`, `flags.board`, `flags.medicineDelivered`, `flags.lastForage`, and `tank.hide`; a selective field copier can lose them (`src/main.js:163`, `:346`, `:408`, `:767`). Mid-opening resume intentionally restarts the opening and clears `storyBeat`; after loan decision it resumes morning (`src/main.js:814`).
- Storage is per browser origin. Changing hostname or port makes an existing save appear absent; preserve the launch origin or document export/import before relocation. Do not run migration QA against the user’s only save.
- Existing validation is partial: many flags, `visited` member values, money integer-ness, some history fields and post score objects are not validated. This is a recorded hardening gap, not permission to change saves during visual M0. A stricter future validator must tolerate/default legitimate omitted legacy fields instead of rejecting them accidentally.

## Controls and movement differences to stage deliberately

- Current movement is continuous fractional, diagonal-normalized, axis-separated wall sliding at 3.15 tiles/s walk and 5.2 run; facing follows x first, otherwise y; no grid commitment or independent turn state. Blocked input still returns `true` for animation (`src/world.js:298`). Interact chooses nearest entity within 1.65 tiles in any direction (`src/world.js:268`). Collisions currently reuse visual furniture/building rectangles with margins; NPCs do not enter `isBlocked`. A cardinal grid system must preserve approachability through new explicit collision/interaction layers, rather than carrying these distance constants blindly.
- All small scenes are 16×12 old tiles; town is 32×27 (`src/world.js:105`, `:134`). At 16 pixels these become 256×192 and 512×432, so simply changing tile/canvas constants does **not** reproduce the old room composition in a 240×160 viewport. Decide room geometry, border padding and camera behavior in M2.
- Arrow keys / lowercase WASD walk; Z/z, Enter or Space is A; X/x or Escape is B; P/p Start; Shift held runs; virtual RUN toggles; D-pad pointers hold movement or move menu focus. Panel arrows focus choices, Tab loops focus, A activates focused choice. B advances dialogue, backs tank subpanels to the tank, and opens pause from exploration. Opening/title/setup/loan block normal back/pause (`src/main.js:697`, `:954`, `:992`). Pointer release/cancel/lost capture, window blur and page visibility clear held movement (`src/main.js:961`, `:1062`). Preserve these semantics and touch accessibility.
- Current rAF loop uses variable `dt` capped at 50 ms (`src/main.js:1080`), no fixed exploration update. Skateboard scales outdoor run by 1.25 (`:1093`). Fixed-clock migration must avoid speeding/slowing habitat time, payment progression and simulated video duration, and must avoid hidden-tab catch-up.

## Existing automated coverage and relevant gaps

Ten domain/world tests cover both loan branches and idempotence, rescues, deterministic care, births/no deaths, inventory, Critter score/payout progression, same-schema round-trip/backup recovery, several malformed saves, door spawn validity/approachable interactions, collision/diagonal normalization/run (`tests/simulation.test.mjs:30`). The diagonal expectation at `:190` is an intentional prototype behavior to replace with an approved cardinal grid contract in M2, not preserve as Emerald behavior.

Browser runner walks actual held-key routes (no teleports), completes girl Hero/accepted loan, all rescues, shops, notebook/reward, neighbor homes, prescription, tank, photo/video, save/reload, four layout sizes and one virtual D-pad hold/release (`tests/browser.mjs:163`). Root owns actual execution/verification; these are inspected coverage claims, not a fresh pass from this audit.

Gaps for staged follow-up:

1. No cross-version fixtures/migration tests, fractional-position conversion, changed geometry relocation, or explicit per-scene restore matrix. Save tests need optional flags, post snapshots/scores, next ID, and exactly-once payouts **across reload**.
2. Browser reload currently asserts name/money/post count/rescued only (`tests/browser.mjs:297`); its success prose also mentions tank and inventory, which it does not explicitly compare. Preserve the full stated contract with direct assertions during migration.
3. No frame/update timing measurements, turn-only behavior, input commitment mid-step, opposed/simultaneous input policy, fixed-clock rates at 30/60/120/144 Hz, camera/border/occlusion assertions, or native-pixel image checks. New movement invalidates path helpers’ continuous half-tile targets (`tests/browser.mjs:63`, `:96`); adapt helpers, do not weaken reachability.
4. No browser decline-loan path, repayment, repeat reward/kit prevention, forage cooldown, pause/visibility habitat-clock assertions, night-resume checkpoint matrix, new-story cancellation or storage-error UI assertions.
5. Current viewport checks assert panel/A/B bounding boxes, not D-pad/RUN/Start reachability, controller separation from the native viewport, integer scale, keyboard focus flow, multi-touch cancellation, or physical Safari behavior (`tests/browser.mjs:308`). Pointer test uses mouse; touch-capable emulation is not physical multi-touch validation.
