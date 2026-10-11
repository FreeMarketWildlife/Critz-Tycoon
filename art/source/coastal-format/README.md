# Shared coastal format — WA8 review

Direction and lessons live in `docs/ART_BIBLE.md`. One native construction in `src/coastal-format.js` serves every water/ground and water/water pair. Current review renderers do not load the retired WA6/WA7 transition sheets. Original texture/prop pixels are repacked without resampling.

Build from repository root:

1. Run `node art/source/coastal-format/build.mjs`.
2. Run Pillow Python `art/source/coastal-format/pack.py`.
3. Run Pillow Python `art/source/coastal-format/color.py`.
4. Run `node art/source/coastal-format/proof.mjs` and Pillow Python `scripts/check-coastal-format.py`.

Intermediate pixel/proof files live in `/tmp`; do not commit them. Masks, overlays and colored references share the same construction. Use raw eight-neighbor context, retaining diagonals; canonical format alone does not select a joining variant. `atlas.json` maps logical IDs to shared native pixels, deduplicating identical frames. Animation heads remain distinct Tiled IDs where different sequences begin with identical pixels; transparent tide frames share one native blank frame. Do not interpret logical aliases as independently authored tiles.

The colored PNG/Tiled exports contain frame0 reference artwork; water textures and foam have separate3.2-second sequences. `coastal-drawing.js` composes the continuous field for live animation. Shore exports use16px Y registration; surface exports use0. Whole-cell collision and source palettes remain unchanged. This is review artwork, awaiting the user.
