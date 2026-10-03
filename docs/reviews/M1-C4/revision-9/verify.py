from pathlib import Path
from PIL import Image
import json,hashlib,sys
repo=Path(__file__).resolve().parents[4];root=repo/'art/source/hero-idle-r9';out=repo/'assets/review/hero-idle-r9';external=Path(sys.argv[1]);user=json.loads((root/'user-template.rle.json').read_text())
def decode(rle):
 rows=[]
 for row in rle['frames'][0]['rows']:
  r=[]
  for c,n in zip(row[::2],row[1::2]):r += [c]*n
  assert len(r)==32;rows.append(r)
 assert len(rows)==64;return rows
source=decode(user);report={'approved':False,'cellsChecked':0,'bodyTemplatePreserved':True,'outlineDefinition':'one occupied-cell four-neighbor boundary layer; no dilation','assets':[]}
strip=Image.open(external/'five-idles-native.png').convert('RGBA');assert strip.size==(160,64)
for i,slug in enumerate(['a-afro','b-flat-top','c-twists','d-cornrows'],1):
 p=json.loads((root/(slug+'.sprite.json')).read_text());r=json.loads((root/(slug+'.rle.json')).read_text());rows=decode(r);assert p['frames'][0]['pixels']==sum(rows,[])
 masks=json.loads((root/(slug+'-masks.json')).read_text());im=Image.open(out/(slug+'.png')).convert('RGBA');assert im.size==(32,64)
 occupied={(x,y)for y,row in enumerate(rows)for x,c in enumerate(row)if c}
 for y,row in enumerate(rows):
  for x,c in enumerate(row):
   rgba=tuple(bytes.fromhex(p['palette'][c][1:]))+(255,) if c else (0,0,0,0)
   assert im.getpixel((x,y))==rgba==strip.getpixel((i*32+x,y));report['cellsChecked']+=1
   boundary=(x,y) in occupied and any(n not in occupied for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
   assert bool(int(masks['outline'][y][x]))==boundary
   if y>=36:assert bool(c)==bool(source[y][x])==bool(rows[y][31-x])
   assert masks['bodyTemplate'][y][x]==masks['bodyTemplate'][y][31-x]
 for y in range(38,42):
  for x in [12,13,18,19]:assert rows[y][x]==8
 assert im.getbbox()[3]==62
 seen={next(iter(occupied))};stack=list(seen)
 while stack:
  x,y=stack.pop()
  for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if q in occupied and q not in seen:seen.add(q);stack.append(q)
 assert seen==occupied
 assert p['palette']==user['palette']
 report['assets'].append({'slug':slug,'bbox':im.getbbox(),'opaqueColors':len(set(sum(rows,[]))-{0}),'connected':True,'bodyMismatchPixels':0,'sha256':hashlib.sha256((out/(slug+'.png')).read_bytes()).hexdigest()})
reference=Image.open('/Users/tanoshi/.codex/visualizations/2026/10/03/hero-revision-8/five-characters-native.png').convert('RGBA')
assert strip.crop((0,0,32,64)).tobytes()==reference.crop((0,0,32,64)).tobytes();report['brendanUnchanged']=True
(Path(__file__).parent/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
