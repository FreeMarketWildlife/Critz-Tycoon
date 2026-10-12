"""Original native fence sprites. Pixel registration is independent of collision."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/review/fence-r5';OUT.mkdir(parents=True,exist_ok=True)
styles=['wood'] if '--wood-only' in sys.argv else ['wood','picket','barbed']
items=[]
for style in styles:
 for mask in range(16):
  im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im);vertical=bool(mask&5)
  dark,body,light={'wood':('#755739','#ac8554','#ddbb7b'),'picket':('#899f93','#e2e6d5','#fff5dc'),'barbed':('#596b68','#98aaa2','#d4d9bf')}[style]
  # Rails at both heights reach adjoining horizontal metatiles exactly.
  for yy in [27,39]:
   if mask&8:d.rectangle((0,yy,15,yy+(1 if style=='barbed' else 3)),fill=body);d.line((0,yy,15,yy),fill=light)
   if mask&2:d.rectangle((16,yy,31,yy+(1 if style=='barbed' else 3)),fill=body);d.line((16,yy,31,yy),fill=light)
  # Continuous perspective rails, without per-tile caps or disconnected stubs.
  for xx in [10,21]:
   if vertical:d.rectangle((xx,16,xx+(1 if style=='barbed' else 2),47),fill=body);d.line((xx,16,xx,47),fill=light)
  if vertical:
   if not mask&1:d.line((10,16,23,16),fill=light)
   if not mask&4:d.line((10,47,23,47),fill=body)
  if vertical and style!='barbed':
   for yy in [28,40]:d.rectangle((10,yy,23,yy+2),fill=body);d.line((10,yy,23,yy),fill=light)
  def post(cx,top,bottom):
   if style=='picket':
    d.polygon([(cx,top),(cx+3,top+4),(cx+3,bottom),(cx-3,bottom),(cx-3,top+4)],fill=dark)
    d.polygon([(cx,top+1),(cx+2,top+4),(cx+2,bottom-1),(cx-2,bottom-1),(cx-2,top+4)],fill=body);d.line((cx-1,top+4,cx-1,bottom-1),fill=light)
   else:
    d.rectangle((cx-2,top,cx+3,bottom),fill='#786147' if style=='barbed' else dark);d.rectangle((cx-1,top+2,cx+2,bottom-1),fill='#a79773' if style=='barbed' else body);d.line((cx-1,top+2,cx-1,bottom-1),fill='#d0bd92' if style=='barbed' else light);d.rectangle((cx-2,top,cx+3,top+2),fill=light)
  post(16,20 if vertical else 16,44 if vertical else 47)
  if style=='picket':
   if mask&8:post(6,18,46)
   if mask&2:post(26,18,46)
  if style=='barbed':
   for xx in [6,26]:
    if (xx<16 and mask&8) or (xx>16 and mask&2):
     for yy in [27,39]:d.line((xx-2,yy-2,xx+2,yy+2),fill=dark);d.line((xx-2,yy+2,xx+2,yy-2),fill=light)
   for yy in [24,40]:
    if (yy<32 and mask&1) or (yy>=32 and mask&4):
     for xx in [10,21]:d.line((xx-2,yy-2,xx+2,yy+2),fill=dark);d.line((xx-2,yy+2,xx+2,yy-2),fill=light)
  name=f'{style}-{mask}.png';im.save(OUT/name);items.append({'id':f'fence:{style}:{mask}','image':name,'rect':[mask*32,styles.index(style)*64,32,64],'registered':True,'paintRows':[16,47]})
# No sprite reanchoring/contact compilation: exact two-cell frames.
atlas=Image.new('RGBA',(512,64*len(styles)))
for a in items:atlas.paste(Image.open(OUT/a['image']),a['rect'][:2])
atlas.save(OUT/'atlas.png');(OUT/'atlas.json').write_text(json.dumps({'image':'atlas.png','tileSize':32,'assets':items,'approval':'M1.ME5 user-directed fence revision; appearance awaits feedback'},indent=2)+'\n')
print(f'{len(items)} original fence frames')
