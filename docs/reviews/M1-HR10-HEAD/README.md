# M1.HR10H — Forward head overlay correction

**Implemented and checked; awaiting user visual review.** Original-only assets remain outside accepted gameplay. This checkpoint answers the direct head-overlay request visible in this conversation. A subsequent coordination note requests a separate HR10 body-only pass and disputes chronology. This head draft uses its own `M1-HR10-HEAD` / `hero-head-overlay-r10` namespace so it cannot masquerade as that body deliverable. No head/body/motion approval is inferred.

The first attempted broader hair draft increased the upper-head mismatch and was rejected locally. The saved candidate narrows the upper sweep, removes the isolated high spike and simplifies the interior into connected color masses. Existing rounded ears, eyes, underlying face layers, empty nose/mouth, outfit, body, ground registration and walk translations are protected. Only the union of old/new hair regions changes. No profile, rear, variant or customization work is included.

## Concrete review

- [Original-only before/after, 4x and native light/dark](head-before-after.png)
- [All eight saved candidate frames](hero-all-eight-contact.png)
- [800 ms native walk](hero-forward-walk-native.gif), [exact nearest 4x](hero-forward-walk-4x.gif)
- [Editable idle](../../../art/source/hero-head-overlay-r10/hero-forward-idle.sprite.json), [editable eight-frame walk](../../../art/source/hero-head-overlay-r10/hero-forward-walk.sprite.json)
- [Independent checks](independent-checks.json), [row-by-row overlay evidence](overlay-evidence.json)

Reference-colored overlays are outside the repository/build:

- `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr10-head/head-overlay-before-after.png`: supplied custom Brendan redraw, stride and passing, current before/after and actual 50% superpositions.
- `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr10-head/emerald-head-overlay.png`: pinned Emerald south idle at exact 2x, same full-frame registration and actual before/after superpositions.
- `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr10-head/source-hero-all-eight-contact.png`
- `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr10-head/source-hero-native.gif` and `source-hero-4x.gif`: synchronized 8x100 ms, 800 ms loop.

All overlays use full 32x64 frames with no independent sprite fitting. The custom animation uses its existing fixed 14px top padding; pinned Emerald uses exact native 2x. These are different sources/poses, separately labeled. Neither hat contour measures a hidden skull.

## Evidence and residual critique

In the custom reference head crop, stride silhouette extra/missing cells change 33/16 to 4/24; passing changes 34/25 to 7/35. The sum decreases, but missing cells increase. This locates contour changes; it does not prove artistic equivalence. Original hair, small rounded ears and cap occlusion intentionally differ. The preserved face and fringe still need visual judgment. Body cuff/shoe weight is unchanged and unresolved; this checkpoint does not satisfy the separately requested body-only refinement.

Independent checks pass for exact editable-source/PNG equality, 15-color binary alpha, connected silhouettes, unchanged face/ear/eye masks, no nose/mouth, every changed pixel within the authored hair union, protected body, unchanged three-pose/eight-frame sequence, four decoded GIFs with exact saved pixels/nearest scaling/100 ms delays/loop0. Original HR6 masks omitted some outline raster cells; the independent protection check reconstructs the old polygon plus line from the authored coordinates rather than silently broadening the allowed area. Actual Sprite Editor validation passes for both editable projects and four preview projects. No full-game tests or deployment are needed for isolated review assets.

Rebuild with the bundled Pillow Python: run `head.py`, `build.py`, `review.py <external-folder>`, `prepare-review.py <external-folder>`, encode `gif-jobs.json` with the Sprite Editor `validateProject`/`gifBytes`, then `verify.py <external-folder>`. External source locations and hash assertions are explicit in the review scripts. Source originals remain untouched.

Work is on `main`. Commit/push verification is recorded in `publication.json`. Playable build unchanged; no Sites deployment. Exact next action: user evaluates the actual head overlay; broader approval and the independent body checkpoint remain pending.
