# M1.NET1 — Net Meadow

Playable review: [Net Meadow](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/net.html). Delivery is awaiting user visual/feel review. This prototype does not install catching or these review sprites into the adventure.

The user's October 15 request authorizes a pixel-art net that can be carried while walking, held ready while walking slowly, swung, and tested against catchable critters. Animal Crossing is the confirmed direction reference; no version, capture, exact range, timing or behavior has been measured from it. All new values are **proposed Critz test decisions**.

## Try it

- Arrows / WASD / touch D-pad: walk with the net.
- Hold Space / SWING: ready the net and creep. Release: swing.
- R / READY: latch the ready position so you can creep without holding the action; tap Space / SWING to swing.
- Face a critter and approach within roughly one net length. Fast footsteps startle nearby beetles; snails and isopods wander calmly.
- BAG / Escape / B: pause, inspect catches, release all, choose close or wide view, or show the catch area. Catches last for this visit only. Reload starts fresh.

The close view uses a minimum 2× integer display scale for legible tool pixels on phones; the camera follows through the same meadow. Wide view fits the existing 480px baseline, including uniform nearest-neighbor downscaling on narrow phones. The whole meadow is open ground: flowers and turf are decorative, no new static colliders, world expansion, purchases, fishing, inventory schema or save migration.

## Construction and proposed measurements

Art specifications and lessons live in [ART_BIBLE](../../ART_BIBLE.md#m1net1--pixel-net-and-catching-playground). Deterministic editable net source: `art/source/net-r1/build.py`. Native asset manifest includes per-direction hand registration, pose center coordinates, exact source hashes and sheet cells. Existing FM2 source `73434fc` supplies 16 unchanged 32×64 Hero images. These remain review candidates, not newly approved gameplay art. Existing C7 snail, stag beetle and isopod images are reused at their native size. No reference-game pixels are shipped.

| Item | Proposed test value | Evidence / limits |
| --- | --- | --- |
| Walk / ready movement | 96 / 38 native px/s | Fixed 60 Hz model; slow gait advances from traveled distance |
| Swing | 560ms total, strike at 180ms | Player position and facing lock for the swing |
| Catch center / radius | 34px ahead / 17px | Explicit ground-space circle, nearest eligible critter only, once per swing |
| Critters | Six, three existing kinds | Wander, beetle startle, temporary catch bag; no death or care simulation |
| Timing origin | Original Critz prototype | Not measured Animal Crossing or emulator behavior |
| Display | Close integer 2×, optional wide | 320×568, 390×844, 844×390, 1280×900 inspected in Chromium |

The net has a screen-space height offset from the catch ground plane, including the northward head clearance; its painted rim is not a collision mask. No hidden bones or new character anatomy are claimed. Tool hold centers are registered to the existing hand region; the unchanged walking arms are reused, so this first test does not add a dedicated two-handed body pose.

## Verification

- 322 unit tests passed, including five net model tests for four-direction movement, ready speed, catch timing/range/facing, one catch per swing, misses, startle and boundary clamping.
- Existing syntax checks and new net module syntax checks passed.
- 172 saved PNG checks passed: exact pinned Hero bytes, native dimensions, binary alpha, sheet equality, unclipped tool pixels and grip registration.
- Seven browser scenarios passed using actual input and read-only snapshots. Carry/creep, hold/release and a moving snail catch, pause/release, pointer cancellation/focus loss, four viewport layouts and real emulated two-finger touch are covered. All controls are at least 44 CSS pixels; no console/page/asset errors. Synthetic adventure save and backup markers remain exact, with zero storage writes.
- [Browser report](browser-report.json), [native report](native-checks.json), [phone touch capture](phone-two-finger-ready.png), [countable tool grid](tool-grid.png). [Pose inspector](../../../art-review/net-poses.html) provides native/3× synchronized poses, pause and stepping.

These checks validate the prototype, not user art/movement acceptance. Physical iPhone Safari and real-device touch feel remain untested. Production build, remote commit and deployment evidence are recorded in PROJECT_STATUS and the final delivery receipt.

Next action: user tests carry, ready/creep, directional swing and catches, then gives visual/feel feedback before adventure integration or additional tools.

## Publication receipt

Version **58** deployed successfully through the existing public Sites project. [Public phone test](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/net.html). All seven actual-input browser scenarios then passed on the hosted page, including an isolated emulated phone context without sign-in. An initial phone load timeout is retained in the initial hosted report; a fresh phone load and the complete unchanged suite passed on retry. Physical iPhone Safari remains untested.

All six moving critters were caught in six swings through actual keyboard input on the clean production build, including both beetles and both isopods; no state injection. [All-six report](all-six-report.json) and [bag capture](all-six-bag.png). [Production checks](production-browser-report.json), [hosted checks](hosted-browser-report.json), [publication/source/archive proof](publication.json).

Tested GitHub source `46881c32f6cde130176552a6fb830afb700125a2` was pushed and remote-verified; all6005 committed source files matched the Sites source byte for byte. Published Sites source `bf05494282db4bad3607675eb9f45bb3fa31d48a`, deployment `appgdep_6ad10acf33e48191b1a098f376f0d407`. Build checks verify4577 exact files,1269 equal JSON documents and the generated contact catalogue reconstruction. Two oversized archive attempts were rejected before saving; compacting copied review/source JSON and disabling macOS resource metadata fixed delivery without removing any media/pages or changing JSON values. Original authored files remain unchanged. Adventure `src`, root entry/style and accepted playable/character assets have zero diff against the previously published source.

This receipt and additional QA evidence are documentation-only follow-ups; the exact tested runtime is already deployed. User art/feel review is the next action. Unrelated workspace edits remain preserved.
