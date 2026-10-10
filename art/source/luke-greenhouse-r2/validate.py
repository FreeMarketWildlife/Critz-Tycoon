"""Independent native PNG/index verification; preserve prior collection hashes."""
from PIL import Image,ImageOps
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'assets/review/luke-greenhouse-r2';src=root/'art/source/luke-greenhouse-r2';doc=root/'docs/reviews/M1-LG2'
m=json.loads((out/'manifest.json').read_text());report={'status':'pass','assets':{}}
for name,e in m['assets'].items():
 a=Image.open(root/e['path']).convert('RGBA');s=json.loads((src/(name+'.sprite.json')).read_text());assert a.size==(s['width'],s['height'])==(e['width'],e['height'])
 pal=[(0,0,0,0) if c is None else tuple(bytes.fromhex(c[1:]))+(255,) for c in s['palette']]
 rgba=bytes(v for n in s['frames'][0]['pixels'] for v in pal[n]);assert a.tobytes()==rgba,name
 assert set(a.getchannel('A').get_flattened_data())<={0,255};digest=hashlib.sha256((root/e['path']).read_bytes()).hexdigest();assert digest==e['sha256']
 report['assets'][name]={'size':a.size,'rgbaMatchesIndexedSource':True,'binaryAlpha':True,'sha256':digest}
for n in ['equipment','inlet','wall-riser']:
 a=Image.open(out/(n+'-left.png'));b=Image.open(out/(n+'-right.png'));assert ImageOps.mirror(a).tobytes()==b.tobytes()
report['threeEquipmentPairsExactMirrors']=True
h=Image.open(out/'header.png');assert h.tobytes()==ImageOps.mirror(h).tobytes();report['headerExactMirrorAxis208']=True
g=Image.open(out/'greenhouse.png').convert('RGBA');assert g.getchannel('A').tobytes()==ImageOps.mirror(g.getchannel('A')).tobytes();report['facadeAlphaSymmetryAxis160']=True
# Exclude original fish sign and practical right-hand door latch from RGB symmetry.
mask=g.copy();d=__import__('PIL.ImageDraw',fromlist=['Draw']).Draw(mask);d.rectangle((112,84,207,105),fill=(0,0,0,0));d.rectangle((144,111,175,174),fill=(0,0,0,0));assert mask.tobytes()==ImageOps.mirror(mask).tobytes();report['facadeArchitectureRGBSymmetry']=True
for n,expected in m['sourceFrozenHashes'].items():assert hashlib.sha256((root/'assets/review/luke-greenhouse'/n).read_bytes()).hexdigest()==expected,n
report['oldCollectionFilesUnchanged']=len(m['sourceFrozenHashes'])
a=Image.open(out/'contact-native.png');b=Image.open(doc/'art-contact-3x.png');assert a.resize(b.size,Image.Resampling.NEAREST).tobytes()==b.tobytes();report['contactExact3x']=True
(doc/'art-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='assets'}))
