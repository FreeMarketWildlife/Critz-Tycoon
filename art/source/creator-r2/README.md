# CC1 BS2-backed creator source

Run `build.py` with Pillow to regenerate `character-creator/data.json`, registered native close-crop hair and explicit feature/material masks. Only BS2 and the established per-view source feature registration are read; no NB3 anatomical body data. All default dressed/bald pixels remain exact, and PM1 is excluded.

`review-looks.json` defines six meaningful review combinations. Run `node art/source/creator-r2/proof.mjs`, then `proof.py` with Pillow to regenerate the three native/enlarged composition sheets and two looks' all-direction1×/4× walk GIFs. The proof decodes every saved GIF frame, alpha, timing and loop. Temporary raw vectors stay in `/tmp`; original editable source/masks remain here.

The close crop is original registered native art using the existing hair ramp on the accepted scalp. Actual eyes/ears stay outside its mask. Skin remaps include hair-dependent skin/nape shadows. Ear and shoe variants retain their exact source silhouettes; optional face marks stay inside registered skin sites. [Prototype review and limits](../../../docs/reviews/M1-CC1/README.md).
