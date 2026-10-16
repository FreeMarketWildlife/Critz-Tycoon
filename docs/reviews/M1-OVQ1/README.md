# M1.OVQ1 — independent overnight cast review

Active: source/reference audit complete; new four-idle visual review pending. Scope is Girl Hero, Mom and Professor Nugget, read-only artwork review. No artwork authored, artist files edited, shared documentation changed, index staged, commit made or deployment performed. Root coordinates freezes and review gates. The playable build is unchanged by this review.

## Located design and canon

| Target | Canon and design files | Restraints |
| --- | --- | --- |
| Girl Hero | `docs/GAME_VISION.md` §2; `docs/ART_BIBLE.md` C6/R11; `docs/reviews/M1-C4/revision-11/girl-hero-concept.png`, `user-girl-design-reference.png`; existing `docs/reviews/M1-GH1/girl-front-idle.png`, `art/source/hero-girl-r1/` | Player-named ten-year-old Black child. Twin puffs/coral ties, coral/cream top, blue shorts, burgundy/cream shoes are selected appearance direction. Same body volume; no gender-based thinning. Selected generated concept is not native approval. |
| Mom | `docs/GAME_VISION.md` §3; `docs/ART_BIBLE.md` C6; `docs/reviews/M1-C2/mom-nugget-design-guide.png`, `docs/reviews/M1-C3/core-guides/mom-guide.png`; `assets/review/idle-collection-v1/mom.png` | Adult Black mother; loving, compassionate portrayal. Rounded natural hair/paired puffs, earrings, rose cardigan, cream top, navy trousers. Earlier guide's historical pixel budgets do not control current geometry. |
| Professor Nugget | `docs/GAME_VISION.md` §4; `docs/ART_BIBLE.md` C6; same C2 guide; `assets/review/idle-collection-v1/professor-nugget.png` | Adult herpetologist and mentor. Field hat, silver hair, glasses, cream field coat and green/sage shirt. No new biography or occupation. |

`docs/CHARACTER_FRAMEWORK.md` explicitly supersedes its historical 20×26/24×32 constraints with the 32×64 contract. `docs/character-study/ROSTER_QUEUE.md` is a historical/conditional queue; current direct overnight assignment authorizes these isolated candidates, not gameplay adoption. No local `.agents/` directory exists in this checkout.

## Actual reference evidence

`audit.py` reads source strips and exports numeric-only `reference-audit.json`. Source-bearing inputs and the actual inspected plate remain ignored in `local-review/overnight-cast-qa/`. Primary strips use palette index zero for transparency; default PNG alpha would count the background incorrectly. No emulator or frame-capture observation is claimed.

| Family | Actual pinned revision | Input |
| --- | --- | --- |
| Brendan, Man1 | `731ad5bfd6e6f265508d0efcca0ba42f9dcf5881` from `/tmp/ds1-primary-reference/source.json` | `/tmp/ds1-primary-reference/brendan-walking.png`, `man_1.png` |
| May, Mom, Birch | `5eff78649e7170a877b961ef0b3da13b81a16038`, downloaded exact raw URLs | `local-review/overnight-cast-qa/may-walking.png`, `mom.png`, `prof_birch.png` |

All three downloads match the existing 5eff measurement-ledger SHA256 values. The actual 731ad Brendan strip also matches the older 5eff ledger bytes; that equality does not relabel the entire repository revision. Man1 has only the stated 731ad evidence. Full hashes are in JSON. The network download initially failed sandbox DNS, then succeeded through the requested escalated command; no blocker remains.

All selected strips are indexed 144×32: nine 16×32 frames. Idle South is index0, North1, West2. Standard East mirrors West2. Original asymmetric Critz accessories require explicit physical-side reasoning; mirroring reference display does not approve blind mirroring of original parts. `primary-idles-native-6x.png` shows all five families at true native and exact 6× and was actually viewed. No sprite is fit to its own crop.

### Measurable anchors (source pixels, top-down, half-open bounds)

| Family | South / North bbox | West bbox | Final row | South/North contact x | West contact x |
| --- | --- | --- | --- | --- | --- |
| Brendan | [1,10,15,31] | [2,10,16,31] | 30 | 4–6 and 9–11 | 5–9 |
| Man1 | [1,11,15,31] | [2,11,14,31] | 30 | 4–6 and 9–11 | 5–9 |
| May | [1,11,15,31] | [2,11,16,31] | 30 | 5–6 and 9–10 | 5–9 |
| Mom | [0,11,16,31] | [2,11,14,31] | 30 | 5–6 and 9–10 | 6–8 |
| Birch | [0,11,16,31] | [2,11,16,31] | 30 | 4–6 and 9–11 | 6–10 |

The same feature doubles linearly for a 32×64 comparison. Keep the full-canvas ground edge (16,64) separate from final painted rows60–61. These are full visible garments/hat/hair and contact runs, not anatomical foot dimensions. Family-specific narrow contact patches do not override the current full-shoe-volume instruction.

## RD1 caveats and current construction anchors

Read `docs/reviews/M1-RD1/README.md`, `DIAGNOSIS.md`, `art/source/reference-dummy-r1/construction.json`, and actual `reference-derived-dummy.png`/region proof. Current source pin is `a25379df5c76fc1d4bf88c02525aef5affa4781c`. Actual original GIF SHA256 is `5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e`; frame2 left128×192 removes exact repeated4× display blocks to32×48, then translates +16Y. This is a passing pose, not an observed idle. The front fan GIF supplies no back/profile evidence.

RD1 retains all338 occupied source cells45+, face/ear36..45 and full shoes58+. Row47 [5,27), rows50..52 [3,29), waist54 [5,27), row61 contacts [9,13)+[19,23). Eyes x12..13/18..19,y38..41. These anchors are useful for candidate comparison; the new idle is an original pose adaptation, not automatically a pixel-exact fan idle.

Only the covered skull above36/crown25 is reconstructed. Internal torso/arm/hand/pelvis/leg boundaries and readability lines are proposed labels, currently awaiting manual corrections. Neither disjoint masks nor alpha-XOR0 proves those internal divisions are anatomically correct or visually approved. Keep candidate geometry and layer ownership editable.

## Actual visual findings and review targets

Viewed the original selected R11 girl image; native/4× fan frame2, RD1, GH1 front and C6 Mom/Nugget; and primary native/6× S/N/W/E plate.

- Primary front and back: crown/head dominates; shoulder band begins beneath the head. Rear hair/collar occlusion is compact, without a long visible neck or elongated torso. Coat width and hair can signal adult identity without taller shins.
- Primary profiles: forehead/eye/face project forward, ear/rear head connect, near sleeve/arm/hand descend continuously toward the hip. Avoid a two-pixel hand dot attached by a long thin line. A profile face outline must survive optional hair removal.
- Primary footwear: lower overlap forms a connected projected shoe mass; two separately visible anatomical feet are not mandatory in profile. Preserve the current full shoe envelope and consistent material hierarchy across directions. A bright horizontal rail or tiny exposed ankle/shoe replacement would fail the intended continuity.
- R11 Girl: distinct puff volumes and coral ties are essential; these cannot become a stretched cranium. Verify both visible eyes after fringe, rather than merely symmetric hidden masks.
- C6 Mom/Nugget: useful costume identity; their older native geometry is not current proportion approval. Nugget's glasses must retain readable eyes rather than a solid mask. Mom's cardigan must not become a rectangular long torso with thin hanging arms.
- Packs, if present: require torso-local rigid attachment and unchanged normalized raster under torso transform; static placement metadata alone is insufficient. No pack is required by these three identities.

New four-idle deliverables expected in `docs/reviews/M1-OGH1/`, `M1-OM1/`, `M1-ON1/`. For each, inspect true native plus exact enlargement and report direction-specific defects before root coordinates any walking. User retains appearance/M1 approval. No technical count substitutes for that gate.

## Reproduction and handoff

Run the bundled Python path with `docs/reviews/M1-OVQ1/audit.py`; requires Pillow. Audit asserts indexed dimensions and exact existing ledger hashes where applicable. Initial audit: all five files present, hashes verified, four directions measured each. No game tests needed for these read-only evidence files. Root owns selective commit/push coordination; this task must not stage other artists or parked edits.
