# M1.ME1 — Map Studio

User-requested map authoring and playable art review. New extension art and editor test feel await the user's response; existing gameplay layouts are not replaced or self-approved. The secret-base idea is set aside per the user's correction.

Open [Map Studio](https://critz-tycoon.freemarketwildlife.chatgpt.site/map-editor/). It is also linked from Sprite Editor and the game's Studio & credits menu.

## Use it

- **Terrain:** select Grass, Dirt path, Concrete, Garden soil, Water or Mountain, then paint. Brush, Rectangle and Fill operate on semantic cells. Neighbor changes automatically rebuild their quarter-tile transitions. Fences join cardinal neighbors. Erase removes features, raw overrides, stamps and passages, preserving the ground.
- **Cliffs:** Mountain paints solid raised terrain. Cliff stairs and Cliff opening create explicitly walkable cells through it. Paint an entire connected stair lane to clear ground; an opening can have a Passage to another map. Directed ledges allow a two-cell hop only in their marked direction, with a clear landing. Water and its boundary cells are blocked; Bridge overrides water collision.
- **Stamps:** drag a whole building/object onto the map, or select it and tap. Move a stamp picks up the whole assembly, footprint and linked doorway. Buildings have a walkable rear row, solid walls and a clear door cell. Use Passage at that door cell to link an interior; a building does not invent a room or game shop logic. Planters and boulders remain objects; boulders are pushable in Test.
- **Tiles:** search all 942 existing world tiles and 861 new editor tiles. Exact overrides have an explicit collision checkbox. Terrain paint restores automatic selection. Ground, feature and override sources are baked into one cached metatile before drawing; the ground renderer does not stack fence/world sprites.
- **Maps:** use a source-derived preset or custom 8–128 cell dimensions. Up to 16 maps and 65,536 cells per project. Shrinking crops outside content; Undo restores it. Edge Connections pair maps with an alignment offset. Passage sets a directional entrance cell and explicit arrival coordinates; return passages are authored separately.
- **Copy for chat:** lossless compact versioned JSON with run-length terrain/features, stamp identities, coordinates, Hero starts, raw collision, notes, passages and connections. Paste it into chat for implementation. Open / paste accepts both compact chat data and downloaded JSON. Save project is a portable backup; Map PNG exports native pixels without guides.
- **Test with Hero:** arrows/WASD or touch D-pad; walls/shores/fences block, ledges jump, boulders push and map links travel. The selected living-collection Black child Hero uses existing source pixels. Test works on a disposable project copy. Closing it discards movement and object pushes. Editor movement is a preview approximation, not a new full M2 acceptance claim.
- **Navigation:** wheel/two-finger scroll pans; Ctrl/Command-wheel zooms around the pointer; Space-drag or Pan moves the map. Fit recenters. Keyboard arrows select cells and Enter applies the tool. Ctrl/Command-Z and Shift-Z undo/redo. All work autosaves separately to `critz.map-editor.v1`; a corrupt stored draft is retained rather than overwritten. Download backups, especially if storage is unavailable.

## Reference-verified Emerald facts

Inspected source at pret/pokeemerald **`5eff78649e7170a877b961ef0b3da13b81a16038`**. This is source/data analysis, not emulator/frame-capture observation. No Pokémon artwork ships.

| Example | Authored cells | Critz extent at 32px/cell |
| --- | --- | --- |
| Littleroot / Oldale / Route 101 | 20×20 | 640×640 |
| Route 102 | 50×20 | 1600×640 |
| Petalburg | 30×30 | 960×960 |
| Mauville / Fortree | 40×20 | 1280×640 |
| Slateport / Rustboro | 40×60 | 1280×1920 |
| Route 104 | 40×80 | 1280×2560 |
| Route 103 | 80×22 | 2560×704 |
| Bedroom | 9×8 | 288×256 |
| House first floor | 11×9 | 352×288 |

These are complete layout rectangles, including blocked scenery, not exclusively walkable space. There is no universal map-section size. Pixel dimensions double for Critz; cell counts stay the same. [Outdoor layouts](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/layouts.json#L4-L201), [house layouts](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/layouts/layouts.json#L534-L573).

Outdoor connections carry direction, target and offset; door warps carry entrance coordinates/elevation, target map and warp identity. Narrow passages come from authored blocking landscape, not an inherent connection restriction. [Littleroot connection and doors](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/data/maps/LittlerootTown/map.json), [connection runtime](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/fieldmap.c#L578-L630).

Map words separate metatile ID, collision and elevation; behavior and layer type are separate attributes. Direction-specific ledge behavior leads to a two-cell jump action. [Map format](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/include/global.fieldmap.h#L4-L54), [ledge direction lookup](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c#L7664-L7687), [jump action](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_player_avatar.c#L955-L959).

A reference 16×16 metatile has four 8×8 base tiles in each of two layers; renderer layer type determines sprite overlap. The reference runtime draws an already selected metatile. Automatic adjacency selection is our editor feature, not a claim about Game Freak's original software. [Renderer](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_camera.c#L226-L306).

## Critz decisions and limits

Original native editor extension is separate from the unchanged playable master. [Art direction](../../ART_BIBLE.md#map-authoring-review--m1me1) is authoritative. Five ranked materials over lower-ranked neighbors provide 15 pair banks × 47 shapes, plus 96 fence contacts, six feature sources and 54 feature contacts: **861 new inspectable cells**. Quarter-tile selection handles mixed material corners; assembled cells are cached. Exact existing pixels are reused for Hero, buildings, foliage and props. Source generator is `art/source/map-editor/build.py`; no arbitrary bitmap resampling authors the art.

The editor stores logical material, feature, exact override/collision, stamps and travel separately, with versioned compiler semantics. It does not emulate the ROM bit layout or implement a general elevation engine. Raised mountains are solid, and stairs/openings are explicit exceptions; a walkable summit can be authored as enclosed grass. Shore blocking is the user's requested rule. Building interiors and interactions must be linked/authored; no accepted-world replacement or story/economy migration happens automatically when importing. The complete sheets include variants that are useful only for expert raw painting; semantic tools remain the default.

Current playtest approximates walking at a 268ms cell step and 360ms jump with integer raster placement. It is for collision/layout review, not a source-exact emulator test or physical Safari verification. Finite map bounds render a quiet dark surround; edge connections switch maps rather than pre-rendering adjacent strips. Water/flowers use still source tiles in the editor. This does not alter their gameplay animation.

## Verification and release

The clean release passes **150 unit tests, 22 editor browser scenarios, 10 sprite-editor regressions, 17 adventure scenarios**, syntax checks and independent native art checks. [Editor report](browser-report.json) · [Sprite regressions](sprite-regression.json) · [Adventure regressions](adventure-regression.json) · [Native art check](art-check.json) · [Desktop](desktop.png) · [Phone editor](phone.png) · [Phone test](phone-test.png). Results and exact source/deployment state are recorded in [PROJECT_STATUS](../../PROJECT_STATUS.md). Browser tests use new isolated contexts and synthetic drafts/save sentinels only. The task leaves pre-existing character work untouched and excluded from the release. The original adventure save keys, progress, characters, story and accepted world layouts remain unchanged.
