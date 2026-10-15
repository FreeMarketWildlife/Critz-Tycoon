"""External source-colored comparison only. Does not vendor reference artwork."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('--references',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parents[3];r=root/'docs/reviews/M1-DS1';f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12);b=Image.new('RGB',(960,1100),'#eee8d1');d=ImageDraw.Draw(b)
for row,(dr,po,n) in enumerate([('south','idle',0),('north','idle',1),('west','idle',2),('west','A',7),('west','C',8)]):
 for col,name in enumerate(['Brendan primary','Man1 primary','Original16x32','Original32x64']):
  x=col*240;y=row*220;d.text((x+6,y+6),name+' '+dr+'/'+po,font=f,fill='#292634')
  if col<2:
   strip=Image.open(a.references/('brendan-walking.png' if col==0 else 'man_1.png'));q=strip.crop((n*16,0,(n+1)*16,32));alpha=Image.new('L',q.size);alpha.putdata([255 if v else 0 for v in q.get_flattened_data()]);q=q.convert('RGBA');q.putalpha(alpha)
  else:q=Image.open(r/f'dummy-{col-1}x-{dr}-{po}.png').convert('RGBA')
  native=q.copy();q=q.resize((80,160),Image.Resampling.NEAREST);b.paste(q,(x+40,y+35),q);b.paste(native,(x+160,y+110),native)
a.output.parent.mkdir(parents=True,exist_ok=True);b.save(a.output)
