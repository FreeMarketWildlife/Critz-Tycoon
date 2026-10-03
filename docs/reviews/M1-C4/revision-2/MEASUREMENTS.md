# Measured front-idle construction — revision 2

All coordinates are half-open `(left, top, right, bottom)`. Measurements use the pinned source, not inferred screenshot scaling.

| Annotated region | Reference size | 2× target size | Actual 2× | Bounds deviation |
| --- | --- | --- | --- | --- |
| full figure | 14×21 | 28×42 | 28×42 | 0 |
| headwear / original hair envelope | 12×8 | 24×16 | 24×16 | 0 |
| face and ear band, with borders | 14×5 | 28×10 | 28×10 | 0 |
| head and face combined | 14×13 | 28×26 | 28×26 | 0 |
| shoulder row | 12×1 | 24×2 | 24×2 | 0 |
| central torso region | 6×5 | 12×10 | 12×10 | 0 |
| left arm and hand region | 4×4 | 8×8 | 8×8 | 0 |
| right arm and hand region | 4×4 | 8×8 | 8×8 | 0 |
| left distal limb region | 4×3 | 8×6 | 8×6 | 0 |
| right distal limb region | 4×3 | 8×6 | 8×6 | 0 |
| shorts and feet band | 10×3 | 20×6 | 20×6 | 0 |
| left leg and shoe region | 4×3 | 8×6 | 8×6 | 0 |
| right leg and shoe region | 4×3 | 8×6 | 8×6 | 0 |

Eyes: `(6,19)…(6,20)` and `(9,19)…(9,20)` become rectangles `[12,38,14,42]` and `[18,38,20,42]`. Actual labeled eye masks match exactly.

Anchor: `(8,32)` → `(16,64)`. Idle final row: 30 → 60–61. Actual last row: 61.

The face/ear and complete body occupancy from reference rows 18–30 matches the 1× Hero exactly and is doubled exactly in the 2× Hero. Costume, skin, palette and hairstyle are original.

## Definitions and deviations

- The hidden skull and exact anatomical boundaries beneath headwear/clothes cannot be recovered from this raster. Symmetric construction is required for Critz; it is not an observed hidden bone shape.
- Arm/hand and distal-limb windows include their outline and sleeve/glove overlap. Original Hero clothing changes their color/material partition without changing the measured occupied silhouette.
- Original afro occupies the measured headwear envelope but has a different contour and fill area (78 vs 66 cells at 1x). This is an explicit hairstyle adaptation, not exact copying of the pointed cap.
- The newly supplied montage is a visual preference reference, not a provenance-verified Emerald source sheet.

Source: [pinned Brendan sheet](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/brendan/walking.png). The complete source revision, SHA-256, bounds and occupied-cell counts are in [measurements.json](measurements.json).
