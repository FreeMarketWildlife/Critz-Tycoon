"""DS1 second revision, base-first internal idle checkpoint. Prior assets read-only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-DS2';src=Path(__file__).parent
pal={'i':'#292634','s':'#80503d','m':'#ac724b','l':'#d19662','h':'#e2ad79','r':'#e87560','d':'#b6494d','w':'#f7e3b8','g':'#b7b6a1','b':'#485b78','n':'#2d3a55','a':'#7b91a3'}
heads={'south':[(6,9),(4,11),(3,12),(3,12),(2,13),(2,13),(2,13),(2,13),(3,12),(4,11),(5,10)],'north':[(5,10),(4,11),(3,12),(2,13),(2,13),(2,13),(2,13),(2,13),(3,12),(3,12),(4,11),(5,10)],'west':[(6,9),(4,11),(3,12),(3,12),(3,12),(3,12),(3,12),(3,12),(4,12),(4,11),(4,11),(5,10)]}
def base(dr):
 im=Image.new('RGBA',(16,32));d=ImageDraw.Draw(im)
 def r(box,c):d.rectangle(box,fill=pal[c])
 def p(pts,c):d.polygon(pts,fill=pal[c])
 # Clothes/shoulders FIRST. Head is drawn over this upper garment volume.
 if dr=='west':
  p([(7,20),(10,20),(12,22),(12,26),(11,27),(5,27),(4,25),(4,22)],'i');r((5,21,11,25),'r');r((10,22,11,25),'d');r((5,22,6,23),'w');r((8,24,10,24),'w')
  p([(5,26),(11,26),(11,28),(6,29),(5,28)],'n');r((6,26,10,27),'b')
  # Relaxed near hand below sleeve and on the torso edge, no forward elbow.
  r((4,23,6,23),'w');r((4,24,4,25),'s');r((5,24,6,25),'m');r((5,24,5,24),'l');im.putpixel((4,26),(0,0,0,0));r((5,26,5,26),'s')
  r((6,29,10,30),'i');r((6,29,9,29),'d');r((7,30,9,30),'g')
 else:
  p([(5,20),(10,20),(12,22),(13,24),(13,26),(11,27),(4,27),(2,26),(2,24),(3,22)],'i');r((4,21,11,25),'r');r((3,23,4,24),'w');r((11,23,12,24),'g');r((5,24,10,24),'w')
  r((2,25,3,26),'m');r((12,25,13,26),'s');r((4,26,11,28),'n');r((5,26,10,26),'b');r((7,28,8,28),'i')
  for x in (4,9):r((x,29,x+2,30),'i');r((x,29,x+2,29),'d');r((x,30,x+2,30),'g')
 # Head occludes shoulders. North rear head reaches lower than front face.
 rows=heads[dr]
 for j,(a,b) in enumerate(rows):
  y=11+j;r((a,y,b,y),'i')
  if b-a>=3:
   r((a+1,y,b-1,y),'m')
   if 1<=j<len(rows)-2:r((a+1,y,max(a+1,b-2),y),'l')
   # Offset crown light plane, no concentric cap or hair-dependent fringe.
   if 1<=j<=3 and b-a>=6:r((a+2,y,b-3,y),'h')
 if dr=='south':
  for x in (4,10):r((x,17,x,18),'i')
  r((2,17,2,18),'m');r((13,17,13,18),'m')
 elif dr=='west':
  r((6,17,6,18),'i');r((11,18,12,19),'s');r((11,18,11,18),'m')
 else:r((2,17,2,18),'m');r((13,17,13,18),'m')
 return im
frames={dr:base(dr) for dr in ['south','north','west']}
for dr,q in frames.items():q.save(out/f'dummy-1x-{dr}-idle.png')
b=Image.new('RGB',(900,660),'#eee8d1');d=ImageDraw.Draw(b);f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',13)
for j,dr in enumerate(['south','north','west']):
 for col,(name,q) in enumerate([('REJECTED DS1',Image.open(root/f'docs/reviews/M1-DS1/dummy-1x-{dr}-idle.png').convert('RGBA')),('REVISED BASE',frames[dr])]):
  x=col*450;y=j*220;d.text((x+10,y+8),name+' '+dr+' 16x32 / INTERNAL',font=f,fill='#292634');big=q.resize((80,160),Image.Resampling.NEAREST);b.paste(big,(x+40,y+30),big);b.paste(q,(x+200,y+100),q)
b.save(out/'base-first-idle-internal.png')
(src/'base-manifest.json').write_text(json.dumps({dr:{'sha256':hashlib.sha256((out/f'dummy-1x-{dr}-idle.png').read_bytes()).hexdigest(),'bounds':q.getbbox()} for dr,q in frames.items()},indent=2)+'\n')
print('Base-first only: three16x32 idle proposals. No refined/allpose rollout.')
