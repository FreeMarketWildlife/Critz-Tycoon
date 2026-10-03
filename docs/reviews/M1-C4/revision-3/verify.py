"""Independent native, grid, source-envelope and contour checks. No image writes.
Usage: python verify.py /path/to/pinned/brendan/walking.png
"""
from pathlib import Path
from collections import Counter
from PIL import Image
import json,sys,hashlib,xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
source=Path(sys.argv[1]);src=Image.open(source)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
old=json.loads((root.parent/'revision-2/measurements.json').read_text())
high=json.loads((root/'hero-32x64.json').read_text())
region_results=[]
def bounds(pts):return [min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts)+1,max(y for x,y in pts)+1]
for m in old['measurements']:
 l,t,r,b=m['annotationWindow']
 ref=bounds([(x,y) for y in range(t,b) for x in range(l,r) if src.getpixel((x,y))])
 expected=[v*2 for v in ref]
 actual=bounds([(x,y) for y in range(t*2,b*2) for x in range(l*2,r*2) if high['rows'][y][x]!='.'])
 assert actual==expected,(m['region'],expected,actual)
 region_results.append({'region':m['region'],'referenceBBox':ref,'target2xBBox':expected,'actual2xBBox':actual,'deviation':[0,0,0,0]})
reports=[];plate=Image.open(root/'hero-grid.png').convert('RGB')
for w,h,z,ox in [(16,32,24,98),(32,64,12,636)]:
 data=json.loads((root/f'hero-{w}x{h}.json').read_text());im=Image.open(root/f'hero-{w}x{h}.png').convert('RGBA');pts=set();colors=set();eye=set()
 assert im.size==(w,h)
 for y,row in enumerate(data['rows']):
  for x,k in enumerate(row):
   p=data['partLabels'][y][x]
   rgba=(0,0,0,0) if k=='.' else (*bytes.fromhex(data['palette'][k][1:]),255)
   assert im.getpixel((x,y))==rgba
   assert plate.getpixel((ox+x*z+z//2,180+y*z+z//2))==(rgba[:3] if k!='.' else (237,240,236))
   assert (k=='.')==(row[w-1-x]=='.')
   assert p==data['partLabels'][y][w-1-x]
   if k!='.':pts.add((x,y));colors.add(rgba)
   if p=='eyes':eye.add((x,y))
 s=w//16
 expected={(x*s+i,y*s+j) for x in [6,9] for y in [19,20] for i in range(s) for j in range(s)}
 assert eye==expected
 assert len(colors)<=15 and set(im.getchannel('A').get_flattened_data())=={0,255}
 assert list(im.getbbox())==data['opaqueBBox']
 seen={next(iter(pts))};todo=list(seen)
 while todo:
  x,y=todo.pop()
  for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if q in pts and q not in seen:seen.add(q);todo.append(q)
 assert seen==pts
 reports.append({'frame':[w,h],'cellsVerified':w*h,'opaqueColors':len(colors),'oneConnectedFigure':True,'symmetryMismatchPairs':0,'exactEyes':True,'sha256':hashlib.sha256((root/f'hero-{w}x{h}.png').read_bytes()).hexdigest()})
assert (root/'hero-16x32.png').read_bytes()==(root.parent/'revision-2/hero-16x32.png').read_bytes()
tree=ET.parse(root/'hero-grid.svg');paths=tree.findall('.//{http://www.w3.org/2000/svg}path')
assert [p.attrib['d'] for p in paths if p.attrib.get('stroke')=='#3e697c']==[f'M{x} {180+j*z}h384' for x,h,z in [(98,32,24),(636,64,12)] for j in range(h+1) if j%10==0 or j==h]
assert [p.attrib['d'] for p in paths if p.attrib.get('stroke')=='#c23a78']==['M290 174v780','M828 174v780']
def mixed(rows):return sum(len({rows[y+j][x+i]!='.' for i in range(2) for j in range(2)})>1 for y in range(0,64,2) for x in range(0,32,2))
before=json.loads((root.parent/'revision-2/hero-32x64.json').read_text())
assert mixed(before['rows'])==0 and mixed(high['rows'])>0
alphaChanged=sum((before['rows'][y][x]!='.')!=(high['rows'][y][x]!='.') for y in range(64) for x in range(32))
boundary=Counter()
for y in range(32):
 for x in range(16):
  v=src.getpixel((x,y))
  if v and any(not(0<=a<16 and 0<=b<32) or src.getpixel((a,b))==0 for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):boundary[str(v)]+=1
result={'status':'pass','frames':reports,'regions':region_results,'mixedAlpha2x2Blocks':{'r2':mixed(before['rows']),'r3':mixed(high['rows'])},'changedAlphaCells':alphaChanged,'referenceBoundaryPaletteCounts':dict(boundary),'limitations':['Envelope and landmark fidelity is measured; per-row occupancy intentionally differs to refine contours.','Mixed-block count proves subdivision, not aesthetic quality. User art acceptance remains pending.','Only one pinned reference front-idle frame was analyzed; no universal Emerald art-process or lighting claim is made.']}
(root/'independent-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','cells':2560,'regions':len(region_results),'mixedBlocks':result['mixedAlpha2x2Blocks'],'changedAlphaCells':alphaChanged,'colors':[r['opaqueColors'] for r in reports]}))
