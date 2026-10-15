# M1.HR13 — Four-direction elevated-view Hero checkpoint

**Stable, technically checked, UNAPPROVED artwork.** Implements Eutychus's user-authorized projection correction and four-direction construction study. The head overlaps the upper torso and completely hides the neck primitive in both clothed Hero and neutral template. Existing front head pixels, mirrored ears, front joints and lower body remain exact to HR12. Compact backpack, starter outfit, Black child identity and nose/mouth-free face are retained. One bounded profile cleanup removes stacked internal cuff/shoe bands without changing silhouette, foot extent or joints.

## Review files

- [Original-only idle checkpoint](four-direction-idle-hero-template.png), [projection before/after](projection-before-after.png) and [occlusion map](projection-occlusion-map.png).
- [Labelled anatomy contact](four-direction-anatomy-contact.png), [registered clothing/attachment overlay](four-direction-outfit-registration.png) and [bounded profile cleanup](profile-overlap-cleanup.png).
- Per-direction `*-all-poses.png`, native `hero-*-native.gif` and `dummy-*-native.gif` retain editable originals separately from reference comparisons.
- External comparison directory: `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr13-review/`. Primary delivery files: `four-direction-idle-source-hero-template.png`, `four-direction-source-hero-template-4x.gif`, `four-direction-source-hero-template-SLOW4x-4x.gif`. Combined walks show south/north/west/east, each as reference/Hero/template; 224×192 native and exact nearest 896×768 exports. Per-direction native/4x/labelled-slow comparisons and all-eight-frame contact sheets are also present there.
- Idle sheets preserve the first checkpoint wording “walk proofs pending checks”; subsequent completed walk checks are recorded below. Historical `checkpoint-1-*` copies remain external. Artifact pixels are now frozen for parent review/Library delivery.

## Reference facts and construction proposals

Pinned Emerald PNG and animation tables: pret/pokeemerald revision `5eff78649e7170a877b961ef0b3da13b81a16038`. Exact hashes and decoded frame/row observations are in [reference-observations.json](reference-observations.json). Source paths are `graphics/object_events/pics/people/brendan/walking.png` and `src/data/object_events/object_event_anims.h`. Indexed transparency is palette index zero; source 16×32 frames are expanded exactly 2× with a shared full-frame anchor, without per-pose fitting. Source walk sequences are south 3/0/4/0, north 5/1/6/1, west 7/2/8/2 and east mirrored west, with eight engine ticks per phase. This is source inspection, not emulator observation.

The supplied front GIF is separately pinned by SHA256 `5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e`: eight 100ms frames, front only, A/A/P/P/C/C/P/P. South comparison uses this source. Other comparisons synchronize ROM poses to the **proposed Critz 100ms preview clock**, not Emerald engine cadence. Normal cycle is 800ms; labelled slow is 3200ms with identical actor pixels. Critz inherited painted foot bottoms are row61 in contacts and59 passing; ROM stride ends row63. A common frame anchor does not prove equal painted ground contact or gait.

Hidden joints, profile bodies and projected attachment sites are original 2D proposals. Numeric camera pitch, world bones and hidden anatomical measurements remain unresolved. Profile L/R mask names denote near/far limbs; front/back use viewer-side labels. The dummy is a registration scaffold, not measured source anatomy. Source headwear and Critz hair are different designs; no exact Emerald head-shape or motion match is claimed.

## Checks and remaining judgment

`verify.py` passes 32 native poses, ten actual Sprite Editor editable projects and all 28 decoded eight-frame GIFs: binary alpha, connectivity, palette budget, saved-source equality, timing/looping, nearest enlargement, visible-ear layering, neck occlusion, intended clothing-part registration, protected front pixels/joints/lower body and unchanged profile cleanup alpha/extent. [Machine report](independent-checks.json), [editor report](editor-validation.json). The large combined4x files are derived exports from a validated native project; editor canvas limits were not changed.

Parent's independent static/phase review found the four-direction neck correction successful and bounded cleanup visible; its initial report covered the preceding25 GIF set. Parent subsequently independently verified the combined eight-frame panels and exact4x/fast-slow actor pixels. Owner's final report covers all28. Continuous browser playback was not established by the independent reviewer. Profiles still read angular/heavier and their stride spread may feel too wide; passing boot weight remains subjective. Technical checks do not resolve or approve those concerns.

No gameplay/editor UI/save/map changes, deployment or M1/M2 acceptance. HR11 remains parked, unadopted and unstaged. Exact next action: Eutychus presents this stable review and handles Library export; owner holds further art pending the scoped response.

## Library delivery

Seven review files are saved as new Library version0 items. Downloaded copies match exact local bytes and decoded pixels; the combined walking GIFs retain eight frames at100ms/400ms. [Identity/download verification receipt](library-review-receipt.json) records actual IDs and checks. This delivers the stable unapproved review; it changes no artwork or playable build. Parent/user visual response remains next, with profile weight/stride and proposed template fit explicitly unresolved as appearance judgments.
