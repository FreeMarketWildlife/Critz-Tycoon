# M1.HR12 — Backpack, ear layering, shoe spur and construction template

**Implemented and checked; awaiting independent/user visual review.** Direct user authorization in this chat permits Eutychus's correction handoff and continuation. Eutychus explicitly selects the latest delivered HR10-BODY source `d158c3ecceaddaf1a0919f01ef75eac47f367cc5` as the best-supported base. The exact shared image Phil viewed remains unverified; this is an explicit base choice, not a claim he saw HR11. HR11 is unshared, preserved and unadopted. No further proportion/head/hair restyling.

## Concrete deliverables

Original-only repository files:

- [Hero and neutral mannequin,4× and native](hero-and-mannequin.png)
- [Bounded ears/pack/shoe before-after](bounded-before-after.png)
- [Labelled allpose anatomy contact](anatomy-contact.png): arms, legs, torso, feet, ears, shoulder/elbow/hip/knee/ankle sites. Hidden joint sites are explicitly **PROPOSED**, not reference-measured anatomy.
- [Fixed registered outfit/scaffold overlay](outfit-registration.png): ear seam, strap anchors, pack root and joint sites. P/idle pack root is hidden behind the body.
- [Native Hero GIF](hero-native.gif), [exact nearest4× Hero GIF](hero-4x.gif), [native neutral mannequin GIF](mannequin-native.gif)
- [Editable Hero idle](../../../art/source/hero-forward-r12/hero-forward-idle.sprite.json), [editable8-frame walk](../../../art/source/hero-forward-r12/hero-forward-walk.sprite.json), [editable mannequin](../../../art/source/hero-forward-r12/mannequin.sprite.json), [proposed scaffold/attachment map](../../../art/source/hero-forward-r12/scaffold.json)
- [Independent saved-pixel/attachment/export checks](independent-checks.json), [actual Sprite Editor validation](editor-validation.json), [bounded edit log](bounded-edits.json)

Reference-containing comparisons remain outside repository/build under `/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr12-review/`:

| File | Contents |
| --- | --- |
| `source-hero-mannequin-all-eight.png` | All8 source/Hero/dummy triples, nearest3× and true native |
| `source-hero-mannequin-native.gif` | Native32×64 actors on contrasting checker,8×100ms =800ms cycle |
| `source-hero-mannequin-4x.gif` | Exact nearest4× of the complete native panel |
| `source-hero-mannequin-SLOW4x-native.gif` | Same actor pixels/order; baked **SLOW4x400ms** label,8×400ms =3200ms cycle |
| `source-hero-mannequin-SLOW4x-4x.gif` | Exact nearest4× of labelled slow panel |

Columns use the same32×64 frame and declared ground registration. REF is the confirmed supplied left Brendan redraw, HERO is corrected HR10-BODY, DUMMY is an abstract featureless segmented construction diagram. Its head has no facial features; body parts use categorical colors and mechanical joint dots, not literal unclothed-child anatomy. The source has no observed idle; the existing original idle remains labelled proposed. No new directions, body types, customization UI, live replacement, deployment or TN4 work.

## Bounded corrections

**Ears:** inherited anatomy masks were paired, but the final right cheek covered its ear separator. At rest, left x6/rows37–40 was dark outline while right x25 was skin; inner ear highlights also differed. The saved visible3×5 left ear/separator patch is now mirrored to the right, with the existing head translation applied per pose. Final rendered RGBA patches match, beyond mask/bounds symmetry. Only five head-color cells change; alpha, hair, eyes, face center and all other original head pixels stay exact. No mouth or nose added.

**Backpack:** rebuild the slate side pack within its existing region as a shorter rounded/flapped volume. Visible pack-to-shoulder straps have an explicit connected chain through the shoulder onto the chest; front P/idle shows paired straps while the bag remains behind the torso. The shoulder strap may cover its bounded upper-arm attachment. No body silhouette/proportion restyle. The actual chain is checked in rendered colors, not inferred merely from opaque body pixels.

**Shoe:** remove the single-neighbor protrusion at A`(16,60)` and C`(15,60)` only. Every other lower-body pixel from row51 down stays exact to HR10-BODY. The broader HR11 occlusion reconstruction is not adopted.

**Template:** separate editable original mannequin and per-pose joint/part/ear/strap/pack attachment map. L/R means viewer sides for these forward poses; C swaps limb keys after mirroring so names stay on consistent viewer sides. Hidden skull/joint contours are authored construction proposals, not decoded anatomy. Hero remains unchanged when the template is displayed. No body variants or actual customization system is implemented, and this draft does not freeze future anatomical guides without review.

## Actual checks and remaining judgment

The HR10 source matches the pinned source commit. Independent checks pass for exact PNG/editable-source equality,15-color/binary-alpha connected Hero poses, connected neutral mannequin, bounded edit rectangles, mirrored final ear RGBA, protected head/ear geometry masks, no nose/mouth, all original head pixels outside the ear patch, exact lower body except spur, actual one-neighbor spur removal, visible strap chain and scaffold attachment sites inside the saved Hero. Mannequin head/ear raster remains stable across opposed poses; all hidden joints stay labelled proposed.

Seven GIFs independently decode to8 frames/loop0/exact saved pixels. Five use100ms holds; two labelled slow panels use400ms holds. All three actors retain exact opaque native pixels in both panels; nearest4× panels are exact. Actual Sprite Editor validates seven preview projects plus Hero idle/walk/mannequin projects. Editable6ticks approximates100.45623779296875ms; GIF source speed is exact100ms. No gameplay clock change.

Native/enlarged before-after, all8triple contact, labelled anatomy and registered overlay were visually inspected. Browser samples of slow/source-speed triples were inspected; sampled views are not continuous motion capture. A clipped last-column label was caught and corrected before the stable export. No full-game tests are claimed for isolated review assets.

Remaining visual judgment: the pack is tiny at native scale and needs Eutychus/Phil to judge its read as an attached backpack; straps change a small part of the cream/coral chest. The mannequin is a mechanical construction aid, not final character art or recovered hidden anatomy. Existing HR10 limb weight/proportions are deliberately preserved per the new direction. No whole-base/motion/scaffold acceptance is inferred from technical checks.

Workflow: read the imagegen skill; it explicitly excludes small project-local edits with an existing editable native source and simple diagrams. This task therefore uses the existing native Python sprite source and a code-authored diagram, preserving protected cells deterministically. No image-generation tool/API or fallback was used. Rebuild with bundled Pillow Python: `build.py`, `scaffold.py`, `prepare-review.py <external-folder>`, `node encode-review.mjs <external-folder>/gif-jobs.json`, `verify.py <external-folder>`. The hash-pinned original GIF is in the sibling `brendan-user-reference-original` directory. Source pixels are only read by comparison tools, never native Hero authoring.

Work on main; only completed HR12 files and its shared-doc sections are staged. Existing HR11 source/review and prior shared-doc changes stay unstaged; its preexisting document diff is preserved externally as `parked-HR11-docs.patch`. Unrelated Tanoshi recovery35df869 is preserved. Source/push and artifact hashes are in `publication.json`. Playable build unchanged; no Sites deployment. Exact next action: Eutychus independently reviews the stable triples, anatomy contact, ear seam and pack attachment; root handles Library delivery. No owner cross-chat message/export performed.
