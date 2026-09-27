# M1.I1 — Recovered art, one atlas

User goal: update the playable game with the new Emerald-style artwork and tile movement. This review supplies the recovered original art handoff needed for that goal; it does not claim the full game update is complete.

Published review: [open on phone](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/integration.html). Native deployment succeeded for source `1c1c62bcff554394ae27c5b02501e6554abdedfb`; receipt in PROJECT_STATUS. 18/18 review checks, 10/10 domain tests and 14/14 existing browser checkpoints passed. Physical Safari remains untested.

- [Static scene review](../../../art-review/integration.html): ten character choices, doorway and tree placements, 16px grid.
- [Combined PNG](../../../assets/review/integration-v1/atlas.png): 256×160, 23 entries.
- [Runtime manifest](../../../assets/review/integration-v1/atlas.json): stable asset IDs and exact rectangles.
- [Original character metadata](../../../assets/review/characters-v1/source-manifest.json), [editable source](../../../art/source/characters-v1/README.md).
- [Pixel validation](atlas-validation.json). Rebuild with `python3 scripts/pack-review-atlas.py` using Pillow.

The 13 revised environment parts retain their original positions in the top 256×128. Ten unmodified 16×32 character images occupy the next row. Every source crop is compared byte-for-byte in RGBA, including transparent pixels. The original character PNG hashes also match their handoff manifest. Atlas PNG SHA-256: `e0dae602ae0a52bdbb0c452e9e980c2337f38fdbde6201305e05fb84c4b3f431`.

All 23 assets await review. B1 is only the initial preview selection; none is selected as the canonical Hero or rival. Original task `01a0d6b8-9fb4-78f1-b303-7c01d427e62f` supplied the candidates; none was a walking sheet. The source package's reference-only material and generated illustration were excluded. Rejected environment revision 1 is also excluded.

The page composes a 240×160 scene directly from atlas entries with nearest-neighbor rendering and integer CSS scale. Hero candidates share a `(8,32)` frame-bottom anchor. Tree placement demonstrates artwork draw order only; it has no collision rules, inputs, movement or saved game state. The appearance loader lives in `src/atlas.js` and is not imported by the production game. Buttons are previews, not approval submissions.

Still needed: a chosen/approved character direction, side/back/walk/run poses, Mom/Kaid/Professor Nugget and the revised indoor kit. Emerald tile movement is a separate code change; the existing game remains continuous/diagonal. Exact source-derived movement targets and unresolved observations are in `docs/REFERENCE_MEASUREMENTS.md`. No emulator capture was made here.

Pending user decision: authorize a combined missing-art and movement playable review, or retain staged art then movement approval. Neither G1 nor G2 is self-approved. The current game and its v1 saves remain intact.
