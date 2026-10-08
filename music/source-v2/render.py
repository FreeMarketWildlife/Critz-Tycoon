"""Original fixed-pitch instruments. Reads the exported MIDI, not the notation source.
No detuning, pitch envelopes, vibrato, wow, chorus, reference samples or presets.
"""
from pathlib import Path
from collections import defaultdict,deque
from concurrent.futures import ProcessPoolExecutor,as_completed
import argparse,json,math,subprocess,tempfile,hashlib
import numpy as np
from scipy import signal
import soundfile as sf
import mido,imageio_ffmpeg
from score import ROOT,PATCHES
SR=32000
PROGRAMS={v:k for k,v in PATCHES.items()}
RELEASE={'felt':.8,'epiano':.55,'bell':.9,'box':.8,'vibes':.7,'marimba':.18,'organ':.15,'nylon':.35,'pluck':.2,'upright':.22,'sub':.2,'strings':.9,'brass':.2,'reed':.2,'flute':.3,'square':.12,'saw':.16,'triangle':.17,'pulse':.12,'air':1.5,'sine':.5,'glass':1.3,'bubble':.14}

def read_midi(path):
    mid=mido.MidiFile(path,charset='utf-8');time=0;active=defaultdict(deque);notes=[];patch={};vol={};pan={};wet={}
    for msg in mid:
        time+=msg.time
        if msg.is_meta:continue
        c=msg.channel
        if msg.type=='program_change':patch[c]=PROGRAMS[msg.program]
        elif msg.type=='pitchwheel':assert msg.pitch==0
        elif msg.type=='control_change':
            if msg.control in [1,65,93]:assert msg.value==0
            if msg.control==7:vol[c]=msg.value/127
            if msg.control==10:pan[c]=msg.value/127
            if msg.control==91:wet[c]=msg.value/127
        elif msg.type=='note_on' and msg.velocity:active[c,msg.note].append((time,msg.velocity))
        elif msg.type=='note_off' or (msg.type=='note_on' and not msg.velocity):
            assert active[c,msg.note],('orphan',c,msg.note)
            at,v=active[c,msg.note].popleft();notes.append((at,time-at,c,msg.note,v))
    assert not any(active.values())
    return notes,patch,vol,pan,wet,time

def tone(patch,n,d,velocity=80):
    f=440*2**((n-69)/12);release=RELEASE[patch];t=np.arange(round((d+release)*SR),dtype=np.float64)/SR
    phase=2*np.pi*f*t;out=np.zeros(len(t));attack=.009;decay=.4;sustain=.8
    maxh=min(40,int((SR*.45)/f))
    if patch in ['sine','sub']:
        out=np.sin(phase)
        if patch=='sub':out+=.08*np.sin(2*phase);attack=.015;sustain=.8
        else:attack=.05;sustain=1
    elif patch=='triangle':
        for h in range(1,maxh+1,2):out+=(-1)**((h-1)//2)*np.sin(h*phase)/(h*h)
        out*=.82;attack=.02;sustain=.85
    elif patch in ['square','pulse','saw','strings','air','brass','reed']:
        cutoff={'square':4200,'pulse':3400,'saw':3100,'strings':2100,'air':1000,'brass':2300,'reed':3000}[patch]
        for h in range(1,maxh+1):
            if patch in ['square','reed']:
                if h%2==0:continue
                coeff=1/h if patch=='square' else 1/(h**1.3)
                out+=coeff*np.sin(h*phase)*math.exp(-(h*f/cutoff)**2)
            elif patch=='pulse':
                coeff=2*np.sin(np.pi*h*.28)/(np.pi*h)
                out+=coeff*np.cos(h*phase-np.pi*h*.28)*math.exp(-(h*f/cutoff)**2)
            else:out+=np.sin(h*phase)*(-1)**(h+1)/h*math.exp(-(h*f/cutoff)**2)
        out*=.72 if patch!='pulse' else 1.4
        attack={'air':.45,'strings':.2,'brass':.065,'reed':.035}.get(patch,.016)
        sustain=.9 if patch in ['air','strings'] else .75
    elif patch=='organ':
        for h,a in [(1,.65),(2,.32),(3,.12),(4,.08),(6,.025)]:
            if h<=maxh:out+=a*np.sin(h*phase)
        attack=.018;sustain=1
    elif patch in ['felt','epiano','nylon','pluck','upright']:
        if patch=='epiano':
            out=.85*np.sin(phase+.65*np.exp(-t*6)*np.sin(2*phase))+.06*np.sin(3*phase)*np.exp(-t*3)
            decay=.6;sustain=.25
        else:
            strength={'felt':1.9,'nylon':1.65,'pluck':1.3,'upright':2.2}[patch]
            for h in range(1,min(maxh,18)+1):
                coeff=1/(h**strength)
                if patch=='nylon':coeff*=math.cos(h*np.pi*.12)
                out+=coeff*np.sin(h*phase)*np.exp(-t*(.35+(h-1)*({'felt':2.2,'nylon':1.5,'pluck':3.7,'upright':4.0}[patch])))
            out*=.8;decay={'felt':.8,'nylon':.48,'pluck':.12,'upright':.23}[patch];sustain={'felt':.4,'nylon':.3,'pluck':.1,'upright':.5}[patch]
        attack=.007 if patch!='felt' else .012
    elif patch in ['bell','box','vibes','marimba','glass']:
        spectra={'bell':[(1,.8,.3),(2,.22,2),(4,.12,3),(6,.03,6)],'box':[(1,.8,.5),(3,.22,2.8),(5,.05,7)],'vibes':[(1,.95,.3),(4,.13,5),(7,.02,10)],'marimba':[(1,.95,1),(4,.22,13),(8,.04,25)],'glass':[(1,.76,.25),(2,.12,1.5),(4,.14,2),(6,.03,5)]}
        for h,a,dec in spectra[patch]:
            if h<=maxh:out+=a*np.sin(h*phase)*np.exp(-t*dec)
        attack=.007;decay=.3 if patch!='marimba' else .08;sustain=.35 if patch!='marimba' else .2
    elif patch=='flute':
        out=.9*np.sin(phase)+.11*np.sin(2*phase)+.025*np.sin(3*phase);attack=.05;sustain=.9
    elif patch=='bubble':
        out=.85*np.sin(phase+.7*np.exp(-t*10)*np.sin(2*phase));attack=.009;decay=.12;sustain=.28
    else:raise ValueError(patch)
    # Raised-cosine attack and release: no hard waveform edges.
    env=.5-.5*np.cos(np.pi*np.minimum(1,t/attack))
    env*=sustain+(1-sustain)*np.exp(-np.maximum(0,t-attack)/decay)
    env*=np.where(t>d,(.5+.5*np.cos(np.pi*np.minimum(1,(t-d)/release)))**2,1)
    return (out*env*(velocity/127)**1.35).astype(np.float32)

def drum(n,v,seed):
    rng=np.random.default_rng(seed);dur={36:.28,37:.06,38:.18,42:.06,45:.25,47:.2,75:.065}.get(n,.2)
    t=np.arange(round(dur*SR))/SR;noise=rng.normal(0,1,len(t))
    if n==36:
        phase=2*np.pi*(48*t+1.6*(1-np.exp(-35*t)));w=np.sin(phase)*np.exp(-t*16)+.035*noise*np.exp(-t*180)
    elif n==38:
        hp=signal.sosfilt(signal.butter(2,[1200,6500],fs=SR,btype='bandpass',output='sos'),noise)
        w=.34*hp*np.exp(-t*28)+.22*np.sin(2*np.pi*175*t)*np.exp(-t*36)
    elif n==42:
        hp=signal.sosfilt(signal.butter(2,[4800,10500],fs=SR,btype='bandpass',output='sos'),noise)
        w=.24*hp*np.exp(-t*65)
    elif n in [45,47]:w=.62*np.sin(2*np.pi*(110 if n==45 else 150)*t)*np.exp(-t*19)
    else:w=.35*(np.sin(2*np.pi*(1100 if n==37 else 780)*t)+.3*np.sin(2*np.pi*1870*t))*np.exp(-t*80)
    w*=np.minimum(1,t/.002)*np.minimum(1,(dur-t)/.005)
    return (w*(v/127)**1.35).astype(np.float32)

def render(track):
    notes,patches,vol,pan,wet,length=read_midi(ROOT/track['midi']);N=round((length+3)*SR)
    mix=np.zeros((N,2),np.float32);send=np.zeros_like(mix)
    for i,(at,d,c,n,v) in enumerate(notes):
        w=drum(n,v,track['id']*10000+i) if c==9 else tone(patches[c],n,d,v)
        w*=vol[c]*(.8 if c==9 else .42)
        p=pan[c];stereo=w[:,None]*np.array([math.cos(p*np.pi/2),math.sin(p*np.pi/2)])
        offset=round(at*SR);size=min(len(w),N-offset)
        mix[offset:offset+size]+=stereo[:size];send[offset:offset+size]+=stereo[:size]*wet[c]
    # One short room, no duplicated voices or pitch modulation. Atmospheric patches have longer releases.
    rt=np.arange(round(SR*1.4))/SR;rng=np.random.default_rng(882)
    ir=rng.normal(0,1,(len(rt),2))*np.exp(-rt[:,None]*5.5/1.4);ir[:round(SR*.035)]=0
    ir=signal.sosfilt(signal.butter(2,3800,fs=SR,output='sos'),ir,axis=0);ir/=np.sqrt(np.sum(ir**2,axis=0));ir*=.38
    for c in range(2):mix[:,c]+=signal.fftconvolve(send[:,c],ir[:,c])[:N]
    mix=signal.sosfilt(signal.butter(2,24,fs=SR,btype='highpass',output='sos'),mix,axis=0).astype(np.float32)
    mix=signal.sosfilt(signal.butter(2,9500,fs=SR,output='sos'),mix,axis=0).astype(np.float32)
    mix[-round(.3*SR):]*=np.linspace(1,0,round(.3*SR))[:,None]
    peak=float(np.max(np.abs(mix)));assert 0<peak and np.isfinite(mix).all()
    out=ROOT/track['audio'];out.parent.mkdir(parents=True,exist_ok=True)
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    with tempfile.TemporaryDirectory(prefix='critz-m2-') as td:
        wav=Path(td)/'mix.wav';sf.write(wav,mix,SR,subtype='FLOAT')
        analysis=subprocess.run([ff,'-hide_banner','-i',str(wav),'-af','loudnorm=I=-19:TP=-2:LRA=15:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
        measures=json.JSONDecoder().raw_decode(analysis.stderr[analysis.stderr.rfind('{'):])[0]
        filt='loudnorm=I=-19:TP=-2:LRA=15:linear=true:'+':'.join(f'{k}={measures[v]}' for k,v in [('measured_I','input_i'),('measured_LRA','input_lra'),('measured_TP','input_tp'),('measured_thresh','input_thresh'),('offset','target_offset')])
        subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-i',str(wav),'-af',filt,'-ar','44100','-c:a','libmp3lame','-b:a','128k','-metadata',f'title={track["title"]}','-metadata','album=Critz: Tycoon - Thirty Different Days','-metadata','artist=Critz: Tycoon / Codex','-metadata',f'track={track["id"]}/30',str(out)],check=True)
    mono=np.max(np.abs(mix),axis=1)
    return dict(id=track['id'],audioSha256=hashlib.sha256(out.read_bytes()).hexdigest(),audioBytes=out.stat().st_size,waveform=[round(float(x.max())/peak,3) for x in np.array_split(mono,160)],rawPeak=peak,seconds=round(N/SR,4),duration=round(N/SR,3))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--ids',default='');a=parser.parse_args();ids={int(i) for i in a.ids.split(',') if i}
    album=json.loads((ROOT/'album.json').read_text())
    with ProcessPoolExecutor(max_workers=3) as pool:
        jobs={pool.submit(render,t):t for t in album['tracks'] if not ids or t['id'] in ids}
        for job in as_completed(jobs):
            t=jobs[job];r=job.result();(ROOT/'v2/audio'/f'{t["slug"]}.render.json').write_text(json.dumps(r)+'\n');print(f'{t["id"]:02d} rendered {r["seconds"]:.1f}s',flush=True)
    for t in album['tracks']:
        p=ROOT/'v2/audio'/f'{t["slug"]}.render.json'
        if p.exists():t.update(json.loads(p.read_text()))
    (ROOT/'album.json').write_text(json.dumps(album,ensure_ascii=False,indent=2)+'\n')
