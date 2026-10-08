"""Independent event, diversity, tuning and decoded-audio checks; not aesthetic approval."""
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import json,hashlib,itertools,math,subprocess,re,sys,zipfile
import mido,numpy as np,imageio_ffmpeg
from score import ROOT,PATCHES
from render import tone,SR
OUT=ROOT.parent/'docs/reviews/MUSIC-02';OUT.mkdir(parents=True,exist_ok=True)

def midi_info(path):
    mid=mido.MidiFile(path,charset='utf-8');assert mid.type==1 and mid.ticks_per_beat>0
    voices=defaultdict(list);held={};notes=[];bends=0;tracks=0;tempos=[];meters=[];markers=[]
    for tr in mid.tracks:
        tick=0;thisnotes=0
        for m in tr:
            tick+=m.time;assert m.time>=0
            if m.is_meta:
                if m.type=='set_tempo':tempos.append(m.tempo)
                if m.type=='time_signature':meters.append(f'{m.numerator}/{m.denominator}')
                if m.type=='marker':markers.append(m.text)
                continue
            if m.type=='pitchwheel' and m.pitch!=0:bends+=1
            if m.type=='note_on' and m.velocity:
                key=(m.channel,m.note);assert key not in held,(path.name,'overlapping identical pitch',key)
                held[key]=(tick,m.velocity);thisnotes+=1
            elif m.type=='note_off' or (m.type=='note_on' and not m.velocity):
                key=(m.channel,m.note);assert key in held,(path.name,'orphan',key)
                start,v=held.pop(key);assert tick>start
                notes.append((start/mid.ticks_per_beat,(tick-start)/mid.ticks_per_beat,m.channel,m.note,v))
        if thisnotes:tracks+=1
    assert not held
    for n in sorted(notes):voices[n[2]].append(n)
    lead=voices[0]
    # Six-note contours include rhythm/spacing. Absolute key and BPM are removed.
    fingerprints=set()
    for i in range(len(lead)-5):
        group=lead[i:i+6]
        fingerprints.add(tuple((group[j+1][3]-group[j][3],round(group[j+1][0]-group[j][0],2)) for j in range(5)))
    return dict(notes=notes,lead=lead,fingerprints=fingerprints,bends=bends,tracks=tracks,tempos=tempos,meters=meters,markers=markers,duration=mid.length)

def decoded_audio(t):
    ff=imageio_ffmpeg.get_ffmpeg_exe();p=ROOT/t['audio']
    raw=subprocess.run([ff,'-hide_banner','-loglevel','error','-i',str(p),'-f','f32le','-ar','22050','-ac','2','-'],capture_output=True,check=True).stdout
    x=np.frombuffer(raw,dtype='<f4').reshape(-1,2);assert np.isfinite(x).all() and len(x)>0
    peak=float(np.max(np.abs(x)));assert 0<peak<.93,(t['id'],peak)
    duration=len(x)/22050;assert abs(duration-t['duration'])<.08,(t['id'],duration,t['duration'])
    measurement=subprocess.run([ff,'-hide_banner','-i',str(p),'-af','loudnorm=I=-19:TP=-2:LRA=15:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    a=json.JSONDecoder().raw_decode(measurement.stderr[measurement.stderr.rfind('{'):])[0]
    assert -21<float(a['input_i'])<-17,(t['id'],a)
    assert float(a['input_tp'])<=-1.4,(t['id'],a)
    correlation=float(np.corrcoef(x.T)[0,1]);assert correlation>.4
    windows=[np.sqrt(np.mean(w*w)) for w in np.array_split(x,math.ceil(duration*2))]
    return dict(id=t['id'],seconds=round(duration,3),integratedLUFS=float(a['input_i']),truePeakDBTP=float(a['input_tp']),loudnessRangeLU=float(a['input_lra']),stereoCorrelation=round(correlation,4),quietHalfSecondWindows=int(sum(r<.0005 for r in windows)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def main():
    album=json.loads((ROOT/'album.json').read_text());ts=album['tracks'];assert len(ts)==30
    infos=[midi_info(ROOT/t['midi']) for t in ts]
    for t,d in zip(ts,infos):
        assert d['bends']==0 and d['tracks']==len(t['instruments'])
        assert len(d['notes'])==t['noteCount']
        assert d['meters']==[t['meter']]
        assert len(d['tempos'])==1 and abs(mido.tempo2bpm(d['tempos'][0])-t['bpm'])<.001
        assert len(d['markers'])==len(t['sections'])>=2
        assert abs(d['duration']+3-t['duration'])<.01
        assert hashlib.sha256((ROOT/t['midi']).read_bytes()).hexdigest()==t['midiSha256']
    def similar(a,b):return len(a&b)/max(1,min(len(a),len(b)))
    pairs=sorted([dict(a=ts[i]['id'],b=ts[j]['id'],sharedFraction=round(similar(infos[i]['fingerprints'],infos[j]['fingerprints']),4)) for i,j in itertools.combinations(range(30),2)],key=lambda x:-x['sharedFraction'])
    assert pairs[0]['sharedFraction']<.3,pairs[:5]
    assert len({t['bpm'] for t in ts})==30
    assert len({t['midiSha256'] for t in ts})==30
    old=[];prior=Path('/tmp/critz-music-02/old-midi')
    if prior.exists():
        # Previous files may have overlapping pitches in other voices; first-track contour alone is enough for this comparison.
        for path in sorted(prior.glob('*.mid')):
            mid=mido.MidiFile(path,charset='utf-8');ev=[];beat=0
            for m in mid.tracks[1]:
                beat+=m.time/mid.ticks_per_beat
                if m.type=='note_on' and m.velocity:ev.append((beat,m.note))
            fp={tuple((ev[i+j+1][1]-ev[i+j][1],round(ev[i+j+1][0]-ev[i+j][0],2)) for j in range(5)) for i in range(len(ev)-5)}
            old.append((path.name,fp))
    previous=[dict(id=t['id'],maxSharedFraction=round(max((similar(info['fingerprints'],f) for _,f in old),default=0),4)) for t,info in zip(ts,infos)]
    if old:assert max(p['maxSharedFraction'] for p in previous)<.3
    tuning=[]
    for patch in PATCHES:
        sample=tone(patch,69,1.5,90);segment=sample[round(.2*SR):round(1.2*SR)]
        spectrum=np.abs(np.fft.rfft(segment*np.hanning(len(segment))));frequency=float(np.argmax(spectrum)*SR/len(segment))
        cents=1200*math.log2(frequency/440);assert abs(cents)<.1,(patch,cents)
        tuning.append(dict(patch=patch,peakHz=frequency,errorCents=round(cents,6)))
    spectra={p:np.abs(np.fft.rfft(tone(p,69,1.5)[6400:38400]*np.hanning(32000))) for p in ['sine','triangle','square','saw']}
    ratios={p:{'second':round(float(a[880]/a[440]),4),'third':round(float(a[1320]/a[440]),4)} for p,a in spectra.items()}
    assert ratios['sine']['third']<.001 and ratios['triangle']['third']>.1 and ratios['square']['third']>.2 and ratios['saw']['second']>.3
    with zipfile.ZipFile(ROOT/'critz-tycoon-30-midi.zip') as z:
        mids=[n for n in z.namelist() if n.endswith('.mid')];assert len(mids)==30
        for t in ts:assert z.read(Path(t['midi']).name)==(ROOT/t['midi']).read_bytes()
    with ProcessPoolExecutor(max_workers=3) as pool:audio=list(pool.map(decoded_audio,ts))
    for t,a in zip(ts,audio):assert a['sha256']==t['audioSha256']
    result=dict(status='PASS',scope='Technical validation only; listening acceptance remains with the user.',tracks=30,totalMinutes=round(sum(t['duration'] for t in ts)/60,2),tempos=sorted({t['bpm'] for t in ts}),tonalCentres=sorted({t['key'] for t in ts}),meters=sorted({t['meter'] for t in ts}),pitchedPatches=sorted({p['patch'] for t in ts for p in t['instruments'] if p['patch']!='drums'}),drumlessTracks=sum(all(p['patch']!='drums' for p in t['instruments']) for t in ts),nonzeroPitchWheels=0,partCounts=[len(t['instruments']) for t in ts],noteCounts=[t['noteCount'] for t in ts],highestContourOverlaps=pairs[:15],comparisonAgainstRejectedEdition=previous,comparisonLimit='Six-note interval/onset fingerprints detect literal/transposed shared phrases, not subjective similarity or all possible melodic relationships.',tuningChecks=tuning,waveformHarmonicRatios=ratios,audio=audio)
    (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['audio','tuningChecks','comparisonAgainstRejectedEdition','highestContourOverlaps','partCounts','noteCounts']},indent=2))
if __name__=='__main__':main()
