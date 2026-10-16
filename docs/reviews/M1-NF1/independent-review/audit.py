from pathlib import Path
from PIL import Image,ImageOps
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[4];D=R/'docs/reviews/M1-NF1';a=Image.open(D/'front-neutral.png').convert('RGBA');b=Image.open(R/'docs/reviews/M1-NT1/south/neutral.png').convert('RGBA');checks=[]
def ck(n,v):assert v,n;checks.append(n)
def delta(p,q,alpha=False):return [(x,y) for y in range(64) for x in range(32) if (p.getpixel((x,y))[3] if alpha else p.getpixel((x,y)))!=(q.getpixel((x,y))[3] if alpha else q.getpixel((x,y)))]
ck('frame32x64',a.size==(32,64));ck('binary alpha',set(a.getchannel('A').get_flattened_data())=={0,255})
ck('exact RGBA reflected about x15.5',a.tobytes()==ImageOps.mirror(a).tobytes());ck('exact reflected alpha',a.getchannel('A').tobytes()==ImageOps.mirror(a).getchannel('A').tobytes())
ck('full shoes58+ RGBA unchanged',a.crop((0,58,32,64)).tobytes()==b.crop((0,58,32,64)).tobytes());ck('head0..44 RGBA unchanged',a.crop((0,0,32,45)).tobytes()==b.crop((0,0,32,45)).tobytes())
for name,path in [('Hero','docs/reviews/M1-NCR1/south-idle/master-hero.png'),('West','docs/reviews/M1-NT1/west/neutral.png')]:ck(name+' file exact frozen source',(R/path).read_bytes()==subprocess.check_output(['git','show','ef43a54f05d78ce448396415f799e7e664f217b4:'+path]))
pts={(x,y) for y in range(64) for x in range(32) if a.getpixel((x,y))[3]};seen=set();todo=[next(iter(pts))]
while todo:
 p=todo.pop()
 if p in seen:continue
 seen.add(p);x,y=p;todo.extend(v for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if v in pts and v not in seen)
ck('one4connected alpha silhouette',seen==pts);ck('no old pale shoulder cap color',not any(a.getpixel((x,y))==(191,192,170,255) for y in range(43,50) for x in range(32)))
ck('four requested outer waist flare cells removed',all(a.getpixel((x,54))[3]==0 for x in [5,6,25,26]))
c=json.loads((R/'art/source/neutral-front-r1/construction.json').read_text());assembled=Image.new('RGBA',(32,64))
for name in c['renderOrder']:
 layer=Image.open(D/(name+'-region.png')).convert('RGBA');ck(name+' exact reflected RGBA',layer.tobytes()==ImageOps.mirror(layer).tobytes());ck(name+' exact reflected alpha',layer.getchannel('A').tobytes()==ImageOps.mirror(layer).getchannel('A').tobytes());assembled.alpha_composite(layer)
ck('saved region layers exactly recompose corrected front',assembled.tobytes()==a.tobytes())
ck('seventeen warm hand cells each',all(sum(a.getpixel((x,y))==(166,104,69,255) for x in range(lo,hi) for y in range(45,58))==17 for lo,hi in [(0,16),(16,32)]))
report={'task':'M1.NF1','pass':True,'count':len(checks),'checks':checks,'axis':'between columns15 and16, reflection x→31−x','beforeMismatchedPairs':len(delta(b,ImageOps.mirror(b)))//2,'afterMismatchedPairs':len(delta(a,ImageOps.mirror(a)))//2,'rgbaChangedCells':delta(a,b),'alphaChangedCells':delta(a,b,True),'sha256':hashlib.sha256((D/'front-neutral.png').read_bytes()).hexdigest(),'approval':False};(D/'independent-review/saved-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['rgbaChangedCells','alphaChangedCells']}))
