#!/usr/bin/env python3
"""Build the original MUSIC.01 scores as Type-1 MIDI, with expressive automation.
No reference-game notes, samples, recordings or soundfonts are inputs.
"""
from pathlib import Path
import json, math, re, hashlib, zipfile
import mido
from catalogue import TRACKS
ROOT=Path(__file__).resolve().parents[1]
PPQ=480
SCALES={'major':[0,2,4,5,7,9,11],'minor':[0,2,3,5,7,8,10],'dorian':[0,2,3,5,7,9,10],'lydian':[0,2,4,6,7,9,11],'mixolydian':[0,2,4,5,7,9,10],'phrygian':[0,1,3,5,7,8,10]}
PCS={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
DUR={'s':.25,'e':.5,'q':1,'d':1.5,'h':2,'w':4}
PATCHES={'reed':81,'glass':98,'bubble':84,'brass':62,'flute':73,'marimba':12,'musicbox':10,'velvet':85,'epiano':4,'ghost':91,'square':80,'saw':87,'pad':89,'pluck':24,'organ':16,'bass':38}
FORMS={
 'journey':[('Window',4,.42),('A · first steps',8,.78),('A · answering voices',8,.92),('B · new perspective',8,.9),('Breath',4,.48),('A · homeward',8,1),('Coda',4,.56)],
 'intimate':[('Alone',4,.36),('A · a thought',8,.64),('B · an answer',8,.73),('Breath',4,.35),('A · together',8,.82),('Coda',4,.42)],
 'suspense':[('A sound',4,.33),('A · listen',8,.62),('Breath',4,.4),('B · closer',8,.87),('A · understood',8,.75),('Coda',4,.35)],
 'action':[('Signal',4,.75),('A · movement',8,.93),('B · resistance',8,1),('Breath',4,.58),('A · resolve',8,1),('B · breakthrough',8,1),('A · finish',8,1),('Coda',4,.66)],
 'dream':[('Glow',4,.3),('A · drift',8,.62),('B · widening',8,.74),('Breath',4,.34),('A · return',8,.66),('Coda',4,.36)],
 'celebration':[('A spark',4,.66),('A · together',8,.95),('B · everybody',8,1),('Breath',4,.56),('A · once more',8,1),('Coda',4,.62)],
 'finale':[('Remember',4,.37),('A · today',8,.74),('B · tomorrow',8,.86),('Breath',4,.45),('A · friends',8,.86),('Title returns',8,.88),('Coda',4,.42)]}

def pc(note):
    return (PCS[note[0]]+note.count('#')-note.count('b'))%12

def degree(n,t,octave=5):
    q,r=divmod(int(n)-1,7)
    register=-12 if pc(t['key'])>=6 or t['lead'] in ['velvet','epiano'] else 0
    return 12*(octave+1)+pc(t['key'])+SCALES[t['mode']][r]+12*q+register

def phrase(bar,t):
    result=[]; beat=0
    for token in bar.split():
        m=re.fullmatch(r'(R|-?\d+)([seqdhw])',token.strip()); assert m,token
        n,d=m.groups(); dur=DUR[d]
        result.append((beat,dur,None if n=='R' else degree(n,t)))
        beat+=dur
    beats=t['beats']; assert abs(beat-beats)<1e-8,(t['title'],bar,beat,beats)
    return result

def chord(symbol):
    m=re.fullmatch(r'([A-G][b#]?)(.*)',symbol); root,quality=m.groups(); r=pc(root)
    if quality.startswith('maj9'): ints=[0,4,7,11,14]
    elif quality.startswith('maj7'): ints=[0,4,7,11]
    elif quality=='m9': ints=[0,3,7,10,14]
    elif quality=='m7': ints=[0,3,7,10]
    elif quality=='m': ints=[0,3,7]
    elif quality=='13': ints=[0,4,10,14,21]
    elif quality=='9': ints=[0,4,7,10,14]
    elif quality=='7': ints=[0,4,7,10]
    elif quality=='6': ints=[0,4,7,9]
    else: assert not quality,quality; ints=[0,4,7]
    # Root below middle C, upper extensions remain audible without muddy close bass.
    notes=[48+r+i for i in ints]
    while sum(notes)/len(notes)<60: notes=[n+12 for n in notes]
    return r,notes

class Score:
    def __init__(self,t):
        self.t=t; self.events={c:[] for c in [0,1,2,3,4,5,9]}; self.notes=[]; self.markers=[]
    def event(self,c,b,msg,priority=2): self.events[c].append((max(0,round(b*PPQ)),priority,msg))
    def cc(self,c,b,k,v): self.event(c,b,mido.Message('control_change',channel=c,control=k,value=int(v)),1)
    def note(self,c,b,d,n,v=80,bend=0):
        assert 0<=n<=127 and d>0
        if c!=9:
            # All pitched parts use deterministic, very small timing/velocity accents.
            v=max(24,min(115,round(v+3*math.sin(b*2.91+n))))
        v=max(1,min(127,round(v)))
        self.event(c,b,mido.Message('note_on',channel=c,note=n,velocity=v),3)
        self.event(c,b+d,mido.Message('note_off',channel=c,note=n,velocity=0),0)
        self.notes.append(dict(channel=c,beat=round(b,4),duration=round(d,4),note=n,velocity=v))
        if bend:
            # Independent monophonic lead/counter channels; RPN range is +/-2 semitones.
            for frac,val in [(0,-bend),(.035,-bend*.75),(.08,-bend*.28),(.14,0)]:
                self.event(c,b+min(d*.5,frac),mido.Message('pitchwheel',channel=c,pitch=round(val*4096)),1)
            if d>.7:
                for j in range(1,9):
                    at=b+d*.45+(d*.48)*j/9
                    self.event(c,at,mido.Message('pitchwheel',channel=c,pitch=round(340*math.sin(j*1.8))),1)
            self.event(c,b+d,mido.Message('pitchwheel',channel=c,pitch=0),1)
    def save(self,path):
        t=self.t; mid=mido.MidiFile(type=1,ticks_per_beat=PPQ,charset="utf-8")
        conductor=mido.MidiTrack();mid.tracks.append(conductor)
        meta=[(0,mido.MetaMessage('track_name',name=t['title'])),(0,mido.MetaMessage('text',text='Critz: Tycoon / MUSIC.01 / original composition / review edition')),
              (0,mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(t['bpm']))),
              (0,mido.MetaMessage('time_signature',numerator=int(t['meter'].split('/')[0]),denominator=int(t['meter'].split('/')[1])))]
        for b,label in self.markers: meta.append((round(b*PPQ),mido.MetaMessage('marker',text=label)))
        meta.append((round(t['totalBeats']*PPQ),mido.MetaMessage('end_of_track')))
        prev=0
        for tick,msg in sorted(meta,key=lambda x:x[0]): conductor.append(msg.copy(time=tick-prev));prev=tick
        configs=[(0,'Lead',t['lead'],88,60),(1,'Answer',t['reply'],72,81),(2,'Harmony',t['keys'],67,43),(3,'Bass','bass',88,64),(4,'Little movements','glass' if t['groove'] in ['ambient','lullaby'] else 'pluck',54,93),(5,'Air','pad',42,35),(9,'Percussion',None,80,64)]
        for c,name,patch,vol,pan in configs:
            track=mido.MidiTrack();mid.tracks.append(track)
            track.append(mido.MetaMessage('track_name',name=f'{name} / {patch or "GM drums"}'))
            if patch: track.append(mido.Message('program_change',channel=c,program=PATCHES[patch]))
            for k,v in [(7,vol),(10,pan),(91,38),(93,16),(11,100)]: track.append(mido.Message('control_change',channel=c,control=k,value=v))
            if patch:
                for k,v in [(101,0),(100,0),(6,2),(38,0),(101,127),(100,127)]: track.append(mido.Message('control_change',channel=c,control=k,value=v))
            prev=0
            for tick,priority,msg in sorted(self.events[c],key=lambda x:(x[0],x[1])):
                track.append(msg.copy(time=tick-prev)); prev=tick
            end=round(t['totalBeats']*PPQ)
            track.append(mido.MetaMessage('end_of_track',time=max(0,end-prev)))
        mid.save(path)

def swung(beat,t):
    if t['groove'] not in ['shuffle','lofi','bounce']: return beat
    if abs(beat%1-.5)<.001:return beat+(.10 if t['groove']=='shuffle' else .055)
    return beat

def add_melody(s,bar,pattern,intensity,variant=0,channel=0):
    t=s.t; start=bar*t['beats']; notes=phrase(pattern,t)
    for i,(b,d,n) in enumerate(notes):
        if n is None:continue
        b2=swung(b,t); length=max(.10,d-(b2-b)-.065)
        vel=(78 if channel==0 else 65)*intensity+12
        if variant>=2 and i==0 and d>=1 and n>62 and t['groove'] not in ['ambient','stealth']:
            s.note(channel,start+b2,.11,n-2,vel*.7,bend=.22)
            b2+=.14;length-=.14
        # Development adds an occasional upper octave peak, not a wholesale transposition.
        if variant==3 and i==len(notes)-2 and d<=.5:n+=12
        bend=([.35,.7,.22,1.15][t['id']%4] if i%3==0 else 0)
        if t['lead'] in ['bubble','saw','ghost']:bend=max(bend,.7) if i%2==0 else bend
        s.note(channel,start+b2,length,n,vel,bend=bend)

def drums(s,bar,density):
    t=s.t; g=t['groove']; B=t['beats']; base=bar*B
    if density<.5 or g=='ambient':
        if g=='ambient' and bar%4==0:s.note(9,base,.2,75,30)
        return
    def hit(b,n,v,d=.12):
        if b<B:s.note(9,base+swung(b,t),d,n,v*density)
    if g in ['waltz','lullaby']:
        hit(0,36,68);hit(1.5 if t['meter']=='6/8' else 1,37,55)
        for b in [.5,1,2,2.5]:hit(b,42,31)
    elif g=='stealth':
        hit(0,36,48);hit(2.5,37,36);hit(3.5,75,43)
    elif g=='curious':
        for b in [0,2.5]:hit(b,36,60)
        for b in [1.5,4]:hit(b,37,55)
        for b in [0,1,2,3,4]:hit(b,42,32)
    elif g=='urgent':
        for b in [0,1.5,2.5]:hit(b,36,91)
        for b in [1,3]:hit(b,38,76)
        for k in range(int(B*2)):hit(k*.5,42,48 if k%2 else 57)
    elif g=='bossa':
        for b in [0,1.5,2,3.5]:hit(b,36,55)
        for b in [0,1.5,3]:hit(b,37,60)
        for b in [0,.5,1,1.5,2,2.5,3,3.5]:hit(b,42,30)
    else:
        kicks={'lofi':[0,1.75,2.5],'shuffle':[0,2,2.5],'funk':[0,.75,2.5,3.5],'battle':[0,1.5,2,2.75],'drive':[0,1,2,3],'town':[0,2],'bounce':[0,2.5],'celebrate':[0,1.5,2,3.5]}.get(g,[0,1.5,2.5])
        for b in kicks:hit(b,36,80 if g not in ['lofi','town'] else 65)
        for b in [1,3]:hit(b,37 if g in ['lofi','shuffle'] else 38,72)
        for k in range(8):hit(k*.5,46 if k==7 and bar%4==3 else 42,34+12*(k%2==0))
        if g=='lofi':hit(2.75,38,24)
    if bar%8==7 and density>.75:
        for j in range(4):hit(B-1+j*.25,47 if j<2 else 45,45+j*8)
    if bar%8==0 and density>.8 and g in ['battle','drive','adventure','celebrate','urgent']:hit(0,49,54,.8)

def compose(t):
    num,den=map(int,t['meter'].split('/'));t['beats']=num*4/den
    for p in t['A']+t['B']+t['answerA']+t['answerB']:phrase(p,t)
    s=Score(t); B=t['beats']; form=FORMS[t['form']]; cursor=0; passages=0; sections=[]
    totalbars=sum(n for _,n,_ in form)
    for secidx,(label,count,intensity) in enumerate(form):
        sections.append(dict(label=label,bar=cursor+1,seconds=round(cursor*B*60/t['bpm'],3)))
        s.markers.append((cursor*B,label))
        if secidx==1:s.markers.append((cursor*B,'LOOP_START'))
        if label=='Coda':s.markers.append((cursor*B,'LOOP_END'))
        isB=label.startswith('B'); quiet=label=='Breath'; intro=secidx==0; outro=label=='Coda'; title=label=='Title returns'
        if label.startswith('A'):passages+=1
        prog=t['bridge'] if isB or quiet else t['chords']
        for local in range(count):
            bar=cursor+local; at=bar*B
            symbol=prog[local%len(prog)]
            if outro and local>=2:symbol=t['chords'][0]
            root,voicing=chord(symbol)
            # Smooth inversion choices across chords while keeping the lead in its own register.
            voicing=[n-12 if n>74 else n for n in voicing]
            is_sparse=intro or outro or quiet
            for c in [0,1,2,3,4,5]:s.cc(c,at,11,min(118,round(73+35*intensity)));s.cc(c,at,1,12 if is_sparse else 27)
            # Harmony patterns are deliberately tied to scene/groove, not just a common arpeggiator.
            g=t['groove']; chord_vel=54+intensity*15
            if g in ['ambient','stealth'] or (is_sparse and t['keys']=='pad'):
                positions=[(0,B-.12)]
            elif g in ['waltz','lullaby']:
                positions=[(.03,.65),(1,.6),(2,.72)]
            elif g=='bossa':positions=[(0,.65),(1.5,.42),(2.5,.5),(3.5,.35)]
            elif g=='funk':positions=[(.5,.30),(1.75,.22),(2.5,.32),(3.5,.32)]
            elif g in ['battle','urgent']:positions=[(k,.35) for k in [0,1.5,2.5] if k<B]
            elif g=='lofi':positions=[(.04,1.6),(2.55,min(1.15,B-2.6))]
            elif g=='curious':positions=[(0,1.3),(2.5,1.3)]
            else:positions=[(0,.8),(2 if B>=4 else 1.5,.8)]
            if is_sparse:positions=positions[:1]
            for b,d in positions:
                if b+d>B:d=B-b-.07
                if d<=0:continue
                for j,n in enumerate(voicing):s.note(2,at+b+j*.009,d,n,chord_vel-(j%2)*4)
            # Bass is its own moving line, including fifths, octaves and chromatic approaches.
            bass=36+root
            if bass>47:bass-=12
            if is_sparse:bp=[(0,B*.8,bass)]
            elif g in ['waltz','lullaby']:bp=[(0,.9,bass),(1.5,.65,bass+7)]
            elif g in ['ambient','stealth']:bp=[(0,B*.7,bass)]
            elif g=='funk':bp=[(0,.4,bass),(.75,.3,bass+12),(1.5,.35,bass+7),(2.5,.4,bass),(B-.5,.3,bass+10)]
            elif g=='bossa':bp=[(0,.9,bass),(1.5,.45,bass+7),(2,.9,bass),(3.5,.35,bass+7)]
            elif g in ['battle','urgent','drive']:bp=[(k*.5,.36,bass+([0,0,12,7][k%4])) for k in range(int(B*2))]
            elif g=='curious':bp=[(0,1,bass),(2,.6,bass+7),(3.5,.7,bass+12)]
            else:bp=[(0,1.1,bass),(1.5,.35,bass+7),(2,.8,bass),(B-.5,.34,bass+7)]
            for b,d,n in bp:
                if b+d<=B:s.note(3,at+swung(b,t),min(d,B-swung(b,t)-.03),n,72*intensity+15)
            if local%4==3 and not is_sparse:
                nextroot,_=chord(prog[(local+1)%len(prog)])
                # Last half beat was already occupied in many grooves, so approach is a short pickup in the gap.
                if g in ['ambient','stealth','waltz','lullaby']:s.note(3,at+B-.25,.18,36+nextroot-1,53)
            # A quiet sustained layer appears only in broadened passages and atmospheric cues.
            if isB or g in ['ambient','stealth'] or (passages>=3 and not outro):
                for n in voicing[1:4]:s.note(5,at+.06,B-.14,n,35+intensity*10)
            pattern=(t['B'] if isB else t['A'])[local%4]
            if local>=4 and local%4>=2:
                pattern=t['answerB' if isB else 'answerA'][local%4-2]
            if title:pattern=TRACKS[0]['A'][local%4]
            if not (intro and local<2) and not quiet:
                # Last cadence explicitly comes to rest; longer album tails are outside loop markers.
                if outro and local>=2:
                    if local==2:s.note(0,at,B*1.72,degree(1,t),54,bend=.25)
                else:
                    variant=2 if passages>=2 and local>=4 else (1 if isB else 0)
                    add_melody(s,bar,pattern,intensity,variant)
            elif quiet and local%2==1:
                # A fragment is passed to the answering instrument during the break.
                for b,d,n in phrase(t['B'][local%4],t)[:2]:
                    if n is not None:s.note(1,at+b,d*.8,n-12,48,bend=.25)
            # A developed reply uses chord tones in the lead's rests / end of alternate measures.
            if not is_sparse and (local%2==1 or isB) and (passages>=2 or isB or secidx>=3):
                melody=phrase(pattern,t);rests=[(b,d) for b,d,n in melody if n is None]
                windows=rests or [(B-1,.9)]
                for b,d in windows[:1]:
                    for j in range(2):
                        n=voicing[(local+j+1)%len(voicing)]+12
                        s.note(1,at+b+j*d/2,d*.4,n,56*intensity+8,bend=.4 if j==0 else 0)
            # Sparse glints make the habitat texture; energetic tracks use a fuller broken-chord engine.
            arp_on=(local%2==0 and (isB or passages>=2)) or (intro and local<2) or g=='ambient'
            if arp_on and not (outro and local>=2):
                step=.5 if g in ['battle','drive','adventure','urgent'] else 1
                order=[0,2,1,3] if t['id']%2 else [2,0,3,1]
                for j in range(math.ceil(B/step)):
                    b=j*step+.03
                    if b>=B-.1:continue
                    n=voicing[order[j%4]%len(voicing)]+12
                    s.note(4,at+b,min(step*.55,B-b-.03),n,(35 if is_sparse else 43)+6*(j%3==0))
            drums(s,bar,intensity*(.45 if is_sparse else 1))
        cursor+=count
    t['totalBeats']=totalbars*B;t['bars']=totalbars;t['sections']=sections
    t['duration']=round(t['totalBeats']*60/t['bpm']+2.8,3)
    t['loopStart']=round(4*B*60/t['bpm'],3);t['loopEnd']=round((totalbars-4)*B*60/t['bpm'],3)
    t['slug']=f"{t['id']:02d}-"+re.sub(r'[^a-z0-9]+','-',t['title'].lower()).strip('-')
    path=ROOT/'midi'/f"{t['slug']}.mid";s.save(path)
    t['midi']=f"midi/{path.name}";t['audio']=f"audio/{t['slug']}.mp3";t['noteCount']=len(s.notes)
    t['midiSha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    return t

if __name__=='__main__':
    (ROOT/'midi').mkdir(exist_ok=True)
    result=[compose(dict(t)) for t in TRACKS]
    album={'title':'Critz: Tycoon — A Tiny World','revision':'MUSIC.01 · review edition','status':'Awaiting listening review; not integrated into gameplay','tracks':result}
    (ROOT/'album.json').write_text(json.dumps(album,ensure_ascii=False,indent=2)+'\n')
    with zipfile.ZipFile(ROOT/'critz-tycoon-30-midi.zip','w',zipfile.ZIP_DEFLATED) as z:
        for t in result:z.write(ROOT/t['midi'],Path(t['midi']).name)
        z.writestr('README.txt','Critz: Tycoon — A Tiny World\n30 original Type-1 MIDI compositions.\n480 PPQ; separate named parts; GM fallback programs; pitch-bend range +/-2 semitones.\nLOOP_START / LOOP_END are suggested musical loop regions; coda follows.\nMIDI stores performance, not audio. The listening-room MP3s use original custom synth patches.\nOriginal composition/arrangement: Codex for Critz: Tycoon, MUSIC.01 review edition.\nNo Pokemon recordings, melodies or game samples included.\n')
    print(f'Composed {len(result)} tracks / {sum(t["noteCount"] for t in result):,} notes / {sum(t["duration"] for t in result)/60:.1f} minutes')
