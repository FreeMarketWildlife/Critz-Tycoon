# Playable character source

Run `node art/source/playable-characters/build.mjs` from the project root to rebuild `assets/playable/characters/atlas.png` and its stable-ID manifest. Then run `python3 scripts/pack-playable-atlas.py` (Pillow required) to rebuild the single exploration atlas.

This deterministic native pixel source reads only the recovered original B1/G1 indexed rows/palettes. Their south walk-idle pixels remain unchanged. Other directions, alternating strides, run poses and seven supporting roles are original extensions in the same 16×32 frame with the `(8,32)` foot anchor. Human right poses reuse symmetric left design pixels; metadata records this. Kaid's four directions are authored separately so his spout and handle keep their physical identity.

Nine roles × four directions × two gait sets × three poses produce 216 exported entries. NPCs currently stand idle; complete sheets are available without adding NPC schedules or game mechanics. The supplied image-generation study is an illustrative supporting design guide only; it is not sliced, rescaled or shipped as character frames. All exports are playable-review artwork awaiting final user acceptance.
