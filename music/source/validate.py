#!/usr/bin/env python3
"""Independent export checks: MIDI lifecycle, expression, distinctness, and decoded audio."""
import argparse,json,hashlib,subprocess,re
from pathlib import Path
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
import mido,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/'docs/reviews/MUSIC-01'

def check_track(t,check_audio):
    path=ROOT/t['midi'];m=mido.MidiFile(path,charset='utf8')
    assert m.type==1 and m.ticks_per_beat==480 and len(m.tracks)==8
    active=Counter();notes=0;bends=0;velocities=set();programs=0;lead=[];time=0.;peakPoly=defaultdict(int);current=Counter()
    for msg in m:
        time+=msg.time
        if msg.is_meta:continue
        if msg.type=='program_change':programs+=1
        if msg.type=='pitchwheel':bends+=msg.pitch!=0
        if msg.type=='note_on' and msg.velocity:
            key=(msg.channel,msg.note);assert active[key]==0,('overlap same pitch',t['id'],key,time)
            active[key]+=1;notes+=1;current[msg.channel]+=1;peakPoly[msg.channel]=max(peakPoly[msg.channel],current[msg.channel]);velocities.add(msg.velocity)
            if msg.channel==0:lead.append(msg.note)
        if msg.type=='note_off' or msg.type=='note_on' and msg.velocity==0:
            key=(msg.channel,msg.note);assert active[key]==1,('orphan',t['id'],key);active[key]-=1;current[msg.channel]-=1
    assert not any(active.values()) and not any(current.values())
    assert notes==t['noteCount'] and bends>=10 and len(velocities)>20 and programs==6
    assert peakPoly[0]==1 and peakPoly[1]<=1,('pitch bends require mono voices',t['id'],dict(peakPoly))
    assert abs(time+2.8-t['duration'])<.02
    markers=[x.text for x in m.tracks[0] if x.type=='marker'];assert markers.count('LOOP_START')==markers.count('LOOP_END')==1
    assert len(t['sections'])>=6 and t['loopStart']<t['loopEnd']<t['duration']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==t['midiSha256']
    result=dict(id=t['id'],title=t['title'],notes=notes,nonzeroBends=bends,velocityLevels=len(velocities),leadRange=[min(lead),max(lead)],seconds=round(time+2.8,3),leadHash=hashlib.sha256(bytes(lead)).hexdigest(),passMidi=True)
    if check_audio:
        audio=ROOT/t['audio'];assert audio.exists() and audio.stat().st_size>100000
        assert hashlib.sha256(audio.read_bytes()).hexdigest()==t['audioSha256']
        ff=imageio_ffmpeg.get_ffmpeg_exe()
        decoded=subprocess.run([ff,'-v','error','-i',str(audio),'-f','f32le','-ar','22050','-ac','2','-'],check=True,stdout=subprocess.PIPE).stdout
        samples=np.frombuffer(decoded,dtype='<f4').reshape(-1,2)
        assert np.isfinite(samples).all();peak=float(np.max(np.abs(samples)));assert .1<peak<.99,(t['id'],peak)
        assert abs(len(samples)/22050-t['duration'])<.2
        # Check the interior in 250-ms windows; reverb/coda tails intentionally decay at the end.
        y=np.mean(samples,axis=1);width=5512
        rms=np.array([np.sqrt(np.mean(y[j:j+width]**2)) for j in range(0,len(y)-width,width)])
        interior=rms[8:-16];assert np.min(interior)>.0001,(t['id'],'unexpected interior silence')
        cmd=[ff,'-hide_banner','-nostats','-i',str(audio),'-af','ebur128=peak=true','-f','null','-']
        log=subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,check=True).stderr.decode()
        summary=log[log.rfind('Summary:'):]
        lufs=float(re.search(r'I:\s*(-?[\d.]+) LUFS',summary)[1]);truepeak=float(re.search(r'Peak:\s*(-?[\d.]+) dBFS',summary)[1])
        assert -20<lufs<-14 and truepeak<-.7,(t['id'],lufs,truepeak)
        corr=float(np.corrcoef(samples.T)[0,1]);assert corr>.15,('mono compatibility',t['id'],corr)
        result.update(passAudio=True,lufs=lufs,truePeakDb=truepeak,decodedPeak=round(peak,4),stereoCorrelation=round(corr,3),bytes=audio.stat().st_size)
    print('PASS',t['id'],t['title'],flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--midi-only',action='store_true');args=p.parse_args()
    album=json.loads((ROOT/'album.json').read_text());tracks=album['tracks']
    assert len(tracks)==30 and len(list((ROOT/'midi').glob('*.mid')))==30
    assert len({t['title'] for t in tracks})==len({t['slug'] for t in tracks})==30
    with ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda t:check_track(t,not args.midi_only),tracks))
    assert len({r['leadHash'] for r in rows})==30,'duplicate melodies'
    assert len({t['bpm'] for t in tracks})>=20 and len({t['meter'] for t in tracks})>=5 and len({t['mode'] for t in tracks})>=6
    report={'task':'MUSIC.01','tracks':30,'totalSeconds':round(sum(t['duration'] for t in tracks),3),'allPass':True,'method':'Parsed exported MIDI and independently decoded rendered MP3. Technical checks do not establish artistic approval or human listening.','tracksChecked':rows}
    OUT.mkdir(exist_ok=True,parents=True);(OUT/('midi-validation.json' if args.midi_only else 'validation.json')).write_text(json.dumps(report,indent=2)+'\n')
    print('All 30 tracks passed.')
