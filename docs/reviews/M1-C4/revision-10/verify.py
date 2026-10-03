from pathlib import Path
from PIL import Image
import json,hashlib
repo=Path(__file__).resolve().parents[4];root=repo/'art/source/hero-idle-r10';m=json.loads((root/'hero.sprite.json').read_text());s=json.loads((repo/'docs/reviews/M1-C4/revision-7/c-twists.json').read_text());im=Image.open(repo/'assets/review/hero-idle-r10/hero.png').convert('RGBA');outline=json.loads((root/'outline.json').read_text());assert im.size==(32,64)
retained=0;seen=set();occupied=set()
for y in range(64):
 for x in range(32):
  k=m['frames'][0]['pixels'][y*32+x];c=tuple(bytes.fromhex(m['palette'][k][1:]))+(255,) if k else (0,0,0,0);assert im.getpixel((x,y))==c
  before=s['rows'][y][x];assert bool(k)==(before!='.')
  if k:occupied.add((x,y))
  if y>=37:assert bool(k)==bool(m['frames'][0]['pixels'][y*32+31-x])
  if y<=37 and before!='.' and outline[y][x]=='0':assert c[:3]==tuple(bytes.fromhex(s['palette'][before][1:]));retained+=1
  if y>=62:assert not k
for y in range(64):
 for x in range(32):
  boundary=(x,y)in occupied and any(q not in occupied for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
  assert boundary==(outline[y][x]=='1')
  assert (im.getpixel((x,y))==(0,0,0,255))==boundary
for y in range(63):
 for x in range(31):assert not all(im.getpixel((x+dx,y+dy))==(0,0,0,255)for dy in range(2)for dx in range(2))
for y in range(38,42):
 for x in [12,13,18,19]:assert im.getpixel((x,y))==(13,12,13,255)
stack=[next(iter(occupied))];seen=set(stack)
while stack:
 x,y=stack.pop()
 for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if q in occupied and q not in seen:seen.add(q);stack.append(q)
assert seen==occupied
r=json.loads((root/'hero.rle.json').read_text());flat=[]
for row in r['frames'][0]['rows']:
 vals=[]
 for k,n in zip(row[::2],row[1::2]):vals +=[k]*n
 assert len(vals)==32;flat+=vals
assert flat==m['frames'][0]['pixels']
report={'approval':False,'frame':[32,64],'bbox':im.getbbox(),'occupiedPixels':len(occupied),'paletteColors':len(m['palette'])-1,'nativeCellsChecked':2048,'interiorHairRegionCellsPreserved':retained,'silhouetteChangesFromTarget':0,'symmetricBody':True,'bottomPadding':2,'blackOutlineLayers':1,'black2x2Blocks':0,'rleRoundTrip':True,'connected':True,'sha256':hashlib.sha256((repo/'assets/review/hero-idle-r10/hero.png').read_bytes()).hexdigest()}
(Path(__file__).parent/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
