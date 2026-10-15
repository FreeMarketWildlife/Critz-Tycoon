"""Compact South/West registered diagnostic; references stay external."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-NB2';src=Path(__file__).parent;ext=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/nb2-small-diagnostic');ext.mkdir(exist_ok=True);meta=json.loads((src/'construction.json').read_text())
def put(p,im,x,y,s=4):
 q=im.resize((im.width*s,im.height*s),Image.Resampling.NEAREST);p.paste(q,(x,y),q if q.mode=='RGBA' else None)
def load(dr,n):return Image.open(out/f'{dr}-idle'/(n+'.png')).convert('RGBA')
def anchor(d,x,y):d.line((x,y+256,x+128,y+256),fill='#748894');d.line((x+61,y+256,x+67,y+256),fill='#ed745c')
for external in (False,True):
 p=Image.new('RGB',(1280,660),'#bed4d5');d=ImageDraw.Draw(p)
 for row,dr in enumerate(('south','west')):
  ref=Image.open(Path('/Users/tanoshi/.codex/visualizations/2026/10/15/hero-hr13-review')/f'ROM-{0 if dr=="south" else 2:02}.png').convert('RGBA')
  old=Image.open(root/f'docs/reviews/M1-HR14/dummy-{dr}-idle.png').convert('RGBA')
  columns=[('PINNED ROM ART0/2' if external else 'OLD MATERIAL MAP',ref if external else old),('NEW NEUTRAL BODY',load(dr,'neutral-body')),('REMOVABLE COSTUME',load(dr,'removable-appearance')),('EXACT DRESSED HERO',load(dr,'recomposed-hero'))]
  for col,(name,im) in enumerate(columns):
   x=col*320;y=row*330;d.text((x+5,y+5),dr+' '+name,fill='#253340');put(p,im,x+12,y+25);anchor(d,x+12,y+25);put(p,im,x+205,y+150,1)
   if col==1:
    # Actual part colors at head/shoulder interface, native geometry/no fitting.
    q=load(dr,'body-torso');q.alpha_composite(load(dr,'body-head'));crop=q.crop((6,38,26,50));put(p,crop,x+174,y+38,5);d.text((x+164,y+105),'head OVER torso',fill='#253340');d.text((x+164,y+122),'actual layer inset',fill='#253340')
  d.text((8,row*330+302),'32x64 fixed frame /16,64 red anchor; native+nearest4x. Under-clothes body contours are authored reconstruction.',fill='#253340')
 p.save((ext if external else out)/('pinned-reference-south-west.png' if external else 'south-west-small-diagnostic.png'))
# Small part-removal views: show actual support, not a composite beauty sheet.
p=Image.new('RGB',(1280,660),'#bed4d5');d=ImageDraw.Draw(p)
for row,dr in enumerate(('south','west')):
 f=out/f'{dr}-idle';e=meta['directions'][dr]['idle'];head=load(dr,'body-head');torso=load(dr,'body-torso');arm=Image.new('RGBA',(32,64));leg=Image.new('RGBA',(32,64))
 for n in ('arm1','hand1','torso','arm0','hand0'):arm.alpha_composite(load(dr,'body-'+n))
 for n in ('leg1','foot1','leg0','foot0','pelvis'):leg.alpha_composite(load(dr,'body-'+n))
 q=torso.copy();q.alpha_composite(head)
 for col,(name,im) in enumerate([('HEAD / TORSO OCCLUSION',q),('ARMS/HANDS / TORSO',arm),('PELVIS / LEGS / FEET',leg),('BODY + SHIRT ONLY',load(dr,'body-plus-shirt'))]):
  x=col*320;y=row*330;d.text((x+4,y+4),dr+' '+name,fill='#253340');put(p,im,x+12,y+25);anchor(d,x+12,y+25);put(p,im,x+205,y+150,1)
p.save(out/'south-west-part-toggle-diagnostic.png')
records={}
for dr in ('south','west'):
 e=meta['directions'][dr]['idle'];pts=lambda n:{tuple(p) for p in e['bodyMasks'][n]};records[dr]={'visibleBodyCells':len(e['actualVisibleBodyCells']),'headTorsoOverlap':len(pts('head')&pts('torso')),'headBrownSupportAdded':e['explicitHeadSurfaceExtension'],'footLegOverlap':e['footLegOverlapCells'],'clippedBodyCells':e['dressingClippedBodyCells']}
# Frozen South prior body/layers stay immutable and byte-exact in this proposal.
compared=[]
for p in (root/'docs/reviews/M1-NB1/south-idle').glob('*.png'):
 q=out/'south-idle'/p.name;assert q.read_bytes()==p.read_bytes(),p.name;compared.append(p.name)
neutral=out/'south-idle/neutral-body.png';assert hashlib.sha256(neutral.read_bytes()).hexdigest()=='92c68cd507ab6b1c9311360e6dd119cd2ce2d87945ed5f0c801b3a617aeba571'
(out/'small-diagnostic-checks.json').write_text(json.dumps({'scope':'SOUTH+WEST IDLE diagnostic first, full pose packaging held','records':records,'southPriorPNGFilesExact':compared,'southNeutralSHA256':hashlib.sha256(neutral.read_bytes()).hexdigest(),'reference':'pret/pokeemerald 5eff78649e7170a877b961ef0b3da13b81a16038 ROM art0/2 exact2x32x64; source-art observation not emulator/bone measurement','externalReferencePlate':str(ext/'pinned-reference-south-west.png'),'visualApproval':False},indent=2)+'\n');print('Compact two-view diagnostic ready. South prior',len(compared),'PNGs exact; profile actual brown support',len(records['west']['headBrownSupportAdded']),'neck/shoulder overlap',records['west']['headTorsoOverlap'])
