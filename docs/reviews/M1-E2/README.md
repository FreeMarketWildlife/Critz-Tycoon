# M1.E2 — Overworld master tileset, review 01

**Asset package delivered for user visual review.** The user authorizes a full original overworld kit including tiled buildings, water, cliffs, fences, gardens and fountains at the established Emerald 2× budget. This supersedes the older small house/tree-only restriction for this review. No art acceptance, new canon or gameplay integration is inferred.

[Phone review](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/overworld.html) · [Master PNG](../../../assets/review/overworld-v1/master.png) · [Tile kit ZIP](../../../assets/review/overworld-v1/critz-overworld-v1.zip) · [Native view](../../../assets/review/overworld-v1/viewport.png) · [Town assembly](../../../assets/review/overworld-v1/town-with-hero.png)

The master has **385 named entries**, each exposing four base tiles. Its reserved transparent space supports future additions. **59 opaque colors** are actually used. Five-cell cottages and a seven-cell shop genuinely reuse roof, wall, window and split-door tiles; the interactive review extends the same parts to eleven cells. Three- and five-cell fountain basins share rim and center modules.

Four complete 47-mask terrain families cover paths, grassy water banks, paving and cultivated soil. Fences and hedges each have sixteen cardinal connections. Other parts include cliff cap/face/foot, corners, returns, stairs, static waterfall/splash, two roof materials, three wall materials, window boxes, door states, awnings, chimney, trees, bushes, grass, reeds, rocks, lilies, crops, gates, bridges, fountain/jet, bench, lamp, sign, mailbox and pots.

## Source and reference evidence

The [Art Bible](../../ART_BIBLE.md) is authoritative. Existing source measurements pin pret/pokeemerald `5eff78649e7170a877b961ef0b3da13b81a16038`: 8px base tile, 16px metatile, selected 5×5 house and 2×2 tree assemblies, 1×2 door redraw. This revision doubles those structural budgets. The wider shop, cypress, fountains, palette, footprints and individual pixels are original Critz proposals. No new emulator/frame-capture observation or universal architecture measurement is claimed.

Built-in imagegen supplied a [design study](../../../art/source/overworld-v1/design-study.png) from the [exact prompt](../../../art/source/overworld-v1/design-prompt.txt). Its irregular spacing and raster artifacts prevent it being a native tileset. The master is separately authored with the project's integer-pixel raster source; it contains no sampled reference-game or generated-study pixels. [Editable source and rebuild instructions](../../../art/source/overworld-v1/README.md).

## Verification

[Independent pixel report](pixel-checks.json): **28 checks pass**, including exact source/export pixels, dimensions/alignment, binary alpha, palette membership, all terrain masks, **8,192 exhaustive compatible terrain-edge comparisons**, IDs, reused building modules, exact enlargements and three maps independently reconstructed pixel-for-pixel from the PNG. The initial seam check caught a two-pixel inner-corner mismatch; it was corrected before the successful run.

The approved Hero Boy V1 PNG matches the scale composition exactly. Native/enlarged town, architecture, terrain and atlas proofs were inspected. These checks establish asset/assembly consistency, **not user visual acceptance or gameplay behavior**.

[Eight browser scenarios](browser-report.json) pass: asset loading, all five views, grid/integer zoom, 5–11-cell building width and roof color, library filtering/inspection, downloads, desktop/phone layout, and zero runtime errors/storage calls. [Five independent browser-to-PNG comparisons](browser-pixel-checks.json) match every rendered pixel. A fresh isolated context uses a synthetic save sentinel and throws if review code accesses browser storage. No user browser data is tested. [390px phone](review-390.png) and [1440px desktop](review-1440.png) screenshots were inspected; 320px and landscape 844px layouts also have no page overflow. Physical phone hardware/Safari were not tested. Fit can reduce pixels on narrow screens, while native 1×/2×/3× modes scroll without smoothing.

Rebuilding from editable `pixels.json` reproduces all native outputs byte-for-byte. The reproducible ZIP passes CRC and byte equality for all 25 packaged files. Publication and verified source receipts are recorded below after deployment.

Opening branch `main`, commit `20f7c8d`. Existing tracked and untracked character/game work is preserved and excluded; concurrent project changes are retained. Shared status/plan entries are staged separately from pre-existing edits.

## Limits and next action

This is a static review kit. Water/fountain/waterfall do not animate; door states are not an accepted animation. Collision, anchors, footprints and foreground metadata are proposals. The review never accesses game saves. The sample town is not a new Rootport map. The generated study is not a native asset.

**Next action:** user reviews this exact native atlas and its assemblies; refine the appearance before replacement gameplay integration or animation. Existing game art, movement, story and save keys are unchanged.
