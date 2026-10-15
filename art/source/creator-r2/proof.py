"""Actual pure-rendered combination/GIF proof. UI screenshots are separate."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-CC1';looks=json.loads(Path('/tmp/critz-cc1-renders.json').read_text());checks=[]
def image(pixels):
 im=Image.new('RGBA',(32,64));im.putdata([tuple(bytes.fromhex(q[1:]))+(255,) if q else (0,0,0,0) for q in pixels]);return im
def check(n,v):assert v,n;checks.append(n)
plate=Image.new('RGB',(1180,1040),'#efe9d6');d=ImageDraw.Draw(plate);d.fontmode='1'
for row,dr in enumerate(['south','north','west','east']):
 y=row*260;d.text((6,y+4),dr.upper()+' / 6 REGISTERED LOOKS / NATIVE1x + NEAREST3x / BS2, NO PM1',fill='#253340')
 for col,look in enumerate(looks):
  x=col*195;d.text((x+4,y+20),str(col)+' '+look['name'][:27],fill='#253340');im=image(look['poses'][dr]['idle']);q=im.resize((96,192),Image.Resampling.NEAREST);plate.paste(q,(x+8,y+43),q);plate.paste(im,(x+135,y+145),im)
plate.save(out/'six-looks-four-directions.png')
for n in [2,3]:
 plate=Image.new('RGB',(960,1000),'#efe9d6');d=ImageDraw.Draw(plate);d.fontmode='1';d.text((8,5),looks[n]['name']+' / EXISTING POSES / REGISTERED SOURCE SHAPE',fill='#253340')
 for row,p in enumerate(['idle','A','P','C']):
  y=25+row*240;d.text((4,y+5),p,fill='#253340')
  for col,dr in enumerate(['south','north','west','east']):
   x=30+col*230;d.text((x,y+5),dr.upper(),fill='#253340');im=image(looks[n]['poses'][dr][p]);q=im.resize((96,192),Image.Resampling.NEAREST);plate.paste(q,(x,y+25),q);plate.paste(im,(x+140,y+145),im)
 plate.save(out/f'look{n}-existing-poses.png')
expected=json.loads(Path('/tmp/critz-cc1-gif-expected.json').read_text())
for e in expected:
 for scale in [1,4]:
  name=f"look{e['look']}-{e['direction']}-walk-{scale}x.gif";g=Image.open(out/name);ds=[100]*8 if e['direction']=='south' else [70,60,70,70,70,60,70,70];check(name+' eight slots/loop',g.n_frames==8 and g.info['loop']==0)
  for i,f in enumerate(e['frames']):
   g.seek(i);im=image([e['palette'][n] for n in f['pixels']]).resize((32*scale,64*scale),Image.Resampling.NEAREST);check(name+str(i)+' exact native colors/alpha/holds',g.convert('RGBA').tobytes()==im.tobytes() and g.info['duration']==ds[i])
(out/'render-checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'looks':[{k:v for k,v in l.items() if k!='poses'} for l in looks],'scope':'Pure composition/export evidence; browser screenshots and UI checks are separate; no visual acceptance'},indent=2)+'\n');print('PASS',len(checks),'actual exported GIF RGBA/holds/loop checks')
