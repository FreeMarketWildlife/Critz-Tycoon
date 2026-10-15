# HR14 existing-frame rotation and synchronized phase review

Review visualization only, 2026-10-15. No original frame, editable character source, runtime asset or save was changed. All 32 input PNGs are byte-exact to material source `c98a8cbd8d85e160e9080d6690964c3c3deb3ef1`, frozen by receipt `d5dc45838c1ee5bc4ea9f402e73edd2e8ebcce87`. [Composition checks](composition-checks.json) and [Library verification](library-receipt.json) pin every input/output.

## Layout and clocks

Each character retains its full 32×64 frame, fixed edge anchor `(16,64)` and source pixels. Markers sit outside the source rectangles. Neutral rotation is South → West → North → East, 500ms per orientation, 2000ms total. Hero is left, dummy right. This is an inspection sequence, not a new authored turning animation.

The gait boards have S/N/W/E columns, Hero above dummy. They synchronize the existing A/A/P/P/C/C/P/P slots on a common 100ms clock, 800ms total. The labelled slow version uses 400ms slots, 3200ms total. **These are phase comparisons, not native ROM cadence.** Duplicate identical holds coalesce in GIF encoding; decoded visible pixels and total holds match the requested schedule exactly. No interpolation or invented in-between pose was added.

The unique-phase contact sheet has S/N/W/E rows and six columns: Hero A/P/C, then dummy A/P/C. Native and nearest 4× versions use identical registration. The idle sheet has Hero and dummy rows and S/N/W/E columns.

## Actual inspection and limits

Root viewed the native and 4× idle plates, all 12 distinct Hero/dummy gait pairs, and the existing external source/Hero/dummy material/contact sheet. Thus reference comparisons include actual source pixels, not just metadata. Reference artwork was not copied into these new Library previews.

The local browser successfully rendered the new GIFs. Three actual screenshots sampled rotation, normal-phase and labelled-slow playback, including an east rotation view and differing walking poses. These are rendered samples, **not uninterrupted viewing**. Zero continuous full-watch cycles are claimed. Frame-by-frame findings below cover all views/unique poses; new full continuous rotation/gait visual acceptance remains pending. Earlier HR14 automated rendered-cycle coverage is separate evidence, not rerun or expanded here.

## Visual findings

| Check | Observed result and implication |
| --- | --- |
| Head/torso overlap | In all four idles and A/P/C views, the face/head overlaps the upper shirt without a free-standing skin neck column. Dummy profile collar notches remain costume/occlusion cues, not measured neck bones. No new gap or independent head displacement found. |
| Scale and rotation | Hair creates the Hero's irregular crown; the dummy is a plain construction head. Their different crown silhouettes are deliberate material/design distinctions. All idle top bounds are row21 and last painted contact is row61. No idle ground jump found. Profile/back costume and pack look wider than the front, but no per-view resizing or fitted canvas masks that difference. |
| Bob and phase coordination | A/C torso registration is `(16,48)` and P is `(16,46)`, a two-row vertical passing displacement in every view. Hero and dummy corresponding phases agree; opposed strides exchange the visible forward/trailing costume masses. No independent sideways head bob was identified in the distinct-pose plates or rendered samples. These observations do not establish source-speed cadence. |
| Shoulder/hand path | Upper hand sites exchange sides with A/C and are readable in the dummy; back-facing eyes are correctly absent. Profile hands remain upper costume-adjacent clusters rather than the colored lower accents. However, Hero front wrists are visually busy: cream/red cloth surrounds small brown skin clusters at native scale. This is a specific material-read concern, below. |
| Contact and compact stride | Frame anchor stays `(16,64)` throughout. South A/C last painted row61; P59. N/W/E A/C63; P61. All idles61. These are visible costume contours, not anatomical foot contact coordinates. Front lowest stride span is4px; rear6px; profile stride4px. Profile P is one joined10px dark costume mass, also present in the inspected source. It reads broad/square, but the evidence does not justify carving a shoe split or narrowing it as an anatomical correction. |
| Pack/strap alignment | The back pack stays centered and moves with torso bob; profile pack stays at the rear edge through A/P/C and remains connected. No detached cape island or lateral pose-to-pose jump was found. The already disclosed profile A/C exception remains one extra column over two rows (W x26 / E x5, y48–49), not a new two-pixel sideways swing. |
| Dummy versus Hero | Dummy material planes reveal the lower overlap more clearly than Hero's dark costume. They do not expose hidden hip/knee/ankle bones. Both must retain separate visual judgments; exact silhouette or export checks do not approve either artwork. |

### Specific correction recommendation

Before final Hero appearance acceptance, perform a **bounded front hand/cuff material-ownership correction or clarification**, using the selected brown complexion and clean readable hands. In the outer wrist audit region x3–9 and22–28, y47–53, the current Hero has 12 skin-ramp cells surrounded by 15 cream and seven muted cloth-highlight cells. At native size those pale/red rings compete with the skin read, the same class of issue already corrected in GH1. Do not blindly repaint every pale cell or invent arm anatomy: separate actual exposed skin, sleeve trim and clothing highlights, then simplify the ambiguous wrist material while protecting alpha, head, lower contacts and original costume identity. This is a documented recommendation only; no writer message or correction was performed.

No new geometric correction to feet, stride, head placement or pack is established by this review. Broad profile costume remains an appearance question requiring judgment in complete motion, not a hidden-foot measurement. Overall visual acceptance and runtime promotion remain open.

## Native Library previews

- [Turn in place · native](https://chatgpt.com/api/library/files/libfile_49255296fb388191aa631fbef101b88c/download) · [nearest 4×](https://chatgpt.com/api/library/files/libfile_e088333253488191842bfd9c26d31309/download)
- [Synchronized phase · native](https://chatgpt.com/api/library/files/libfile_9cf56acdcab081919facd35975864287/download) · [nearest 4×](https://chatgpt.com/api/library/files/libfile_8d68c152a1d481919a781bb5d94d4428/download)
- [Labelled slow phase · native](https://chatgpt.com/api/library/files/libfile_8f327d14675481918311f7d338524356/download) · [nearest 4×](https://chatgpt.com/api/library/files/libfile_cb607ee42480819194ac164160a9d9df/download)
- [Idle directions · native](https://chatgpt.com/api/library/files/libfile_ddbe314092388191b0b34dbf9affebba/download) · [nearest 4×](https://chatgpt.com/api/library/files/libfile_510ec6b661408191a2328463b437d70d/download)
- [All unique phases · native](https://chatgpt.com/api/library/files/libfile_5923e5099bd88191bcbc6e9e040ee960/download) · [nearest 4×](https://chatgpt.com/api/library/files/libfile_e08acd3b13288191a6a7360162fb0f1a/download)

All ten files are version0 and match downloaded bytes, dimensions, every RGBA frame and GIF holds/loop. These are source-derived review compositions, not browser screenshots. The original frames and parked edits remain untouched. No Girl directions, denied-scope messages, runtime change or deployment. Next: parent inspects these previews; decide on the specific hand/cuff concern and complete continuous playback judgment without inferring permission to create new assets.
