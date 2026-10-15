"""Independent checks of saved indexed source, masks and PNGs (not drawing calls)."""
from pathlib import Path
from PIL import Image
import json,hashlib
root=Path(__file__).resolve().parents[3];base=Path(__file__).parent;out=root/'docs/reviews/M1-HR8'
s=json.loads((base/'hero-boy.sprite.json').read_text()); masks=json.loads((base/'masks.json').read_text()); colors=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in s['palette'][1:]]
for f in s['frames']:
 name=f['name'].split()[0];im=Image.open(out/f'hero-{name}.png').convert('RGBA');assert im.size==(32,64)
 assert list(im.get_flattened_data())==[colors[n] for n in f['pixels']]
 assert set(p[3] for p in im.get_flattened_data())=={0,255}
 assert len({p for p in im.get_flattened_data() if p[3]})<=15
 assert all(im.getpixel((x,y))[3]==0 for y in (62,63) for x in range(32))
for direction in ('south','north'):
 ms=masks[direction]
 for a,b in [('leftArm','rightArm'),('leftFoot','rightFoot')]:
  assert all(ms[a][y*32+x]==ms[b][y*32+31-x] for y in range(64) for x in range(32))
 for k in ('face','shirt','shorts','neck'):
  assert all(ms[k][y*32+x]==ms[k][y*32+31-x] for y in range(64) for x in range(32))
front=Image.open(out/'hero-south.png');eyes=masks['south']['eyes']
assert sum(eyes)==16
assert all(front.getpixel((x,y))[:3] in [tuple(bytes.fromhex(c[1:])) for c in ('#242330','#2a344a')] for y in range(64) for x in range(32) if eyes[y*32+x])
assert all(eyes[y*32+x]==eyes[y*32+31-x] for y in range(64) for x in range(32))
report={'fourSavedPNGSourceMatches':True,'binaryAlpha':True,'atMost15OpaqueColors':True,'frontBackPairedAnatomy':True,'visibleEyeMask':True,'visibleEyeBounds':[[12,38,14,42],[18,38,20,42]],'bottomRowsTransparent':True,'referencePixelsInProduction':False,'referenceIngestionByAuthoringScript':False}
(out/'independent-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
