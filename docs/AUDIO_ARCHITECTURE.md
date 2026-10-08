# MIDI soundtrack architecture

MUSIC.03, 2026-10-08. The user accepted MUSIC.02 and explicitly authorized saving it for future use, deleting the rejected edition and choosing its in-game placements. All thirty approved note files retain their original SHA-256 values. No first-edition MIDI or MP3 remains in the current project. Historical review documents and normal Git history remain; history is not rewritten.

## Assets and source of truth

| Path | Responsibility |
|---|---|
| `assets/audio/midi/` | The only canonical loose copies of the thirty approved Type-1 MIDI files. Game and listening-room downloads both refer here. |
| `assets/audio/soundtrack.json` | Lean versioned runtime catalogue with stable numeric IDs, file paths, titles, hashes, duration, tempo/key/meter and note counts. |
| `music/source-v2/` | Editable original scorebook, individual resolved JSON scores, exporter, offline preview renderer and validation. |
| `music/album.json` | Rich listening-room catalogue, including stories and MP3 preview metadata. MIDI paths point to the canonical assets. |
| `music/v2/audio/` | Existing approved-listening-room MP3 previews. Gameplay does not request them. |
| `music/critz-tycoon-30-midi.zip` | Portable thirty-file download with compatibility notes. No rejected file is included. |
| `scripts/build-soundtrack.mjs` | Verifies every canonical file's hash/header and generates the runtime manifest. Runs automatically before the production build. |

## Runtime boundaries

| Module | Responsibility |
|---|---|
| `src/audio/midi.js` | Pure bounded SMF decoder: format 0/1, PPQ, multiple tracks, running status, tempo map, program changes, note on/off and velocity-zero release. Captures volume/expression/pan/room at note onset. Rejects malformed input, orphan/hanging/overlapping same-pitch notes, SMPTE timing and nonzero pitch bends or sustain/modulation/portamento/chorus outside this soundtrack profile. It is not a full General MIDI interpreter. |
| `src/audio/synth.js` | Pure MIDI-event-to-stereo-PCM renderer with original fixed-pitch A440 patches and procedural percussion. Harmonic recurrences provide band-limited sine/triangle/square/pulse/saw and acoustic-inspired voices. Shaped envelopes, modest fixed room reflections, static gain normalization and a silent ending avoid hard loop cuts. |
| `src/audio/worker.js` | Runs decoding and synthesis in a module worker and transfers PCM buffers. A rapid scene change terminates obsolete work; generation IDs reject stale responses. |
| `src/audio/director.js` | One AudioContext, user-gesture unlock, lazy local fetch, bounded cache, 750 ms cue crossfades, full-piece replay, volume/mute, lifecycle suspension and soft failure/retry. Old music continues until the new cue is ready. At most one worker and two playing/fading sources. Cache holds at most two pieces / 34 MiB; transient worker and active/fading buffers can temporarily exceed the cache budget. |
| `src/audio/cues.js` | Pure scene/story/panel selection and separate preference persistence. Changing placement never requires editing musical notes or saves. |
| `src/main.js` | Supplies read-only scene/story/menu context; unlocks on a tap/key; exposes music controls in existing Options and suspends playback while hidden. No new HUD/popup clutter. |

Browser synthesis uses the same original patch families, fixed pitches and envelopes as the approved collection. Its lighter room/percussion processing and 22,050 Hz worker rendering are not a claim of bit-identical MP3 playback. The MIDI performance is authoritative. No soundfont download, external audio service, Web MIDI hardware permission, runtime package or new user account is needed. Web Audio starts only after a user gesture; returning from a background/interrupted browser may require another tap.

Complete arrangements replay with their written pauses and three-second tail; they are not falsely labeled seamless loop edits. Pausing in a menu keeps the current location cue. Habitat submenus share one cue to avoid needless restarts. Returning to the title selects the opening track. No battle system or new place is introduced to justify unused cues.

## Current cue placements

| Context | Track |
|---|---|
| Title / character setup | 01 · The First Open Window |
| Home / bedroom, daytime | 02 · Soup Cooling on the Table |
| Yard / Vet | 19 · New Leaves, Uneven Edges |
| Rootport, daytime | 05 · Rootport on a Tuesday |
| Mossway, daytime | 06 · Mossway beyond the Map |
| Liarsville, daytime | 23 · Postcard from Liarsville |
| Old Waterworks | 25 · The Footprint That Stops |
| Kaid’s home / opening Kaid arrival and gift | 04 · Kaid Takes the Other Handle |
| Rival’s home | 10 · Try Again, with Both Hands |
| Critz pet shop | 03 · A Button with Feet |
| Pharmacy | 18 · Leave a Chair beside You |
| Bike Shop | 24 · Downhill with Your Arms Out |
| Glow n’ Blow | 09 · Seven Screws for a Tiny Roof |
| Tank / Manage / Stats / View / capture | 20 · A Universe behind the Glass |
| Living collection | 07 · The Page with No Answer |
| Critter | 22 · One Critter, One Very Big Day |
| Opening quiet night / home and yard after dark | 21 · Filter Hum at 1 AM |
| Opening distress and broken tanks | 11 · Rain after the Conversation; compassionate, not a horror cue for Mom |
| Rootport after dark | 28 · Porch Radio, Last Summer |
| Mossway after dark | 29 · Fireflies Need No Audience |
| Liarsville after dark | 27 · Salt Air, Empty Calendar |

Night variants apply before 06:00 and from 20:00, using existing saved simulation time. Other approved pieces remain available for future scenes, events or full-game systems. Stable IDs are not array positions.

## Preferences, failures and future changes

`critz-tycoon.audio.v1` stores only `{enabled, volume}`. Defaults: on, 40%. The game save, its backup and UI settings keys are unchanged. Preferences tolerate corrupt/blocked storage. A real slider supports lowering and raising volume by touch or keyboard; Music toggles mute. A missing MIDI, unsupported browser audio or worker failure leaves the game usable, reports only inside Options, and can be retried using Music. Tab hiding suspends the audio clock rather than advancing while inaudible; page restoration resumes the existing cue or prepares the latest requested cue. No music state is serialized into gameplay.

To revise a piece, edit `music/source-v2/scorebook.py`, run its composer and preview renderer, then `node scripts/build-soundtrack.mjs`. Keep IDs stable. Update mappings in `cues.js`, not filenames in gameplay code. The current collection build guard deliberately expects these thirty approved pieces; explicitly update that guard/catalogue and checks if a future task adds a new collection. New MIDI must fit the documented decoder profile, or the decoder and corresponding tests must be extended together. Update synthesis and preview patches together when changing timbres.

## Verification and source references

Unit tests cover every canonical file/hash/patch/duration, MIDI timing and malformed data, cue precedence, separate preferences, spectra and PCM boundaries. The synthesis report renders all thirty MIDI files through the game renderer. Browser tests measure nonzero PCM output after a real gesture, all scene and nighttime selections, habitat changes, cache/source bounds, mute/volume persistence, hidden/visible lifecycle, error recovery, phone layout and unchanged synthetic saves. The ordinary chapter/UI regressions and listening-room tests also run against the clean release.

Implementation references: [MIDI Association SMF specification](https://midi.org/standard-midi-files-specification), [Web Audio specification](https://www.w3.org/TR/webaudio-1.0/), and [MDN AudioContext resume](https://developer.mozilla.org/en-US/docs/Web/API/AudioContext/resume). These informed format/lifecycle behavior, not composition. Physical iPhone/Safari and a human headphone evaluation remain unverified; Chromium device emulation and measured PCM are the available evidence.
