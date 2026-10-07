#!/usr/bin/env python3
"""Render the actual MIDI performances through original procedural synth patches.
Reproducible local instruments; no external samples or copyrighted sound banks.
"""
from pathlib import Path
from collections import defaultdict,deque
import argparse, json, math, subprocess, tempfile, hashlib
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
from scipy import signal
import soundfile as sf
import mido, imageio_ffmpeg
from compose import PATCHES
ROOT=Path(__file__).resolve().parents[1]
SR=32000
PROGRAMS={v:k for k,v in PATCHES.items()}

def read_midi(path):
    mid=mido.MidiFile(path,charset='utf-8');time=0.;active=defaultdict(deque);notes=[]
    patch={};controls=defaultdict(list);pitch=defaultdict(list);volume={};pan={}
    for msg in mid:
        time+=msg.time
        if msg.is_meta:continue
        c=msg.channel
        if msg.type=='program_change':patch[c]=PROGRAMS[msg.program]
        elif msg.type=='control_change':
            controls[c,msg.control].append((time,msg.value))
            if msg.control==7:volume[c]=msg.value/127
            if msg.control==10:pan[c]=msg.value/127
        elif msg.type=='pitchwheel':pitch[c].append((time,msg.pitch/4096))
        elif msg.type=='note_on' and msg.velocity:
            active[c,msg.note].append((time,msg.velocity))
        elif msg.type=='note_off' or (msg.type=='note_on' and not msg.velocity):
            assert active[c,msg.note],('orphan',c,msg.note)
            at,vel=active[c,msg.note].popleft();notes.append((at,time-at,c,msg.note,vel))
    assert not any(active.values()),'stuck notes'
    return notes,patch,controls,pitch,volume,pan,time

def env(t,d,attack,release,decay=0.,sustain=.8):
    e=np.minimum(1,t/max(.002,attack))
    if decay:e*=sustain+(1-sustain)*np.exp(-np.maximum(0,t-attack)/decay)
    e*=np.where(t>d,np.exp(-(t-d)/(release/5)),1)
    # Exactly zero at both edges keeps releases click-free.
    e*=np.minimum(1,np.maximum(0,d+release-t)/.012)
    return e

def curve(points,times,default):
    if not points:return np.full_like(times,default)
    x,y=zip(*points);return np.interp(times,x,y,left=y[0],right=y[-1])

def tone(patch,n,d,bends,mod,seed):
    f=440*2**((n-69)/12)
    release={'pad':.72,'glass':.65,'musicbox':.62,'epiano':.40,'ghost':.75,'marimba':.22,'pluck':.18}.get(patch,.16)
    size=max(1,int((d+release)*SR));t=np.arange(size,dtype=np.float64)/SR
    bends=bends(t);vibrato=mod*.0011*np.sin(2*np.pi*5.2*t)*np.minimum(1,t/.25)
    phase=2*np.pi*np.cumsum(f*2**((bends+vibrato)/12))/SR
    if patch=='epiano':
        wave=np.sin(phase+1.35*np.exp(-t*5.0)*np.sin(phase*2))*.8+np.sin(phase*3)*.11*np.exp(-t*2)
        envelope=env(t,d,.009,release,.45,.35)*np.exp(-t*.20)
    elif patch in ['glass','musicbox']:
        ratio=2.997 if patch=='glass' else 3.997
        wave=np.sin(phase)*.75+np.sin(phase*ratio)*.19*np.exp(-t*4)+np.sin(phase*6.01)*.06*np.exp(-t*8)
        envelope=env(t,d,.006,release,.35,.30)*np.exp(-t*(.8 if patch=='glass' else 1.1))
    elif patch=='marimba':
        wave=np.sin(phase)+np.sin(phase*3.99)*.23*np.exp(-t*16)+np.sin(phase*9.98)*.06*np.exp(-t*25)
        envelope=env(t,d,.004,release,.13,.25)*np.exp(-t*1.5)
    elif patch=='bubble':
        wave=.72*np.sin(phase+1.05*np.exp(-t*8)*np.sin(phase*2))+.2*np.sin(phase*2)*np.exp(-t*4)
        envelope=env(t,d,.008,release,.16,.7)
    elif patch in ['flute','velvet','ghost']:
        wave=np.sin(phase)+(.16 if patch=='flute' else .24)*np.sin(phase*2)+.07*np.sin(phase*3)
        if patch=='ghost':wave=.70*wave+.22*np.sin(phase*1.003+1.4*np.sin(2*np.pi*.8*t))
        envelope=env(t,d,.035 if patch!='ghost' else .09,release,.2,.8)
    elif patch=='pad':
        wave=.45*np.sin(phase)+.24*np.sin(phase*1.003)+.24*np.sin(phase*.997)+.10*np.sin(phase*2)
        envelope=env(t,d,.23,release,.4,.8)
    elif patch=='bass':
        wave=np.sin(phase)*.85+np.sin(phase*2)*.24*np.exp(-t*4)+np.sin(phase*3)*.12*np.exp(-t*6)
        envelope=env(t,d,.007,release,.12,.65)
    elif patch=='organ':
        wave=.6*np.sin(phase)+.3*np.sin(phase*2)+.15*np.sin(phase*3)+.08*np.sin(phase*4)
        envelope=env(t,d,.008,release,.1,.85)
    else:
        # Band-limited additive oscillators; no aliased sign(sin) waveforms.
        harmonics=range(1,min(13,int(SR*.44/f))+1)
        wave=np.zeros(size)
        for h in harmonics:
            if patch=='square' and h%2==0:continue
            weight=1/(h**(1.4 if patch in ['reed','pluck'] else 1.25))
            if patch=='brass':weight*=min(1,h/2)
            brightness=np.exp(-t*(h-1)*(.8 if patch=='pluck' else .09))
            wave+=weight*np.sin(phase*h)*brightness
        wave*=.68
        if patch=='reed':wave=.76*wave+.24*np.sin(phase)
        envelope=env(t,d,.025 if patch=='brass' else .012,release,.15,.73 if patch!='pluck' else .28)
        if patch=='pluck':envelope*=np.exp(-t*2)
    return (wave*envelope).astype(np.float32)

def drum(n,v,seed):
    rng=np.random.default_rng(seed);duration={36:.38,38:.25,37:.09,42:.075,46:.22,49:1.1,45:.35,47:.3,75:.09}.get(n,.2)
    t=np.arange(int(duration*SR))/SR;noise=rng.normal(0,1,len(t))
    if n==36:
        ph=2*np.pi*np.cumsum(48+115*np.exp(-t*35))/SR
        w=np.sin(ph)*np.exp(-t*12)+noise*.055*np.exp(-t*130)
    elif n==38:
        hp=signal.sosfilt(signal.butter(2,1400,fs=SR,btype='high',output='sos'),noise)
        w=hp*.40*np.exp(-t*22)+np.sin(2*np.pi*185*t)*.35*np.exp(-t*30)
    elif n==37:
        w=(np.sin(2*np.pi*1700*t)+.5*np.sin(2*np.pi*2300*t)+noise*.15)*np.exp(-t*75)*.55
    elif n in [42,46,49]:
        hp=signal.sosfilt(signal.butter(2,5700,fs=SR,btype='high',output='sos'),noise)
        w=hp*.38*np.exp(-t*(65 if n==42 else 19 if n==46 else 5))
    elif n in [45,47]:
        ph=2*np.pi*np.cumsum((108 if n==45 else 145)+40*np.exp(-t*25))/SR
        w=np.sin(ph)*np.exp(-t*15)+noise*.07*np.exp(-t*30)
    else:w=(np.sin(2*np.pi*780*t)+.35*np.sin(2*np.pi*1560*t))*np.exp(-t*62)*.6
    w*=np.minimum(1,t/.0015)*np.minimum(1,(duration-t)/.006)
    return (w*(v/127)**1.25).astype(np.float32)

def render(track):
    notes,patches,controls,pitches,volumes,pans,length=read_midi(ROOT/track['midi'])
    N=int((length+2.8)*SR);mix=np.zeros((N,2),dtype=np.float32);send=np.zeros_like(mix)
    gains={0:.29,1:.22,2:.135,3:.35,4:.17,5:.11,9:.40}
    wet={0:.24,1:.3,2:.18,3:.025,4:.35,5:.43,9:.085}
    for idx,(at,d,c,n,vel) in enumerate(notes):
        offset=round(at*SR)
        if c==9:w=drum(n,vel,track['id']*100000+idx)
        else:
            bend=lambda ts:curve(pitches[c],ts+at,0)
            mod=float(curve(controls[c,1],np.array([at]),0)[0])
            w=tone(patches[c],n,d,bend,mod,idx)*(vel/127)**1.25
            ex=curve(controls[c,11],np.arange(len(w))/SR+at,100)/100
            w*=ex.astype(np.float32)
        w*=gains[c]*volumes[c]
        p=pans[c]
        if c in [2,4,5]:p=np.clip(p+(n%5-2)*.05,.1,.9)
        if c==9:p=.5 if n in [36,38,37] else .60 if n in [42,46] else .35
        size=min(len(w),N-offset);w=w[:size]
        stereo=w[:,None]*np.array([math.cos(p*np.pi/2),math.sin(p*np.pi/2)],dtype=np.float32)
        mix[offset:offset+size]+=stereo;send[offset:offset+size]+=stereo*wet[c]
    # Short tempo-synced echoes, deliberately quieter than the direct melody.
    delay=60/track['bpm']*(.75 if track['groove'] not in ['battle','urgent'] else .5)
    for tap in range(1,5):
        shift=round(delay*tap*SR)
        if shift<N:mix[shift:]+=send[:-shift,::-1 if tap%2 else 1]*(.43**tap)
    # Deterministic diffuse room, not a downloaded impulse response.
    rng=np.random.default_rng(713+track['id']);seconds=1.45 if track['groove'] in ['ambient','stealth'] else .8
    rt=np.arange(int(seconds*SR))/SR
    ir=rng.normal(0,1,(len(rt),2))*np.exp(-rt[:,None]*6/seconds)
    ir[:int(.023*SR)]=0
    ir=signal.sosfilt(signal.butter(2,4300,fs=SR,output='sos'),ir,axis=0)
    ir/=np.sqrt(np.sum(ir**2,axis=0));ir*=.30
    for c in range(2):mix[:,c]+=signal.fftconvolve(send[:,c],ir[:,c],mode='full')[:N]
    # Tape softness and slow wow belong only to the lo-fi cues.
    if track['groove']=='lofi':
        times=np.arange(N);wow=times+SR*.0005*np.sin(2*np.pi*.48*times/SR)
        for c in range(2):mix[:,c]=np.interp(wow,times,mix[:,c])
        mix=np.tanh(mix*1.15)/1.15
    cutoff=5600 if track['groove']=='lofi' else 8500
    mix=signal.sosfilt(signal.butter(2,cutoff,fs=SR,output='sos'),mix,axis=0).astype(np.float32)
    mix=signal.sosfilt(signal.butter(2,27,fs=SR,btype='high',output='sos'),mix,axis=0).astype(np.float32)
    mix[:320]*=np.linspace(0,1,320)[:,None]
    mix[-int(SR*.6):]*=np.linspace(1,0,int(SR*.6))[:,None]
    peak=float(np.max(np.abs(mix))); assert np.isfinite(mix).all() and peak>0
    mix*=min(2,.85/peak)
    out=ROOT/track['audio'];out.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='critz-render-') as td:
        wav=Path(td)/'mix.wav';sf.write(wav,mix,SR,subtype='FLOAT')
        command=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y','-i',str(wav),'-af','loudnorm=I=-17:TP=-1.8:LRA=10','-ar','44100','-c:a','libmp3lame','-b:a','128k','-metadata',f'title={track["title"]}','-metadata','album=Critz: Tycoon - A Tiny World','-metadata','artist=Critz: Tycoon / Codex','-metadata',f'track={track["id"]}/30',str(out)]
        subprocess.run(command,check=True)
    # Small waveform envelope makes the listening room usable without decoding every file.
    mono=np.max(np.abs(mix),axis=1);bins=np.array_split(mono,200)
    waveform=[round(float(np.max(x))/max(.001,float(np.max(mono))),3) for x in bins]
    return {'id':track['id'],'audioSha256':hashlib.sha256(out.read_bytes()).hexdigest(),'audioBytes':out.stat().st_size,'waveform':waveform,'rawPeak':peak,'seconds':N/SR}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--ids',default='');args=parser.parse_args()
    album=json.loads((ROOT/'album.json').read_text());ids={int(i) for i in args.ids.split(',') if i}
    selected=[t for t in album['tracks'] if not ids or t['id'] in ids]
    with ProcessPoolExecutor(max_workers=3) as pool:
        pending={pool.submit(render,t):t for t in selected}
        for job in as_completed(pending):
            track=pending[job];result=job.result()
            (ROOT/'audio'/f'{track["slug"]}.render.json').write_text(json.dumps(result))
            print(f'{track["id"]:02d}/30  {track["title"]}  {result["seconds"]:.1f}s',flush=True)
    # Merge per-file receipts so interrupted render runs can resume cleanly.
    for track in album['tracks']:
        receipt=ROOT/'audio'/f'{track["slug"]}.render.json'
        if receipt.exists():track.update(json.loads(receipt.read_text()))
    (ROOT/'album.json').write_text(json.dumps(album,ensure_ascii=False,indent=2)+'\n')
