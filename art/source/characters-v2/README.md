# M1.C2 — Editable chibi stills

The JSON files are the canonical native drawings. Each character has one south/front idle pose; there are no animation frames. A symbol in `rows` is one pixel. `.` is transparent; other symbols resolve through that character's explicit RGB palette. Storage is 24×32, with at most 20×26 opaque artwork, bottom-center anchor `[12,32]`, and feet on row 30.

`design` records identity, body family, construction intent, head/body bounds and the shoulder division. Bounds use **left, top, right-exclusive, bottom-exclusive**, in storage-frame coordinates. These annotations describe Critz drawings; they are not claimed measurements of Emerald anatomy. Additional semantic/layer annotations are retained where supplied by the artist.

Run from the repository root:

```sh
node art/source/characters-v2/build.mjs
python3 scripts/check-character-stills.py
```

The second command requires Pillow. The packer exports the single shared atlas, individual transparent PNGs, stable metadata, native/4×/8× sheets and native validation. The independent checker decodes actual PNG bytes and verifies their equality to the editable sources, anchors, palette counts, bounds, connected silhouettes and enlargement. `kaid.mjs` is an additional drawing helper; the JSON still is the final reviewed source.

The two Hero options can also represent the opposite-gender, player-named rival, following the existing shared appearance convention. Other NPCs receive individual IDs even where the game previously shared a renderer appearance. New stills are review assets and are not installed into the playable game by this task.

The [drawing framework](../../../docs/CHARACTER_FRAMEWORK.md) and [review record](../../../docs/reviews/M1-C2/README.md) contain source/roster limits, prompts, provenance, technical checks and acceptance status.
