"""Prepare ignored LOCAL-ONLY input for the existing Sprite Editor's body-region mode.
Requires Pillow; never modifies artwork. local-review/ is excluded from normal build.
"""
from pathlib import Path
from PIL import Image
import argparse,hashlib,json,subprocess
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--reference',type=Path,default=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/brendan-user-reference-original/01agijgmbz561.gif'));args=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest()
reference=args.reference;reference_sha='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e'
assert sha(reference.read_bytes())==reference_sha,'Use the exact supplied fan-made reference GIF.'
g=Image.open(reference);assert g.size==(256,192) and g.n_frames==8;g.seek(2);left=g.convert('RGBA').crop((0,0,128,192));native=left.resize((32,48),Image.Resampling.NEAREST);assert native.resize((128,192),Image.Resampling.NEAREST).tobytes()==left.tobytes();registered=Image.new('RGBA',(32,64));registered.alpha_composite(native,(0,16))
dummy_path=R/'docs/reviews/M1-RD1/reference-derived-dummy.png';dummy_bytes=dummy_path.read_bytes();assert sha(dummy_bytes)=='606a6305a9a3bc9473a8cf6314ad86188627b6e107cfbaa97ff7e0d9a64100f8';dummy=Image.open(dummy_path).convert('RGBA');seg_path=R/'art/source/reference-dummy-r1/construction.json';seg_bytes=seg_path.read_bytes();seg=json.loads(seg_bytes)
parts=[(0,'Unassigned','#273440'),(1,'Head','#c29e5c'),(2,'Ears','#ee9c7a'),(3,'Eyes','#fcf1d9'),(4,'Torso','#4477aa'),(5,'Pelvis','#009988'),(6,'Left arm','#66ccee'),(7,'Right arm','#aa3377'),(8,'Left hand','#ee7733'),(9,'Right hand','#ccbb44'),(10,'Left leg','#228833'),(11,'Right leg','#cc6677'),(12,'Left shoe','#bbbbbb'),(13,'Right shoe','#7744aa')]
labels=[0]*2048
for name,rec in seg['regions'].items():
 for x,y in rec['cells']:
  screen_right=x>=16
  if name in ['head','ears','torso','pelvis']:part={'head':1,'ears':2,'torso':4,'pelvis':5}[name]
  elif name=='arms':part=6 if screen_right else 7
  elif name=='hands':part=8 if screen_right else 9
  elif name.endswith('leg'):part=10 if screen_right else 11
  elif name.endswith('shoe'):part=12 if screen_right else 13
  else:raise ValueError('Unknown RD1 part '+name)
  index=y*32+x;assert labels[index]==0;labels[index]=part
for x,y in seg['eyes']['cells']:labels[y*32+x]=3
assert all(bool(v)==bool(dummy.getpixel((i%32,i//32))[3]) for i,v in enumerate(labels));assert sum(v!=0 for v in labels)==sum(p[3]>0 for p in dummy.get_flattened_data());assert sum(v==3 for v in labels)==16
registration={'crop':[0,0,128,192],'displayDivisor':4,'native':[32,48],'translation':[0,16],'centerlineX':15.5,'contactEdgeY':62,'facing':'front','leftRight':'character-relative; left is screen-right'}
seed={'schema':'critz.body-regions.seed','version':1,'seedId':'RD1-source-a25379d-frame2-v1','width':32,'height':64,'source':{'reference':{'id':'fan-brendan-01agijgmbz561-frame2','url':'https://i.redd.it/01agijgmbz561.gif','gifSha256':reference_sha,'frame':2},'dummy':{'id':'RD1-front','commit':'a25379df5c76fc1d4bf88c02525aef5affa4781c','sha256':sha(dummy_bytes)},'segmentation':{'id':'RD1-regions','sha256':sha(seg_bytes)}},'registration':registration,'parts':[{'id':i,'name':n,'color':c} for i,n,c in parts],'referenceRGBA':list(registered.tobytes()),'dummyRGBA':list(dummy.tobytes()),'labels':labels}
out=R/'local-review';out.mkdir(exist_ok=True);target=out/'body-regions-seed.json';target.write_text(json.dumps(seed,separators=(',',':'))+'\n');assert dummy_path.read_bytes()==dummy_bytes
# Production builder's explicit top-level copy list omits local-review. Keep it
# ignored in Git as well, so local supplied reference bytes cannot be staged.
assert '"local-review"' not in (R/'scripts/build.mjs').read_text()
print(json.dumps({'path':str(target),'bytes':target.stat().st_size,'seedSHA256':sha(target.read_bytes()),'dimensions':[32,64],'labels':len(labels),'sourcePixels45plus':sum(1 for i,v in enumerate(labels) if v and i//32>=45),'characterLeftIsScreenRight':True,'artworkUnchanged':True,'excludedFromProductionBuild':True}))
