"""Reference-registered native transfer, per the user's explicit overlay/trace workflow.
Usage: python trace-reference.py COMPLETE_REFERENCE_SCREENSHOT EXTERNAL_REVIEW_DIR
The retained 738×248 complete reference is used because newer zoom crops cut shoe bottoms.
No independent head/hair resizing. Reference-only cutouts stay outside the repository.
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
from collections import deque,Counter
import json,hashlib,sys,shutil
source=Path(sys.argv[1]).resolve()
im=Image.open(source).convert('RGB')
out=Path(sys.argv[2]).resolve();repo=Path(__file__).resolve().parents[4]
assert not out.is_relative_to(repo), 'Keep reference-only cutouts outside the project'
out.mkdir(parents=True,exist_ok=True)
assert im.size==(738,248)
if source!=out/'complete-design-reference.png':shutil.copyfile(source,out/'complete-design-reference.png')
specs=[('a-afro',(15,25,145,243),79.5),('b-flat-top',(205,25,334,243),270),('c-twists',(393,25,525,243),459.25),('d-cornrows',(585,25,714,243),649.75)]
scale=5.25;foot=239;yOrigin=foot-62*scale
models=[]
for slug,box,cx in specs:
 crop=im.crop(box);w,h=crop.size
 # Flood connected paper from the outside; cream cloth and enclosed whites stay intact.
 def paper(x,y):
  c=crop.getpixel((x,y));return min(c)>140 and max(c)-min(c)<22
 bg=set();queue=deque()
 for x in range(w):
  for y in (0,h-1):
   if paper(x,y):bg.add((x,y));queue.append((x,y))
 for y in range(h):
  for x in (0,w-1):
   if paper(x,y) and (x,y) not in bg:bg.add((x,y));queue.append((x,y))
 while queue:
  x,y=queue.popleft()
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<w and 0<=yy<h and (xx,yy) not in bg and paper(xx,yy):bg.add((xx,yy));queue.append((xx,yy))
 mask=Image.new('L',crop.size,255)
 for p in bg:mask.putpixel(p,0)
 cut=crop.convert('RGBA');cut.putalpha(mask);cut.save(out/f'{slug}-reference-cutout.png')
 native=Image.new('RGBA',(32,64));coords=[];colors=[];coverage={}
 xOrigin=cx-16*scale
 # Use covered source area for silhouette registration; keep all body parts together.
 def source_samples(x,y):
  sx=xOrigin+(x+.5)*scale-box[0];sy=yOrigin+(y+.5)*scale-box[1]
  samples=[];inside=0;total=0
  for ix in range(5):
   for iy in range(5):
    xx=round(sx+(ix-2)*scale/5);yy=round(sy+(iy-2)*scale/5);total+=1
    if 0<=xx<w and 0<=yy<h and mask.getpixel((xx,yy)):
     inside+=1;samples.append(crop.getpixel((xx,yy)))
  return inside/total,samples
 for y in range(64):
  for x in range(32):coverage[x,y]=source_samples(x,y)
 for y in range(64):
  for x in range(32):
   cov,samples=coverage[x,y]
   # Only the anatomical silhouette is paired. Hairstyle texture/volume stays as supplied.
   alpha=(cov+coverage[31-x,y][0])/2 if y>=37 else cov
   if alpha>=.5:
    if not samples:samples=coverage[31-x,y][1]
    c=tuple(sorted(v[k] for v in samples)[len(samples)//2] for k in range(3))
    coords.append((x,y));colors.append(c)
 strip=Image.new('RGB',(len(colors),1));strip.putdata(colors)
 q=strip.quantize(colors=24,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
 for p,c in zip(coords,q.getdata()):native.putpixel(p,c+(255,))
 # Preserve exact matched eye boxes; source antialiasing is not a new eye shape.
 eye_color=min((native.getpixel((x,y)) for x in [12,13,18,19] for y in [38,39,40]),key=lambda c:sum(c[:3]))
 for x in [12,13,18,19]:
  for y in range(38,42):native.putpixel((x,y),eye_color)
 # Remove pale screenshot-edge contamination on the outside contour only.
 edge_repairs=[]
 for y in range(64):
  for x in range(32):
   c=native.getpixel((x,y))
   if not c[3]:continue
   edge=any(not(0<=xx<32 and 0<=yy<64) or native.getpixel((xx,yy))[3]==0 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
   if edge and 80<min(c[:3])<190 and max(c[:3])-min(c[:3])<28:
    nearby=[native.getpixel((xx,yy)) for xx in range(max(0,x-2),min(32,x+3)) for yy in range(max(0,y-2),min(64,y+3)) if native.getpixel((xx,yy))[3] and max(native.getpixel((xx,yy))[:3])<80]
    if nearby:edge_repairs.append(((x,y),min(nearby,key=lambda q:sum(q[:3]))))
 for p,c in edge_repairs:native.putpixel(p,c)
 native.save(out/f'{slug}-transfer.png')
 palette={};rows=[]
 for y in range(64):
  row=[]
  for x in range(32):
   rgb=native.getpixel((x,y))
   if not rgb[3]:row.append('.')
   else:
    if rgb not in palette:palette[rgb]=chr(65+len(palette))
    row.append(palette[rgb])
  rows.append(''.join(row))
 m={'slug':slug,'method':'uniform-reference-registration-and-native-trace','cleanup':{'pairedAlphaFromNativeRow':37,'edgeColorRepairs':len(edge_repairs),'eyeRectangles':[[12,38,14,42],[18,38,20,42]],'independentPartScaling':False},'frame':[32,64],'rows':rows,'palette':{k:'#%02x%02x%02x'%rgb[:3] for rgb,k in palette.items()},'bbox':native.getbbox(),'registration':{'sourceCrop':box,'sourceCenterX':cx,'sourceFootEdge':239,'sourcePixelsPerNativePixel':scale,'uniformScale':True,'sourceFrameOrigin':[xOrigin,yOrigin]},'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest()}
 models.append(m)
(out/'transfers.json').write_text(json.dumps(models,indent=2))
plate=Image.new('RGB',(1280,660),'#faf7ef');draw=ImageDraw.Draw(plate)
f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
for i,(slug,box,cx) in enumerate(specs):
 native=Image.open(out/f'{slug}-transfer.png');zoom=native.resize((256,512),Image.Resampling.NEAREST)
 plate.paste(zoom,(25+i*315,55),zoom);draw.text((25+i*315,20),slug,fill='#253438',font=f)
plate.save(out/'transfer-preview.png')
for m in models:
 print(m['slug'],m['bbox'],len(m['palette']))
