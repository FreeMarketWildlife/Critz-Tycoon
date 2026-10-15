"""Directional still/pose/animated proof packaging. References remain external."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR13';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
directions=('south','north','west','east');order=['A','A','P','P','C','C','P','P'];ink='#253340'
def background(w,h):
 im=Image.new('RGBA',(w,h),'#9dbac8');d=ImageDraw.Draw(im)
 for y in range(0,h,8):
  for x in range(0,w,8):
   if (x//8+y//8)%2:d.rectangle((x,y,x+7,y+7),fill='#aecbd2')
 return im
original=ext.parent/'brendan-user-reference-original/01agijgmbz561.gif';assert hashlib.sha256(original.read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e'
gif=Image.open(original);front=[]
for i in range(8):
 gif.seek(i);im=Image.new('RGBA',(32,64));im.paste(gif.convert('RGBA').crop((0,0,128,192)).resize((32,48),Image.Resampling.NEAREST),(0,14));front.append(im)
refids={'north':[5,5,1,1,6,6,1,1],'west':[7,7,2,2,8,8,2,2],'east':[7,7,2,2,8,8,2,2]};fastPanels={};slowPanels={};jobs=[]
def project(frames,name):
 palette=[];lookup={}
 for im in frames:
  for px in im.get_flattened_data():
   if px[3]:
    c='#%02x%02x%02x'%px[:3]
    if c not in lookup:lookup[c]=len(palette)+1;palette.append(c)
 assert len(palette)<256
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'custom','width':frames[0].width,'height':frames[0].height,'palette':[None]+palette,'bank':'custom','notes':'HR13 REVIEW clock100ms; ROM pose image preview is not Emerald engine cadence.32x64 actors with shared anchor16,64.','frames':[{'name':str(i),'ticks':6,'pixels':[lookup['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in im.get_flattened_data()]} for i,im in enumerate(frames)]}
def job(frames,name,path,delay=100):
 p=ext/(name+'.review-project.json');p.write_text(json.dumps(project(frames,name),separators=(',',':')));jobs.append({'project':str(p),'output':str(path),'delayMs':delay})
for direction in directions:
 hero=[Image.open(out/f'hero-{direction}-{p}.png').convert('RGBA') for p in order];dummy=[Image.open(out/f'dummy-{direction}-{p}.png').convert('RGBA') for p in order]
 refs=front if direction=='south' else [Image.open(ext/f'ROM-{n:02}.png').convert('RGBA') for n in refids[direction]]
 if direction=='east':refs=[im.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for im in refs]
 for i,r in enumerate(refs):r.save(ext/f'reference-{direction}-{i:02}.png')
 for slow in (False,True):
  panels=[]
  for i in range(8):
   im=background(112,96);d=ImageDraw.Draw(im);d.fontmode='1'
   title=direction[0].upper()+(' SLOW4x 400ms' if slow else ' GIF 100ms' if direction=='south' else ' POSES 100ms')
   d.text((2,0),title,fill=ink)
   for x,label,sprite in [(4,'REF',refs[i]),(40,'HERO',hero[i]),(76,'DUMMY',dummy[i])]:d.text((x-3 if label=='DUMMY' else x,13),label,fill=ink);im.alpha_composite(sprite,(x,28))
   panels.append(im);im.save(ext/f'panel-{direction}-{"slow" if slow else "fast"}-{i:02}.png')
  (slowPanels if slow else fastPanels)[direction]=panels
  suffix='-SLOW4x' if slow else '';delay=400 if slow else 100
  job(panels,direction+suffix+'-native',ext/f'source-hero-template-{direction}{suffix}-native.gif',delay)
  job([im.resize((448,384),Image.Resampling.NEAREST) for im in panels],direction+suffix+'-4x',ext/f'source-hero-template-{direction}{suffix}-4x.gif',delay)
 job(hero,'hero-'+direction,out/f'hero-{direction}-native.gif');job(dummy,'dummy-'+direction,out/f'dummy-{direction}-native.gif')
 # All8 phase comparisons, including the real duplicate holds.
 p=background(1152,640);d=ImageDraw.Draw(p)
 for i in range(8):
  x=i%4*288;y=i//4*320;d.text((x+7,y+5),direction.upper()+f' frame{i} / REF | HERO | DUMMY',fill=ink)
  for j,im in enumerate((refs[i],hero[i],dummy[i])):p.alpha_composite(im.resize((96,192),Image.Resampling.NEAREST),(x+j*96,y+25));p.alpha_composite(im,(x+j*96+32,y+242))
 p.convert('RGB').save(ext/f'{direction}-all-eight-source-hero-template.png')
 # Original-only three unique walking poses, plus separately labelled idle.
 p=background(1120,380);d=ImageDraw.Draw(p)
 for col,pose in enumerate(('idle','A','P','C')):
  x=col*280;d.text((x+8,5),direction.upper()+' '+pose.upper()+' / HERO | DUMMY',fill=ink)
  for j,kind in enumerate(('hero','dummy')):
   im=Image.open(out/f'{kind}-{direction}-{pose}.png').convert('RGBA');p.alpha_composite(im.resize((128,256),Image.Resampling.NEAREST),(x+4+j*140,25));p.alpha_composite(im,(x+52+j*140,300))
 p.convert('RGB').save(out/f'{direction}-all-poses.png')
# All four directional loops at once, true native actors; per-view4x above.
for slow in (False,True):
 combined=[]
 for i in range(8):
  im=background(224,192)
  for n,direction in enumerate(directions):im.alpha_composite((slowPanels if slow else fastPanels)[direction][i],((n%2)*112,(n//2)*96))
  combined.append(im)
 suffix='-SLOW4x' if slow else '';delay=400 if slow else 100;name='four-direction'+suffix+'-native'
 job(combined,name,ext/f'four-direction-source-hero-template{suffix}-native.gif',delay)
 # Export-only exact enlargement from the validated native project; the
 # resulting896x768 preview exceeds the editor's480px authoring UI limit.
 jobs.append({'project':str(ext/(name+'.review-project.json')),'output':str(ext/f'four-direction-source-hero-template{suffix}-4x.gif'),'delayMs':delay,'deriveNearestScale':4})
(ext/'gif-jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
# Explicit projection masks/occlusion, original-only diagram.
meta=json.loads((src/'projection-and-joints.json').read_text());p=background(1120,400);d=ImageDraw.Draw(p)
for col,direction in enumerate(directions):
 x=col*280;entry=meta['directions'][direction]['idle'];d.text((x+8,8),direction.upper()+' / HEAD > NECK / TORSO',fill=ink)
 for j,kind in enumerate(('Hero','Dummy')):
  im=Image.new('RGBA',(32,64));hm=entry['headMask'+kind];tm=entry['torsoMask'+kind];nm=entry['neckMask'+kind]
  for k in range(2048):
   color='#cf8f67' if hm[k] and tm[k] else '#b8dce0' if hm[k] else '#4ac2b0' if tm[k] else None
   if color:im.putpixel((k%32,k//32),tuple(bytes.fromhex(color[1:]))+(255,))
  p.alpha_composite(im.resize((128,256),Image.Resampling.NEAREST),(x+4+j*140,30))
 d.text((x+8,304),'Warm: head-over-torso overlap',fill=ink);d.text((x+8,322),'Neck primitive visible cells:0 /0',fill=ink);d.text((x+8,340),'Joint site retained, not displayed',fill=ink)
p.convert('RGB').save(out/'projection-occlusion-map.png')
# Part and attachment sites mapped over saved clothing, full frames unchanged.
p=background(1120,420);d=ImageDraw.Draw(p)
for col,direction in enumerate(directions):
 x=col*280+8;entry=meta['directions'][direction]['idle'];d.text((x,8),direction.upper()+' / REGISTERED BODY OVERLAY',fill=ink)
 h=Image.open(out/f'hero-{direction}-idle.png').convert('RGBA');m=Image.open(out/f'dummy-{direction}-idle.png').convert('RGBA');m.putalpha(m.getchannel('A').point(lambda a:a//2));overlay=Image.alpha_composite(h,m);p.alpha_composite(overlay.resize((128,256),Image.Resampling.NEAREST),(x+45,30))
 for key,(xx,yy) in entry['joints'].items():
  if key in ('neck','headCenter','torsoCenter') or direction in ('west','east') and key=='earR':continue
  px=x+45+xx*4;py=30+yy*4;d.line((px-2,py,px+2,py),fill='#ffffff');d.line((px,py-2,px,py+2),fill='#ffffff')
 for label,key,y in [('ear slot','earL',186),('strap slot','strapL',230),('pack slot','packAttach',260)]:
  xx,yy=entry['joints'][key];d.line((x+45+xx*4,30+yy*4,x+183,y+4),fill=ink);d.text((x+186,y),label,fill=ink)
 d.text((x,309),'White: joint/attachment guides',fill=ink);d.text((x,327),'Neck/far ear hidden; retained in data',fill=ink);d.text((x,345),'Hidden joints PROPOSED, not measured',fill=ink);d.text((x,363),'Same frame/anchor; no layer fitting',fill=ink)
p.convert('RGB').save(out/'four-direction-outfit-registration.png')
p=background(1400,560);d=ImageDraw.Draw(p)
for col,direction in enumerate(directions):
 x=col*350;entry=meta['directions'][direction]['idle'];points=entry['joints'];d.text((x+8,7),direction.upper()+' / NEUTRAL CONSTRUCTION',fill=ink);d.text((x+8,23),'Hidden joints PROPOSED',fill=ink)
 im=Image.open(out/f'dummy-{direction}-idle.png').convert('RGBA');p.alpha_composite(im.resize((160,320),Image.Resampling.NEAREST),(x+85,40))
 labels=[('shoulder','shoulderL',243,False),('elbow','elbowL',264,False),('hip','hipL',284,False),('knee*','kneeL',304,False),('ankle*','ankleL',325,False),('ear','earL',220,True),('torso','torsoCenter',244,True),('arms','wristR',267,True),('legs*','kneeR',299,True),('feet','footR',336,True)]
 for label,key,yy,right in labels:
  xx,sy=points[key];tx=x+255 if right else x+5;end=x+250 if right else x+75;d.line((x+85+xx*5,40+sy*5,end,yy+4),fill=ink);d.text((tx,yy),label,fill=ink)
 h=Image.open(out/f'hero-{direction}-idle.png').convert('RGBA');p.alpha_composite(h.resize((64,128),Image.Resampling.NEAREST),(x+85,382));d.text((x+164,393),'Clothed Hero2x',fill=ink);d.text((x+164,411),'registered guide',fill=ink)
 d.text((x+8,530),'*covered joints are original proposals',fill=ink)
p.convert('RGB').save(out/'four-direction-anatomy-contact.png')
# One authorized bounded profile cleanup: preserve its original checkpoint.
p=background(800,535);d=ImageDraw.Draw(p)
for col,direction in enumerate(('west','east')):
 for row,pose in enumerate(('idle','A','P','C')):
  x=col*400+8;y=row*128+8;d.text((x,y),direction.upper()+' '+pose+' / BEFORE | OVERLAP CLEANUP',fill=ink)
  for j,path in enumerate((ext/f'before-cleanup-hero-{direction}-{pose}.png',out/f'hero-{direction}-{pose}.png')):
   im=Image.open(path).convert('RGBA');c=im.crop((4,50,28,64)).resize((144,84),Image.Resampling.NEAREST);p.alpha_composite(c,(x+j*195,y+24))
d.text((8,521),'Same alpha, extent and joints; shoe top lies under continuous garment. No visual acceptance inferred.',fill=ink);p.convert('RGB').save(out/'profile-overlap-cleanup.png')
print(f'{len(jobs)} GIF jobs prepared:4 directional native/4x/slow triples,8 original-only walks, simultaneous native proof.')
