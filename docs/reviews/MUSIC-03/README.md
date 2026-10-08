# MUSIC.03 — Approved MIDI soundtrack in the game

The user approved the thirty-track rewrite and authorized saving, cleanup and game placement. All thirty approved MIDI files are now permanent canonical assets under `assets/audio/midi/`. Their musical bytes/hashes are unchanged. The rejected edition's loose files are removed; normal Git history and labeled historical research are retained.

[Play Critz on your phone](https://critz-tycoon.freemarketwildlife.chatgpt.site) · [All thirty in the listening room](https://critz-tycoon.freemarketwildlife.chatgpt.site/music/) · [Architecture and complete cue map](../../AUDIO_ARCHITECTURE.md) · [MIDI asset guide](../../../assets/audio/README.md)

The game now fetches the `.mid` files, decodes their note/tempo/instrument events and synthesizes original fixed-pitch voices in a background worker. It does not substitute the preview MP3s. Twenty-one pieces have scene, nighttime, story or habitat placements; nine are retained for future fitting moments. The opening remains compassionate. No new battle or area was added.

Music starts after a tap/key. **Start → Options → Music / Music volume** provides a mute switch and a touch/keyboard slider. Defaults are on at 40%. Scene changes fade over 750 ms; old music continues until the next cue is ready. Backgrounding suspends the audio clock. Missing assets fail softly, with retry through the Music switch. Settings use a separate key and never enter saved game state.

## Verified

- [Asset audit](asset-audit.json): all thirty approved hashes preserved, one canonical loose copy per track, exact files inside the ZIP, no rejected loose tracks, and fourteen non-shared opening edited files byte-identical. Existing status/plan edits also remain outside this task's commits.
- [127 unit checks](unit-tests.txt): all existing game tests plus MIDI timing/running-status/error validation, canonical asset profiles, cue selection, preference isolation, stable spectra and PCM boundaries.
- [All thirty game-synth renders](synthesis-report.json): finite, non-silent, peak-bounded stereo PCM; measured slowest render 493 ms on this host. This is not a physical phone performance claim.
- [11 game-music browser scenarios](music-browser-report.json): silent pre-gesture page, actual measured audio after unlock, all fourteen scenes and night variants, mute/volume/reload, stable menu cue, tank submenus/collection, rapid toggles, source/cache bounds, hidden/visible lifecycle, phone controls, real MIDI requests with no MP3 substitution, and missing-file recovery. Final control changes were rechecked on the release build.
- [Eight UI scenarios](ui-browser-report.json), [17 complete chapter scenarios](chapter-browser-report.json), and [nine listening-room scenarios](listening-room-report.json): gameplay, opening/loans/rescues/shops/care/Critter, saves, menus, all thirty preview files and downloads remain functional. All browser contexts use synthetic saves.
- [Phone Options](phone-options.png) inspected; controls remain reachable at 320px portrait, 390px portrait and landscape. Physical iPhone/Safari and a new human headphone evaluation remain unverified.

An early JavaScript exponentiation syntax error was caught by unit tests and fixed before browser testing. A test fixture initially wrote a synthetic save while leaving active gameplay, allowing the existing page-hide save handler to correctly overwrite it; the fixture was corrected to write from the title screen. Neither issue was published. Review of the first control draft also replaced a cycling volume button with a proper bidirectional slider before release.

The runtime preserves the approved pitch/envelope families; lighter room/percussion processing and 22,050 Hz rendering mean its sound is not asserted to be bit-identical to the offline MP3s. This implementation supports the documented fixed-pitch soundtrack MIDI profile, not every possible MIDI controller or external soundfont. Complete pieces replay with written rests and a three-second tail, not fabricated seamless-loop claims.

Source, remote verification and successful publication are recorded in PROJECT_STATUS and the deployment receipt. Exact next action after delivery: play the integrated soundtrack and refine any concrete placement, balance or browser feedback. No implementation remains after verified publication.
