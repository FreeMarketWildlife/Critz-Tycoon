from PIL import Image,ImageColor
from pathlib import Path
import json,hashlib
root=Path('/Users/tanoshi/Documents/ChatGPT/Critz-Tycoon');out=root/'docs/reviews/M1-OVN2/independent-review';out.mkdir(parents=True,exist_ok=True)
checks=[];characters=[]
def check(n,v):checks.append({'name':n,'pass':bool(v)})
for char,review in [('girl','M1-OGH2'),('mom','M1-OM2'),('nugget','M1-ON2')]:
 rows=[];src=root/f'art/source/overnight-{char}-continuation-r1'
 for d in ['south','north','west','east']:
  layerpath=src/(f'{d}/layers.json' if char=='mom' else f'{d}.layers.json');q=json.loads(layerpath.read_text())
  path=root/f'docs/reviews/{review}'/(f'{d}/idle.png' if char=='girl' else f'idle-{d}.png' if char=='mom' else f'{d}-idle.png')
  im=Image.open(path).convert('RGBA');re=Image.new('RGBA',(32,64));order=q.get('order',q.get('renderOrder'))
  if char=='girl':
   layers={l['id']:l for l in q['layers']}
   for n in order:
    l=layers[n]
    if not l.get('visible',True):continue
    p=Image.new('RGBA',(32,64));p.putdata([(0,0,0,0) if not k else (*ImageColor.getrgb(q['palette'][k]),255) for k in l['pixels']]);re.alpha_composite(p)
  else:
   for n in order:
    p=Image.new('RGBA',(32,64));cells=q['layers'][n]
    if isinstance(cells,dict):cells=cells['pixels']
    for cell in cells:
     x,y=cell[:2];color=(*ImageColor.getrgb(cell[2]),255) if isinstance(cell[2],str) else tuple(cell[2:]);p.putpixel((x,y),color)
    re.alpha_composite(p)
  check(f'{char}/{d} exact saved-layer recompose',im.tobytes()==re.tobytes());check(f'{char}/{d} frame',im.size==(32,64))
  a=im.getchannel('A');check(f'{char}/{d} binary alpha',set(a.getdata())<={0,255})
  sites={(x,y) for y in range(64) for x in range(32) if a.getpixel((x,y))};seen=set();pending=[next(iter(sites))]
  while pending:
   s=pending.pop()
   if s in seen:continue
   seen.add(s);x,y=s;pending += [p for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if p in sites and p not in seen]
  check(f'{char}/{d} connected alpha',seen==sites);check(f'{char}/{d} contact61',max(y for x,y in sites)==61)
  oldpath=root/f'docs/reviews/{review}/history-v0'/path.relative_to(root/f'docs/reviews/{review}')
  if oldpath.exists() and d in ['south','north']:
   old=Image.open(oldpath).convert('RGBA');check(f'{char}/{d} full front shoe alpha58+ v0 exact',im.getchannel('A').crop((0,58,32,64)).tobytes()==old.getchannel('A').crop((0,58,32,64)).tobytes());
   if char!='girl':check(f'{char}/{d} front shoe RGBA58+ v0 exact',im.crop((0,58,32,64)).tobytes()==old.crop((0,58,32,64)).tobytes())
  rows.append({'direction':d,'file':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bbox':im.getbbox(),'lowerAlphaWidths58to61':[sum(a.getpixel((x,y))>0 for x in range(32)) for y in range(58,62)]})
 characters.append({'character':char,'poses':rows})
j={'task':'M1.OVN2 fresh continuation static audit','passed':sum(c['pass'] for c in checks),'total':len(checks),'checks':checks,'characters':characters,'visualReview':'Actual all-three corrected boards/native/grid inspected. Girl near puff now distinct rounded volume; shorter sole accents avoid v0 rail. Mom tapered shoes/full near hand improved; small forward rose far-sleeve remains ambiguous. Nugget compact shoes and framed smaller lens improve side read. No walking or user appearance approval inferred.','referenceCaveat':'Original NWE inference, primary family comparisons are occupancy/projection evidence rather than hidden anatomy or shoe quotas.'}
(out/'corrected-static-audit.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps({'passed':j['passed'],'total':j['total'],'failed':[c for c in checks if not c['pass']]}))
