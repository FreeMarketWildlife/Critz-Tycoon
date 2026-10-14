# Tanoshi — original pet references

Reference-only handoff `REF.TANOSHI`, saved 2026-10-14. Phil loves the completed Tanoshi pet and requested its originals for a **later** Critz adaptation. No pixels were resized, redrawn, recolored or integrated into gameplay. Approval of the pet does not approve a game sprite or pass a Critz visual/movement gate.

## Files

All six files in `originals/` retain their exact Library bytes (742,107 bytes total):

| File | Original dimensions | Purpose |
| --- | --- | --- |
| [Tanoshi-spritesheet.png](originals/Tanoshi-spritesheet.png) | 1536×2288, RGBA | Authoritative final v2 pet atlas |
| [Tanoshi-all-states.gif](originals/Tanoshi-all-states.gif) | 384×448; 57 frames | Nine-state motion preview |
| [Tanoshi-look-loop.gif](originals/Tanoshi-look-loop.gif) | 384×448; 16 frames | Clockwise gaze preview |
| [Tanoshi-contact-sheet.png](originals/Tanoshi-contact-sheet.png) | 768×1386 | Labeled frame/row overview |
| [Tanoshi-motion-stills.png](originals/Tanoshi-motion-stills.png) | 1536×448 | Idle, running-right, jumping and waving stills |
| [Tanoshi-pixel-preview-12x.png](originals/Tanoshi-pixel-preview-12x.png) | 768×768, RGBA | Earlier static pixel design preview |

The sprite is exactly **57,695 bytes**, SHA-256 `455e8a6a5664e8cf4104b9a9c5872d03b77cbc00126be09cddc6a5beb46f4701`. Its Library filename is `spritesheet-extended(1).png`; the local filename follows the requested Tanoshi name. The earlier static preview also drops the Library filename's `(1)` suffix. Neither rename changes file bytes.

[manifest.json](manifest.json) records every Library ID, source file ID/version/name, local size, dimensions and hash. Local Library identity attributes were verified; Git does not preserve those attributes, so the manifest also retains provenance.

## Sprite layout and identity

The final pet atlas uses `spriteVersionNumber: 2`: **8 columns × 11 rows**, each cell **192×208**. Coordinates start at the top left; cell `(column, row)` begins at `(192×column, 208×row)`. Used frames run left to right. Unused trailing cells are fully transparent.

| Row (zero based) | Pet state | Used columns |
| --- | --- | --- |
| 0 | idle | 0–5 |
| 1 | running-right | 0–7 |
| 2 | running-left | 0–7 |
| 3 | waving | 0–3 |
| 4 | jumping | 0–4 |
| 5 | failed | 0–7 |
| 6 | waiting | 0–5 |
| 7 | running (active-work pet state) | 0–5 |
| 8 | review | 0–5 |
| 9 | gaze 0°–157.5° | 0–7, in 22.5° steps |
| 10 | gaze 180°–337.5° | 0–7, in 22.5° steps |

Gaze angles increase clockwise from up/12 o'clock: 90° right, 180° down, 270° left. These are pet states and presentation dimensions, not game animation names, timing or frame budgets. GIFs/contact sheets include preview labels and backgrounds; use the final transparent atlas as the authoritative final visual source.

Observed identity: pale blush-pink body, lavender shading and dark plum edges; a large pointed, curved flame-shaped head with four short, separate diagonal rays around it; two narrow vertical eye openings with transparent interiors; a small body with upturned arms, splayed feet and a short rear tail. The tail is clearer in movement/profile poses. The static preview is earlier reference history; the final atlas wins if poses differ.

## Later adaptation and production boundary

A future original native-pixel adaptation must follow the **actual current** [ART_BIBLE.md](../../docs/ART_BIBLE.md), including its authoritative Emerald 2× contract and later user corrections. Consult [PROJECT_STATUS.md](../../docs/PROJECT_STATUS.md), [PROJECT_PLAN.md](../../docs/PROJECT_PLAN.md) and the relevant [REFERENCE_MEASUREMENTS.md](../../docs/REFERENCE_MEASUREMENTS.md) before authoring. This packet chooses no game role, target canvas, collision footprint, palette or movement cadence. Preserve these originals and submit any new adaptation for the required user review.

This folder is outside `assets/`, `art/` and `docs/`. The explicit copy list in [scripts/build.mjs](../../scripts/build.mjs) excludes root `references/`; no runtime/editor asset registration points here. Keep the original media outside production copy paths and recheck that exclusion if packaging changes.
