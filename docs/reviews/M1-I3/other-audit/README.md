# M1.I3 — targeted four-character walk audit

Ready for root integration. This folder contains staged source corrections only; the project checkout, runtime, atlas, Git and Sites were not modified by this subtask. The user retains final visual and movement acceptance.

## Scope and findings

Inspected all 48 poses: Kaid, Ollie, rival-mom and rival-dad; each south/north/west/east idle/strideA/strideB. Reviewed the final native, 4× and 8× exports and before/after plates. Corrected editable palette rows, with no new guide, external pixels, palette change or global mirroring operation.

- **Kaid:** the profile strideA shirt/collar previously shifted horizontally beneath a head that only bobbed vertically. Restored each profile's own garment alignment and gave the hands and short legs opposite articulated phases. Retained all jug-head pixels and the intentional topology: west has the near handle loop; east has the near spout and an occluded far handle. Front/back handle loops and spout sides are unchanged. All eyes and highlights are unchanged.
- **Ollie:** the cream shoulder bands disappeared from the north strides. The rear upper shirt now retains those bands throughout both phases. Removed the profile collar/torso shift and retained the original directional cream front trim. Hands swing with matching outlines; feet trade consistent forward/back silhouettes. Hat brim, cap highlights, hair and face are unchanged.
- **Rival-mom:** the back collar/blouse shape changed between the idle and stride poses. Kept the canonical directional collar and blouse hem aligned through the bob and restored the localized arm/leg swing. Preserved the individual profile hair contours and the south hair part. No face or head edits.
- **Rival-dad:** fixed the profile collar/torso offset and stabilized the green shirt hem while articulating the hands and short trouser legs. The front/back hands now exchange positions with matching lengths. Preserved the asymmetrical hair tuft, profile lighting and all facial pixels.

### Explicit no-change decisions

All 16 idle poses, all 48 head/face/accessory regions, every palette, the 24×32 frame contract, anchor metadata, native scale and sequence timing are unchanged. Deliberate near/far-side differences, lighting and hair/hat/jug asymmetry were not forced to match. No unrelated characters were edited.

## Files

- `characters/{kaid,ollie,rival-mom,rival-dad}.json`: final corrected sources, ready to copy over the same IDs in `art/source/characters-walk-v2/`.
- `before/`: exact pre-audit source snapshots.
- `edits.json`: all exact row-coordinate/color changes, per character and pose.
- `proofs/*-before-after-4x.png`: left original, right corrected, identical light background. Rows south/north/west/east; columns idle/strideA/strideB in each half.
- `proofs/*-{before,after}-{native,4x,8x}.png`: transparent full-sheet source exports; individual pose PNGs are also present.
- `validation.json`: 644/644 technical checks passed across all 48 frames.
- `export-manifest.json`: current SHA-256 hashes for source and evidence.
- `correct.py`, `validate.py`: reproducible native source edit/export and technical validation.

## Validation and limits

Checked 24×32 rows and allowed palette codes; ink width/height at most 20×26; x ink bounds 2..21; idle foot baseline 30 and stride baseline 31; one connected eight-neighbor ink component; no empty scanline within each figure; distinct opposite arm and foot phases; exact one-pixel downward head bob; unchanged head/face/accessory pixels and all idle poses; aligned collars; binary-alpha PNGs matching the final JSON exactly; exact nearest-neighbor 4×/8× exports; correct Kaid loop topology and independently authored east profile. All 644 checks pass.

These checks establish consistency and export integrity, not user acceptance or exact Emerald equivalence. Compact pixel anatomy still needs the user's visual review. Runtime timing, motion feel, atlas integration and in-game running mapping belong to the root task; no claim is made here about them.
