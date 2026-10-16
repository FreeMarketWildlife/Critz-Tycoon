"""Independent read-only source phase and Mom inset audit; no artist builders."""
from pathlib import Path
from PIL import Image, ImageColor
import json, hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def guard(n,v):checks.append({'name':n,'pass':bool(v)})
refs=[]
for name,file,expected in [('May','may-walking.png','7f185cda9854f7812545c306795b454dc750be440e582974518ba8a63c9b7e87'),('Birch','prof_birch.png','6618f1249880bd3672c453512351f63b173cb655fb136ceea84fdb2c9cd76c15')]:
 p=ROOT/'local-review/overnight-cast-qa'/file;im=Image.open(p)
 guard(name+' exact pinned source SHA',sha(p)==expected)
 guard(name+' indexed144x32',im.mode=='P' and im.size==(144,32))
 frames=[]
 for i in range(9):
  cells={(x,y) for y in range(32) for x in range(16) if im.getpixel((i*16+x,y))!=0}
  last=max(y for x,y in cells)
  frames.append({'index':i,'lastRow':last,'lastRowXs':[x for x in range(16) if (x,last) in cells]})
 refs.append({'name':name,'revision':'5eff78649e7170a877b961ef0b3da13b81a16038','sha256':sha(p),'frames':frames})
mom=[]
src=ROOT/'art/source/overnight-mom-inset-r1'
for d in ['south','north','west','east']:
 old=ROOT/'docs/reviews/M1-OM2'/('idle-'+d+'.png');new=ROOT/'docs/reviews/M1-OM3'/('idle-'+d+'.png')
 a=Image.open(old).convert('RGBA');b=Image.open(new).convert('RGBA')
 changed=[(x,y) for y in range(64) for x in range(32) if a.getpixel((x,y))!=b.getpixel((x,y))]
 guard('Mom '+d+' whole alpha protected',a.getchannel('A').tobytes()==b.getchannel('A').tobytes())
 guard('Mom '+d+' head0..43 protected',a.crop((0,0,32,44)).tobytes()==b.crop((0,0,32,44)).tobytes())
 guard('Mom '+d+' lower55+ protected',a.crop((0,55,32,64)).tobytes()==b.crop((0,55,32,64)).tobytes())
 if d in ['south','north']:guard('Mom '+d+' byte exact',old.read_bytes()==new.read_bytes())
 o=json.loads((src/d/'layers.json').read_text());comp=Image.new('RGBA',(32,64));owner={}
 for n in o['order']:
  layer=Image.new('RGBA',(32,64))
  for x,y,c in o['layers'][n]:layer.putpixel((x,y),ImageColor.getrgb(c)+(255,));owner[x,y]=n
  lp=src/d/(n+'.png');guard('Mom '+d+'/'+n+' actual cells match PNG',layer.tobytes()==Image.open(lp).convert('RGBA').tobytes())
  if n!='torso':guard('Mom '+d+'/'+n+' frozen OM2 layer',lp.read_bytes()==(ROOT/'art/source/overnight-mom-continuation-r1'/d/(n+'.png')).read_bytes())
  comp=Image.alpha_composite(comp,layer)
 guard('Mom '+d+' actual layers recompose',comp.tobytes()==b.tobytes())
 guard('Mom '+d+' changed only visible torso',all(owner[x,y]=='torso' for x,y in changed))
 mom.append({'direction':d,'file':str(new.relative_to(ROOT)),'sha256':sha(new),'changedCells':changed})
tick=280896/16777216
report={'task':'M1.OVQ3','checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'references':refs,'mom':mom,'timing':{'sourceTickSeconds':tick,'slotTicks':8,'slotMilliseconds':tick*8*1000,'fourSlotLoopMilliseconds':tick*32*1000,'normalGifMilliseconds':[130,140,130,140],'slow4xGifMilliseconds':[540,530,540,530],'gifQuantization':'Four-slot GIF loops540ms and2140ms approximate exact535.7666ms and2143.0664ms; browser exact timeline requires separate actual review.'},'limitations':'Raw source-asset palettes, index0 transparent; no emulator color/timing observation or hidden anatomy claim. Mom remains no-walk pending root.'}
(OUT/'preflight-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'momChanges':[(m['direction'],len(m['changedCells'])) for m in mom]}))
assert not report['failed']
