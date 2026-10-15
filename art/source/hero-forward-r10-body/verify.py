"""Independent saved-source/PNG/GIF/timing and head-identity checks for HR9."""
from pathlib import Path
from PIL import Image
import json,sys,hashlib,subprocess
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR10-BODY';ext=Path(sys.argv[1]).resolve();assert ext!=root and root not in ext.parents
walk=json.loads((src/'hero-forward-walk.sprite.json').read_text());idle=json.loads((src/'hero-forward-idle.sprite.json').read_text());mask=json.loads((src/'masks.json').read_text());obs=json.loads((root/'docs/reviews/M1-HR9/reference-observations.json').read_text());author=json.loads((out/'authoring-report.json').read_text())
assert walk['width']==idle['width']==32 and walk['height']==idle['height']==64 and len(walk['frames'])==8
rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in walk['palette'][1:]]
accepted=Image.open(root/'docs/reviews/M1-HR6/hero-south.png').convert('RGBA')
frames=[]
for i,f in enumerate(walk['frames']):
 im=Image.open(out/f'walk-{i:02}.png').convert('RGBA');frames.append(im);assert list(im.get_flattened_data())==[rgba[n] for n in f['pixels']]
 assert set(p[3] for p in im.get_flattened_data())=={0,255} and len({p for p in im.get_flattened_data() if p[3]})<=15
 pose=author['order'][i];dy=author['headWholeTranslationFromHR6'][pose]
 for y in range(46):
  for x in range(32):
   px=accepted.getpixel((x,y))
   if px[3]:assert 0<=y+dy<64 and im.getpixel((x,y+dy))==px,(i,x,y,'head pixel changed')
 assert not sum(mask['poses'][pose]['mouth']) and not sum(mask['poses'][pose]['nose'])
 # One connected actor, including the partially occluded rear leg.
 pts={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]};seen={next(iter(pts))};todo=list(seen)
 while todo:
  x,y=todo.pop()
  for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if q in pts and q not in seen:seen.add(q);todo.append(q)
 assert seen==pts,i
 # Visible front eyes remain at source-observed band after chosen fixed registration.
 eyemask=mask['poses'][pose]['eyes'];eyes=[(j%32,j//32) for j,v in enumerate(eyemask) if v]
 bbox=[min(x for x,y in eyes),min(y for x,y in eyes),max(x for x,y in eyes)+1,max(y for x,y in eyes)+1]
 assert bbox==obs['frames'][i]['eyeBounds']
 assert sorted(eyes)==sorted(tuple(q) for q in obs['frames'][i]['eyeCoordinates'])
assert frames[0].tobytes()==frames[1].tobytes() and frames[2].tobytes()==frames[3].tobytes()==frames[6].tobytes()==frames[7].tobytes() and frames[4].tobytes()==frames[5].tobytes()
assert len({im.tobytes() for im in frames})==3
idleIm=Image.open(out/'idle-forward.png').convert('RGBA');assert list(idleIm.get_flattened_data())==[rgba[n] for n in idle['frames'][0]['pixels']]
assert idleIm.crop((0,0,32,46)).tobytes()==accepted.crop((0,0,32,46)).tobytes()
# Default idle passing anatomy pairs, no forced RGB mirror of lighting/hair.
pm=mask['idle']
for a,b in [('leftArm','rightArm'),('leftLeg','rightLeg'),('leftShoe','rightShoe')]:assert all(pm[a][y*32+x]==pm[b][y*32+31-x] for y in range(64) for x in range(32)),(a,b)
report={'scope':'forward only, unapproved motion/art review','sourceFrameCount':8,'candidateFrameCount':8,'candidateUniquePoseCount':3,'allPNGsEqualEditableSource':True,'allWalkHeadsExactlyTranslatedHR6':True,'idleHeadExactHR6':True,'defaultMouthNoseEmpty':True,'visibleEyeBandsMatchConfirmedReference':True,'allCandidatePosesConnected':True,'originalPosePaletteLimit':15,'idleAnatomyPaired':True,'registration':obs['registration'],'gifs':{}}
def checkgif(path,expected,delay=100):
 gif=Image.open(path);assert gif.n_frames==8 and gif.info.get('loop')==0,(path,gif.n_frames)
 durations=[]
 for i,im in enumerate(expected):
  gif.seek(i);decoded=gif.convert('RGBA');assert decoded.size==im.size
  assert list(decoded.get_flattened_data())==list(im.get_flattened_data()),(path,i,'GIF color/pixels changed')
  durations.append(gif.info['duration'])
 assert durations==[delay]*8,(path,durations)
 report['gifs'][path.name]={'frames':8,'durationMs':durations,'loop':0,'exactSavedPixels':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
checkgif(out/'hero-forward-walk-native.gif',frames)
checkgif(out/'hero-forward-walk-4x.gif',[im.resize((128,256),Image.Resampling.NEAREST) for im in frames])
comp=[Image.open(ext/f'comparison-native-{i:02}.png').convert('RGBA') for i in range(8)]
checkgif(ext/'source-hero-native.gif',comp);checkgif(ext/'source-hero-4x.gif',[im.resize((352,328),Image.Resampling.NEAREST) for im in comp])
# Comparison crop RGB retains the source's actual decoded pixels on the common paper.
for i in range(8):
 ref=Image.open(ext/f'registered-left-{i:02}.png').convert('RGBA');paper=Image.new('RGBA',(32,64),'#eee6d0');paper.alpha_composite(ref);assert comp[i].crop((4,16,36,80)).tobytes()==paper.tobytes()
report['comparisonReferencePixelsExact']=True
slow=[Image.open(ext/f'slow-native-{i:02}.png').convert('RGBA') for i in range(8)]
lightdark=[Image.open(ext/f'light-dark-native-{i:02}.png').convert('RGBA') for i in range(8)]
checkgif(ext/'source-hero-SLOW4x-native.gif',slow,400)
checkgif(ext/'source-hero-SLOW4x-4x.gif',[im.resize((448,400),Image.Resampling.NEAREST) for im in slow],400)
checkgif(out/'hero-light-dark-native.gif',lightdark)
for i,im in enumerate(frames):
 for panel,x,y in [(slow[i],64,32),(lightdark[i],8,32),(lightdark[i],72,32)]:
  for yy in range(64):
   for xx in range(32):
    px=im.getpixel((xx,yy))
    if px[3]:assert panel.getpixel((x+xx,y+yy))==px
# Baseline is HR9, never the separate unapproved head detour.
baselineCommit='9d1d1595329004829082ebe6fd44ea33208a3e06'
for path in ['art/source/hero-forward-r9/hero-forward-walk.sprite.json','art/source/hero-forward-r9/hero-forward-idle.sprite.json']:
 assert subprocess.check_output(['git','show',baselineCommit+':'+path],cwd=root)==(root/path).read_bytes()
baseMask=json.loads((root/'art/source/hero-forward-r9/masks.json').read_text())
for pose in ('A','P','C'):
 for k in ('hair','face','eyes','leftEar','rightEar','jawContact','mouth','nose'):
  assert baseMask['poses'][pose][k]==mask['poses'][pose][k]
for k in ('hair','face','eyes','leftEar','rightEar','jawContact','mouth','nose'):assert baseMask['idle'][k]==mask['idle'][k]
report['HR9BaselineCommitVerified']=baselineCommit
report['allHeadEarFaceEyeMasksExactlyHR9']=True
report['slowLoopMs']=3200;report['sourceSpeedLoopMs']=800
report['slowPixelsExactlySourceSpeedPixels']=True
report['nativeLightDarkSpritePixelsExact']=True
original=ext.parent/'brendan-user-reference-original/01agijgmbz561.gif'
assert hashlib.sha256(original.read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e'
gif=Image.open(original)
for i in range(8):
 gif.seek(i);logical=gif.convert('RGBA').crop((0,0,128,192)).resize((32,48),Image.Resampling.NEAREST)
 fixed=Image.new('RGBA',(32,64));fixed.paste(logical,(0,14))
 assert fixed.tobytes()==Image.open(ext/f'registered-left-{i:02}.png').convert('RGBA').tobytes()
report['referenceRecheckedAgainstOriginalGIF']=True
report['shoeMaskAreaBeforeAfter']={}
for pose,keys in [('P',('leftShoe','rightShoe')),('A',('leadingShoe','trailingShoe')),('C',('leadingShoe','trailingShoe'))]:
 for k in keys:
  before=baseMask['poses'][pose][k];after=mask['poses'][pose][k]
  assert sum(after)<=sum(before),(pose,k,'shoe area increased')
  report['shoeMaskAreaBeforeAfter'][pose+'/'+k]=[sum(before),sum(after)]
report['timingCaveat']='GIFs exactly100ms/frame/800ms loop; editor6 ticks imply100.45623779296875ms. No gameplay timing integration.'
(out/'independent-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('registration','gifs')},indent=2));print('PASS seven GIFs: exact8-frame pixels,100ms source-speed/400ms labelled slow, native/nearest4x; HR9 head exact, shoe mask areas not increased.')
