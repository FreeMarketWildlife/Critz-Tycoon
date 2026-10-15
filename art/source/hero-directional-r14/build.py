"""HR14 original identity + observed visible costume construction; rigid pack.
Authoring reads only Critz source assets. Reference comparison lives separately.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,copy
from lower import LOWER
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR14';old=root/'docs/reviews/M1-HR13'
P={'O':'#242330','h':'#322a31','m':'#4c3739','l':'#705044','s':'#a66845','S':'#c38a58','d':'#744539','r':'#ed745c','R':'#ffad7a','v':'#ae454a','c':'#f9edc8','C':'#bfc0aa','b':'#465671','B':'#748894','n':'#2a344a'}
D={'O':'#253340','head':'#b8dce0','ear':'#ed8ccd','torso':'#4ac2b0','arms':'#f1a566','hands':'#ffd4a1','pants':'#9b83d4','cuff':'#65a6de','sole':'#f1d171'}
meta13=json.loads((root/'art/source/hero-directional-r13/projection-and-joints.json').read_text());eyeMasks=json.loads((root/'art/source/hero-redesign-r6/masks.json').read_text());order=['A','A','P','P','C','C','P','P'];directions=('south','north','west','east')
def blank():return Image.new('RGBA',(32,64))
def shift(im,dy):
 q=Image.new(im.mode,im.size);q.paste(im,(0,dy));return q
def poly(points,color,edge=None):
 q=blank();d=ImageDraw.Draw(q);d.polygon(points,fill=color)
 if edge:d.line(points+[points[0]],fill=edge)
 return q
def bits(im):return [int(px[3]>0) for px in im.get_flattened_data()]
def maskimage(b):
 q=Image.new('L',(32,64));q.putdata([255 if v else 0 for v in b]);return q
def extracted(im,b):
 q=blank();q.paste(im,(0,0),maskimage(b));return q
# Reuse only original native upper-body drawing function, without any pack.
code=(root/'art/source/hero-forward-r12/base-build.py').read_text();a=code.index("  poly('daypackEdge'");b=code.index("  poly('farArm'",a);code=code[:a]+code[b:];ns={'__file__':str(root/'art/source/hero-forward-r12/base-build.py')};exec(compile(code.split('rawP,partsP=')[0],'<original-upper-body-no-pack>','exec'),ns)
def upper(d,pose):
 e=meta13['directions'][d][pose];dy=-2 if pose=='P' else 0
 if d=='south':
  raw,_=ns['body']('P' if pose in ('P','idle') else 'A')
  if pose=='C':raw=raw.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  body=shift(raw,0 if pose=='idle' else -2)
  t=poly([(12,42+dy),(19,42+dy),(21,45+dy),(20,48+dy),(13,49+dy),(11,46+dy)],P['c']);body.alpha_composite(t)
 else:
  h=Image.open(old/f'hero-{d}-{pose}.png').convert('RGBA');body=h.copy()
  hm=e['headMaskHero']
  for i,on in enumerate(hm):
   if on:body.putpixel((i%32,i//32),(0,0,0,0))
  # Clear the old bag and straps through original upper-layer reconstruction.
  # Central back gets a fresh coral torso; profile keeps original arm silhouette.
  if d=='north':
   body=blank();raw,_=ns['body']('P' if pose in ('P','idle') else 'A')
   if pose=='A':raw=raw.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   body=shift(raw,0 if pose=='idle' else -2)
   t=poly([(10,42+dy),(21,42+dy),(23,47+dy),(22,52+dy),(19,54+dy),(12,54+dy),(9,51+dy),(8,47+dy)],P['r'],P['O']);body.alpha_composite(t)
  else:
   # Old bag was behind torso at x23..27; mirror to remove exact old coverage.
   for y in range(42+dy,53+dy):
    for xw in range(23,29):body.putpixel((31-xw if d=='east' else xw,y),(0,0,0,0))
   t=extracted(h,e['torsoMaskHero']);body.alpha_composite(t)
 return body

def pack_layers(d):
 # Canonical layers in torso-local coordinates (anchor16,48); translated as one
 # rigid unit with torso. A/C NEVER mirror the bag or change its attachment.
 if d in ('south','north'):
  bag=poly([(12,44),(19,44),(21,46),(21,51),(19,53),(12,53),(10,51),(10,46)],P['b'],P['O'])
  dd=ImageDraw.Draw(bag);dd.rectangle((12,46,18,49),fill=P['B']);dd.line((12,51,19,51),fill=P['n'])
  strap=blank();sd=ImageDraw.Draw(strap)
  for line in [[(11,45),(11,48),(12,50)],[(20,45),(20,48),(19,50)]]:sd.line(line,fill=P['n']);sd.point(line[0],fill=P['B'])
 else:
  bag=poly([(23,44),(25,44),(26,46),(26,50),(25,52),(23,51),(22,49),(22,46)],P['b'],P['O']);dd=ImageDraw.Draw(bag);dd.line((24,46,24,49),fill=P['B'])
  strap=blank();ImageDraw.Draw(strap).line([(20,45),(19,48),(19,50)],fill=P['n'])
  if d=='east':bag=bag.transpose(Image.Transpose.FLIP_LEFT_RIGHT);strap=strap.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 return bag,strap

def lower_image(d,pose):
 rows=LOWER[d][pose];im=blank();semantic={k:[] for k in ('darkPlane','slateShadow','slateLight','warmGray','coral','paleBand')}
 for iy,row in enumerate(rows):
  for x,key in enumerate(row):
   if key=='.':continue
   y=54+iy;col=P[{'p':'n','h':'b','f':'B','l':'C','a':'v'}.get(key,key)]
   if key=='p':
    # Retain connected garment mass, use dark outer contour. Top row connects
    # into torso rather than drawing an invented separate waistband rail.
    neighbors=[(x-1,iy),(x+1,iy),(x,iy+1)]+([(x,iy-1)] if iy else [])
    if any(xx<0 or xx>=32 or yy>=10 or rows[yy][xx]=='.' for xx,yy in neighbors):col=P['O']
   im.putpixel((x,y),tuple(bytes.fromhex(col[1:]))+(255,))
   group={'p':'darkPlane','n':'darkPlane','h':'slateShadow','f':'slateLight','l':'warmGray','a':'coral','c':'paleBand'}[key];semantic[group].append([x,y])
 return im,semantic
frames={k:{d:{} for d in directions} for k in ('hero','dummy')};records={d:{} for d in directions}
for d in directions:
 for pose in ('idle','A','P','C'):
  dy=-2 if pose=='P' else 0;e=meta13['directions'][d][pose];body=upper(d,pose)
  # Four-direction source passing/rest construction; south idle is explicitly
  # a proposed2px-down passing derivative, not an observed supplied-GIF idle.
  lp='P' if pose=='idle' else pose;lower,semantic=lower_image(d,lp)
  if pose=='idle' and d=='south':lower=shift(lower,2);semantic={k:[[x,y+2] for x,y in v] for k,v in semantic.items()}
  for y in range(56 if pose=='idle' and d=='south' else 54,64):
   for x in range(32):body.putpixel((x,y),lower.getpixel((x,y)))
  # Pack follows torso/head bounce; no lateral bob or per-pose shape redraw.
  bag0,straps0=pack_layers(d);bag=shift(bag0,dy);straps=shift(straps0,dy);anchor=[16,48+dy]
  # Visible torso occludes rear bag in front/profile; back bag is on torso.
  torsoNoPack=body.copy();composite=blank()
  if d=='north':composite.alpha_composite(body);composite.alpha_composite(bag)
  else:composite.alpha_composite(bag);composite.alpha_composite(body)
  # Straps are fixed canonical slots, clipped by actual opaque upper torso;
  # sleeve/hand occlusion is explicit instead of dragging the pack with arms.
  for y in range(42+dy,54):
   for x in range(32):
    px=straps.getpixel((x,y));bp=body.getpixel((x,y))
    if px[3] and bp[3] and bp[:3] not in [tuple(bytes.fromhex(P[k][1:])) for k in ('s','S','d')]:composite.putpixel((x,y),px)
  original=Image.open(old/f'hero-{d}-{pose}.png').convert('RGBA');head=extracted(original,e['headMaskHero']);composite.alpha_composite(head)
  # Save actual visible pack coverage by comparing canonical bag against every
  # foreground layer, not by pretending the unoccluded mask is the composite.
  visible=blank()
  for i,px in enumerate(bag.get_flattened_data()):
   x,y=i%32,i//32
   if px[3] and composite.getpixel((x,y))==px and not head.getpixel((x,y))[3] and (d=='north' or not body.getpixel((x,y))[3]):visible.putpixel((x,y),px)
  dummy=blank()
  # Color-coded visible construction, with no invented exposed calf or neck.
  lowerCoords={tuple(pt):k for k,v in semantic.items() for pt in v}
  for y in range(64):
   for x in range(32):
    px=body.getpixel((x,y))
    if not px[3]:continue
    rgb=px[:3];group=lowerCoords.get((x,y));isHand=rgb in [tuple(bytes.fromhex(P[k][1:])) for k in ('s','S','d')]
    if rgb==tuple(bytes.fromhex(P['O'][1:])):col=D['O']
    elif group:col=D[{'darkPlane':'pants','slateShadow':'pants','slateLight':'cuff','warmGray':'cuff','coral':'pants','paleBand':'sole'}[group]]
    elif isHand:col=D['hands']
    else:col=D['torso']
    dummy.putpixel((x,y),tuple(bytes.fromhex(col[1:]))+(255,))
  # Restore same projected head, ears and occlusion as HR13, now with aligned eyes.
  dh=extracted(Image.open(old/f'dummy-{d}-{pose}.png').convert('RGBA'),e['headMaskDummy'])
  for i,on in enumerate(eyeMasks[d].get('eyes',[0]*2048)):
   x,y=i%32,i//32+dy
   if on and 0<=y<64 and dh.getpixel((x,y))[3]:dh.putpixel((x,y),tuple(bytes.fromhex(D['O'][1:]))+(255,))
  dummy.alpha_composite(dh)
  frames['hero'][d][pose]=composite;frames['dummy'][d][pose]=dummy
  for kind,im in [('hero',composite),('dummy',dummy),('pack-layer',bag),('strap-layer',straps),('pack-visible',visible)]:im.save(out/f'{kind}-{d}-{pose}.png')
  records[d][pose]={'torsoAnchor':anchor,'torsoTransform':[0,dy],'canonicalPackAnchor':[16,48],'canonicalPackMask':bits(bag0),'canonicalStrapMask':bits(straps0),'packMask':bits(bag),'strapMask':bits(straps),'visiblePackMask':bits(visible),'visibleMaterialPlanes':semantic,'headMaskHero':e['headMaskHero'],'headMaskDummy':e['headMaskDummy'],'headTorsoProjection':'Retained head/torso overlap; neck remains fully occluded; no visible bone positions inferred','hiddenAnatomy':'inferred/occluded; no visible knees/calves created','frontIdle':'proposed P+2, not source observed' if d=='south' and pose=='idle' else None}
def export(name,ims,ticks=6):
 colors=[];lookup={}
 for _,im in ims:
  for px in im.get_flattened_data():
   if px[3]:
    c='#%02x%02x%02x'%px[:3]
    if c not in lookup:lookup[c]=len(colors)+1;colors.append(c)
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'character','width':32,'height':64,'palette':[None]+colors,'bank':'custom','notes':'HR14 UNAPPROVED. Original identity/materials, observed visible lower-costume coordinates, rigid torso-local bag. No source colored image/palette imported. Hidden anatomy inferred/occluded. FrontGIF100ms/editor6ticks; ROMwalk8ticks per phase via paired4tick frames; GIF quantization documented separately.','frames':[{'name':n,'ticks':ticks,'pixels':[lookup['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in im.get_flattened_data()]} for n,im in ims]}
for kind,views in frames.items():
 (src/f'{kind}-idles.sprite.json').write_text(json.dumps(export('HR14 '+kind+' idles',[(d,views[d]['idle']) for d in directions]),separators=(',',':'))+'\n')
 for d in directions:(src/f'{kind}-{d}-walk.sprite.json').write_text(json.dumps(export('HR14 '+kind+' '+d,[(str(i)+' '+p,views[d][p]) for i,p in enumerate(order)],6 if d=='south' else 4),separators=(',',':'))+'\n')
(src/'construction.json').write_text(json.dumps({'task':'M1.HR14','status':'UNAPPROVED checkpoint','base':'HR13 identity and projection only; rejected legs/pack replaced; HR11 not consumed','canvas':[32,64],'anchor':[16,64],'lowerRows':[54,64],'directions':records,'order':order},separators=(',',':'))+'\n')
print('Authored four directions,32 Hero/dummy poses; rigid canonical pack/strap layers and observed lower construction.')
