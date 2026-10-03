# M1.C4 revision 3 — Target-pixel contours and depth

**Delivered for visual review; not approved artwork.** The user rejected revision 2's retained 2×2 blocks and flat rendering and requested diagnosis, correction and persistent art-bible lessons. This is still the boy Hero's front idle only.

[Clean before/after](before-after.png) · [1×/2× grid](hero-grid.png) · Native PNGs: [16×32](hero-16x32.png), [32×64](hero-32x64.png)

## What went wrong

1. **The implementation froze the coarse contour.** R2 constructed its high image with duplicated source rows/cells and duplicated part labels. Its `set` helper asserted the destination was already painted, preventing additions to empty edge cells. The final alpha mask had zero partially occupied 2×2 blocks.
2. **The tests rewarded the wrong constraint.** Exact doubled face/body row occupancy was treated as a success criterion. That preserved enlarged corners even though the standing contract allowed fine target-grid linework. Region envelopes, landmarks and mirrored anatomy are the constraints to retain; every source pixel's complete 2×2 occupancy is not.
3. **Outlines and shading did not explain the form.** Large doubled dark bands enclosed rectangular color fields. Small disconnected highlights changed the texture without improving the head, sleeve or shoe volume. The displayed grid also made edge weight harder to judge; a clean proof was missing.

## Reference inspection and target table

The pinned Brendan front-idle source and the prior annotation table were re-inspected before drawing. The source file SHA remains `f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1`, at revision `5eff78649e7170a877b961ef0b3da13b81a16038`. The user was shown the measured/doubled targets before authoring: full figure 14×21 → 28×42, headwear 12×8 → 24×16, face/ears 14×5 → 28×10, each arm/hand region 4×4 → 8×8, each leg/shoe region 4×3 → 8×6, eyes 1×2 → 2×4. Anchor `(8,32)` → `(16,64)`; final idle row 30 → 60–61. All thirteen annotated region bounds remain at their measured doubled targets, as recorded with actuals in [independent-validation.json](independent-validation.json).

Boundary inspection used foreground pixels having any four-neighbor transparent/out-of-frame neighbor. Among the selected frame's 50 boundary pixels, 25 use black, 12 blue-violet (palette index 5), 11 brown (4), and 2 dark blue (8). This supports selective colored outlining in this particular frame; it does not establish a universal formula, lighting rule or historical authoring process. [Pinned source](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/brendan/walking.png). Source artwork remains outside the repository.

## What changed

- Authored the 32×64 drawing from explicit target-grid contours and anatomical labels, not a doubled low-resolution mask. Hair, cheeks, sleeves, hands and shoes now have single-target-pixel corner steps and shorter edge runs.
- Preserved the native frame, measured region bounds, eye positions, ground anchor and mirrored anatomical masks. Individual row occupancy and occupied area intentionally differ; that is the requested contour refinement, not a change to frame scale.
- Used dark brown skin edges, colored hair contours, warm sleeve shading and darker local arm/torso/sole contacts. Highlights form connected light-facing groups. The palette contains 15 opaque colors; the hair highlight and cream shadow are explicit original choices, not copied reference colors.
- Retained the exact 1× PNG as a comparison baseline. Added a clean enlarged before/after, native-scale samples, and the required one-pixel grid with the central X symmetry line and numbered ten-row Y guides. Review grids are not baked into native assets.
- Added the cause, contour rules, outline/depth guidance and clean-view requirement to ART_BIBLE, with reminders in AGENTS and the reusable prompt.

## Checks, limitations and delivery

Independent checks pass for **2,560 native/source/grid cell comparisons**, all **13 measured region envelopes**, exact eye locations, paired anatomical masks, binary alpha, connected figures, palette limits, centerlines and every ten-row guide. The 1× PNG is byte-identical to R2. The 2× revision changes **50 alpha cells** and has **34 partially occupied 2×2 blocks**, compared with zero before. This demonstrates actual contour subdivision, not artistic quality. Both clean/grid proofs were inspected at enlarged and native presentation sizes. See [native checks](validation.json) and [independent checks](independent-validation.json).

Original afro shape and clothing remain adaptations inside the reference envelopes. Hidden anatomy is not recoverable from the source; no such measurement is claimed. No universal Emerald rendering formula, emulator observation, final visual acceptance, animation, back pose, roster expansion or playable integration is claimed.

Run `build.mjs` with Node and `CODEX_PRIMARY_RUNTIME_NODE_MODULES` pointing to modules containing `sharp`. Run `verify.py` with the pinned local reference PNG. This edits original native indexed artwork; no concept bitmap was resized into a sprite. Native JSONs include editable rows and anatomical labels.

Work is on `main`, opening commit `94a8f18246a5777aed7de0a627f3858d4e443d66`. Existing unfinished M1.I3 edits are preserved and excluded. Commit/push verification is recorded in PROJECT_STATUS and the handoff. Only review/documentation changes were made: the playable build remains unchanged and requires no deployment. Next action: the user reviews contour, outline weight and depth; continue still refinements before animation.
