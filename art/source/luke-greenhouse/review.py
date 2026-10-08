"""Create exact integer review grids; never rewrite production PNG assets."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[3]
out=root/'assets/review/luke-greenhouse'; doc=root/'docs/reviews/M1-LG1'
font=ImageFont.load_default(size=13)
# Native dimensions retained, one visible review square per source pixel.
s=8; im=Image.new('RGB',(520,600),'#ece7d6');d=ImageDraw.Draw(im); x,y=56,45
idle=Image.open(out/'luke-idle.png').convert('RGBA'); im.paste(idle.resize((256,512),Image.Resampling.NEAREST),(x,y),idle.resize((256,512),Image.Resampling.NEAREST))
for n in range(33):d.line((x+n*s,y,x+n*s,y+512),fill='#b8b3a4',width=1)
for n in range(65):d.line((x,y+n*s,x+256,y+n*s),fill='#b8b3a4',width=1)
for height in [0,10,20,30,40,50,60,64]:
 yy=y+(64-height)*s;d.line((x,yy,x+256,yy),fill='#556f88',width=2);d.text((20,yy-6),str(height),fill='#304052',font=font)
d.line((x+128,y,x+128,y+512),fill='#b34862',width=2)
d.text((x,15),'Luke / 32 x 64 / review scale 8x',fill='#263d42',font=font)
d.text((x+111,565),'X = 16',fill='#a63252',font=font)
d.text((337,64),'Clean 4x',fill='#263d42',font=font)
c=idle.resize((128,256),Image.Resampling.NEAREST);im.paste(c,(345,90),c)
d.text((337,370),'Bounds:',fill='#263d42',font=font);d.text((337,390),'[3,23,29,62]',fill='#263d42',font=font)
d.text((337,420),'Anchor (16,64)',fill='#263d42',font=font)
d.text((337,460),'Y rises upward.',fill='#263d42',font=font)
d.text((337,480),'Source rows run',fill='#263d42',font=font)
d.text((337,500),'top to bottom.',fill='#263d42',font=font)
im.save(doc/'art-luke-grid.png')
sheet=Image.open(out/'luke.png').convert('RGBA');sheet.resize((512,1024),Image.Resampling.NEAREST).save(doc/'art-luke-poses-4x.png')
frames=[]
for col in range(4):
 panel=Image.new('RGBA',(4*128,256),'#d9dcc1')
 for row in range(4):
  f=sheet.crop((col*32,row*64,col*32+32,row*64+64)).resize((128,256),Image.Resampling.NEAREST)
  panel.alpha_composite(f,(row*128,0))
 frames.append(panel.convert('RGB'))
frames[0].save(doc/'art-luke-walk.gif',save_all=True,append_images=frames[1:],duration=[130,140,130,140],loop=0)
# Every source fish phase, silhouette, side and front visible together at same zoom.
fish=Image.open(out/'fish.png').convert('RGBA'); front=Image.open(out/'fish-front.png').convert('RGBA');sil=Image.open(out/'silhouettes.png').convert('RGBA')
rows=Image.new('RGBA',(288,512),'#d9dcc1');rows.alpha_composite(fish,(0,0));rows.alpha_composite(front,(128,0));rows.alpha_composite(sil,(208,0));rows.resize((864,1536),Image.Resampling.NEAREST).save(doc/'art-fish-poses-3x.png')
meta=json.load(open(out/'manifest.json')); masks=json.load(open(root/'art/source/luke-greenhouse/luke.masks.json'))['masks'];metrics={}
for name,ids in masks.items():
 xs=[i%32 for i in ids];ys=[i//32 for i in ids];metrics[name]={'bounds':[min(xs),min(ys),max(xs)+1,max(ys)+1],'area':len(ids)}
json.dump(metrics,open(doc/'art-measurements.json','w'),indent=2)
print(metrics)
# Representative animal grids: full native frame, one square per pixel.
s=8; grid=Image.new('RGB',(4*300,335),'#ece7d6');gd=ImageDraw.Draw(grid)
for j,row in enumerate([0,5,8,11]):
 ox=j*300+32;oy=32;f=front.crop((0,row*32,32,row*32+32)).resize((256,256),Image.Resampling.NEAREST);grid.paste(f,(ox,oy),f)
 gd.text((ox,8),meta['fish']['individuals'][row]['name']+' / 32 x 32',font=font,fill='#263d42')
 for n in range(33):
  gd.line((ox+n*s,oy,ox+n*s,oy+256),fill='#b8b3a4');gd.line((ox,oy+n*s,ox+256,oy+n*s),fill='#b8b3a4')
 for h in [0,10,20,30,32]:
  yy=oy+(32-h)*s;gd.line((ox,yy,ox+256,yy),fill='#556f88',width=2);gd.text((ox-25,yy-6),str(h),font=font,fill='#304052')
 gd.line((ox+128,oy,ox+128,oy+256),fill='#b34862',width=2);gd.text((ox+105,301),'X = 16',font=font,fill='#a63252')
grid.save(doc/'art-fish-grid.png')
loops=[]
for phase in range(2):
 panel=Image.new('RGBA',(256,128),'#d9dcc1')
 for row in range(16):
  for view in range(2):
   src=fish if view==0 else front;xx=(64+phase*32) if view==0 else phase*32
   panel.alpha_composite(src.crop((xx,row*32,xx+32,row*32+32)),((row%8)*32,(row//8)*64+view*32))
 loops.append(panel.resize((768,384),Image.Resampling.NEAREST).convert('RGB'))
loops[0].save(doc/'art-fish-loop.gif',save_all=True,append_images=loops[1:],duration=[240,240],loop=0)
