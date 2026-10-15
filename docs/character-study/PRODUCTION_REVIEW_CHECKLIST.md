# Character production review checklist

**Proposed review method, not a new art specification.** Use the latest [canonical character contract](../ART_BIBLE.md#emerald-2-visual-contract--authoritative-2026-10-02), [HR14 correction](../ART_BIBLE.md#source-visible-lower-construction-and-torso-local-pack--m1hr14), [review presentation rules](../ART_BIBLE.md#character-review-grid--default-presentation-honor-explicit-overrides) and [contact rules](../ART_BIBLE.md#transition-tile-contact-study--m1ct1-user-correction). Latest user instructions control conflicts. Do not copy historical framework dimensions into a new standard.

## Before review

- Record task/revision, exact source and export hashes, reviewer, time and scope. Preserve the prior rejected revision for comparison.
- Pin the reference file/revision and explain registration, transparency and phase mapping. Keep source-derived facts, original adaptations and unresolved anatomy labelled separately.
- Export native transparent poses, editable sources and exact nearest enlargement. Keep reference-colored material outside the repository/build under the established policy.
- State whether playback is source timing, quantized export, labelled slow or phase-index comparison. Record the duration actually decoded, not an assumed nominal FPS.

## Still and per-pose inspection

- Inspect every direction and distinct pose side by side at invariant registration. Compare silhouette, crown, visible face/eye line, shoulders, hands, head-over-torso overlap and observed ground-contact contours. Do not independently fit each pose to hide drift.
- Check eyes and hands on the final composite, including deliberate back/profile occlusion. Confirm the default face has no accidental mouth/nose mark under current Hero direction.
- Distinguish hair/headwear from skull, costume planes from anatomical skin, and painted contact from hidden joints. Leave unobserved bones unresolved. Do not invent camera degrees or skeletal ratios.
- Check connected, readable contour clusters and garment overlaps. Reject accidental isolated pixels, clipping, overly heavy shoes, exposed invented legs, proportion drift and flattening of the established elevated projection.
- Inspect pack/straps as a torso-attached unit, then inspect their actual visible occlusion. A matching hidden mask does not prove the final visible shape is correct.
- Review native game-scale appearance on relevant backgrounds, then nearest enlargement for pixel diagnosis. Pixel refinement must not grow feet/legs or restyle protected identity without a reviewed reason.
- Review Hero and dummy independently. Confirm dummy annotations describe visible evidence honestly; do not add anatomical geometry solely to fill an annotation slot.

## Motion inspection

- Actually watch complete repeated cycles in each direction at native scale and exact nearest enlargement, with a fixed world anchor. Log number of observed cycles, actual duration and playback method.
- Separate intended whole-body bob from sideways drift, accessory sway, contour flicker and slipping contacts. Watch contact-to-passing transitions, alternating overlap and the return to the first frame.
- Watch normal timing first and explicitly labelled slow timing for diagnosis. Slow motion and a common-clock phase board cannot establish native cadence.
- Retain every unique phase/all-frame plate to locate defects, while recording that static inspection alone does not complete motion review.

## Context and technical checks

- Test scene sorting, counter overlap and door approach separately from sprite canvas/painted bounds and explicit collision/ground footprint. Apply canonical contact rules in both axes and independent renderers where relevant.
- Reopen editable files and decode exported PNG/GIF pixels. Verify source/export equality, alpha, palette/registration, phase order, duration, loop and exact nearest scaling under the current Bible contract.
- Use isolated contexts and synthetic saves for gameplay checks. Record device/browser limits honestly.
- Repeated passing test counts cannot substitute for an artist's actual viewing or the user's acceptance.

## Decision and correction record

Each failure needs a concrete visible symptom, exact affected direction/pose/transition, evidence path, bounded fix and recheck. Mark unperformed checks **pending**, unavailable evidence **blocked**, and failed art **failed**. Do not label “all passed” when playback, native inspection or a material concern remains unreviewed.

Use this appendable result form:

```text
Revision / source SHA / export hashes:
Reviewer / timestamp:
Reference / registration / clock:
Native still review: pending | pass | fail — evidence and limits
Enlarged pose review: pending | pass | fail — evidence and limits
Actual normal playback: pending | pass | fail — directions, cycles, method
Actual slow playback: pending | pass | fail — directions, cycles, method
Hero result: pending | pass | fail — unresolved defects
Reusable dummy result: pending | pass | fail — unresolved defects
Context/contact result: pending | pass | fail | outside this review — scope
Technical checks: actual commands/reports and results
Defect / bounded fix / recheck:
User visual response: pending | exact quoted scope + source
Next action / owner:
Publication: not attempted | exact commit/push/deployment evidence
```

Only move to the next existing character when **both Hero and reusable dummy** have the rigorous visual pass required by the latest authorization. Such a local pass is not broader M1/M2 approval or permission to promote unapproved art into gameplay. Final user acceptance remains with the user.
