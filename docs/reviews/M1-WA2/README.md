# M1.WA2 — Minute clock, tile walking and seamless water

[Play the updated phone test](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/water.html) · [Adventure clock](https://critz-tycoon.freemarketwildlife.chatgpt.site).

The user explicitly likes WA1 and requests these refinements. The clock now displays every minute—6:10, 6:11, 6:12—at 1.4 real seconds each. The full active day remains 28 minutes, 6am–2am. Saved data stays in the original ten-minute bucket plus remainder; the displayed minute, sky dial, lighting and music derive the intermediate minute. No schema/key migration or progress reset. Existing pause/early sleep/pass-out behavior remains.

The pond test imports the adventure's actual `src/movement.js`: fixed tick, turn in place, cardinal committed steps, walking poses and released collision behavior. The complete 32px water cells block travel; so do the two occupied bed cells. The shoreline's upper corners remain grass. Hero starts at cell(2,7), and waking places Hero on the clear bed landing(2,4). Controls and actors use tile motion; turtle proximity still uses the actual rendered Hero foot. The test remains disposable and does not read adventure progress.

Water now has 32 frames at 100ms each: a **3.2-second loop**. Each frame advances the ripples one native pixel through a complete 32px toroidal cycle, so frame31→0 is the same step as every other transition. The old eight-frame partial translation had a jump back at its wrap. Preserve the liked palette, native hard pixels and binary alpha. All twelve rock/turtle/fish/splash frames are pixel-identical to WA1 despite their new atlas positions. Calm freezes water; shadows stay separate. GIF exports exactly match the PNG frames and runtime cadence. New animation remains open to user visual feedback; no broader gate or adventure wildlife placement is inferred.

Clean release:174 unit tests including a minute-continuity/midnight/2am case; native 44-asset checks, 32-frame GIF equality and cyclic frame-difference measurements; phone/desktop browser report alongside this file. Test-harness polling was changed to await actual snapshots, and its shoreline expectation was corrected for the existing walkable corner cell. Synthetic save contexts only. Physical Safari remains unverified. Pre-existing character edits remain excluded and preserved. Baseline `bd5348551e8bbd03ec47240fb051416abef37ef7`, main. Final push/deployment evidence is in PROJECT_STATUS.

Next: try the refined walking and water loop and provide any remaining motion feedback. No user approval is self-issued.
