"""Three-column reference/Hero/neutral mannequin reviews, fixed registration."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR12';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
original=ext.parent/'brendan-user-reference-original/01agijgmbz561.gif';assert hashlib.sha256(original.read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e'
gif=Image.open(original);hero=[];dummy=[];ref=[]
for i in range(8):
 gif.seek(i);im=Image.new('RGBA',(32,64));im.paste(gif.convert('RGBA').crop((0,0,128,192)).resize((32,48),Image.Resampling.NEAREST),(0,14));ref.append(im);im.save(ext/f'registered-left-{i:02}.png')
 hero.append(Image.open(out/f'walk-{i:02}.png').convert('RGBA'));dummy.append(Image.open(out/f'mannequin-{i:02}.png').convert('RGBA'))
ink='#253340';bg='#9dbac8'
def background(w,h):
 im=Image.new('RGBA',(w,h),bg);d=ImageDraw.Draw(im)
 for y in range(0,h,8):
  for x in range(0,w,8):
   if (x//8+y//8)%2:d.rectangle((x,y,x+7,y+7),fill='#aecbd2')
 return im
def panels(slow=False):
 frames=[]
 for i in range(8):
  im=background(112,96);d=ImageDraw.Draw(im);d.fontmode='1';d.text((2,0),'SLOW4x 400ms' if slow else '100ms / 800ms loop',fill=ink)
  for x,label,sprite in [(4,'REF',ref[i]),(40,'HERO',hero[i]),(76,'DUMMY',dummy[i])]:d.text((x-3 if label=='DUMMY' else x,13),label,fill=ink);im.alpha_composite(sprite,(x,28))
  frames.append(im);im.save(ext/f'triple-{"slow" if slow else "fast"}-{i:02}.png')
 return frames
fast=panels();slow=panels(True)
def project(frames,name):
 palette=[];lookup={}
 for im in frames:
  for px in im.get_flattened_data():
   if px[3]:
    c='#%02x%02x%02x'%px[:3]
    if c not in lookup:lookup[c]=len(palette)+1;palette.append(c)
 assert len(palette)<256
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'custom','width':frames[0].width,'height':frames[0].height,'palette':[None]+palette,'bank':'custom','notes':'Review only; exact native32x64 actors. Proposed neutral construction dummy. No per-column rescale/translation.','frames':[{'name':str(i),'ticks':6,'pixels':[lookup['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in im.get_flattened_data()]} for i,im in enumerate(frames)]}
jobs=[]
for ims,name,path,delay in [(fast,'three-column-native',ext/'source-hero-mannequin-native.gif',100),([im.resize((448,384),Image.Resampling.NEAREST) for im in fast],'three-column-4x',ext/'source-hero-mannequin-4x.gif',100),(slow,'three-column-SLOW4x-native',ext/'source-hero-mannequin-SLOW4x-native.gif',400),([im.resize((448,384),Image.Resampling.NEAREST) for im in slow],'three-column-SLOW4x-4x',ext/'source-hero-mannequin-SLOW4x-4x.gif',400),(hero,'hero-native',out/'hero-native.gif',100),([im.resize((128,256),Image.Resampling.NEAREST) for im in hero],'hero-4x',out/'hero-4x.gif',100),(dummy,'mannequin-native',out/'mannequin-native.gif',100)]:
 temp=ext/(name+'.review-project.json');temp.write_text(json.dumps(project(ims,name),separators=(',',':')));jobs.append({'project':str(temp),'output':str(path),'delayMs':delay})
(ext/'gif-jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
# Actual all8 triples, full native actors and exact3x enlargement.
p=background(1152,640);d=ImageDraw.Draw(p)
for i in range(8):
 x=i%4*288;y=i//4*320;d.text((x+8,y+4),f'FRAME {i} /100ms: REF | HERO | DUMMY',fill=ink)
 for j,im in enumerate((ref[i],hero[i],dummy[i])):
  large=im.resize((96,192),Image.Resampling.NEAREST);p.alpha_composite(large,(x+j*96,y+25));p.alpha_composite(im,(x+j*96+32,y+242))
p.convert('RGB').save(ext/'source-hero-mannequin-all-eight.png')
# Labeled allpose abstract anatomy, exact part colors; no source pixels.
maps=json.loads((src/'scaffold.json').read_text());p=background(1400,560);d=ImageDraw.Draw(p)
poseFiles=[('idle','idle-forward.png','mannequin-idle.png'),('A','walk-00.png','mannequin-00.png'),('P','walk-02.png','mannequin-02.png'),('C','walk-04.png','mannequin-04.png')]
for col,(pose,hf,mf) in enumerate(poseFiles):
 x=col*350;d.text((x+10,8),('PROPOSED IDLE' if pose=='idle' else 'WALK '+pose)+' / CONSTRUCTION',fill=ink);d.text((x+10,23),'All hidden joints PROPOSED',fill=ink)
 im=Image.open(out/mf).convert('RGBA');p.alpha_composite(im.resize((160,320),Image.Resampling.NEAREST),(x+85,40));points=maps['poses'][pose]
 left=[('shoulder','shoulderL',242),('elbow','elbowL',262),('hip','hipL',282),('knee*','kneeL',302),('ankle*','ankleL',322)]
 right=[('ears','earR',220),('torso','torsoCenter',240),('arms','wristR',265),('legs*','kneeR',295),('feet','footR',330)]
 for label,key,yy in left+right:
  xx,sy=points[key];sx=x+85+xx*5;sy=40+sy*5
  if (label,key,yy) in left:tx=x+5;ex=x+75
  else:tx=x+255;ex=x+250
  d.line((sx,sy,ex,yy+5),fill=ink);d.text((tx,yy),label,fill=ink)
 h=Image.open(out/hf).convert('RGBA');p.alpha_composite(h.resize((64,128),Image.Resampling.NEAREST),(x+85,382));d.text((x+165,390),'Clothed Hero 2x',fill=ink);d.text((x+165,409),'same registration',fill=ink)
 d.text((x+10,530),'*hidden joint sites are proposals',fill=ink)
p.convert('RGB').save(out/'anatomy-contact.png')
# Full-frame, fixed registered clothing overlay and joint sites.
p=background(1040,390);d=ImageDraw.Draw(p)
for col,(pose,hf,mf) in enumerate(poseFiles):
 x=col*260+10;d.text((x,8),pose.upper()+' / REGISTERED OUTFIT OVERLAY',fill=ink)
 h=Image.open(out/hf).convert('RGBA');m=Image.open(out/mf).convert('RGBA');m.putalpha(m.getchannel('A').point(lambda a:a//2));overlay=Image.alpha_composite(h,m);large=overlay.resize((128,256),Image.Resampling.NEAREST);p.alpha_composite(large,(x+50,32))
 for key,pt in maps['poses'][pose].items():
  if key not in ('headCenter','torsoCenter','neck'):
   px=x+50+pt[0]*4;py=32+pt[1]*4;d.line((px-2,py,px+2,py),fill='#ffffff');d.line((px,py-2,px,py+2),fill='#ffffff')
 for label,key,yy in [('ear seam','earR',181),('strap anchor','strapR',221),('pack root*','packAttach',249)]:
  pt=maps['poses'][pose][key];px=x+50+pt[0]*4;py=32+pt[1]*4;d.line((px,py,x+180,yy+5),fill=ink);d.text((x+182,yy),label,fill=ink)
 d.text((x+4,308),'White: proposed joint/attachment sites',fill=ink);d.text((x+4,326),'No per-layer fitting or offsets',fill=ink)
 d.text((x+4,344),'*pack root hidden in P / idle',fill=ink)
p.convert('RGB').save(out/'outfit-registration.png')
# Focused ears/backpack/shoe before-after; original-only, contrasting paper.
p=background(1000,510);d=ImageDraw.Draw(p)
for row,(idx,label,box) in enumerate([(0,'EARS / FULL HEAD',(0,32,32,44)),(0,'PACK / SHOULDER STRAPS',(18,42,30,52)),(0,'SHOE SPUR',(14,56,23,63))]):
 old=Image.open(root/f'docs/reviews/M1-HR10-BODY/walk-{idx:02}.png').convert('RGBA');new=hero[idx];y=15+row*165;d.text((10,y),label+' / BEFORE | HR12',fill=ink)
 for j,im in enumerate((old,new)):
  c=im.crop(box).resize(((box[2]-box[0])*8,(box[3]-box[1])*8),Image.Resampling.NEAREST);p.alpha_composite(c,(20+j*400,y+25))
p.convert('RGB').save(out/'bounded-before-after.png')
# Stable original-only full Hero + mannequin checkpoint, native and4x.
p=background(900,340);d=ImageDraw.Draw(p)
for col,(label,name) in enumerate([('PROPOSED IDLE','idle-forward.png'),('STRIDE A','walk-00.png'),('PASSING','walk-02.png'),('STRIDE C','walk-04.png'),('DUMMY P','mannequin-02.png'),('DUMMY A','mannequin-00.png')]):
 x=col*150;im=Image.open(out/name).convert('RGBA');p.alpha_composite(im.resize((128,256),Image.Resampling.NEAREST),(x+10,25));p.alpha_composite(im,(x+55,285));d.text((x+10,5),label,fill=ink)
p.convert('RGB').save(out/'hero-and-mannequin.png')
print('Three-column native/4x/labelled-slow jobs, all8contact, anatomy labels, registered overlay and bounded before/after saved.')
