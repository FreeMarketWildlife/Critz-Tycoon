# M1.GH1 — Girl Hero first front idle

**One front idle candidate, technically checked; awaiting Eutychus/independent visual review.** No other direction or walk has been authored. Review-only original art; existing game assets, saves and deployment are unchanged.

![Front head, ears and body join](front-head-ears-join.png)

The selected R11/C6 identity remains a ten-year-old Black child with twin natural puffs, coral ties, short temple locks/fringe, coral/cream shirt, blue shorts and burgundy shoes. The native C6 front is also the exact C7 passing still. The separate 24×32 G1/v3 lineage is excluded. The enlarged generated R11 concept supplies design intent only; its pixels are never resampled into the candidate.

## Construction decisions

- Retain original C6 visible head through row44. Its old “skull” annotation includes neck/collar rows45–46; those rows are excluded from the head layer. That inherited scaffold is authored evidence, not observed hidden skull anatomy.
- Change only the bounded ear field to small rounded mirrored ears. Both actual rendered ear patches mirror in RGBA; preserve the original asymmetric puffs, fringe and face outside that field. Paired visible eyes remain two2×4 clusters; no new mouth or nose is drawn.
- Adapt the checked HR14 South idle body layer as a **declared shared visual construction**, retaining its full silhouette, contacts and registration. This is neither a girl-specific observed pose nor proof of hidden anatomy. Do not narrow/tallify the child by gender or expose a neck/leg to explain the costume.
- Restore the selected burgundy shoe material deliberately: C6's native palette had lost it. Existing near-sole color sites become burgundy/coral accents; the pale band remains. No extra shoe pixel or longer foot is added.
- No backpack is added to this selected Girl design. Existing Hero pack corrections remain in HR14. Hidden neck, hip, knee, ankle and anatomical-foot measurements remain unresolved/null.

Canvas32×64, frame-edge anchor(16,64), occupied bounds[3,21,29,62), last painted row61,14 colors. Anchor and painted contact are distinct. All display enlargements use nearest-neighbor integer scaling; no per-character fitting.

## Inspectable deliverables

- [Native candidate](girl-front-idle.png) and [construction map](girl-front-construction.png).
- [Native/4× light and dark comparison](front-native-light-dark.png).
- [Separate actual feature/material masks](front-feature-material-masks.png): hair, puff regions, ties, eyes, ears, hands, near-sole color and pale band. The old authored scaffold is explicitly distinguished from observed anatomy; hair/puff masks exclude tie material.
- [Existing grass/path context](front-world-context.png): original review mock, not a live game/collision test.
- [Editable source and builder](../../../art/source/hero-girl-r1/), separate head/body layers and source hashes in construction.json.
- [29 actual-pixel checks](checks.json) and [two actual Sprite Editor validations](editor-validation.json).

The fixed-frame design/C6/C7/current/HR14 comparison, including the generated concept thumbnail, is external review evidence at `/Users/tanoshi/.codex/visualizations/2026/10/15/girl-hero-preflight/front-identity-comparison.png`. It is excluded from runtime assets. No source game/reference pixels enter the native candidate.

## Review limits and next action

Owner inspected the saved head/join, native/light/dark, material masks, design comparison and world-context plates. The current front has a narrower silhouette below the retained puffed head than C6, and the front cuffs/hands remain bright; their overall balance needs independent visual judgment. Tests prove protection and source consistency, not artistic acceptance. There is no animation/cycle claim for this static checkpoint.

Eutychus reviews this **first front** before any four-direction idles or walks. Broader M1 appearance and M2 movement gates remain open. Do not silently install this candidate or extend the roster. The completed HR14 boy construction/delivery does not grant Girl appearance approval.

Rebuild with the bundled Pillow Python: run `art/source/hero-girl-r1/build.py`, then `present.py` with an external review directory, then `verify.py`. Validate both `.sprite.json` projects with `sprite-editor/model.js`'s `validateProject`.
