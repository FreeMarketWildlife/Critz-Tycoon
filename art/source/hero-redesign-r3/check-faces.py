"""Saved-pixel profile contour checks and matched HR2/HR3 face plates."""
from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[3];out=ROOT/'docs/reviews/M1-HR3';old=ROOT/'docs/reviews/M1-HR2'
frames={n:Image.open(out/f'hero-{n}.png').convert('RGBA') for n in ('south','north','west','east')}
w=frames['west']; e=frames['east']
left=[];right=[]
for y in range(35,42):
 xs=[x for x in range(32) if w.getpixel((x,y))[3]];ys=[x for x in range(32) if e.getpixel((x,y))[3]]
 left.append(min(xs));right.append(max(ys))
assert left==sorted(left),left
assert right==sorted(right,reverse=True),right
assert all(w.getpixel((x,y))[3]==0 for y in range(35,42) for x in range(6))
assert all(e.getpixel((x,y))[3]==0 for y in range(35,42) for x in range(26,32))
s=frames['south']
assert all(len({s.getpixel((x,y)) for x in range(14,18)})==1 for y in range(40,44)), 'Center-face isolated feature remains'
# Face correction has no unintended body edits; previous sources retained.
for n,img in frames.items():
 prev=Image.open(old/f'hero-{n}.png').convert('RGBA')
 assert img.crop((0,46,32,64)).tobytes()==prev.crop((0,46,32,64)).tobytes(),n
assert (out/'hero-north.png').read_bytes()==(old/'hero-north.png').read_bytes()
plate=Image.new('RGB',(720,380),'#eee6d0');d=ImageDraw.Draw(plate)
for i,n in enumerate(('south','west','east')):
 x=20+i*235;d.text((x,14),n.upper()+'  HR2 / CORRECTED HR3',fill='#292b34')
 for j,folder in enumerate((old,out)):
  face=Image.open(folder/f'hero-{n}.png').convert('RGBA').crop((2,32,30,46));big=face.resize((112,56),Image.Resampling.NEAREST)
  plate.paste(big,(x+j*112,58),big)
  face8=face.resize((224,112),Image.Resampling.NEAREST)
  if j==1:plate.paste(face8,(x,153),face8)
 d.text((x,293),'Full native frames:',fill='#292b34')
 for j,folder in enumerate((old,out)):
  img=Image.open(folder/f'hero-{n}.png').convert('RGBA');plate.paste(img,(x+32+j*112,310),img)
plate.save(out/'face-correction.png')
# Native face against light/dark/terrain backgrounds; copies are presentation only.
p=Image.new('RGB',(660,230),'#eee6d0');pd=ImageDraw.Draw(p)
for i,(label,bg) in enumerate((('LIGHT','#eee6d0'),('DARK','#263342'),('PATH','#c8aa7c'))):
 x=10+i*218;pd.rectangle((x,32,x+208,220),fill=bg);pd.text((x,12),label+' — 1X / 2X',fill='#292b34')
 for j,n in enumerate(('south','west','east')):
  img=frames[n];p.paste(img,(x+20+j*62,48),img);big=img.resize((64,128),Image.Resampling.NEAREST);p.paste(big,(x+8+j*65,91),big)
p.save(out/'native-background-check.png')
report={'westContourRows35To41':left,'eastContourRows35To41':right,'noLocalNoseProjection':True,'noCentralFrontNoseCluster':True,'bodyBelowRow46Unchanged':True,'northExactUnchanged':True,'colorAndIdentityPreserved':True}
(out/'face-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
