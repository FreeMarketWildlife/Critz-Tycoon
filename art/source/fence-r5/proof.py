from PIL import Image,ImageDraw
from pathlib import Path
out=Path(__file__).resolve().parents[3]/'assets/review/fence-r5';c=Image.new('RGBA',(384,512),'#90bd7d');d=ImageDraw.Draw(c)
for i,style in enumerate(['wood','picket','barbed']):
 x=i*128
 for xx in range(x,x+128,32):
  for yy in range(0,512,32):d.rectangle((xx,yy,xx+31,yy+31),outline='#698b68');d.line((xx,yy+16,xx+31,yy+16),fill='#bcd7a0')
 for n,mask in enumerate([2,10,10,8]):
  im=Image.open(out/f'{style}-{mask}.png');c.alpha_composite(im,(x+n*32,32))
 for n,mask in enumerate([4,5,5,5,1]):
  im=Image.open(out/f'{style}-{mask}.png');c.alpha_composite(im,(x+32,128+n*32))
 for n,mask in enumerate([6,10,8]):c.alpha_composite(Image.open(out/f'{style}-{mask}.png'),(x+n*32,352))
 for n,mask in enumerate([5,1]):c.alpha_composite(Image.open(out/f'{style}-{mask}.png'),(x,384+n*32))
c.save(out/'registration-proof.png')
