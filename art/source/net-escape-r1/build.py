"""NET3 original native wing/grass pixels; existing actor rasters remain exact."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
root=Path(__file__).resolve().parents[3];out=root/'assets/review/net-escape-r1';out.mkdir(parents=True,exist_ok=True)
source=root/'assets/review/living-collection-v1/stag-beetle/frame-0.png'
ink='#263138';leaf='#416c43';mid='#6c9b53';light='#a4c879';wing='#c8ceb1';shade='#8aa78d'
for frame in range(4):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 if frame%2==0:
  left=[(4,9),(10,10),(14,17),(10,22),(2,17)];cover=[(7,9),(10,8),(13,19),(9,22),(5,15)]
 else:
  left=[(2,15),(9,12),(14,17),(9,23),(1,23)];cover=[(5,11),(9,9),(13,18),(9,22),(4,18)]
 for mirror in [False,True]:
  poly=lambda points:[(31-x if mirror else x,y) for x,y in points]
  d.polygon(poly(left),fill=wing,outline=ink);d.line(poly([(4,15),(10,16),(13,19)]),fill=shade)
  d.polygon(poly(cover),fill='#536e69',outline=ink)
 body=Image.open(source).convert('RGBA');im.alpha_composite(body);im.save(out/f'beetle-flight-{frame}.png')
for phase,shift in enumerate([0,-2,2]):
 back=Image.new('RGBA',(32,48));front=back.copy();b=ImageDraw.Draw(back);f=ImageDraw.Draw(front)
 # Deliberate leaf clusters; roots stay fixed as tips sway during an escape.
 for i,(x,h) in enumerate([(3,22),(8,31),(13,25),(18,34),(23,27),(28,23)]):
  tip=x+shift;b.polygon([(x-3,43),(tip-2,43-h),(tip+2,42-h+7),(x+4,43)],fill=leaf);b.line([(x,40),(tip,45-h)],fill=mid,width=2)
 for x,h in [(2,14),(7,22),(12,16),(17,23),(22,18),(28,19)]:
  tip=x-shift;f.polygon([(x-3,46),(tip-2,46-h),(tip+1,46-h+5),(x+4,46)],fill=leaf);f.line([(x,43),(tip,48-h)],fill=mid,width=2);f.line([(tip,48-h),(tip,50-h)],fill=light)
 back.save(out/f'grass-back-{phase}.png');front.save(out/f'grass-front-{phase}.png')
prepared={}
for direction in ['down','up','left','right']:
 pose='ready' if direction=='up' else 'windup';original=root/f'assets/review/net-r1/net-{direction}-{pose}.png';dest=out/f'net-prepared-{direction}.png';shutil.copyfile(original,dest);prepared[dest.name]={'source':str(original.relative_to(root)),'sha256':hashlib.sha256(original.read_bytes()).hexdigest()}
manifest={'task':'M1.NET3','approval':'review candidate','flightFrame':[32,32],'grassFrame':[32,48],'grassAnchor':[16,48],'sourceBeetleSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'files':{},'preparedSources':prepared}
for p in sorted(out.glob('*.png')):
 im=Image.open(p).convert('RGBA');assert set(im.getchannel('A').get_flattened_data())=={0,255};manifest['files'][p.name]={'size':list(im.size),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Exported 4 wing frames, 6 grass layers and 4 exact prepared-net registrations.')
