# M1.HR11 — Reconstructed lower-garment overlap

**Implemented and checked; local structural critique received, awaiting parent visual judgment.** HR10 is structurally rejected. This revision reconstructs the lower torso/shorts/cuff occlusion rather than trimming stripes on its exposed calf/boot posts. HR9 head/ears/face/eye masks and every original rendered head pixel retain the existing P−2/A,C0 translations; no HEAD-detour adoption or new head revision. Same Black child identity, original coral/cream shirt, blue/navy shorts, slate daypack, dark sneakers and empty nose/mouth. Forward only; original proposed idle plus8×100ms A,A,P,P,C,C,P,P walk. No other directions, variants, UI, runtime replacement, deployment or TN4 work.

## Diagnosis and reconstruction

Source P remains one occupied interval `[7,25)` through native row56. HR10 splits at54, leaving three rows of unsupported separate posts. In source A/C, lower costume stays joined through57; HR10 splits at57 and turns the leading cluster into a narrow stub. The source's wider lower spans include clothing/cuffs/overlap, **not measured anatomical shoe width**.

HR11 draws compact sneakers behind cuffs, then the joined lower shorts over both. It removes exposed calf marks and the separately outlined rear shoe in strides. The shirt's lower hem and blue/navy shorts drape are reconstructed to allow the lower costume to overlap naturally. Cuffs supply the broad upper material spans; small shoe tips emerge only below them. No hidden knee or bone coordinate is inferred.

| Visible observation / authored region | Source P | HR11 P | Source A/C | HR11 A/C |
| --- | --- | --- | --- | --- |
| Lower-body costume bottom | Annotated56 | Shorts-mask bottom56 | Annotated57 | Shorts-mask bottom57 |
| Colored lower costume starts | Annotated55; cuff/shoe boundary uncertain | Visible cuff56; top authored cuff row55 is hidden by shorts | Annotated56; cuff/shoe boundary uncertain | Visible cuff56 |
| First separated lower alpha runs |57 |57 | No split into detached feet through57 | No split through57 |
| Definite pale shoe band / emerged shoe | Pale band58 | Shoe visible58–59; pale band58 | Pale band60 | Shoe visible60–61; pale band60 |
| Foot/costume last occupied row |59 |59 |61, source crop touches bottom |61 |
| Knee landmark | **UNRESOLVED / covered** | No knee coordinate | **UNRESOLVED / covered** | No knee coordinate |

Body/costume annotations are visible-region interpretations, not skeleton measurements. Source alpha intervals and pale-color rows are directly decoded facts. Candidate masks document authored parts/occlusion; matching them to annotations does not make hidden anatomy observable. Stride source clips at the original crop bottom, so uncropped extent/padding remains unknown. Shared `(16,64)` anchor and14top/2bottom reference registration are retained conventions, with no per-frame fitting. Proposed idle remains unobserved in source and uses the existing rest-height offset.

## Actual review artifacts

Repository contains original-only pixels and numeric observations:

- [Proposed idle and three unique poses, native plus4×](draft-poses.png)
- [All8 candidate frames, native plus4×](hero-all-eight-contact.png)
- [Native800ms walk](hero-forward-walk-native.gif) / [nearest4×](hero-forward-walk-4x.gif)
- [True32×64 light/dark800ms animation](hero-light-dark-native.gif)
- [Editable idle](../../../art/source/hero-forward-r11/hero-forward-idle.sprite.json) / [editable8-frame walk](../../../art/source/hero-forward-r11/hero-forward-walk.sprite.json)
- [All8 source alpha runs/annotations](reference-structure.json), [candidate material runs/occlusion/structural comparisons](structural-checks.json), [independent export/head checks](independent-checks.json), [actual Sprite Editor validation](editor-validation.json)

All reference-colored files are external, under `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr11-structure/`:

| File | Contents |
| --- | --- |
| `structural-native-grids.png` | Source / rejectedHR10 / HR11 actual colored lower-body grids, native row guides, visible-region annotations |
| `body-clusters-source-before-after.png` | Same three-way comparison at nearest8× without grid |
| `source-hero-all-eight-contact.png` | Every exact source/candidate frame,3× and true1× |
| `source-hero-native.gif` | True native actor pixels,8×100ms =800ms source-speed loop |
| `source-hero-4x.gif` | Exact nearest4× of the source-speed panel |
| `source-hero-SLOW4x-native.gif` | Identical pixels/order, distinctly labelled400ms/frame =3200ms slow loop |
| `source-hero-SLOW4x-4x.gif` | Exact nearest4× of labelled slow panel |
| `reference-material-runs.json` | Exact actual source RGBA runs for every inspected native row; source-colored encoding stays outside repo/build |

## Checks, critique and limits

All8 source frames are redecoded from the original hash-verified31726-byte GIF, SHA256 `5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e`. No stock sheet/static substitute. Native lower alpha intervals now match source exactly at P53–59 and A/C55–61, including the specific center-bridge/first-opening and compact tip contours. Candidate shorts-mask bottoms and visible shoe rows match the declared table. No exposed lower-leg skin cells or fabricated knee coordinate. **This fixes the early alpha-opening defect; it does not approve garment shape, color clusters or motion.**

Independent checks pass: exact PNG/editable-source pixels,15-color/binary alpha, connected poses, paired passing cuffs/shoes/arms, HR9 baseline file equality to9d1d159, exact HR9 head masks and translated rendered pixels, no nose/mouth, exact source comparison pixels. Seven decoded GIFs retain8frames/loop0/exact pixels. Five run100ms/frame; two labelled slow previews run400ms/frame. Nearest enlargements and native light/dark actor pixels are exact. Actual Sprite Editor validates seven preview projects and both editable projects. Editable6-tick holds approximate100.45623779296875ms; review GIF source speed remains exact100ms. No gameplay clock change.

Source/HR10/HR11 colored grids, clean lower-body plate, full three-pose/native/contact and browser samples of slow/source-speed playback were inspected. Sampled browser observations are not continuous motion capture. Local independent alpha-run critique confirms the P early-gap defect is corrected. **Residual visual concern:** blue/navy garment and cuff clusters still read heavier and more horizontal than the source's dark body/multicolor tips; the widened occluding shorts can read baggy. Original shirt/material contrast and retained head/upper-body remain unapproved. Exact silhouette rows are not beauty scores; no whole-body/feet/motion self-approval. Pixels are held stable after this structural pass for parent judgment; no automatic broader redesign.

Rebuild with bundled Pillow Python: `analyze-structure.py <external-folder>`, `build.py`, `prepare-review.py <external-folder>`, `structure-review.py <external-folder>`, `node encode-review.mjs <external-folder>/gif-jobs.json`, `verify.py <external-folder>`. The external folder is beside the preserved `brendan-user-reference-original` source directory. Source raster is read only by observation/comparison scripts; the body-authoring script draws original shapes/materials independently.

Work on main; source/push/artifact hashes recorded in `publication.json`. No playable-build change or Sites deployment. Exact next action: local relay delivers stable structural/contact/source-speed/slow proofs for parent judgment; owner holds further artwork.
