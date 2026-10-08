from score import ROOT
from scorebook import PIECES
import json,zipfile
if __name__=='__main__':
    tracks=[]
    for make in PIECES:
        s=make();t=s.save();tracks.append(t);print(f'{s.id:02d} {s.title}: {t["noteCount"]} notes',flush=True)
    album=dict(title='Critz: Tycoon — Thirty Different Days',revision='MUSIC.02 / completely rewritten',status='Approved by the user on 2026-10-08; selected cues integrated into gameplay',tracks=tracks)
    (ROOT/'album.json').write_text(json.dumps(album,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(ROOT/'critz-tycoon-30-midi.zip','w',zipfile.ZIP_DEFLATED) as z:
        for t in tracks:z.write(ROOT/t['midi'],ROOT.joinpath(t['midi']).name)
        z.writestr('READ ME.txt','Critz: Tycoon — Thirty Different Days\nMUSIC.02: 30 newly written compositions, replacing rejected MUSIC.01.\n960 PPQ Type-1 MIDI, named parts, section markers, dynamics and GM fallback programs.\nA440 equal temperament. No nonzero pitch wheels, portamento, modulation or chorus.\nMIDI contains notes, not oscillator waveforms. Custom listening-room sounds are defined in source-v2/render.py; ordinary MIDI players use their own sound bank.\nOriginal music and procedural sounds: Codex for Critz: Tycoon. No reference-game melodies or samples used.\nApproved collection; canonical game assets are in assets/audio/midi.\n')
        z.writestr('TRACKLIST.txt','\n'.join(f'{t["id"]:02d}. {t["title"]} / {t["bpm"]} BPM / {t["meter"]} / {t["key"]}\n{t["personality"]}\n' for t in tracks))
    print(f'{len(tracks)} pieces, {sum(t["duration"] for t in tracks)/60:.1f} minutes')
