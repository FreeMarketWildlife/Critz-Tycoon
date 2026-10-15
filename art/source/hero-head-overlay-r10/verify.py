"""Independent saved-source/PNG/GIF/timing and head-identity checks for HR9."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib,ast
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR10-HEAD';ext=Path(sys.argv[1]).resolve();assert ext!=root and root not in ext.parents
walk=json.loads((src/'hero-forward-walk.sprite.json').read_text());idle=json.loads((src/'hero-forward-idle.sprite.json').read_text());mask=json.loads((src/'masks.json').read_text());obs=json.loads((root/'docs/reviews/M1-HR9/reference-observations.json').read_text());author=json.loads((out/'authoring-report.json').read_text())
assert walk['width']==idle['width']==32 and walk['height']==idle['height']==64 and len(walk['frames'])==8
rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in walk['palette'][1:]]
accepted=Image.open(out/'head-forward.png').convert('RGBA')
frames=[]
for i,f in enumerate(walk['frames']):
 im=Image.open(out/f'walk-{i:02}.png').convert('RGBA');frames.append(im);assert list(im.get_flattened_data())==[rgba[n] for n in f['pixels']]
 assert set(p[3] for p in im.get_flattened_data())=={0,255} and len({p for p in im.get_flattened_data() if p[3]})<=15
 pose=author['order'][i];dy=author['headTranslationFromNewRestHead'][pose]
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
report={'scope':'forward only, unapproved motion/art review','sourceFrameCount':8,'candidateFrameCount':8,'candidateUniquePoseCount':3,'allPNGsEqualEditableSource':True,'allWalkHeadsExactlyTranslatedNewRestHead':True,'idleHeadExactNewRestHead':True,'defaultMouthNoseEmpty':True,'visibleEyeBandsMatchConfirmedReference':True,'allCandidatePosesConnected':True,'originalPosePaletteLimit':15,'idleAnatomyPaired':True,'registration':obs['registration'],'gifs':{}}
def checkgif(path,expected):
 gif=Image.open(path);assert gif.n_frames==8 and gif.info.get('loop')==0,(path,gif.n_frames)
 durations=[]
 for i,im in enumerate(expected):
  gif.seek(i);decoded=gif.convert('RGBA');assert decoded.size==im.size
  assert list(decoded.get_flattened_data())==list(im.get_flattened_data()),(path,i,'GIF color/pixels changed')
  durations.append(gif.info['duration'])
 assert durations==[100]*8,(path,durations)
 report['gifs'][path.name]={'frames':8,'durationMs':durations,'loop':0,'exactSavedPixels':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
checkgif(out/'hero-forward-walk-native.gif',frames)
checkgif(out/'hero-forward-walk-4x.gif',[im.resize((128,256),Image.Resampling.NEAREST) for im in frames])
comp=[Image.open(ext/f'comparison-native-{i:02}.png').convert('RGBA') for i in range(8)]
checkgif(ext/'source-hero-native.gif',comp);checkgif(ext/'source-hero-4x.gif',[im.resize((352,328),Image.Resampling.NEAREST) for im in comp])
# Comparison crop RGB retains the source's actual decoded pixels on the common paper.
for i in range(8):
 ref=Image.open(ext/f'registered-left-{i:02}.png').convert('RGBA');paper=Image.new('RGBA',(32,64),'#eee6d0');paper.alpha_composite(ref);assert comp[i].crop((4,16,36,80)).tobytes()==paper.tobytes()
report['comparisonReferencePixelsExact']=True
report['timingCaveat']='GIFs exactly100ms/frame/800ms loop; editor6 ticks imply100.45623779296875ms. No gameplay timing integration.'
(out/'independent-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('registration','gifs')},indent=2));print('PASS four GIFs: eight exact100ms frames, exact palettes/pixels, no nearest4x drift.')

# Independently protect all lower-body and unchanged face/ear pixels.
oldMasks=json.loads((root/'art/source/hero-forward-r9/masks.json').read_text())
# Historical HR6 mask omitted line rasterization at sloped contour edges.
# Reconstruct its authored polygon plus outline, independently of new pixels.
tree=ast.parse((root/'art/source/hero-redesign-r6/build.py').read_text())
call=next(n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='shape' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value=='hair')
pts=ast.literal_eval(call.args[1]);oldHair=Image.new('1',(32,64));hd=ImageDraw.Draw(oldHair);hd.polygon(pts,fill=1);hd.line(pts+[pts[0]],fill=1)
for i,im in enumerate(frames):
 old=Image.open(root/f'docs/reviews/M1-HR9/walk-{i:02}.png').convert('RGBA')
 pose=author['order'][i];h=Image.new('1',(32,64));h.paste(oldHair,(0,author['headTranslationFromNewRestHead'][pose]));allowed=[bool(a or b) for a,b in zip(h.get_flattened_data(),mask['poses'][pose]['hair'])]
 assert im.crop((0,46,32,64)).tobytes()==old.crop((0,46,32,64)).tobytes()
 for j,v in enumerate(allowed):
  if not v:assert im.getpixel((j%32,j//32))==old.getpixel((j%32,j//32)),(i,j)
 for key in ('face','eyes','leftEar','rightEar','nose','mouth'):
  assert oldMasks['poses'][pose][key]==mask['poses'][pose][key],key
report['allChangesWithinOldOrNewHairMasks']=True
report['bodyAndFaceEarEyeMasksProtected']=True
(out/'independent-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS protected body, face, ears and eyes; changed pixels confined to old/new hair union.')
