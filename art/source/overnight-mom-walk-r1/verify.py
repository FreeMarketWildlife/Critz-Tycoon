"""Independent OM4 saved-file/phase checks; does not import the builder."""
from pathlib import Path
from collections import deque
from PIL import Image
import json,hashlib
S=Path(__file__).resolve().parent;R=S.parents[2];O=R/'docs/reviews/M1-OM4';I=R/'art/source/overnight-mom-inset-r1';V=R/'docs/reviews/M1-OM3'
checks=[];measure={};dirs=['south','north','west','east'];seq=['A','idle','B','idle']
def check(n,v):
 assert v,n
 checks.append(n)
def rgba(p):return Image.open(p).convert('RGBA')
def blank():return Image.new('RGBA',(32,64))
def move(im,dx=0,dy=0):
 out=blank();out.alpha_composite(im,(dx,dy));return out
def connected(im):
 cells={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]};seen={next(iter(cells))};q=deque(seen)
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if p in cells and p not in seen:seen.add(p);q.append(p)
 return cells==seen
for path,h in json.loads((S/'protected-inputs.json').read_text()).items():check('OM3 preserved '+path,hashlib.sha256((R/path).read_bytes()).hexdigest()==h)
primary=R/'local-review/overnight-cast-qa/mom.png';check('pinned Mom source',hashlib.sha256(primary.read_bytes()).hexdigest()=='a404a3c79252a6a13e10622307c3bce4c76c1e1a39814b7c7a11ad7520442289')
raw=Image.open(primary)
headEvidence={}
for idle,strides in [(0,[3,4]),(1,[5,6]),(2,[7,8])]:
 for n in strides:
  check('source rigid down1 head '+str(n),raw.crop((idle*16,0,idle*16+16,21)).tobytes()==raw.crop((n*16,1,n*16+16,22)).tobytes())
  headEvidence[str(n)]={'sourceIdle':idle,'sourceStride':n,'rigidHeadDownNativePixels':1,'comparison':'indexed exact all16x21 upper cells against translated stride; no recolor'}
for dr in dirs:
 project=json.loads((S/dr/'walk.sprite.json').read_text());check(dr+' four slots8 updates',[f['name'] for f in project['frames']]==seq and all(f['ticks']==8 for f in project['frames']))
 for phase in ['A','idle','B']:
  im=rgba(O/f'{dr}-{phase}.png');src=json.loads((S/dr/(phase+'.layers.json')).read_text());layers={};re=blank()
  check(dr+phase+' dimensions',im.size==(32,64));check(dr+phase+' binary alpha',set(im.getchannel('A').get_flattened_data())=={0,255});check(dr+phase+' fixed registration',src['frame']==[32,64] and src['anchor']==[16,64])
  for n in src['order']:
   layer=rgba(S/dr/phase/(n+'.png'));j=blank()
   for x,y,c in src['layers'][n]:j.putpixel((x,y),tuple(bytes.fromhex(c[1:]))+(255,))
   check(dr+phase+' actual layer JSON '+n,j.tobytes()==layer.tobytes());re.alpha_composite(layer);layers[n]=layer
  check(dr+phase+' exact layer composite',re.tobytes()==im.tobytes());check(dr+phase+' connected figure',connected(im))
  ys=[y for y in range(64) for x in range(32) if im.getpixel((x,y))[3]];check(dr+phase+' contact',max(ys)==(61 if phase=='idle' else 63))
  if phase=='idle':check(dr+' exact OM3 idle PNG',(O/f'{dr}-{phase}.png').read_bytes()==(V/f'idle-{dr}.png').read_bytes())
  else:
   for n in ['head','face','hair','jewelry','torso']:check(dr+phase+' rigid +2Y '+n,layers[n].tobytes()==move(rgba(I/dr/(n+'.png')),dy=2).tobytes())
   if dr in ['west','east']:
    sign=1 if dr=='west' else -1;dx=(-3 if phase=='A' else 3)*sign
    check(dr+phase+' full near shoe exact rigid translation',layers['near-shoe'].tobytes()==move(rgba(I/dr/'feet.png'),dx,2).tobytes())
    check(dr+phase+' far shoe darker',all(p[:3] in [(66,59,72),(32,16,8)] for p in layers['far-shoe'].get_flattened_data() if p[3]))
    hand=layers['near-hand'];check(dr+phase+' full near hand cells',sum(p[3]>0 for p in hand.get_flattened_data())==sum(p[3]>0 for p in rgba(I/dr/'hands.png').get_flattened_data()))
   else:
    for side,left in [('left',True),('right',False)]:
     lead=left==(phase=='A')
     if lead:
      original=rgba(I/dr/'feet.png');half=blank()
      for y in range(64):
       for x in range(32):
        if (x<16)==left:half.putpixel((x,y),original.getpixel((x,y)))
      check(dr+phase+' full lead shoe exact',layers[side+'-shoe'].tobytes()==move(half,1 if left else -1,2).tobytes())
  for index,p in enumerate(seq):
   if p!=phase:continue
   decoded=blank();decoded.putdata([(0,0,0,0) if not v else tuple(bytes.fromhex(project['palette'][v][1:]))+(255,) for v in project['frames'][index]['pixels']]);check(dr+phase+str(index)+' project exact',decoded.tobytes()==im.tobytes())
  measure[dr+'-'+phase]={'bounds':im.getbbox(),'opaqueCells':sum(p[3]>0 for p in im.get_flattened_data()),'contactXs':[x for x in range(32) if im.getpixel((x,max(ys)))[3]],'sha256':hashlib.sha256((O/f'{dr}-{phase}.png').read_bytes()).hexdigest()}
 atlas=rgba(O/'walk-atlas.png')
 for col,p in enumerate(seq):check(dr+str(col)+' atlas exact',atlas.crop((32*col,64*dirs.index(dr),32*col+32,64*dirs.index(dr)+64)).tobytes()==rgba(O/f'{dr}-{p}.png').tobytes())
for speed,holds in [('normal',[130,140,130,140]),('slow4x',[540,530,540,530])]:
 for dr in dirs:
  for scale in [1,4]:
   g=Image.open(O/f'{dr}-{speed}-{scale}x.gif');check(dr+speed+str(scale)+' GIF fourframes loop',g.n_frames==4 and g.info['loop']==0)
   for i,p in enumerate(seq):
    g.seek(i);check(dr+speed+str(scale)+str(i)+' GIF hold',g.info['duration']==holds[i]);expect=rgba(O/f'{dr}-{p}.png').resize((32*scale,64*scale),Image.Resampling.NEAREST);check(dr+speed+str(scale)+str(i)+' GIF exact RGBA',g.convert('RGBA').tobytes()==expect.tobytes())
 g=Image.open(O/f'four-directions-{speed}.gif');check(speed+' board GIF frames loop',g.n_frames==4 and g.info['loop']==0)
 for i in range(4):
  g.seek(i);check(speed+str(i)+' board hold',g.info['duration']==holds[i]);check(speed+str(i)+' board frame exact',g.convert('RGB').tobytes()==Image.open(O/f'four-directions-slot{i}.png').convert('RGB').tobytes())
report={'task':'M1.OM4','checksPassed':len(checks),'checks':checks,'frames':measure,'sourceHeadEvidence':headEvidence,'appearanceAccepted':False,'noRuntime':True}
(S/'saved-file-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checksPassed':len(checks),'contacts':{n:v['contactXs'] for n,v in measure.items()}}))
