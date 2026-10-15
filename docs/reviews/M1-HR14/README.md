# M1.HR14 — Literal visible lower construction, rigid pack, featured dummy

**Stable technical checkpoint, UNAPPROVED.** Phil rejects HR13's legs and cape-like backpack swing. Eutychus's authorized HR14 handoff supersedes the previous lower-body proposals; HR11 remains parked and is not the construction base. Original Black child identity, hair, rounded ears, no-mouth/no-nose default and HR13 head-over-torso projection remain intact.

## What changed

The lower visible costume on rows54–63 is reconstructed from the actual registered reference: same occupied spans, gaps, colored-plane positions, overlap and phase, with Critz's original palette. No exposed calf or hidden bone length is invented. Front P remains joined through56 and first opens57; A/C retain the source's connected mass rather than the HR13 early split. North/west/east retain the actual pinned ROM lower boundaries, including stride bottoms63 and passing bottoms61. Front uses the supplied custom GIF's59/61 bottoms under its fixed registration. No per-pose fitting hides these differences.

The back and profile pack has one compact canonical shape per direction and one torso-local attachment. South's rear bag is occluded by the torso/head; its fixed straps remain visible. A/C never mirror the bag with the arms. The pack and straps translate only with the declared torso transform `[0,0]` or `[0,-2]`; normalized RGBA hashes are identical across all poses. Actual visible pack coverage is checked separately against the final composite, since occlusion is not deformation. [All-eight torso registration proof](torso-registered-pack-all-eight.png).

Dummy now shows aligned eyes (back eyes naturally occluded), rounded ears and clear upper hand attachments, plus head/torso/arms and the same covered lower construction. It does not expose a neck column or turn costume shading into bare anatomy. [All-direction/pose featured dummy sheet](four-direction-featured-dummy-sheet.png). [Common features and contact registration](four-direction-common-feature-registration.png) labels head, ears, eyes, arms/hands, torso, occluded/inferred legs and feet/contact candidates. [Feature records](common-feature-registration.json) retain observed last-painted spans and the invariant16,64 edge anchor, while hidden hip/knee/ankle/anatomical-foot attachments remain explicitly unresolved/null. This supplement changes no character pixels.

Independent checkpoint review caught a mistaken interpretation of a red side costume rectangle as a hand. That extra skin was removed before final checks; the region is now an original coral costume plane. Existing upper hands supply the dummy's hand features. Lower masks are named visible material planes, not asserted anatomical pants/cuff/foot roles. Colored garment shading does not establish where a hidden leg, knee, hand or foot begins.

## Exact review deliverables

Reference-bearing artifacts remain outside the repository/build at:
`/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr14-review/`

- `first-native-aligned-boundary-checkpoint.png`: all four directions and three unique walking poses; source/Hero/dummy at3x and native, aligned lower alpha overlap/difference.
- `{south,north,west,east}-aligned-lower-boundary-grid.png`: true lower pixel grids, source/Hero and aligned difference (white both, red missing, blue excess).
- `{direction}-all-eight-source-hero-template.png`: every actual paired pose/hold at3x and native.
- `source-hero-template-{direction}-native.gif` and `-4x.gif`: source/Hero/dummy at native and exact nearest4x. `-SLOW4x-native.gif` / `-SLOW4x-4x.gif` are distinctly labelled4x slower copies, with identical actor pixels.
- `four-direction-PHASE-source-hero-template-{native,4x}.gif` and labelled `-SLOW4x-*`: additional synchronized phase-index comparison boards. **Their common100ms phase clock is not stock Emerald playback.** Use the individual directional loops to judge timing.
- `preview.html`: local review page pairing normal and slow directional loops, without touching game/runtime/editor files.

Original-only PNGs, native Hero/dummy GIFs, material-boundary diagrams and reports live in this review directory. Editable native projects and the repeatable scripts live in `art/source/hero-directional-r14/`. `lower.py` is an authored coordinate template in original materials; its build imports no reference image/palette/costume raster. `construction.json` records the canonical layers, torso transforms, final visible masks and explicitly qualified construction data. Source-colored observations/previews stay external.

## Reference facts and timing

Supplied front GIF: `https://i.redd.it/01agijgmbz561.gif`, SHA256 `5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e`. Freshly decoded all8 frames,100ms each, A/A/P/P/C/C/P/P; exact4-display-pixel reduction of the left sprite into32×48, fixed14top/2bottom32×64 registration. It proves front motion only; actual source idle is unobserved. Front idle is explicitly a passing-derived Critz proposal.

Other directions: pret/pokeemerald `5eff78649e7170a877b961ef0b3da13b81a16038`, `graphics/object_events/pics/people/brendan/walking.png` and `src/data/object_events/object_event_anims.h`. PNG SHA256 `f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1`; indexed transparency0, exact2x expansion, one invariant full32×64 frame/edge anchor16,64. N5/1/6/1, W7/2/8/2, E flippedW, with8 engine ticks per phase. [Fresh source/table/row observations](reference-observations.json). Source inspection is not emulator observation.

Normal front GIF cycle800ms; slow3200ms. Native editable ROM-direction projects use paired4tick frames, preserving8ticks per phase (approximately535.77ms cycle). GIF centiseconds cannot represent133.94ms phases exactly: normal ROM-direction phases use130/140/130/140ms,540ms cycle, with duplicate holds70/60/70/70/70/60/70/70ms. Slow is exactly4x those holds,2160ms cycle. Quantization is disclosed, not called emulator-perfect timing. All GIF headers and the preview distinguish normal/slow and the optional phase board.

## Checks, interpretation limits and review state

[First checkpoint report](first-checkpoint-checks.json) verifies all12 unique lower alpha masks and16 rigid pack/strap/composite cases. [Final independent-code checks](independent-checks.json) verify32 connected native Hero/dummy poses, binary alpha, palette budget, protected exact HR13 head pixels/neck occlusion, dummy eyes/hands, exact lower alpha and visible material-plane positions across12 unique walking poses, ten saved editable projects and28 independently decoded eight-frame GIFs. Exact holds, looping and nearest enlargement pass. [Actual Sprite Editor validation/export](editor-validation.json) validates ten native editable projects; large896×768 combined boards are derived exports from a validated224×192 project, without changing the editor canvas limit.

Visible material masks classify dark plane, slate shadow/light, warm gray, coral and pale band; their proof colors are diagrams. They establish image-plane boundaries only. Hidden knees, bones, anatomy under costume and numeric camera pitch remain inferred/occluded or unresolved. Retained upper body/head are Critz design and are not claimed to match the full reference silhouette. Owner sampled normal/slow browser playback in all four directions and inspected actual unique/all8 pixel sheets; discrete browser samples are not a continuous video capture or emulator test.

First checkpoint review verified lower alpha and canonical pack invariance and identified the corrected skin/material semantic defect. Final independent pixel review confirms the corrected lower alpha/material maps, no lower skin, eyes/hands, rigid pack/straps and directional timing. Its remaining request for common feet/contact registration is supplied in the separate guide and16 metadata records without changing sprite pixels. The guide was independently reviewed as honest/no extra geometry; the requested explicit legs occluded/inferred entry and label are complete and checked. Eutychus handles final Library export/download verification; no self-approval is implied by checks. No gameplay, save, map, editor UI, body variants, deployment or M1/M2 acceptance. Exact next action: Eutychus and read-only reviewer inspect stable corrected proofs before Library delivery; owner holds further art.
