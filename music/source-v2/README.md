# Thirty Different Days — MUSIC.02 source

Thirty fresh scores replacing the user-rejected MUSIC.01 collection. The user accepted this collection and authorized gameplay integration on 2026-10-08. No previous catalogue or melody is an input.

- `scorebook.py`: thirty independently authored functions with absolute-note notation, local rhythms, accompaniment, instrumentation and form. Numbers refer to zero-based bars. Notes such as `F#4:1` last one quarter-note beat; `R` is rest; `+` joins simultaneous pitches; `|` starts a new measure. Unfilled time is silence. Within-piece reprises are explicit.
- `score.py`: shared notation parsing and Type-1 MIDI serialization only; no composition templates. 960 PPQ. All parts have named tracks, dynamics, pan and GM fallback programs. Section markers support navigation; they do not claim tested seamless game loops.
- `scores/`: all thirty resolved scores as separate editable JSON files, including each note's quarter-beat start, duration, MIDI pitch and velocity. Regenerated from the scorebook; edit the scorebook for reproducible changes.
- `render.py`: reparses the actual exported MIDI and renders original fixed-pitch waveforms at 32 kHz before producing 44.1 kHz stereo MP3 previews. Two-pass loudness normalization targets −19 LUFS and −2 dBTP. All source sounds are generated from equations. No reference samples, detuning, wow, chorus or melody pitch modulation.
- `validate.py`: independent MIDI/audio/archive checks and a limited, transposition-invariant six-note contour comparison. A440 patch checks and harmonic ratios distinguish sine/triangle/square/saw. See the review report for actual results and limitations.

MIDI stores performances, not custom waveforms. Use the supplied renderer for these exact original timbres. DAWs and GM players may assign different sounds. This edition's absence of pitch glides is intentional.

Use Python 3.12 and pinned `requirements.txt` in an external virtual environment:

```sh
python -m pip install -r music/source-v2/requirements.txt
python music/source-v2/compose.py
python music/source-v2/render.py
python music/source-v2/validate.py
```

`render.py --ids 1,13,21` renders a subset. Recomposition resets the album manifest; render afterward to restore audio receipts. The composer writes the MIDI ZIP and all resolved score files. The historical MUSIC.02 validation receipt records comparison against all thirty rejected files. Those obsolete scratch files have now been deleted. Future validation omits that optional comparison.

Browser checks: `tests/music-browser.mjs`; set the existing runtime/Chrome environment variables, `CRITZ_MUSIC_URL` and `CRITZ_QA_OUTPUT`. All browser tests use an isolated context and synthetic storage.

Original composition, arrangement and procedural synthesis: Codex for the user's Critz: Tycoon project, 2026-10-07. General genre inspiration: Minecraft, Pokémon and Terraria. Research and the limits of source evidence are documented in `docs/reviews/MUSIC-02/RESEARCH.md`.

Canonical MIDI assets now live in `assets/audio/midi/`. Run `node scripts/build-soundtrack.mjs` after composing to verify hashes and regenerate the lean game manifest. The production build also performs that check. The browser MIDI decoder, worker synth and music director live under `src/audio/`; see `docs/AUDIO_ARCHITECTURE.md`. The approved note bytes remain unchanged.
