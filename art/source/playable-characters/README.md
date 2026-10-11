# Playable character source

Run `node art/source/playable-characters/build.mjs` from the project root, then `python3 scripts/pack-playable-atlas.py` (Pillow required) to rebuild the single exploration atlas.

The exporter reads the corrected, editable native rows in `art/source/characters-walk-v3`. It copies each 24×32 frame with foot anchor `[12,32]` exactly; no resizing, smoothing, palette substitution, procedural limb drawing or mirroring occurs. Maximum painted bounds remain 20×26. Kaid has independent physical-side artwork.

Twelve designs × four directions × two movement modes × three poses produce 288 stable runtime entries. Run entries deliberately reuse the corrected walk artwork at the existing 5/3 tick cadence, with unchanged 8-tick movement. Dedicated run poses are pending a later art pass. NPCs retain existing stationary behavior; the complete directional sheets add no schedules or mechanics. Appearance mapping uses existing story IDs in `src/appearance.js`; names, state and collision data are unchanged.

The 288×768 character PNG and unchanged 512×320 environment PNG are copied losslessly into one 512×1088 atlas. Every character entry is independently compared to canonical native rows by the packer. Final user visual/movement acceptance remains pending. See `docs/reviews/M1-I3/README.md` for corrections and actual validation results.
