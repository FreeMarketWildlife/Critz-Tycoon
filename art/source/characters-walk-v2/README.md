# M1.C3 — Native four-direction walking sources

Each JSON is an editable indexed drawing: `frames[direction][pose]` contains 32 rows of 24 one-pixel symbols. `.` is transparent; the canonical character palette supplies every opaque RGB color. Each of the twelve characters has `south`, `north`, `west` and `east`, with `idle`, `strideA` and `strideB` in every direction. The south idle and complete palette are exact M1.C2 originals.

All poses have a 20×26 maximum painted bounding box, 24×32 storage and anchor `[12,32]`. Idle feet finish on row 30; stride feet finish on row 31, with a one-pixel head/body bob rather than elongated anatomy. The two strides change arm and foot clusters. Directional asymmetries and artist decisions are recorded per character. Native artwork is authored as exact rows; generated pose guides are reference studies, not downsampled sprite exports.

From the repository root, with Node and Python/Pillow available:

```sh
node art/source/characters-walk-v2/build.mjs
python3 scripts/check-walking-atlas.py
python3 scripts/export-character-walks.py
node tests/walking-timing.mjs
```

The packer exports one 288×384 transparent PNG, stable asset IDs/metadata and twelve 288×32 individual sheets. The GIF assembler uses a fixed exact palette, nearest-neighbor enlargement and verified decoded output. The web player uses the fixed tick period from the pinned reference; GIF holds are rounded cumulatively to centiseconds. Source-based animation timing is not a claim of emulator-observed equivalence.

These are walking-review assets. The current playable atlas, controller and save data are unchanged. [Review notes, original guide prompts and validation](../../../docs/reviews/M1-C3/README.md).
