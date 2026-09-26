# Reference measurements — Emerald exploration

Measured 2026-09-24. All Emerald file links below are pinned to pret/pokeemerald commit `5eff78649e7170a877b961ef0b3da13b81a16038` (repository HEAD at retrieval). This is source/asset analysis, not a frame-by-frame emulator observation. No reference-game artwork is copied into Critz. `Reference verified` means a cited source or measured PNG supports the value; `proposed for Critz` means an unapproved production choice; `unresolved` means evidence is incomplete. Source-derived coordinates/timing require capture confirmation at M2 boundaries. Current Critz discrepancies are in [AUDIT_M0.md](AUDIT_M0.md).

## Verified screen/tile/palette foundations

- **Reference verified, high confidence:** native framebuffer 240×160; 3:2 derives arithmetically; base tile 8×8. [Engine constants](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/gba/defines.h#L66-L76).
- **Reference verified, high:** a map metatile is 16×16: `DrawMetatile` writes four adjacent 8×8 cells in a 2×2 arrangement per layer. Eight tile indices encode two such layers, NOT an 8-tile-wide metatile. [Renderer](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_camera.c#L245-L306), [metatile constants](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/fieldmap.h#L4-L12).
- **Reference verified, high:** 4bpp graphics select from 16-entry palette banks, with index 0 transparent for sprite pixels. Hardware has separate background and object palette memory; sixteen 16-entry banks are possible in each, not one sixteen-color palette for the game. Emerald's map tileset constants allocate 6 primary palette banks and 13 map tileset banks total. Do not conflate those map allocations with the separate object banks or all UI/fade behavior. [GBA background documentation](https://gbadev.net/gbadoc/backgrounds.html), [object documentation](https://gbadev.net/gbadoc/sprites.html), [Emerald palette allocation constants](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/fieldmap.h#L4-L9).
- **Reference verified, high:** hardware refresh ~59.7275 Hz from 280,896 CPU cycles/frame and clock 16,777,216 Hz; ~16.7427 ms/frame. Hardware refresh is not an animation FPS. [GBA graphics hardware](https://gbadev.net/gbadoc/graphics.html).
- **Reference verified, high:** Brendan/May bedroom layout dimensions are 9×8 metatiles (144×128 before border presentation); their first-floor house layouts are 11×9. This describes map data extent, not a claim the screen crops to these dimensions. [Layouts](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/layouts.json#L534-L573).

## Reproducible sprite measurements

Method: read the pinned indexed PNGs with Pillow. Source PNGs have no alpha/transparency metadata. Derive visible mask from **palette index !=0**, then crop each source sheet into consecutive 16×frame-height cells, matching `overworld_frame(..., 2, 4, frame)` for 16×32 or `(2,2,frame)` for 16×16. Compute the nonzero-mask bounding box. A default RGBA conversion/alpha bbox would falsely count the background as visible. Bounding boxes below are `(left, top, right-exclusive, bottom-exclusive)` in zero-based frame coordinates; no outlines or hair pixels are excluded. Exact per-frame measurements and source SHA-256 values are in [emerald-sprite-bounds.json](reference-data/emerald-sprite-bounds.json); the reproducible [measurement script](reference-data/measure-sprites.py) takes the path of a local checkout at the pinned revision: `python3 docs/reference-data/measure-sprites.py /path/to/pokeemerald`. Requires Pillow. It reads reference PNGs but copies no art into this project.

Every numeric entry in this table is **reference verified / high confidence**:

| Reference | Frame canvas | Idle south, frame 0 bbox | Visible W×H | Width range all 9 poses | Height all poses | Last visible row idle / stride |
| --- | --- | --- | --- | --- | --- | --- |
| Brendan protagonist / rival | 16×32 | (1,10,15,31) | 14×21 | 14 | 21 | 30 / 31 |
| May protagonist / rival | 16×32 | (1,11,15,31) | 14×20 | 14 | 20 | 30 / 31 |
| Wally | 16×32 | (0,12,16,31) | 16×19 | 13–16 | 19 | 30 / 31 |
| Mom | 16×32 | (0,11,16,31) | 16×20 | 12–16 | 20 | 30 / 31 |
| Professor Birch | 16×32 | (0,11,16,31) | 16×20 | 14–16 | 20 | 30 / 31 |
| Generic little boy | 16×16 | (2,1,14,15) | 12×14 | 11–12 | 14 | 14 / 15 |
| Generic little girl | 16×16 | (1,1,15,15) | 14×14 | 12–14 | 14 | 14 / 15 |

Original PNG sources:

- [Brendan walking](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/brendan/walking.png)
- [May walking](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/may/walking.png)
- [Wally](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/wally.png)
- [Mom](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/mom.png)
- [Professor Birch](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/prof_birch.png)
- [Little boy](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/little_boy.png)
- [Little girl](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/little_girl.png)

The graphics metadata corroborates frame dimensions and proves RivalBrendanNormal/RivalMayNormal use the same image tables as the playable variants. [Metadata](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/object_events/object_event_graphics_info.h#L1920-L2033), [frame tables](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/object_events/object_event_pic_tables.h).

**Conclusion:** adults are not double-sized; Mom/Birch visible heights are 20 px versus Brendan's 21 px including headwear. Distinguish stature from frame allocation and from hats/hair. Generic tiny children exist but are not a mandate for ten-year-old protagonists.

## Anchors, collision, poses and semantic measurement limits

| Property | Reference measurement / status |
| --- | --- |
| Frame origin | **Reference verified:** upper-left frame coordinate (0,0) for PNG measurements. Engine sprite position is center-based; these are different conventions. |
| Ground alignment | **Reference verified, source-derived:** frame bottom center is (8,32) for 16×32, (8,16) for 16×16. Engine center = map-tile origin + (8,16−height/2), top-left = tile origin + (0,16−height). Thus bottom edge aligns to tile bottom; top of 16×32 frame projects 16 px above occupied tile. This anchor is a geometric edge coordinate, not the last painted foot pixel. |
| Foot baseline | **Reference verified:** final painted row 30 idle/31 stride in 32px frames; 14/15 in 16px frames. The stance poses include one-pixel vertical silhouette offset. Do not crop frames independently and lose alignment. |
| Collision | **Reference verified:** destination metatile/elevation checks plus current/previous object-coordinate reservations. This is not an alpha outline or 16×32 sprite rectangle. One occupied map cell is 16×16 ground space; runtime movement reservation can involve previous and destination cells. |
| Walking/idle pose storage | **Reference verified:** 9 source frames: 0 south idle,1 north idle,2 west idle;3/4 south strides;5/6 north;7/8 west. East is horizontal mirroring in the standard table. Four logical directions, three poses per direction, but only nine stored images. |
| Eye line | **Unresolved as a validated cross-character measure:** no semantic eye metadata. Manual front-image/index-map inspection suggests most eyes occupy roughly y18–20 in 32px frames, but hair, eyebrows, pupil outlines, hats and back/side poses require defined pixel annotation before calling any per-character number exact. |
| Head/body proportion | **Unresolved as an exact reference fact:** no anatomical segmentation. Bbox alone cannot establish skull/chin/hair boundary or body proportions. The measured large head silhouettes support chibi proportions; original Critz target ratios below are art proposals. |

Sources: [sprite placement](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L1460-L1465), [map-coordinate conversion](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L4793-L4799), [collision](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L4650-L4742), [directional pose definitions](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/object_events/object_event_anims.h#L178-L240).

## Suggested Critz specification, all PROPOSED FOR CRITZ and unapproved

These are M1 test constraints, not measurements of Emerald or finalized roster art. All main characters use a 16×32 transparent frame, frame-top-left (0,0), fixed ground anchor (8,32), idle last foot row 30, stride row 31, one 16×16 collision cell independent of painted silhouette. Pose exports should carry explicit left/right direction metadata; asymmetric designs may need twelve unique frames rather than blindly mirroring nine. Exact colors and semantic face pixels remain subject to lineup review.

| Character | Proposed visible W×H south idle | Proposed head silhouette / body height | Proposed eye band | Proposed poses |
| --- | --- | --- | --- | --- |
| Boy Hero, ten-year-old Black child | 14×20 | 12/8 px | y19–20 | 4 directions × idle+2 stride poses |
| Girl Hero, ten-year-old Black child | 14×20 | 12/8 px | y19–20 | same |
| Rival boy / girl variants, children | 14×20 each | 12/8 px | y19–20 | same |
| Kaid, child | 14–16×19–20 | expressive vessel/head silhouette 11–12; legs/body 8 | y19–20, final face unresolved | same; review asymmetric spout/handle in left/right |
| Hero's mother, adult | 14–16×21 | 11/10 px | y18–19 | same |
| Professor Nugget, adult | 16×21 | 11/10 px | y18–19 | same |

The head split is a design guide, not a hard horizontal chop through hair/accessories. Hero's skin ramp should retain a readable dark skin base/midtone/highlight without washing out the Black child identity. Adult age should read through shoulder/torso/clothing/silhouette and only slight stature difference, not doubled pixels. Kaid should have an original small rounded pitcher silhouette, compact legs/arms, expressive face and asymmetrical spout/handle details; avoid copying a branded pitcher mascot. Name remains Kaid.

Proposed environment scale tests (UNAPPROVED; do not label Emerald measurements): doorway 16×32 art with one-cell threshold; bed 32×32 art with 2×2 blocked footprint; chair 16×16 or 16×24 art with one-cell foot contact; desk 32×32; fence 16×16 modular segments; tree 32×48 canopy with 1×1 or 2×1 trunk footprint and foreground canopy; compact house 96×80 initial silhouette, grid-composed not fixed all buildings; starter tank 32×32 display fixture. Furniture artwork and footprint are separate metadata; some decorative pixels project above occupied cells. M1 bedroom sample should test hero/adult relationships against a door, bed, chair, desk and original 25-gallon tank fixture within one 240×160 render, with native 1× and nearest-neighbor 4× exports. Large exterior examples are proposals for M3/M5, not M1 scope.

Unresolved before final art standards: exact semantic eye/head annotations; texture/light/outline choices require M1 approval; actual environmental artwork dimensions should be measured on selected source tile assemblies if claimed reference exact; nonintegral phone display policy needs explicit product tradeoff; all runtime camera/motion validation remains a separate M2 gate.

## Clock, sprite cadence and displacement

All rows marked reference verified below are **source verified/source-derived**, high confidence in constants and sequences. No emulator or hardware gameplay capture was performed in M0. Exact first/last presented frames at action boundaries remain U003.

| Quantity | Reference verified | Proposed for Critz |
| --- | --- | --- |
| Hardware display refresh | CPU 16,777,216 Hz / 280,896 cycles per refresh = **59.72750057 Hz**, period ~16.742706 ms | Display refresh is the user's screen rate, separate from the simulation. |
| Normal overworld update | One input/callback iteration per VBlank in normal non-lagging operation | Fixed tick period `280896 / 16777216` seconds, driven by accumulator, independent of rAF frequency. |
| Normal walk | 1 native pixel/update; 16 updates per 16px step; ~267.8833ms | Reproduce in M2 harness. |
| Normal run | 2 native pixels/update; 8 updates per step; ~133.9417ms | Reproduce where run is allowed; preserve Shift/virtual RUN controls as Critz mapping. |
| Rest turn | Fast in-place action, 8 updates, zero displacement | Prove tap/hold behavior in M2. |
| Ordinary blocked on-foot attempt | Slow in-place action, 32 updates, zero displacement; interruptible in specific cases below | Reproduce only after testing exceptions; do not advance player's position. |

Clock sources: [main loop](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/main.c#L131-L168), [WaitForVBlank](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/main.c#L410-L415), [overworld callback order](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/overworld.c#L1438-L1475). Hardware timing is corroborated by emulator source: mGBA revision `1d201b22a86d31dfb3bc75145403711f6762015f`, [CPU clock](https://github.com/mgba-emu/mgba/blob/1d201b22a86d31dfb3bc75145403711f6762015f/include/mgba/internal/gba/gba.h#L20), [video constants](https://github.com/mgba-emu/mgba/blob/1d201b22a86d31dfb3bc75145403711f6762015f/include/mgba/internal/gba/video.h#L23-L33). These are technical sources, not evidence that we ran mGBA.

Reference animation indices address Emerald's logical player image table (walking/run images may come from separate PNGs). They are not proposed Critz asset IDs.

| Action | South sequence | North | West | East | Individual holds / phase |
| --- | --- | --- | --- | --- | --- |
| Idle | 0 | 1 | 2 | West flipped | Standing pose paused indefinitely; no idle bob cycle. |
| Walk | 3,0,4,0 | 5,1,6,1 | 7,2,8,2 | West flipped | 8,8,8,8 updates; full gait 32, one tile 16. |
| Run | 12,9,13,9 | 14,10,15,10 | 16,11,17,11 | West flipped | 5,3,5,3 updates; full gait 16, one tile 8. |
| Fast walk / turn action | Walk image sequence | Corresponding direction | Corresponding direction | Flipped | Commands hold 4 each; a turn action lasts 8 updates and consumes part of the cycle. |
| Slow blocked in-place | Walk image sequence | Corresponding direction | Corresponding direction | Flipped | Animation-delay advance every other action tick; effective holds 16; blocked action 32, not a full 64 gait. |

Walking/running phases alternate across steps; resetting to the first frame on every tile would lose the gait. Frame tables: [idle/walking/fast sequences](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/object_events/object_event_anims.h#L178-L271), [run](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/object_events/object_event_anims.h#L346-L379), [player animation table](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/object_events/object_event_anims.h#L979-L1003), [phase metadata](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/object_events/object_event_anims.h#L1146-L1159). In-place action code: [timers](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L5704-L5801).

## Input and step behavior

Reference verified (high confidence for ordinary on-foot path):

- Cardinal directions; held input selection precedence up, down, left, right. A normal step commits to its destination; release or direction change mid-step takes effect at a subsequent action boundary, not halfway through a tile. This is sampled held-state behavior, not evidence of a queued turn FIFO.
- From rest, a new facing direction selects turn-in-place; continued hold starts a step afterward. Turning during continuous movement at a tile boundary need not add the rest-turn action.
- Collision is checked before movement. It includes destination map behavior/elevation, barriers, map connections and object reservations; image transparency is irrelevant.
- Ordinary blocked walking starts the slow in-place action. A changed direction or a newly clear route can interrupt that action; release alone does not interrupt it.
- Reference running requires held B, the unlock flag and map/metatile permission. Brendan's bedroom forbids running. Critz can keep Shift/virtual RUN and choose room permissions, but those are explicit design differences. The existing skateboard's 1.25× outdoor benefit must remain available during eventual integration; how it maps to integer tick motion is unresolved, not permission to remove it.

Sources: [held input precedence](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_control_avatar.c#L89-L132), [player action acceptance](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_player_avatar.c#L332-L382), [turn/walk/run selection](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_player_avatar.c#L588-L679), [blocked/turn action selection](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_player_avatar.c#L1011-L1029), [blocked interruption](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_player_avatar.c#L353-L379), [step setup](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L5081-L5125), [step displacement tables](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L8191-L8312), [run permission](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/bike.c#L1056-L1061), [bedroom map](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/maps/LittlerootTown_BrendansHouse_2F/map.json).

## Doors and environmental animation

| Reference | Verified sequence | Hold / limits |
| --- | --- | --- |
| General flower | 0,1,0,2 | 16 updates each; 64-update loop. |
| General water | 0,1,2,3,4,5,6,7 | 16 each; 128-update loop. |
| General waterfall | 0,1,2,3 | 16 each; 64-update loop. |
| Standard door opening | Closed metatile, image offsets 0,0x100,0x200 | Table stores time 4, but compare-before-increment counter gives **5 task calls** per entry. End image persists. |
| Standard door closing | 0x200,0x100,0,closed metatile | Same 5-call entry cadence; final closed state persists. |
| Door entrance | Freeze → open → normal north step → close/hide → fade/load | Ordered source states verified; total displayed duration unresolved. |
| Door exit | Hidden/open → wait fade/weather → show/south step → close → unlock | Ordered source states verified; total displayed duration unresolved. |

Environmental callbacks have phase offsets 0/1/3 modulo 16 for flower/water/waterfall, so do not treat them as all changing together. [Animation arrays](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/tileset_anims.c#L77-L137), [callbacks](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/tileset_anims.c#L586-L674). Door timing: [tables](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_door.c#L135-L150), [counter](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_door.c#L391-L406). Transition state machines: [entrance](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_screen_effect.c#L677-L727), [exit](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_screen_effect.c#L317-L362).

These are representative ordinary cases, not a universal rate for every plant, water surface, door variant, battle or scripted effect. No environmental animation art is created in M0.

## Camera and borders

Reference verified/source-derived, high confidence in normal tracking path; medium until visual capture for exact screen coordinates:

| Situation | Reference behavior | Critz proposal / proof |
| --- | --- | --- |
| Ordinary on-foot tracking | Camera receives followed sprite's integer movement delta directly; no normal easing/dead zone. | Direct native-pixel movement, no generic smooth follow. |
| Standard 16×32 player frame | Canvas center `(120,72)`; top-left `(112,56)`; bottom-center edge anchor `(120,88)`. Last canvas row 87. | Reproduce in M2 and capture-check the visible foot, distinct from canvas edge. |
| Small room | Same normal tracker; authored bedroom 9×8 metatiles, not viewport-sized map clamping. | Show padded small room; test movement toward every wall. |
| Large map | Scrolling follows player; map connections update focus and carry adjacent strips. | Scrolling outdoor test plus boundary captures; no easing. |
| Map border | Authored map placed at offset 7,7; buffer width +15, height +14. Repeated 2×2 border fills absent data and is impassable; connections can replace border with neighboring map strips. | Separate authored dimensions, padded drawing extent and walkable region; padding values are reference implementation details, not new playable cells. |
| Doors / scripted camera | Door fade/load is separate; scripts can freeze/pan. Normal “pan ahead” branch is unreachable in the inspected path. | No extra smoothing; evaluate ordinary doors first. Special scripted cases unresolved. |

Anchor derivation: `MAP_OFFSET=7` gives 112px displacement; sprite center adds `(8,16−height/2)`; normal camera vertical pan is 32+8=40. Thus for height 32 center is `(112+8,112+16−16−40)=(120,72)`. This derives the frame placement, **not anatomical foot pixels**. Idle frame 0 last opaque row 30 therefore predicts screen row 86 for these assets; direct capture confirmation remains unresolved.

Sources: [camera update/pan](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_camera.c#L332-L505), [object camera init](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L2236-L2271), [map offsets](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/fieldmap.h#L18-L20), [border lookup](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/fieldmap.c#L51-L55), [buffer initialization](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/fieldmap.c#L91-L118), [border tile](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/fieldmap.c#L337-L344), [connections](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/fieldmap.c#L522-L631), [camera focus coordinates](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/fieldmap.c#L748-L757).

Border movement permission is checked through [map movement validity](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/fieldmap.c#L566-L575) and [object collision](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L4658-L4671).

## Fixed-clock implementation proposal (M2, not implemented)

Accumulate elapsed visible foreground time and advance exploration with constant `280896/16777216` second ticks. Sprite holds, committed tile displacement, inputs and camera update on those ticks; rAF presents the latest complete integer state without fractional interpolation. A 60 Hz display will occasionally repeat a state; a 120 Hz display repeats more often. Exactly 60 simulation ticks/sec would be ~0.456% faster than the reference and must be called an approximation if adopted.

Keep the habitat's 8-second active-hour clock, deliberate menu pauses, video countdown and monetary updates separate from the exploration timing refactor. Clear held inputs on blur/visibility change; reset timing on resume and do not simulate hours while hidden. Put a bounded catch-up policy and dropped-time diagnostic in the proof; the long-frame policy needs measurement/review rather than silently changing speed. Compare identical input traces under 30/60/90/120 Hz presentation; additional 144 Hz is useful. No rAF-dependent gait or eased camera positions.

## Unresolved register and verification plan

| ID | Unresolved item | Resolve / consequence |
| --- | --- | --- |
| U001 | Exact semantic head/body split and per-character eye lines in reference sprites | M1 annotate front pixels with an explicit hair/chin/eye definition; until then Critz dimensions are proposals, not exact anatomical reference matches. |
| U002 | Exact reference bed/chair/door/tree/building assembly bounds and contrast ramps | M1 measure selected assemblies if claiming reference-exact dimensions; original proposed dimensions can instead be judged as Critz art at G1. Outdoor assemblies can wait until M2/M3. |
| U003 | First/last displayed frame, gait phase at action boundaries, actual visible-foot screen position | M2 frame-step a permitted reference build/capture for idle→turn→walk→run, release/change mid-step and collision. Source tables alone do not establish every presented boundary. |
| U004 | Full door/fade/load elapsed time and variant differences | M2 record entrance/exit update traces and captures; do not use 20 task invocations as total warp duration. |
| U005 | Scripted camera exceptions / edge capture confirmation | M2 compare 9×8 room, town interior, impassable border, map connection and door. Ordinary tracking is sourced; special scripts remain outside proof scope unless encountered. |
| U006 | Phone presentation / UI readability | M1 review 1×/4×; M2 test integer scale with external controller; M6 approve any fractional option and text strategy on real phone. |
| U007 | Exact palettes, outline/light/texture decisions and Kaid silhouette | G1 user approves original sample; no approved examples currently exist. |
| U008 | Critz room-running permission, skateboard integer cadence, long-frame cap | M2/M3 explicitly preserve control/transport functionality and label deviations. G2 must approve a declared approximation if reference behavior cannot be reproduced. |

No unresolved item is silently converted into an exact-match claim. Where measurement cannot be obtained, present the proposed approximation and its effect in the relevant user review packet before integration.


## M1.E1 environment follow-up — 2026-09-25

The [environment construction study](reference-data/EMERALD_ENVIRONMENT_RESEARCH.md) narrows U002 with selected source-data assemblies: 32×32 tree, 80×80 house, 64×64 rug, shared primary/secondary banks and measurable tile reuse. These are allocated map rectangles, not universally segmented visible/collision bounds. Original authoring software/workflow, exact prop silhouettes beyond the selected assemblies, full dynamic rendering and emulator confirmation remain unresolved. Revision-1 Critz art was rejected by the user; measured dimensions alone do not establish a stylistic match.
