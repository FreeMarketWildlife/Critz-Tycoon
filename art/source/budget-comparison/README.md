# M1.C1 native character sources

These are original, provisional drawings for the two-budget comparison, not approved replacement game assets. `mom.json`, `kaid.json`, and `nugget.json` are the editable native sources. Each stores a palette and full untrimmed rows for two frame widths (16 and 24), four directions, and idle/strideA/strideB. `.` is transparent. Each nontransparent symbol corresponds to one exact native pixel. `kaid.mjs` is Kaid's additional authoring helper.

From the repository root, run `node art/source/budget-comparison/build.mjs` to export the shared PNG, stable metadata, all-frame proof and authoring validation. Run `python3 scripts/check-budget-atlas.py` with Pillow to independently validate the exported PNG. No artwork is resized to fit either budget. The fourfold proof is nearest-neighbor presentation only.

Frames use bottom-center ground anchors `[8,32]` and `[12,32]`; idle feet end at row 30 and stride feet at row 31. The empty idle row permits the one-pixel gait extension without clipping. Both widths share each character's palette; larger drawings can use more entries from that same palette. Kaid's two sides are authored explicitly to preserve physical handle/spout asymmetry.

See [study notes](../../../docs/reviews/M1-C1/README.md) for provenance, limits and review state.
