# Living collection source

Four-direction character walks, critter movement and layered habitats. [Review/download](../../../docs/reviews/M1-C7/README.md). Art direction lives in [ART_BIBLE](../../../docs/ART_BIBLE.md).

`build.mjs` checks baseline hashes and invokes `characters.mjs`, `critters.mjs` and `habitats.mjs`. `pixels.mjs` supplies integer-cell operations and native export through Sharp and the Sprite Editor model. JSON/RLE files reopen in the editor. Larger projects store every native animation frame with exact custom RGB.

Run with Node and Sharp via `CODEX_PRIMARY_RUNTIME_NODE_MODULES`, then the review's `verify-and-present.py` with Pillow. Reproduction uses this repository's M1.C6 and approved Boy V1 source inputs. The pack supplies assets, not a standalone app. No gameplay files are changed.
