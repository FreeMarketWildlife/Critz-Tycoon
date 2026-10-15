"""Saved-pixel, source/pose, occlusion, intended part-slot and GIF checks."""
from pathlib import Path
from PIL import Image
import json,sys,hashlib,subprocess
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR13';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
meta=json.loads((src/'projection-and-joints.json').read_text());fits=json.loads((src/'clothing-part-masks.json').read_text())['directions'];oldsc=json.loads((root/'art/source/hero-forward-r12/scaffold.json').read_text());directions=('south','north','west','east');order=meta['walkOrder']
report={'task':'M1.HR13','status':'UNAPPROVED visual review; technical checks do not accept art','frames':[],'GIFs':{},'profileCleanup':{},'referenceFacts':{},'limitations':['No emulator or continuous-frame gameplay capture','Numeric camera angle/world skeleton remains unresolved','Side heads/bodies and hidden joints are original construction proposals','Critz100ms preview cadence differs from pinned ROM8-engine-tick phase holds','ROM strides end63 while inherited Critz contacts end61; sharedframe anchor does not equate painted feet']}
def coords(bits):return {(i%32,i//32) for i,v in enumerate(bits) if v}
def connected(im):
 p={(i%32,i//32) for i,px in enumerate(im.get_flattened_data()) if px[3]};seen={next(iter(p))};q=list(seen)
 while q:
  x,y=q.pop()
  for a in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if a in p and a not in seen:seen.add(a);q.append(a)
 assert p==seen,('disconnected',p-seen)
def alpha(im):return im.getchannel('A').tobytes()
def rgba_project(p,frame):
 cols=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in p['palette'][1:]];im=Image.new('RGBA',(p['width'],p['height']));im.putdata([cols[n] for n in frame['pixels']]);return im
def load(kind,d,p):return Image.open(out/f'{kind}-{d}-{p}.png').convert('RGBA')
# Pin the liked base; this task does not consume the parked HR11 draft.
for n in ('hero-forward-idle.sprite.json','hero-forward-walk.sprite.json'):
 path='art/source/hero-forward-r12/'+n;assert subprocess.check_output(['git','show','3b947e8:'+path],cwd=root)==(root/path).read_bytes()
oldHead=Image.open(root/'docs/reviews/M1-HR6/hero-south.png').convert('RGBA').crop((0,0,32,46))
for d in directions:
 for p in ('idle','A','P','C'):
  h=load('hero',d,p);m=load('dummy',d,p);e=meta['directions'][d][p];j=e['joints'];fm=fits[d][p];hd=-2 if p=='P' else 0
  for im in (h,m):assert im.size==(32,64) and set(px[3] for px in im.get_flattened_data())=={0,255};connected(im)
  assert len({px for px in h.get_flattened_data() if px[3]})<=15
  for kind in ('Hero','Dummy'):
   hm=coords(e['headMask'+kind]);tm=coords(e['torsoMask'+kind]);nm=coords(e['neckMask'+kind]);assert nm<=hm
   assert len(hm&tm)>20 and tuple(e['hiddenNeckSite']) in hm
   assert e['neckVisibleCells'+kind]==0
  assert h.getbbox()[3]==m.getbbox()[3]==(60 if p=='P' else 62),(d,p,'foot bottom')
  # Stronger than a shared anchor: proposed limb sites stay in their intended
  # saved clothing masks AND on the actual saved figure.
  for side in ('L','R'):
   for key,parts in [('shoulder'+side,('torso','arm'+side)),('wrist'+side,('arm'+side,)),('hip'+side,('hips',)),('knee'+side,('leg'+side,'hips')),('ankle'+side,('leg'+side,'foot'+side)),('foot'+side,('foot'+side,))]:
    x,y=j[key];assert h.getpixel((x,y))[3],(d,p,key,'outside rendered Hero');assert any(fm[k][y*32+x] for k in parts),(d,p,key,'outside intended clothing mask')
  if d=='south':
   assert j==oldsc['poses'][p],(p,'front joint moved')
   path='idle-forward.png' if p=='idle' else f'walk-{dict(A=0,P=2,C=4)[p]:02}.png';old=Image.open(root/'docs/reviews/M1-HR12'/path).convert('RGBA')
   assert alpha(old)==alpha(h),'front silhouette changed'
   for y in range(46):
    for x in range(32):
     if oldHead.getpixel((x,y))[3]:assert h.getpixel((x,y+hd))==old.getpixel((x,y+hd)),(p,x,y,'liked head changed')
   # No cyan column survives below the template head; no exposed neck skin
   # survives at the old Hero collar pocket below the projected head.
   for y in (46+hd,47+hd,48+hd):assert m.getpixel((16,y))[:3]==(74,194,176),(p,y,'cyan neck column')
   skin={(166,104,69),(195,138,88),(116,69,57)}
   for y in (46+hd,47+hd):
    for x in range(15,19):assert h.getpixel((x,y))[:3] not in skin,(p,x,y,'old visible neck skin')
   for yy in range(37+hd,42+hd):
    for xx in range(4,7):assert h.getpixel((xx,yy))==h.getpixel((31-xx,yy))
   for y in range(51,64):
    for x in range(32):assert h.getpixel((x,y))==old.getpixel((x,y)),(p,x,y,'liked compact lower body moved')
  if d in ('west','east'):
   before=Image.open(ext/f'before-cleanup-hero-{d}-{p}.png').convert('RGBA')
   assert alpha(before)==alpha(h),(d,p,'bounded cleanup changed silhouette')
   changed=[(x,y) for y in range(64) for x in range(32) if before.getpixel((x,y))!=h.getpixel((x,y))]
   assert all(50<=y<=61 for x,y in changed),(d,p,'cleanup escaped lower leg')
   report['profileCleanup'][d+'/'+p]={'changedCells':len(changed),'allAlphaAndExtentUnchanged':True,'jointsRetained':True,'region':'lower garment overlaps shoe top; no silhouette/size change'}
   # Only one visible magenta ear group in profiles, no fake far ear dot.
   pink={(x,y) for y in range(64) for x in range(32) if m.getpixel((x,y))[:3]==(237,140,205)}
   assert pink and len({x for x,y in pink})<=2
  report['frames'].append({'direction':d,'pose':p,'heroBounds':h.getbbox(),'dummyBounds':m.getbbox(),'paintedFootBottom':h.getbbox()[3]-1,'hiddenNeckSite':j['neck'],'headCoversNeck':True,'headOverlapsTorso':True,'intendedClothingSlotMembership':True,'connected':True,'canvas':[32,64],'groundAnchor':[16,64]})
# Saved editable sources equal exact native PNGs, including all duplicate holds.
for kind in ('hero','dummy'):
 p=json.loads((src/f'{kind}-idles.sprite.json').read_text());assert len(p['frames'])==4
 for d,f in zip(directions,p['frames']):assert rgba_project(p,f).tobytes()==load(kind,d,'idle').tobytes()
 for d in directions:
  p=json.loads((src/f'{kind}-{d}-walk.sprite.json').read_text());assert len(p['frames'])==8
  for phase,f in zip(order,p['frames']):assert rgba_project(p,f).tobytes()==load(kind,d,phase).tobytes()
# Decode each GIF independently, including export-only896x768 combined panels.
for job in json.loads((ext/'gif-jobs.json').read_text()):
 p=json.loads(Path(job['project']).read_text());gif=Image.open(job['output']);assert gif.n_frames==8 and gif.info.get('loop')==0
 scale=job.get('deriveNearestScale',1);dur=[]
 for i,f in enumerate(p['frames']):
  expected=rgba_project(p,f)
  if scale!=1:expected=expected.resize((expected.width*scale,expected.height*scale),Image.Resampling.NEAREST)
  gif.seek(i);assert gif.convert('RGBA').tobytes()==expected.tobytes(),(job['output'],i,'GIF pixel drift');assert gif.info['duration']==job['delayMs'];dur.append(gif.info['duration'])
 report['GIFs'][Path(job['output']).name]={'frames':8,'durationsMs':dur,'cycleMs':sum(dur),'loop':0,'exactPixels':True,'size':gif.size,'nativeProjectValidated':True,'deriveNearestScale':scale,'sha256':hashlib.sha256(Path(job['output']).read_bytes()).hexdigest()}
for d in directions:
 for speed in ('fast','slow'):
  for i,p in enumerate(order):
   panel=Image.open(ext/f'panel-{d}-{speed}-{i:02}.png').convert('RGBA')
   for x,im in [(4,Image.open(ext/f'reference-{d}-{i:02}.png').convert('RGBA')),(40,load('hero',d,p)),(76,load('dummy',d,p))]:
    for y in range(64):
     for xx in range(32):
      if im.getpixel((xx,y))[3]:assert panel.getpixel((x+xx,28+y))==im.getpixel((xx,y))
 for suffix in ('','-SLOW4x'):
  small=Image.open(ext/f'source-hero-template-{d}{suffix}-native.gif');large=Image.open(ext/f'source-hero-template-{d}{suffix}-4x.gif')
  for i in range(8):small.seek(i);large.seek(i);assert large.convert('RGBA').tobytes()==small.convert('RGBA').resize((448,384),Image.Resampling.NEAREST).tobytes()
for suffix in ('','-SLOW4x'):
 small=Image.open(ext/f'four-direction-source-hero-template{suffix}-native.gif');large=Image.open(ext/f'four-direction-source-hero-template{suffix}-4x.gif')
 for i in range(8):small.seek(i);large.seek(i);assert large.convert('RGBA').tobytes()==small.convert('RGBA').resize((896,768),Image.Resampling.NEAREST).tobytes()
obs=json.loads((out/'reference-observations.json').read_text());assert obs['PNGsha256']=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1';assert obs['engineWalkTables']['east']['hFlip']
assert obs['engineWalkTables']['south']['frames']==[3,0,4,0] and obs['engineWalkTables']['north']['frames']==[5,1,6,1] and obs['engineWalkTables']['west']['frames']==[7,2,8,2]
report['referenceFacts']={'sourcePNGAndTablePinned':True,'sourceIndex0TransparencyUsed':True,'ROMWalkHoldsTicks':[8]*4,'customGIFFacts':'8x100ms, front only','previewProposal':'All Critz directional proofs8x100ms; referenceROMpose images synchronized at this review clock, not engine cadence','nativeReferenceRowsUntouched':True}
report['allChecksPass']=True;report['cameraAngle']='UNRESOLVED, no numeric pitch claimed';report['worldBoneCoordinates']='UNRESOLVED; only proposed2D projected guides supplied'
(out/'independent-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS:32native frames,10editable projects,28decoded8frameGIFs,exact4x including896x768,head/neck/torso occlusion,intended part slots,front joints/head/lowerbody protected,profilecleanup alpha/extent unchanged.')
