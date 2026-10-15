"""Verify actual GH1 pixels against protected native sources; never art approval."""
from pathlib import Path
from PIL import Image
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-GH1'
meta=json.loads((src/'construction.json').read_text());checks=[]
def check(name,value):
 checks.append({'name':name,'pass':bool(value)});assert value,name
old=Image.open(root/'assets/review/idle-collection-v1/hero-girl.png').convert('RGBA');girl=Image.open(out/'girl-front-idle.png').convert('RGBA');dummy=Image.open(out/'girl-front-construction.png').convert('RGBA');head=Image.open(out/'head-layer.png').convert('RGBA');body=Image.open(out/'body-layer.png').convert('RGBA');base=Image.open(root/'docs/reviews/M1-HR14/body-layer-south-idle.png').convert('RGBA');parts=json.loads((root/'art/source/idle-collection-v1/hero-girl.masks.json').read_text())
for name,im in [('girl',girl),('construction',dummy),('head',head),('body',body)]:
 check(name+' 32x64 binary alpha',im.size==(32,64) and set(im.getchannel('A').get_flattened_data())<={0,255})
 if name in ('girl','construction'):
  p=json.loads((src/('girl-front-idle.sprite.json' if name=='girl' else 'girl-front-construction.sprite.json')).read_text());pal=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in p['palette'][1:]]
  check(name+' editable exact PNG',list(im.get_flattened_data())==[pal[i] for i in p['frames'][0]['pixels']])
  check(name+' single static frame',len(p['frames'])==1)
check('shared frame-edge anchor',meta['edgeAnchor']==[16,64])
check('girl <=15 colors',len(set(p for p in girl.get_flattened_data() if p[3]))<=15)
check('original C6 equals C7 front still',old.tobytes()==Image.open(root/'assets/review/living-collection-v1/hero-girl/frame-1.png').convert('RGBA').tobytes())
allowed={tuple(p) for p in meta['earOverrideAllowed']}
protected=[(i%32,i//32) for i,k in enumerate(parts['visibleParts']) if k in {'skull','hair','eyes','accessory'} and i//32<=44 and (i%32,i//32) not in allowed]
check('protected original head pixels exact',all(head.getpixel(p)==old.getpixel(p) for p in protected))
check('no inherited neck/collar rows45-46',all(head.getpixel((x,y))[3]==0 for y in range(45,64) for x in range(32)))
ears={tuple(p) for p in meta['earCells']}
check('26 actual mirrored ear cells',len(ears)==26 and all((31-x,y) in ears and girl.getpixel((x,y))==girl.getpixel((31-x,y)) for x,y in ears))
check('cleared old outer ear columns',all(head.getpixel((x,y))[3]==0 for x in (3,28) for y in range(37,42)))
eyes={tuple(p) for p in meta['eyeCells']};expected={(x,y) for x in (12,13,18,19) for y in range(38,42)}
check('two 2x4 eyes exact and unoccluded',eyes==expected and all(girl.getpixel(p)==old.getpixel(p) for p in eyes))
check('no new face nose/mouth pixels',all(head.getpixel((x,y))==old.getpixel((x,y)) for x in range(8,24) for y in range(35,45)))
for key in ('puffMask','tieMask'):
 points=[(i%32,i//32) for i,v in enumerate(meta[key]) if v]
 check(key+' source pixels exact',len(points)>0 and all(girl.getpixel(p)==old.getpixel(p) for p in points))
check('composite equals declared layers',girl.tobytes()==Image.alpha_composite(body,head).tobytes())
check('body silhouette unchanged from HR14',body.getchannel('A').tobytes()==base.getchannel('A').tobytes())
check('all final rows45+ retain HR14 silhouette',girl.getchannel('A').crop((0,45,32,64)).tobytes()==base.getchannel('A').crop((0,45,32,64)).tobytes())
check('construction exactly matches final silhouette',dummy.getchannel('A').tobytes()==girl.getchannel('A').tobytes())
skin={(168,112,56),(196,142,74),(120,72,32)}
check('no exposed central neck column45-48',all(girl.getpixel((x,y))[:3] not in skin for y in range(45,49) for x in range(11,21)))
check('all actual body skin matches hand mask',{(x,y) for y in range(47,64) for x in range(32) if girl.getpixel((x,y))[3] and girl.getpixel((x,y))[:3] in skin}=={tuple(p) for p in meta['handCells']})
burgundy={(x,y) for y in range(64) for x in range(32) if girl.getpixel((x,y))==(128,57,78,255)}
check('selected burgundy restored only near soles',len(burgundy)>0 and all(57<=y<=59 for x,y in burgundy) and burgundy<={tuple(p) for p in meta['burgundyMaterialCells']})
check('no skin lower legs',all(girl.getpixel((x,y))[:3] not in skin for y in range(54,64) for x in range(32)))
check('hidden anatomy unresolved',all(v is None for v in meta['hiddenJoints'].values()))
occupied={(x,y) for y in range(64) for x in range(32) if girl.getpixel((x,y))[3]};seen={next(iter(occupied))};todo=list(seen)
while todo:
 x,y=todo.pop()
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
  p=(x+dx,y+dy)
  if p in occupied and p not in seen:seen.add(p);todo.append(p)
check('single 4-connected visible character',seen==occupied)
report={'task':'M1.GH1','result':'PASS technical checks; visual approval pending','checks':checks,'nativeBounds':list(girl.getbbox()),'paintedLastRow':girl.getbbox()[3]-1,'edgeAnchor':meta['edgeAnchor'],'colors':len(set(p for p in girl.get_flattened_data() if p[3])),'protectedHeadPixels':len(protected),'burgundyPixels':len(burgundy),'limits':['One FRONT idle only; no girl-specific observed gait or directional reference.','Old C6 skull is authored scaffold, not observed bones.','HR14 shared body is declared adaptation; no hidden anatomy inferred.','Pixel checks are not independent review or user approval.'],'hashes':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(list(src.glob('*.sprite.json'))+[out/'girl-front-idle.png',out/'girl-front-construction.png'])}}
(out/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(len(checks),'GH1 technical checks passed; visual approval pending.')
