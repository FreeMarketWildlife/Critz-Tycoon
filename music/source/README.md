# A Tiny World — editable soundtrack source

MUSIC.01, 30 original compositions for Critz: Tycoon. Listening acceptance is pending.

`catalogue.py` contains each track's title, story, key/mode, time signature, tempo, groove, patch choices, chord progressions, explicitly authored A/B melodies and answering cadences. Notes are relative scale degrees with `s/e/q/d/h/w` durations (sixteenth, eighth, quarter, dotted quarter, half, whole); `R` is a rest. Every bar is checked against its meter. No reference MIDI is an input.

`compose.py` develops these phrases into intros, contrasting sections, breaks, reprises and codas. It writes Type-1 `.mid` files at 480 PPQ: conductor, lead, answer, harmony, bass, glints, air and percussion. Pitch wheels use a ±2-semitone RPN range on independent monophonic parts. Standard GM programs provide portable fallback timbres; they are not the custom MP3 patches. `LOOP_START` / `LOOP_END` mark the proposed arrangement region, not a tested seamless game-audio implementation.

`render.py` reads those actual MIDI events, synthesizes the instruments and drums from equations, applies expression/pan/velocity/bends, generated room ambience and tempo echoes, and renders stereo MP3 at 44.1 kHz / 128 kbps. Lo-fi cues add filtered warmth, mild saturation and slow wow. It uses no soundfont, ROM sample, downloaded impulse or recorded loop. Per-track render receipts and `album.json` preserve hashes and technical metadata.

`validate.py` independently checks MIDI lifecycles, mono bend lanes, note counts, diversity and loop metadata, then decodes MP3s and measures loudness, peaks, interior continuity and stereo compatibility. `tests/music-browser.mjs` exercises the listening room in an isolated browser context with synthetic save data.

## Rebuild

Requires Python 3.12 and the pinned packages in `requirements.txt`. Install into a separate virtual environment, not the game project. FFmpeg is provided by `imageio-ffmpeg`.

```sh
python -m pip install -r music/source/requirements.txt
python music/source/compose.py
python music/source/render.py
python music/source/validate.py
```

Render a subset with `--ids 1,13,21`. Run the renderer after recomposing: composition rebuilds the manifest and MIDI archive, while rendering adds the audio hashes. Rebuild the MIDI ZIP with the composer. It includes only original MIDI files and a compatibility note; MP3s remain individual files for phone-friendly downloading.

The scripts are deterministic for the pinned package/runtime versions. MP3 binary identity across different FFmpeg builds is not guaranteed. Source authorship: Codex for the user's Critz: Tycoon project, 2026-10-06/07. Pokémon research informs general scene-writing principles, not melodies or proprietary instruments. See `docs/reviews/MUSIC-01/RESEARCH.md` for sources and limits.
