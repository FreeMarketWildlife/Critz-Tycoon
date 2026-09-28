# M1.C3 — Everyone walking

The user requested walking animations for **each of the twelve delivered character designs**, with a GIF showing everyone. This authorizes directional animation beyond the prior still-only task. It does not constitute final visual approval or request replacement of the playable game's art.

[Open the walking review](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/walking.html) · [All-character GIF](../../../assets/review/characters-walk-v2/all-characters.gif) · [Native shared atlas](../../../assets/review/characters-walk-v2/atlas.png).

## Deliverable

- Twelve characters × four cardinal directions × three poses = **144 native frames**. Every M1.C2 south idle and palette remains exact.
- One **288×384 PNG atlas**, stable per-character/direction/pose metadata, and twelve individual native PNG sheets.
- **Thirteen GIFs:** one labeled 720×768 cast sheet at exact 4×, plus twelve 240×288 individual GIFs at exact 6×. Each cycles through down, left, up and right, showing three complete gaits in each direction.
- An interactive review with synchronized cast playback, enlarged individual inspection, three-pose strip, pause, single-pose stepping, direction selection, background switching and individual downloads. Reduced-motion preference starts playback paused. It reads/writes no game storage.

| Character | Individual GIF | Native poses |
| --- | --- | --- |
| Hero boy | [Walk](../../../assets/review/characters-walk-v2/gifs/hero.boy.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/hero.boy.png) |
| Hero girl | [Walk](../../../assets/review/characters-walk-v2/gifs/hero.girl.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/hero.girl.png) |
| Mom | [Walk](../../../assets/review/characters-walk-v2/gifs/mom.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/mom.png) |
| Kaid | [Walk](../../../assets/review/characters-walk-v2/gifs/kaid.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/kaid.png) |
| Professor Nugget | [Walk](../../../assets/review/characters-walk-v2/gifs/professor.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/professor.png) |
| Juniper | [Walk](../../../assets/review/characters-walk-v2/gifs/juniper.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/juniper.png) |
| Dr. Fern | [Walk](../../../assets/review/characters-walk-v2/gifs/dr-fern.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/dr-fern.png) |
| Mina | [Walk](../../../assets/review/characters-walk-v2/gifs/mina.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/mina.png) |
| Ollie | [Walk](../../../assets/review/characters-walk-v2/gifs/ollie.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/ollie.png) |
| Aunt Ember | [Walk](../../../assets/review/characters-walk-v2/gifs/aunt-ember.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/aunt-ember.png) |
| Rival's mom | [Walk](../../../assets/review/characters-walk-v2/gifs/rival-mom.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/rival-mom.png) |
| Rival's dad | [Walk](../../../assets/review/characters-walk-v2/gifs/rival-dad.gif) | [PNG](../../../assets/review/characters-walk-v2/sheets/rival-dad.png) |

The Hero variants also support the player-named opposite-gender rival under the existing shared appearance convention. The earlier requested 102-character roster remains unlocated; this request animates all twelve current delivered drawings rather than inventing extra identities.

## Drawing and timing

The [chibi framework](../../CHARACTER_FRAMEWORK.md#m1c3-walking-extension) governs all poses: dominant rounded heads, small connected bodies, distinct body shapes, no elongated legs. Frames remain 24×32, at most 20×26 opaque pixels, with anchor `[12,32]`. Idle feet end on row 30; stride feet end on row 31 with the head and upper body shifted down one pixel. Back and profile poses are separately authored. Kaid's handle/spout and Fern's badge have explicit physical-side notes.

Walk sequence: **stride A → idle/passing → stride B → idle/passing**, eight ticks per hold, 32 ticks per complete gait. Tick period is `280896/16777216` seconds. This follows the pinned source tables recorded in [REFERENCE_MEASUREMENTS](../../REFERENCE_MEASUREMENTS.md#clock-sprite-cadence-and-displacement); no new emulator capture is claimed. The review shows walking **in place**, not tile displacement or a new controller test. Running is outside this request.

GIF stores delays only in hundredths of a second. Holds are rounded using cumulative exact time, alternating 130/140ms where needed. The 48-hold loop is approximately 6.43 seconds; actual timing error is recorded in the GIF report. The live review uses fixed ticks and drops long/suspended gaps instead of accelerating through poses on resume.

## Provenance and editable assets

All art is original Critz artwork. Built-in **image_gen** produced one walking-pose guide per character following the imagegen skill; native frames were separately authored/refined in exact indexed rows. Existing M1.C2 source PNGs were references, and all front-idle pixels are preserved. No Pokémon sprites are shipped or stretched.

- [Core guide prompts/provenance](core-guides/provenance.json): Hero boy, Hero girl, Mom, Professor Nugget. Each guide and exact prompt is retained in `core-guides/`.
- [NPC prompts](npc-prompts.json): Juniper, Dr. Fern, Mina, Aunt Ember, with original `*-walking-guide.png` files alongside them.
- Kaid, Ollie and both rival parents: original guides and exact prompts in `other-guides/`.
- [Editable native sources and reproducible export commands](../../../art/source/characters-walk-v2/README.md).

## Verification and delivery

**Actual results:**

- **816/816 native authoring checks** pass, including the full frame matrix, stable IDs, palette/source identity, compact bounds, foot baselines and three distinct poses per direction. [Report](native-validation.json).
- **986/986 independent decoded-PNG checks** pass: atlas pixels equal editable rows, individual sheets match atlas rows, original front idles are unchanged, every figure is connected, and strides alter limbs rather than simply shifting an idle. [Report](png-validation.json).
- **13 GIFs / 624 decoded frames** match their rendered source frames exactly, with **145 global palette colors**, no dithering or color loss. Every loop lasts **6430ms**, only **0.80078125ms** longer than the source-timed 384 ticks. [Report](gif-validation.json).
- **6/6 fixed-clock checks** pass, including identical ticks at 30/60/90/120/144Hz, eight-tick holds, direction boundaries, pause/resume, long-frame dropping and pose stepping. [Report](timing-validation.json).
- **14/14 browser checks** pass: all twelve designs and 48 directional sequences, 192 rendered pose holds, exact pixel scales, ≥44px controls, keyboard/touch, 25 exact downloads, reduced motion, background/focus suspension, missing-asset failures, zero exceptions and zero save/storage access. Portrait 320×568 / 390×844, landscape 844×390 and desktop 1280×900 screenshots were inspected. [Report](browser-report.json).
- **33 existing gameplay, playable-atlas and still-art files** remain byte-identical to the opening commit. [Preservation](preservation.json). Existing game domain/story suites were not repeated because their runtime inputs are unchanged.

Individual proofs and generated design guides were inspected. Review caught and corrected Kaid’s profile near/far handle interpretation, stale proof exports after profile-eye corrections, and an unsupported GIF title glyph. A direct RGB-to-index lookup avoids Pillow’s approximate palette cache, with decoded pixel equality verified after export. Technical checks establish export correctness and do not replace the user's visual acceptance. Physical iPhone/Safari was not tested; browser checks use isolated Chrome contexts and synthetic save sentinels. Current gameplay, story, movement, accepted save keys and playable atlas remain unchanged.

## Published delivery

Source `41377f766ac895927feb36da19c4e24944be0496` was committed on `main`, pushed to GitHub and verified against the remote; the Sites source workflow verified the same commit. The archive matches all **70 tested file hashes**. Deployment `appgdep_6ab9d9e03d8c819197ab1a3e310d5fed` succeeded at **2026-09-28 03:07:22 UTC**, with no failure and the existing owner-only audience unchanged. [Deployment receipt](deployment.json) · [Tested files](tested-runtime.json). The subsequent documentation-only receipt changes no runtime or artwork. Final character/movement acceptance remains the user’s.
