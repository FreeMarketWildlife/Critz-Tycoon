# M1.TN2 native asset checkpoint

New appearances await the user's native/playable review. Technical checks do not approve artwork. These files adapt four completed imagegen outputs; there were no additional generation jobs and no procedural silhouette or eye edits.

The [native comparison](native.png), [light 8×](clean-light-8x.png), [dark 8×](clean-dark-8x.png) and [countable 8× grid](grid-8x.png) show tiny blush, small mint, the unchanged accepted regular Apricot, and large lilac in that order. Every family member occupies a 32×32 frame at the same native pixel density, bottom-center anchor `(16,32)`, with rows30/31 transparent.

| New atlas ID | Painted bounds | Painted extent | Occupied pixels | Opaque colors | Enclosed face transparency, 8-neighbor |
| --- | --- | --- | --- | --- | --- |
| `tiny-blush` | `[8,12,24,30]` | 16×18 | 150 | 3 | Two 1×2 holes |
| `small-mint` | `[6,8,26,30]` | 20×22 | 228 | 3 | Left 1×2; right 1×1 |
| `large-lilac` | `[1,0,31,30]` | 30×30 | 461 | 3 | Two 2×3 envelopes, five transparent pixels each |

Bounds are top-left, Y-down, right/bottom exclusive. The large individual's separate two-pixel body/tail cutout is preserved and is not counted as an eye. The tiny notch is open under eight-neighbor transparency. All occupied pixels in each native variant form one eight-connected component: sampling lets ray tips meet the head at native diagonals. Four disconnected native rays are not claimed. Connected body/arm/foot/tail anatomy is preserved without code drawing.

The mint crop adds ten **source** pixels of transparent margin on the left. Tight-bounds sampling lost the narrow right eye; the documented fixed crop retains both authored eye interiors without filling, carving, masking, recoloring eye geometry, or generating another image. The smaller right eye remains a measured fidelity limit/expression difference for review.

The [native bear](bear-native.png), [light 8×](bear-light-8x.png), [dark 8×](bear-dark-8x.png), and [registration grid](bear-grid-8x.png) show an original long-bodied russet animal with rounded ears, closed eyes, a cream muzzle and tucked paws. The source's 1218×680 occupied aspect is fit to64×36, rather than stretched square. The0.748% integer aspect difference is disclosed. Six opaque material colors are used; there is no baked ground or cast shadow.

The bear's frame is96×96, painted bounds `[16,44,80,80]`,1740 occupied pixels. Its local ground footprint is `[0,32,96,32]` pixels / `[0,1,3,1]` cells. Draw offset from footprint is `[0,-32]`; ground anchor is `[48,80]`; sort anchor is `[48,64]`. Rows0–15 and80–95 stay transparent, all lower pixels fit x16–79, and the last painted paw row is79. Lower art extends beyond its explicit blocking cells according to approved B registration. PNG bounds do not create collision. Runtime/game/editor integration belongs to the parent task.

Production files are in `assets/playable/tanoshi-sizes/`: `tiny-blush.png`, `small-mint.png`, `large-lilac.png`, the96×32 `atlas.png`/`atlas.json`, and `bear.png`/`bear.json`. Editable indexed `.pixels.json` files and unchanged generated sources are in `art/source/tanoshi-sizes/`.

The export is openly mechanical: fixed crops, Pillow12.3.0 nearest sampling, alpha threshold128, and closest squared-RGB flat material encoding. It performs no silhouette construction, eye-hole repair, smoothing, dithering or shadow creation. Crop, placement, palette, generation IDs, source/native hashes and limitations are recorded in [provenance](asset-provenance.json). Prompt direction is a summary of the authorized specification, not a verbatim claim about the original tool prompts.

Original imagegen sources and jobs:

| File | Completed job | SHA-256 |
| --- | --- | --- |
| `generated-tiny-blush.png` | `exec-c1f4e522-54a3-4dba-88db-8b80866bfc78` | `f88c05e97af9c910eed42c765b8ac5fd772638d4f9de5138e173dc200473b9a1` |
| `generated-small-mint.png` | `exec-93743be4-13e8-4fa3-8948-c7559485e568` | `a0a5d6e174fb69de717fab10bf6da44b3c76cf6a0827ebf64ad9df7243f9612c` |
| `generated-large-lilac.png` | `exec-83e6951c-aae3-4675-b6a5-c61fd9966d9b` | `851b41c71b47896f1784955e70bcb773b9e253884313b9fdef27e8f1df92e480` |
| `generated-bear.png` | `exec-9b40ce49-ed08-4f66-9c61-522b36370c87` | `95f5e0a044ec38344ec1fcd1c654cedd0ac4f82d3d5e58984130e05c1e899716` |

All originals are1254×1254 RGBA. [Saved-file checks](native-checks.json) independently reload PNGs, reconstruct editable indexed colors, compare atlas cells, verify binary alpha and two empty foot rows, count truly enclosed8-connected face transparency, and verify bear registration. Source resampling/material equality uses a separate checker and the pinned installed Pillow sampler. Ideal floating-point sampling formulas differ at exact boundaries, so the actual nearest implementation is explicit. All TN1 source/playable files match Git HEAD byte for byte; all six original pet reference sizes/hashes match their existing manifest. The accepted regular Apricot PNG remains SHA `4ca30eb7d60eb20e24629c9c0ac193f93ebc335bb5dc422b81f3f146829b3cf5`.

Actual native PNGs, all original generated inputs, light/dark8× views and both integer grids were visually inspected. The [complete file manifest](file-manifest.json) records each delivered path/hash. Gameplay placement, phone readability, camera changes and save compatibility require the parent's runtime tests and user checkpoint; they are not certified by this asset packet.

Reproduce with a Pillow-capable Python:

```sh
python3 art/source/tanoshi-sizes/export.py
python3 art/source/tanoshi-sizes/check.py
```

On this execution host, the successful interpreter is `/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`. No commit, push or deployment was performed by this asset owner.
