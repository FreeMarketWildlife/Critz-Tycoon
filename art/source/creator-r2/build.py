"""CC1 BS2-backed registered character creator data. No NB anatomy dependency."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;bs=root/'docs/reviews/M1-BS2';ref=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());meta=json.loads((root/'art/source/hero-bald-shading-r2/changes.json').read_text());palette=[None];lookup={};poses={};records={}
SKIN={(116,69,57,255),(166,104,69,255),(195,138,88,255)};SHOE={(174,69,74,255),(237,116,92,255),(191,192,170,255),(249,237,200,255)}
def encode(im):
 out=[]
 for p in im.get_flattened_data():
  if not p[3]:out.append(0);continue
  c='#%02x%02x%02x'%p[:3]
  if c not in lookup:lookup[c]=len(palette);palette.append(c)
  out.append(lookup[c])
 return out
def pts(im):return [[i%32,i//32] for i,q in enumerate(im.get_flattened_data()) if q[3]]
for dr in ['south','north','west','east']:
 poses[dr]={};records[dr]={}
 for po in ['idle','A','P','C']:
  tag=dr+'-'+po;f=bs/tag;base=Image.open(f/'bald-template.png').convert('RGBA');hair=Image.open(f/'hair-art.png').convert('RGBA');shade=Image.open(f/'hair-dependent-shading.png').convert('RGBA');e=ref['directions'][dr][po]['commonFeatureRegistration'];dy=-2 if po=='P' else 0;protected={tuple(q) for n in ['eyes','ears'] for q in e[n]['cells']}
  # Original close-crop appearance drawn on the accepted scalp surface only.
  # Three existing hair tones, deliberate native clusters; never resample hair.
  crop=Image.new('RGBA',(32,64));limit=(44 if dr=='north' else 36)+dy
  for y in range(27+dy,limit):
   for x in range(32):
    if base.getpixel((x,y)) not in SKIN or (x,y) in protected:continue
    if dr!='north' and y==35+dy and ((x+1)//3)%2==0:continue
    color='#322a31'
    # Connected highlight patches follow one repeatable scalp-relative layout.
    if (9<=x<=14 and 29+dy<=y<=31+dy) or (16<=x<=21 and 32+dy<=y<=33+dy):color='#4c3739'
    if 10<=x<=12 and y==29+dy:color='#705044'
    crop.putpixel((x,y),tuple(bytes.fromhex(color[1:]))+(255,))
  if dr=='east':
   # The fixed scalp is mirrored West; register crop highlights accordingly.
   west=poses['west'][po]['layers']['crop'];q=Image.new('RGBA',(32,64))
   for i,n in enumerate(west):
    if n:q.putpixel((31-i%32,i//32),tuple(bytes.fromhex(palette[n][1:]))+(255,))
   crop=q
  folder=src/tag;folder.mkdir(exist_ok=True);crop.save(folder/'crop-hair.png')
  # Explicit native feature sites remain internal to the existing face surface.
  nose=[] if dr=='north' else [[15,41+dy]] if dr=='south' else [[7,40+dy]] if dr=='west' else [[24,40+dy]]
  mouth=[] if dr=='north' else [[15,43+dy],[16,43+dy]] if dr=='south' else [[10,43+dy]] if dr=='west' else [[21,43+dy]]
  smile=[] if dr=='north' else [[14,42+dy],[15,43+dy],[16,43+dy],[17,42+dy]] if dr=='south' else [[9,42+dy],[10,43+dy]] if dr=='west' else [[22,42+dy],[21,43+dy]]
  for feature in [nose,mouth,smile]:assert all(base.getpixel(tuple(q)) in SKIN for q in feature),(tag,feature)
  shoes=[[i%32,i//32] for i,q in enumerate(base.get_flattened_data()) if i//32>=57 and q in SHOE]
  layers={'base':encode(base),'hair':encode(hair),'hairShade':encode(shade),'crop':encode(crop)}
  poses[dr][po]={'layers':layers,'expected':encode(Image.open(f/'dressed-exact.png').convert('RGBA')),'eyes':e['eyes']['cells'],'ears':e['ears']['cells'],'shoes':shoes,'nose':nose,'mouth':mouth,'smile':smile,'hairHiddenScalp':meta['poses'][dr][po]['selectedHairHiddenScalpCells'],'anchor':[16,64],'dy':dy}
  records[dr][po]={'baseSource':str(f/'bald-template.png'),'baseSHA256':hashlib.sha256((f/'bald-template.png').read_bytes()).hexdigest(),'cropCells':pts(crop),'eyes':e['eyes']['cells'],'ears':e['ears']['cells'],'shoeMaterialCells':shoes,'nose':nose,'mouth':mouth,'smile':smile,'hairDependentSkinShadingCells':pts(shade),'hairHiddenScalp':poses[dr][po]['hairHiddenScalp'],'limits':'Shoe/ear choices preserve exact source silhouettes; source outfit and gait fixed. New crop and optional face marks are original review proposals.'}
data={'task':'M1.CC1','source':'Accepted BS2 da3ec84 / FM2 dressed source; PM1 excluded','width':32,'height':64,'palette':palette,'order':ref['order'],'poses':poses};(root/'character-creator/data.json').write_text(json.dumps(data,separators=(',',':'))+'\n');(src/'registration.json').write_text(json.dumps({'task':'M1.CC1','foundation':'BS2','anatomicalDummyDependency':False,'PM1Included':False,'poses':records},indent=2)+'\n');print('CC1:16 BS2 bases + separate hair/shadow/crop and registered features;',len(palette)-1,'lossless source colors')
