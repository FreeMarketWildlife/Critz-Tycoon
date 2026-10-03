"""Independent PNG, anatomical-mask and upward-grid verification."""
from pathlib import Path
from PIL import Image
import hashlib, json, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
layout=json.loads((root/'grid-layout.json').read_text())
slugs=['a-afro','b-flat-top','c-twists','d-cornrows']
report={'approval':False,'nativeCellComparisons':0,'gridCellComparisons':0,'anatomyCellComparisons':0,'coordinateSystem':'Y up, 0 bottom, 64 top','figures':[]}
models=[]
for slug,top in zip(slugs,[27,27,28,29]):
 m=json.loads((root/f'{slug}.json').read_text());models.append(m)
 im=Image.open(root/f'{slug}.png').convert('RGBA');assert im.size==(32,64)
 occupied=set();colors=set();parts=[r.split(',') for r in m['parts']];anatomy=[r.split(',') for r in m['anatomyParts']]
 for y in range(64):
  for x in range(32):
   k=m['rows'][y][x];rgb=m['palette'].get(k,'#000000');expected=tuple(bytes.fromhex(rgb[1:]))+(0 if k=='.' else 255,)
   assert im.getpixel((x,y))==expected,(slug,x,y)
   report['nativeCellComparisons']+=1
   assert anatomy[y][x]==anatomy[y][31-x],(slug,'anatomy',x,y)
   assert m['skullMask'][y][x]==m['skullMask'][y][31-x]
   report['anatomyCellComparisons']+=1
   if y>=38:assert parts[y][x]==parts[y][31-x]
   if k!='.':occupied.add((x,y));colors.add(rgb)
 assert len(colors)<=15
 assert list(im.getbbox())==m['opaqueBBox']==[3,top,29,62]
 assert m['anchor']==[16,64]
 assert m['paintedSize']==[26,62-top]
 assert m['reviewCoordinates']['origin']=='bottom-left'
 eyes={(x,y) for y in range(64) for x in range(32) if parts[y][x]=='eyes'}
 assert eyes=={(x,y) for x in [12,13,18,19] for y in range(38,42)}
 for x in [15,16]:
  assert anatomy[36][x]=='face'
  if slug!='c-twists':assert parts[36][x]=='face'
  assert parts[35][x]=='hair'
 todo=[next(iter(occupied))];seen=set(todo)
 while todo:
  x,y=todo.pop()
  for c in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if c in occupied and c not in seen:seen.add(c);todo.append(c)
 assert seen==occupied,(slug,'disconnected')
 mixed=sum(0<sum((x+i,y+j) in occupied for i in range(2) for j in range(2))<4 for x in range(0,32,2) for y in range(0,64,2))
 assert mixed>0
 panels=[]
 for name,entries in layout.items():
  p=next(p for p in entries if p['slug']==slug);panels.append((root/f'{name}.png',p))
  tree=ET.fromstring((root/f'{name}.svg').read_text())
  texts=list(tree.iter('{http://www.w3.org/2000/svg}text'))
  for value in [0,10,20,30,40,50,60,64]:
   assert any(t.text==str(value) and t.attrib.get('x')==str(p['x']-10) and t.attrib.get('y')==str(p['y']+(64-value)*12+5) for t in texts),(name,slug,value)
  paths=list(tree.iter('{http://www.w3.org/2000/svg}path'))
  assert any(t.attrib.get('d')==f'M{p["x"]+192} {p["y"]-5}v778' for t in paths)
 panels.append((root/f'{slug}-grid.png',{'x':50,'y':95}))
 for file,p in panels:
  grid=Image.open(file).convert('RGB')
  for y in range(64):
   for x in range(32):
    pix=im.getpixel((x,y));expected=pix[:3] if pix[3] else (237,240,235)
    assert grid.getpixel((p['x']+12*x+6,p['y']+12*y+6))==expected,(file.name,x,y)
    report['gridCellComparisons']+=1
 report['figures'].append({'id':m['id'],'bbox':im.getbbox(),'paintedSize':m['paintedSize'],'topEdgeReviewY':64-top,'colors':len(colors),'mixedAlpha2x2Blocks':mixed,'anatomyMismatchPairs':0,'connected':True,'sha256':hashlib.sha256((root/f'{slug}.png').read_bytes()).hexdigest()})
# Optional existing local reference plate verifies the same source pixels at the same scale.
external=Path('/Users/tanoshi/.codex/visualizations/2026/10/03/hero-revision-6')
ref_path=Path('/Users/tanoshi/.codex/visualizations/2026/10/03/hero-brendan-comparison/brendan-reference.json')
if (external/'brendan-and-four-grid.png').exists() and ref_path.exists():
 grid=Image.open(external/'brendan-and-four-grid.png').convert('RGB');ref=json.loads(ref_path.read_text())
 for i,m in enumerate([ref]+models):
  for y,row in enumerate(m['rows']):
   for x,k in enumerate(row):
    expected=tuple(bytes.fromhex(m['palette'][k][1:])) if k!='.' else (237,240,235)
    assert grid.getpixel((50+i*450+x*12+6,175+y*12+6))==expected
    report['gridCellComparisons']+=1
 report['externalReferencePlateVerified']=True
repo=root.parents[3]
agent=(repo/'AGENTS.md').read_text()
assert 'docs/ART_BIBLE.md' in agent
assert all(word not in agent for word in ['32×64','28×42','480×320','2×2','skull','hair'])
report['agentsDirectionPointerOnly']=True
(root/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
