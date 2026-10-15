from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3];dest=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/dummy-ds4');dest.mkdir(parents=True,exist_ok=True);b=Image.new('RGB',(960,720),'#eee8d1');d=ImageDraw.Draw(b);f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',13)
for row,(po,n) in enumerate([('A',7),('P',2),('C',8)]):
 for col,name in enumerate(['Brendan SOURCE','Man1 SOURCE','Critz NATIVE','Critz REFINED']):
  x=col*240;y=row*240
  if col<2:
   strip=Image.open('/tmp/ds1-primary-reference/'+('brendan-walking.png' if col==0 else 'man_1.png'));q=strip.crop((16*n,0,16*(n+1),32));a=Image.new('L',q.size);a.putdata([255 if v else 0 for v in q.get_flattened_data()]);q=q.convert('RGBA');q.putalpha(a);label=f'EXACT index{n} (not same phase)'
  else:
   p=root/f'docs/reviews/M1-DS4/dummy-{col-1}x-west-{po}.png'
   if not p.exists():continue
   q=Image.open(p).convert('RGBA');label=f'ORIGINAL proposed {po}'
  d.text((x+5,y+5),name,font=f,fill='#292634');d.text((x+5,y+24),label,font=f,fill='#485b78');big=q.resize((80,160),Image.Resampling.NEAREST);b.paste(big,(x+30,y+55),big);b.paste(q,(x+155,y+135),q);d.line((x+20,y+210,x+125,y+210),fill='#80503d')
b.save(dest/'actual-source-gait-indices-comparison.png')
