"""Decode actual outputs; check trace fidelity, registration, anatomy and all display cells."""
from pathlib import Path
from PIL import Image
import json,hashlib,sys
root=Path(__file__).resolve().parent;ex=Path(sys.argv[1]).resolve()
layout=json.loads((root/'grid-layout.json').read_text())
report={'approval':False,'nativeCells':0,'gridCells':0,'pairedAnatomyCells':0,'figures':[],'limitations':['Skull guide is inferred construction, not recovered hidden anatomy.','Screenshot transfer and 24-color quantization are not byte-exact copies of the screenshot.','Reference silhouettes differ from Brendan; this preserves supplied design proportions and registers eyes/feet rather than copying his costume.']}
models=[]
for slug in ['a-afro','b-flat-top','c-twists','d-cornrows']:
 m=json.loads((root/(slug+'.json')).read_text());models.append(m);im=Image.open(root/(slug+'.png')).convert('RGBA')
 assert im.size==(32,64)
 assert im.tobytes()==Image.open(ex/(slug+'-transfer.png')).convert('RGBA').tobytes()
 colors=set();occupied=set()
 for y in range(64):
  for x in range(32):
   k=m['rows'][y][x];expected=tuple(bytes.fromhex(m['palette'][k][1:]))+(255,) if k!='.' else (0,0,0,0)
   assert im.getpixel((x,y))==expected;report['nativeCells']+=1
   assert m['skullGuide'][y][x]==m['skullGuide'][y][31-x]
   if y>=37:
    assert m['constructionZones'][y][x]==m['constructionZones'][y][31-x]
    assert bool(im.getpixel((x,y))[3])==bool(im.getpixel((31-x,y))[3]);report['pairedAnatomyCells']+=1
   if k!='.':colors.add(expected);occupied.add((x,y))
 assert len(colors)<=24
 assert im.getbbox()==tuple(m['bbox'])
 assert im.getbbox()[3]==62
 assert m['registration']['uniformScale'] and m['registration']['sourcePixelsPerNativePixel']==5.25
 assert m['cleanup']['independentPartScaling'] is False
 assert len(set(im.getpixel((x,y)) for x in [12,13,18,19] for y in range(38,42)))==1
 todo=[next(iter(occupied))];seen=set(todo)
 while todo:
  x,y=todo.pop()
  for c in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if c in occupied and c not in seen:seen.add(c);todo.append(c)
 assert seen==occupied,(slug,'disconnected',occupied-seen)
 panels=[]
 for name,positions in layout.items():
  pos=next(p for p in positions if p['slug']==slug)
  panels.append(((ex if name=='five-character-grid' else root)/(name+'.png'),pos))
 panels.append((root/(slug+'-grid.png'),{'x':48,'y':102}))
 for file,p in panels:
  grid=Image.open(file).convert('RGB')
  for y in range(64):
   for x in range(32):
    c=im.getpixel((x,y));expected=c[:3] if c[3] else (237,240,235)
    assert grid.getpixel((p['x']+12*x+6,p['y']+12*y+6))==expected,(file.name,x,y)
    report['gridCells']+=1
  # The pink centerline and colored ten-height guides are observed in the output.
  assert grid.getpixel((p['x']+192,p['y']-2))==(196,57,118)
  for height in [0,10,20,30,40,50,60,64]:
   assert grid.getpixel((p['x']+2,p['y']+(64-height)*12))!=(237,240,235)
 report['figures'].append({'id':m['id'],'bbox':m['bbox'],'paintedSize':[m['bbox'][2]-m['bbox'][0],m['bbox'][3]-m['bbox'][1]],'colors':len(colors),'connected':True,'bodyAlphaMismatchPairs':0,'sourceTransform':m['registration'],'sha256':hashlib.sha256((root/(slug+'.png')).read_bytes()).hexdigest()})
ref=json.loads((ex/'brendan-reference.json').read_text());grid=Image.open(ex/'five-character-grid.png').convert('RGB')
for y,row in enumerate(ref['rows']):
 for x,k in enumerate(row):
  expected=tuple(bytes.fromhex(ref['palette'][k][1:])) if k!='.' else (237,240,235)
  assert grid.getpixel((48+x*12+6,176+y*12+6))==expected
  report['gridCells']+=1
report['referenceUnchanged']=True
(root/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
