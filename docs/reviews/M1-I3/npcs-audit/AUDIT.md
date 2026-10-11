# M1.I3 NPC native cleanup audit

Scope: Juniper, Dr. Fern, Mina and Aunt Ember; all 48 existing direction/pose combinations. These are proposed corrections for the parent's `characters-walk-v3` pack. The repository `characters-walk-v2` sources were read only and remain preserved. Final art acceptance belongs to the user.

The corrected source files are `juniper.json`, `dr-fern.json`, `mina.json`, and `aunt-ember.json` in this directory. They retain the complete source schema. No new image generation was needed: these are edits to the existing editable native pixel rows, with exact per-pixel logs. There are no palette additions, image resizes, generated pose substitutions or changes to gameplay data.

## Findings and corrections

| Character | Concrete findings | Correction | Exact changed pixels |
| --- | --- | --- | --- |
| Juniper | One front-idle elbow outline protruded one pixel to screen-left. Stride arm overlays retained old hand/cuff pixels, especially in north view, and had unequal outer widths. Profile hand relocation could leave cuff remnants. | Retracted the front elbow by one pixel; rebuilt only the lower arm strips from clean neutral clothing with paired three-pixel sleeves, one connected hand per side and a closed apron edge. Cleaned the former profile hand/cuff before placing each compact swung arm. | 137 |
| Dr. Fern | Pink badge pixels appeared on both the front coat panel and outer sleeve. A profile interior outline block looked like a missing coat patch. The forward profile arm overwrote the teal inner opening, and front/back stride overlays retained hand fragments. | Kept one two-pixel badge on her physical-left chest; restored cream/skin where the duplicate sleeve badge had appeared. Replaced the interior black coat block with the existing cream shadow. Moved the forward profile hand one pixel rearward so the teal opening remains continuous; rebuilt matched lower arm strips. | 96 |
| Mina | Front/back stride hands had broader overlay fragments than the still, and old profile cuff/hand pixels could survive a new arm placement. | Rebuilt paired compact two-pixel outlined arm strips and cleaned the old profile cuff/hand before placing the near arm. Kept cardigan center, buttons and compact body shape. | 83 |
| Aunt Ember | Front/back stride overlays left old skin-colored pixels inside the mustard sleeve edges, creating doubled or lumpy hands. Idle profile hand/cuff changed size relative to the walking poses. | Restored old skin fragments to mustard cloth, kept a single small hand per arm, and matched the idle profile cuff/hand to the existing stride construction. | 81 |

All 397 edits lie on rows 23–28, below the unchanged heads and above the unchanged foot rows 29–31. The complete coordinate/glyph changes are in `{id}-pixel-edits.json`; these logs use zero-based storage coordinates, with `.` meaning transparency.

## Every front-idle change

| Character | Coordinate | Before → after | Reason |
| --- | --- | --- | --- |
| Juniper | (3,26) | O → . | Remove one-pixel elbow outline protrusion. |
| Juniper | (4,26) | S → O | Place the outer elbow outline on the matched arm column. |
| Juniper | (5,26) | O → S | Continue the attached hand's skin shadow inside that outline. |
| Dr. Fern | (16,23) | V → W | Remove duplicate pink badge pixel from the outer sleeve. |
| Dr. Fern | (14,24) | A → V | Finish one continuous two-pixel chest badge. |
| Dr. Fern | (16,24) | V → S | Restore hand shadow beneath the sleeve instead of a second badge. |

Mina and Aunt Ember's front idle are byte-exact. All four north idles are byte-exact. Mina west stride B and Aunt Ember west strides A/B needed no corrections and remain byte-exact. Every other frame's complete change count is in `change-summary.json`.

## Reviewed and intentionally preserved

- All 48 heads/faces are byte-exact through row 20 for idle and row 21 for stride. Eye positions, facial expressions, one-pixel head bob, hair silhouettes/parts, Fern's fringe, Mina's glasses and Ember's goggles/orange tie/strap remain unchanged.
- All palettes retain their original key order and exact values. Upper-left highlights remain intentional color asymmetry, rather than being mirrored with silhouette geometry.
- Fern's physical-left badge is visible in south and west views and hidden in north/east. It remains a single connected two-pixel mark in each visible pose.
- Profile body alpha silhouettes are matched across west/east in every pose. Purposeful directional hair and lighting differences were preserved above the body.
- The existing distinct body types, aprons, coat/cardigan identity, gait phases, hip connection and foot contacts are retained. No foot pixels on rows 29–31 changed. All three poses in every direction remain distinct.

## Evidence and checks

`validation.json`: **487/487 checks passed across 48 frames**. It records source/corrected SHA-256 values and per-frame bounds. Checks cover 24×32 storage, unchanged [12,32] anchor, exact palettes, at most 15 colors, binary alpha, x=2…21, at most 20×26 painted bounds, idle last opaque row 30 / stride 31, connected eight-neighbor silhouettes, no empty internal scanline, exact PNG export, preserved heads, unique poses, paired profile body silhouettes, Fern badge placement and her continuous teal profile opening.

Evidence files:

- `{id}-{direction}-{pose}.png`: 48 native transparent PNGs.
- `{id}-before-after-{paper|dark}-{1|4|8}x.png`: before at left, corrected at right, all directions and poses at nearest-neighbor scale; native/light/dark and large-pixel proofs were visually inspected.
- `{id}-pixel-edits.json`: exact coordinate/glyph change list.
- `cleanup.py`: reproducible changes against the preserved v2 source.
- `validate.py`: checks and additional proof export.

The proofs show cleaner connected sleeves/hands and uninterrupted coat/apron panels at native and enlarged sizes. These checks establish artifact validity and document the reviewed corrections; they do not constitute user visual approval. Gameplay occlusion, collision and animation-in-scene checks are the parent's integration responsibility.
