# Critz character framework — 20×26 chibi

**Current idle symmetry and review rules:** follow [ART_BIBLE: idle front/back symmetry](ART_BIBLE.md#idle-frontback-symmetry--mandatory-character-rule-2026-10-03) and [character review grid](ART_BIBLE.md#character-review-grid--required-presentation). Skull/body/eyes/arms/hands/legs mirror by default in front/back idle; hair and color can differ. Explicit unusual-character exceptions are recorded per feature. New characters use the 2× grid with centerline and ten-row guides; boy Hero continues with both 1× and 2× until the user accepts the style.

**Superseded production framework, 2026-10-02:** New assets must follow the [Emerald 2× visual contract](ART_BIBLE.md#emerald-2-visual-contract--authoritative-2026-10-02): standard 32×64 frames, exact doubled reference proportions and measured pose landmarks. The 20×26 painted ceiling, 24×32 storage, guessed head/body ranges and exact preservation of older idle pixels below are historical constraints, not requirements for new 2× work. Existing files and unfinished corrections are preserved; no new art is approved by this documentation update.

M1.C2, 2026-09-27. The user selected the larger **20×26 visible-pixel budget** and requested a new construction framework, distinct body types and **one still frame per character, no animations**. These proportions are Critz design rules, not measurements of Emerald anatomy. The pinned source facts remain in [REFERENCE_MEASUREMENTS](REFERENCE_MEASUREMENTS.md).

The goal is a compact, expressive cast: large rounded heads, small connected bodies, readable faces and short feet. Extra pixels clarify silhouette and identity. They must not become longer torsos, narrow waists or tall legs.

## Native asset contract

| Property | Rule |
| --- | --- |
| Painted budget | At most 20×26 pixels; a ceiling, not a requirement to fill every edge |
| Storage frame | 24×32 RGBA PNG, one south/front idle pose |
| Allowed painted region | x=2…21, y=5…30, inclusive |
| Origin / ground anchor | Top-left (0,0); bottom-center edge (12,32) |
| Foot baseline | Last opaque row 30; row 31 remains transparent |
| View | Overhead RPG front idle; crown and shoulders visible, head/torso same direction |
| Stance | Both feet planted; balanced small stance, relaxed arms |
| Color | At most 15 opaque RGB colors per sprite; alpha 0/255 only |
| Presentation | Native 1× plus exact 4×/8× nearest-neighbor views |
| Gameplay | Existing 16×16 ground cell remains separate from silhouette; this still-art task changes no movement or save data |

Transparent storage padding is not additional drawing budget. Hair, hats, handles and clothing all count toward 20×26. Export individual frames as well as a shared atlas with stable IDs. Never derive collision from the sprite's bounding box.

## Construction rules

Build the large head mass first, then fit a small body underneath it. Annotate head and body guides in editable source so reviewers can inspect the proportions rather than infer them from a hat.

- **Head with hair/hat:** normally 13–16 rows, around 55–62% of painted height. Face/head width 13–18px, with hair/hat permitted up to 20px. Use rounded, stepped clusters rather than box corners.
- **Body including shoes:** normally 9–11 rows. Torso 5–7 rows, legs/shoes 3–4 rows. Conceal the neck or show at most one row; no long waist or exposed shins.
- **Children:** usually 23–24px tall, with especially broad head-to-shoulder proportions. Adults generally 24–26px, but age must read through styling, shoulders, hair and posture. A hat does not establish age.
- **Eyes:** two deliberate dark clusters, often 1×2, with a clear skin bridge. Eyes must survive native-size inspection. Skin highlights cannot wash out the Black Hero's identity.
- **Face:** keep nose/shadow compact and mouth restrained. Avoid heavy dark cheek/chin lines that accidentally create a beard, a pointed snout or an unhappy expression.
- **Connection:** the head, neck/collar, torso, hips and feet must form a plausible connected figure. No entirely transparent scanline through the body or detached leg blocks.
- **Light:** consistent upper-left highlights, subdued cool shadows, short ramps and dark colored outlines. Put contrast around the face and silhouette, not random clothing texture.

These ranges guide deliberate drawings. Metadata records deviations and reasons; they are not an automatic character generator or a substitute for visual judgment.

## Different bodies, one visual language

| Starting body family | Shape to develop | Keep compact by |
| --- | --- | --- |
| Compact child | Broad head, narrow small shoulders, rounded cheeks | 10–12px clothing/arm width, tiny legs |
| Slim adult | Light shoulders and straight short clothing | 11–13px torso width; no extra height |
| Soft round adult | Rounded middle, broad sleeves, curved hem | 15–17px middle; connected short feet |
| Broad adult | Strong shoulders, wide short stance | 16–18px shoulders, 13–15px waist |
| Pear-shaped adult | Narrower shoulders, fuller lower garment | 15–17px lower body; no stretched skirt |
| Petite elder | Compact slightly lowered posture | Hair/face/clothing signal age |
| Sturdy elder | Broad short coat and confident stance | A full middle, not longer legs |
| Whimsical child | Oversized expressive nonhuman head | Small connected body; physical asymmetry retained |

Use these as drawing starting points, not interchangeable dolls. Every design must differ in at least two structural features beyond color: head contour, hair, shoulders, sleeve/hem, stance, accessory or body shape. Mix body families across ages and occupations; body size is not a personality, competence or moral cue.

## Identity and roster controls

Keep existing names and story roles. Hero remains a player-named ten-year-old Black child, with boy/girl options; the player-named opposite-gender rival is also a child. Kaid is a teal pitcher child, with warm amber contents, a handle and spout whose physical relationship is explicit. Mom and Professor Nugget are adults. The original supporting-character concept's strong silhouettes remain useful references.

The requested count is **102**, but the current repository/history audit found **12 story identities**, nine reusable appearance roles, and ten Hero/rival candidate designs. Animation frames and alternate views are not additional characters. The roster source/count has been requested from the user; do not invent 90 unnamed people and label them established canon. Work on the framework and confirmed cast can proceed independently.

## Per-character workflow

1. Record name/stable ID, source of identity, age category, key design cues, body family, dominant color and one recognizable silhouette feature.
2. Develop an original still design using the applicable image-generation workflow where helpful. Keep its prompt and provenance. A large generated illustration is a design guide, not evidence of native pixel compliance.
3. Author/refine at the actual native grid. Separate hair/head, face, clothing/body, hands, legs and signature-detail intent in the editable source or annotations. Do not stretch old sprites or downsample a large illustration and call it finished.
4. Inspect the silhouette alone and the full image at 1×/4× against light, dark and room backgrounds. Check head dominance, readable eyes, connected limbs, clothing clarity, age/identity and shape differences from nearby cast members.
5. Correct each drawing individually. A valid frame with awkward anatomy or a generic recolored silhouette is unfinished.
6. Export individual transparent PNGs, a shared atlas, source rows/palette and stable metadata. Validate bounds, baseline, alpha, color count, frame uniqueness and exact enlargement. Record actual review findings and remaining limitations.

Technical checks establish usable files. The user retains final acceptance of the character designs and their charm. This assignment produces one still pose; walking, running and playable replacement are separate work.

[View the annotated native construction plate](reviews/M1-C2/character-framework-annotated.png) · [Inspect the confirmed cast](reviews/M1-C2/character-still-contact-sheet.png).

## M1.C3 walking extension

The user subsequently requested walking for every delivered character. Keep each exact south idle and palette. Author north, west and east idle plus two distinct opposite strides in every direction. Store all twelve directional poses explicitly, including asymmetric designs; Kaid’s spout and handle retain their physical sides. Walking frames have the same 24×32 storage and at most 20×26 painted bounding box. Idle feet end on row 30; stride feet may end on row 31 with a one-pixel whole-head/body bob, so stride ink may occupy y=6…31. Do not enlarge the figure to achieve this movement. Keep connected hips, alternating short foot contacts, opposite arm swings and stable faces/accessories.

The source-derived walk is stride A, idle/passing, stride B, idle/passing, each held eight ticks at `280896/16777216` seconds. A full gait lasts 32 ticks and spans two ordinary 16-tick tile steps in the game; this review displays the gait in place. GIF delays are rounded cumulatively to 10ms. Animation review does not approve the drawings or integrate them into the game.

## M1.I3 correction and playable extension

The user’s follow-up authorizes correcting existing poses and integrating them into the playable visual-review game. Compare bilateral structure by anatomy and garment construction, not blanket RGB mirroring: hair parts, light direction, badges and Kaid’s physical asymmetry remain intentional. Inspect collar and sleeve continuity through all three poses, remove leftover hand pixels when a limb swings, and avoid shifting whole torsos sideways beneath stationary heads. A front idle may receive a documented local artifact correction; do not treat the earlier pixel-equality requirement as a reason to retain a known defect.

Historical I3 compact bank: use corrected `characters-walk-v3` for its GIF review. M1.ALL1 retains the later approved Hero/C7 cast in gameplay and uses this corrected bank for the two remaining parents. All twelve native frames per design retain the selected budget, anchor and cadence. Run mode currently reuses the corrected walking drawings at its existing 5/3 tick holds; dedicated running artwork remains a recorded limitation. Technical checks and playable integration do not establish user acceptance.
