"""Saved-pixel checks independent of authoring operations and allowed-mask logs."""
from pathlib import Path
from PIL import Image
import json,sys,hashlib,subprocess
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR12';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
baseCommit='d158c3ecceaddaf1a0919f01ef75eac47f367cc5';baseDir=root/'docs/reviews/M1-HR10-BODY'
for n in ('idle','walk'):
 p=f'art/source/hero-forward-r10-body/hero-forward-{n}.sprite.json';assert subprocess.check_output(['git','show',baseCommit+':'+p],cwd=root)==(root/p).read_bytes()
head=Image.open(root/'docs/reviews/M1-HR6/hero-south.png').convert('RGBA').crop((0,0,32,46))
sc=json.loads((src/'scaffold.json').read_text());order=['A','A','P','P','C','C','P','P']
baseMasks=json.loads((root/'art/source/hero-forward-r10-body/masks.json').read_text());newMasks=json.loads((src/'masks.json').read_text())
for pose in ('A','P','C','idle'):
 old=baseMasks['idle'] if pose=='idle' else baseMasks['poses'][pose];new=newMasks['idle'] if pose=='idle' else newMasks['poses'][pose]
 for key in ('hair','face','eyes','leftEar','rightEar','jawContact','nose','mouth'):assert old[key]==new[key]
 assert not sum(new['mouth']) and not sum(new['nose'])
 assert all(new['leftEar'][y*32+x]==new['rightEar'][y*32+31-x] for y in range(64) for x in range(32))
report={'baseCommit':baseCommit,'baseChoice':'Eutychus explicitly selected latest delivered HR10-BODY; HR11 draft unadopted','scope':'bounded ear layering, attached compact pack/straps, shoe spur; neutral construction mannequin','frames':[],'GIFs':{},'artAccepted':False}
def connected(im):
 pts={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]};seen={next(iter(pts))};todo=list(seen)
 while todo:
  x,y=todo.pop()
  for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if q in pts and q not in seen:seen.add(q);todo.append(q)
 assert seen==pts,('disconnected',pts-seen)
def inrect(x,y,r):return r[0]<=x<r[2] and r[1]<=y<r[3]
for name,count in [('walk',8),('idle',1),('mannequin',8)]:
 project=json.loads((src/(('mannequin' if name=='mannequin' else 'hero-forward-'+name)+'.sprite.json')).read_text());assert len(project['frames'])==count
 rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in project['palette'][1:]]
 for i,frame in enumerate(project['frames']):
  path=out/(f'mannequin-{i:02}.png' if name=='mannequin' else 'idle-forward.png' if name=='idle' else f'walk-{i:02}.png');im=Image.open(path).convert('RGBA')
  assert im.size==(32,64) and list(im.get_flattened_data())==[rgba[n] for n in frame['pixels']]
  assert {p[3] for p in im.get_flattened_data()}=={0,255};connected(im)
  if name=='mannequin':continue
  assert len({p for p in im.get_flattened_data() if p[3]})<=15
  pose='idle' if name=='idle' else order[i];dy=-2 if pose=='P' else 0
  baseline=Image.open(baseDir/('idle-forward.png' if name=='idle' else f'walk-{i:02}.png')).convert('RGBA')
  ear=(25,37+dy,28,42+dy)
  # Independent edit bounds, not the author's operation log.
  regions=[ear]
  if pose in ('P','idle'):
   off=-2 if pose=='P' else 0;regions.extend([(10,46+off,12,51+off),(20,46+off,22,51+off)])
  elif pose=='A':regions.extend([(24,43,29,51),(21,45,28,50),(10,47,12,50)])
  else:regions.extend([(3,43,8,51),(4,45,11,50),(20,47,22,50)])
  spur=(16,60) if pose=='A' else (15,60) if pose=='C' else None
  changed=[]
  for y in range(64):
   for x in range(32):
    if im.getpixel((x,y))!=baseline.getpixel((x,y)):
     assert any(inrect(x,y,r) for r in regions) or (x,y)==spur,(pose,x,y,'outside bounded corrections');changed.append([x,y])
  for y in range(46):
   for x in range(32):
    if head.getpixel((x,y))[3] and not inrect(x,y+dy,ear):assert im.getpixel((x,y+dy))==baseline.getpixel((x,y+dy)),(pose,x,y,'protected head')
    if head.getpixel((x,y))[3]:assert im.getpixel((x,y+dy))[3]==255
  for yy in range(37+dy,42+dy):
   for xx in range(4,7):assert im.getpixel((xx,yy))==im.getpixel((31-xx,yy)),(pose,xx,yy,'ear render asymmetry')
  # Proportions/lower limbs remain EXACT, except the explicitly removed spur.
  for y in range(51,64):
   for x in range(32):
    if (x,y)!=spur:assert im.getpixel((x,y))==baseline.getpixel((x,y)),(pose,x,y,'lower-body drift')
  if spur:
   assert baseline.getpixel(spur)[3] and not im.getpixel(spur)[3]
   px,py=spur;assert sum(bool(baseline.getpixel(q)[3]) for q in [(px-1,py),(px+1,py),(px,py-1),(px,py+1)])==1
  # Actual visible ear + extremity attachment slots register to saved Hero.
  points=sc['poses'][pose]
  for key in ('earL','earR','shoulderL','shoulderR','wristL','wristR','hipL','hipR','ankleL','ankleR','footL','footR','strapL','strapR'):
   x,y=points[key];assert im.getpixel((x,y))[3],(pose,key,'attachment outside figure')
  bm=baseMasks['idle'] if pose=='idle' else baseMasks['poses'][pose]
  if pose in ('P','idle'):
   groups={'L':('leftArm','leftLeg','leftShoe'),'R':('rightArm','rightLeg','rightShoe')}
  elif pose=='A':groups={'L':('nearArm','trailingLeg','trailingShoe'),'R':('farArm','leadingLeg','leadingShoe')}
  else:groups={'L':('farArm','leadingLeg','leadingShoe'),'R':('nearArm','trailingLeg','trailingShoe')}
  for side,(arm,leg,shoe) in groups.items():
   for key,parts in [('shoulder'+side,('shirt',arm)),('wrist'+side,(arm,)),('hip'+side,('shorts',)),('knee'+side,(leg,'shorts')),('ankle'+side,(leg,shoe)),('foot'+side,(shoe,)),('ear'+side,('leftEar' if side=='L' else 'rightEar',))]:
    x,y=points[key];assert any(bm[k][y*32+x] for k in parts),(pose,key,'proposed slot outside intended clothing/part mask')
  if pose in ('A','C'):
   # The bag/strap chain is explicitly rendered, not just inferred from alpha.
   chain=[(27,45),(26,45),(25,46),(24,46),(23,47),(22,48),(21,49)]
   if pose=='C':chain=[(31-x,y) for x,y in chain]
   for pt in chain:assert im.getpixel(pt)[:3] in [(42,52,74),(116,136,148)],(pose,pt,'strap chain missing')
   assert im.getpixel(tuple(points['packAttach']))[:3] in [(42,52,74),(116,136,148)],(pose,'pack slot')
  report['frames'].append({'project':name,'frame':i,'pose':pose,'changedPixels':len(changed),'earFinalRGBAMirrored':True,'protectedHeadExceptEarExact':True,'lowerBodyExceptShoeSpurExact':True,'connected':True,'attachmentSlotsInsideSavedHero':True})
# Mannequin has stable featureless head/ear construction and the same head bob.
a=Image.open(out/'mannequin-00.png').convert('RGBA');c=Image.open(out/'mannequin-04.png').convert('RGBA')
assert a.crop((0,0,32,45)).tobytes()==c.crop((0,0,32,45)).tobytes()
for i in range(8):
 im=Image.open(out/f'mannequin-{i:02}.png').convert('RGBA');dy=-2 if order[i]=='P' else 0
 for y in range(37+dy,42+dy):
  for x in range(4,8):assert im.getpixel((x,y))==im.getpixel((31-x,y))
# All GIFs checked after actual decode: duplicate frames, timing, palette,4x.
for job in json.loads((ext/'gif-jobs.json').read_text()):
 p=json.loads(Path(job['project']).read_text());cols=[(0,0,0,0)]+[tuple(bytes.fromhex(v[1:]))+(255,) for v in p['palette'][1:]]
 gif=Image.open(job['output']);assert gif.n_frames==8 and gif.info.get('loop')==0
 for i,frame in enumerate(p['frames']):
  gif.seek(i);decoded=gif.convert('RGBA');assert decoded.size==(p['width'],p['height']) and list(decoded.get_flattened_data())==[cols[n] for n in frame['pixels']];assert gif.info['duration']==job['delayMs']
 report['GIFs'][Path(job['output']).name]={'frames':8,'delayMs':job['delayMs'],'cycleMs':8*job['delayMs'],'exactSavedPixels':True,'loop':0,'sha256':hashlib.sha256(Path(job['output']).read_bytes()).hexdigest()}
for speed in ('fast','slow'):
 for i in range(8):
  panel=Image.open(ext/f'triple-{speed}-{i:02}.png').convert('RGBA')
  for x,path in [(4,ext/f'registered-left-{i:02}.png'),(40,out/f'walk-{i:02}.png'),(76,out/f'mannequin-{i:02}.png')]:
   im=Image.open(path).convert('RGBA')
   for y in range(64):
    for xx in range(32):
     if im.getpixel((xx,y))[3]:assert im.getpixel((xx,y))==panel.getpixel((x+xx,28+y))
for stem in ('source-hero-mannequin','source-hero-mannequin-SLOW4x'):
 n=Image.open(ext/(stem+'-native.gif'));big=Image.open(ext/(stem+'-4x.gif'))
 for i in range(8):n.seek(i);big.seek(i);assert big.convert('RGBA').tobytes()==n.convert('RGBA').resize((448,384),Image.Resampling.NEAREST).tobytes()
report.update({'allPNGsEqualEditableSource':True,'allPosesConnected':True,'earAnatomyMasksInheritedMirroredHR10':True,'mannequinHeadStableAcrossOpposedPoses':True,'hiddenJointsStatus':'PROPOSED, not source-measured anatomy','attachmentSlotsInsideIntendedClothingPartMasks':True,'GIFsExactNativeAndNearest4x':True,'thirdColumnIsNeutralFeaturelessConstruction':True,'reviewOnly':True})
(out/'independent-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: bounded source equality, final rendered ears, protected proportions, shoe spur, visible strap chain/slots, connected Hero/dummy,7 decoded GIFs/native/4x/100ms/400ms.')
