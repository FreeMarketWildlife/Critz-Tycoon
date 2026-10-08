"""Independent Pillow PNG decode vs editable palette source, geometry and hashes."""
from pathlib import Path
from PIL import Image
import json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'assets/review/luke-greenhouse';src=root/'art/source/luke-greenhouse';doc=root/'docs/reviews/M1-LG1'
meta=json.loads((out/'manifest.json').read_text());report={'status':'pass','assets':{}}
for name,expected in meta['assets'].items():
 raw=(root/expected['path']).read_bytes();actual=Image.open(root/expected['path']).convert('RGBA');source=json.loads((src/(name+'.sprite.json')).read_text());assert actual.size==(source['width'],source['height'])==(expected['width'],expected['height'])
 colors=[(0,0,0,0) if c is None else tuple(bytes.fromhex(c[1:]))+(255,) for c in source['palette']]
 decoded=bytes(v for i in source['frames'][0]['pixels'] for v in colors[i]);assert actual.tobytes()==decoded,name+' source mismatch'
 alpha=set(actual.getchannel('A').get_flattened_data());assert alpha<={0,255};digest=hashlib.sha256(raw).hexdigest();assert digest==expected['sha256']
 report['assets'][name]={'size':list(actual.size),'indexedSourceExact':True,'binaryAlpha':True,'pngSHA256':digest}
a=Image.open(out/'silhouettes.png').convert('RGBA');unique=len({a.crop((0,i*32,32,i*32+32)).getchannel('A').tobytes() for i in range(16)});assert unique==16;report['uniqueTopSilhouetteAlphaMasks']=unique
masks=json.loads((src/'luke.masks.json').read_text())['masks'];report['symmetricAnatomyMasks']={}
for k,ids in masks.items():
 mask=set(ids);assert all((i//32)*32+31-i%32 in mask for i in mask);report['symmetricAnatomyMasks'][k]=True
n=Image.open(out/'contact-native.png');large=Image.open(out/'contact-3x.png');assert n.resize(large.size,Image.Resampling.NEAREST).tobytes()==large.tobytes();report['contactExact3x']=True
# Check visible eye positions survive brown cheek beard, not only hidden masks.
luke=Image.open(out/'luke-idle.png').convert('RGBA');blue=(54,180,237,255)
assert all(luke.getpixel((x,y))==blue for x in [12,13,18,19] for y in [37,38]);report['visibleBlueEyeLandmarks']=True
sheet=Image.open(out/'luke.png').convert('RGBA');feet=[]
for row in range(4):
 for col in range(4):
  box=sheet.crop((col*32,row*64,col*32+32,row*64+64)).getbbox();expected=62 if col%2 else 64;assert box[3]==expected,(row,col,box);feet.append(box[3]-1)
report['poseLastPaintedRows']=feet
(doc/'art-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='assets'}))
