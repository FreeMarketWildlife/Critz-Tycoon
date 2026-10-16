"""Independent OM4 actual saved-pixel/source-contact/GIF audit. No artist writes."""
from pathlib import Path
from PIL import Image,ImageColor
import json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
S=ROOT/'art/source/overnight-mom-walk-r1';R=ROOT/'docs/reviews/M1-OM4'
C=[];poses=[];gifs=[]
def guard(n,v):C.append({'name':n,'pass':bool(v)})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def shift(im):
 q=Image.new('RGBA',(32,64));q.paste(im,(0,2));return q
for d in ['south','north','west','east']:
 layers={}
 for phase in ['idle','A','B']:
  jp=S/d/(phase+'.layers.json');o=json.loads(jp.read_text());comp=Image.new('RGBA',(32,64));layers[phase]={}
  for n in o['order']:
   q=Image.new('RGBA',(32,64))
   for x,y,color in o['layers'][n]:q.putpixel((x,y),ImageColor.getrgb(color)+(255,))
   guard(f'{d}/{phase}/{n} JSON equals PNG',q.tobytes()==Image.open(S/d/phase/(n+'.png')).convert('RGBA').tobytes())
   layers[phase][n]=q;comp=Image.alpha_composite(comp,q)
  fp=R/(d+'-'+phase+'.png');im=Image.open(fp).convert('RGBA')
  guard(f'{d}/{phase} exact composition',comp.tobytes()==im.tobytes())
  guard(f'{d}/{phase} native32x64 binaryalpha',im.size==(32,64) and set(im.getchannel('A').getdata())<={0,255})
  mask={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]};row=max(y for x,y in mask)
  guard(f'{d}/{phase} painted contact',row==(61 if phase=='idle' else 63))
  seen=set();stack=[next(iter(mask))]
  while stack:
   cell=stack.pop()
   if cell in seen:continue
   seen.add(cell);x,y=cell
   stack.extend(p for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if p in mask and p not in seen)
  guard(f'{d}/{phase} single fourconnected cluster',seen==mask)
  if phase=='idle':guard(d+' frozen OM3 idle bytes',fp.read_bytes()==(ROOT/'docs/reviews/M1-OM3'/('idle-'+d+'.png')).read_bytes())
  poses.append({'direction':d,'phase':phase,'file':str(fp.relative_to(ROOT)),'sha256':sha(fp),'layersJsonSHA256':sha(jp),'contactRow':row,'contactXs':[x for x in range(32) if (x,row) in mask]})
 for phase in ['A','B']:
  for n in ['head','face','hair','jewelry','torso']:
   guard(f'{d}/{phase}/{n} exact idle+2Y',shift(layers['idle'][n]).tobytes()==layers[phase][n].tobytes())
for fp in sorted(R.glob('*.gif')):
 im=Image.open(fp);holds=[]
 for j,phase in enumerate(['A','idle','B','idle']):
  im.seek(j);holds.append(im.info.get('duration'));decoded=im.convert('RGBA')
  for k,d in enumerate(['south','north','west','east']):
   png=Image.open(R/(d+'-'+phase+'.png')).convert('RGBA')
   if 'four-directions' in fp.name:regions=[(15+210*k,60,4),(165+210*k,240,1)]
   elif fp.name.startswith(d+'-'):regions=[(0,0,4 if '-4x.gif' in fp.name else 1)]
   else:continue
   for x,y,scale in regions:
    expected=png.resize((32*scale,64*scale),Image.Resampling.NEAREST);crop=decoded.crop((x,y,x+32*scale,y+64*scale))
    if 'four-directions' in fp.name:
     bg=Image.new('RGBA',expected.size,decoded.getpixel((0,0)));bg.alpha_composite(expected);ok=crop.convert('RGB').tobytes()==bg.convert('RGB').tobytes()
    else:ok=crop.getchannel('A').tobytes()==expected.getchannel('A').tobytes() and all(crop.getpixel((xx,yy))==expected.getpixel((xx,yy)) for yy in range(expected.height) for xx in range(expected.width) if expected.getpixel((xx,yy))[3])
    guard(f'{fp.name}/slot{j}/{d}/{scale}x exact decoded PNG',ok)
 guard(fp.name+' four declared GIF holds',im.n_frames==4 and holds==([540,530,540,530] if 'slow' in fp.name else [130,140,130,140]))
 gifs.append({'file':str(fp.relative_to(ROOT)),'sha256':sha(fp),'holdsMs':holds})
source=ROOT/'local-review/overnight-cast-qa/mom.png';im=Image.open(source)
guard('actual Mom pinned primary SHA',sha(source)=='a404a3c79252a6a13e10622307c3bce4c76c1e1a39814b7c7a11ad7520442289')
sourceFrames=[]
for i in range(9):
 cells={(x,y) for y in range(32) for x in range(16) if im.getpixel((i*16+x,y))!=0};row=max(y for x,y in cells)
 sourceFrames.append({'index':i,'contactRow':row,'contactXs':[x for x in range(16) if (x,row) in cells]})
manifest=json.loads((S/'manifest.json').read_text())
for d,order in [('south',[3,0,4,0]),('north',[5,1,6,1]),('west',[7,2,8,2]),('east',['flip7','flip2','flip8','flip2'])]:guard(d+' declared source order',manifest['sourceOrder'][d]==order)
guard('exact source clock8tick',manifest['updatesPerSlot']==8 and manifest['tickSeconds']==280896/16777216)
report={'task':'M1.OVQ3 Mom walk followup','passed':sum(c['pass'] for c in C),'failed':sum(not c['pass'] for c in C),'checks':C,'poses':poses,'gifs':gifs,'source':{'revision':'5eff78649e7170a877b961ef0b3da13b81a16038','sha256':sha(source),'frames':sourceFrames},'limitations':'Root source-command audit confirms8ticks/order; actual PNG asset contacts independently decoded index0 transparent, raw palette not emulator color. Exact torso+2Y preserves inset material; does not approve visual read. GIF540/2140ms quantization versus exact535.7666/2143.0664ms.'}
(OUT/'mom-walk-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'failures':[c for c in C if not c['pass']],'sourceContacts':sourceFrames}))
assert report['failed']==0
