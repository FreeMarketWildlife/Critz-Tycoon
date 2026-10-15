"""Saved-pixel HR7 body review; preserve HR6 heads, external reference only."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys
root=Path(__file__).resolve().parents[3];base=Path(__file__).parent;out=root/'docs/reviews/M1-HR7';old=root/'docs/reviews/M1-HR6';ext=Path(sys.argv[1]).resolve();assert ext!=root and root not in ext.parents
rp=ext/'walking.png';assert hashlib.sha256(rp.read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
new={n:Image.open(out/f'hero-{n}.png').convert('RGBA') for n in ('south','north','west','east')};prior={n:Image.open(old/f'hero-{n}.png').convert('RGBA') for n in new}
m=json.loads((base/'masks.json').read_text());oldm=json.loads((root/'art/source/hero-redesign-r6/masks.json').read_text())
src=json.loads((base/'hero-boy.sprite.json').read_text());assert src['defaultFeatures']=={'mouth':None,'nose':None,'body':'normal'}
report={'earsComponent':'accepted by parent HR6 review','wholeNormalBody':'pending review','canvas':[32,64],'groundAnchor':[16,64],'directions':{},'laterStagesStarted':False}
land={'status':'Proposed visible costume/pose landmarks for HR7 review; no hidden-anatomy measurement','canvas':[32,64],'anchor':[16,64],'directions':{}}
def bbox(mask):
 q=[(i%32,i//32) for i,v in enumerate(mask) if v]
 return [min(x for x,y in q),min(y for x,y in q),max(x for x,y in q)+1,max(y for x,y in q)+1] if q else None
for n,img in new.items():
 assert img.crop((0,0,32,46)).tobytes()==prior[n].crop((0,0,32,46)).tobytes(),n+' head drift'
 for k in ('hair','face','eyes','leftEar','rightEar','nearEar','jawContact','mouth','nose'):
  if k in oldm[n]:assert m[n][k]==oldm[n][k],(n,k)
 assert sum(m[n]['mouth'])==sum(m[n]['nose'])==0
 changes=[(x,y) for y in range(64) for x in range(32) if img.getpixel((x,y))!=prior[n].getpixel((x,y))]
 assert all(y>=46 for x,y in changes)
 assert img.getbbox()[3]==62
 report['directions'][n]={'headRows0To45ExactHR6':True,'acceptedEarsAndHairMasksExact':True,'defaultMouthNoseEmpty':True,'changedPixels':len(changes),'changedBounds':[min(x for x,y in changes),min(y for x,y in changes),max(x for x,y in changes)+1,max(y for x,y in changes)+1],'sha256':hashlib.sha256((out/f'hero-{n}.png').read_bytes()).hexdigest()}
 keys=['shirt','sleeve','leftArm','rightArm','nearArm','shorts','leftFoot','rightFoot','nearFoot','farFoot','pack']
 land['directions'][n]={'visibleRegionBounds':{k:bbox(m[n][k]) for k in keys if k in m[n]},'shoulderGuideRow':46,'sleeveToForearmGuideRow':50,'hipGarmentGuideRow':54,'knee':'not separately visible; shorts/shoe overlap is not a measured knee','soleLastPaintedRow':61,'feetAnchor':[16,64]}
# Profile hand remains under sleeve rather than projecting forward of it.
for n in ('west','east'):
 hand=bbox(m[n]['nearArm']);sleeve=bbox(m[n]['sleeve']);assert hand[0]>=sleeve[0] and hand[2]<=sleeve[2],(n,hand,sleeve)
 report['directions'][n]['forearmBoundsUnderSleeve']=True
# No long cream/light sole bands in bottom contact rows.
light={tuple(bytes.fromhex(c))+(255,) for c in ('f9edc8','bfc0aa')}
assert all(new[n].getpixel((x,y)) not in light for n in new for y in (59,60,61) for x in range(32))
report['brightSoleRailsRemoved']=True
(out/'body-checks.json').write_text(json.dumps(report,indent=2)+'\n');(base/'body-landmarks.proposed.json').write_text(json.dumps(land,indent=2)+'\n')
# Focused body crops, full registered frames at3x, then native on light/dark.
p=Image.new('RGB',(920,530),'#eee6d0');d=ImageDraw.Draw(p)
for i,n in enumerate(new):
 x=12+i*230;d.text((x,10),n.upper()+' | HR6 / HR7 BODY',fill='#292b34')
 for j,group in enumerate((prior,new)):
  img=group[n];big=img.resize((96,192),Image.Resampling.NEAREST);p.paste(big,(x+110*j,32),big)
  crop=img.crop((0,44,32,64)).resize((96,60),Image.Resampling.NEAREST);p.paste(crop,(x+110*j,242),crop)
  p.paste(img,(x+32+110*j,335),img)
 d.rectangle((x,411,x+215,521),fill='#263342')
 for j,group in enumerate((prior,new)):p.paste(group[n],(x+32+110*j,430),group[n])
p.save(out/'body-before-after.png')
# Four isolated body panels enlarged6x, useful for shoulder-elbow-hip-shoe critique.
p=Image.new('RGB',(850,190),'#eee6d0');d=ImageDraw.Draw(p)
for i,n in enumerate(new):
 x=8+i*210;d.text((x,8),n.upper()+' HR7 | BODY6X',fill='#292b34');crop=new[n].crop((0,44,32,64)).resize((192,120),Image.Resampling.NEAREST);p.paste(crop,(x,32),crop)
p.save(out/'body-detail-6x.png')
# Reference source overlays, exact doubled raster, full frame shared registration.
sheet=Image.open(rp);r=sheet.convert('RGBA');a=Image.new('L',sheet.size);a.putdata([255 if v else 0 for v in sheet.get_flattened_data()]);r.putalpha(a)
p=Image.new('RGB',(1000,680),'#eee6d0');d=ImageDraw.Draw(p)
for i,(n,f) in enumerate([('south',0),('north',1),('west',2),('east',2)]):
 x=15+(i%2)*500;y=15+(i//2)*330;d.text((x,y),n.upper()+' | REFERENCE2X / HR7 NORMAL / ACTUAL50% OVERLAY',fill='#292b34')
 ref=r.crop((16*f,0,16*f+16,32)).resize((32,64),Image.Resampling.NEAREST)
 if n=='east':ref=ref.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 t=new[n].copy();t.putalpha(t.getchannel('A').point(lambda n:round(n*.5)));over=Image.alpha_composite(ref,t)
 for j,img in enumerate((ref,new[n],over)):
  big=img.resize((128,256),Image.Resampling.NEAREST);p.paste(big,(x+j*155,y+28),big)
 d.text((x,y+296),'Same frame/anchor. Visible garments, not inferred hidden anatomy.',fill='#292b34')
p.save(ext/'normal-body-reference-overlay.png')
# Per-direction visible landmark guide, preserving full native32x64 canvases.
p=Image.new('RGB',(720,335),'#eee6d0');d=ImageDraw.Draw(p)
for i,n in enumerate(new):
 x=20+i*174;d.text((x,8),n.upper(),fill='#292b34');big=new[n].resize((128,256),Image.Resampling.NEAREST);p.paste(big,(x,28),big)
 for row,col in ((46,'#61918b'),(50,'#a28c52'),(54,'#9572a0'),(62,'#797165')):d.line((x,28+row*4,x+128,28+row*4),fill=col)
d.text((20,306),'Guides: shoulder46 / sleeve-elbow50 / hip54 / foot edge62. Knee hidden.',fill='#292b34');p.save(out/'visible-landmark-guides.png')
print(json.dumps(report,indent=2))
# Standalone current native/light/dark comparison, no reference or old art.
p=Image.new('RGB',(600,445),'#eee6d0');d=ImageDraw.Draw(p)
for i,n in enumerate(new):
 x=8+i*150;d.text((x,8),n.upper()+' | 1X / 2X',fill='#292b34')
 p.paste(new[n],(x+14,111),new[n]);big=new[n].resize((64,128),Image.Resampling.NEAREST);p.paste(big,(x+68,47),big)
 d.rectangle((x,218,x+142,435),fill='#263342');p.paste(new[n],(x+14,328),new[n]);p.paste(big,(x+68,264),big)
p.save(out/'native-light-dark.png')
# Actual BEFORE/AFTER source-over reference overlays for all directions, external only.
p=Image.new('RGB',(1000,680),'#eee6d0');d=ImageDraw.Draw(p)
for i,(n,f) in enumerate([('south',0),('north',1),('west',2),('east',2)]):
 x=15+(i%2)*500;y=15+(i//2)*330;d.text((x,y),n.upper()+' | HR6 OVERLAY / HR7 OVERLAY / HR7 CLEAN',fill='#292b34')
 ref=r.crop((16*f,0,16*f+16,32)).resize((32,64),Image.Resampling.NEAREST)
 if n=='east':ref=ref.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 values=[]
 for group in (prior,new):
  t=group[n].copy();t.putalpha(t.getchannel('A').point(lambda v:round(v*.5)));values.append(Image.alpha_composite(ref,t))
 values.append(new[n])
 for j,img in enumerate(values):
  big=img.resize((128,256),Image.Resampling.NEAREST);p.paste(big,(x+j*155,y+28),big)
 d.text((x,y+296),'Same reference, scale and anchor; accepted head pixels stay exact.',fill='#292b34')
p.save(ext/'body-overlay-before-after.png')
# Proposed drawing guides only; knees are hidden, no reference bone coordinates invented.
for n in land['directions']:
 side=n in ('west','east');center=17 if n=='west' else 15 if n=='east' else 16
 land['directions'][n]['proposedConstructionGuidePoints']={'shoulder':[[center,47]] if side else [[7,47],[25,47]],'elbow':[[center,51]] if side else [[6,51],[26,51]],'hipCenter':[center if side else 16,54],'knee':None,'soleBaselineY':62}
 land['directions'][n]['guidePointStatus']='Original drawing guide edge coordinates; shoulder/elbow/knee anatomy is partly hidden by clothing. Not measured reference bones.'
(base/'body-landmarks.proposed.json').write_text(json.dumps(land,indent=2)+'\n')
for n in ('west','east'):
 img=new[n];frontX=range(11,14) if n=='west' else range(18,21)
 assert all(img.getpixel((x,y)) not in light for y in range(50,55) for x in frontX),n+' dangling pale front edge'
 assert any(a and b for a,b in zip(m[n]['nearArm'],m[n]['sleeve'])),n+' unattached sleeve/arm masks'
 # Internal ankle rows may have isolated contours, never another full-width dark rail.
 ink=(36,35,48,255)
 for y in (56,57,58):
  longest=run=0
  for x in range(10,22):
   run=run+1 if img.getpixel((x,y))==ink else 0;longest=max(longest,run)
  assert longest<=3,(n,y,longest)
 report['directions'][n]['noDanglingCreamFrontStrip']=True
 report['directions'][n]['sleeveArmMasksTouch']=True
 report['directions'][n]['internalAnkleRailsRemoved']=True
(out/'body-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS second-pass pale-edge, sleeve attachment and internal ankle-rail checks.')
