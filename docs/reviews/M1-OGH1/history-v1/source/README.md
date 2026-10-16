# M1.OGH1 editable four-idle candidate

Review-only, awaiting root visual review. See `docs/reviews/M1-OGH1/README.md` for actual reference basis, proposals, checks, defects and next action. Existing GH1/C6 and shared sources remain untouched.

`{south,north,west,east}.layers.json` stores actual ordered32×64 native indexed layer arrays and palette. Layers include independent original hair, ties, eyes, ears, face, clothing, exposed arms/hands, shorts and shoes. Recomposition is tested against each saved PNG. `*.sprite.json` files open in the existing Sprite Editor. Flat-construction projects are separate diagram views with proposed covered skull/internal ownership, not accepted anatomy.

`build.py` uses bundled Python/Pillow and writes only this folder and `docs/reviews/M1-OGH1/`. It does not stage, commit, push, deploy or touch runtime. v0 is frozen in review `history-v0/` before bounded corrections. No walking frames are authored.
