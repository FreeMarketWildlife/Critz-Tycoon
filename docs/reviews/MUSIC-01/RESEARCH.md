# MUSIC.01 — What makes a little world memorable?

Research consulted 2026-10-06/07. These are original Critz compositions, not covers, sound-alikes of individual songs, or a recreation of a proprietary sound bank. The composer is Codex; musical acceptance belongs to the user. Source inspection and signal measurements are distinguished from human listening below.

## What the composers say

**A few voices can still have a conversation.** In the official Pokémon interview from May 13, 2014, Masuda describes studying Bach's three-voice writing, his interest in synthesizers/FM programming, and drawing from many genres. He emphasizes imagining the game scene and its player-dependent timing, rather than treating music as a fixed film cue. The Ruby/Sapphire transition also brought sampled timbres and a wider palette, including timpani. [Official interview](https://www.pokemon.com/us/pokemon-news/a-conversation-with-pokemons-musical-maestro/) · [Readable archival reproduction](https://www.pocketmonsters.net/content/Interview_A_Conversation_with_Pokemons_Musical_Maestro). The official page itself did not expose the interview text to the browser tool; the archival reproduction was read and is identified as such.

**Melody is the anchor, but the small answers matter.** The July 30, 2009 HeartGold/SoulSilver sound-team interview describes retaining memorable melodies, countermelodies and grace notes when arranging older music. Sato discusses Route 47 in terms of anticipation of a destination. Ichinose describes balancing the peaceful image of Ho-Oh with the power a battle requires. Different instruments and arrangements can express temperature, relaxation, and nostalgia. [Interview booklet, fan translation](https://dogasu.bulbagarden.net/features/interview_hgss_sound.html). This is translated first-person material, not a verified official English transcript. Its channel-count footnote is unreliable; hardware claims below use technical documentation instead.

**Rhythm can evoke a place without copying its tunes.** Masuda describes taking core rhythmic inspiration from Hawaiian traditions while creating different melodies for Alola. That is a useful distinction between a compositional principle and a borrowed song. [TIME's direct interview](https://time.com/4536438/pokemon-sun-moon-interview/), October 19, 2016.

## Hardware facts, without nostalgia mythology

Game Boy audio has two pulse channels, one wave channel, and one noise channel. Channel 1 has a hardware period sweep; the wave channel holds a 32-sample, 4-bit waveform. These limits encourage clear part-writing, register separation and meaningful articulations, but they do not prove why a particular melody is loved. [Pan Docs audio registers](https://gbdev.io/pandocs/Audio_Registers.html).

GBA retains related legacy channels and adds two direct-sound PCM channels; those PCM streams can carry software-mixed material. Therefore neither “four instruments maximum” nor “just square waves” describes the whole Emerald-era palette. [Tonc's sound introduction](https://gbadev.net/tonc/sndsqr.html). Critz uses modern rendered synths and ordinary MIDI, not a hardware-accuracy claim.

## Pinned Emerald source inspection

Inspected seven MIDI source files from the community decompilation at `pret/pokeemerald` revision **5eff78649e7170a877b961ef0b3da13b81a16038**, the same revision as the project's reference ledger. This is modern source-file inspection, not proof of Game Freak's original authoring files, ROM playback timing, emulator observation, or a performed listening comparison. The MIDI data stayed outside the repository and deployment; no reference notes or assets enter the authoring scripts.

The [measurement receipt](reference-measurements.json) stores exact source URLs, SHA-256 hashes, tempo events, track counts, note counts, controller IDs, pitch-wheel counts and markers. Examples: Littleroot has 10 MIDI tracks at 108 BPM; Route 101 has 9 at 114 BPM and 29 pitch-wheel events; Route 104 has 11 tracks and several tempo events (128, 122, 120 BPM); Abandoned Ship has 9 at 100 BPM. Track counts include metadata and are not simultaneous hardware voice counts. Source marker brackets identify repeat regions in these files; arbitrary controllers are not assumed to mean their General MIDI equivalents.

**Inference:** contrast, phrasing and orchestration deserve at least as much attention as tempo. A moderate source tempo does not imply low energy, and an atmosphere cue need not be extremely slow. A pitch-wheel event count does not establish perceived expressiveness. Critz therefore uses independent melodic identities, five meters, six modes, distinct groove families, gaps, replies and section changes instead of relying on speed or a single “retro” preset.

## Decisions for this collection

These are Critz proposals, not claims about Pokémon's theory or new game canon.

- **An eight-bar thought.** Each cue starts with four authored question bars and has individually authored answer/cadence bars; a separately written B idea changes the perspective. Later returns change orchestration, articulation and occasional grace notes. Deterministic pattern assembly performs the written material; it does not learn from reference melodies.
- **A recurring voice, not thirty identical loops.** Reed, flute, glass and bubble sounds recur across the album. The final piece explicitly recalls the original title motif. Each track still has distinct A/B melodies, harmony, meter/tempo or accompaniment identity. This is a collection of compact game cues, not thirty unrelated genre productions.
- **A small cast of sounds.** Lead, answer, harmony, bass, glints, air and drums get separate named MIDI tracks. Seven sounding parts are a production choice; they are not an emulated GBA channel budget.
- **Bends as speech.** Short scoops and encoded vibrato decorate selected lead notes. Independent monophonic channels keep a scoop from detuning a chord. MIDI RPN sets a ±2-semitone pitch range. Warm and darker patches use lower registers; glints sit above the main line.
- **Rhythm tells the scene.** The snail gets 3/4; the notebook gets 5/4 curiosity; rising water gets an unsettled 7/8; the glass shop gets syncopated funk; home and night receive swung lo-fi beats; the seaside daydream uses a relaxed bossa pattern. Different breaks and arrangements prevent every cue from following the same density curve.
- **Tenderness has room.** Mom's forgiveness cue is sparse and warm. The frightening cue concerns an uncertain shadow, not a villainous portrayal of medication needs. Every rescued animal survives. Future-place and battle cues remain explicitly imagined soundtrack proposals.
- **Lo-fi is color, not damaged intelligibility.** Original FM-style keys, rounded bass, mild saturation, slow wow, filtered percussion and restrained stereo space. No vinyl recordings or borrowed loops. The MIDI captures notes/controllers; the rendered MP3 additionally includes the custom timbres and mix effects.

## Production and honest limits

Thirty Type-1 MIDI files, 480 ticks per quarter, six pitched channels plus GM channel-10 drums, tempo/time-signature metadata, expression, velocity, modulation and pitch-wheel data. Suggested `LOOP_START` / `LOOP_END` regions omit the introduction/coda. They are musical arrangement markers; seamless in-engine looping and transition behavior still require an implementation pass. MP3s are album presentations with endings, not seamless audio loops.

The renderer reads the actual exported MIDI. Original additive/FM/sine percussion synthesis uses no downloaded samples. Release envelopes, voice levels, stereo positions, tempo echoes and a generated diffuse room are reproducible in source. MP3s are 44.1 kHz stereo at 128 kbps, loudness-targeted to approximately −17 LUFS with conservative peak headroom. MIDI playback on arbitrary devices will sound different because custom patches/effects are not embedded in Standard MIDI Files.

Checks independently parse note lifecycles and automation, compare all 30 lead fingerprints, decode every MP3, measure integrated loudness/true peaks/mono compatibility/interior silence, and exercise actual browser playback and seeking. These establish functioning deliverables, not musical greatness. No human listening panel or physical iPhone/Safari evaluation was available; the user is the listening reviewer. Revision 1 remains awaiting that response.
