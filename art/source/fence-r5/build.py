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
  # A north/south run shows one narrow side plane, not a ladder of
  # two widely separated rails and repeated cross-rungs.
  if vertical:
   if style=='barbed':
    d.line((16,16,16,47),fill=body);d.line((17,16,17,47),fill=light)
   else:
    d.rectangle((13,16,20,47),fill=dark)
    d.rectangle((14,16,17,47),fill=body)
    d.line((14,16,14,47),fill=light)
    d.line((18,16,18,47),fill=body)
    if style=='picket':
     for yy in [21,37]:
      d.polygon([(12,yy),(14,yy-3),(16,yy),(16,yy+6),(12,yy+6)],fill=body)
      d.line((13,yy,13,yy+5),fill=light)
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
   for yy in [22,38]:
    if (yy<32 and mask&1) or (yy>=32 and mask&4):
     for xx in [16]:d.line((xx-2,yy-2,xx+2,yy+2),fill=dark);d.line((xx-2,yy+2,xx+2,yy-2),fill=light)
  name=f'{style}-{mask}.png';im.save(OUT/name);items.append({'id':f'fence:{style}:{mask}','image':name,'rect':[mask*32,styles.index(style)*64,32,64],'registered':True,'paintRows':[16,47]})
# No sprite reanchoring/contact compilation: exact two-cell frames.
atlas=Image.new('RGBA',(512,64*len(styles)))
for a in items:atlas.paste(Image.open(OUT/a['image']),a['rect'][:2])
atlas.save(OUT/'atlas.png');(OUT/'atlas.json').write_text(json.dumps({'image':'atlas.png','tileSize':32,'assets':items,'approval':'M1.ME5 user-directed fence revision; appearance awaits feedback'},indent=2)+'\n')
print(f'{len(items)} original fence frames')
