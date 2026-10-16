from pathlib import Path
from PIL import Image,ImageColor
import json,hashlib
R=Path(__file__).resolve().parents[4];checks=[];pins={}
def ck(n,v):checks.append({'name':n,'pass':bool(v)})
def decode(q):
 out={}
 if isinstance(q['layers'],list):
  for l in q['layers']:
   im=Image.new('RGBA',(32,64));im.putdata([(0,0,0,0) if k==0 else (*ImageColor.getrgb(q['palette'][k]),255) for k in l['pixels']]);out[l['id']]=im
 else:
  for n,l in q['layers'].items():
   im=Image.new('RGBA',(32,64))
   for x,y,*v in l['pixels']:im.putpixel((x,y),tuple(v))
   out[n]=im
 return out
for char,task,old in [('girl','M1-OGH3','M1-OGH2'),('nugget','M1-ON3','M1-ON2')]:
 for d in ['south','north','west','east']:
  maps={}
  for pose in ['A','idle','B']:
   if char=='girl':
    key={'A':'stride-a','idle':'idle','B':'stride-b'}[pose];sp=R/f'art/source/overnight-girl-walk-r1/{d}-{key}.layers.json';p=R/f'docs/reviews/{task}/{d}/{key}/composite.png'
   else:sp=R/f'art/source/overnight-nugget-walk-r1/{d}/{pose}.layers.json';p=R/f'docs/reviews/{task}/{d}-{pose}.png'
   q=json.loads(sp.read_text());layers=decode(q);maps[pose]=layers;a=Image.open(p).convert('RGBA');b=Image.new('RGBA',(32,64))
   for n in q.get('order',q.get('renderOrder')):b.alpha_composite(layers[n])
   ck(f'{char}/{d}/{pose} saved layer recompose',a.tobytes()==b.tobytes());ck(f'{char}/{d}/{pose} binary frame',a.size==(32,64) and set(a.getchannel('A').get_flattened_data())<={0,255})
   sites={(x,y) for y in range(64) for x in range(32) if a.getpixel((x,y))[3]};ck(f'{char}/{d}/{pose} contact',max(y for x,y in sites)==(61 if pose=='idle' else 63))
   visited=set();pending=[next(iter(sites))]
   while pending:
    t=pending.pop()
    if t in visited:continue
    visited.add(t);x,y=t;pending.extend(s for s in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if s in sites and s not in visited)
   ck(f'{char}/{d}/{pose} connected',visited==sites);pins[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
   if pose=='idle':
    prev=R/f'docs/reviews/{old}'/(f'{d}/idle.png' if char=='girl' else f'{d}-idle.png');ck(f'{char}/{d} exact frozen idle bytes',p.read_bytes()==prev.read_bytes())
  headnames=[n for n in maps['idle'] if (n in ['head','ear','ears','eyes','glasses','ties'] or n.startswith(('face','hair','hat')))]
  for pose in ['A','B']:
   for name in headnames:
    im=Image.new('RGBA',(32,64));im.alpha_composite(maps['idle'][name],(0,2));ck(f'{char}/{d}/{pose} rigid2Y {name}',im.tobytes()==maps[pose][name].tobytes())
for speed,holds in [('normal',[130,140,130,140]),('slow4x',[540,530,540,530])]:
 for d in ['south','north','west','east']:
  p=R/f'docs/reviews/M1-ON3/{d}-{speed}-1x.gif';g=Image.open(p);ck(f'Nugget{d}{speed}4frames',g.n_frames==4);ck(f'Nugget{d}{speed}loop',g.info.get('loop')==0)
  for i,pose in enumerate(['A','idle','B','idle']):g.seek(i);a=g.convert('RGBA');b=Image.open(R/f'docs/reviews/M1-ON3/{d}-{pose}.png').convert('RGBA');ck(f'Nugget{d}{speed}{i}exact RGBA',a.tobytes()==b.tobytes());ck(f'Nugget{d}{speed}{i}hold',g.info.get('duration')==holds[i])
j={'task':'M1.OWR1','state':'Saved integrity audit; Girl far-foot material concern remains separately under correction','count':len(checks),'passed':sum(c['pass'] for c in checks),'failures':[c for c in checks if not c['pass']],'checks':checks,'PNGpins':pins};(Path(__file__).parent/'saved-walk-audit.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps({'passed':j['passed'],'count':j['count'],'failures':j['failures']}))
