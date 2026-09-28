# M 1.C 3 — four NPC walking sets

Final staged handoff: **Juniper, Dr. Fern, Mina, Aunt Ember**. Each `{id}.json` has four direction keys (`south`, `north`, `west`, `east`), each with `idle`, `strideA`, `strideB`, each containing 32 rows of 24 symbols. Dots are transparent. Palette objects preserve canonical v 2 keys, order and values exactly. South-idle rows also preserve canonical v 2 sources exactly.

All 48 frames fit the 20×26 painted budget within 24×32 storage, anchored at[12, 32]. Idle feet end on row 30; stride feet end on row 31. Every stride moves the head/body down 1px and changes the arm and leg geometry independently. Heads do not morph or change expression during a direction's gait. Legs remain compact; no new longer shins or waist are introduced.

## Character-specific direction decisions

- Juniper: rounded bun follows the back of her head in profiles; the back has cream sleeves, apron straps, short waist tie and full teal hem. Cream cuffs and hands alternate visibly.
- Dr. Fern: rounded dark bob and swept fringe use distinct opposite-side treatment. The pink badge stays on the physical left chest: it is visible in the west-facing near-side profile, hidden in east and back views. The short cream coat retains its teal center in front/profile and plain light back.
- Mina: the petite lilac cardigan stays narrow. Profiles have one clear golden lens with a dark pupil and no high bun. Back hair hides the glasses; cardigan back has no front buttons.
- Aunt Ember: orange-tied textured bun remains high/back, goggles keep a dark strap around the back of the head, and the indigo apron gains straps/tie in back. Mustard sleeves carry the arm swing.

West and north poses are independently authored native rows. East uses mirrored geometry with re-authored upper-left hair light and Fern's explicit fringe/badge asymmetry. North has no face eyes. South idle remains the immutable supplied v 2 source; the new animation work does not claim to improve or approve that source.

## Files and checks

- `{id}.json`: canonical editable source in the requested schema.
- `{id}-{direction}-{pose}.png`: exact native RGBA exports.
- `{id}-proof-1x.png`, `-proof-4x.png`, `-proof-8x.png`: all 12 poses on light/dark backgrounds, inspected at all three scales. `I`, `A`, `B` abbreviate idle/strideA/strideB in native proofs.
- `final-validation.json`: 48 frame bounds/baselines, binary alpha, one 8-connected silhouette per frame, no empty internal scanline, exact south-idle/palette including key order, 12 unique frames per character, fixed head geometry with only the 1px stride bob, and separate arm/foot geometry changes on every stride.
- `{id}-validation.json`: individual native frame hashes and palette counts.
- `build.py`: deterministic original row authoring/export.
- `verify.py`: independent native-source and PNG checks.

The intended source-derived preview order is **strideA → idle → strideB → idle**, with 8 simulation ticks each at 280896/16777216 seconds per tick. These are walk poses only. Root owns the actual clock, animation page, GIF, shared atlas, publishing and browser validation; none of those is asserted completed by this handoff.

## Image-generation provenance

Four separate **built-in image_gen** calls produced `{id}-walking-guide.png`; `prompts.json` retains the exact prompts, references and default generated paths. The original generated alpha is preserved. Guides were inspected for directional identity and pose intent, but they are illustrative: they are not exact native sheets, and generation duplicated Fern's badge across sides. The native source corrects that physical asymmetry. No generated guide was cropped/downsampled into production pixels, and no reference-game artwork is included.

Profile face protrusions were reduced during inspection to keep cheeks/noses compact. Final proofs preserve the large-head/small-body proportions and each character's clothing/body family. Technical checks and this inspection do not constitute the user's final art or movement approval.
