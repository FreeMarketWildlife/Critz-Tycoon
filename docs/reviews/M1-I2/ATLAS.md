# Single playable PNG atlas

`assets/playable/atlas.png` combines the native environment and character exports without changing any source pixels. The 512×320 environment sheet starts at `[0,0]`; the 256×448 character sheet starts at `[0,320]`. The result is 512×768, with 54 environment entries and 216 frames across nine character roles.

`assets/playable/atlas.json` has schema version 1 and points to only `atlas.png`, matching `src/atlas.js`. The packer preserves every stable asset ID, anchor, animation mapping, role/direction/pose field, and other entry metadata. Only source rectangles gain their sheet offset. Whole-sheet and per-entry pixel comparisons include transparent RGB bytes.

Rebuild after authoring either source sheet:

```sh
python3 scripts/pack-playable-atlas.py
```

The script requires Pillow. For isolated output, pass `--source-root /path/to/project --output-root /path/to/output`. It writes the combined PNG, metadata, and `docs/reviews/M1-I2/atlas-validation.json`, and exits unsuccessfully before publishing atlas outputs if a check fails.

Checks cover unique IDs, bounds, nonoverlap, binary alpha, source pixel and metadata preservation, anchors, complete 4-direction × 2-mode × 3-pose matrices, all animation references, exact B1/G1 south walk-idle candidate pixels, and Kaid's explicit nonmirrored directional frames. PNG serialization is deterministic under the installed Pillow version. The report records source and output hashes.

These are technical validation results. Original artwork and Emerald-style movement remain a playable review awaiting the user's acceptance.
