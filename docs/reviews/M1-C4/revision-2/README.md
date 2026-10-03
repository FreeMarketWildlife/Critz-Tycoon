# M1.C4 revision 2 — Mirrored idle anatomy

**Delivered for user review; artwork acceptance pending.** The user identified uneven arm/hand shapes in revision 1 and required a centerline, default bilateral idle anatomy, measured Emerald 2× construction and permanent art-bible presentation rules.

[Hero at both budgets](hero-grid.png) · [Symmetry / part proof](hero-symmetry.png) · [Reference measurements and actuals](MEASUREMENTS.md)

Native transparent exports: [16×32](hero-16x32.png), [32×64](hero-32x64.png). Editable indexed pixels and per-pixel part labels: [1× source](hero-16x32.json), [2× source](hero-32x64.json). SVG review versions retain countable cells at any zoom: [character grid](hero-grid.svg), [symmetry grid](hero-symmetry.svg).

## What changed

- Each front-idle skull/face, eye, arm, hand, torso and lower-limb mask mirrors around x=8 / x=16. Matching visible clothing/skin boundaries are checked independently of shading. The old 32×64 drawing had **15 body material-boundary mismatch pairs**; the new drawing has **zero**. An equal outer silhouette alone did not catch the old defect.
- Eyes moved to the measured source positions: 1× columns 6 and 9, rows 19–20; 2× rectangles `[12,38,14,42]` and `[18,38,20,42]`. Eye highlights can differ without changing those rectangles.
- The narrower **12×8 → 24×16 headwear envelope** replaces revision 1's oversized hair envelope. The original afro is a declared contour adaptation inside that measured envelope, not a copy of the pointed reference cap. Its occupied area differs; see the measurement record. Hidden skull bones are not observable in the source and are not claimed as measured.
- Every native cell is displayed as one square. The prominent pink **vertical** line splits the X width in half; blue **horizontal** guides are numbered at each ten Y pixels. Both frames occupy 384×768 display pixels, using 24× and 12× integer enlargement. Grid lines are not baked into native PNGs.
- ART_BIBLE now makes symmetric front/back idle anatomy the default, explicitly permits hairstyle/color asymmetry and documented unusual-character exceptions, and requires this 2× grid presentation for all new characters. Boy Hero retains both budgets until the user accepts the style. AGENTS and the reusable prompt carry the rule forward.

## Evidence and limits

The pinned Brendan front-idle PNG was freshly fetched outside the repository and its SHA-256 matched the earlier ledger. Its measured table and doubled targets were shown to the user before the revision was drawn. [measure.py](measure.py) independently reads that source and the new native outputs; all **13 annotated region envelopes**, both eye rectangles, anchor, baseline and the face/body occupied rows match their targets. Anatomical region definitions and original-design deviations are explicit. The new user-supplied montage is a style preference reference, not asserted to be a verified Emerald source sheet.

[Native validation](validation.json) and [independent decoded-PNG validation](independent-validation.json) pass: all **2,560 grid-cell centers** match the indexed data and PNGs; both figures have binary alpha and connected silhouettes; anatomical reflection and body-material reflection have zero mismatch pairs. Both review plates were visually inspected. Original lighting and hue differences remain permitted. Hair is excluded from mandatory anatomical mirroring, although this version's outer afro mask is symmetric.

This is **front idle only**. Back-idle symmetry is a permanent rule, but no new back frame, animation, roster expansion or playable migration was requested or produced. Reference pixels stay outside the repository and runtime. No gameplay, v1 storage, collision or world files were changed for this task. Existing unrelated M1.I3 edits remain intact and are excluded from the commit.

## Reproduction and delivery

Run `build.mjs` with Node and `CODEX_PRIMARY_RUNTIME_NODE_MODULES` pointing to modules containing `sharp`. It edits native indexed source and exports original PNGs and deterministic grid layouts; no generated concept image is resized into a sprite. Run `measure.py` with the pinned local reference PNG to reproduce the source comparison. The reference SHA is checked before analysis.

Branch: `main`, opening commit `787643fd1974c82af5c284209312ca32fe717d45`. Commit/push and remote verification are recorded in PROJECT_STATUS and the handoff. Only documentation and review artifacts changed; the playable build is unchanged and no deployment is required. Next action: the user reviews this still's anatomy/style; revise the idle before walking.
