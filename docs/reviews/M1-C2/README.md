# M1.C2 — 20×26 chibi still-character design

**Framework and confirmed-cast artwork; the full requested 102-character roster remains unresolved.** The user selected the larger visible budget and required cute compact chibi proportions, individual body types and one still frame each with no animations. This records a budget/direction choice, not final approval of the new drawings.

[Inspect the new characters](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/characters.html). Every card selects one native still; inspect it at exact 8×, switch light/dark/grass backgrounds, view pixel guides, see it in the existing bedroom, and download the individual transparent PNG. The gallery itself has no animation loop and accesses no saves. [Drawing framework](../../CHARACTER_FRAMEWORK.md).

## Roster source and scope

The repository and its 17 available historical commits contain **12 story identities**, nine shared renderer appearances, and ten B1–B5/G1–G5 candidate designs. The prior character-art task explicitly requested ten candidates. None contains a 102-character roster. The user has been asked to locate or clarify it. No unnamed extras were invented or presented as established characters.

This batch contains **12 unique still designs** covering the currently located cast. The two Hero options also support the player-named opposite-gender rival, matching the existing shared appearance convention. They are two drawings, not four counted variants. The full 102-design request cannot be marked complete without its roster/count being resolved.

| Design | Painted W×H | Colors | Construction |
| --- | --- | --- | --- |
| Hero boy | 18×24 | 12 | Rounded afro, small raglan tee, broad child stance |
| Hero girl | 20×24 | 13 | Twin puffs, flared short tee, petite child stance |
| Mom | 20×26 | 15 | Rounded twin puffs, broad soft pink jacket, short legs |
| Kaid | 18×24 | 13 | Rounded asymmetrical pitcher, expressive eyes, connected tiny body |
| Professor Nugget | 20×26 | 14 | Broad hat, readable glasses, sturdy short coat |
| Juniper | 18×26 | 12 | High bun, puff sleeves, pear-shaped teal apron |
| Dr. Fern | 18×25 | 13 | Swept rounded bob, slim short coat, turquoise center |
| Mina | 16×24 | 13 | Petite compact cardigan, glasses, distinct close stance |
| Ollie | 20×26 | 15 | Stepped cap, broad sports sleeves, short cargo legs |
| Aunt Ember | 18×26 | 14 | Textured tied hair, goggles, sturdy indigo apron |
| Rival’s mom | 18×25 | 12 | Rounded side-parted hair, soft pear silhouette, short trousers |
| Rival’s dad | 17×25 | 11 | Tidy hair, broad short green pullover, planted stance |

All have 24×32 transparent storage frames, maximum 20×26 painted regions, anchor `[12,32]`, and the same row-30 foot baseline. Head construction is 14–16 rows, body construction 9–10 rows. Size is a ceiling: petite characters need not fill all 26 rows. Width, shoulders, clothing and stance distinguish bodies without extending their legs. These are Critz design choices, not exact Emerald anatomy claims.

## Assets and provenance

- [One shared transparent PNG](../../../assets/review/characters-v2/atlas.png), **144×64**, with 12 stable frame entries; [metadata and measurements](../../../assets/review/characters-v2/atlas.json).
- Individual native PNGs are in `assets/review/characters-v2/individual/`; download each through the inspector.
- [Labeled cast sheet](character-still-contact-sheet.png), [annotated construction plate](character-framework-annotated.png), [lossless plate checks](plate-validation.json).
- [Native lineup](lineup-native.png), [exact 4×](lineup-4x.png), [exact 8×](lineup-8x.png), [light-background 8×](lineup-light-8x.png).
- [Editable source rows and palettes](../../../art/source/characters-v2/README.md), plus measured head/body annotations and identity sources.

All designs are original Critz artwork. Built-in **image_gen** created design guides, following the imagegen skill and using the original [supporting-character study](../M1-I2/supporting-character-study.png) and recovered Hero designs as references. The native stills were independently authored/refined as exact indexed rows. Generated illustrations were not downsampled into the finished sprites. No Pokémon sprites or rejected environment-v1 assets are shipped.

Exact generation briefs: [Hero pair](heroes-prompt.txt), [Mom/Nugget](mom-nugget-prompt.txt), [Kaid](kaid-prompt.md), [seven NPC prompts](npc-prompts.json). Their original guide PNGs are preserved beside this record as `*-design-guide.png`; each is a design reference, not a verified native asset. The drawing framework explains the distinction and future handoff process.

## Individual refinement and checks

Mom’s puffs were revised again after the first native pass read as pointed ears. Their final caps/sides are rounded, while her face and soft jacket remain intact. Nugget’s lens/pupil clusters were separated, shoulders broadened and lower body shortened. Kaid’s previous gap between pelvis and legs is eliminated; his new handle has a clear transparent opening. Hero facial pixels preserve warm dark skin, separate eyes and compact child anatomy. NPC eyes, goggles, hats and clothing silhouettes were inspected individually on light/dark backgrounds and in a common lineup. Reused game appearances now have distinct stills.

- **108 native-source checks pass** across all 12 frames: exact storage, palette symbols/counts, maximum ink extent, baseline, no blank body scanlines, unique drawings and annotated compact proportions.
- **90 independent decoded-PNG checks pass**: source-pixel equality, exact atlas/individual hash equality, binary alpha, bounds/anchors, connected figures, all 12 unique silhouette masks and exact 4×/8× enlargement. [PNG report](png-validation.json), [native report](native-validation.json).
- Per-artist evidence: [Hero checks](heroes-validation.json), [Mom/Nugget checks](mom-nugget-validation.json), [NPC checks](npc-validation.json).

**15/15 browser checks pass** across all twelve designs and 320×568 / 390×844 portrait, 844×390 landscape and 1280×900 desktop. All controls, labels, exact integer scales, native PNG download bytes, static canvases, missing-asset failures and zero storage access pass in isolated synthetic contexts. [Browser report](browser-report.json), [testing notes](browser-notes.md), [portrait](characters-390x844.png), [landscape](characters-844x390.png). The portable test runner is `tests/characters-browser.mjs`. All twelve previous gameplay/atlas hashes remain unchanged ([preservation](gameplay-preservation.json)).

The labeled contact sheet and construction plate preserve every opaque source pixel at exact 4×/8× and reproduce identical PNG hashes. Their assembly script is `scripts/export-character-plates.py`. **Published successfully** from source `f709e2bca0750aebbe2a375d513f5bd7cceb74d3` on `main`, verified against GitHub and Sites source. Deployment `appgdep_6ab9d35fd22c8191a1ef4bacaf993ea5` succeeded at 2026-09-28 02:39:36 UTC, with existing owner-only audience unchanged. All 34 [tested hashes](tested-runtime.json) match the packaged deployment. [Deployment receipt](deployment.json). The subsequent documentation-only receipt does not change the published runtime. Native and enlarged art inspection is an artist/engineering check, not the user's acceptance. No physical iPhone/Safari or Emerald emulator capture is claimed. The current playable character sheets, world, controller, story and saves are preserved; this task only adds still-design review artifacts and links.

Next dependency: identify/clarify the requested 102-character roster, then create the remaining specified designs with this framework. Final character acceptance remains with the user.
