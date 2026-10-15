"""Original four-direction projection layers. Reference rasters are not inputs."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,copy
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR13'
base=root/'docs/reviews/M1-HR12';oldsc=json.loads((root/'art/source/hero-forward-r12/scaffold.json').read_text())
palette=json.loads((root/'art/source/hero-forward-r12/hero-forward-walk.sprite.json').read_text())['palette']
rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in palette[1:]]
P={'O':'#242330','h':'#322a31','m':'#4c3739','l':'#705044','s':'#a66845','S':'#c38a58','d':'#744539','r':'#ed745c','R':'#ffad7a','v':'#ae454a','c':'#f9edc8','C':'#bfc0aa','b':'#465671','B':'#748894','n':'#2a344a'}
order=['A','A','P','P','C','C','P','P'];directions=('south','north','west','east');heroes={d:{} for d in directions};dummies={d:{} for d in directions};data={d:{} for d in directions}
baseBodyMasks=json.loads((root/'art/source/hero-forward-r12/masks.json').read_text());fitMasks={d:{} for d in directions}
def blank():return Image.new('RGBA',(32,64))
def shift(im,dy):
 q=Image.new(im.mode,(32,64));q.paste(im,(0,dy));return q
def mask(im):return im.getchannel('A').point(lambda a:255 if a else 0)
def poly(pts,col,edge=None):
 im=blank();d=ImageDraw.Draw(im);d.polygon(pts,fill=col)
 if edge:d.line(pts+[pts[0]],fill=edge)
 return im
def line(pts,col,width=1):
 im=blank();ImageDraw.Draw(im).line(pts,fill=col,width=width);return im
def rect(box,col):
 im=blank();ImageDraw.Draw(im).rectangle(box,fill=col);return im
def pts(im):return {(i%32,i//32) for i,v in enumerate(im.get_flattened_data()) if v[3]}
def frombits(bits):
 im=Image.new('L',(32,64));im.putdata([255 if b else 0 for b in bits]);return im
def front_fit(pose):
 m=baseBodyMasks['idle'] if pose=='idle' else baseBodyMasks['poses'][pose]
 pairs={'L':('leftArm','leftLeg','leftShoe'),'R':('rightArm','rightLeg','rightShoe')} if pose in ('P','idle') else {'L':('nearArm','trailingLeg','trailingShoe'),'R':('farArm','leadingLeg','leadingShoe')} if pose=='A' else {'L':('farArm','leadingLeg','leadingShoe'),'R':('nearArm','trailingLeg','trailingShoe')}
 result={'hips':m['shorts'],'torso':m['shirt']}
 for side,ks in pairs.items():
  for label,k in zip(('arm','leg','foot'),ks):result[label+side]=m[k]
 return copy.deepcopy(result)
def no_pack_body(pose):
 code=(root/'art/source/hero-forward-r12/base-build.py').read_text();start=code.index("  poly('daypackEdge'");end=code.index("  poly('farArm'",start);code=code[:start]+code[end:]
 ns={'__file__':str(root/'art/source/hero-forward-r12/base-build.py')};exec(compile(code.split('rawP,partsP=')[0],'<original-body-no-front-pack>','exec'),ns)
 raw,_=ns['body']('A')
 if pose=='C':raw=raw.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 return shift(raw,-2)
oldHead=Image.open(root/'docs/reviews/M1-HR6/hero-south.png').convert('RGBA').crop((0,0,32,46));oldHeadFull=blank();oldHeadFull.paste(oldHead,(0,0))
def head_for(direction,pose):
 hd=-2 if pose=='P' else 0
 if direction=='south':
  f='idle-forward.png' if pose=='idle' else f'walk-{dict(A=0,P=2,C=4)[pose]:02}.png';im=Image.open(base/f).convert('RGBA');head=blank();head.paste(im,(0,0),mask(shift(oldHeadFull,hd)));return head
 im=Image.open(root/f'docs/reviews/M1-HR6/hero-{direction}.png').convert('RGBA').crop((0,0,32,46));head=blank();head.paste(im,(0,hd))
 if direction=='north':
  # Keep the same small human-ear family behind the hair in the back view.
  for y in range(37+hd,42+hd):
   for x in range(4,7):head.putpixel((31-x,y),head.getpixel((x,y)))
 return head
def front_straps(pose):
 s=blank();d=ImageDraw.Draw(s);off=0 if pose=='idle' else -2
 if pose in ('P','idle'):
  for ps in [[(10,46),(10,48),(11,50)],[(21,46),(21,48),(20,50)]]:d.line([(x,y+off) for x,y in ps],fill='#ffffff')
 else:
  d.line([(27,45),(26,45),(25,46),(24,46),(22,48),(21,49)],fill='#ffffff');d.line([(10,47),(11,48),(11,49)],fill='#ffffff')
  if pose=='C':s=s.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 return s
def south(pose):
 hd=-2 if pose=='P' else 0;f='idle-forward.png' if pose=='idle' else f'walk-{dict(A=0,P=2,C=4)[pose]:02}.png';im=Image.open(base/f).convert('RGBA');head=head_for('south',pose)
 torso=poly([(12,42+hd),(19,42+hd),(21,45+hd),(20,48+hd),(13,49+hd),(11,46+hd)],P['c'])
 im.alpha_composite(torso)
 s=front_straps(pose);original=Image.open(base/f).convert('RGBA')
 for x,y in pts(s):im.putpixel((x,y),original.getpixel((x,y)))
 # Anatomical neck primitive remains at its original joint, entirely hidden.
 neck=rect((15,43+hd,17,45+hd),P['d']);im.alpha_composite(neck);im.alpha_composite(head)
 return im,head,torso,neck,copy.deepcopy(oldsc['poses'][pose]),front_fit(pose)
def north(pose):
 hd=-2 if pose=='P' else 0;fpose={'A':'C','C':'A'}.get(pose,pose)
 im,frontHead,_,_,points,fits=south(fpose)
 # Remove only the old foreground head; rebuild the upper back behind new head.
 for x,y in pts(frontHead):im.putpixel((x,y),(0,0,0,0))
 if fpose in ('A','C'):
  # Back view has ONE central pack: remove the old front-side peek and strap
  # using the original body beneath it, preserving arm attachment/skin.
  raw=no_pack_body(fpose);bounds=(24,43,29,51) if fpose=='A' else (3,43,8,51)
  for yy in range(bounds[1],bounds[3]):
   for xx in range(bounds[0],bounds[2]):im.putpixel((xx,yy),raw.getpixel((xx,yy)))
 torso=poly([(10,42+hd),(21,42+hd),(23,47+hd),(22,52+hd),(19,54+hd),(12,54+hd),(9,51+hd),(8,47+hd)],P['r'],P['O']);im.alpha_composite(torso)
 y=hd
 pack=poly([(12,44+y),(19,44+y),(21,46+y),(21,51+y),(19,53+y),(12,53+y),(10,51+y),(10,46+y)],P['b'],P['O'])
 pack.alpha_composite(poly([(12,46+y),(18,46+y),(19,47+y),(19,49+y),(12,49+y)],P['B']))
 pack.alpha_composite(line([(12,50+y),(19,50+y)],P['n']))
 im.alpha_composite(pack)
 im.alpha_composite(line([(9,46+y),(10,49+y)],P['n']));im.alpha_composite(line([(22,46+y),(21,49+y)],P['n']))
 head=head_for('north',pose);neck=rect((15,43+hd,17,45+hd),P['s']);im.alpha_composite(neck);im.alpha_composite(head)
 points['packAttach']=[16,47+hd]
 fits['pack']=[int(p[3]>0) for p in pack.get_flattened_data()]
 return im,head,torso,neck,points,fits
def side(pose,east=False):
 hd=-2 if pose=='P' else 0;dy=-2 if pose=='P' else 0
 # Coordinates are original projected construction guides, not source bones.
 if pose=='A':nearX,farX,handX=20,10,14
 elif pose=='C':nearX,farX,handX=11,21,19
 else:nearX,farX,handX=14,19,17
 im=blank();parts={}
 def add(k,layer):parts[k]=shift(layer,dy);im.alpha_composite(parts[k])
 # Far side lies behind near torso/limbs; tiny fragment, no long detached sole.
 add('farFoot',poly([(farX-1,58),(farX+1,58),(farX+2,59),(farX+1,60),(farX-1,60),(farX-2,59)],P['n'],P['O']))
 add('farLeg',poly([(14,54),(17,54),(farX+1,57),(farX+1,59),(farX-1,59),(farX-2,57)],P['n'],P['n']))
 add('pack',poly([(24,44),(26,44),(27,46),(27,50),(25,51),(23,50),(23,46)],P['b'],P['O']))
 add('packFlap',line([(24,46),(25,45),(26,46)],P['B']))
 add('farArm',poly([(11,46),(13,47),(13,50),(12,52),(10,51),(9,49)],P['d'],P['O']))
 add('nearFoot',poly([(nearX-2,58),(nearX+1,58),(nearX+2,59),(nearX+2,60),(nearX+1,61),(nearX-2,61),(nearX-3,60),(nearX-3,59)],P['n'],P['O']))
 # Continuous garment overlaps the shoe top instead of another outlined cuff
 # sitting on a separately outlined boot. Extents/joints remain unchanged.
 add('nearLeg',poly([(14,54),(19,54),(nearX+1,57),(nearX+1,59),(nearX-2,59),(nearX-2,57)],P['n'],P['n']))
 add('nearLegPlane',poly([(16,55),(18,55),(nearX,57),(nearX,58),(nearX-1,58),(nearX-1,57)],P['b']))
 add('shoeAccent',line([(nearX-1,60),(nearX,60)],P['b']))
 add('shorts',poly([(12,52),(20,52),(22,54),(21,56),(18,57),(14,56),(11,55)],P['n'],P['n']))
 add('shortsPlane',poly([(12,53),(16,53),(17,55),(14,55),(12,54)],P['b']))
 torso=poly([(12,42),(19,42),(22,45),(22,52),(20,54),(12,54),(10,51),(10,46)],P['r'],P['O']);add('torso',torso)
 add('chest',poly([(12,44),(16,44),(18,47),(16,49),(11,48),(11,46)],P['c']))
 add('shirtShade',poly([(20,46),(21,48),(21,52),(19,53),(17,53),(18,50)],P['v']))
 add('nearArm',poly([(16,47),(18,47),(handX+1,50),(handX+1,52),(handX-1,53),(handX-2,51),(handX-1,49)],P['s'],P['O']))
 add('sleeve',poly([(15,45),(18,45),(20,47),(18,49),(15,48),(14,47)],P['c'],P['O']))
 add('skinLight',line([(handX-1,50),(handX-1,51)],P['S']))
 add('strap',line([(21,46),(20,48),(20,50)],P['n']))
 points={'shoulderL':[17,47+dy],'shoulderR':[12,47+dy],'elbowL':[handX,50+dy],'elbowR':[11,49+dy],'wristL':[handX,52+dy],'wristR':[11,51+dy],'hipL':[17,55+dy],'hipR':[14,55+dy],'kneeL':[nearX,57+dy],'kneeR':[farX,57+dy],'ankleL':[nearX,59+dy],'ankleR':[farX,59+dy],'footL':[nearX,60+dy],'footR':[farX,59+dy],'strapL':[20,48+dy],'strapR':[21,46+dy],'packAttach':[25,46+dy],'earL':[19,40+hd],'earR':[21,39+hd],'neck':[16,45+hd],'headCenter':[16,35+hd],'torsoCenter':[16,49+dy]}
 head=head_for('east' if east else 'west',pose);neck=rect((15,43+hd,17,45+hd),P['d']);torso=shift(torso,dy)
 if east:
  im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT);torso=torso.transpose(Image.Transpose.FLIP_LEFT_RIGHT);neck=neck.transpose(Image.Transpose.FLIP_LEFT_RIGHT);points={k:[31-x,y] for k,(x,y) in points.items()}
 im.alpha_composite(neck);im.alpha_composite(head)
 def partmask(k):
  q=parts[k].transpose(Image.Transpose.FLIP_LEFT_RIGHT) if east else parts[k]
  return [int(p[3]>0) for p in q.get_flattened_data()]
 fits={'armL':partmask('nearArm'),'armR':partmask('farArm'),'legL':partmask('nearLeg'),'legR':partmask('farLeg'),'footL':partmask('nearFoot'),'footR':partmask('farFoot'),'hips':partmask('shorts'),'torso':partmask('torso'),'pack':partmask('pack')}
 return im,head,torso,neck,points,fits
def projected_front_dummy(pose,back=False):
 fp={'A':'C','C':'A'}.get(pose,pose) if back else pose
 f='mannequin-idle.png' if fp=='idle' else f'mannequin-{dict(A=0,P=2,C=4)[fp]:02}.png';im=Image.open(base/f).convert('RGBA');hd=-2 if pose=='P' else 0
 head=blank()
 for y in range(0,45+hd):
  for x in range(32):head.putpixel((x,y),im.getpixel((x,y)))
 # Project the chin over the neck site; no separate cyan neck cylinder.
 for x in range(12,20):head.putpixel((x,44+hd),(184,220,224,255));head.putpixel((x,45+hd),(37,51,64,255))
 for x in (10,11,20,21):head.putpixel((x,44+hd),(37,51,64,255))
 torso=rect((10,42+hd,21,49+hd),'#4ac2b0');neck=rect((15,43+hd,17,45+hd),'#b8dce0');im.alpha_composite(torso);im.alpha_composite(neck);im.alpha_composite(head)
 if back:im.alpha_composite(line([(16,47+hd),(16,51+hd)],'#359b93'))
 return im,head,torso,neck
def side_dummy(pose,points,east=False):
 hd=-2 if pose=='P' else 0;im=blank();C={'outline':'#253340','head':'#b8dce0','ears':'#ed8ccd','torso':'#4ac2b0','pelvis':'#9b83d4','arms':'#f1a566','legs':'#65a6de','feet':'#f1d171','joint':'#f5f1d9'}
 # Render in west space, then mirror all geometry once for east.
 ps={k:([31-x,y] if east else [x,y]) for k,(x,y) in points.items()}
 def bar(a,b,key,w=3):
  im.alpha_composite(line([ps[a],ps[b]],C['outline'],w+2));im.alpha_composite(line([ps[a],ps[b]],C[key],w))
 for suf in ('R','L'):
  bar('hip'+suf,'knee'+suf,'legs');bar('knee'+suf,'ankle'+suf,'legs');x,y=ps['foot'+suf];im.alpha_composite(poly([(x-2,y-1),(x+1,y-1),(x+2,y),(x+1,y+1),(x-2,y+1),(x-3,y)],C['feet'],C['outline']))
 bar('shoulderR','elbowR','arms');bar('elbowR','wristR','arms')
 torso=poly([(13,42+hd),(19,42+hd),(21,47+hd),(20,54+hd),(13,54+hd),(11,50+hd)],C['torso'],C['outline']);im.alpha_composite(torso)
 im.alpha_composite(poly([(13,52+hd),(20,52+hd),(21,55+hd),(18,56+hd),(13,55+hd)],C['pelvis'],C['outline']))
 bar('shoulderL','elbowL','arms');bar('elbowL','wristL','arms')
 neck=rect((15,43+hd,17,45+hd),C['head']);im.alpha_composite(neck)
 head=poly([(11,27+hd),(20,27+hd),(24,30+hd),(25,35+hd),(24,41+hd),(20,45+hd),(11,45+hd),(7,42+hd),(6,37+hd),(7,31+hd)],C['head'],C['outline'])
 # Only near ear visible; far ear is fully occluded, joint remains in data.
 head.alpha_composite(poly([(19,38+hd),(20,38+hd),(21,39+hd),(21,41+hd),(20,42+hd),(19,42+hd),(18,41+hd),(18,39+hd)],C['ears'],C['outline']));im.alpha_composite(head)
 d=ImageDraw.Draw(im)
 for k,(x,y) in ps.items():
  if k.startswith(('shoulder','elbow','wrist','hip','knee','ankle','foot')):d.point((x,y),fill=C['joint'])
 if east:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT);head=head.transpose(Image.Transpose.FLIP_LEFT_RIGHT);torso=torso.transpose(Image.Transpose.FLIP_LEFT_RIGHT);neck=neck.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 return im,head,torso,neck
for direction in directions:
 for pose in ('idle','A','P','C'):
  if direction=='south':hero,hh,ht,hn,joints,fits=south(pose);dummy,dh,dt,dn=projected_front_dummy(pose)
  elif direction=='north':hero,hh,ht,hn,joints,fits=north(pose);dummy,dh,dt,dn=projected_front_dummy(pose,True)
  else:hero,hh,ht,hn,joints,fits=side(pose,direction=='east');dummy,dh,dt,dn=side_dummy(pose,joints,direction=='east')
  heroes[direction][pose]=hero;dummies[direction][pose]=dummy
  fitMasks[direction][pose]=fits
  data[direction][pose]={'joints':joints,'hiddenNeckSite':joints['neck'],'farEarVisibility':'occluded' if direction in ('west','east') else 'paired visible','neckVisibleCellsHero':len(pts(hn)-pts(hh)),'neckVisibleCellsDummy':len(pts(dn)-pts(dh)),'headTorsoOverlapCellsHero':len(pts(ht)&pts(hh)),'headTorsoOverlapCellsDummy':len(pts(dt)&pts(dh)),'headMaskHero':[int(p[3]>0) for p in hh.get_flattened_data()],'headMaskDummy':[int(p[3]>0) for p in dh.get_flattened_data()],'torsoMaskHero':[int(p[3]>0) for p in ht.get_flattened_data()],'torsoMaskDummy':[int(p[3]>0) for p in dt.get_flattened_data()],'neckMaskHero':[int(p[3]>0) for p in hn.get_flattened_data()],'neckMaskDummy':[int(p[3]>0) for p in dn.get_flattened_data()]}
  hero.save(out/f'hero-{direction}-{pose}.png');dummy.save(out/f'dummy-{direction}-{pose}.png')
def export(name,frames):
 colors=[];lookup={}
 for _,im in frames:
  for px in im.get_flattened_data():
   if px[3]:
    c='#%02x%02x%02x'%px[:3]
    if c not in lookup:lookup[c]=len(colors)+1;colors.append(c)
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'character','width':32,'height':64,'palette':[None]+colors,'bank':'custom','notes':'HR13 projection review; original Hero/neutral construction dummy. Joint sites PROPOSED; neck/head occlusion explicit. Anchor16,64; review only.','frames':[{'name':label,'ticks':6,'pixels':[lookup['#%02x%02x%02x'%px[:3]] if px[3] else 0 for px in im.get_flattened_data()]} for label,im in frames]}
for kind,ims in [('hero',heroes),('dummy',dummies)]:
 (src/f'{kind}-idles.sprite.json').write_text(json.dumps(export('HR13 '+kind+' four idles',[(d,ims[d]['idle']) for d in directions]),separators=(',',':'))+'\n')
 for d in directions:(src/f'{kind}-{d}-walk.sprite.json').write_text(json.dumps(export('HR13 '+kind+' '+d+' proposed walk',[(str(i)+' '+p,ims[d][p]) for i,p in enumerate(order)]),separators=(',',':'))+'\n')
(src/'projection-and-joints.json').write_text(json.dumps({'status':'PROPOSED hidden anatomy/projection guides; no art approval','base':'HR12 3b947e8','canvas':[32,64],'groundAnchor':[16,64],'walkOrder':order,'previewHoldMs':100,'previewTimingStatus':'Critz proposal matched to front user GIF; ROM comparisons use phase images at this preview clock, not engine timing','frontJointSitesUnchangedFromHR12':True,'headBodyOcclusion':'neck primitive entirely under head; torso projects behind head','directions':data},separators=(',',':'))+'\n')
(src/'clothing-part-masks.json').write_text(json.dumps({'status':'Original projected clothing masks for proposed attachment-fit checks; hidden joints not source-measured','canvas':[32,64],'directions':fitMasks},separators=(',',':'))+'\n')
print({d:{p:(data[d][p]['neckVisibleCellsHero'],data[d][p]['neckVisibleCellsDummy'],data[d][p]['headTorsoOverlapCellsHero'],data[d][p]['headTorsoOverlapCellsDummy']) for p in ('idle','A','P','C')} for d in directions})
