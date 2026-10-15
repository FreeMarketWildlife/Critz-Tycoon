"""CHT1 focused shape-preserving CHARACTER templates, not anatomy."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,argparse
args=argparse.ArgumentParser();args.add_argument('--direction',choices=['south','north','west','east'],default='south');args.add_argument('--pose',choices=['idle','A','P','C'],default='idle');args=args.parse_args();d=args.direction;p=args.pose;dy=-2 if p=='P' else 0
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;review=root/'docs/reviews/M1-CHT1';out=review if (d,p)==('south','idle') else review/f'{d}-{p}';out.mkdir(exist_ok=True);folder=root/f'docs/reviews/M1-NB3/{d}-{p}';tag=f'{d}-{p}';regname='registration.json' if (d,p)==('south','idle') else f'registration-{tag}.json'
hero=Image.open(root/f'docs/reviews/M1-PS1/hero-{tag}.png').convert('RGBA');hair=Image.open(folder/'overlay-hair.png').convert('RGBA')
# Only scalp is newly authored; no prior anatomical dummy part is read.
head=Image.new('RGBA',(32,64));hd=ImageDraw.Draw(head)
contour=[(11,27),(20,27),(23,29),(25,32),(25,36),(26,38),(26,40),(23,42),(21,44),(19,45),(12,45),(10,44),(8,42),(5,40),(5,38),(6,36),(6,32),(8,29)]
if d in ('west','east'):
 # Smooth side scalp has no invented far-ear bulge. Actual profile face/ear
 # pixels from the original character are applied as their separate region.
 contour=[(11,27),(20,27),(23,29),(25,32),(25,38),(23,41),(21,43),(19,45),(12,45),(10,44),(8,42),(6,39),(6,32),(8,29)]
 if d=='east':contour=[(31-x,y) for x,y in contour]
hd.polygon([(x,y+dy) for x,y in contour],fill='#a66845',outline='#242330')
# Existing smooth bald head only. No torso/pelvis/limb/foot anatomy is reused.
# Finished source outfit owns every non-hair silhouette pixel below the head.
template=Image.new('RGBA',(32,64));skin={}
for i,q in enumerate(head.get_flattened_data()):
 if q[3]:
  c='#%02x%02x%02x'%q[:3];c=skin.get(c,c);template.putpixel((i%32,i//32),tuple(bytes.fromhex(c[1:]))+(255,))
regions={};layers={};region_colors={name:None for name in ['shirt','shorts','shoes','pack','straps','skin-face-features']}
for name,color in region_colors.items():
 im=Image.open(folder/f'overlay-{name}.png').convert('RGBA');layers[name]=im;regions[name]=[]
 for i,q in enumerate(im.get_flattened_data()):
  if q[3]:
   x,y=i%32,i//32;regions[name].append([x,y]);template.putpixel((x,y),q)
# The standard template keeps the SAME starter outfit, including every sole,
# cuff, outline and shading pixel. Region masks are independent editable layers;
# color separation does not mean flattening away the character's material cues.
# Bald surface and hair are independent. Source outfit remains exact when
# recolor is off; selected-hair coverage removes only scalp hidden by source.
# Hide only selected-hair scalp outside its actual source silhouette, then
# reapply the actual independent hair layer. No full-Hero overlay is used.
headcoverage=[[i%32,i//32] for i,q in enumerate(head.get_flattened_data()) if q[3] and not hero.getpixel((i%32,i//32))[3]]
dressed=template.copy()
for pt in headcoverage:dressed.putpixel(tuple(pt),(0,0,0,0))
dressed.alpha_composite(hair)
lowerStart=45 if d=='north' and p!='P' else 44
check={}
# Below head, exact all occupied source cells; same waist, contact and shoe size.
for y in range(lowerStart,64):check['exact lower silhouette row '+str(y)]=all(bool(hero.getpixel((x,y))[3])==bool(template.getpixel((x,y))[3]) for x in range(32))
check['below-head RGBA exact']=hero.crop((0,lowerStart,32,64)).tobytes()==template.crop((0,lowerStart,32,64)).tobytes()
check['shoe mask unchanged']=all(template.getpixel(tuple(pt))[3] for pt in regions['shoes'])
check['waist rows51to55 exact']=all(check['exact lower silhouette row '+str(y)] for y in range(51,56))
check['selected dressed source exact']=dressed.tobytes()==hero.tobytes()
assert all(check.values()),check
for n,im in [('hero-'+tag,hero),('template-'+tag,template),('hair-'+tag,hair),('recomposed-'+tag,dressed)]:im.save(out/(n+'.png'))
for name,im in layers.items():im.save(out/('region-'+name+'.png'))
# One still image per editor project; no generated animation or inferred poses.
palette=[None];lookup={};pixels=[]
for q in template.get_flattened_data():
 if not q[3]:pixels.append(0);continue
 c='#%02x%02x%02x'%q[:3]
 if c not in lookup:lookup[c]=len(palette);palette.append(c)
 pixels.append(lookup[c])
project={'format':'fmw-sprite','version':1,'name':'CHT1 '+tag,'preset':'character','width':32,'height':64,'palette':palette,'bank':'custom','notes':'Unapproved character template still. Same selected outfit/waist/full shoes; bald scalp only. Anchor16,64. Not anatomy.','frames':[{'name':tag,'ticks':6,'pixels':pixels}]}
(out/(tag+'.sprite.json')).write_text(json.dumps(project,separators=(',',':'))+'\n')

# Countable original-grid overlay, no interpolated edges or reference fitting.
plate=Image.new('RGB',(1180,550),'#efe9d6');dd=ImageDraw.Draw(plate);dd.fontmode='1'
for j,(name,im) in enumerate([('HERO / '+d.upper()+' '+p.upper(),hero),('CHARACTER TEMPLATE / BALD',template),('ALIGNED SHAPE OVERLAY',template)]):
 x=j*390+20;dd.text((x,12),name,fill='#253340');big=im.resize((256,512),Image.Resampling.NEAREST);plate.paste(big,(x,28),big)
 for y in [44,51,55,58,62]:dd.line((x,28+y*8,x+256,28+y*8),fill='#b29360');dd.text((x+260,28+y*8),str(y),fill='#61563c')
 if j==2:
  # Hero's occupied body cells outlined over template's same grid. Head/hair
  # intentionally differs; lower body coincides at every occupied pixel.
  for y in range(lowerStart,64):
   for xx in range(32):
    if hero.getpixel((xx,y))[3]:dd.rectangle((x+xx*8,28+y*8,x+xx*8+7,28+y*8+7),outline='#e56d4d')
plate.save(out/(tag+'-aligned.png'))
# Lower crop is true native cells with coordinates and material ownership.
crop=Image.new('RGB',(1050,380),'#efe9d6');dd=ImageDraw.Draw(crop)
for j,(name,im) in enumerate([('HERO',hero),('BALD CHARACTER TEMPLATE',template)]):
 x=j*520+30;dd.text((x,5),name,fill='black');q=im.crop((0,44,32,64)).resize((448,280),Image.Resampling.NEAREST);crop.paste(q,(x,40),q)
 for xx in range(33):dd.line((x+xx*14,40,x+xx*14,320),fill='#919a8c')
 for yy in range(21):dd.line((x,40+yy*14,x+448,40+yy*14),fill='#919a8c')
 for yy in range(20):dd.text((x-22,40+yy*14),str(44+yy),fill='#253340')
crop.save(out/(tag+'-lower-grid.png'))
rows={str(y):{'hero':[x for x in range(32) if hero.getpixel((x,y))[3]],'template':[x for x in range(32) if template.getpixel((x,y))[3]]} for y in range(lowerStart,64)}
(src/regname).write_text(json.dumps({'task':'M1.CHT1','scope':'one '+tag+' frame; character template, NOT anatomy','frame':[32,64],'anchor':[16,64],'pose':p,'protectedLowerStartRow':lowerStart,'sourceSlot':[i for i,q in enumerate(['A','A','P','P','C','C','P','P']) if q==p],'regions':regions,'selectedHairHiddenScalpCells':headcoverage,'lowerSilhouetteRows':rows,'sourceHeroSHA256':hashlib.sha256((root/f'docs/reviews/M1-PS1/hero-{tag}.png').read_bytes()).hexdigest(),'checks':check,'approval':False},indent=2)+'\n')
(out/'checks.json').write_text(json.dumps({'pass':True,'checks':check,'approval':False},indent=2)+'\n')
print('CHT1 one-frame template:',len(check),'exact source-shape checks; review pending')
