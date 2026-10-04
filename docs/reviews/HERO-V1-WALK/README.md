# M1.C5 — Official Hero Boy V1 and front-walk GIF

**Hero Boy V1 still is user-approved. The new walk is delivered for animation review.** The user declared their editor-corrected still perfect, explicitly requested it be logged as official V1, then supplied the exact RLE. That is approval of this supplied still, not of earlier assistant revisions or unseen animation.

- [Official V1 still PNG](../../../assets/characters/hero-boy-v1/idle-south.png)
- [Native transparent walking GIF — 32×64](../../../assets/review/hero-boy-v1-walk/walk-native.gif)
- [6× walking preview — neutral background](../../../assets/review/hero-boy-v1-walk/walk-preview-6x.gif)
- [Four-frame native sheet](../../../assets/review/hero-boy-v1-walk/walk-sheet.png)
- [Editable walk project](../../../art/source/hero-boy-v1/walk.sprite.json) · [Exact RLE](../../../art/source/hero-boy-v1/walk.rle.json)
- [Complete asset pack](hero-boy-v1.zip)

## Preserve the official still

`art/source/hero-boy-v1/user-approved.rle.json` is a byte-for-byte copy of the supplied export. Source SHA-256: `bef3289d8d62801ea2f223ae9359beb305856764a54afed8fe9990f42676fb3a`. A build guard rejects a changed approved input; later user corrections must create a new version instead of silently modifying V1.

The official PNG exactly decodes all 2,048 source cells: 32×64 frame, 757 occupied cells, 14 used opaque colors, bounds `[3,25,29,62]`, anchor `[16,64]`, two empty bottom rows. The full source palette and every color/index are preserved, including unused slots. PNG SHA-256: `0099dd331ae2c2d995663328e52763e8b10b1df0d36854d59676ee0ac52f7883`. Stable asset ID `hero.boy.v1.idle.south`; approval and both source/pixel hashes are in the [official manifest](../../../assets/characters/hero-boy-v1/manifest.json).

This input supersedes prior Hero review drafts. Do not repaint it to match old outline, palette, generic-chibi or symmetry assumptions. Approval belongs to the user's actual pixels. The approved still is registered as an asset; it is not automatically integrated into the existing playable renderer.

## Emerald study and motion adaptation

Inspected the native Brendan walking sheet at pinned pret/pokeemerald revision `5eff78649e7170a877b961ef0b3da13b81a16038`. Downloaded reference SHA-256 matches the established ledger: `f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1`. Reference pixels and the three-pose inspection plate stay outside the project. This is native-source inspection, not emulator footage.

The [south-walk source table](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/data/object_events/object_event_anims.h#L191-L199) uses frame indices **3 → 0 → 4 → 0**, eight updates each. [Native sheet](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/brendan/walking.png). The reference's stride poses lower the head, alternate a forward foot with the opposing forward arm, and tuck the rear foot under the compact torso. The character is not simply translated or flipped as a whole.

| Landmark | Inspected Emerald idle → stride | Hero at 2× |
| --- | --- | --- |
| Topmost headwear pixel | Native row10 → 11 | Relative head movement +2px; Hero hair row25 → 27 |
| Eye rows | 19–20 → 20–21 | User eyes38–41 → 40–43 |
| Bottom foot row | 30 → 31 | 61 → 63 |
| Frontmost shoe X, alternating strides | Around x8–10 / x5–7 | Original Hero shoes move inward 2px and alternate sides |
| Walk hold | 8 source updates | 8 ticks at 16.742706ms/tick |

Hero's stride head/hair/face is copied without recoloring or mirroring, shifted down two native pixels. The source shirt clusters bob with it. Arms move in opposition to the leading foot; the rear arm rises behind the head and receives an existing skin-shadow color. The rear leg tucks inward/up behind the pelvis; the forward leg/shoe moves inward/down. The compact pelvis is separately posed to connect the legs. Original clothing shapes and colors remain Critz artwork, not copied Brendan pixels. Hair asymmetry stays on the same side throughout.

The four displayed poses are **stride A → exact V1 → stride B → exact V1**. Only a front-facing walk in place is included. No side/back/run frames, world translation, new controller behavior or emulator-equivalence claim. Front/back idle bilateral geometry does not require each walking stride to be symmetric.

## GIF export and checks

Both GIFs loop indefinitely, with four frames and holds **130 / 140 / 130 / 140 ms**. GIF has 10ms time units: the resulting 540ms loop is 4.233ms longer than the 535.7666ms source cycle (under 0.8%). Editable projects/metadata retain the exact 8/8/8/8 tick timing. Native GIF transparency is preserved; the 6× proof duplicates each cell exactly and composites it on neutral `#eee9df` solely for visibility. No palette quantization, interpolation or blur.

Independent decoded-output checks validate the official still, all four source/PNG frames, both exact idle returns, head/hair translation, connected silhouettes, foot extents, genuine limb changes rather than a whole-sprite shift, both GIF loops/delays and every decoded GIF pixel. **2,048 approved-still cells, 8,192 pose cells and 303,104 GIF cells** pass. This also verifies that disposal clears prior frames without trails. [Validation](validation.json). All unique poses were visually inspected at native and integer-enlarged scale. Technical checks do not self-approve animation quality.

Rebuild with Node/Sharp (`CODEX_PRIMARY_RUNTIME_NODE_MODULES`) and verify with Python/Pillow:

```sh
node art/source/hero-boy-v1/build.mjs
python3 docs/reviews/HERO-V1-WALK/verify.py
```

No runtime source, saved progress or accepted playable atlas changed. No website deployment is required for this asset/GIF delivery. Unrelated edits remain preserved. Commit/push evidence is in PROJECT_STATUS. **Next action:** user reviews the front walk; retain V1 still unchanged during any animation refinement.
