"""Independent native image/connection checks; not visual approval."""
from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
root=Path(__file__).resolve().parents[3];out=root/'assets/review/map-studio-r3'
entries=json.loads((out/'sources.json').read_text());checks=0
for e in entries:
    im=Image.open(out/e['image']).convert('RGBA');assert im.size==(e['w'],e['h']);assert set(im.getchannel('A').tobytes())<={0,255};checks+=1
def ledge(direction,mask):return Image.open(out/f'ledge-{direction}-{mask}.png').convert('RGBA')
for direction in ['down','up']:
    for left in [2,3]:
        for right in [1,3]:
            a,b=ledge(direction,left),ledge(direction,right)
            assert [a.getpixel((31,y)) for y in range(64)]==[b.getpixel((0,y)) for y in range(64)];checks+=1
for direction in ['left','right']:
    for top in [2,3]:
        for bottom in [1,3]:
            a,b=ledge(direction,top),ledge(direction,bottom)
            assert [a.getpixel((x,47)) for x in range(32)]==[b.getpixel((x,16)) for x in range(32)];checks+=1
for direction,bit,other in [('horizontal',2,8),('vertical',4,1)]:
    for mask in range(16):
        if not mask&bit:continue
        for peer in range(16):
            if not peer&other:continue
            a=Image.open(out/f'fence-{mask}.png').convert('RGBA');b=Image.open(out/f'fence-{peer}.png').convert('RGBA')
            if direction=='horizontal':assert [a.getpixel((31,y)) for y in range(64)]==[b.getpixel((0,y)) for y in range(64)]
            else:assert [a.getpixel((x,47)) for x in range(32)]==[b.getpixel((x,16)) for x in range(32)]
            checks+=1
for name,w in [('cottage',160),('garden',160),('shop',224)]:
    im=Image.open(out/f'building-{name}.png').convert('RGBA')
    # One full 32px aperture and readable threshold, with adjacent walls present.
    assert all(im.getpixel((x,140))[:3]==(28,48,46) for x in range(w//2-14,w//2+14))
    assert all(im.getpixel((x,158))[:3]==(213,187,140) for x in range(w//2-16,w//2+16));checks+=1
master=root/'assets/playable/overworld/master.png';before=subprocess.check_output(['git','show','HEAD:assets/playable/overworld/master.png'],cwd=root)
assert before==master.read_bytes();checks+=1
print(json.dumps(dict(checks=checks,nativeSources=len(entries),originalMasterSHA256=hashlib.sha256(before).hexdigest(),result='pass'),indent=2))
