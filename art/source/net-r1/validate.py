from pathlib import Path
from PIL import Image
import json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'assets/review/net-r1';meta=json.loads((out/'manifest.json').read_text());checks=[]
def check(n,v):
 assert v,n
 checks.append(n)
for name,expected in meta['heroHashes'].items():
 data=(out/name).read_bytes();check(name+' pinned exact bytes',hashlib.sha256(data).hexdigest()==expected);check(name+' 32x64 frame',Image.open(out/name).size==(32,64))
sheet=Image.open(out/'net-sheet.png').convert('RGBA')
for row,d in enumerate(meta['directions']):
 for col,pose in enumerate(meta['poses']):
  tag=f'net-{d}-{pose}';im=Image.open(out/(tag+'.png')).convert('RGBA');check(tag+' frame',im.size==(128,128));check(tag+' binary alpha',set(im.getchannel('A').get_flattened_data())=={0,255});check(tag+' exact sheet cell',im.tobytes()==sheet.crop((col*128,row*128,(col+1)*128,(row+1)*128)).tobytes());bbox=im.getbbox();check(tag+' unclipped native pixels',bbox[0]>0 and bbox[1]>0 and bbox[2]<128 and bbox[3]<128);gx,gy=meta['grips'][d];check(tag+' handle at registered hand',im.getpixel((64+gx,80+gy))[3]==255)
report={'task':'M1.NET1','passed':len(checks),'checks':checks,'visualApproval':False};(root/'docs/reviews/M1-NET1/native-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(checks),'native registration/export checks')
