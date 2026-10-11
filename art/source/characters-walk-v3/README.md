# Corrected native chibi walk sources — M1.I3

These twelve editable indexed-pixel sources supersede v2 for the compact walking review. M1.ALL1 integrates the two parent designs from this bank while retaining the later approved Hero and C7 living cast already in gameplay. The v2 drawings and their review evidence remain available for comparison. All palettes are preserved; corrections repair garment continuity and unintended limb/outline artifacts, with the per-character audit in `docs/reviews/M1-I3`.

Frames use 24×32 transparent storage, `[12,32]` feet and at most 20×26 painted pixels. Walking is stride A, idle, stride B, idle with eight fixed ticks each. All four views are explicit; Kaid’s asymmetric handle/spout is preserved.

From the repository root:

```sh
CRITZ_WALK_VERSION=v3 node art/source/characters-walk-v2/build.mjs
CRITZ_WALK_VERSION=v3 python3 scripts/check-walking-atlas.py
CRITZ_WALK_VERSION=v3 python3 scripts/export-character-walks.py
node art/source/playable-characters/build.mjs
python3 scripts/pack-playable-atlas.py
```

Python commands require Pillow. The shared v2 exporter defaults to v2 for historical reproducibility; the explicit version switch selects these corrected sources and M1.I3 reports. GIF creation only assembles exported native PNG frames, with exact palette lookup and nearest-neighbor integer enlargement. No image-generation call is needed for these targeted edits to existing editable native artwork. Visual acceptance remains the user’s.
