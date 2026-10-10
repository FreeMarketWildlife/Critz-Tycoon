"""Independent native-pixel checks for the M1.CT1 review assets (requires Pillow)."""
from pathlib import Path
from PIL import Image
import json, hashlib
root=Path(__file__).resolve().parents[1]
p=root/'assets/review/contact-lab'
m=json.loads((p/'manifest.json').read_text())
source=root/'assets/playable/overworld/master.png'
assert hashlib.sha256(source.read_bytes()).hexdigest()==m['sourceMasterSHA256']
master=Image.open(source).convert('RGBA')
meta=json.loads(source.with_suffix('.json').read_text())
tiles={t['id']:t for t in meta['tiles']}
house=Image.new('RGBA',(160,160))
for y,row in enumerate(meta['assemblies']['house.cottage']):
 for x,key in enumerate(row):
  t=tiles[key];house.alpha_composite(master.crop((t['x'],t['y'],t['x']+32,t['y']+32)),(x*32,y*32))
sheet=Image.open(p/'transitions.png').convert('RGBA')
assert sheet.size==(160,1536)
for row,a in enumerate(m['assets']):
 im=Image.open(p/a['image']).convert('RGBA');cut=a['materialRows'];base=a['baseRow'];surface=a['id'].split('-')[1]
 g=Image.open(p/f'ground-{surface}.png').convert('RGBA')
 assert im.size==tuple(a['size'])
 assert set(im.getchannel('A').getdata())<={0,255}
 assert im.crop((0,0,160,cut)).getbbox() is None
 for x in range(5):
  assert im.crop((x*32,base+cut,x*32+32,base+32)).tobytes()==g.crop((0,cut,32,32)).tobytes()
 assert sheet.crop((0,row*32,160,(row+1)*32)).tobytes()==im.crop((0,base,160,base+32)).tobytes()
 if a['id'].startswith('house-'):
  actual=im.crop((0,cut,160,cut+160))
  # Ground beneath transparent source pixels is deliberate; every opaque house pixel is exact.
  for expected,got in zip(house.getdata(),actual.getdata()):
   if expected[3]:assert expected==got
for a in m['assets']:
 station,surface,option=a['id'].split('-')
 actual=Image.open(p/a['image']).convert('RGBA').crop((0,a['materialRows'],160,a['materialRows']+a['baseRow']-28))
 reference=Image.open(p/f'{station}-{surface}-A.png').convert('RGBA').crop((0,8,160,8+a['baseRow']-28))
 assert actual.tobytes()==reference.tobytes()
hero_path=root/'assets/playable/living'
hero_meta=json.loads((hero_path/'atlas.json').read_text())
hero=Image.open(hero_path/hero_meta['image']).convert('RGBA')
frames=[a for a in hero_meta['assets'] if a['id'].startswith('hero-boy.')]
assert len(frames)==16
for a in frames:
 x,y,w,h=a['rect'];bounds=hero.crop((x,y+h-8,x+w,y+h)).getbbox()
 assert bounds and bounds[0]>=5 and bounds[2]<=27,(a['id'],bounds)
print(json.dumps({'passed':True,'assemblies':48,'transition_cells':240,'checks':['source master SHA matches','native dimensions and binary alpha','transparent top padding','exact ground bands for all four surfaces','sheet cells equal fixture transition rows','all opaque original house pixels preserved','structure translations retain native pixels across A–D','all 16 Hero lower-foot bands fit the 22×8 collision footprint']},indent=2))
