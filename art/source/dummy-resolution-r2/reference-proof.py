from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
root=Path(__file__).resolve().parents[3];dest=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/dummy-ds2');dest.mkdir(parents=True,exist_ok=True);frames=[]
for name,path in [('Brendan primary','brendan-walking.png'),('Man1 primary','man_1.png')]:
 q=Image.open('/tmp/ds1-primary-reference/'+path).crop((32,0,48,32));a=Image.new('L',q.size);a.putdata([255 if v else 0 for v in q.get_flattened_data()]);q=q.convert('RGBA');q.putalpha(a);frames.append((name,q))
for name,path in [('Rejected DS1','M1-DS1'),('Revised BASE','M1-DS2')]:frames.append((name,Image.open(root/f'docs/reviews/{path}/dummy-1x-west-idle.png').convert('RGBA')))
b=Image.new('RGB',(1120,580),'#eee8d1');d=ImageDraw.Draw(b);f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',13)
for col,(name,q) in enumerate(frames):
 x=col*280;d.text((x+10,10),name,font=f,fill='#292634');big=q.resize((128,256),Image.Resampling.NEAREST);b.paste(big,(x+60,40),big);d.line((x+45,288,x+205,288),fill='#80503d');b.paste(q,(x+225,170),q)
 crop=q.crop((0,17,16,28)).resize((192,132),Image.Resampling.NEAREST);b.paste(crop,(x+30,355),crop);d.text((x+20,325),'Actual jaw/shoulder crop',font=f,fill='#292634');d.text((x+20,510),'Same source rows17..27\nNo individual fitting\nFrame baseline row31',font=f,fill='#485b78')
b.save(dest/'west-base-source-baseline.png')
