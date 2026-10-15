from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
root=Path(__file__).resolve().parents[3];dest=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/dummy-ds5');dest.mkdir(parents=True,exist_ok=True);b=Image.new('RGB',(1100,940),'#eee8d1');d=ImageDraw.Draw(b);f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
for row,(po,bf,mf) in enumerate([('idle',2,2),('A',7,8),('P',2,2),('C',8,7)]):
 for col,name in enumerate(['Brendan primary','Man1 primary','DS4 rejected arm','DS5 native','DS5 refined']):
  x=col*220;y=row*235;offset=0
  if col<2:
   n=bf if col==0 else mf;strip=Image.open('/tmp/ds1-primary-reference/'+('brendan-walking.png' if col==0 else 'man_1.png'));q=strip.crop((16*n,0,16*(n+1),32));a=Image.new('L',q.size);a.putdata([255 if v else 0 for v in q.get_flattened_data()]);q=q.convert('RGBA');q.putalpha(a);last=max(j for j in range(32) if any(q.getpixel((i,j))[3] for i in range(16)));offset=30-last;label=f'idx{n} contactrow{last} dy{offset}'
  else:
   p=root/f'docs/reviews/{"M1-DS4" if col==2 else "M1-DS5"}/dummy-{2 if col==4 else 1}x-west-{po}.png'
   if not p.exists():continue
   q=Image.open(p).convert('RGBA');label=f'Original {po}'
  d.text((x+5,y+5),name,font=f,fill='#292634');d.text((x+5,y+24),label,font=f,fill='#485b78');big=q.resize((64,128),Image.Resampling.NEAREST);b.paste(big,(x+25,y+55+offset*4),big);b.paste(q,(x+150,y+120),q);d.line((x+15,y+179,x+120,y+179),fill='#80503d')
  if po=='P':d.text((x+5,y+217),'Idle ref: overlap only',font=f,fill='#80503d')
b.save(dest/'contact-aligned-source-side-gait.png')
