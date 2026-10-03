# Critz: Tycoon — art bible

## Current Wildlife palette — 32 slots, 2026-10-03

The user supplied the following exact palette for the Sprite Editor. **Slot 00 is transparent; slots 01–31 are fully opaque.** This replaces the editor's previous selectable Critz banks. All 31 opaque colors may be used together in an editor character project; the older proposed 15-color restriction below is superseded for this workflow. Palette selection is not artwork approval, a reference-game palette claim or authorization to recolor existing gameplay assets.

Editable source: [sprite-editor/palettes.json](../sprite-editor/palettes.json). Preserve the slot order, exact RGB values and names. Existing project pixels retain their legacy colors on open/restore; do not silently quantize old artwork. New drawing/imports use this palette. Reference overlays may retain their source/averaged colors because they are inspection-only and excluded from shipped artwork/exported sprites.

| Slot | Exact value | Color | Family |
| --- | --- | --- | --- |
| 00 | `#00000000` | Transparent | Transparency |
| 01 | `#E84038` | Saturated Ruby Red | Tropical vibrant creatures |
| 02 | `#FC7858` | Coral Salmon | Tropical vibrant creatures |
| 03 | `#FCD080` | Warm Belly Yellow | Tropical vibrant creatures |
| 04 | `#289870` | Tropical Teal Green | Tropical vibrant creatures |
| 05 | `#48D098` | Saturated Mint | Tropical vibrant creatures |
| 06 | `#A0F8D0` | Seafoam Cream | Tropical vibrant creatures |
| 07 | `#F85888` | Bioluminescent Pink | Tropical vibrant creatures |
| 08 | `#082048` | Midnight Trench Blue | Reef & deep water |
| 09 | `#184080` | Sunken Sapphire | Reef & deep water |
| 10 | `#3878B8` | Classic Surf Aqua | Reef & deep water |
| 11 | `#68B0E0` | Shallow Lagoon Teal | Reef & deep water |
| 12 | `#98E0F8` | Crisp Glass Ice | Reef & deep water |
| 13 | `#F8F8F8` | Pure Bubble White | Reef & deep water |
| 14 | `#201008` | Damp Humus Black | Substrate, wood & roots |
| 15 | `#482810` | Bogwood Brown | Substrate, wood & roots |
| 16 | `#784820` | Mangrove Bark | Substrate, wood & roots |
| 17 | `#A87038` | Golden Tan Oak | Substrate, wood & roots |
| 18 | `#D0A068` | Desert Clay/Sand | Substrate, wood & roots |
| 19 | `#F8D8B0` | Soft Silicate Sand | Substrate, wood & roots |
| 20 | `#083018` | Overgrown Shadow Green | Forestry & rainforest canopy |
| 21 | `#185828` | Monstera Leaf Base | Forestry & rainforest canopy |
| 22 | `#388840` | Vibrant Emerald | Forestry & rainforest canopy |
| 23 | `#68B858` | Chartreuse Sprout | Forestry & rainforest canopy |
| 24 | `#A0E068` | Vivid Lime | Forestry & rainforest canopy |
| 25 | `#D8F880` | Acidic Shoot Yellow | Forestry & rainforest canopy |
| 26 | `#282830` | Obsidian Iron | Hardscape & hardware |
| 27 | `#484850` | Weathered Basalt | Hardscape & hardware |
| 28 | `#707078` | River Slate | Hardscape & hardware |
| 29 | `#9898A0` | Pumice Ash | Hardscape & hardware |
| 30 | `#C0C0C8` | Polished Chrome Filter | Hardscape & hardware |
| 31 | `#E0E0E8` | Anodized Aluminum | Hardscape & hardware |

## Emerald 2× visual contract — authoritative, 2026-10-02

**User-confirmed direction:** Critz uses Pokémon Emerald's art style, camera framing and character proportions at **twice the linear pixel resolution**. Use the selected reference's face/body landmarks, pose, overlapping forms and pixel rendering to construct original characters. Separate the skull, exposed face, hairstyle and headwear. Matching the highest hat/hair pixel or full opaque bounding box is not anatomical fidelity; original hairstyles do not have to reach a reference hat's tip.

This contract supersedes conflicting production dimensions, generic chibi formulas and 20×26/24×32 constraints below and in CHARACTER_FRAMEWORK, PROJECT_PLAN and older prompts. Those passages remain historical records. It does not retroactively certify existing assets, implement a renderer migration, approve finished art or expand the authorized roster/world. GAME_VISION remains story canon.

### Current correction — register the actual references; separate skull, hair and headwear (revision 7)

**User instruction, 2026-10-02:** retain the four supplied Black boy designs (rounded afro/teal raglan; flat-top/gold vest; short twists/red stripes; cornrows/blue jacket and olive shorts). Lay out **five full 32×64 grids, Brendan first**, then align the actual supplied character references over Brendan before transferring their designs. Preserve the reference designs' head-to-body proportions. Idle front only; no animation or accepted gameplay replacement.

**Two rejected mistakes, both revoked:** R4 treated Brendan's high hat tip as required skull/hair height and stretched the heads. R6 overcorrected by independently shortening the head/hair and forcing bare heads to the hat's lower boundary. This flattened the afro, twists and especially the cornrows. Native row 36 (review Y=28) is Brendan's central **hat-to-exposed-face boundary**, not a universal bare-head hairline or a measured skull crown. His hat hides upper forehead. The historical R5 diagnosis below was incomplete: extra exposed forehead is not automatically a proportion defect in an uncovered head.

Register each supplied design as a **whole figure with one uniform scale for X and Y**, centered at x=16, matching eye and foot landmarks while checking jaw, neck, shoulders, hands and legs. Compare this actual-source overlay with the final native-grid transfer. Do not scale the head, hair, torso or limbs independently to satisfy a mistaken rectangle. Build or annotate the symmetric cranium separately, explicitly labeling hidden anatomy as inferred construction. Hair sits around that skull and may vary in height/volume; a rounded cornrow hairstyle must retain cranial volume rather than becoming a thin horizontal cap.

The 32×64 frame is capacity, not required body height. Neither the former 33–35px figures, the miscounted 36, nor Brendan's 42px headwear-inclusive extent is a mandatory height. Keep transparent padding. In R7 the supplied designs, uniformly registered, occupy **24×38 / 24×39 / 24×38 / 24×37**; the supplied Brendan reconstruction occupies **26×42**. This preserves design proportions and registers eyes/feet; it does not claim identical clothing silhouettes or recovered hidden skull measurements.

**Review evidence:** show the five grids first, with one native pixel per square, x=16 symmetry line, horizontal guides every ten pixels, **Y=0 at bottom and Y=64 at top**. Preserve all 64 rows. Include the real source-over-reference registration as supporting evidence and inspect native-size, enlarged clean and gridded results before delivery. Technical dimensions and symmetry checks alone cannot establish reference fidelity or visual acceptance. Only the user accepts the artwork.

R7 is a **reference-traced native transfer**, using the complete supplied concept screenshot and a 24-color per-character quantization, followed by paired body contours and exact eye placement. It is not a byte-exact screenshot copy, a new hand-drawn production sprite, or an approved global palette change. Preserve these source colors for this requested comparison; the Sprite Editor's Wildlife palette remains a separate workflow. Avoid resampling noise in production art: reference transfers are review evidence, and any later palette/cluster refinement must retain the accepted design. See [R7 method and measurements](reviews/M1-C4/revision-7/README.md).

### Resolution and framing

| Quantity | Reference basis | Critz target |
| --- | --- | --- |
| Exploration raster | 240×160 | **480×320**, same 3:2 view |
| Total raster pixels | 38,400 | **153,600** (4× area) |
| Standard human overworld frame | 16×32 | **32×64** transparent canvas |
| Small NPC/item frame family | 16×16 | **32×32**, where that reference family applies |
| Map metatile | 16×16 | **32×32** |
| Base art tile | 8×8 | **16×16** |
| Battle/intro front/back frame budget | User-supplied 64×64 basis | **128×128** when such assets are authorized |

Battle/intro dimensions are a user-selected production budget, not a newly verified universal fact about Emerald portraits or an instruction to implement battles. Do not substitute Platinum, HeartGold, remakes or other generations for the Emerald reference.

Scale viewport, artwork, rendered distances and camera offsets together. The view remains 15×10 metatiles, not a zoom-out showing more world. Keep the controller outside it. At 2×, a standard bottom-center frame anchor `(8,32)` becomes `(16,64)`; the 16×16 family anchor `(8,16)` becomes `(16,32)`. Edge coordinates double; an inclusive pixel row `r` maps to rows `2r` and `2r+1`: reference idle foot row 30 becomes rows 60–61, stride row 31 becomes 62–63. Do not mistake transparent frame padding for body height.

The existing ledger's south-idle bounds imply these **derived, not newly measured full-silhouette examples (including hair/headwear), not required anatomy or mandatory heights for original hairstyles**: Brendan 14×21 → 28×42; May 14×20 → 28×40; Wally 16×19 → 32×38; Mom/Birch 16×20 → 32×40. These examples show why a 32×64 frame must not be filled by a 64px-tall person. Select a specific measured reference family for each Critz design; there is no single universal Gen 3 head/body ratio.

### Mandatory measured construction

1. Inspect actual native Emerald overworld frames from pinned revision `5eff78649e7170a877b961ef0b3da13b81a16038`, using the ledger's transparency rules. Record source path, frame index, direction, revision and method. Use gameplay captures for camera/motion claims; label source-only evidence accurately.
2. Before production, create an annotated measurement table per representative body/pose family: full opaque bounds; head width/height; face/eye/chin landmarks; hair and hat envelopes separately from face/head; shoulder and torso widths/heights; arm/hand bounds and attachment points; leg/shoe bounds, stance and contact points; ground anchor; all pose offsets. Each row must contain reference coordinates or dimensions, exact 2× target where that same feature applies, actual Critz value and deviation. Label headwear-only extents and hidden anatomy explicitly; do not turn an inapplicable hat height into a skull target. Head/eye/limb segmentation remains unresolved in the old ledger: inspect and annotate it instead of inventing values.
3. Use the measured structure as the drawing scaffold in front, back and both profiles. Preserve face/body relative size, placement, overlap and foreshortening. Compare silhouette mass by anatomical region; the highest hair/hat pixel is not a universal head-height target. No improvised taller torsos, long shins, narrow waists, oversized hands/shoes or enlarged hair/hats merely because the canvas has room. Distinct body types use corresponding measured reference families. Kaid's nonhuman vessel/spout/handle require a labeled original adaptation while limb scale, ground contact and gait stay coherent; do not pretend Emerald contains an exact Kaid template.
4. Author original Critz PNGs and editable pixel sources against that scaffold. Reference sprites remain inspection material, never shipped game assets. Preserve the Black child Hero, child rival/Kaid and adult Mom/Nugget. Do not recolor reference characters and call them original designs.

### Idle front/back symmetry — mandatory character rule, 2026-10-03

**User-confirmed:** we are committed to the measured **Emerald 2× style and pixel budget**. New standard-human character reviews use 32×64 frames. Derive face/body landmarks from the selected reference; measure actual painted bounds separately after original hair/headwear construction. Do not force those bounds to match a hat-bearing reference. Older approximate chibi budgets are not alternate defaults. Show the user the measured reference proportions and their doubled targets **before drawing**, with the reference revision, frame/pose, annotation definitions and unresolved hidden anatomy clearly identified.

For **front idle and back idle**, the underlying skull/cranium, face construction, eye positions, torso/body, shoulders, arms, hands, hips, legs and feet must be bilaterally symmetric by default. Corresponding parts have mirrored contours, equal dimensions and area, equal attachment heights and equal offsets from the centerline. The eye positions and shape must mirror; matching outer alpha alone is insufficient. A larger hand, a lower shoulder or displaced eye is a defect unless the user explicitly requests that structural exception.

- Mirror geometry across the vertical line halfway across the X extent: `x = frameWidth / 2`. For native pixel indices the partner is `frameWidth - 1 - x`. A 32×64 frame has its centerline at edge coordinate **x=16**, between columns 15 and 16; the 16×32 comparison has x=8, between columns 7 and 8.
- **Hair is separate.** Hairstyles, bangs, parts and uneven hair volume may be asymmetric. Keep the underlying skull construction symmetric; do not let hair asymmetry silently distort the cranium or eye placement. Hair follows the supplied character design and its recorded construction; it need not fill a reference hat envelope.
- **Color is separate.** Lighting, shadows, highlights, fabric colors and decorative color patterns may be asymmetric. Do not RGB-mirror the whole character. Conversely, do not excuse different anatomical or sleeve/hand boundaries as mere shading; inspect the actual part masks and visible shape.
- **Explicit exceptions:** unusual/nonhuman designs such as Kaid may have documented asymmetric features (for example, a pitcher spout and handle), or the user may explicitly request another exception. Record the specific exempt feature; an unusual character does not automatically exempt every limb or eye.
- This bilateral idle rule applies to front/back rest poses. It does not force profile views, walking strides, running or expressive action poses to be symmetric. Those still follow measured reference construction and pose-specific checks.

Author or annotate separate anatomical masks for skull/face, eyes, torso, arms, hands and legs/feet. Validate each reflected pair, its bounds/attachments and occupied area, independently of RGB shading and hair. Where a hat or garment hides anatomy, label the hidden construction as a symmetric Critz scaffold, not a measured Emerald bone shape. Inspect the visible result as well as the automated mask comparison.

### Character review grid — required presentation

**User correction: Y increases upward.** Display **0 at the bottom and 64 at the top** of a standard 32×64 grid, with major horizontal lines labeled 0/10/20/30/40/50/60 and the top boundary 64. X increases left to right, with the vertical symmetry line at x=16. Preserve all 64 rows of available space in each requested review panel. Changing labels does not flip the artwork.

Native PNG/source indices still run from top row 0 downward. Convert an edge at native row `r` to displayed height `Y = 64 - r`; cell row `r` occupies heights `[63-r, 64-r]`. Label coordinate systems explicitly in measurements. Earlier review references to “row 36” use top-down native coordinates and therefore mean the face edge at displayed Y=28, not a 36px skull height. The user explained that the earlier 36 estimate came from counting upward on a downward-labeled grid; **do not impose 36px as a required skull or figure height**.

Present every new character in its **Emerald 2× native budget** with a countable grid: **one square equals one native pixel**, even when enlarged. Always show a distinct **vertical symmetry line through the horizontal midpoint** (x=16 for a standard 32×64 human frame). Draw and number **horizontal major guides every 10 pixels up the Y axis**, with frame boundaries labeled too. Keep the ordinary one-pixel cell lines visible and clearly distinguish the centerline from the ten-row guides. Use integer enlargement and report the native frame, painted bounds and display scale. Blank padding is not anatomy.

For **boy Hero**, the earlier 1×/2× paired comparison remains available on request; the latest explicit review request controls the layout. The current revision requests five full grids: Brendan first, followed by the four 2× candidates. Other characters normally need only the 2× presentation unless a comparison is requested. Include a part/silhouette proof when checking symmetry. Grids are review overlays, never baked into the native character PNG. Present idle revisions first; this rule does not authorize animation or game integration.

### Lessons from prior rejected revisions (history, subject to the current correction)

#### Human ear/face correction and review priority — revision 4

The user rejected the previous Hero as elf-like and supplied four human-boy concepts. Human Hero ears must be small, blunt lobes close to the head; do not stretch or taper them sideways to satisfy an overall bounding width. Preserve a full, rounded cheek/jaw mass. The anatomy includes mirrored ears; hairstyle volume and costume shading remain independent. Measure candidate deviations explicitly instead of compensating for smaller hair with oversized ears. Revision 4’s narrower face/ear shapes are proposed adaptations to those concepts, not approval of a changed global proportion standard.

When the user explicitly requests multiple 2× candidates, that request determines the current comparison layout: revision 4 presents four 2× idles, without an added 1× panel. **Lead the delivery with the requested gridded artwork**, not a clean-only sheet with the grid hidden behind a link. Every candidate still requires one native pixel per cell, the x=16 symmetry line and numbered ten-row Y guides. A clean view can supplement that presentation. Technical symmetry/bounds checks never substitute for whether the character visibly matches the user’s reference.

#### Aligned-reference diagnosis — revision 5 (incomplete; corrected by revision 7)

The user requested their refined Brendan screenshot beside all four unchanged R4 Heroes. The comparison reveals that equal frame/painted height and mirrored anatomy do not ensure the same proportions or character read. In the supplied reference, the continuous central exposed face begins at row 36; A/B/D begin around rows 30–31 while retaining eyes at rows 38–41. This changed the face, but treating it as automatically wrong was an incomplete diagnosis: Brendan’s hat hides forehead that a bare head exposes. Do not copy its occlusion boundary as a mandatory hairline. C’s locks partly cover the underlying scaffold. A pointed hat peak and a broad afro/flat-top cannot be equated solely by their topmost pixel; compare occupied row widths and distinguish hat, hair, exposed face and hidden skull.

Before the next correction, compare the exposed hairline-to-eye and eye-to-chin distances, face width profile, neck overlap, shoulder/arm attachment, torso width profile and dark separation between body parts. The prior broad shirt rectangles and weak arm/torso separation flatten the image. Preserve the reference’s structural readability without changing Hero’s identity/skin tone. This is a diagnosis of the supplied comparison, not new ROM-source measurement or approval of a revised anatomy standard. Keep all reference-colored review images outside the shipped build; screenshot interpolation is not additional native colors.

### Asset integration boundary

Keep appearance separate from collision, interaction, warp and gameplay data. Ship original reusable PNG assets with stable IDs and metadata; do not ship reference-game sprites or reference-colored comparison plates. Reference-only files remain outside the repository because the build copies documentation. Keep art workflow details here rather than duplicating them in AGENTS.md.

### What the extra pixels are for

Each reference pixel occupies a 2×2 area in the structural comparison. Start comparison guides with exact nearest-neighbor doubling. Final original assets may subdivide those blocks into finer **1px target-grid** clusters for cleaner linework, texture, expressive faces and material detail while retaining the measured envelopes and landmarks. Literal upscaling alone adds no detail; a freely redesigned 32×64 figure also does not satisfy this contract.

Aim for the user's richer texture and cleaner linework within Emerald's restrained contrast, palette relationships and readable shapes. Detail must survive inspection at intended screen size. Avoid noise, pillow shading, antialiasing, blur, fractional pixel placement or mixed asset densities. A reference 1px outline initially occupies 2 target pixels; selective 1px refinements must not change silhouette mass or make the whole character look thin. Do not silently turn the 4× pixel count into a 4× color budget.

### Target-grid contours, outlines and depth — revision-3 correction

**User-confirmed correction, 2026-10-03:** Emerald 2× means authoring with individual target pixels. Preserve measured dimensions, proportions, landmarks, anchor and pose; do **not** freeze the final silhouette to an exact nearest-neighbor doubling of every occupied source pixel. The source's 2×2 blocks are a comparison scaffold. Redraw stair-step corners, curves, diagonals, overlap boundaries and material edges at **one target pixel** where it improves the form. Add/remove individual opaque edge pixels within the measured envelope and mirror corresponding anatomical changes in front/back idle. Document meaningful envelope/landmark deviations instead of disguising them as refinement.

The rejected M1.C4 revision 2 illustrates the failure: its high-resolution mask and part labels were duplicated from the low-resolution source, and its pixel-edit helper prohibited editing empty cells. It therefore had **zero partially occupied 2×2 silhouette blocks**. A few internal color changes did not correct its doubled corners or heavy bands. The validation of exact doubled row occupancy reinforced the error. Future checks must preserve the measured envelopes, landmarks and paired anatomical masks **without requiring the old block pattern**. Mixed-block counts can diagnose a locked enlargement; they are not a beauty score or a required texture quota.

**Selective outline treatment:** study the selected native reference, then use dark colors appropriate to the material and lighting. In the inspected Brendan south-idle frame, the four-neighbor exterior boundary contains black, dark blue, blue-violet and brown; it is not one uniform black stroke. This is evidence for that frame, not a universal claim about every Emerald sprite or Game Freak's drawing process. Keep strong dark accents at useful overlaps and contacts (under the hair, between arm and torso, under feet). Use lighter/colored edge pixels on lit faces or materials where readable. At 2×, mix deliberate 1px contour refinements with stronger 2px shadow/overlap clusters where warranted. Neither a uniformly doubled dark border nor globally thinning every outline to one pixel is the standard.

**Depth through clustered shading:** establish a consistent light direction for the asset; make highlights, midtones and shadows describe rounded skull/cheeks, sleeve volume, hair masses, cloth turns and shoes. Use short material-specific hue/value ramps and connected clusters. Separate a cast/contact shadow from the object's outline. Avoid broad rectangular color patches that ignore form, long accidental nose stripes, randomly scattered bright pixels and texture added solely to appear more detailed. Symmetry constrains anatomy; it does not require symmetric light and shadow. Remain within the declared palette and native opaque pixels—no blur, antialiasing, interpolated gradients or fractional coordinates.

Review at native size and an exact enlargement **both with and without the grid**. Keep the required centerline/ten-row grid, but add a clean view when evaluating edge weight, material contrast and volume. Inspect a before/after when fixing a style error. Technical checks must not be described as proof of visual success; final acceptance is the user's. See [revision-3 diagnosis and evidence](reviews/M1-C4/revision-3/README.md).

### Animation fidelity

Map each authorized Critz key pose to a named reference pose and measure limb travel, foot contacts, arm opposition, body bob, head stability and accessory motion. Double spatial offsets, preserve timing and phase continuity. Do not animate disconnected feet beneath a static invented body or reset the gait every tile. Author both profiles for asymmetric designs.

The existing source-derived baseline remains walk `stride A → idle/passing → stride B → idle/passing`, holds `8/8/8/8` ticks, and run holds `5/3/5/3`, at `280896/16777216` seconds per tick. Scaling changes walk displacement from 1 to 2 rendered pixels/tick and run from 2 to 4; a 32px cell still takes 16 walk ticks or 8 run ticks. These are source-derived targets, not a claim of emulator-observed equivalence. Finer spatial resolution alone does not add animation frames or temporal smoothness. When smoother animation is in scope, add measured in-between poses within the same cycle duration and preserve key-pose/contact timing; present the refinement beside the reference-cadence version for user review.

### Required evidence and acceptance

For the currently authorized sample, deliver a measured overlay/comparison at matched apparent scale (reference 2× beside Critz 1×), native 480×320 room context when environment/framing is in scope, enlarged nearest-neighbor sheets, and synchronized loops plus frame stepping when animation is in scope. Include a table of targets/actual values/deviations, original asset IDs, source/PNG hashes and unresolved measurements. Keep reference imagery separate from production atlases and build output.

Check PNG dimensions, binary alpha, palette counts, opaque bounds, landmarks, anchors, pose continuity, tile seams and exact enlargement. Inspect actual pixels as well as automated results. Do not declare compliance from dimensions or bounding boxes alone. No unmeasured “close enough” substitutions: document the gap and resolve it before calling that requirement complete. The user retains visual/feel approval; documentation acceptance approves the specification only.

For a future renderer migration, keep appearance units separate from gameplay cells, collision, interactions, warps and v1 save coordinates. Re-evaluate phone presentation explicitly: 480px cannot fit a 320px-wide screen at 1×. Present and test any nearest-neighbor downsampling or orientation/layout solution with its detail-loss tradeoff; never silently crop, blur or stretch. This documentation task changes no runtime or saves.

---

## Historical art direction and implementation records

The following specifications predate the authoritative 2× contract. Read conflicting dimensions and construction rules as history, not current authoring instructions.

**M1.C3 animation extension:** The user now requests walking cycles and GIFs for every current M1.C2 design. The [walking extension](CHARACTER_FRAMEWORK.md#m1c3-walking-extension) retains the 20×26 painted ceiling, compact anatomy, exact front-idle art and four explicit directions. This supersedes still-only scope for animation review; finished artwork remains awaiting user acceptance.

**M1.C2 current character direction:** The user selected a 20×26 maximum visible budget and requested a new compact chibi framework, distinct body types and one still frame per character. [CHARACTER_FRAMEWORK.md](CHARACTER_FRAMEWORK.md) now governs this still-character design pass, superseding the earlier 16×32 character-production proposal for these new assets. Storage remains 24×32 with explicit anchors; the map grid stays 16×16. Final artwork acceptance is pending; budget selection alone does not approve the drawings.

**2026-09-27 scope amendment:** The user explicitly authorized M1.I2 to complete the existing roster/environment art, directional walk/run sheets, playable integration and tile movement together without intermediate art approvals. Earlier staged restrictions below are historical and superseded for this deliverable. Technical/visual proposals remain provisional; final user acceptance is pending. The [playable-review record](reviews/M1-I2/README.md) documents actual asset extents, native rendering, limitations and checks. No world expansion is authorized.

M1 environment review edition, 2026-09-25. **No example artwork, character proportions, palette swatches or motion proof has user approval yet.** “Approved direction” below means the user's supplied technical brief, not a finished art asset. [REFERENCE_MEASUREMENTS.md](REFERENCE_MEASUREMENTS.md) separates measured evidence from proposals. [GAME_VISION.md](GAME_VISION.md) remains canon.

## Approved direction

- Exploration is rendered first into a **240×160 native raster (3:2)**. Construct artwork from **8×8 base tiles** and **16×16 map metatiles**. Final world/sprite/camera positions align to integer native pixels; nearest-neighbor presentation, no bilinear resampling.
- Overhead three-quarter orthographic tile conventions: roofs, building fronts and furniture tops are visible together; ground-plane contact is consistent. This is an authored drawing convention, not a numerical camera angle or a perspective-projected 3D scene.
- Original Critz characters, environments, tiles and interface. Emerald is a measurement/reference source, not a source of shipped artwork or copied characters.
- Hero is a ten-year-old Black child; Hero and opposite-gender rival are player-named. Kaid and rival are children; Mom and Professor Nugget adults. Kaid remains an original whimsical pitcher child. Do not make adults twice the frame size.
- Controller stays **outside** the 240×160 exploration image. Preserve keyboard and touch access and readable menus.

## Presentation proposal — validate in M2 and M6

Default to the largest integer CSS scale fitting the space reserved for the world after HUD/controller layout: `floor(min(availableWidth/240, availableHeight/160))`, minimum 1 when it fits. Center/letterbox unused space; keep browser zoom/device-pixel-ratio in QA because integer CSS scale does not guarantee integer physical pixels on every screen. For example, a 320px-wide phone fits 240px at 1×, leaving lateral space; 2× requires 480px. Never stretch x/y independently or move controls onto the image to fill the phone.

If portrait readability makes 1× too small, offer a documented optional nearest-neighbor fractional presentation (e.g. 1.25× = 300×200). It preserves hard edges but produces uneven physical pixel widths and loses a perfect uniform pixel grid. This is a **proposed tradeoff requiring review**, not the approved default. If the available space is under 240×160, present a documented orientation/layout fallback; do not silently crop or downsample the game. DOM menu text/touch targets can use display-scale sizing independent of native exploration artwork.

## Character production specification — proposed for Critz

All values in this section are **proposed for Critz**, not user-approved or claimed Emerald anatomy. Reference frame/bounds tables live in the measurement ledger; exact Emerald head/eye segmentation remains unresolved.

| Character | Frame | Visible front idle W×H | Head silhouette / body guide | Eye rows (zero-based frame) |
| --- | --- | --- | --- | --- |
| Boy Hero | 16×32 | 14×20 | 12px / 8px | 19–20 |
| Girl Hero | 16×32 | 14×20 | 12px / 8px | 19–20 |
| Boy rival | 16×32 | 14×20 | 12px / 8px | 19–20 |
| Girl rival | 16×32 | 14×20 | 12px / 8px | 19–20 |
| Kaid | 16×32 | 14–16×19–20 including handle | 11–12px vessel/face + ~8px short body/legs; exact split unresolved | 19–20, face placement to review |
| Mom | 16×32 | 14–16×21 | 11px / 10px | 18–19 |
| Professor Nugget | 16×32 | 16×21 | 11px / 10px | 18–19 |

The guides describe silhouette regions rather than anatomical cuts through hair/clothes. Adults read through posture, torso/shoulders and clothing, with only a small height difference. Show Hero's dark skin ramp clearly in light and shadow; highlights must not erase identity. Kaid uses a small rounded vessel, expressive face, short limbs and distinctive spout/handle, with the teal glass/amber contents slice direction from the vision. Do not copy a branded mascot.

| Shared property | Proposed production rule |
| --- | --- |
| Frame origin | Top-left `(0,0)`; never independently trim frames. |
| Ground anchor | Frame edge coordinate `(8,32)`; frame extends 16px above its 16px ground cell. Anchor is not the final painted foot pixel. |
| Foot baseline | Idle last painted row 30 (edge below it y31); stride last row 31 (edge y32), matching observed source-asset vertical offsets. Foot guide and anchor must both appear on review overlay. |
| Collision footprint | One 16×16 ground cell and explicit current/destination reservation during a step; not the 16×32 image rectangle or silhouette. Final behavior validated in M2. |
| Directional poses | Four logical directions × idle plus two alternating stride poses. Store 12 images where needed; allow mirrored east only for genuinely symmetric art. Kaid handle/spout needs explicit east/west inspection. |
| Run poses | Separate four-direction run set where silhouette demands it; cadence from reference ledger. Do not generate the full run sheet in M1. |
| Gait metadata | Integer update holds and phase continuity; no generic “12 FPS” label. M1 static lineup only; M2 approves motion. |

## Environment scale — proposed for Critz

These are original composition targets to test, **not verified Emerald prop measurements**. Art extent may project above or beside the ground footprint; both must be explicit.

| Element | Draft artwork extent | Ground/collision and interaction |
| --- | --- | --- |
| Door | 16×32 | One-cell threshold; adjacent approach cell and explicit warp target/arrival direction. |
| Bed | 32×32 | 2×2 blocked cells; reachable side/foot interaction. |
| Chair | 16×16 or 16×24 | One-cell contact/occupancy; upper back can occlude. |
| Desk | 32×32 | 2×1 occupied ground cells plus upper projection; interaction at front. |
| Shelf | 32×32 | 2×1 occupied ground cells; upper shelving above contact line. |
| Fence | Modular 16×16 segments | One blocked cell per segment, explicit gate opening. |
| Tree | 32×48 | 1×1 or 2×1 trunk footprint per asset; canopy foreground separate. |
| Compact house | Initial 96×80 silhouette | Grid-composed roof/front; explicit building footprint and one-cell entrance. Not a size rule for every building. |
| Starter tank fixture | 32×32 | 2×1 supporting cabinet/contact footprint; reachable front interaction, identified as 25 gallons in UI. Artwork alone is not a gallon measurement. |

The user authorized M1.E1 environment review artwork on 2026-09-25, including original indoor/outdoor pieces and proposed Rootport, forest-route and Liarsville views. This is a review-only scope extension; it does not authorize gameplay expansion or approve G1/G2. Revision 1 was rejected for missing the intended Emerald style; revision 2 returns to a small house/tree proof before more map work. Leave floor and wall areas visually quiet enough that silhouettes, doors and interactions remain readable.

## Palette, outlines and light — proposals for G1

Emerald's 4bpp art uses multiple 16-entry palette banks; **the whole game is not limited to sixteen colors**. Background and object memory are separate; map tileset allocation is not a global character/UI budget. See reference sources for bank counts.

For Critz, propose named reusable families: warm wood/plaster interiors; leaf green ground/canopy ramps; cool teal water/glass; terracotta roofs; warm brown skin ramps; distinct clothing accents; dark blue-green UI ink and warm light text. Start with at most 15 opaque colors plus transparency per character palette, and multiple explicit 16-entry environment banks where needed. These are practical discipline targets, not a claim the browser emulates every GBA hardware limit. Exact RGB swatches await M1 and must be stored in editable palette files.

Use selective dark colored 1px silhouette outlines; reserve darkest values for faces/contact edges. Light comes from upper-left on the image plane as a **Critz proposal**; keep roof/top surfaces lighter, building fronts quieter, and short ground/contact shadows consistent. Use 2–4 deliberately chosen tones per material, hue-shifted shadows, clustered pixels rather than gradients. No antialiased ellipses, translucent blur, painterly noise or per-frame subpixel shading in exploration assets. Sparse texture in floors/grass; stronger contrast on actor edges, doors and key objects. Confirm exact ramps, texture density and outline breaks together in the bedroom sample, not through text approval alone.

## Draw order, collision and interactions

Proposed rendering order: ground and floor detail → anchored objects/characters sorted by ground-contact y with stable tie-breaker → explicit foreground/canopy/roof segments → native effects/interface. Split tall objects where necessary; an entire tree/building must not always draw behind every actor as it does in the prototype. Each sortable asset records a `sortAnchor`; each foreground tile records its intended cover behavior. No collision is inferred from alpha pixels.

Map collision, warp, interaction and spawn data remain distinct from appearances. Door opening/closing state chooses art without changing quest rules. Interaction metadata records reachable cells, facing requirements if adopted, action ID and prompt; keep generous touch interaction while preserving all current actions. Reference tile/elevation rules guide M2; any simplified Critz footprint is labeled as a choice.

## Reusable asset and map workflow — technical proposal

Use **Tiled finite orthogonal maps with JSON export**, a 16×16 placement grid, and PNG tilesets assembled from editable 8×8 source tiles. Tiled supplies tile/object layers and custom properties, so this avoids building a custom editor. Keep source `.tmx`/`.tsx` and exported JSON together; finalize a small supported subset and version in M3. See the official [layer guide](https://doc.mapeditor.org/en/stable/manual/layers/) and [JSON format](https://doc.mapeditor.org/en/stable/reference/json-map-format/), consulted 2026-09-24 (displayed version 1.12.2).

Proposed layers: `ground`, `detail`, `foreground` for appearance; `collision`, `interactions`, `warps`, `spawns`, `actors` for nonvisual data/placements. Sortable prop objects reference stable artwork IDs. Named actions dispatch into existing game logic; map files contain no story scripts/economy formulas. Treat map object coordinates as native pixels at export boundaries, map gameplay cells as explicitly converted units. Preserve existing scene and map-local entity IDs; use `<sceneId>:<entityId>` for globally unique lookup. Never persist Tiled GIDs as gameplay identity; resolve GIDs through export metadata into stable asset IDs.

Proposed paths/IDs (not files promised as implemented):

- `assets/characters/hero-boy.png`, ID `char.hero.boy`; analogues for girl, rival variants, Kaid, Mom, Nugget.
- `assets/tilesets/home.png`, ID `tiles.home.v1`; shared environmental bank plus area-specific additions in later milestones.
- `assets/metadata/characters.json` and tileset metadata: schemaVersion, assetId, PNG path, paletteId, frame dimensions/rectangles, origin, ground/sort anchor, opaque bbox, logical direction, mirrored flag, animation sequences/holds, source path and approval revision.
- `maps/home/bedroom.tmx` + exported map JSON with stable scene ID `bedroom`; sprite/collision/interaction metadata never hidden in renderer switch statements.
- `art/source/` for `.aseprite`/`.ora`, editable indexed PNG/palette data, or deterministic authoring sources plus manual correction layers. A procedural generator may author art; approved PNG outputs remain checked-in and inspectable.
- `docs/reviews/M1/` for `lineup-native.png`, `lineup-4x.png`, `bedroom-native.png` (240×160), `bedroom-4x.png` (960×640), guides and review notes. Export actual assets separately from labeled review sheets.

Export PNG at 1× with hard pixels and binary transparency for exploration sprites. Keep source palette/index data where practical, no JPEG, no blurred resizing, no outlines baked into blank margins. A 4× export must map every native pixel to exactly 4×4 identical pixels. Metadata must survive atlas reorder; validators in M3 check bounds/IDs/anchors/references. Build currently copies only HTML/CSS/src/icon, so M3 must explicitly add asset/map export paths and server MIME types.

## Interface standard and approval registry

Preserve accessible DOM menus/control semantics while native borders/icons/fonts are evaluated in M6. Never shrink touch hit areas to sprite dimensions. Primary touch targets proposed at ≥44 CSS px; preserve scroll and keyboard focus, player-entered names and live causal tank data. Manage/Stats/View remain the first tank choices. Whether dialogue/menu text is native bitmap or display-scale DOM is unresolved pending readability review.

Approved example images: **none**. Existing `docs/screenshots/` and M0 test captures document the prototype only. Proposed standards become approved only with the user's G1/G2 response recorded alongside exact artifact revision/hash. M1 will present seven original characters (front and side, both sides for Kaid) together plus one bedroom at native and 4×; it will not finalize the remaining roster.

Recovered character proposals: the separate art task delivered ten shared Hero/rival candidates B1–B5/G1–G5, one south-idle pose each. They are now in `assets/review/characters-v1/`, with editable indexed rows/palettes in `art/source/characters-v1/`. The combined [M1.I1 atlas](../assets/review/integration-v1/atlas.png) contains those ten and environment revision 2, using [stable IDs](../assets/review/integration-v1/atlas.json). It is a lossless review package, not a complete production sheet. No directional/animated character or revised indoor assets are implied. Inspect them together at [the static assembly review](../art-review/integration.html).


## Environment construction research and the rejected first draft — 2026-09-25

Read the [pinned environment research](reference-data/EMERALD_ENVIRONMENT_RESEARCH.md) for source links, assembly measurements and limits. Emerald uses shared primary and area-specific secondary tilesets, reusable 8×8 references inside 16×16 metatiles, and explicit layering. Selected measured examples are a **32×32 tree assembly** and **80×80 house assembly**; these are not universal silhouette dimensions. The earlier 32×48 tree and 96×80 house remain Critz proposals. Original Game Freak drawing software, brush/layer workflow and art review process were not verified; the decompilation's modern file organization does not establish those historical facts. No emulator observations were made.

The first Critz environment draft passed elementary grid constraints but the user rejected its visual style: “What I see you making does not look like Pokémon emerald.” Treat **all revision-1 environment PNGs/maps as rejected review history**. Technical validity is not visual approval. Do not integrate them, call them accepted, or use them as a new style reference.

### Revised drawing guidance — proposed, awaiting review

- **Draw volume before texture.** Roofs should show distinct planes, narrow side returns and layered eaves above a short front wall. Avoid a flat rectangle with a brick pattern and a front-facing triangular porch pasted onto it. Not every building needs the same silhouette.
- **Use material-specific pixel clusters.** Roof highlights describe the direction and overlap of tiles. Avoid a uniform decorative dash pattern. Windows need a simple cyan glass ramp and structural framing; walls should be calmer than roof edges.
- **Separate warm/cool material families.** Explore warm ochre/terracotta roof surfaces against pale cream plaster, cool gray-violet structural shadows and cyan window glass. Ground can be lighter mint green than deep foliage. These color relationships are observations/proposals, not a copied reference palette or exact final RGB specification.
- **Trees are compact foliage masses.** Prefer a 32×32 specimen for the next comparison, with jagged interlocking leaf clusters, bright yellow-green upper planes, dark connected lower canopy, and a mostly concealed trunk. Avoid smooth pear silhouettes, isolated circular highlight spots, long lollipop trunks and detached oval shadows. Taller variants remain possible after the small reference-scale specimen works.
- **Judge at native size.** A 240×160 proof and exact nearest-neighbor enlargement must both be shown. Generative mood studies may guide a direction but cannot establish native dimensions, palette membership or tile reusability. Exported native proofs require independent pixel checks.
- **Keep originality explicit.** Source assemblies can be studied outside the repository. New Critz palettes, pixels and assemblies must be authored separately; never ship source-game sprites. The checked-in generators read no reference artwork.
- **Build connected compositions.** Keep paths clear of border trees, bridge the full stream width, connect each doorstep to a lane, and leave room below south-facing doors. These static layout checks do not prove collision or movement.

Current review: [M1.E1 packet](reviews/M1-E1/README.md), [revision-2 native proof](../assets/review/environment-v2/house-tree-native.png), [exact 4× proof](reviews/M1-E1/revision-2/house-tree-4x.png). The revised proof is **awaiting user feedback**, not an accepted art example. Indoor furniture, all town maps and the production tileset must be revised after the direction is settled. The planned Hero/Mom scale test and G1/G2 gates remain outstanding.

## M1.C1 character-budget comparison (2026-09-27)

The user likes the supporting-character concept designs and requested animated 16×32 versus 24×32 samples. [The comparison](reviews/M1-C1/README.md) uses Mom, Kaid and Nugget at equal pixel zoom with the same 16px tile movement. This is a proposed character-only budget comparison, not a change to the 240×160 viewport, map grid, or approved production standard. Final budget and native-sheet acceptance await the user.
