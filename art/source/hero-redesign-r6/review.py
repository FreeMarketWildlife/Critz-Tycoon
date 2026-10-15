"""Stage1 HR6 original review plates, protected-art checks and external reference overlay."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib,sys
root=Path(__file__).resolve().parents[3];base=Path(__file__).parent;out=root/'docs/reviews/M1-HR6';old=root/'docs/reviews/M1-HR5';ext=Path(sys.argv[1]).resolve()
assert ext!=root and root not in ext.parents
refpath=ext/'walking.png';assert hashlib.sha256(refpath.read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
masks=json.loads((base/'masks.json').read_text());oldm=json.loads((root/'art/source/hero-redesign-r5/masks.json').read_text());src=json.loads((base/'hero-boy.sprite.json').read_text())
assert src['defaultFeatures']=={'mouth':None,'nose':None,'body':'normal'}
imgs={n:Image.open(out/f'hero-{n}.png').convert('RGBA') for n in masks}
prior={n:Image.open(old/f'hero-{n}.png').convert('RGBA') for n in masks}
report={'stage':1,'body':'normal','mouthDefault':None,'noseDefault':None,'canvas':[32,64],'anchor':[16,64],'directions':{},'scope':'Correct normal ears only; no body variants, swapping implementation, UI or runtime integration.'}
landmarks={'status':'PROPOSED stage1 review; not accepted/frozen anatomy','canvas':[32,64],'groundAnchor':[16,64],'coordinates':'half-open boxes in target pixels; top-left origin, Y down','starterOutfit':'Same original coral/cream shirt, blue shorts, slate daypack and dark sneakers in every future body type; current normal only','directions':{}}
def box(v):
 pts=[(i%32,i//32) for i,n in enumerate(v) if n]
 return [min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts)+1,max(y for x,y in pts)+1] if pts else None
for n,img in imgs.items():
 m=masks[n]
 assert img.crop((0,46,32,64)).tobytes()==prior[n].crop((0,46,32,64)).tobytes(),n+' outfit/body drift'
 assert m['hair']==oldm[n]['hair'],n+' hair geometry changed'
 assert all(img.getpixel((i%32,i//32))==prior[n].getpixel((i%32,i//32)) for i,v in enumerate(m['hair']) if v),n+' hair color changed'
 assert sum(m['mouth'])==0 and sum(m['nose'])==0
 earKeys=['leftEar','rightEar'] if n in ('south','north') else ['nearEar']
 ears={}
 for k in earKeys:
  visible=[int(v and not m['face'][i] and not m['hair'][i]) if n in ('south','north') else int(v and not m['hair'][i]) for i,v in enumerate(m[k])]
  ears[k]={'scaffoldBounds':box(m[k]),'scaffoldArea':sum(m[k]),'visibleBoundsAfterFaceHairOcclusion':box(visible),'visibleAreaAfterOcclusion':sum(visible)}
  assert sum(visible)>0,(n,k)
 if n in ('south','north'):
  assert all(m['leftEar'][y*32+x]==m['rightEar'][y*32+31-x] for y in range(64) for x in range(32))
  assert all(m['face'][y*32+x]==m['face'][y*32+31-x] for y in range(64) for x in range(32))
 # Center of lower face contains skin rows and full jaw contact only, no isolated mouth mark.
 if n=='south':
  assert all(len({img.getpixel((x,y)) for x in range(14,18)})==1 for y in range(40,45))
 report['directions'][n]={'ears':ears,'bodyBelow46ExactHR5':True,'hairMaskAndVisiblePixelsExactHR5':True,'emptyNoseMouthMasks':True,'pngSha256':hashlib.sha256((out/f'hero-{n}.png').read_bytes()).hexdigest()}
 bodykeys=[k for k in m if k in ('shirt','neck','shorts','leftFoot','rightFoot','nearFoot','farFoot','pack','nearArm','leftArm','rightArm','sleeve')]
 landmarks['directions'][n]={'headFaceScaffoldBounds':box(m['face']),'hairOcclusionBounds':box(m['hair']),'eyeBounds':box(m['eyes']) if 'eyes'in m else None,'earLandmarks':{k:box(m[k]) for k in earKeys},'noseSlotDefault':None,'mouthSlotDefault':None,'bodyLandmarks':{k:box(m[k]) for k in bodykeys},'occlusionOrder':['neck/body','ears','face for south/north','eyes and small profile ear','hair foreground']}
# Bounded head correction: prove every pixel outside approved ear/cheek regions exact.
allowed={'south':[2,36,30,46],'north':[2,36,30,46],'west':[17,38,22,43],'east':[10,38,15,43]}
for n,img in imgs.items():
 l,t,r,b=allowed[n];changes=[(x,y) for y in range(64) for x in range(32) if img.getpixel((x,y))!=prior[n].getpixel((x,y))]
 assert all(l<=x<r and t<=y<b for x,y in changes),n+' outside allowed region'
 report['directions'][n]['allowedChangedRegion']=allowed[n]
 report['directions'][n]['actualChangedPixels']=len(changes)
 report['directions'][n]['actualChangedBounds']=[min(x for x,y in changes),min(y for x,y in changes),max(x for x,y in changes)+1,max(y for x,y in changes)+1]
 report['directions'][n]['outsideAllowedRegionPixelExact']=True
for n,roi in [('west',(4,35,17,46)),('east',(15,35,28,46))]:
 assert imgs[n].crop(roi).tobytes()==prior[n].crop(roi).tobytes(),n+' added facial mark'
 report['directions'][n]['frontFaceNoseMouthAreaExactHR5']=True
report['southCenterFaceNoIsolatedLipOrNoseCluster']=True
(out/'ear-checks.json').write_text(json.dumps(report,indent=2)+'\n');(base/'normal-landmarks.proposed.json').write_text(json.dumps(landmarks,indent=2)+'\n')
# All four head/neck before and after, at matched native registration.
plate=Image.new('RGB',(900,550),'#eee6d0');d=ImageDraw.Draw(plate)
for i,n in enumerate(('south','north','west','east')):
 x=18+(i%2)*450;y=15+(i//2)*265;d.text((x,y),n.upper()+' | REJECTED HR5 / CORRECTED NORMAL HR6',fill='#292b34')
 for j,images in enumerate((prior,imgs)):
  crop=images[n].crop((0,30,32,48)).resize((192,108),Image.Resampling.NEAREST);plate.paste(crop,(x+215*j,y+28),crop)
  crop=images[n].crop((0,18,32,48)).resize((128,120),Image.Resampling.NEAREST);plate.paste(crop,(x+32+215*j,y+141),crop)
plate.save(out/'ears-head-before-after.png')
# Four-direction full-body old/new plus native on light and dark. Original art only.
p=Image.new('RGB',(900,420),'#eee6d0');pd=ImageDraw.Draw(p)
for i,n in enumerate(('south','north','west','east')):
 x=12+i*222;pd.text((x,12),n.upper()+' | HR5 / HR6 NORMAL',fill='#292b34')
 for j,images in enumerate((prior,imgs)):
  img=images[n];big=img.resize((96,192),Image.Resampling.NEAREST);p.paste(big,(x+108*j,35),big);p.paste(img,(x+32+108*j,260),img)
 pd.rectangle((x,330,x+205,410),fill='#263342')
 for j,images in enumerate((prior,imgs)):p.paste(images[n],(x+32+108*j,338),images[n])
p.save(out/'full-body-before-after.png')
# Countable front grid default plus compact feature/occlusion proof.
g=Image.new('RGB',(340,590),'#eee6d0');gd=ImageDraw.Draw(g);big=imgs['south'].resize((256,512),Image.Resampling.NEAREST);g.paste(big,(54,38),big)
for x in range(33):gd.line((54+x*8,38,54+x*8,550),fill='#b6b3aa')
for y in range(65):gd.line((54,38+y*8,310,38+y*8),fill='#b6b3aa')
for y in list(range(0,61,10))+[64]:
 yy=550-y*8;gd.line((54,yy,310,yy),fill='#757e77');gd.text((22,yy-4),str(y),fill='#292b34')
gd.line((182,38,182,550),fill='#c35151',width=2);gd.text((55,12),'HR6 NORMAL | 8x | one cell = one pixel',fill='#292b34');gd.text((55,566),'No mouth | X16 center | Y upward',fill='#292b34');g.save(out/'normal-front-grid.png')
# Stable full-head/neck plate, native plus clean3x for every direction.
headplate=Image.new('RGB',(900,235),'#eee6d0');hd=ImageDraw.Draw(headplate)
for i,n in enumerate(('south','north','west','east')):
 x=12+i*222;hd.text((x,10),n.upper()+' | HR5 / NORMAL HR6',fill='#292b34')
 for j,images in enumerate((prior,imgs)):
  crop=images[n].crop((0,18,32,48));headplate.paste(crop,(x+32+108*j,38),crop)
  big=crop.resize((96,90),Image.Resampling.NEAREST);headplate.paste(big,(x+108*j,95),big)
hd.text((12,211),'Native full head/neck above | clean3x below | same canvas registration',fill='#292b34');headplate.save(out/'head-neck-native-3x.png')
# Literal external reference overlay and full body. No overlay score used as acceptance.
sheet=Image.open(refpath);r=sheet.convert('RGBA');a=Image.new('L',sheet.size);a.putdata([255 if v else 0 for v in sheet.get_flattened_data()]);r.putalpha(a)
p=Image.new('RGB',(1000,680),'#eee6d0');pd=ImageDraw.Draw(p)
for i,(n,f) in enumerate([('south',0),('north',1),('west',2),('east',2)]):
 x=15+(i%2)*500;y=15+(i//2)*330;pd.text((x,y),n.upper()+' | REFERENCE2X / NORMAL1X / ACTUAL50% OVERLAY',fill='#292b34')
 ref=r.crop((16*f,0,16*f+16,32)).resize((32,64),Image.Resampling.NEAREST)
 if n=='east':ref=ref.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 h=imgs[n];t=h.copy();t.putalpha(t.getchannel('A').point(lambda v:round(v*.5)));overlay=Image.alpha_composite(ref,t)
 for j,img in enumerate((ref,h,overlay)):
  large=img.resize((128,256),Image.Resampling.NEAREST);p.paste(large,(x+j*155,y+28),large)
 pd.text((x,y+296),'Full frames / same anchor. Headwear is not bare anatomy.',fill='#292b34')
p.save(ext/'normal-reference-overlay.png')
print(json.dumps(report,indent=2))
