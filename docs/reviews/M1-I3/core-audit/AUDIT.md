# M1.I3 core sprite audit and correction

Scope: Hero boy, Hero girl, Mom and Professor Nugget; 48 native poses. Sources are the current `art/source/characters-walk-v2` assets. This staging directory contains no checkout edits. Visual acceptance remains with the user.

## Findings

- **Professor Nugget — repaired.** Olive undershirt colors crossed the lateral coat/sleeve in each side pose, creating an apparent torn panel. The side opening is now narrow and confined to the leading lapel. Cream and coat-shadow pixels close the lateral panel, with the foreground arm occluding the opening during stride B. Both directions receive corresponding edits. All six north/south poses are unchanged.
- **Hero boy — no change.** All four directions and three poses inspected. Rounded hair, connected shoulders/hands, opposed strides, cream shoulder details and tiny shoe contacts remain consistent. Side body geometry mirrors exactly; upper-left hair highlights intentionally differ.
- **Hero girl — no change.** All twelve poses inspected. Twin puffs, connected coral sleeves, dark eye clusters and short shoes retain their shapes. No clear outline, garment or attachment artifact found. Profile head shading is intentionally image-space based.
- **Mom — no change.** All twelve poses inspected. Twin puff volumes, earrings, open jacket/cream shirt, connected curved sleeves and short navy feet remain coherent. Profile bodies have matching proportions and mirrored geometry; intentional head lighting is retained.

## Exact edit scope

82 color substitutions in six Professor frames. No opaque pixels are added or removed; frame geometry is identical. Front idle, all head pixels, feet, palette keys/order/values, body proportions and anchors remain unchanged. Coordinates are zero-based; `coordinate-changes.json` and `.csv` list every old/new palette symbol.

| Character | Direction | Pose | Changed pixels |
| --- | --- | --- | --- |
| Professor | west | idle | 16 |
| Professor | east | idle | 16 |
| Professor | west | strideA | 14 |
| Professor | east | strideA | 14 |
| Professor | west | strideB | 11 |
| Professor | east | strideB | 11 |

## Checks performed

- 48/48 frames: 24×32 storage, anchor (12,32), valid 32 rows of 24 palette symbols.
- Maximum 20×26 opaque bounds; x=2…21. Last opaque row 30 for idle and 31 for strides. Children remain 24 px tall; adults 26 px.
- Every frame remains one four-neighbor connected component; original alpha mask exactly preserved.
- Palettes and their key order match current canonical sources; each PNG uses at most 15 opaque RGB colors and only alpha 0/255.
- Three distinct frames in each direction; heads and feet unchanged, no translated-only substitution introduced.
- West/east body rows remain exact mirrors in all poses. Existing separately lit head pixels are preserved.
- Reviewed before/after sheets at 1×, 4× and 8× nearest-neighbor, with a 6× side-coat comparison crop. Both enlarged color behavior and native garment read were inspected.
- Canonical sources were compared with captured snapshots immediately before handoff; no concurrent source change detected.

## Files

- Root-ready `{hero.boy,hero.girl,mom,professor}.json`: complete twelve-frame source schema.
- `frames/<id>/<direction>-<pose>.png`: 48 native transparent exports.
- `<id>-before/after-{1,4,8}x.png`: full direction/pose inspection sheets. Direction rows south/north/west/east; pose columns idle/stride A/stride B.
- `professor-coat-before-after-6x.png`: labeled comparison.
- `coordinate-changes.json`, `coordinate-changes.csv`, `validation.json`: exact change records and per-frame checks.
- `fix_core.py`: deterministic native edit and proof exporter; uses included `*-before.json` snapshots.
- `report_core.py`: additional RGBA/head/feet/canonical-source validation and this report.

These are targeted native corrections only. No animation timing, run poses, game integration, collision, save, Git or deployment changes were made by this subtask. Root handles integration and the final user review.
