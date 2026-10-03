# M1.C4 — Countable idle pixels and chibi construction

**Current review: [revision 9](revision-9/README.md).** Four native idles preserve the user's exact editor-template anatomy, add the requested hairstyles/outfits, and use one-pixel exterior outlines. Reopenable editor projects and PNG assets are supplied; animation and visual acceptance remain pending.

**Awaiting user art review.** The user requested a boy Hero idle comparison at 16×32 versus 32×64, then required a true one-native-pixel grid, numbered marks every ten pixels, and the compact construction of the supplied character reference. No animation or playable replacement is included.

- [Countable Hero comparison](hero-grid.png) · [vector version](hero-grid.svg)
- [Construction / skeleton comparison](hero-skeleton.png) · [vector version](hero-skeleton.svg)
- Native transparent PNGs: [16×32](hero-16x32.png), [32×64](hero-32x64.png)
- Editable indexed source: [16×32](hero-16x32.json), [32×64](hero-32x64.json)

Each small square represents exactly one native source pixel. The left frame is shown at 24×; the right at 12×. Both frames therefore occupy 384×768 display pixels. Numbered heavy lines mark native boundaries 0, 10, 20, etc., with the final edge also labeled. Transparent padding is deliberately visible. The figures occupy 14×21 and 28×42 painted bounds, respectively. A frame dimension is not a painted-body dimension.

## Construction copied from the reference

The supplied screenshot's coarse figure was inspected on its displayed 16-screen-pixel pitch, sampling cell centers from screen origin `(304,9)`. This is analysis of the user's screenshot, not a new measurement of Emerald source or emulator footage. The eight torso/arm/hip/foot occupancy rows are explicitly recorded and checked in [build.mjs](build.mjs). The smaller Hero uses that exact body construction mask. The larger version doubles the structural spacing, then refines native pixels.

The head region retains the reference's broad, dominant mass and compact face-to-body relationship. Original rounded afro construction replaces the reference's pointed hat. It is not a literal copy of the hat or the entire head outline. Thirteen head rows, five torso/arm rows, and three shorts/feet rows become 26, 10 and 6 rows. The construction plate separates those bands. No long shins, extra neck or stretched torso were added.

Hero remains a ten-year-old Black child with warm brown skin, rounded afro, teal raglan shirt, cream sleeves, navy shorts and cream sneakers. Original palette and indexed-pixel authoring format come from the existing Hero source. No reference-game colored sprites, screenshot, costume or palette are shipped. The larger source has 174 recorded native refinement operations; it is not a nearest-neighbor enlargement alone. Neither drawing is approved production art.

## Method and checks

This is an exact native-source revision, using the existing project raster authoring format. The prior generated concept is a style discussion aid, not a texture or a resized sprite source. No new image-generation prompt was used for this native pass.

Run `build.mjs` with Node and `CODEX_PRIMARY_RUNTIME_NODE_MODULES` pointing at a modules directory containing `sharp`. It exports native PNGs from indexed rows and draws grid artwork from the same source coordinates. Sharp rasterizes the vector review layout; it does not resample a concept illustration into sprites.

Independent decoded-PNG checks pass for all **2,560 frame cells**, including exact agreement between source colors, native PNGs and the centers of displayed grid squares. Both figures have binary alpha, one connected four-neighbor silhouette, correct bounds, and 12/13 opaque colors. Native authoring also checks the copied eight-row body mask. See [independent validation](independent-validation.json) and [source validation](validation.json). Both final plates were visually inspected. Technical checks do not approve the artwork.

## Scope, delivery and next action

Work is directly on `main`, based on `2d00b5b`, after a safe fast-forward brought in two ideas-only commits. The existing unfinished M1.I3 files were preserved and excluded from this task's commit. Only this review packet and its status/plan entries are delivered. Native files live in documentation and have no runtime consumers; the playable build, save data, audience and hosted game are unchanged. No website deployment is needed for this documentation/art-review packet.

The updated ideas notebook separately proposes a whole character inside 32×32. This comparison follows the user's specific 16×32/32×64 request; its 28×42 painted figure does **not** satisfy that separate one-tile proposal. Neither preference silently changes the game standard.

Next action: the user reviews the head/body/limb construction and requests still-pose changes. Continue refining this idle pose before walking animation. Commit/push and remote-SHA verification are recorded in the task handoff/status.
