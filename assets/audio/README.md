# Approved Critz MIDI assets

All 30 original **Thirty Different Days** MIDI tracks are saved here for the game and future use. User-approved on 2026-10-08. The first, rejected collection has been removed from the current project; no first-edition track is bundled.

`midi/` is canonical; do not create another loose copy in the listening-room folder. `soundtrack.json` is generated and verified by `node scripts/build-soundtrack.mjs`, also run by `node scripts/build.mjs`. Stable IDs and hashes identify the pieces. The listening room references these same files and offers the complete MIDI ZIP.

Editable scores: `music/source-v2/`. Runtime architecture and cue placements: `docs/AUDIO_ARCHITECTURE.md`. MIDI contains musical events, not oscillator waveforms; original game patches live in `src/audio/synth.js`. Preview MP3s remain available in the listening room and are not gameplay audio inputs.
