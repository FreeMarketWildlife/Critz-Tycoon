# Emerald environment construction research

Research for the original Critz environment review, 2026-09-24. **Reference evidence and proposed production rules; no Critz artwork is approved by this document.** Read alongside [ART_BIBLE.md](../ART_BIBLE.md) and [REFERENCE_MEASUREMENTS.md](../REFERENCE_MEASUREMENTS.md).

All repository evidence is pinned to pret/pokeemerald **`5eff78649e7170a877b961ef0b3da13b81a16038`**. The local reference checkout returned that SHA and a clean Git status. Searches for original production accounts were also made, but no accessible first-party account establishing Emerald's environment artists' exact drawing software, brush process, layer files, or review workflow was verified. Do not fill those gaps with modern ROM-hacking tutorials. The decompilation exposes shipped data and reconstructed runtime behavior; its current PNG, JASC palette and C organization is **not evidence that Game Freak authored assets in those formats or with those tools**.

## 1. What the shipped construction actually supports

**Reference verified.** A background base tile is 8×8. Each 16×16 metatile references eight base tiles: four for a lower 2×2 image and four for an upper 2×2 image. Tile references also carry palette selection and flipping. This makes a large object an assembly of small reusable pieces, rather than requiring one unique large bitmap. The renderer's three layer types route these two authored layers to different pairs of hardware backgrounds; the NORMAL upper layer explicitly covers object sprites. This is not a universal instruction to draw every tree behind or in front of every actor. [Renderer](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_camera.c#L225-L310), [attributes and layer enum](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/global.fieldmap.h#L34-L54).

**Reference verified.** Layouts pair a primary tileset with a secondary one. Littleroot and Oldale share `General` + `Petalburg`, as do Routes 101–103; the protagonist's bedroom uses `Building` + `BrendansMaysHouse`. Shared landscape or furniture vocabulary therefore coexists with a local architectural/interior kit. `Tileset` stores graphics, palettes, metatiles, attributes and an animation callback separately. [Outdoor layouts](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/layouts.json#L94-L194), [house layouts](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/layouts.json#L534-L573), [structure](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/global.fieldmap.h#L65-L75).

**Reference verified.** The allocation constants allow 512 primary / 1,024 combined base tiles, 512 primary / 1,024 combined metatiles, and 6 primary / 13 combined map palette banks. A bank contains 16 entries. The loader places the primary map banks at 0–5 and secondary banks at 6–12. This is a map allocation, not a sixteen-color limit for the whole game or a browser requirement. Do not assume every slot in every source atlas is loaded or used. For example, Petalburg's indexed PNG is 128×80 (160 physical 8×8 cells), but its graphics declaration requests 159 tiles. [Constants](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/fieldmap.h#L4-L12), [palette loading](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/fieldmap.c#L831-L879), [graphics declaration](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/tilesets/graphics.h#L1-L22).

**Reference verified.** Each map word encodes a 10-bit metatile ID, 2 collision bits, and 4 elevation bits. Metatile attributes carry behavior and layer type separately. Appearance alone does not define collision, traversal, interaction or warps. [Map and attribute masks](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/global.fieldmap.h#L4-L54).

## 2. Selected assemblies, measured from source data

Coordinates below are zero-based map cells; ranges are inclusive. Dimensions measure **reserved assembly cells**, not alpha-bounded silhouettes or collision footprints. Source PNG index zero is treated as transparent while composing upper/lower layers. Static reconstructions were visually inspected; they are not emulator screenshots.

| Selected source example | Verified allocation | Evidence and limits |
| --- | --- | --- |
| Littleroot whole layout | 20×20 cells = 320×320 px | Layout JSON and 800-byte map data. Not viewport size. |
| Common forest tree at Littleroot x0–1, y0–1 | 2×2 cells = 32×32 px | Metatile IDs `[[0x1D4,0x1D5],[0x1DC,0x1DD]]`. Includes ground at corners; not a universal size for all trees. |
| Left Littleroot house at x2–6, y4–8 | 5×5 cells = 80×80 px | Full roof and front assembly. No chimney or ground approach included. |
| Same house's roof center | Three repeated cells per row | IDs `0x209`, `0x211`, `0x219` each occur three times across their respective rows, with separate left/right end caps. |
| Protagonist bedroom | 9×8 cells = 144×128 px | Interior layout size; distinct from exterior house allocation. |
| Bedroom blue rug at x4–7, y3–6 | 4×4 cells = 64×64 px | Edge/corner/middle assembly; visible rug border falls inside the allocation. |
| Bedroom bed neighborhood x0–2, y3–5 | Nine dedicated metatiles | IDs `0x27B–0x27D`, `0x283–0x285`, `0x28B–0x28D`. Includes surrounding floor; **not** a 48×48 bed silhouette claim. |
| Standard animated exterior doorway | 1×2 cells = 16×32 px redraw | Door code redraws `(x,y−1)` and `(x,y)`; wide variant redraws another column. Does not establish warp footprint or full entry duration. |

Sources: [Littleroot binary map](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/LittlerootTown/map.bin), [bedroom binary map](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/LittlerootTown_BrendansHouse_2F/map.bin), [General metatiles](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/tilesets/primary/general/metatiles.bin), [Petalburg metatiles](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/tilesets/secondary/petalburg/metatiles.bin), [bedroom tileset](https://github.com/pret/pokeemerald/tree/5eff78649e7170a877b961ef0b3da13b81a16038/data/tilesets/secondary/brendans_mays_house), [door assembly](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_door.c#L282-L361).

The selected house expands to **200 base-tile references but only 39 unique base-tile IDs**. Its descriptors use palette banks 0, 2, 6, 9 and 10. The tree expands to **32 references and 17 unique IDs**, with palette banks 0 and 2 and two flipped references. These counts include blank/ground references and both layers; they are not counts of visibly painted colors or unique decorative details. They demonstrate actual assembly reuse without prescribing an identical Critz house.

The art bible's 96×80 compact house and 32×48 tree are therefore still **Critz proposals**, not measurements of these Emerald examples. The exact painted bounds of the reference bed, chair, desk, shelf and door are not segmented by this study. U002 is partly narrowed, not universally resolved.

## 3. Terrain, readable depth and animation

**Reference verified.** `DrawMetatileAt` selects the stored metatile ID and expands its tile references; it does not calculate terrain adjacency or generate edge pixels. The named General variants distinguish grass beside trees, tall grass beside trees, water, and other terrain. Reusable edge artwork must already exist in the chosen assembly. [Metatile selection](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_camera.c#L225-L243), [named variants](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/constants/metatile_labels.h#L207-L245).

**Visual interpretation, not artist testimony.** The inspected house shows roof planes and its front at the same time, without converging perspective. A darker eave separates the roof from the wall. Repeating roof centers establish rhythm; end pieces finish the silhouette. Tree foliage forms contiguous leaf clusters above darker bases. Interior furniture exposes a top and a short front. Large quiet rug/floor areas provide space around objects. These observations support the bible's three-quarter orthographic convention; they do not establish a numeric camera angle, exact light vector, or universal outline thickness.

**Reference verified, source timing only.** General water has eight source frames. Flower playback is `0 → 1 → 0 → 2`. Sand/water edge uses seven unique frames in eight sequence positions; land/water edge and waterfall each have four positions. General queues each family once per 16 animation updates, staggered at offsets 0–4. It replaces particular 8×8 tile ranges, so repeated instances sharing those references animate together. Building television updates every eight animation updates. The source does not support a rule that every tree or every tile must move. Runtime appearance, initial displayed phase, pauses and final cadence still require capture verification. [Frame tables](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/tileset_anims.c#L77-L150), [counter and queue behavior](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/tileset_anims.c#L564-L679).

## 4. Proposed Critz rules derived from this evidence

These are original design decisions for review, not claims about Game Freak's production process.

- Build a shared landscape kit and a shared interior kit; add small Rootport/Liarsville accent families. Reuse structural pieces across towns while changing roof color, sign, porch, planting and silhouette accents.
- Author roof ridge, eave, left/right ends, repeatable middle, wall, window and one-cell door modules. Check every house at native size beside a child character before accepting its scale.
- Keep a compact 32×32 tree option and the proposed 32×48 specimen. Provide separate canopy/foreground and trunk/contact metadata. Canopy overlap may cover an actor without turning the entire visible canopy into blocked ground.
- Supply terrain centers, four edges, outer corners and inner corners, then test narrow paths, turns, islands and shore junctions. For fences/hedges, include ends, corners and deliberate gaps. This topology checklist is a Critz choice; no claim is made that Emerald uses a modern autotile editor.
- Keep environment colors in named reusable banks/ramps. Share grass and wood ramps across regions; use town accent colors sparingly. Do not recolor every module independently or copy the reference palette wholesale.
- Keep floors, grass and walkable routes quieter than entrances, characters and useful objects. Use authored opaque pixel clusters, clean material boundaries and short contact shadows. Judge texture density on a 240×160 viewport, not only an enlarged atlas.
- If animation is added after static approval, start with a small water/shore/flower set and explicit update holds. Align loop seams, preserve collision and anchors, and avoid moving every canopy merely to demonstrate animation.
- Store stable asset IDs, native rectangles, palette IDs, origins, contact/sort anchors, collision/interaction references and review revision separately. A review map should expose where trees cover an actor and where a doorway can actually be approached.

## 5. Reproduction and limits

Use the pinned checkout and read little-endian 16-bit words from the cited binaries. For map width `w`, cell `(x,y)` uses word `y*w+x`; mask with `0x03FF` for the metatile ID. IDs below 512 select the primary table; otherwise select secondary ID minus 512. Read eight words at `id*8`. For each tile descriptor, bits 0–9 select the 8×8 base tile, bits 10/11 flip horizontally/vertically, and bits 12–15 select the bank. Composite four lower and four upper tiles at `(0,0)`, `(8,0)`, `(0,8)`, `(8,8)`. Palette indices are measured before conversion to RGB. Count distinct base IDs separately from descriptors.

Checksums of the measured binary inputs:

| Input | SHA-256 |
| --- | --- |
| Littleroot `map.bin` | `9bc2d52ac0f515a2af3a12483e3913aee3948531f91ca0547513f53ce92acf9d` |
| Bedroom `map.bin` | `112f73b62a84f4d870b45dc8c90918fc74851bf7643628cf70a229588a21b02c` |
| General `metatiles.bin` | `17974b0ba1bb9d105d5ba255c69a3b80d8484a26ea0b8ff22c6c6567c6c22910` |
| Petalburg `metatiles.bin` | `3f2e021f25bc0ed6130956d70de833e874191349bc761188dbb716f32d8d7bae` |

The temporary static reference renderer omits object events, scripts, weather, camera, palette fades, animation and dynamic tile replacement. Two chimney metatiles elsewhere in Littleroot reference lower-layer slots outside Petalburg's static loaded range; those were not used for the selected house measurement and do not establish runtime fidelity. No ROM was downloaded or run. No reference artwork is copied into this project's assets or playable build. Pixel art made for Critz must remain original; review concepts do not authorize gameplay integration or waive the visual/movement gates.
