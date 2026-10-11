# M1.ALL1 — Full game integration

The user's 2026-10-10 request explicitly authorizes all completed game, tiles, animations, characters, water, autotiling and Luke-greenhouse work to enter gameplay. Earlier review-only integration boundaries for these deliverables are superseded. Wider visual/feel approval remains the user's; rejected revisions and future ideas stay historical/planned.

## Play

[Phone game](https://critz-tycoon.freemarketwildlife.chatgpt.site)

- Walk north at the **LUKE ↑** sign beside Rootport's directory, then walk north through the native garden into Luke's greenhouse. Start → Luke's Greenhouse is another entrance.
- The greenhouse uses actual adventure savings. Admission costs $100; missed scoops cost nothing; leaving before catching refunds admission. Caught fish and completed/unfinished visits persist in the existing v1 adventure save. The old standalone review wallet/collection stays intact. Goldfish remain a separate collection rather than being stocked into the 25-gallon terrarium.
- Start → Visit the coast opens all six landscapes with the selected Hero, adventure clock, animated water, beaches, shallows, reflections, rock turtles and fish.
- Map Studio has sand and eight explicit freshwater/ocean × still/moving × shallow/deep brushes. Deep water blocks; shallows walk. Map checking flags unsupported thin water cells. Existing map files retain their format/key and import/export losslessly.
- Start → Play my map opens the saved Map Studio project. Edit/import in Map Studio, return to play, and test terrain, passages, edge connections, ledges and boulders. Custom-map exploration is disposable and preserves adventure progress and the authored map. It does not replace Rootport's authored story layout.
- The later approved Hero/C7 cast, animals and habitats stay intact. The two corrected compact parent designs replace their placeholders. The full unfinished compact-character bank, animations and audits are published as sources/reviews alongside the current game. Runs reuse existing walk artwork; no new dedicated run drawings are invented.
- Current WA8 shore geometry is shared by main outdoor water and Map Studio. Freshwater reflects actors; ocean excludes actor reflections. Mixed depths have curved color edges and no stone bank. Sky/cloud windows, shallow-still foot rings, B contact and separate collision/overhead rules remain.

## Verification

215 unit tests; 60 JavaScript syntax checks; 310 lossless atlas/source checks; 986 independent decoded compact-frame PNG checks. 118 isolated browser checks across adventure (17), living collection (10), Map Studio (22), greenhouse (16), walking gallery (14), all doors (30), and final built-release integration (9). All pass; no browser exceptions/missing assets in successful runs. Synthetic contexts/fixtures only, including save failure rollback, cents, payment/refund, caught-fish reload, custom maps and walking greenhouse entry. Physical iOS Safari/haptics remain unverified.

A stale atlas audit compared source-sheet rectangles against packed coordinates; correcting the audit to use packed rectangles confirms exact source pixels. No art was resampled to make the audit pass. Earlier combined browser attempts ran against files during edits or used asynchronous polling/timing that captured a previous scene; final release uses synchronous module snapshots and confirms the actual garden and room. Historical C7 screenshots generated during regression were restored; task evidence is kept here.

Work stays on main. The existing feature/playable-foundation branch is already an ancestor, with no unmerged work; it is retained. Publication/source SHA and archive proof are recorded in deployment.json after native success. Preserve owner-private audience, original save keys/data, story, optional loan, gift, all surviving animals, and selected soundtrack. Exact next action after publication: try the integrated game and report any specific visual/feel refinement.
