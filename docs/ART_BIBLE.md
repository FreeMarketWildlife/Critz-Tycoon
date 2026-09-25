# Critz: Tycoon — initial art bible

M0 edition, 2026-09-24. **No example artwork, character proportions, palette swatches or motion proof has user approval yet.** “Approved direction” below means the user's supplied technical brief, not a finished art asset. [REFERENCE_MEASUREMENTS.md](REFERENCE_MEASUREMENTS.md) separates measured evidence from proposals. [GAME_VISION.md](GAME_VISION.md) remains canon.

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

M1 tests indoor scales only. Outdoor tree/fence/building dimensions await M2/M3 examples; do not expand to Rootport now. Leave floor and wall areas visually quiet enough that silhouettes, doors and interactions remain readable.

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
