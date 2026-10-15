"""DS3 restricted native side idle. Compact DS1 head height; shoulders behind it."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,ast
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-DS3';src=Path(__file__).parent
old=root/'docs/reviews/M1-DS2/dummy-1x-west-idle.png';im=Image.open(old).convert('RGBA');before=im.copy()
# Read only declarative DS1 head/palette maps. Never execute its asset builder.
mod=ast.parse((root/'art/source/dummy-resolution-r1/build.py').read_text());values={}
for n in mod.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('pal','side1'):values[n.targets[0].id]=ast.literal_eval(n.value)
pal=values['pal'];rows=values['side1'];assert len(rows)==11
d=ImageDraw.Draw(im)
def r(box,c):d.rectangle(box,fill=pal[c])
# Preserve DS2 relaxed palm/garment below23. Upper shoulder rises behind head.
d.rectangle((0,0,15,22),fill=(0,0,0,0));d.polygon([(7,19),(10,19),(12,21),(12,22),(4,22),(5,21)],fill=pal['i']);r((6,20,10,22),'r');r((11,21,11,22),'d');r((5,22,5,22),'r')
for j,(a,b) in enumerate(rows):
 y=11+j;r((a,y,b,y),'i')
 if b-a>=3:
  r((a+1,y,b-1,y),'m')
  if j>0 and j<len(rows)-2:r((a+1,y,max(a+1,b-2),y),'l')
  if j>0 and j<4:r((a+2,y,max(a+2,b-3),y),'h')
r((6,17,6,18),'i');r((11,17,12,19),'s');r((11,18,11,18),'m')
assert im.crop((0,23,16,32)).tobytes()==before.crop((0,23,16,32)).tobytes()
im.save(out/'dummy-1x-west-idle.png')
landmarks={'crownRow':11,'eyeRows':[17,18],'chinRow':21,'garmentHiddenShoulderStartsRow':19,'visibleShoulderBesideJawRow':21,'sleeveRow':23,'palmRows':[24,25,26],'soleRow':30,'frameBaselineRow':31,'headAuthoredRows':11,'belowRow23ExactDS2':True,'sha256':hashlib.sha256((out/'dummy-1x-west-idle.png').read_bytes()).hexdigest()}
(src/'landmarks.json').write_text(json.dumps(landmarks,indent=2)+'\n')
f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',13);b=Image.new('RGB',(960,410),'#eee8d1');p=ImageDraw.Draw(b)
for col,(name,q) in enumerate([('DS1 compact / rejected',Image.open(root/'docs/reviews/M1-DS1/dummy-1x-west-idle.png').convert('RGBA')),('DS2 elongated / rejected',before),('DS3 compact overlap / INTERNAL',im)]):
 x=col*320;p.text((x+6,10),name,font=f,fill=pal['i']);big=q.resize((112,224),Image.Resampling.NEAREST);b.paste(big,(x+45,45),big);b.paste(q,(x+230,150),q);p.line((x+30,262,x+190,262),fill=pal['s']);p.text((x+10,295),'Native16x32 / same frame\nCrown11 eyes17..18\nChin21 (DS2:22) sole30',font=f,fill=pal['b'])
b.save(out/'side-idle-compact-overlap-internal.png')
print(landmarks)
