"""HR12 bounded native-source edits, preserving delivered HR10 proportions."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,runpy
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR12'
ns=runpy.run_path(str(src/'base-build.py'))
P=ns['P'];order=ns['order'];rgba=ns['rgba'];colors=ns['colors']
frames={};records={};baseMasks=json.loads((src/'masks.json').read_text())
def edit(name,baseline,dy,mirror=False):
 im=baseline.copy();allowed=Image.new('1',(32,64));ad=ImageDraw.Draw(allowed)
 # Source-drawn ear anatomy was paired; final cheek overlap wasn't. Mirror
 # only the visible 3x5 ear and separator, preserving all head alpha/shape.
 for y in range(37+dy,42+dy):
  for x in range(4,7):im.putpixel((31-x,y),baseline.getpixel((x,y)));ad.point((31-x,y),fill=1)
 # Rebuild the side pack from original native shapes in its existing region.
 # Restore the underlying body by reconstructing the same source without
 # its daypack layer; no inferred background colors are painted over it.
 bodyDy=0 if name=='idle' else -2
 if name in ('A','C'):
  code=(src/'base-build.py').read_text()
  start=code.index("  poly('daypackEdge'");end=code.index("  poly('farArm'",start)
  noPackCode=code[:start]+code[end:]
  # Function prefix ends before any exports, safe construction in memory.
  env={'__file__':str(src/'base-build.py')};exec(compile(noPackCode.split('rawP,partsP=')[0],'<same-body-without-pack>','exec'),env)
  raw,_=env['body']('A')
  if mirror:raw=raw.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  raw=ns['translate'](raw,bodyDy)
  # Only replace old pack coverage outside the original head.
  oldPack=baseMasks['poses'][name]['daypackEdge']
  head=ns['accepted']
  for j,on in enumerate(oldPack):
   x,y=j%32,j//32
   if on and not (0<=y-dy<46 and head.getpixel((x,y-dy))[3]):
    im.putpixel((x,y),raw.getpixel((x,y)));ad.point((x,y),fill=1)
  pack=Image.new('RGBA',(32,64));pd=ImageDraw.Draw(pack)
  pts=[(26,44),(27,44),(28,45),(28,48),(27,49),(25,49),(25,45)]
  pd.polygon(pts,fill=P['b']);pd.line(pts+[pts[0]],fill=P['O'])
  pd.line([(26,45),(27,45)],fill=P['B']);pd.line([(26,48),(27,48)],fill=P['n'])
  if mirror:pack=pack.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  # Pack remains behind the established head and front arm/body.
  frontParts=baseMasks['poses'][name]
  hide=set()
  for key in ('hair','face','leftEar','rightEar','jawContact','farArm','nearArm','shirt'):
   hide.update(i for i,v in enumerate(frontParts[key]) if v)
  for j,px in enumerate(pack.get_flattened_data()):
   if px[3] and j not in hide:im.putpixel((j%32,j//32),px);ad.point((j%32,j//32),fill=1)
 # Readable slate shoulder straps, within existing torso/sleeve pixels.
 straps=Image.new('RGBA',(32,64));sd=ImageDraw.Draw(straps)
 if name in ('P','idle'):
  yoff=0 if name=='idle' else -2
  for pts in [[(10,46),(10,48),(11,50)],[(21,46),(21,48),(20,50)]]:
   sd.line([(x,y+yoff) for x,y in pts],fill=P['n']);sd.point((pts[0][0],pts[0][1]+yoff),fill=P['B'])
 else:
  sd.line([(27,45),(26,45),(25,46),(24,46),(22,48),(21,49)],fill=P['n']);sd.point((24,46),fill=P['B'])
  sd.line([(10,47),(11,48),(11,49)],fill=P['b'])
  if mirror:straps=straps.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 for j,px in enumerate(straps.get_flattened_data()):
  if px[3]:
   x,y=j%32,j//32
   # Existing opaque shoulder/chest pixels only; the shoulder strap may cover
   # its bounded upper-arm attachment, never the protected head/face.
   if baseline.getpixel((x,y))[3]:im.putpixel((x,y),px);ad.point((x,y),fill=1)
 if name in ('A','C'):
  x=15 if mirror else 16;im.putpixel((x,60),(0,0,0,0));ad.point((x,60),fill=1)
 records[name]={'allowedEditMask':[int(v) for v in allowed.get_flattened_data()],'changedCells':[(j%32,j//32) for j,(a,b) in enumerate(zip(baseline.get_flattened_data(),im.get_flattened_data())) if a!=b]}
 frames[name]=im;return im
for name,idx,dy in [('A',0,0),('P',2,-2),('C',4,0)]:edit(name,Image.open(root/f'docs/reviews/M1-HR10-BODY/walk-{idx:02}.png').convert('RGBA'),dy,name=='C')
edit('idle',Image.open(root/'docs/reviews/M1-HR10-BODY/idle-forward.png').convert('RGBA'),0)
for i,k in enumerate(order):frames[k].save(out/f'walk-{i:02}.png')
frames['idle'].save(out/'idle-forward.png')
for name,ims in [('walk',[frames[k] for k in order]),('idle',[frames['idle']])]:
 project=json.loads((src/f'hero-forward-{name}.sprite.json').read_text())
 project['name']=f'HR12 delivered-HR10-base Hero {name}';project['notes']='HR12 bounded mirrored-ear layering, compact strapped pack, shoe spur removal. HR10 proportions preserved. No mouth/nose. Review only; anchor16,64.'
 for f,im in zip(project['frames'],ims):f['pixels']=[rgba.index(p) for p in im.get_flattened_data()]
 (src/f'hero-forward-{name}.sprite.json').write_text(json.dumps(project,separators=(',',':'))+'\n')
(out/'bounded-edits.json').write_text(json.dumps(records,indent=2)+'\n')
report=ns['report'];report.update({'baseCommit':'d158c3ecceaddaf1a0919f01ef75eac47f367cc5','baseChoice':'Eutychus explicitly selected latest delivered HR10-BODY; HR11 preserved/unadopted','boundedCorrections':['visible right ear mirrors left ear and dark separator','compact side pack with connected shoulder straps','single-neighbor shoe spur removed'],'headRestyled':False,'bodyProportionsPreserved':True,'approval':'awaiting independent/user visual review'})
(out/'authoring-report.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:len(v['changedCells']) for k,v in records.items()})
