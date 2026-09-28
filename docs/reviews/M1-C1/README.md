# M1.C1 — Animated character pixel budgets

Review delivery, awaiting the user's budget choice and art acceptance. The user likes the supporting-character concept designs and requested two native sizes side by side, including walking. This does not select a new production standard.

[Open the interactive comparison](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/budgets.html). Choose Mom, Kaid or Professor Nugget, let both walk the same loop, or use the keyboard/touch arrows. Pause, single-tick step and frame guides help inspect the drawings. Both room views use the current bedroom at 240×160; on narrow phones their horizontal scrolling is synchronized so pixels retain integer scale.

## Exact comparison

| Option | Native frame | Front-idle visible artwork | Shared movement |
| --- | --- | --- | --- |
| A, compact | 16×32 | Mom 14×21; Nugget 16×22; Kaid 13×20 | 16-pixel cells, 16-tick walking |
| B, more detail | 24×32 | Mom 20×26; Nugget 20×26; Kaid 18×26 | Identical controller, coordinates and gait phase |

Each budget is drawn independently, using the same palette for each character. Frame bounds include transparent padding. Additional width and greater painted height are intentional; this compares the proposed compact and more detailed proportions, not only extra horizontal padding. Both versions are displayed at exactly equal native-pixel zoom. The larger option retains chunky native pixels and the existing tile grid, while occupying more of the room. These are design tradeoffs for the user's review, not a claim that 24×32 matches Emerald's original sprite dimensions.

One transparent **288×192 PNG** contains **72 frames**: three characters × two budgets × four directions × three poses. [PNG](../../../assets/review/budget-comparison/atlas.png), [stable-ID metadata](../../../assets/review/budget-comparison/atlas.json), [native sources](../../../art/source/budget-comparison/README.md), [all frames at 4×](frames-4x.png). [Animated overview of all three characters](../../../assets/review/budget-comparison/character-budget-comparison.gif) uses exact 4× pixels in a 48-frame loop. GIF holds alternate 130/140 ms because GIF timing is stored in centiseconds; the interactive page retains the fixed simulation clock. [Lossless export validation](gif-validation.json). There is no new running set in this walking comparison. The full roster can follow the user's chosen direction later.

## Artwork provenance

The user's liked reference is the repository's [supporting-character study](../M1-I2/supporting-character-study.png). Mom keeps her warm brown skin, twin puffs, earrings and pink jacket; Kaid remains a child with a rounded teal pitcher, amber contents, cream shirt and asymmetric handle/spout; Nugget remains an adult with grey hair, spectacles, safari hat and cream coat.

The built-in image-generation tool produced [walking-study.png](walking-study.png) as a pose/design guide using that original concept as a reference. The [generation brief](prompt.md) records subjects and constraints. The generated guide is not a valid native frame sheet: its resolution, direction layout and Kaid's handle placement require interpretation. Its pixels were not downsampled or stretched into the game. The deliverable consists of separately authored indexed native rows with exact palette, bounds and anchoring, exported deterministically. No reference-game sprites or rejected environment-v1 artwork are included.

## Motion and preservation

The page imports the existing pure movement controller. One fixed simulation clock (`280896/16777216` seconds per tick) drives both versions, with 16 ticks per 16px cardinal step and a shared strideA → idle → strideB → idle gait, held eight ticks per pose. Release finishes a committed step; controller turning, blocked input and phase rules remain as documented in [REFERENCE_MEASUREMENTS](../../REFERENCE_MEASUREMENTS.md). Source-derived motion is not claimed emulator/frame-capture-equivalent.

The review imports no game persistence/entrypoint module, reads no game saves, and writes no storage. All 12 previously recorded gameplay runtime/assets other than `index.html` retain the M1.I2 hashes; `index.html` only adds a link to this comparison. The game retains its current cast, art, story, controller and v1 data. No art selection button records acceptance.

## Actual checks and limits

- **165 authoring checks** and **7 independent decoded-PNG checks** pass: all 72 stable IDs, complete directional poses, full frame sizes, binary alpha, nonoverlapping rectangles, exact native RGBA hashes, visible bounds, palettes, bottom-center anchors and unmirrored Kaid sides. [Authoring](asset-validation.json), [PNG](png-validation.json).
- **16 browser checks** pass in isolated Chrome contexts: all roles/budgets, shared gait, four-direction loop, pause/step, committed release, pointer cancellation, blur, reset, guides, reduced-motion start, load-failure feedback and zero writes to synthetic save sentinels. Layouts checked at 320×568, 390×844, 844×390 and 1280×900 with integer nearest-neighbor scales and no horizontal page overflow. [Report](browser-report.json).
- A selected-button hover contrast issue found in visual inspection was fixed and rechecked. Selected text contrast is **8.73:1**; landscape has no clipped canvases or button labels. [Focused report](hover-landscape-report.json).
- **45 existing domain tests pass**, including both loan paths, progress/recovery, coordinate migration, world reachability and fixed-tick traces across display rates. [Output](domain-tests.txt). This additive review does not re-run the prior complete story/browser journey; unchanged runtime hashes and domain results document that boundary honestly.

Desktop comparisons, mobile portrait/landscape and all native frames were visually inspected. Browser device emulation is not a physical iPhone/Safari test. The user decides whether either budget preserves the desired charm and whether these drawings/animations are acceptable. Technical checks do not provide that approval.

Publication succeeded; evidence is recorded in [PROJECT_STATUS](../../PROJECT_STATUS.md) and the [deployment receipt](deployment.json). Next action: review A versus B in motion and choose the budget/design direction before replacing the game's character artwork.
