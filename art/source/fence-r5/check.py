"""Independent alpha-band and exhaustive joining proof, before adding variants."""
from PIL import Image
from pathlib import Path
import json
OUT=Path(__file__).resolve().parents[3]/'assets/review/fence-r5';m=json.loads((OUT/'atlas.json').read_text());checks=0
styles=sorted({a['id'].split(':')[1] for a in m['assets']})
for style in styles:
 ims={mask:Image.open(OUT/f'{style}-{mask}.png').convert('RGBA') for mask in range(16)}
 for im in ims.values():
  assert im.size==(32,64);assert set(im.getchannel('A').tobytes())<={0,255}
  assert not im.crop((0,0,32,16)).getbbox();assert not im.crop((0,48,32,64)).getbbox();assert im.getbbox()[1]==16 and im.getbbox()[3]==48;checks+=1
 for bit,peerbit,axis in [(2,8,'h'),(4,1,'v')]:
  for mask in range(16):
   for peer in range(16):
    if not(mask&bit and peer&peerbit):continue
    a,b=ims[mask],ims[peer]
    aa=[a.getpixel((31,y)) for y in range(64)] if axis=='h' else [a.getpixel((x,47)) for x in range(32)]
    bb=[b.getpixel((0,y)) for y in range(64)] if axis=='h' else [b.getpixel((x,16)) for x in range(32)]
    assert aa==bb,(style,mask,peer,axis);assert any(p[3] for p in aa);checks+=1
print(json.dumps({'result':'pass','checks':checks,'styles':styles,'frames':len(m['assets']),'paintRows':[16,47]},indent=2))
