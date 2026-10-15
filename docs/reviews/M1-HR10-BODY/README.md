# M1.HR10-BODY — Focused cuff, shoe and hand-cluster trial

**One focused pass implemented/checked; awaiting local/parent visual judgment.** Base is HR9 source `9d1d1595329004829082ebe6fd44ea33208a3e06`, not the separate HEAD candidate. HR9 head/face/ears/eyes and rigid translations remain exact, including its original hair, Black child identity and empty nose/mouth. Forward only, same starter outfit, original proposed idle and eight-frame A,A,P,P,C,C,P,P walk. No runtime integration, directions, variants, UI, Library upload, Sites deployment or TN4 work.

The HEAD detour arose from a historical HR5 human instruction resurfaced through compaction; no newer authenticated head instruction was identified. Its `fb4a66b`/`e598fbc` commits remain preserved, unapproved and unadopted. [Verified chronology and scope reconciliation](scope-reconciliation.json). The resumed active task is this body-only pass.

## Concrete review paths

Original-only repository artifacts:

- [Proposed idle and three unique poses, native plus nearest4x](draft-poses.png)
- [All eight frames, native plus nearest4x](hero-all-eight-contact.png)
- [True32x64 sprites on light/dark, animated100ms](hero-light-dark-native.gif)
- [Native walk](hero-forward-walk-native.gif) / [nearest4x walk](hero-forward-walk-4x.gif): **8x100ms = 800ms**, source speed.
- [Editable idle](../../../art/source/hero-forward-r10-body/hero-forward-idle.sprite.json) / [editable walk](../../../art/source/hero-forward-r10-body/hero-forward-walk.sprite.json)
- [Independent decoded-pixel/timing/baseline checks](independent-checks.json)

Reference-containing files stay outside the repository/build, all under `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr10-body/`:

| Filename | Contents |
| --- | --- |
| `body-clusters-source-before-after.png` | Actual supplied source / HR9 / this candidate, fixed lower-body crop of all3 unique poses, nearest8x |
| `source-hero-all-eight-contact.png` | Every original source frame beside candidate,3x and true1x |
| `source-hero-native.gif` | Source and candidate at native sprite resolution,8x100ms,800ms cycle |
| `source-hero-4x.gif` | Exact nearest4x of that entire source-speed panel |
| `source-hero-SLOW4x-native.gif` | Separately labelled slow panel; true32x64 actors,8x400ms,3200ms cycle |
| `source-hero-SLOW4x-4x.gif` | Exact nearest4x of the labelled slow panel |

Slow panels bake **SLOW4x 400ms/frame** into every frame. They use identical source/candidate pixels and order; only preview delay changes. The original editor100ms approximation remains6ticks=100.45623779296875ms; this does not change gameplay clocks. Slow GIF delays are explicitly retimed to400ms by walking GIF blocks, preserving all8 duplicate frames without optimization/merging.

## What changed and what still fails

Passing cuff/ankle/shoe shapes now overlap diagonally, removing the full-width skin ring and separate shoe-top rail. Toes taper at contact instead of expanding into a wide second bar; dark sneaker material and original shorts stay distinct. Stride shoes narrow, with one subordinate overlapping rear cluster. Calves are not elongated. Hands use smaller rounded groups; sleeve edges are angled/overlapped instead of paired horizontal cuff bars. Cream/coral shirt clusters lose isolated accent runs and one full chest-border row, retaining the starter outfit.

**Residual criticism:** passing feet remain heavier/more boot-like than the source's compact integrated clusters. Repeated horizontal bands are reduced, not proven fully solved. The unchanged shoe area in P makes this a contour/overlap refinement, not a smaller-area shoe claim. Original blue cuffs/dark sneakers and outlined torso remain more graphic than the source costume; front-facing shirt shading is deliberately bilateral and does not establish final asymmetric lighting. The retained HR9 head and daypack are scope constraints, not newly approved. Source costume blocks cannot reveal hidden bones; actual stride reaches the original crop bottom, so uncropped anatomy remains unknown. No new anatomy is inferred. No artistic acceptance follows from mask counts or export checks.

The local relay's first-contact critique agrees horizontal bands are reduced and hands more compact, while retaining the boot-weight objection. No additional automatic redesign was requested. This is the single focused pass returned for judgment, not a claim that all mechanical-post defects are solved.

## Actual checks and inspection

All8 source frames are redecoded from the original hash-verified supplied GIF; derived reference frames use fixed14top/2bottom placement on32x64, never per-frame fitting. PNG/editor equality,15-color/binary alpha, connected poses, eye/source registration, paired passing anatomy and empty mouth/nose pass. HR9 source files match the pinned commit; all head masks match HR9 and every rendered original head pixel matches its documented translation. Shoe-mask areas P17→17 each, stride leading14→13 and trailing14→10, mirrored in C; no shoe area grows. These are technical measurements only.

All seven GIFs decode to exactly8 frames/loop0 and exact intended saved pixels. Five run100ms/frame; two labelled slow comparisons run400ms/frame. Enlargements are exact nearest4x. True native light/dark actor pixels and slow/source-speed actor pixels match exactly. Actual Sprite Editor validates seven preview projects and both editable native sources. Source/candidate all-frame, focused source/before/after and three unique pose plates were visually inspected; browser samples of source-speed and slow playback were also inspected. Sampled screenshots are not continuous video analysis. No game tests are claimed for these isolated review assets. Diff/whitespace checks run before commit.

Rebuild with bundled Pillow Python: `build.py`, `prepare-review.py <external-folder>`, `node encode-review.mjs <external-folder>/gif-jobs.json`, `verify.py <external-folder>`. The external folder must contain the eight registered reference PNGs from the pinned HR9 analysis; verifier rechecks them against the actual original GIF in the sibling `brendan-user-reference-original` directory. Reference pixels are never inputs to original body authoring.

Main branch. Source/push evidence and stable artifact hashes are recorded in `publication.json`. No playable-build change or deployment. Exact next action: relay returns these stable native/source-speed/slow comparisons for parent judgment; owner pauses further artwork.
