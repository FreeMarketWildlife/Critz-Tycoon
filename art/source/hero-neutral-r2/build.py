"""NB2 initial reconstructed neutral mannequin. No runtime or Hero edits.
Authored under-clothes anatomy, not reference-measured bones. Separate RGBA parts
and selected-Hero-specific appearance/costume ownership, not a creator system.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-NB2';base=root/'docs/reviews/M1-HR14';meta=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());order=meta['order'];records={};images={};checks=[]
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
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'character','width':32,'height':64,'palette':pal,'bank':'custom','notes':'NB2 UNAPPROVED authored neutral mannequin reconstruction; no measured hidden anatomy.','frames':[{'name':name,'ticks':6,'pixels':[look['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in im.get_flattened_data()]}]}
for dr in ('south','west'):
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
  if dr in ('west','east'):
   for i,pixel in enumerate(hero.get_flattened_data()):
    if pixel[3] and pixel[:3] in {(166,104,69),(195,138,88),(116,69,57)} and e['headMaskHero'][i] and not head.getpixel((i%32,i//32))[3]:extension.putpixel((i%32,i//32),rgba('#b8dce0'))
   head.alpha_composite(extension)
  # Independent authored tapered core, no shirt flare, cuff/shorts/pack outline.
  profile=dr in ('west','east');cx=16
  parts['torso']=shape([(10,43+dy),(21,43+dy),(22,47+dy),(20,52+dy),(11,52+dy),(9,47+dy)],'#afbdc2')
  if profile:
   parts['torso']=shape([(11,42+dy),(22,42+dy),(22,47+dy),(20,52+dy),(13,52+dy),(10,47+dy)],'#afbdc2')
   if dr=='east':parts['torso']=parts['torso'].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  parts['pelvis']=shape([(12,51+dy),(19,51+dy),(20,54+dy),(18,56+dy),(13,56+dy),(11,54+dy)],'#9eafb6')
  last=hero.getbbox()[3]-1;xs=[x for x in range(32) if hero.getpixel((x,last))[3]]
  if po in ('idle','P'):
   footcenters=[(11,last),(20,last)] if not profile else [(14,last),(18,last-1)]
  elif not profile:
   near=round(sum(xs)/len(xs));far=11 if near>15 else 21;footcenters=sorted([(near,last),(far,last-2)])
  else:
   near=round(sum(xs)/len(xs));far=11 if near>15 else 21;footcenters=[(near,last),(far,last-2)]
  if dr=='east' and po in ('idle','P'):footcenters=[(17,last),(13,last-1)]
  for k,(fx,fy) in enumerate(footcenters):
   hip=(14 if k==0 else 18,54+dy);parts[f'leg{k}']=limb(hip,(fx,fy-2),'#bbc8cc');foot=blank();dd=ImageDraw.Draw(foot);dd.rounded_rectangle((fx-1,fy-2,fx+2,fy),radius=1,fill='#c5d0d3',outline='#56656e');parts[f'foot{k}']=foot
  # Actual selected hand sites are visible evidence; connecting arms reconstructed.
  hp=[tuple(p) for p in e['commonFeatureRegistration']['hands']['cells']];groups=[[(x,y) for x,y in hp if x<16],[(x,y) for x,y in hp if x>=16]]
  if profile:groups=[hp,[]]
  for k,g in enumerate(groups):
   shoulder=((19 if dr=='west' else 12) if profile and k==0 else (13 if dr=='west' else 18) if profile else 12 if k==0 else 19,(43 if profile else 46)+dy)
   target=(round(sum(x for x,y in g)/len(g)),round(sum(y for x,y in g)/len(g))) if g else ((12 if dr=='west' else 19) if profile else 11 if k==0 else 20,50+dy)
   elbow=((shoulder[0]+target[0])//2,(48 if profile else 49)+dy);arm=limb(shoulder,elbow,'#b6c3c8');arm.alpha_composite(limb(elbow,target,'#b6c3c8'));parts[f'arm{k}']=arm
   hand=blank()
   if g:
    for p in g:hand.putpixel(p,rgba('#c7d1d4'))
   else:ImageDraw.Draw(hand).ellipse((target[0]-1,target[1]-1,target[0]+1,target[1]+1),fill='#c7d1d4',outline='#56656e')
   parts[f'hand{k}']=hand
  body=blank();z=['leg1','foot1','arm1','hand1','leg0','foot0','pelvis','torso','arm0','hand0','head']
  if not profile and po in ('A','C'):
   nearleg=0 if footcenters[0][1]>footcenters[1][1] else 1;farleg=1-nearleg
   z=[f'leg{farleg}',f'foot{farleg}','arm1','hand1',f'leg{nearleg}',f'foot{nearleg}','pelvis','torso','arm0','hand0','head']
  for name in z:body.alpha_composite(parts[name])
  topOwner={}
  for name in z:
   for pt in cells(parts[name]):topOwner[tuple(pt)]=name
  # Actual source pixels partitioned into removable semantic appearance layers.
  # Region ownership is a declared Hero-specific proposal, not hidden anatomy.
  costume={n:blank() for n in ('hair','skin-face-features','shirt','shorts','shoes','pack','straps')};owners={};skinRGB={(166,104,69),(195,138,88),(116,69,57)}
  for i,p in enumerate(hero.get_flattened_data()):
   if not p[3]:continue
   x,y=i%32,i//32
   if e['headMaskHero'][i]:
    isEye=[x,y] in e['commonFeatureRegistration']['eyes']['cells']
    collarTop=(43 if dr=='south' else 45 if dr=='north' else 44)+dy
    name='skin-face-features' if p[:3] in skinRGB or isEye else 'shirt' if y>=collarTop else 'hair'
   elif e['visiblePackMask'][i]:name='pack'
   elif e['strapMask'][i] and p==Image.open(base/f'strap-layer-{dr}-{po}.png').convert('RGBA').getpixel((x,y)):name='straps'
   elif p[:3] in skinRGB:name='skin-face-features'
   elif y>=(58+(0 if po=='idle' else dy) if dr=='south' else last-3):name='shoes'
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
  (src/f'{dr}-{po}.sprite.json').write_text(json.dumps(export('NB2 '+dr+' '+po,body),separators=(',',':'))+'\n')
  records[dr][po]={'bodyZOrder':z,'bodyMasks':{n:cells(im) for n,im in parts.items()},'visibleBodyPartMasks':{n:[list(p) for p,owner in topOwner.items() if owner==n] for n in parts},'faceFeatureCells':e['commonFeatureRegistration']['eyes']['cells'],'bodyAppearanceMask':cells(costume['skin-face-features']),'costumeMasks':{n:cells(im) for n,im in costume.items() if n!='skin-face-features'},'appearanceOwnership':owners,'dressingClippedBodyCells':occluded,'actualVisibleBodyCells':cells(costume['skin-face-features']),'explicitHeadSurfaceExtension':cells(extension),'darkHeadBoundaryOwnership':'Non-skin/non-eye head-labelled pixels43+ are collar/garment; earlier edge/fringe sites are removable hair. Old headMaskHero is not anatomical truth.','footLegOverlapCells':{str(k):[list(p) for p in sorted({tuple(p) for p in cells(parts[f'foot{k}'])}&{tuple(p) for p in cells(parts[f'leg{k}'])})] for k in (0,1)},'rearPackRole':'Full canonical source pack stored separately; actual pack ownership uses verified original visiblePackMask. North pack foreground; other views source occlusion preserved.','headTorsoProjection':'Head overlaps upper torso; no exposed neck column','underClothes':'Authored reconstruction; no measured hidden joints or bone lengths','costumeOwnership':'Selected-Hero-specific explicit material/region proposal; shorts/shoe split and jaw/hair-edge ownership are not source facts','contact':'Same existing last painted row; barefoot footprint is authored compact4px, not copied shoe width','sourceHeroSHA256':hashlib.sha256((base/f'hero-{dr}-{po}.png').read_bytes()).hexdigest()}
  images[dr][po]=(old,body,overlay,recomposed)
  check('costume does not own skin/face/hand cells',all(not overlay.getpixel(tuple(pt))[3] for pt in cells(costume['skin-face-features'])))
  check('visible body contributes exact selected skin/face',all(recomposed.getpixel(tuple(pt))==covered.getpixel(tuple(pt)) for pt in cells(costume['skin-face-features'])))
(src/'construction.json').write_text(json.dumps({'task':'M1.NB2','state':'SOUTH+WEST IDLE COMPACT DIAGNOSTIC / UNAPPROVED','frame':[32,64],'edgeAnchor':[16,64],'priorCheckpoint':'NB1 source f871866; South idle must remain exact','limits':['Hidden contours/joints are authored reconstruction, not reference-measured bones','Garment/footwear split is per-view selected-art ownership, not anatomical source facts','Profile head extends only at actual brown visible face sites, never dark collar edges','Explicit dressing stencil records all concealed neutral pixels','This is current selected outfit proof, not creator/swaps approval'],'directions':records,'order':order},separators=(',',':'))+'\n')
(out/'construction-checks.json').write_text(json.dumps({'checks':checks,'pass':True,'visualApproval':False},indent=2)+'\n');print('NB2 compact South/West idle diagnostic; awaiting independent construction review.')
