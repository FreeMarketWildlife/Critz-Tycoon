# M1.E1 — environment artwork review

Latest state: **revision 2 awaiting user review**. Revision 1 was explicitly rejected for not looking like the intended Pokémon Emerald style. G1 and G2 remain unapproved. This packet is not a production tileset release or a playable world expansion.

## Review this first

- [Native 240×160 scene](../../../assets/review/environment-v2/house-tree-native.png)
- [Exact 960×640 / 4× scene](revision-2/house-tree-4x.png)
- [House enlargement](revision-2/house-4x.png) and [tree enlargement](revision-2/tree-8x.png)
- [13-piece draft atlas](../../../assets/review/environment-v2/atlas.png), [asset metadata](../../../assets/review/environment-v2/atlas.json), [separate geometry proposals](../../../assets/review/environment-v2/geometry-proposals.json)
- [Technical validation: 23/23 checks](revision-2/validation.json)
- [Local review page](../../../art-review/index.html); with the project server running, open `http://localhost:5173/art-review/`.

The small revision uses layered roof planes, a short facade, cool structural shadows, pale plaster, cyan windows and compact 32×32 foliage. These are proposed corrections, not a claim that visual matching is complete. The native scene was authored in [editable deterministic source](../../../art/source/environment-v2/build.mjs), using an integer [raster module](../../../art/source/environment-v1/raster.mjs). Source generation reads no reference images. The art is newly authored; no Emerald sprite PNG is shipped.

Reproduce from repository root with Node 20+: `node art/source/environment-v2/build.mjs`. No packages are required. Primitive parts and house assembly references are provided; hand-authored roof trim remains in the source. This is not the finalized M3 Tiled pipeline. Static geometry proposals have no production collision, warp or interaction behavior.

## Direction studies

[Revised generated style study](revision-2/style-study.png) used the built-in imagegen tool with the inspected, pinned Emerald source-map reconstruction as a **reference image**, not a shipped asset. [Exact revised prompt](../../../art/source/environment-v1/revision-2-prompt.txt). The generated study is visibly closer to the reference construction but has not passed a native-pixel grid or palette contract; it is not the reusable native tileset. The native proof above is a separate original construction, not a claim of lossless conversion from the generated illustration.

[Original three-location concept board](environment-concept-v1.png), also made with built-in imagegen, has a preserved [prompt](../../../art/source/environment-v1/concept-prompt.txt). It proposed warm Rootport, a short creek route, and plum-roofed Liarsville. Its high detail, waterfront and perspective are concept-only; they are neither canon nor approved tiles.

## Rejected revision 1 — history only

The user said: “What I see you making does not look like Pokémon emerald. It might work for a prototype but it is not looking like the style we want”. Do not integrate this draft or use it as a style baseline.

The prior kit contains 162 atlas entries, original reusable pieces, 8×8 source-tile references, palette metadata, and separate draft maps:

- [Old buildings](buildings-4x.png), [old trees](scenery-4x.png), [old bedroom](bedroom-4x.png)
- [Old Rootport overview](rootport-2x.png), [old forest route](forest-route-2x.png), [old Liarsville overview](liarsville-2x.png)
- [Old native atlas](../../../assets/review/environment-v1/atlas.png), [metadata](../../../assets/review/environment-v1/atlas.json), [editable source](../../../art/source/environment-v1/build.mjs)

The first draft's grid validity did not overcome flat building volumes, repetitive roof texture, muted material separation or lollipop-like trees. Layout fixes cleared border exits and connected doorstep lanes, but these remain rejected visual proposals, with no gameplay reachability claim. Rootport retains exactly three homes and the five established shops. Liarsville's pond/square/notice board are proposals. No new businesses, schools, characters or story content were added.

## Research and checks

[Deep environment research](../../reference-data/EMERALD_ENVIRONMENT_RESEARCH.md) pins pret/pokeemerald `5eff78649e7170a877b961ef0b3da13b81a16038`, distinguishes reconstructed source evidence from emulator captures and historical author testimony, and measures selected assemblies/reuse. The [art Bible](../../ART_BIBLE.md) now records the findings and the user's style correction.

Revision-2 validation covers native dimensions, exact nearest-neighbor enlargement, binary alpha, unique atlas IDs, bounds/nonoverlap, standalone PNG equality and 44 valid house-part references. Browser review observed the current page and image in the in-app browser. Physical phone/Safari and character-scale comparisons are untested. The existing game source, build script, save keys and canon document are unchanged. Visual quality and G1/G2 approval cannot be inferred from tests.

## Next action and publication

Get the user's response to this small revision. If it still misses the style, revise the sample; do not expand it. Once the direction is accepted, rebuild the indoor/outdoor tiles and all three location proposals in that style, then perform the planned character-scale and broader visual review. The original environment request remains active at this review boundary.

The Sites network permission was declined. No hosting attempt succeeded, no audience changed, and [the phone game](https://critz-tycoon.freemarketwildlife.chatgpt.site) still serves the earlier playable build. This review page is local and committed source only; a GitHub push does not deploy it. See PROJECT_STATUS for Git delivery evidence.
