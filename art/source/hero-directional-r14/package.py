from PIL import Image,ImageDraw
from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR14';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
meta=json.loads((src/'construction.json').read_text());directions=('south','north','west','east');order=meta['order'];ink='#253340';jobs=[];phasePanels={}
def bg(w,h):
 im=Image.new('RGBA',(w,h),'#9dbac8');d=ImageDraw.Draw(im)
 for y in range(0,h,8):
  for x in range(0,w,8):
   if (x//8+y//8)%2:d.rectangle((x,y,x+7,y+7),fill='#aecbd2')
 return im
def project(frames,name):
 colors=[];look={}
 for im in frames:
  for px in im.get_flattened_data():
   if px[3]:
    c='#%02x%02x%02x'%px[:3]
    if c not in look:look[c]=len(colors)+1;colors.append(c)
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'custom','width':frames[0].width,'height':frames[0].height,'palette':[None]+colors,'bank':'custom','notes':'HR14 review proof only. Actual GIF delays in jobs manifest; no runtime change.','frames':[{'name':str(i),'ticks':6,'pixels':[look['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in im.get_flattened_data()]} for i,im in enumerate(frames)]}
def job(frames,name,target,delays,scale=1):
 f=ext/(name+'.review-project.json');f.write_text(json.dumps(project(frames,name),separators=(',',':')));jobs.append({'project':str(f),'output':str(target),'delaysMs':delays,'deriveNearestScale':scale})
# Source8ticks per phase=133.943ms. Four GIF phase durations130/140/130/140
# total540ms, nearest10ms to exact535.77ms loop. Duplicate pair holds retain
# all8phase comparison slots without claiming a100ms stock engine cadence.
rom=[70,60,70,70,70,60,70,70]
for direction in directions:
 hero=[Image.open(out/f'hero-{direction}-{p}.png').convert('RGBA') for p in order];dummy=[Image.open(out/f'dummy-{direction}-{p}.png').convert('RGBA') for p in order];refs=[Image.open(ext/f'reference-{direction}-{p}.png').convert('RGBA') for p in order]
 delays=[100]*8 if direction=='south' else rom
 for slow in (False,True):
  ds=[n*(4 if slow else 1) for n in delays];panels=[]
  for i in range(8):
   im=bg(112,96);d=ImageDraw.Draw(im);d.fontmode='1';d.text((2,0),direction[0].upper()+(' SLOW4x' if slow else ' GIF100' if direction=='south' else ' ROM~8ticks'),fill=ink)
   for x,label,sprite in [(4,'REF',refs[i]),(40,'HERO',hero[i]),(76,'DUMMY',dummy[i])]:d.text((x-3 if label=='DUMMY' else x,13),label,fill=ink);im.alpha_composite(sprite,(x,28))
   panels.append(im);im.save(ext/f'panel-{direction}-{"slow" if slow else "normal"}-{i:02}.png')
  suffix='-SLOW4x' if slow else '';job(panels,direction+suffix,ext/f'source-hero-template-{direction}{suffix}-native.gif',ds);job([im.resize((448,384),Image.Resampling.NEAREST) for im in panels],direction+suffix+'-4x',ext/f'source-hero-template-{direction}{suffix}-4x.gif',ds)
  if not slow:
   for kind,frames in [('hero',hero),('dummy',dummy)]:job(frames,kind+'-'+direction,out/f'{kind}-{direction}-native.gif',ds)
 # Additional combined board compares matched phase indices; clock explicitly
 #100ms for all directions, NEVER advertised as normal ROM motion playback.
 phasePanels[direction]=[]
 for i in range(8):
  im=bg(112,96);d=ImageDraw.Draw(im);d.fontmode='1';d.text((2,0),direction[0].upper()+' PHASE100ms',fill=ink)
  for x,label,sprite in [(4,'REF',refs[i]),(40,'HERO',hero[i]),(76,'DUMMY',dummy[i])]:d.text((x-3 if label=='DUMMY' else x,13),label,fill=ink);im.alpha_composite(sprite,(x,28))
  phasePanels[direction].append(im)
 p=bg(1152,640);d=ImageDraw.Draw(p)
 for i in range(8):
  x=i%4*288;y=i//4*320;d.text((x+7,y+5),direction.upper()+f' frame{i} / REF | HERO | DUMMY',fill=ink)
  for j,im in enumerate((refs[i],hero[i],dummy[i])):p.alpha_composite(im.resize((96,192),Image.Resampling.NEAREST),(x+j*96,y+25));p.alpha_composite(im,(x+j*96+32,y+242))
 p.convert('RGB').save(ext/f'{direction}-all-eight-source-hero-template.png')
 # True grid: source and Hero separate; aligned boundary/material difference.
 p=bg(1536,460);dd=ImageDraw.Draw(p)
 for n,pose in enumerate(('A','P','C')):
  xx=n*512;dd.text((xx+5,5),direction.upper()+' '+pose+' / SOURCE | HERO lowerrows54..63',fill=ink)
  ref=Image.open(ext/f'reference-{direction}-{pose}.png').convert('RGBA');h=Image.open(out/f'hero-{direction}-{pose}.png').convert('RGBA')
  for k,im in enumerate((ref,h)):
   tile=im.crop((0,54,32,64)).resize((256,80),Image.Resampling.NEAREST);p.alpha_composite(tile,(xx,35+k*132))
   for x in range(33):dd.line((xx+x*8,35+k*132,xx+x*8,115+k*132),fill='#748894')
   for y in range(11):dd.line((xx,35+k*132+y*8,xx+256,35+k*132+y*8),fill='#748894')
   dd.text((xx+260,63+k*132),'SOURCE' if k==0 else 'HERO',fill=ink)
  delta=Image.new('RGBA',(32,10))
  for y in range(54,64):
   for x in range(32):
    a=ref.getpixel((x,y))[3]>0;b=h.getpixel((x,y))[3]>0
    if a or b:delta.putpixel((x,y-54),(248,248,248,255) if a==b else (230,70,70,255) if a else (70,90,230,255))
  p.alpha_composite(delta.resize((256,80),Image.Resampling.NEAREST),(xx,299));dd.text((xx+5,391),'White=both. Red=missing. Blue=excess. Same frame.',fill=ink);dd.text((xx+5,409),'Material masks checked separately; no bare calf inferred.',fill=ink)
 p.convert('RGB').save(ext/f'{direction}-aligned-lower-boundary-grid.png')
for slow in (False,True):
 combined=[]
 for i in range(8):
  im=bg(224,192)
  for n,d in enumerate(directions):im.alpha_composite(phasePanels[d][i],((n%2)*112,(n//2)*96))
  combined.append(im)
 suffix='-SLOW4x' if slow else '';ds=[400 if slow else 100]*8
 if slow:
  # Labelled board slowdown includes label in the pixels, not just filename.
  for im in combined:
   dr=ImageDraw.Draw(im);dr.rectangle((0,0,223,11),fill='#aecbd2');dr.text((2,0),'SLOW4x PHASE BOARD400ms',fill=ink)
 job(combined,'four-direction-phase'+suffix,ext/f'four-direction-PHASE-source-hero-template{suffix}-native.gif',ds);job(combined,'four-direction-phase'+suffix+'-4x',ext/f'four-direction-PHASE-source-hero-template{suffix}-4x.gif',ds,4)
# New dummy sheet includes eyes, ears, clear hands and covered legs/feet; no
# fabricated knee or visible neck. Back eyes physically occluded, not drawn.
p=bg(1440,1280);d=ImageDraw.Draw(p)
for row,direction in enumerate(directions):
 for col,pose in enumerate(('idle','A','P','C')):
  x=col*360;y=row*320;d.text((x+5,y+5),direction.upper()+' '+pose+' / HERO | DUMMY',fill=ink)
  for k,kind in enumerate(('hero','dummy')):
   im=Image.open(out/f'{kind}-{direction}-{pose}.png').convert('RGBA');p.alpha_composite(im.resize((96,192),Image.Resampling.NEAREST),(x+15+k*130,y+23));p.alpha_composite(im,(x+47+k*130,y+221))
  d.text((x+5,y+301),'Head/ears/eyes/hands; knees inferred/occluded',fill=ink)
p.convert('RGB').save(out/'four-direction-featured-dummy-sheet.png')
(ext/'gif-jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
(ext/'preview.html').write_text('<!doctype html><meta charset="utf-8"><style>body{background:#263440;color:white;font:16px sans-serif}section{display:inline-block;vertical-align:top}img{image-rendering:pixelated;max-width:48vw}</style><h1>HR14 review only: source | Hero | dummy</h1><p>Front800ms supplied source; ROM otherdirections540ms approximate535.77ms engine loop. Slow4x. No acceptance.</p>'+''.join('<section><h2>'+d+'</h2><img src="source-hero-template-'+d+'-4x.gif"><img src="source-hero-template-'+d+'-SLOW4x-4x.gif"></section>' for d in directions))
print('Prepared28 GIF jobs,4 all8 sourceproofs + aligned grids, featured dummy sheet. ROMnormal540ms,front800ms; phaseboard explicitly100ms.')
