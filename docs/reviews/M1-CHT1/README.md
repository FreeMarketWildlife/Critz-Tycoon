# M1.CHT1 — Shape-preserving character template

**Existing16 static poses awaiting review. Creator and animation work remain paused.** The user corrected the premise: a dummy is a standardized character template retaining the finished waist, clothes, hands, full shoes and each pose's projected shape. All prior NB anatomical dummy bodies are rejected, including South. Protected South **dressed Hero** is preserved.

Per-direction native-size pairs and countable native-grid lower crops:

- [South idle/A/P/C](south-static-native-grid.png)
- [North idle/A/P/C](north-static-native-grid.png)
- [West idle/A/P/C](west-static-native-grid.png)
- [East idle/A/P/C](east-static-native-grid.png)

[Actual saved source/region/contact checks](static-checks.json) · [16 Sprite Editor still-project validations](editor-validation.json) · [Source builder and registration masks](../../../art/source/character-template-r1/README.md).

Only a new head-only bald scalp contour replaces hair. Below-head RGBA, waist, hands, cuffs, full shoe shape, soles and contacts stay exact to the current dressed Hero. Hair, face/skin, shirt, shorts, shoes, pack and straps have separate real source-region PNGs per pose. The same starter clothes remain. No reconstructed torso/pelvis/limb/foot part is read. Existing NB3 appearance ownership is reused solely to identify actual dressed-Hero material pixels; its rejected body geometry is not reused.

Actual original hair reapplied over each template, with explicit selected-hair hidden-scalp coverage, reproduces all16 dressed Hero PNGs exactly. No opaque full-Hero image hides a smaller mannequin. Source dimensions32×64, anchor16,64, selected source hash, exact material sites and protected row spans are recorded per pose. All four South dressed Heroes remain exact to original HR14. The profile scalp adds no far-ear bulge; actual source eye/ear/skin pixels remain. No nose or mouth is added.

Protected below-head rows begin44 in South/profile and northP; north idle/A/C's original hair/nape reaches row44, so their below-head region begins45. Their row44 hair changes with the bald scalp; this is not a body/outfit change. Every actual non-hair material-region cell, waist/shoe/contact RGBA remains exact independently of this boundary. The7011 saved-pixel checks and16 editor validations establish these facts, not appearance acceptance. Current north/side dark pants/shoe readability and mixed-scale judgment remain OPEN under Eutychus; those source colors/shapes have not been changed by this template pass.

Eutychus inspected [South idle aligned](south-idle-aligned.png), [northP aligned](north-P/north-P-aligned.png) and [West idle aligned](west-idle/west-idle-aligned.png), confirming scoped single-frame shared-shape preservation. He then directed the remaining existing static proofs. This is method confirmation for those individual frames, not user scalp acceptance, full-pose acceptance or creator release. Individual pose folders include aligned full views, source/template grid crops, independent regions, exact recomposition and editable `.sprite.json` still projects. Root South idle remains at this directory's top level to preserve its first checkpoint links.

The earlier untested `character-creator/` draft remains explicitly PAUSED, excluded from the playable build and unpublished. Its NB3 body dependency must be replaced after the template is reviewed. No new animations, roster, gameplay, saves or hosting change. Earlier rejected NB history and contact-tile review namespace remain intact.

Exact next action: Eutychus critiques all16 static source/template/contact comparisons and supplies concrete NWE material findings before any shoe redesign, new animation or creator continuation.
