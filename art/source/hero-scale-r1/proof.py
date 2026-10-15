"""Saved native/phase checks and focused four-direction normal/slow review."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-PS1';base=root/'docs/reviews/M1-HR14';nb=root/'docs/reviews/M1-NB3';meta=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());bm=json.loads((root/'art/source/hero-neutral-r3/construction.json').read_text());order=meta['order'];checks=[];report={}
def check(n,v):assert v,n;checks.append(n)
def load(folder,name):return Image.open(folder/name).convert('RGBA')
def connected(im):
 pts={(i%32,i//32) for i,p in enumerate(im.get_flattened_data()) if p[3]};seen={next(iter(pts))};todo=list(seen)
 while todo:
  x,y=todo.pop()
  for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if q in pts and q not in seen:seen.add(q);todo.append(q)
 return pts==seen
for dr in ('south','north','west','east'):
 report[dr]={}
 for po in ('idle','A','P','C'):
  old=load(base,f'hero-{dr}-{po}.png');new=load(out,f'hero-{dr}-{po}.png');body=load(nb/f'{dr}-{po}','neutral-body.png');render=load(nb/f'{dr}-{po}','body-render-with-selected-skin.png');clothes=load(nb/f'{dr}-{po}','removable-appearance.png');e=meta['directions'][dr][po];b=bm['directions'][dr][po]
  check(dr+po+' selected exact layer composition',Image.alpha_composite(render,clothes).tobytes()==new.tobytes());check(dr+po+' hero connected',connected(new));check(dr+po+' neutral connected',connected(body));check(dr+po+' native binary alpha',new.size==body.size==(32,64) and set(new.getchannel('A').get_flattened_data())<={0,255} and set(body.getchannel('A').get_flattened_data())<={0,255});check(dr+po+' skin ownership',all(not clothes.getpixel(tuple(p))[3] and body.getpixel(tuple(p))[3] for p in b['actualVisibleBodyCells']))
  if dr=='south':check(po+' front exact',old.tobytes()==new.tobytes())
  check(dr+po+' hair/head exact',all(new.getpixel((i%32,i//32))==old.getpixel((i%32,i//32)) for i,on in enumerate(e['headMaskHero']) if on))
  check(dr+po+' hand skin exact',all(new.getpixel(tuple(p))==old.getpixel(tuple(p)) for p in e['commonFeatureRegistration']['hands']['cells']))
  if dr!='south' and po=='idle':check(dr+' upper idle=P+2',load(out,'body-'+dr+'-idle.png').crop((0,50,32,56)).tobytes()==load(out,'body-'+dr+'-P.png').crop((0,48,32,54)).tobytes())
  report[dr][po]={'bodyVisibleCells':len(b['actualVisibleBodyCells']),'dressingClippedBodyCells':b['dressingClippedBodyCells'],'headSupportBrownCells':b['explicitHeadSurfaceExtension'],'bodyPartZOrder':b['bodyZOrder'],'selectedHeadAndHandsExact':True,'HeroPNGsha256':hashlib.sha256((out/f'hero-{dr}-{po}.png').read_bytes()).hexdigest()}
 # Compact per-direction4-unique panels, no single huge roster sheet.
 p=Image.new('RGB',(1280,1050),'#bed4d5');d=ImageDraw.Draw(p)
 for row,po in enumerate(('idle','A','P','C')):
  d.text((4,row*260+4),dr+' '+po+' / BEFORE | AFTER | BALD BASE | EXACT RECOMPOSITION',fill='#253340')
  ims=[load(base,f'hero-{dr}-{po}.png'),load(out,f'hero-{dr}-{po}.png'),load(nb/f'{dr}-{po}','neutral-body.png'),load(nb/f'{dr}-{po}','recomposed-hero.png')]
  for col,im in enumerate(ims):
   x=col*320;y=row*260;big=im.resize((96,192),Image.Resampling.NEAREST);p.paste(big,(x+20,y+25),big);p.paste(im,(x+190,y+125),im);d.line((x+20,y+217,x+116,y+217),fill='#748894')
 p.save(out/f'{dr}-unique-review.png')
 for slow in (False,True):
  frames=[]
  for i,po in enumerate(order):
   p=Image.new('RGB',(120,96),'#bed4d5');d=ImageDraw.Draw(p);d.fontmode='1';d.text((1,0),dr+' '+str(i)+(' SLOW' if slow else ''),fill='#253340')
   for j,im in enumerate([load(base,f'hero-{dr}-{po}.png'),load(out,f'hero-{dr}-{po}.png'),load(nb/f'{dr}-{po}','neutral-body.png')]):p.paste(im,(j*40+4,22),im)
   frames.append(p)
  ds=([100]*8 if dr=='south' else [70,60,70,70,70,60,70,70]);ds=[v*(4 if slow else 1) for v in ds]
  for scale in (1,4):
   ims=[p.resize((p.width*scale,p.height*scale),Image.Resampling.NEAREST) for p in frames];dest=out/f'{dr}-{"slow" if slow else "normal"}-{scale}x.gif';ims[0].save(dest,save_all=True,append_images=ims[1:],duration=ds,loop=0,optimize=False,disposal=2);g=Image.open(dest);check(dest.name+' eight slots',g.n_frames==8 and g.info['loop']==0)
   for i,p in enumerate(ims):g.seek(i);check(dest.name+str(i)+' exact pixels/holds',g.convert('RGB').tobytes()==p.tobytes() and g.info['duration']==ds[i])
# Freeze front base and its original part/costume PNGs in addition to Hero front.
for p in (root/'docs/reviews/M1-NB1/south-idle').glob('*.png'):check('South foundation exact '+p.name,p.read_bytes()==(nb/'south-idle'/p.name).read_bytes())
(out/'checks.json').write_text(json.dumps({'scope':'Native-grid side/back + existing bald-base pose review','checks':checks,'allPass':True,'poses':report,'limits':['All body hidden contours reconstructed, not source anatomy','Reference lowest contact pixels kept; contour/material refinements proposed','Bald foundation and scale appearance require independent review','No creator/runtime/save/deployment']},indent=2)+'\n');print('PASS',len(checks),'saved-pixel/base/export protection checks.')
