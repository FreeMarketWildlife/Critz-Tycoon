# M1.CHT1 — South character template, single-frame checkpoint

**Awaiting review. Creator paused.** The user corrected the premise: a dummy is a standardized character template retaining the finished waist, clothes, hands, full shoes and each pose's shape. The prior NB anatomical reconstruction is rejected, including South. Protected South **dressed Hero**, rather than the rejected dummy, is the source of this checkpoint.

[Aligned South idle Hero / bald template / occupied-pixel overlay](south-idle-aligned.png) · [Countable lower native grid](south-idle-lower-grid.png) · [24 saved-pixel checks](checks.json) · [Exact region cells and row spans](../../../art/source/character-template-r1/registration.json).

Only a new head-only bald scalp contour replaces hair. Every RGBA pixel on rows44–63 is exact to current South dressed Hero, including waist, hands, cuffs, shoe shape and pale soles. Hair, face/skin, shirt, shorts, shoes, pack and straps have independent real source region PNGs. The same starter clothes remain. This is not a naked body or a smaller body hidden beneath a full opaque Hero overlay. No reconstructed torso, pelvis, limb, foot or prior NB body part is read by this builder. Existing NB3 appearance ownership is reused only to identify actual dressed-Hero material pixels; this does not reuse the rejected dummy geometry.

Reapplying the independent original hair over this template with an explicit selected-hair hidden-scalp mask reproduces the original Hero exactly. The mask, original source hash, dimensions32×64, anchor16,64, all region sites and lower row occupancy are recorded. Optional face variants and other poses are not implemented in CHT1. No mouth/nose is added. Tests prove pixel facts; the bald head and appearance still require visual judgment.

The first uncommitted northP experiment was superseded by the direct South-first instruction and parked outside the repository. No new animation or all-pose rollout yet. The earlier untested `character-creator/` draft is paused and excluded from the build; it currently references rejected NB3 layers and must be replaced after this direction is reviewed. No gameplay/save/hosting changes.

Exact next action: Eutychus reviews this one aligned frame before the same shape-preserving method extends to existing NWE directions/poses and later the creator.

## Focused follow-up frames

Eutychus inspected South idle and [north P](north-P/north-P-aligned.png), confirming that each retains the actual dressed waist, hands and full shoes and that north P has continuous head/nape/collar contact. This is scoped shape confirmation for those individual frames; user scalp/appearance and full-pose readiness remain open. North's [native lower grid](north-P/north-P-lower-grid.png) and24 saved checks are separate from South's unchanged proof.

[West idle aligned comparison](west-idle/west-idle-aligned.png) · [West lower grid](west-idle/west-idle-lower-grid.png). The head-only profile scalp omits an invented far-ear bulge, while the actual source near-ear/eye/skin and every finished outfit/waist/shoe pixel remain. Its24 saved checks pass; profile critique is pending. These are still images, not an animation or creator release. No remaining-pose batch has been run.
