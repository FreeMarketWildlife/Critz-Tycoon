"""Independent PNG decoding: dimensions, authored cells, symmetry, continuity and 1x strip."""
from pathlib import Path
from PIL import Image
import json,sys,hashlib
root=Path(__file__).resolve().parent
external=Path(sys.argv[1])
strip=Image.open(external/'five-characters-native.png').convert('RGBA')
assert strip.size==(160,64)
report={'visualApproval':False,'nativeCellsChecked':0,'stripCellsChecked':0,'displayScale':1,'figures':[]}
for i,slug in enumerate(['a-afro','b-flat-top','c-twists','d-cornrows'],1):
 m=json.loads((root/(slug+'.json')).read_text());im=Image.open(root/(slug+'.png')).convert('RGBA');assert im.size==(32,64)
 for y,row in enumerate(m['rows']):
  assert len(row)==32
  for x,k in enumerate(row):
   expected=tuple(bytes.fromhex(m['palette'][k][1:]))+(255,) if k!='.' else (0,0,0,0)
   assert im.getpixel((x,y))==expected
   assert strip.getpixel((32*i+x,y))==expected
   report['nativeCellsChecked']+=1;report['stripCellsChecked']+=1
   if y>=37:assert bool(im.getpixel((x,y))[3])==bool(im.getpixel((31-x,y))[3])
 for part,rows in m['masks'].items():
  if part!='hair':assert all(row==row[::-1] for row in rows),(slug,part)
 assert all(im.getpixel((x,y))[:3]==tuple(bytes.fromhex(m['palette']['O'][1:])) for x in [12,13,18,19] for y in range(38,42))
 occupied={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]}
 stack=[next(iter(occupied))];seen=set(stack)
 while stack:
  x,y=stack.pop()
  for p in [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]:
   if p in occupied and p not in seen:seen.add(p);stack.append(p)
 assert seen==occupied,(slug,occupied-seen)
 assert im.getbbox()[3]==62
 report['figures'].append({'slug':slug,'bbox':im.getbbox(),'opaqueColors':len(m['palette']),'connected':True,'anatomyMasksSymmetric':True,'sha256':hashlib.sha256((root/(slug+'.png')).read_bytes()).hexdigest()})
ref=json.loads((external/'brendan-reference.json').read_text())
for y,row in enumerate(ref['rows']):
 for x,k in enumerate(row):
  expected=tuple(bytes.fromhex(ref['palette'][k][1:]))+(255,) if k!='.' else (0,0,0,0)
  assert strip.getpixel((x,y))==expected;report['stripCellsChecked']+=1
report['brendanPixelsUnchanged']=True
(root/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
