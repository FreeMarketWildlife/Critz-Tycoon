# Native idle collection source

M1.C6: eleven new character stills and eight animal studies. These are review outputs, not accepted gameplay replacements. Art direction lives only in [ART_BIBLE](../../../docs/ART_BIBLE.md); see [the review packet](../../../docs/reviews/M1-C6/README.md) for design choices, actual measurements, preview grids and limitations.

`build.mjs` authors exact indexed cells and writes PNG, Sprite Editor JSON, exact RLE and metadata. Each JSON/RLE opens in the existing editor. `*.masks.json` records authored construction masks separately from visible hair, clothes and accessories. Do not edit the approved Hero Boy V1 to rebuild this collection.

Reproduction requires Node and Sharp via `CODEX_PRIMARY_RUNTIME_NODE_MODULES`. The review's `verify-and-present.py` uses Pillow to verify exact exports and render countable guides. No screenshot sampling, generative-image overlay or smoothing is part of the source pipeline.
