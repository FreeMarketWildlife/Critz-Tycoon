# Actual supplied fan-made Brendan / NF1 overlay

[Private reference comparison](https://chatgpt.com/api/library/files/libfile_16397c0cf0f481918959ef0d4e1f139d/download), Library v0,1080×805. Exact downloaded bytes/RGBA/dimensions and original/download identity/version metadata verified. Reference-bearing pixels remain external to Git and the playable build; only the reproducer, numeric evidence and receipt are committed.

This uses the **actual fan-made left sprite** in [Phil's supplied GIF](https://i.redd.it/01agijgmbz561.gif), SHA256 `5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e`, not an enlarged original Brendan. Root decoded and actually viewed all8frames:100ms each, three unique images in A/A/P/P/C/C/P/P order. Frame2 (identical3/6/7) is the closest two-foot front passing stance. **No true idle is present; NF1 is idle.** No emulator or hidden-anatomy claim.

The full supplied GIF is256×192. Its refined left128×192 crop consists of exact4×4 repeated display blocks in every frame. Removing ONLY that display magnification yields32×48 native authored pixels; exact4× reconstruction is verified for all8frames. The primary16×32 Brendan is not substituted or enlarged. The right-hand original/comparison sprite is excluded.

Native reference frame2 is translated(0,+16) into a32×64 comparison frame; NF1 stays(0,0). Centerline x15.5 and contact-edge y62 align, with no body stretching, width fitting, per-part registration or head matching. Every native pixel corresponds1:1; all three large panels display nearest6×. Small panels are actual32×64. Side originals retain source colors. Overlay uses cyan reference and magenta NF1 at57% alpha each in labelled compositing order; mixed color marks overlap. Centerline/baseline annotations are presentation-only.

Measured findings at this registration:

- Eye sites coincide: x12..13 and18..19,y38..41. Reference hat begins20 while NF1 bare crown begins27; headwear extent does not measure skull height.
- Row47 outer shoulder/upper-arm projection: source x5..26 (22px), NF1 x7..24 (18px). The clothed source is not a naked-shoulder measurement.
- Outer arm/hand span at rows50..52 is x3..28 (26px) in both. Actual glove/hand shape/material differs; source gloves are not interchangeable with a skin-only mask or bone lengths.
- At row54 the source's remaining glove/costume projection is22px wide versus NF1 waist14px. At row55 source18px versus NF1 16px. Walking/idle and outfit differences remain explicit; these are visible runs, not hidden waist anatomy.
- **Shoe alpha rows58+ is exactly equal**, including contact runs x9..12 and19..22 at row61. Colors/interior material differ.

Root actually viewed the final source/original/overlay/native image, checked native NF1 presentation pixels and nearest6× cells outside labelled registration lines, and verified the frozen NF1 PNG SHA unchanged (`5958a184d1f9ee05a3f30392c40627a156752a3427a3d82c179d5d0acdb2294b`, source24444db). Current head/hand/body evidence is comparison-only. Hat/hair/pack/costume remain visible appearance, never inferred hidden anatomy. Parent visual judgment is next; no sprite edits, West changes, pose/animation/creator/runtime/deployment expansion.

Reproduce externally with bundled Pillow Python: `build.py /tmp/<private-output-directory>`. The source GIF must be the exact local pinned supplied asset; the script refuses repository output destinations. `measurements.json` records every frame hash/bounds, registration and checks without storing source pixels.
