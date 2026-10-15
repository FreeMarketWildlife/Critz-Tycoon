"""FM2 verifies the existing8 exported slots, never authors a gait/pose."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-FM2';order=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text())['order'];checks=[]
def check(n,v):assert v,n;checks.append(n)
for dr in ['south','north','west','east']:
 for slow in [False,True]:
  frames=[]
  for slot,po in enumerate(order):
   canvas=Image.new('RGB',(144,100),'#bed4d5');d=ImageDraw.Draw(canvas);d.fontmode='1';d.text((2,2),f'{dr} {slot} {po}'+(' SLOW' if slow else ''),fill='#253340')
   for j,path in enumerate([root/f'docs/reviews/M1-PS1/hero-{dr}-{po}.png',out/f'hero-{dr}-{po}.png',out/f'template-{dr}-{po}.png']):
    im=Image.open(path).convert('RGBA');canvas.paste(im,(8+j*48,23),im)
   d.text((2,88),'PRIOR   HERO   TEMPLATE',fill='#253340');frames.append(canvas)
  delays=[100]*8 if dr=='south' else [70,60,70,70,70,60,70,70];delays=[t*(4 if slow else 1) for t in delays]
  for scale in [1,4]:
   imgs=[f.resize((144*scale,100*scale),Image.Resampling.NEAREST) for f in frames];path=out/f'{dr}-walk-{"slow" if slow else "normal"}-{scale}x.gif';imgs[0].save(path,save_all=True,append_images=imgs[1:],duration=delays,loop=0,optimize=False,disposal=2)
   gif=Image.open(path);check(path.name+' eight original slots',gif.n_frames==8);check(path.name+' infinite loop',gif.info['loop']==0)
   for i,expected in enumerate(imgs):
    gif.seek(i);check(path.name+f' slot{i} actual pixels exact',gif.convert('RGB').tobytes()==expected.tobytes());check(path.name+f' slot{i} original export hold',gif.info['duration']==delays[i])
(out/'walk-checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'order':order,'timing':'Original source exports; no emulator cadence claim. South800ms; NWE540ms; SLOW4x durations.','approval':False,'scope':'EXISTING WALK VERIFICATION ONLY; no new pose, gait, geometry, creator or runtime'},indent=2)+'\n');print('PASS',len(checks),'actualGIF pixels/8slots/holds/loop checks')
