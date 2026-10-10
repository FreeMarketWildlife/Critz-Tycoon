# M1.CT1 — Transition-tile contact lab

Playable comparison: https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/contact-lab/

**Awaiting user visual/feel review.** This is a separate review environment, not a replacement for accepted adventure movement or Map Studio collision. It uses the selected Black child Hero, existing native house/stone/wall art, and no adventure or editor storage. Canonical terminology and art direction live in [ART_BIBLE.md](../../ART_BIBLE.md#transition-tile-contact-study--m1ct1-user-correction); AGENTS links there.

## Try it

Start with **B**, hold Up, and switch A–D while standing still. Switch House / Indoor wall / Cliff to compare the same rule. Front / Left / Right / Behind move Hero to clear starting points. Arrows/WASD and the touch pad walk; 1–4 choose A–D. Close view follows Hero at 2× native scale. Show blocked cells / Grid / Lift art make the footprint and roof overlap inspectable. Grass, dirt, concrete and wood-floor variants are available for every fixture.

Compare **Fine approach · proposal** with **Full-tile steps · current spacing** separately. Add notes and press **Copy this choice for chat** to record the exact material split, movement choice and fixture. Copy falls back to a selectable text dialog. The preference does not automatically approve or integrate anything. The house is intentionally closed: no doorway warp interrupts the contact comparison.

| Option | Structure / ground in final 32px cell | Front idle-foot gap, fine approach | Gap with full-tile steps |
| --- | --- | --- | --- |
| A | 8 / 24px (25% / 75%) | 30px | 54px |
| B | 16 / 16px (50% / 50%) | 22px | 46px |
| C | 24 / 8px (75% / 25%) | 14px | 38px |
| D | 28 / 4px (87.5% / 12.5%) | 10px | 34px |

Percentages run downward from the tile's top. They describe the front material boundary, **never collision coverage**. The entire transition cell stays solid in all options. D reproduces the previous four-row ground-strip ratio; it is a comparison fixture, not a claim that every current building uses this exact assembly.

## Consistent method and limits

The generator translates the native source assembly by an integer number of pixels inside a padded transparent PNG. It composes the last row with the selected ground and exports the individual transition cells in a separate sheet. No scaling or squash is applied to the building or Hero. The same method generates house, indoor wall and cliff variants. The indoor fixture assembles native wall/skirting strips; the cliff's former four-row ground tail is replaced by its preceding rock row before composition. Wood floor is an original native pattern. Existing master and Hero atlases are unchanged. These review PNGs are intentionally separate from accepted atlases.

All A–D variants use the same five-cell-wide solid mask. The front solid row ends at world y224. The fine controller uses a 22×8 foot rectangle ending at Hero's bottom-center anchor: x±11 and y−8 through y−1. It checks every pixel of the two-pixel cardinal advance against full-cell collision, stopping at anchor y232 from the front. Grid comparison commits 32px steps over 16 ticks and stops at anchor y256. Both use the existing native Hero and the source-derived ~59.73Hz step clock. This small grid controller demonstrates current **spacing**; it is not a full reproduction of the adventure controller's turn waits, animation state, warps or M2 timing.

The measured gap is visible material boundary to the idle foot baseline (anchor−2). Animation changes visible pixels during a step, so compare at rest. Moving the wall base upward while keeping collision and anchor fixed necessarily increases this gap. A half-height ground band alone cannot fix distant contact. The fine approach changes the stopping position within clear ground while keeping every structural cell blocked. It is a new Critz proposal and requires user choice before any integration.

House roof art covers Hero behind the structure, where the foot rectangle remains on clear ground. Lift art exposes that relationship. Side/rear profiles are unchanged native silhouettes; A–D specifically compare the front/base split. Collision overlays are authoritative; alpha, decorative shadow or roof projection do not infer collision. This lab compares a solid cliff, not a ledge jump. Existing Map Studio provides directed ledges.

Bumps flash the foot outline without moving the camera. When `navigator.vibrate` exists and the toggle is enabled, each fresh bump requests 18ms once; continued held contact does not repeat. The page distinguishes unsupported, declined and requested states. A successful API return does not verify physical vibration. Safari/iOS does not expose this API in the inspected compatibility data. Physical phone vibration and Safari behavior remain unverified. [MDN API](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vibrate), [MDN compatibility data](https://github.com/mdn/browser-compat-data/blob/main/api/Navigator.json), [W3C vibration specification](https://w3c.github.io/vibration/).

## Pinned Emerald source observations

Reference: pret/pokeemerald **`5eff78649e7170a877b961ef0b3da13b81a16038`**. These are source/map/PNG observations, **not emulator or frame-capture measurements**. The researcher decoded little-endian map words, metatile descriptors, palette banks and flips; reconstructed the metatiles at their native 16×16 size; and inspected material rows. Coordinates below are zero-based layout cells. No Nintendo reference pixels are shipped in the lab or evidence screenshots.

| Example | Map cell; word; metatile | Native material rows, inclusive | Stored collision / elevation |
| --- | --- | --- | --- |
| Littleroot left house, window base | (3,8); `063A`; `23A` | Building0–15; wall9–13, contact14, foundation15; **no horizontal grass strip** | 1 / 0 |
| Same house, facade beside door | (4,8); `0638`; `238` | Building0–15, no full-width ground strip | 1 / 0 |
| Same house, door | (5,8); `0648`; `248` | Door/foundation0–15; separate entrance behavior `69` | 1 / 0 |
| Brendan's bedroom north wall below picture | (2,1); `0655`; `255` | Picture0–3, wall4–8, lower wall9–14, contact15; **no floor strip** | 1 / 0 |
| Clear floor immediately below | (2,2); `3278`; `278` | Floor0–15 | 0 / 3 |
| Route101 south-facing ledge | (7,6); `0487`; `087` | Grass0–7; six rock pixels in row8; rock fills9–15; jump attribute `103B` | 1 / 0 |
| Route111 cliff foot | (10,108); `30D3`; `0D3` | Rock0–1, taper2–4, only grass5–15 | **0 / 3, walkable** |
| Route103 cliff foot | (23,12); `30D4`; `0D4` | Rock0–1, taper2–3, only grass4–15 | **0 / 3, walkable** |
| Route103 full cliff wall | (58,4); `0479`; `079` | Rock throughout | 1 / 0 |

**Conclusion:** the inspected reference does not specify one universal half-building/half-floor tile. House and indoor wall examples run to the bottom edge; the ledge has an approximately half-height material break; cliff feet vary and can be walkable. Critz's always-blocked structural transition is the user's explicit rule, not a universal reference fact. Source code positions event sprites relative to map cells and handles collision/behavior independently of rendered material colors. Use those separate concepts, then choose Critz's visible split through this lab.

[Verified map words and downloaded source hashes](reference-check.json).

Pinned primary sources:

- [Metatile renderer](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_camera.c#L225-L310), [map-word masks](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/global.fieldmap.h#L4-L54), [event sprite anchor](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L1460-L1465), [coordinate conversion](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L4793-L4799).
- [Littleroot map](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/LittlerootTown/map.bin), [Petalburg metatiles](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/tilesets/secondary/petalburg/metatiles.bin), [source tiles](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/tilesets/secondary/petalburg/tiles.png).
- [Bedroom map](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/LittlerootTown_BrendansHouse_2F/map.bin), [house tileset](https://github.com/pret/pokeemerald/tree/5eff78649e7170a877b961ef0b3da13b81a16038/data/tilesets/secondary/brendans_mays_house).
- [General tileset](https://github.com/pret/pokeemerald/tree/5eff78649e7170a877b961ef0b3da13b81a16038/data/tilesets/primary/general), [Route101](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/Route101/map.bin), [Route103](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/Route103/map.bin), [Route111](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/Route111/map.bin).

## Validation and release

Task tests: `node --test tests/contact-lab.test.mjs`, `python3 tests/check-contact-art.py` (Pillow), and `node tests/contact-lab-browser.mjs` against the local server. Browser fixtures use disposable isolated contexts and synthetic saves only. The native check covers all48 assemblies and240 transition cells, dimensions, alpha, exact ground bands, source preservation and integer translation. The movement tests cover all directions, both controllers, whole-cell exclusion, 60,000 randomized steps, committed-step release and bump requests. Browser coverage includes all12 fixture/options, front/side/rear, controls, phone portrait/landscape, unsupported vibration, copy and unchanged synthetic saves. Screenshots in this folder show Critz art only.

Native QA also widened the foot rectangle from20 to22px to contain the extreme walking-frame foot pixels. An initial grid-side starting-position issue was caught by unit tests and fixed by placing grid-mode starts on full-cell anchors. The browser harness initially retained checkbox focus and therefore did not send walking input; focusing the play canvas corrected the harness. Final results and publication provenance are recorded in the adjacent JSON reports and project status. User choice and physical Safari/haptic testing remain outstanding; no broader M1/M2 gate is self-approved.
