# M1.LG1 original art review

All new artwork awaits the user's visual approval. The files are native pixel proposals for the explicitly labeled Luke's Greenhouse review, not accepted roster art. The original source builder reads the existing approved Critz body scaffold, never reference-game sprites or downloaded photographs.

## Reference observations and limits

- [Luke's official channel](https://www.youtube.com/@lukesgoldies), viewed 2026-10-08 in the browser: the featured **I BOUGHT AN ABANDONED FISH FARM** video visibly shows brown hair, a full brown cheek/jaw beard and pale eyes. Bright blue eyes were explicitly requested by the user; the precise cyan palette is an original readable pixel interpretation. The drawing is a fictional game character inspired by Luke, not a claim of endorsement or a photographic likeness.
- [Official care-guide thumbnail](https://lukesgoldies.com/cdn/shop/files/Screen_Shot_2022-08-29_at_10.42.53_PM.png?v=1661830987&width=1920), visually inspected: plump bodies, bumpy red headgrowth, cream/orange cheeks, widely separated small dark eyes, little circular mouths. These inform original side, top and face views. No reference pixels or real product photos are shipped.
- [Official shop](https://lukesgoldies.com/) on the inspection date listed ranchu and sharkchu. [Luke's breeding guide](https://lukesgoldies.com/blogs/news/how-to-breed-and-raise-goldfish) discusses fancy varieties. Our eight ranchu and eight oranda are original fictional individuals, not assertions of today's inventory or real fish identities. Ranchu side views have no dorsal fin; oranda side views have one. Red cap, calico, panda, warm metallic and dark color patterns are design categories, not additional species.
- Web image searches returned unrelated people. The official channel's visible featured video supplied the actual face reference. BAS and Fitz's Fish Ponds event images turned out to show fish, so they were not used as portrait evidence.

## Measured scaffold

Pinned Emerald source revision remains `5eff78649e7170a877b961ef0b3da13b81a16038`. Existing source measurements establish the 16×32 family doubled to 32×64, bottom-center anchor and idle/stride contacts; they are source inspection, not emulator capture. The current body source is approved Hero Boy V1 plus the already documented C7 adult adaptation. Exact Emerald skull/eye segmentation remains unresolved; the anatomical masks below are the existing **original Critz** scaffold, not newly measured Emerald anatomy. The intended measurements were surfaced before production.

All bounds below are half-open `[left, top, right, bottom]` in native top-down coordinates. Display grids label Y upward from zero at the bottom.

| Feature | Existing source / target | Luke actual | Difference or interpretation |
|---|---|---|---|
| Canvas | 16×32 measured family → 32×64 | 32×64 | None |
| Ground anchor | (8,32) → (16,64) | (16,64) | None |
| Full visible envelope | V1 `[3,25,29,62]`; adult hair unrestricted | `[3,23,29,62]`, 798 cells | New brown hair extends two rows above V1 |
| Hidden skull/face | C7 original adult mask | `[3,24,29,45]`, 402 cells | Symmetric; includes the original ear/neck edge guide |
| Eyes | V1 2×4 at x12/18, rows38–41; adult shift -2 | 2×4 each at x12–13/x18–19, rows36–39 | Exact adult landmarks; blue highlight colors do not change mask |
| Hair | Original style, separate from anatomy | Crown row23; side temples; brown cheek/jaw beard through46 | Original interpretation; not a source-game hat envelope |
| Torso | Adult begins43, V1 begins45 | `[9,43,23,55]`, 168 cells | Existing original adult extension |
| Paired arms | Existing C7 adult body occupancy | Combined `[3,43,29,55]`, 56 cells | Mirrored geometry, attached to shoulders |
| Hands | Existing C7 adult occupancy | Combined `[4,47,28,54]`, 48 cells | Mirrored geometry and attachment heights |
| Legs/shoes | V1 rows55–61 | Combined `[7,55,25,62]`, 108 cells | Unchanged envelope; dark trousers/brown shoes |
| Idle contact | Source row30 → target rows60–61 | Last painted row61 | Two transparent bottom rows |
| Stride contact | Source row31 → target rows62–63 | Last painted row63 | Two-pixel body bob, alternating feet |
| Walk cycle | 8/8/8/8 source ticks | strideA/idle/strideB/idle, four directions | GIF review rounds 134ms to130/140ms; source metadata retains ticks |

Front/back idle body, skull, eyes, arms, hands and legs use symmetric masks. Hair and lighting remain separate. Side poses retain compact adult torso mass and attached neck; both are explicitly authored. Native pose sheets and the loop were visually inspected. Mask symmetry is a technical check, not aesthetic approval.

## Native files and rendering contract

- `luke.png`: 128×256. Cells32×64. Columns strideA/idle/strideB/idle; rows south/north/west/east. Use native size in the32px-cell world.
- `fish.png`: 128×512. Sixteen rows in manifest order. Columns side0/side1/top0/top1, each32×32. Side faces west; top faces north. Cardinal rotations preserve the pixel grid.
- `fish-front.png`: 64×512. Same rows, two32×32 paired-eye reveal portraits. Original names and colors are stable IDs in the manifest.
- `silhouettes.png`: 64×512. Same rows, columns top0/top1. Dark opaque silhouettes retain the original fish shape. Tail/head/cheek variations supply partial recognizable cues, not a promise of certainty about an individual's color pattern.
- `tub.png`: 96×64 native three-quarter black tub. `tub-variants.png`: four96×64 plant layouts. Floating leaves and taller edge plants leave the central water visible for animated goldfish. These are separately authored world props; no downsampled close-up.
- `tank-wall.png`: 96×64, three-quarter planted glass tank/cabinet. Animated fish draw over the water region.
- `tub-closeup.png`: 240×160 separately authored top-down tub. This is an original Critz proposed observation-view size, not an Emerald or gallon measurement. Intended presentation480×320 by exact2× nearest-neighbor;32×32 fish remain native assets, with presentation choice disclosed in the review.
- `tiles.png`: eight32×32 cells; see manifest for stable names. Brick floor, glass/ribs, wall foundation, threshold and potted planting. `greenhouse.png`:320×192 facade assembled with repeating glass/foundation modules; original proposed extent. Door and visible ground contact are explicit in metadata. Collision is the parent implementation's separate responsibility, never alpha-derived.

Each output has indexed editable source, SHA-256, native dimensions and palette count in `manifest.json`. Deterministic rebuild: `node art/source/luke-greenhouse/build.mjs`. Review grid/loop: `python3 art/source/luke-greenhouse/review.py` using Pillow. Both read only project sources; neither downloads images. The measurement grid is [art-luke-grid.png](art-luke-grid.png), one square per native pixel with x16 and ten-pixel Y guides. [The clean sheet](../../../assets/review/luke-greenhouse/contact-3x.png) is exact3×. [All poses](art-luke-poses-4x.png) and [walk loop](art-luke-walk.gif) are review outputs only.

Checks recorded in `assets/review/luke-greenhouse/checks.json`: binary alpha; six bilateral anatomical masks;16 fish rows;16 character frames; bounds. Review exports use integer nearest-neighbor. Visual acceptance and motion acceptance remain the user's decision.

Animal review includes [representative countable grids](art-fish-grid.png), [all side/top/front/silhouette poses](art-fish-poses-3x.png) and [synchronized swim/face loops](art-fish-loop.gif). The swim loop uses original240ms two-pose holds rather than a human gait.

`fish-world.png` is a separately authored64×256 bank of16×16 native fish for world tubs and wall tanks. Columns top0/top1/side0/side1, the same sixteen individual rows; use at native16×16 without reducing the observation artwork. `validate.py` independently decodes every PNG with Pillow and compares each RGBA pixel to indexed source, verifies dimensions/alpha/hashes, six mirrored masks, all sixteen silhouette alpha masks unique, visible blue eyes, idle/stride last painted rows and exact3× presentation. Actual results: [art-validation.json](art-validation.json).
