"""Independent saved-file, source protection, articulation and GIF decoding checks."""
from pathlib import Path
from PIL import Image
import hashlib,json
R=Path(__file__).resolve().parents[3];S=Path(__file__).resolve().parent;O=R/'docs/reviews/M1-OGH3';V=R/'docs/reviews/M1-OGH2';I=R/'art/source/overnight-girl-continuation-r1'
assert S==R/'art/source/overnight-girl-walk-r1'
checks=[];facts={}
def ck(n,v):
 if not v:raise AssertionError(n)
 checks.append(n)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def px(q):return list(q.get_flattened_data())
def blank():return Image.new('RGBA',(32,64))
def mask(q):return {(x,y) for y in range(64) for x in range(32) if q.getpixel((x,y))[3]}
def connected(m):
 seen=set();todo=[next(iter(m))] if m else []
 while todo:
  p=todo.pop()
  if p in seen:continue
  seen.add(p);todo.extend(q for q in [(p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1)] if q in m-seen)
 return bool(m) and seen==m

def decode(p):
 spec=json.loads(p.read_text());ls={}
 for v in spec['layers']:
  q=blank();q.putdata([(0,0,0,0) if i==0 else tuple(bytes.fromhex(spec['palette'][i][1:]))+(255,) for i in v['pixels']]);ls[v['id']]=q
 return spec,ls

def moved(q,dx,dy):
 z=blank()
 for x,y in mask(q):z.putpixel((x+dx,y+dy),q.getpixel((x,y)))
 return z

baseline=json.loads((O/'idle-baseline.json').read_text())
ck('all206 protected OGH2 source review and idle history files byte-exact',all(sha(R/p)==h for p,h in baseline['readOnlyFiles'].items()))
manifest=json.loads((S/'construction.json').read_text());ck('viewer metadata exact source construction',manifest==json.loads((O/'study.json').read_text()))
ck('source clock8ticks per slot and32tick fullgait',manifest['sourceClock']['ticksPerSlot']==8 and manifest['sourceClock']['totalTicks']==32 and manifest['sourceClock']['numeratorSeconds']==280896 and manifest['sourceClock']['denominator']==16777216)
ck('phase order A idle B idle',manifest['cycle']==['stride-a','idle','stride-b','idle'])
for dr in ['south','north','west','east']:
 ispec,idle=decode(I/(dr+'.layers.json'));facts[dr]={}
 ck(dr+' idle PNG exact OGH2 bytes',sha(O/dr/'idle/composite.png')==sha(V/dr/'idle.png'))
 project=json.loads((S/(dr+'.walk.sprite.json')).read_text());ck(dr+' four actual slots8ticks',len(project['frames'])==4 and all(f['ticks']==8 for f in project['frames']))
 for phase in ['idle','stride-a','stride-b']:
  q=Image.open(O/dr/phase/'composite.png').convert('RGBA');spec,ls=decode(S/(dr+'-'+phase+'.layers.json'));comp=blank()
  ck(dr+phase+' actual semantic layer order',spec['order']==list(ls))
  for name,im in ls.items():
   ck(dr+phase+' '+name+' saved semantic PNG exact JSON',im.tobytes()==Image.open(O/dr/phase/(name+'.png')).convert('RGBA').tobytes());comp.alpha_composite(im)
  ck(dr+phase+' layers exactly recompose',comp.tobytes()==q.tobytes())
  ck(dr+phase+' native32x64 binary alpha',q.size==(32,64) and set(q.getchannel('A').get_flattened_data())=={0,255})
  ck(dr+phase+' opaque character connected',connected(mask(q)))
  ck(dr+phase+' lastcontact preserves idle61/stride63',max(y for x,y in mask(q))==(61 if phase=='idle' else 63))
  for name in ['face','ears','hair','ties','eyes']:
   expected=idle[name] if phase=='idle' else moved(idle[name],0,2)
   ck(dr+phase+' '+name+' exact rigid head shape/registration',ls[name].tobytes()==expected.tobytes())
  hq=Image.open(O/'history-v0'/dr/phase/'composite.png').convert('RGBA')
  ck(dr+phase+' bounded correction retains entire alpha',q.getchannel('A').tobytes()==hq.getchannel('A').tobytes())
  if dr in ['south','north'] or phase=='idle':ck(dr+phase+' whole PNG exact initial study',sha(O/dr/phase/'composite.png')==sha(O/'history-v0'/dr/phase/'composite.png'))
  else:
   _,old=decode(O/'history-v0/source'/(dr+'-'+phase+'.layers.json'))
   for name,im in ls.items():
    if name!='far-shoe':ck(dr+phase+' correction protects '+name,im.tobytes()==old[name].tobytes())
   ck(dr+phase+' farshoe mask exact initial study',mask(ls['far-shoe'])==mask(old['far-shoe']))
   ck(dr+phase+' farshoe dark burgundy and ink only',set(px(ls['far-shoe']))<={(0,0,0,0),(128,57,78,255),(32,16,8,255)})
   ck(dr+phase+' full nearfoot56 cells retained',len(mask(ls['near-shoe']))==56 and connected(mask(ls['near-shoe'])))
   ck(dr+phase+' full farfoot56 cells retained before occlusion',len(mask(ls['far-shoe']))==56 and connected(mask(ls['far-shoe'])))
  if phase!='idle' and dr in ['south','north']:
   for name in ['rear-shoe','planted-shoe']:ck(dr+phase+' '+name+' full27cell foot retained',len(mask(ls[name]))==27 and connected(mask(ls[name])))
  if phase!='idle':
   def normalized(m):
    xx=min(x for x,y in m);yy=min(y for x,y in m);return {(x-xx,y-yy) for x,y in m}
   if dr in ['west','east']:
    for shoe in ['near-shoe','far-shoe']:ck(dr+phase+' '+shoe+' full contour exact idle under translation',normalized(mask(ls[shoe]))==normalized(mask(idle['shoes'])))
    ck(dr+phase+' torso core exact rigid2Y',ls['shirt'].tobytes()==moved(idle['shirt'],0,2).tobytes())
   else:
    source_shoes=mask(idle['shoes']);left={p for p in source_shoes if p[0]<16};right=source_shoes-left
    ck(dr+phase+' planted full contour exact idle',normalized(mask(ls['planted-shoe']))==normalized(left if phase=='stride-a' else right))
    ck(dr+phase+' rear full contour exact idle',normalized(mask(ls['rear-shoe']))==normalized(right if phase=='stride-a' else left))
    core=blank()
    for x,y in mask(idle['shirt']):
     if 10<=x<=21:core.putpixel((x,y+2),idle['shirt'].getpixel((x,y)))
    ck(dr+phase+' torso core exact rigid2Y',core.tobytes()==ls['torso'].tobytes())
  last=max(y for x,y in mask(q));facts[dr][phase]={'pngSHA256':sha(O/dr/phase/'composite.png'),'lastContactY':last,'contactXs':sorted(x for x,y in mask(q) if y==last),'changedRGBAFromInitial':sum(a!=b for a,b in zip(px(q),px(hq))),'opaqueCells':len(mask(q))}
 for i,phase in enumerate(manifest['cycle']):
  f=project['frames'][i];actual=[(0,0,0,0) if v==0 else tuple(bytes.fromhex(project['palette'][v][1:]))+(255,) for v in f['pixels']]
  ck(dr+' cycle slot'+str(i)+' exact intended saved pose',actual==px(Image.open(O/dr/phase/'composite.png').convert('RGBA')))
# Decode actual saved GIFs; centisecond holds and RGB frames must match intended saved full frames exactly.
gif_facts={}
for name in ['walk-normal-paired.gif','walk-slow-paired.gif','walk-normal-native.gif','walk-slow-native.gif']:
 expected=json.loads((O/(name+'.frames.json')).read_text());g=Image.open(O/name)
 ck(name+' actual four decoded frames',g.n_frames==4);holds=[];hashes=[]
 for i in range(g.n_frames):
  g.seek(i);holds.append(g.info['duration']);hashes.append(hashlib.sha256(g.convert('RGB').tobytes()).hexdigest())
 ck(name+' decoded duration sequence exact',holds==expected['holdsMs'])
 ck(name+' decoded actual frame pixels exact',hashes==expected['rgbFrameSHA256'])
 ck(name+' full repeat loop',g.info.get('loop')==0)
 gif_facts[name]={'sha256':sha(O/name),'holdsMs':holds,'totalMs':sum(holds),'dimensions':g.size}
for v in manifest['referenceFiles']:ck(v['name']+' pinned source bytes exact',sha(Path(v['path']))==v['sha256'])
record={'task':'M1.OGH3','revision':'v1-far-shoe-material-only','pass':True,'count':len(checks),'checks':checks,'facts':facts,'gifFacts':gif_facts,'phaseBoardSHA256':sha(O/'phase-board.png'),'appearanceAccepted':False,'runtimeChanged':False,'uninterruptedWatchClaimed':False}
(O/'checks.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'pass':True,'count':len(checks),'phaseBoardSHA256':record['phaseBoardSHA256'],'sideCorrectionRGBA':{d:{p:facts[d][p]['changedRGBAFromInitial'] for p in ['stride-a','stride-b']} for d in ['west','east']}}))
