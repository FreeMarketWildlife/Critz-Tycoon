# M1.I2 playable environment artwork

This original native-pixel environment kit extends the editable revision-2 Critz roof, wall, grass, window, flower and tree drawing source. It is intended for the existing game, with final user visual acceptance still pending. No Pokémon artwork, rejected revision-1 environment pixels, or browser prototype furniture drawings are used.

`build.mjs` contains the original revision-2 module authoring source and deterministic packing/validation. `extension.mjs` adds interior materials, furniture, vegetation, rescue markers, signs, and eight centered-entrance building variants using the revised color families. `raster.mjs` is a generic integer raster/PNG writer copied from the earlier authoring utility; it contains no artwork or reference input. `palette.json` records editable color families.

Run from the project root with Node:

```sh
node art/source/playable-environment/build.mjs
```

Exports:

- `assets/playable/environment/atlas.png`: native 512×320 RGBA sheet with binary transparency and 54 stable IDs.
- `assets/playable/environment/atlas.json`: rectangles, ground/sort anchors, opaque bounds, palette families, status, and source revision.
- `assets/playable/environment/atlas-3x.png`: exact nearest-neighbor inspection sheet.
- `assets/playable/environment/bedroom-layout-check*.png`: native 240×160 and exact 4× environment placement checks, without characters. These are QA artifacts rather than runtime backgrounds.
- `docs/reviews/M1-I2/environment-validation.json`: deterministic technical checks.

All props use a bottom-center ground/sort anchor, independent from their collision data. Buildings are 96×80 with centered door anchor `[48,80]` and threshold `[40,64,16,16]`. Tree canopy and trunk layers retain the exact original revision-2 pixels and share a `[16,32]` anchor. Runtime placements must provide explicit collision, foreground, and interaction data separately; image bounds never define gameplay automatically.

The environment additions use the repository-native pixel source workflow rather than a generated raster sheet. Every exported pixel comes from editable integer drawing instructions, and the authoring source never reads any PNG. This keeps 16-pixel repetition, transparent edges, anchors, and building entrances reproducible. The export and visual checks establish technical validity only; they do not record user art approval.

The nighttime tank includes an original 14×5 native gecko sprite for Pebble, placed on the log before the breakage story beat. Its editable pixel rows live in `extension.mjs`; the broken and daytime tank fixtures do not show Pebble.
