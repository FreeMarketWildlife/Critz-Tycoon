"""Notation and MIDI export only. No melodies, forms or genre templates live here."""
from pathlib import Path
import re, json, hashlib, zipfile
import mido
ROOT=Path(__file__).resolve().parents[1]
PPQ=960
# Unique GM programs are portable approximations. Exact original patches live in render.py.
PATCHES={'felt':0,'epiano':4,'bell':8,'box':10,'vibes':11,'marimba':12,'organ':16,'nylon':24,'pluck':27,'upright':32,'sub':38,'strings':48,'brass':62,'reed':71,'flute':73,'square':80,'saw':81,'triangle':85,'pulse':87,'air':89,'sine':90,'glass':98,'bubble':103}
PC={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def pitch(text):
    m=re.fullmatch(r'([A-G])([#b]?)(-?\d)',text); assert m,text
    a,b,c=m.groups();return 12*(int(c)+1)+PC[a]+(1 if b=='#' else -1 if b=='b' else 0)
class Piece:
    def __init__(self,id,title,mood,key,bpm,meter,bars,story,personality):
        self.id=id;self.title=title;self.mood=mood;self.key=key;self.bpm=bpm;self.meter=meter;self.bars=bars;self.story=story;self.personality=personality
        a,b=map(int,meter.split('/'));self.B=a*4/b;self.parts=[];self.sections=[];self.room=.15
    def part(self,name,patch,level=.75,pan=.5,wet=.12):
        c=9 if patch=='drums' else len([p for p in self.parts if p['patch']!='drums']);assert c<9 or patch=='drums'
        p=dict(name=name,patch=patch,channel=c,level=level,pan=pan,wet=wet,notes=[]);self.parts.append(p);return p
    def note(self,p,beat,dur,n,vel=72):
        n=pitch(n) if isinstance(n,str) else n
        assert 0<=n<=127 and dur>0 and beat>=0,(self.title,n,beat,dur)
        assert beat+dur<=self.bars*self.B+.0001,(self.title,'overrun',beat,dur)
        p['notes'].append([round(beat,5),round(dur,5),n,vel])
    def line(self,p,bar,text,v=72,gate=.88,transpose=0):
        for i,measure in enumerate(text.strip().split('|')):
            cursor=0.
            for token in measure.split():
                ns,ds=token.split(':');d=float(ds);assert cursor+d<=self.B+.00001,(self.title,bar+i,measure,cursor+d,self.B)
                if ns!='R':
                    for n in ns.split('+'):self.note(p,(bar+i)*self.B+cursor,d*gate,pitch(n)+transpose,v)
                cursor+=d
    def blocks(self,p,bar,voicings,dur=None,v=56,offset=0):
        # Explicit absolute-note voicings; empty entries deliberately leave space.
        for i,chord in enumerate(voicings.split('|')):
            for n in chord.split():self.note(p,(bar+i)*self.B+offset,(dur or self.B*.88),n,v)
    def arp(self,p,bar,voicings,pattern,v=56):
        for i,chord in enumerate(voicings.split('|')):
            notes=chord.split()
            if not notes:continue
            for at,idx,d in pattern:self.note(p,(bar+i)*self.B+at,d,notes[idx],v)
    def drums(self,bar,count,pattern,v=65):
        p=next((p for p in self.parts if p['patch']=='drums'),None)
        if p is None:p=self.part('Small drum kit','drums',.6,.5,.03)
        for i in range(count):
            for at,n,accent in pattern:self.note(p,(bar+i)*self.B+at,.08,n,max(1,min(120,v+accent)))
    def mark(self,bar,label):self.sections.append(dict(bar=bar,label=label,seconds=round(bar*self.B*60/self.bpm,4)))
    def save(self):
        slug=f'{self.id:02d}-'+re.sub(r'[^a-z0-9]+','-',self.title.lower()).strip('-')
        total=self.bars*self.B
        mid=mido.MidiFile(type=1,ticks_per_beat=PPQ,charset='utf-8'); conductor=mido.MidiTrack();mid.tracks.append(conductor)
        a,b=map(int,self.meter.split('/'))
        metas=[(0,mido.MetaMessage('track_name',name=self.title)),(0,mido.MetaMessage('text',text='Critz: Tycoon MUSIC.02 / independently authored score / A440 / no glides')),(0,mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(self.bpm))),(0,mido.MetaMessage('time_signature',numerator=a,denominator=b)),(0,mido.MetaMessage('text',text=f'Tonal centre: {self.key}'))]
        for s in self.sections:metas.append((round(s['bar']*self.B*PPQ),mido.MetaMessage('marker',text=s['label'])))
        metas.append((round(total*PPQ),mido.MetaMessage('end_of_track')));prev=0
        for tick,msg in sorted(metas,key=lambda a:a[0]):conductor.append(msg.copy(time=tick-prev));prev=tick
        for p in self.parts:
            assert p['notes'],(self.title,p['name'],'empty part')
            c=p['channel'];mt=mido.MidiTrack();mid.tracks.append(mt)
            mt.append(mido.MetaMessage('track_name',name=p['name']+' / '+p['patch']))
            if c!=9:mt.append(mido.Message('program_change',channel=c,program=PATCHES[p['patch']]))
            for cc,val in [(7,round(127*p['level'])),(10,round(127*p['pan'])),(11,100),(1,0),(65,0),(91,round(p['wet']*127)),(93,0)]:mt.append(mido.Message('control_change',channel=c,control=cc,value=val))
            if c!=9:mt.append(mido.Message('pitchwheel',channel=c,pitch=0))
            events=[]
            for at,d,n,v in p['notes']:
                events.extend([(round(at*PPQ),1,mido.Message('note_on',channel=c,note=n,velocity=v)),(round((at+d)*PPQ),0,mido.Message('note_off',channel=c,note=n,velocity=0))])
            prev=0
            for tick,order,msg in sorted(events,key=lambda x:(x[0],x[1])):mt.append(msg.copy(time=tick-prev));prev=tick
            mt.append(mido.MetaMessage('end_of_track',time=round(total*PPQ)-prev))
        path=ROOT/'v2'/'midi'/f'{slug}.mid';path.parent.mkdir(parents=True,exist_ok=True);mid.save(path)
        score=dict(id=self.id,title=self.title,bpm=self.bpm,meter=self.meter,bars=self.bars,key=self.key,sections=self.sections,parts=self.parts)
        (ROOT/'source-v2'/'scores'/f'{slug}.json').write_text(json.dumps(score,indent=2)+'\n')
        return dict(id=self.id,title=self.title,slug=slug,mood=self.mood,key=self.key,bpm=self.bpm,meter=self.meter,bars=self.bars,story=self.story,personality=self.personality,sections=self.sections,room=self.room,instruments=[{k:v for k,v in p.items() if k!='notes'} for p in self.parts],noteCount=sum(len(p['notes']) for p in self.parts),duration=round(total*60/self.bpm+3,3),midi=f'v2/midi/{slug}.mid',audio=f'v2/audio/{slug}.mp3',midiSha256=hashlib.sha256(path.read_bytes()).hexdigest())
