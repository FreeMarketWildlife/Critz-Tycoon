"""GH1 ONE front idle review. Original C6Girl head + declared HR14body adaptation.
No generated concept raster or reference-game pixels enter authoring inputs.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-GH1'
old=json.loads((root/'art/source/idle-collection-v1/hero-girl.sprite.json').read_text());parts=json.loads((root/'art/source/idle-collection-v1/hero-girl.masks.json').read_text());mparts=parts['visibleParts']
colors=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in old['palette'][1:]];original=Image.new('RGBA',(32,64));original.putdata([colors[v] for v in old['frames'][0]['pixels']])
P={'ink':'#201008','skin':'#a87038','light':'#c48e4a','shade':'#784820','coral':'#fa8078','shirtShade':'#c95662','cream':'#f7edcc','blue':'#184080','dark':'#11111a','shoe':'#80394e'}
def rgba(c):return tuple(bytes.fromhex(c[1:]))+(255,)
def blank():return Image.new('RGBA',(32,64))
def bits(im):return [int(px[3]>0) for px in im.get_flattened_data()]
def frompoints(points):
 im=Image.new('L',(32,64));d=ImageDraw.Draw(im)
 for x,y in points:d.point((x,y),fill=255)
 return im
head=blank();headParts={'skull','hair','eyes','accessory'}
for i,k in enumerate(mparts):
 if k in headParts and i//32<=44:head.putpixel((i%32,i//32),original.getpixel((i%32,i//32)))
# Keep existing twinpuffs/ties/fringe/eyes/face; bounded final-ear composite only.
earOverride={(x,y) for y in range(37,42) for x in (3,4,5,6,25,26,27,28)}
for x,y in earOverride:head.putpixel((x,y),(0,0,0,0))
earPattern=[[None,'ink','ink'],['ink','light','skin'],['ink','skin','skin'],['ink','skin','shade'],[None,'ink','shade']];ears=[]
for iy,row in enumerate(earPattern):
 for ix,key in enumerate(row):
  if key:
   x=4+ix;y=37+iy;px=rgba(P[key]);head.putpixel((x,y),px);head.putpixel((31-x,y),px);ears.extend([(x,y),(31-x,y)])
# Native owned body pixels from frozen/tested HR14; no bag/straps are added.
base=root/'docs/reviews/M1-HR14/body-layer-south-idle.png';body0=Image.open(base).convert('RGBA');body=blank()
recolor={'#242330':P['ink'],'#322a31':P['dark'],'#4c3739':P['dark'],'#705044':P['dark'],'#a66845':P['skin'],'#c38a58':P['light'],'#744539':P['shade'],'#ed745c':P['coral'],'#ffad7a':P['coral'],'#ae454a':P['shirtShade'],'#f9edc8':P['cream'],'#bfc0aa':P['cream'],'#465671':P['blue'],'#748894':P['blue'],'#2a344a':P['dark']}
for y in range(64):
 for x in range(32):
  px=body0.getpixel((x,y))
  if px[3]:
   key='#%02x%02x%02x'%px[:3];col=recolor[key]
   if y>=54 and key=='#2a344a':col=P['blue']
   body.putpixel((x,y),rgba(col))
# Existing source-observed colored near-sole material sites become the selected
# Girl's burgundy footwear. Dark connecting costume is NOT exposed leg anatomy.
hr14=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());sem=hr14['directions']['south']['idle']['visibleMaterialPlanes'];shoe=[];pale=[]
for name,points in sem.items():
 for x,y in points:
  if 57<=y<=59 and name in ('slateShadow','slateLight','warmGray','coral'):
   if body0.getpixel((x,y))[:3]!=(36,35,48):body.putpixel((x,y),rgba(P['shirtShade'] if name in ('warmGray','coral') else P['shoe']));shoe.append((x,y))
  if name=='paleBand':pale.append((x,y))
# Dark inset accents inside the visible colored shoe clusters, not a hidden joint.
for x,y in [(10,59),(13,59),(18,59),(21,59)]:
 if body0.getpixel((x,y))[3] and body0.getpixel((x,y))[:3]==(42,52,74):body.putpixel((x,y),rgba(P['shoe']));shoe.append((x,y))
hero=Image.alpha_composite(body,head)
# A color-coded construction map. Hair is a separate material, NOT skull/bone.
C={'ink':'#253340','head':'#b8dce0','hair':'#9b83d4','ties':'#ed8c9c','ear':'#ed8ccd','eyes':'#253340','torso':'#4ac2b0','hands':'#ffd4a1','darkPlane':'#465671','slateShadow':'#9b83d4','slateLight':'#65a6de','warmGray':'#a6d8e2','coral':'#de8b67','paleBand':'#f1d171','shoe':'#de8b67'}
dummy=blank();at={tuple(pt):name for name,pts in sem.items() for pt in pts}
for y in range(64):
 for x in range(32):
  px=body.getpixel((x,y))
  if not px[3]:continue
  name=at.get((x,y));col=C['ink'] if px[:3]==rgba(P['ink'])[:3] else C['hands'] if px[:3] in [rgba(P[k])[:3] for k in ('skin','light','shade')] else C['shoe'] if (x,y) in shoe else C[name] if name else C['torso'];dummy.putpixel((x,y),rgba(col))
headMask=bits(head);hair=[];ties=[];eyes=[(i%32,i//32) for i in parts['masks']['eyes']];puffs=set()
for x0 in (3,19):
 for y in range(21,31):
  for x in range(x0,x0+10):
   if head.getpixel((x,y))[3] and mparts[y*32+x]=='hair':puffs.add((x,y))
for y in range(45):
 for x in range(32):
  px=head.getpixel((x,y));i=y*32+x
  if not px[3]:continue
  if (x,y) in ears:col=C['ink'] if px[:3]==rgba(P['ink'])[:3] else C['ear']
  elif (x,y) in eyes:col=C['eyes']
  elif mparts[i]=='hair':
   isTie=y<=32 and px[:3] in [rgba(P[k])[:3] for k in ('coral','shirtShade')];col=C['ties'] if isTie else C['ink'] if px[:3]==rgba(P['ink'])[:3] else C['hair']
   if isTie:ties.append((x,y))
   else:hair.append((x,y))
  else:col=C['head'] if px[:3]!=rgba(P['ink'])[:3] else C['ink']
  dummy.putpixel((x,y),rgba(col))
puffs.difference_update(ties)
# The inherited head is clipped before the old neck/collar rows.
for k,im in [('girl-front-idle',hero),('girl-front-construction',dummy),('head-layer',head),('body-layer',body)]:im.save(out/f'{k}.png')
def project(name,im):
 pal=[None];look={}
 for px in im.get_flattened_data():
  if px[3]:
   c='#%02x%02x%02x'%px[:3]
   if c not in look:look[c]=len(pal);pal.append(c)
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'character','width':32,'height':64,'palette':pal,'bank':'custom','notes':'M1.GH1 front idle ONLY, UNAPPROVED. C6Girl originalhead/puffs/ties, bounded roundedmirroredears; HR14body is DECLARED shared visualconstructionadaptation, not hidden anatomy. Girlburgundyshoe material restored; no bag added. No runtime replacement.','frames':[{'name':'Proposed front idle','ticks':8,'pixels':[look['#%02x%02x%02x'%px[:3]] if px[3] else 0 for px in im.get_flattened_data()]}]}
for name,im in [('girl-front-idle',hero),('girl-front-construction',dummy)]:(src/f'{name}.sprite.json').write_text(json.dumps(project('GH1 '+name,im),separators=(',',':'))+'\n')
hand=[(x,y) for y in range(47,64) for x in range(32) if hero.getpixel((x,y))[3] and hero.getpixel((x,y))[:3] in [rgba(P[k])[:3] for k in ('skin','light','shade')]]
meta={'task':'M1.GH1','state':'ONE front idle candidate, UNAPPROVED; no otherviews/walks','canvas':[32,64],'edgeAnchor':[16,64],'identityBase':'R11conceptdesignonly -> C6native/C7samefront; separateG1v3NOTused','sources':{'girlC6':str(root/'art/source/idle-collection-v1/hero-girl.sprite.json'),'girlC6SHA256':hashlib.sha256((root/'art/source/idle-collection-v1/hero-girl.sprite.json').read_bytes()).hexdigest(),'bodyHR14':str(base),'bodyHR14SHA256':hashlib.sha256(base.read_bytes()).hexdigest(),'frozenBodyCommit':'c98a8cb'},'adaptation':'ExistingHR14frontpassing-derivedidle body/material/registration as declaredsharedvisualconstruction; not girl-specific referenceangle/gait or accepted hidden anatomy. No narrower/taller gendered body.','headCutoff':44,'excludedLegacyNeckCollarRows':[45,46],'headMask':headMask,'hairMask':[int((i%32,i//32) in hair) for i in range(2048)],'puffMask':[int((i%32,i//32) in puffs) for i in range(2048)],'tieMask':[int((i%32,i//32) in ties) for i in range(2048)],'inheritedSkullScaffoldMask':[int(i in parts['masks']['skull']) for i in range(2048)],'skullMeaning':'Inherited C6 authored scaffold, NOT observed hidden skull/bones; hidden geometry unresolved','earOverrideAllowed':[list(p) for p in sorted(earOverride)],'earCells':[list(p) for p in ears],'eyeCells':[list(p) for p in eyes],'handCells':[list(p) for p in hand],'burgundyMaterialCells':[list(p) for p in sorted(set(shoe))],'paleBandCells':[list(p) for p in pale],'noMouthNoseMasks':True,'hiddenJoints':{k:None for k in ('neck','hip','knee','ankle','anatomicalFoot')},'bodyMaterialPlanes':sem}
(src/'construction.json').write_text(json.dumps(meta,separators=(',',':'))+'\n');print('Created ONE original Girl front-idle review source/candidate. Colors:',len({p for p in hero.get_flattened_data() if p[3]}),'bounds',hero.getbbox())
