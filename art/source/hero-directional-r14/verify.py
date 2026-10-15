"""Independent final saved-pixel checks (never the art approval gate)."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib,subprocess
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR14';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
meta=json.loads((src/'construction.json').read_text());dirs=('south','north','west','east');order=meta['order'];r={'task':'M1.HR14','visualApproval':False,'lowerRowsCompared':[54,64],'frames':{},'GIFs':{},'limits':['Hidden knee/leg bone anatomy inferred and occluded; no visible calf invented','No emulator observation; ROM source-derived8engine-tick phases','ROM GIF centisecond quantization:540ms vs source-derived535.77ms loop','Combined PHASE board uses100ms matched phase slots, not stock engine playback','Head/hair and upper body remain original Critz design, not a full source silhouette match']}
# Do not use authoring LOWER or its semantic data to derive expected boundaries.
def refclass(px,d,y):
 a,b,c,alpha=px
 if not alpha:return '.'
 if a==b==c==0:return 'dark'
 if a<30:return 'dark'
 if b>180 and a<160:return 'warmGray'
 if b>120 and a<100:return 'slateLight'
 if a>240 and b>230:return 'sole'
 if a>180 and b<120:return 'coral'
 return 'slateShadow'
colors={'dark':{(36,35,48),(42,52,74)},'warmGray':{(191,192,170)},'slateLight':{(116,136,148)},'sole':{(249,237,200)},'coral':{(174,69,74)},'slateShadow':{(70,86,113)}}
oldmeta=json.loads((root/'art/source/hero-directional-r13/projection-and-joints.json').read_text());eyes=json.loads((root/'art/source/hero-redesign-r6/masks.json').read_text())
def connected(im):
 p={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]};seen={next(iter(p))};q=list(seen)
 while q:
  x,y=q.pop()
  for a in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if a in p and a not in seen:seen.add(a);q.append(a)
 assert p==seen,('disconnected',sorted(p-seen))
def rgba(p,f):
 cols=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in p['palette'][1:]];im=Image.new('RGBA',(p['width'],p['height']));im.putdata([cols[n] for n in f['pixels']]);return im
for d in dirs:
 for p in ('idle','A','P','C'):
  h=Image.open(out/f'hero-{d}-{p}.png').convert('RGBA');m=Image.open(out/f'dummy-{d}-{p}.png').convert('RGBA');dy=-2 if p=='P' else 0
  for kind,im in [('hero',h),('dummy',m)]:
   assert im.size==(32,64) and set(px[3] for px in im.get_flattened_data())=={0,255}
   try:connected(im)
   except AssertionError as error:raise AssertionError((d,p,kind,str(error)))
  assert len({px for px in h.get_flattened_data() if px[3]})<=15
  old=Image.open(root/f'docs/reviews/M1-HR13/hero-{d}-{p}.png').convert('RGBA');e=oldmeta['directions'][d][p]
  for i,on in enumerate(e['headMaskHero']):
   if on:assert h.getpixel((i%32,i//32))==old.getpixel((i%32,i//32)),(d,p,'identity head changed')
  for i,on in enumerate(e['neckMaskHero']):
   if on:assert e['headMaskHero'][i]
  for i,on in enumerate(e['neckMaskDummy']):
   if on:assert e['headMaskDummy'][i]
  eyeCount=0
  for i,on in enumerate(eyes[d].get('eyes',[0]*2048)):
   x,y=i%32,i//32+dy
   if on and e['headMaskDummy'][y*32+x]:assert m.getpixel((x,y))[:3]==(37,51,64);eyeCount+=1
  if d!='north':assert eyeCount>0
  handCount=sum(px[:3]==(255,212,161) for px in m.get_flattened_data());assert handCount>0,(d,p,'dummy no hands')
  alphaDiff=[];materialDiff=[];classMasks={k:[] for k in colors}
  if p!='idle':
   ref=Image.open(ext/f'reference-{d}-{p}.png').convert('RGBA')
   for y in range(54,64):
    for x in range(32):
     sp=ref.getpixel((x,y));hp=h.getpixel((x,y));mp=m.getpixel((x,y));cl=refclass(sp,d,y)
     if bool(sp[3])!=bool(hp[3]) or bool(sp[3])!=bool(mp[3]):alphaDiff.append([x,y])
     if cl!='.':
      classMasks[cl].append([x,y])
      if hp[:3] not in colors[cl]:materialDiff.append([x,y,cl,hp])
   assert not alphaDiff and not materialDiff,(d,p,'lower alpha/material mismatch',alphaDiff[:6],materialDiff[:6])
   # Material class masks/diff proof contains only diagram colors, no sourceRGB.
   diagram=Image.new('RGB',(32,10),'#9dbac8');dd=ImageDraw.Draw(diagram);cs={'dark':'#253340','warmGray':'#d2a6df','slateLight':'#65a6de','sole':'#f1d171','coral':'#ed745c','slateShadow':'#9b83d4'}
   for cl,pts in classMasks.items():
    for x,y in pts:dd.point((x,y-54),fill=cs[cl])
   diagram.resize((256,80),Image.Resampling.NEAREST).save(out/f'material-boundary-{d}-{p}.png')
  r['frames'][d+'/'+p]={'connected':True,'heroColors':len({px for px in h.get_flattened_data() if px[3]}),'dummyVisibleEyeCells':eyeCount,'dummyHandPixels':handCount,'headExactHR13':True,'neckOccluded':True,'lowerAlphaMismatch':len(alphaDiff),'lowerMaterialMismatch':len(materialDiff),'referenceClasses':{k:len(v) for k,v in classMasks.items()},'paintedBottom':h.getbbox()[3]-1}
for kind in ('hero','dummy'):
 p=json.loads((src/f'{kind}-idles.sprite.json').read_text());assert len(p['frames'])==4
 for d,f in zip(dirs,p['frames']):assert rgba(p,f).tobytes()==Image.open(out/f'{kind}-{d}-idle.png').convert('RGBA').tobytes()
 for d in dirs:
  p=json.loads((src/f'{kind}-{d}-walk.sprite.json').read_text());assert len(p['frames'])==8
  for po,f in zip(order,p['frames']):assert rgba(p,f).tobytes()==Image.open(out/f'{kind}-{d}-{po}.png').convert('RGBA').tobytes()
# Decode all8 frames, realdelayarrays, loop0, native/enlarged pixels.
for job in json.loads((ext/'gif-jobs.json').read_text()):
 p=json.loads(Path(job['project']).read_text());g=Image.open(job['output']);assert g.n_frames==8 and g.info['loop']==0;ds=[]
 for i,f in enumerate(p['frames']):
  im=rgba(p,f);scale=job.get('deriveNearestScale',1)
  if scale!=1:im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
  g.seek(i);assert g.convert('RGBA').tobytes()==im.tobytes(),(job['output'],i,'GIF pixels');assert g.info['duration']==job['delaysMs'][i];ds.append(g.info['duration'])
 r['GIFs'][Path(job['output']).name]={'frames':8,'delaysMs':ds,'cycleMs':sum(ds),'loop':0,'size':g.size,'exactPixels':True,'sha256':hashlib.sha256(Path(job['output']).read_bytes()).hexdigest()}
for d in dirs:
 for suffix in ('','-SLOW4x'):
  a=Image.open(ext/f'source-hero-template-{d}{suffix}-native.gif');b=Image.open(ext/f'source-hero-template-{d}{suffix}-4x.gif')
  for i in range(8):a.seek(i);b.seek(i);assert a.convert('RGBA').resize((448,384),Image.Resampling.NEAREST).tobytes()==b.convert('RGBA').tobytes()
 # Actual normal and slow panels retain spritepixels despite titlelabels.
 a=Image.open(ext/f'source-hero-template-{d}-native.gif');b=Image.open(ext/f'source-hero-template-{d}-SLOW4x-native.gif')
 for i in range(8):a.seek(i);b.seek(i);assert a.convert('RGBA').crop((0,12,112,96)).tobytes()==b.convert('RGBA').crop((0,12,112,96)).tobytes()
features=json.loads((out/'common-feature-registration.json').read_text())
for d in dirs:
 for po in ('idle','A','P','C'):
  record=features['directions'][d][po];e=meta['directions'][d][po]['commonFeatureRegistration']
  assert set(e)=={'head','ears','eyes','arms','hands','torso','feet','legs','hiddenAttachments'}
  assert all(v['xy'] is None for v in e['hiddenAttachments'].values())
  assert e['feet']['edgeAnchor']==[16,64]
  assert e['legs']['anatomicalCoordinates'] is None and 'Occluded/inferred' in e['legs']['status']
  hero=Image.open(out/f'hero-{d}-{po}.png').convert('RGBA');dummy=Image.open(out/f'dummy-{d}-{po}.png').convert('RGBA');info=meta['directions'][d][po]
  actualDummyHands={(x,y) for y in range(64) for x in range(32) if dummy.getpixel((x,y))[:3]==(255,212,161)}
  guideHands={tuple(pt) for pt in e['hands']['cells']};assert guideHands==actualDummyHands
  actualHeroHands={(x,y) for y in range(64) for x in range(32) if hero.getpixel((x,y))[3] and hero.getpixel((x,y))[:3] in [(166,104,69),(195,138,88),(116,69,57)] and not info['headMaskHero'][y*32+x] and not info['headMaskDummy'][y*32+x]}
  assert actualHeroHands==actualDummyHands,(d,po,'actual hand/guide mask mismatch')
  h=Image.open(out/f'hero-{d}-{po}.png').convert('RGBA');last=h.getbbox()[3]-1
  assert last==record['lastPaintedRow']==e['feet']['lastPaintedRow']
  expected={x for x in range(32) if h.getpixel((x,last))[3]};declared={x for a,b in record['lastPaintedSpans'] for x in range(a,b)};assert expected==declared
  for kind in ('hero','dummy'):
   im=Image.open(out/f'{kind}-{d}-{po}.png').convert('RGBA');assert hashlib.sha256(im.tobytes()).hexdigest()==record[kind+'PixelSHA256']
r['commonFeatureRegistration']={'records':16,'hiddenHipKneeAnkleFootAttachments':None,'observedLowestContourSpansChecked':True,'guideChangesNoSpritePixels':True,'actualHeroDummyAndGuideHandCellSetsExact':True}
interface=json.loads((out/'interface-checks.json').read_text());assert interface['allInterfaceChecksPass']
ref=Image.open(ext/'reference-south-P.png').convert('RGBA');h=Image.open(out/'hero-south-P.png').convert('RGBA')
for x in range(32):
 sp=ref.getpixel((x,53));hp=h.getpixel((x,53));assert bool(sp[3])==bool(hp[3])
 if sp[3]:assert hp[:3] in colors[refclass(sp,'south',53)]
r['upperInterfaceReview']={'report':'interface-checks.json','taper':interface['southPassingTaper'],'idleWalkContinuity':interface['idleWalkContinuity'],'headsAndLiteralLowerContactsProtected':True,'canonicalPackStrapsUnchanged':True,'upperMaterials':'Original palette adaptation, not full reference RGB/anatomy match','profileOriginalBagOverhang':'Explicit source-envelope differences in interface report'}
checks=json.loads((out/'first-checkpoint-checks.json').read_text());assert checks['allCheckpointChecksPass'];r['packChecks']=checks['packChecks'];r['allChecksPass']=True
(out/'independent-checks.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS:32 poses connected;12 unique loweralpha+material maps exact;head protected;dummyeyes/hands;16 rigid pack checks;10 editable sources equal;28 GIFs decode exactpixels/holds/nearest4x.')
