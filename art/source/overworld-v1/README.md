# Overworld native source

`build.mjs` authors original integer-pixel artwork with the project's existing `Raster` utility, packs the atlas and builds every proof from that atlas. It reads no reference-game images. Run from the project root:

```sh
node art/source/overworld-v1/build.mjs
python3 scripts/check-overworld.py
```

`pixels.json` is a lossless indexed source. To use edited rows within the declared palette, rebuild with `node art/source/overworld-v1/build.mjs --from-pixels`. Running without the flag restores the deterministic authored version. Preserve edits in version control first. Palette changes also require updating the build's palette declaration.

The built-in imagegen tool made `design-study.png` using the exact saved `design-prompt.txt`. It is **concept evidence only**: irregular spacing, painterly density and transparency artifacts prevent use as a production tileset. No pixels from that study or Pokémon Emerald are sampled into the master. The native kit interprets its warm/cool materials through separately authored pixels and modular geometry.

Official Hero Boy V1 is read unchanged for scale proofs; no character pixels appear in the atlas. Art direction lives in `docs/ART_BIBLE.md`. See the M1.E2 review for checks and limits. ZIP source files preserve their repository-relative paths; rebuild inside this repository, which supplies the approved Hero scale source.
