# M1.HR14 — Source-derived material contrast and visible foot landmarks

**Bounded material pass stable; overall Hero/dummy remain UNAPPROVED pending parent/user review.** The dummy had collapsed dark, shadow and accent planes into one purple mass. This pass restores distinct source-derived material contrast without adding or resizing a single silhouette pixel. Original Hero head/identity/hand sites and every lower pixel remain exact. A small front cream-to-coral recolor quiets the duplicated chest bars while retaining the collar, stripe and cuffs.

## Visible material evidence, not hidden anatomy

All six existing material classes now have distinct dummy diagram colors: dark plane/navy, shadow/purple, mid plane/blue, light plane/cyan, accent/orange and pale band/gold. These are **SOURCE-DERIVED PLANES / DIAGRAM COLORS**, not literal reference palette claims or leg/foot anatomical segmentation. Names in source metadata are Critz material slots; for example the light plane originates from a source green.

Only the front has a clear pale sole band: P58 x9–12 and19–22; A60 x17–20; C60 x11–14. North/west/east have **no pale sole**. Their near-tip colored accents are preserved separately, while black tips join black costume: the internal pants/shoe boundary remains ambiguous. No hidden calf, ankle, toe outline or bone length is filled in. Hidden hip/knee/ankle/anatomical-foot joints remain null/occluded.

The observed lowest painted **costume** contours match source, Hero and dummy exactly:

| View | A / C last contour | P last contour |
| --- | --- | --- |
| South | row61,4px each pose | row59, two4px spans |
| North | row63,6px each pose | row61, two6px spans |
| West/East | row63,4px each pose | row61,10px single costume mass; anatomical shoe split unresolved |

These widths are image-plane contours at the established2x comparison scale, not anatomical foot widths. Exact x spans, actual material-cell masks, pale/near-tip cue coordinates and uncertainty are in [material-landmark-checks.json](material-landmark-checks.json). The source's broad profileP mass was examined and measured, not silently narrowed or left as an unexplored foot-width assumption.

## Current native-art proofs

Reference-bearing files stay external at `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr14-review/`:

- `four-direction-material-source-hero-dummy.png`: each unique source/Hero/dummy at native/nearest4x; separate actual lower-material pixels and contact-cue overlay/key. **Every source/Hero/dummy has the invariant16,64 red crosshair and frame baseline.** Yellow marks observed front pale material, orange near-tip colored cues, gray ambiguous costume. The overlay is not an anatomy mask.
- `{direction}-all-eight-material-source-hero-dummy.png`: all8 holds at native/nearest3x, five registered columns: source/Hero/dummy/actual material pixels/contact cues. Each frame has explicit16,64 baseline/crosshair. Hidden leg/ankle/foot sites are labelled null; profileP is not labelled a10px anatomical foot.
- `chest-source-before-quiet.png`: source/before/current native/4x. Only12 Hero cells in A/C and20 in P/idle change cream to the existing coral color, below the protected head. Original collar/band/cuffs and alpha stay intact.
- Normal `source-hero-template-{direction}-{native,4x}.gif` and labelled `-SLOW4x-*`, plus the original all8 triptychs and pixel-boundary grids, are regenerated from current editable sources.
- Optional `four-direction-PHASE-source-hero-template-*` boards align phase indices on a common100ms clock; they are not ROM engine-timing playback.

Original-only [featured dummy](four-direction-featured-dummy-sheet.png), [common-feature/contact guide](four-direction-common-feature-registration.png), [idle/passing continuity](idle-walk-interface-continuity.png), [torso-registered pack](torso-registered-pack-all-eight.png), actual `material-plane-pixels-*` and `contact-cue-mask-*` masks live here. Eyes/hands and their guide cells remain exact; material maps never create extra bare hands.

## Chest and pack findings

The prior cream panel made two bright bars where the source torso is dark/red/green, with no pale chest patch. It was an original wardrobe choice, not reference-verified construction. The bounded recolor leaves a small cream collar and the original cream stripe/cuffs, reducing the bib-like highlight without changing size, head overlap, taper, arms or identity. Independent draft review found it quieter without gratuitous redesign.

The profile exception is **one extra column across two rows**, W x26/y48–49 in A/C, E x5; not a two-pixel horizontal extension. Actual composites show inward canonical bag neighbors and a compact attached vertical bag; no detached/cape island was found in phase/transition review. Canonical pack/strap RGBA, shape and torso-local transforms remain exact to2750f65. No pack geometry change was warranted. Full layers and actual visible occlusion are checked separately.

Passing taper and idle consistency remain protected: frontP51[4,28)→52[5,27)→53[7,25); actual Hero/dummy/body-layer idle50–55=P48–53 translated2px in all4views. Walking lower54–63/P53 and idle contacts56+ retain their literal geometry. Front idle is still a proposed/unobserved adaptation; no new hidden-anatomy claim is made.

## Complete rendered-cycle trace and its limits

Parent requested an isolated owned-page browser test. [rendered-cycle-trace.json](rendered-cycle-trace.json) analyzes actual Playwright screenshots of two live GIF image elements per direction (normal above slow), never canvas.drawImage or user-browser storage. All captured panel pixels match the exact current exported GIF hashes; zero unmatched/unpainted samples. Captured cyclic order is A→P→C→P→A, including every transition and return.

| Direction | Actual screenshots | Complete normal cycles | Complete slow cycles |
| --- | ---: | ---: | ---: |
| South |189|12|2|
| North |123|13|2|
| West |125|13|2|
| East |124|13|2|

First/last partial runs are excluded. Capture windows are approximately11.0s south and7.6s each other direction. Median sample gaps are50–66ms, maximum101ms; reported phase/cycle holds are midpoint estimates with measured sampling/capture tolerance, not frame-synchronous timing. Duplicate identical GIF slots cannot be visually distinguished: export decoding verifies all8 holds, while actual renders verify complete visible A/P/C/P cycles.

Actual captured phase contacts, all four transition-pair sets for every direction/normal/slow, raw captures and `actual-rendered-cycle-trace-{direction}.gif` playback are **external QA only**, not Library artwork. Capture-playback GIF pixels and quantized timing are independently decoded/RLE-checked. Owner inspected actual phase contacts/transition pairs; root reports inspecting all4normal/all4slow transition sets with no flare, clipping or detached pack observed. This closes the old screenshot-only coverage gap within **automated rendered trace plus visual transition review**. **It is not an uninterrupted human watch; zero human continuous-watch cycles are claimed.** Both full tutorial watches also remain incomplete.

Live native/4x normal/slow review: http://127.0.0.1:8771/preview.html . Parent owns server/session16570 and Chrome tab1219040667; writer handoff tab1219040675 may need reload. Browser-derived QA is kept separate from native-art Library deliverables; root alone handles version-guarded Library updates.

## Reference and validation

Supplied front GIF SHA256 `5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e`,8×100ms, A/A/P/P/C/C/P/P. Left128×192 exact4-grid reduced to32×48, fixed14top/2bottom32×64 comparison registration; front only. Pinned ROM directions use pret/pokeemerald `5eff78649e7170a877b961ef0b3da13b81a16038`; walking PNG SHA256 `f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1`, indexed0 transparency, exact2x32×64. N5/1/6/1, W7/2/8/2, E flippedW,8engine ticks/phase. [Source/table observations](reference-observations.json). Source inspection is not emulator observation.

Front normal/slow800/3200ms. ROM-direction GIF540/2160ms quantizes source-derived535.77ms loop; paired holds70/60/70/70/70/60/70/70ms normal,4x slow. Editable ROM frames use4ticks each,8ticks/phase. Full-frame anchor, painted contact and hidden bones remain separate.

[Independent-code checks](independent-checks.json), [material/landmark checks](material-landmark-checks.json), [interface checks](interface-checks.json) and [actual Sprite Editor validation](editor-validation.json) pass:32native poses, ten editable projects, all28decoded exportGIFs, exact alpha/heads/lowerHeroRGBA/material locations/actual hands/guide cells/pack layers, idleRGBA registration, loops/holds/nearest scaling, and current SHA-pinned render traces. Large phase boards are derived exports without changing editor limits.

Independent draft review passes the material read and source contour widths, chest refinement and protected geometry; final frozen construction-quality/user acceptance remains with root and the user. No current concrete alpha, taper, detached-pack, phase-order or unmatched-render defect was found. The unresolved black costume/shoe anatomy is a limit of the evidence, not permission to invent a boundary.

Main only; no game/runtime/save/deployment/roster changes. Parked HR11 edits/assets, parent study sections and unrelated root work are preserved. Earlier row53-only proofs, prior Library receipt and old Chrome sample report remain historical. Exact next action: root verifies frozen current artifact hashes and handles Library versions/review; sole writer holds further art.

## Current Library material checkpoint

[Current26-file receipt, exact IDs/versions and download checks](library-material-review-receipt.json) supersedes the historical version0 interface receipt. Nineteen existing files updated to version1 with guards; unchangedpack remains version0; six new native-art contact/chest proofs are version0. All26downloadbytes/pixels exact,14eight-frame GIFs preserve holds/loop0,12PNG proofs exact. Earlier Library versions remain in history. No browser captures were uploaded.

[Combined anchored material/cue sheet](https://chatgpt.com/api/library/files/libfile_9028a359e8988191abb484b0d26f88a4/download) · [South all8](https://chatgpt.com/api/library/files/libfile_f2215fd24d2081919ef32d2736b48276/download) · [North all8](https://chatgpt.com/api/library/files/libfile_caea0e874e108191ae159d7ae04823e1/download) · [West all8](https://chatgpt.com/api/library/files/libfile_41616e65df088191b79796fe800bb7e9/download) · [East all8](https://chatgpt.com/api/library/files/libfile_8a8431dac81c8191ab475f365f428082/download) · [Quieter chest comparison](https://chatgpt.com/api/library/files/libfile_054417e753dc8191802b614c4e27c5f2/download). Existing normal/slow/native loop IDs now serve version1.

Final independent frozen construction review atd5dc458 correlates48publicationhashes/source/trace and all26Librarydownloads; no further concrete blocker in the requested scope. Root inspected every captured normal/slow transition set as well. The result supports the user-authorized review-only progression to the existing GirlHero candidate; no broader M1/userappearance/runtime acceptance or new roster expansion. Hidden leg/ankle/foot anatomy remains unmeasured; source-derived material/contact evidence is explicitly separate. Trace tolerance147–161ms and no uninterrupted human-watch claim remain visible. No deployment.
