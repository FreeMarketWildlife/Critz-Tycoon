"""NB1 initial reconstructed neutral mannequin. No runtime or Hero edits.
Authored under-clothes anatomy, not reference-measured bones. Separate RGBA parts
and selected-Hero-specific appearance/costume ownership, not a creator system.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-NB1';base=root/'docs/reviews/M1-HR14';meta=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());order=meta['order'];records={};images={};checks=[]
def blank():return Image.new('RGBA',(32,64))
def rgba(c):return tuple(bytes.fromhex(c[1:]))+(255,)
def check(name,v):assert v,name;checks.append(name)
def shape(points,c):
 q=blank();d=ImageDraw.Draw(q);d.polygon(points,fill=c);d.line(points+[points[0]],fill='#56656e');return q
def limb(a,b,c):
 q=blank();d=ImageDraw.Draw(q);d.line((a,b),fill='#56656e',width=5);d.line((a,b),fill=c,width=3);return q
def cells(im):return [[i%32,i//32] for i,p in enumerate(im.get_flattened_data()) if p[3]]
def hair_site(x,y,p,dy):
 eye=x in (12,13,18,19) and 38+dy<=y<=41+dy
 skin=p[:3] in {(166,104,69),(195,138,88),(116,69,57)}
 return y<36+dy or (y<=40+dy and not skin and not eye)
def export(name,im):
 pal=[None];look={}
 for p in im.get_flattened_data():
  if p[3]:
   c='#%02x%02x%02x'%p[:3]
   if c not in look:look[c]=len(pal);pal.append(c)
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'character','width':32,'height':64,'palette':pal,'bank':'custom','notes':'NB1 UNAPPROVED authored neutral mannequin reconstruction; no measured hidden anatomy.','frames':[{'name':name,'ticks':6,'pixels':[look['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in im.get_flattened_data()]}]}
for dr in ('south',):
 records[dr]={};images[dr]={}
 for po in ('idle',):
  folder=out/f'{dr}-{po}';folder.mkdir(exist_ok=True);hero=Image.open(base/f'hero-{dr}-{po}.png').convert('RGBA');old=Image.open(base/f'dummy-{dr}-{po}.png').convert('RGBA');e=meta['directions'][dr][po];dy=-2 if po=='P' else 0;parts={}
  # Retain previously checked bald head, actual eyes/ears and no-mouth default.
  head=blank()
  for i,on in enumerate(e['headMaskDummy']):
   if on:head.putpixel((i%32,i//32),old.getpixel((i%32,i//32)))
  parts['head']=head
  # Smooth existing bald contour stays unchanged; selected dark jaw/collar
  # edges belong to removable hair/garment, never manufactured skull volume.
  extension=blank()
  # Independent authored tapered core, no shirt flare, cuff/shorts/pack outline.
  profile=dr in ('west','east');cx=16
  parts['torso']=shape([(10,43+dy),(21,43+dy),(22,47+dy),(20,52+dy),(11,52+dy),(9,47+dy)],'#afbdc2')
  parts['pelvis']=shape([(12,51+dy),(19,51+dy),(20,54+dy),(18,56+dy),(13,56+dy),(11,54+dy)],'#9eafb6')
  last=hero.getbbox()[3]-1;xs=[x for x in range(32) if hero.getpixel((x,last))[3]]
  if po in ('idle','P'):
   footcenters=[(11,last),(20,last)] if not profile else [(14,last),(18,last-1)]
  elif not profile:
   near=round(sum(xs)/len(xs));far=11 if near>15 else 21;footcenters=[(near,last),(far,last-2)]
  else:
   near=round(sum(xs)/len(xs));far=11 if near>15 else 21;footcenters=[(near,last),(far,last-2)]
  if dr=='east' and po in ('idle','P'):footcenters=[(17,last),(13,last-1)]
  for k,(fx,fy) in enumerate(footcenters):
   hip=(14 if k==0 else 18,54+dy);parts[f'leg{k}']=limb(hip,(fx,fy-2),'#bbc8cc');foot=blank();dd=ImageDraw.Draw(foot);dd.rounded_rectangle((fx-1,fy-2,fx+2,fy),radius=1,fill='#c5d0d3',outline='#56656e');parts[f'foot{k}']=foot
  # Actual selected hand sites are visible evidence; connecting arms reconstructed.
  hp=[tuple(p) for p in e['commonFeatureRegistration']['hands']['cells']];groups=[[(x,y) for x,y in hp if x<16],[(x,y) for x,y in hp if x>=16]]
  for k,g in enumerate(groups):
   shoulder=(12 if k==0 else 19,46+dy)
   target=(round(sum(x for x,y in g)/len(g)),round(sum(y for x,y in g)/len(g))) if g else (11 if k==0 else 20,50+dy)
   elbow=((shoulder[0]+target[0])//2,49+dy);arm=limb(shoulder,elbow,'#b6c3c8');arm.alpha_composite(limb(elbow,target,'#b6c3c8'));parts[f'arm{k}']=arm
   hand=blank()
   if g:
    for p in g:hand.putpixel(p,rgba('#c7d1d4'))
   else:ImageDraw.Draw(hand).ellipse((target[0]-1,target[1]-1,target[0]+1,target[1]+1),fill='#c7d1d4',outline='#56656e')
   parts[f'hand{k}']=hand
  body=blank();z=['leg1','foot1','arm1','hand1','leg0','foot0','pelvis','torso','arm0','hand0','head']
  for name in z:body.alpha_composite(parts[name])
  # Actual source pixels partitioned into removable semantic appearance layers.
  # Region ownership is a declared Hero-specific proposal, not hidden anatomy.
  costume={n:blank() for n in ('hair','skin-face-features','shirt','shorts','shoes','pack','straps')};owners={};skinRGB={(166,104,69),(195,138,88),(116,69,57)}
  for i,p in enumerate(hero.get_flattened_data()):
   if not p[3]:continue
   x,y=i%32,i//32
   if e['headMaskHero'][i]:
    isEye=x in (12,13,18,19) and 38+dy<=y<=41+dy
    name='skin-face-features' if p[:3] in skinRGB or isEye else 'shirt' if y>=43+dy else 'hair'
   elif e['visiblePackMask'][i]:name='pack'
   elif e['strapMask'][i] and p==Image.open(base/f'strap-layer-{dr}-{po}.png').convert('RGBA').getpixel((x,y)):name='straps'
   elif p[:3] in skinRGB:name='skin-face-features'
   elif y>=58+(0 if po=='idle' else dy):name='shoes'
   elif y>=53+dy:name='shorts'
   else:name='shirt'
   costume[name].putpixel((x,y),p);owners[f'{x},{y}']=name
  check('all selected visible skin/face supported by neutral body geometry',all(body.getpixel(tuple(p))[3] for p in cells(costume['skin-face-features'])))
  for k in (0,1):check('foot '+str(k)+' overlaps its leg',len({tuple(p) for p in cells(parts[f'foot{k}'])}&{tuple(p) for p in cells(parts[f'leg{k}'])})>=2)
  # Explicit dressing coverage: neutral reconstruction has different hidden
  # contours. This mask is separate, inspectable and NOT neutral-body geometry.
  clip=Image.new('L',(32,64));clip.putdata([255 if p[3] else 0 for p in hero.get_flattened_data()]);skinBody=blank()
  for i,pixel in enumerate(body.get_flattened_data()):
   if pixel[3]:skinBody.putpixel((i%32,i//32),rgba('#242330' if pixel[:3] in ((86,101,110),(37,51,64)) else '#744539' if pixel[:3]==(237,140,205) else '#a66845'))
  covered=blank();covered.paste(skinBody,(0,0),clip)
  overlay=blank()
  for name,im in costume.items():
   if name!='skin-face-features':overlay.alpha_composite(im)
  covered.alpha_composite(costume['skin-face-features'])
  recomposed=Image.alpha_composite(covered,overlay)
  covered.save(folder/'body-only-selected-skin.png')
  for garment in ('shirt','shorts','shoes','hair','pack','straps'):
   Image.alpha_composite(covered,costume[garment]).save(folder/f'body-plus-{garment}.png')
  check(dr+po+' exact selected Hero recomposition',recomposed.tobytes()==hero.tobytes());check(dr+po+' registered contact row',body.getbbox()[3]-1==last)
  occluded=[p for p in cells(body) if not hero.getpixel(tuple(p))[3]]
  for n,im in parts.items():im.save(folder/f'body-{n}.png')
  for n,im in costume.items():im.save(folder/f'overlay-{n}.png')
  covered.save(folder/'body-render-with-selected-skin.png');costume['skin-face-features'].save(folder/'actual-visible-body-contribution.png');Image.open(base/f'pack-layer-{dr}-{po}.png').save(folder/'full-rear-pack.png');body.save(folder/'neutral-body.png');overlay.save(folder/'removable-appearance.png');recomposed.save(folder/'recomposed-hero.png');clip.save(folder/'dressing-coverage-mask.png')
  (src/f'{dr}-{po}.sprite.json').write_text(json.dumps(export('NB1 '+dr+' '+po,body),separators=(',',':'))+'\n')
  records[dr][po]={'bodyZOrder':z,'bodyMasks':{n:cells(im) for n,im in parts.items()},'bodyAppearanceMask':cells(costume['skin-face-features']),'costumeMasks':{n:cells(im) for n,im in costume.items() if n!='skin-face-features'},'appearanceOwnership':owners,'dressingClippedBodyCells':occluded,'actualVisibleBodyCells':cells(costume['skin-face-features']),'explicitHeadSurfaceExtension':cells(extension),'darkHeadBoundaryOwnership':'Non-skin/non-eye head-labelled pixels43+ are collar/garment; earlier edge/fringe sites are removable hair. Old headMaskHero is not anatomical truth.','footLegOverlapCells':{str(k):[list(p) for p in sorted({tuple(p) for p in cells(parts[f'foot{k}'])}&{tuple(p) for p in cells(parts[f'leg{k}'])})] for k in (0,1)},'rearPackRole':'Full original rear pack RGBA stored separately; front visible pack contribution is zero under selected costume. Exact partition proof uses visible pack contribution.','headTorsoProjection':'Head overlaps upper torso; no exposed neck column','underClothes':'Authored reconstruction; no measured hidden joints or bone lengths','costumeOwnership':'Selected-Hero-specific explicit material/region proposal; shorts/shoe split and jaw/hair-edge ownership are not source facts','contact':'Same existing last painted row; barefoot footprint is authored compact4px, not copied shoe width','sourceHeroSHA256':hashlib.sha256((base/f'hero-{dr}-{po}.png').read_bytes()).hexdigest()}
  images[dr][po]=(old,body,overlay,recomposed)
  check('costume does not own skin/face/hand cells',all(not overlay.getpixel(tuple(pt))[3] for pt in cells(costume['skin-face-features'])))
  check('visible body contributes exact selected skin/face',all(recomposed.getpixel(tuple(pt))==covered.getpixel(tuple(pt)) for pt in cells(costume['skin-face-features'])))
# Bounded checkpoint plates, not extensive Library packaging.
plate=Image.new('RGB',(1600,370),'#bed4d5');d=ImageDraw.Draw(plate)
for r,dr in enumerate(images):
 for c,(label,im) in enumerate(zip(('OLD MATERIAL MAP','NEUTRAL BODY PROPOSAL','REMOVABLE APPEARANCE','EXACT RECOMPOSED HERO'),images[dr]['idle'])):
  x=c*400;y=r*355;d.text((x+6,y+6),dr+' '+label,fill='#253340');big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+50,y+28),big);plate.paste(im,(x+230,y+160),im);d.line((x+50,y+284,x+178,y+284),fill='#748894');d.line((x+111,y+284,x+117,y+284),fill='#ed745c')
d.text((8,348),'NB1 INITIAL UNAPPROVED reconstruction / fixed32x64 +16,64. Skin/face/hand pixels belong to body rendering, not clothing. Not a creator.',fill='#253340');plate.save(out/'south-idle-initial-body-checkpoint.png')
# Actual exploded front idle body layers; stored independent RGBA, no nominal masks.
plate=Image.new('RGB',(1320,680),'#bed4d5');d=ImageDraw.Draw(plate)
for n,(name,pts) in enumerate(records['south']['idle']['bodyMasks'].items()):
 im=Image.open(out/'south-idle'/f'body-{name}.png');x=(n%6)*220;y=(n//6)*340;d.text((x+4,y+4),name+' / actual layer',fill='#253340');big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+46,y+24),big)
plate.save(out/'front-idle-exploded-body-layers.png')
# Actual selected-body contribution and each costume overlay, no flattened-Hero clothing.
plate=Image.new('RGB',(1600,680),'#bed4d5');d=ImageDraw.Draw(plate)
labels=['body-render-with-selected-skin','actual-visible-body-contribution','overlay-shirt','overlay-shorts','overlay-shoes','overlay-hair','overlay-pack','overlay-straps']
for n,name in enumerate(labels):
 im=Image.open(out/'south-idle'/(name+'.png')).convert('RGBA');x=(n%4)*400;y=(n//4)*340;d.text((x+5,y+5),name,fill='#253340');big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+60,y+25),big);plate.paste(im,(x+240,y+150),im)
plate.save(out/'south-idle-actual-body-costume-contributions.png')
# Removal/single-garment proof uses actual skin-rendered body, not blank backing.
plate=Image.new('RGB',(1600,680),'#bed4d5');d=ImageDraw.Draw(plate)
for n,name in enumerate(['body-only-selected-skin','body-plus-shirt','body-plus-shorts','body-plus-shoes','body-plus-hair','body-plus-pack','body-plus-straps','recomposed-hero']):
 im=Image.open(out/'south-idle'/(name+'.png')).convert('RGBA');x=(n%4)*400;y=(n//4)*340;d.text((x+5,y+4),name,fill='#253340');big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+60,y+24),big);plate.paste(im,(x+240,y+140),im)
plate.save(out/'south-idle-body-garment-toggles.png')
(src/'construction.json').write_text(json.dumps({'task':'M1.NB1','state':'SOUTH IDLE FIRST CHECKPOINT ONLY / UNAPPROVED','frame':[32,64],'edgeAnchor':[16,64],'audit':'HR14 old dummy copies clothed alpha/material shapes; not an independent anatomical base. New core/pelvis/limbs/feet are independent authored shapes.','limits':['Under-clothes contours and joints reconstructed, not measured','Hero-specific garment/shorts/shoe ownership proposed, not observed anatomy','Selected visible skin/face/hands are body rendering, excluded from costume','Dressing stencil only conceals disclosed cells outside selected Hero alpha','Exact recomposition does not validate body reconstruction or later swaps','Other directions/walk checkpoints held for first South review'], 'directions':records},separators=(',',':'))+'\n')
(out/'checks.json').write_text(json.dumps({'checks':checks,'pass':True,'visualApproval':False,'next':'Independent first South body contour and true layer ownership review before continuation'},indent=2)+'\n');print('NB1 first SOUTH IDLE body checkpoint. Seven support/attachment/registration/recomposition/ownership checks pass; visual review required.')
