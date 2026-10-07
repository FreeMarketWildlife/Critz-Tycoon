# Critz overworld collection · review 01

One master PNG contains the whole environment kit, including every building part. **Awaiting user visual review.** These assets do not replace accepted game artwork.

- `master.png`: authoritative native atlas; no grid, labels or spacing between cells.
- `master.json`: stable IDs, coordinates, four base-tile rectangles per cell, terrain connections, assemblies, layer and footprint proposals.
- `master.tsj`: external Tiled tileset, relative to the adjacent PNG. Empty reserved slots are transparent; use named entries in the index.
- `palette.json`: original material ramps.
- `map-0.json` / `map-1.json` / `map-2.json`: lightweight review maps, **not Tiled map exports**. Four named layers contain stable tile IDs.
- `proof-*.png`: independently checked renders of those maps. `town-with-hero.png` adds the unchanged approved Hero V1 for scale.
- `viewport.png` / `water-garden-viewport.png`: native framing examples. Enlarged files use exact nearest-neighbor scaling.
- `critz-overworld-v1.zip`: native atlas, index, Tiled file, maps, proofs and editable sources.

Use `master.png` with 32px cells, zero margin and zero spacing. Base tiles are the four 16px quadrants of each cell. Import the `.tsj` in Tiled or read the index from a custom renderer. Sample at integer positions with nearest-neighbor filtering. The source has no filtering gutters; generate a padded runtime atlas before enabling bilinear filtering or mipmaps.

Terrain masks use N/E/S/W/NE/SE/SW/NW bits from the manifest. Clear a diagonal bit unless both adjoining cardinal bits are present. The resulting 47 masks each have an authored tile. Fence and hedge masks use only N/E/S/W. These rules select artwork, not gameplay collision.

Build houses from `assemblies`, or repeat roof/wall center tiles between their ends. Five-cell cottages and the seven-cell shop reuse roof pieces. `assemblyMetadata` provides proposed footprints, door cells and anchors separately from artwork. Runtime occlusion and tree sorting remain an integration task.

Static water, waterfall, fountain, flowers and door states are supplied. No animation cycle or timing is implied. Interiors, seasonal/night palettes and further biome sets are outside this revision. Art direction: `docs/ART_BIBLE.md`. Evidence: `docs/reviews/M1-E2/README.md`.
