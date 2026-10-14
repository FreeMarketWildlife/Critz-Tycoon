from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/reviews/M1-HR1'
PAL={'ink':'#242335','hair':'#29252d','hairMid':'#42343a','hairLight':'#655047','skinDark':'#704337','skin':'#a26643','skinLight':'#c58b59','coralDark':'#a64249','coral':'#e66b59','coralLight':'#ff9b75','cream':'#fff0ca','creamShadow':'#c5c2aa','blueDark':'#30384f','blue':'#4a6480','blueLight':'#73939a'}
im=Image.new('RGBA',(32,64)); d=ImageDraw.Draw(im)
masks={}
def poly(name,pts,fill,edge='ink'):
 d.polygon(pts,fill=PAL[fill]); d.line(pts+[pts[0]],fill=PAL[edge],width=1)
 m=Image.new('1',im.size); ImageDraw.Draw(m).polygon(pts,fill=1); masks[name]=m
# Deliberate symmetric body scaffold. All coordinates authored on the target grid.
poly('leftLeg',[(9,53),(14,53),(14,57),(13,59),(8,59),(8,57)],'skin')
poly('rightLeg',[(17,53),(22,53),(23,57),(23,59),(18,59),(17,57)],'skin')
poly('leftShoe',[(8,57),(13,57),(14,59),(14,60),(13,61),(8,61),(7,60),(7,59)],'blueDark')
poly('rightShoe',[(18,57),(23,57),(24,59),(24,60),(23,61),(18,61),(17,60),(17,59)],'blueDark')
d.line([(8,60),(13,60)],fill=PAL['creamShadow']);d.line([(18,60),(23,60)],fill=PAL['creamShadow'])
d.line([(9,58),(12,58)],fill=PAL['cream']);d.line([(19,58),(22,58)],fill=PAL['cream'])
poly('shorts',[(9,50),(22,50),(23,55),(18,56),(16,54),(15,54),(13,56),(8,55)],'blue')
d.polygon([(16,51),(21,51),(22,54),(18,55),(16,53)],fill=PAL['blueDark'])
d.line([(10,52),(13,52)],fill=PAL['blueLight'])
poly('leftArm',[(7,44),(10,46),(9,49),(8,51),(8,53),(6,54),(4,52),(4,49)],'skin')
poly('rightArm',[(24,44),(27,49),(27,52),(25,54),(23,53),(23,51),(22,49),(21,46)],'skin')
d.line([(5,49),(5,51),(6,52)],fill=PAL['skinLight']);d.line([(25,49),(26,51),(25,52)],fill=PAL['skinDark'])
poly('shirt',[(11,42),(20,42),(24,44),(26,47),(23,49),(22,48),(22,51),(9,51),(9,48),(8,49),(5,47),(7,44)],'coral')
d.polygon([(20,44),(23,45),(25,47),(23,48),(22,47),(21,50),(18,50)],fill=PAL['coralDark'])
d.line([(8,45),(10,44)],fill=PAL['coralLight']);d.line([(10,46),(19,46)],fill=PAL['cream']);d.line([(10,47),(19,47)],fill=PAL['cream']);d.line([(10,50),(20,50)],fill=PAL['creamShadow'])
d.line([(9,47),(9,48)],fill=PAL['ink']);d.line([(22,47),(22,48)],fill=PAL['ink'])
poly('neck',[(12,40),(19,40),(19,43),(17,45),(14,45),(12,43)],'skinDark')
d.line([(14,43),(17,43)],fill=PAL['skinLight'])
# Face: cheeks slope into chin, eyes remain paired, ears blunt and close.
poly('face',[(8,31),(23,31),(25,35),(25,38),(23,40),(21,42),(18,43),(13,43),(10,42),(8,40),(6,38),(6,35)],'skin')
d.polygon([(8,33),(12,32),(19,32),(22,34),(22,39),(19,41),(12,41),(9,39)],fill=PAL['skinLight'])
d.polygon([(22,34),(24,35),(24,38),(22,40),(19,42),(13,42),(10,41),(18,41),(21,39)],fill=PAL['skin'])
d.point((7,36),fill=PAL['skinLight']);d.point((24,36),fill=PAL['skinDark'])
for x in (11,19):
 d.line([(x,36),(x+1,36)],fill=PAL['skinDark']);d.rectangle((x,37,x+1,39),fill=PAL['ink']);d.point((x,37),fill=PAL['skinDark'])
d.point((15,40),fill=PAL['skin']);d.line([(14,42),(17,42)],fill=PAL['skinDark'])
# Original sculpted short twists: crown plane and overlapping locks, not stippling.
poly('hair',[(11,21),(17,21),(18,22),(22,22),(22,23),(25,24),(25,26),(27,28),(27,33),(25,36),(23,35),(23,32),(21,34),(19,33),(19,31),(16,33),(14,32),(13,34),(11,33),(10,35),(8,34),(8,36),(5,34),(4,31),(4,28),(6,27),(6,25),(8,24),(8,23),(11,23)],'hair')
d.polygon([(8,26),(10,24),(14,23),(16,24),(14,26),(10,27),(9,30),(7,29)],fill=PAL['hairMid'])
d.polygon([(16,24),(19,24),(21,25),(20,28),(18,30),(16,29)],fill=PAL['hairMid'])
d.polygon([(22,26),(24,27),(25,29),(24,32),(22,31)],fill=PAL['hairMid'])
d.line([(10,25),(12,24),(14,24)],fill=PAL['hairLight'])
d.line([(17,25),(19,25)],fill=PAL['hairLight'])
d.line([(10,29),(11,31),(11,32)],fill=PAL['hairMid'])
d.line([(15,27),(15,30),(14,31)],fill=PAL['ink'])
d.line([(20,28),(20,30),(19,32)],fill=PAL['ink'])
im.save(OUT/'hero-front.png')
# Editable Sprite Editor file, exact indexed pixels.
colors=[None]+list(dict.fromkeys(PAL.values())); rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in colors[1:]]
pixels=[rgba.index(p) for p in im.get_flattened_data()]
source={'format':'fmw-sprite','version':1,'name':'Boy Hero — redesign R1','preset':'character','width':32,'height':64,'palette':colors,'bank':'custom','notes':'M1.HR1 original front idle review. Anchor [16,64]. Not approved or integrated.','frames':[{'name':'South idle','ticks':8,'pixels':pixels}]}
(ROOT/'art/source/hero-redesign-r1/hero-boy.sprite.json').write_text(json.dumps(source,separators=(',',':'))+'\n')
# Required clean before/after and countable full-frame review grid.
old=Image.open(ROOT/'assets/characters/hero-boy-v1/idle-south.png').convert('RGBA')
font=ImageFont.load_default()
plate=Image.new('RGB',(560,420),'#e9e2ca'); p=ImageDraw.Draw(plate)
p.text((30,16),'CURRENT HERO',fill='#292b34',font=font);p.text((290,16),'REDESIGN R1 — REVIEW',fill='#292b34',font=font)
for sprite,x in ((old,62),(im,322)):
 plate.paste(sprite.resize((128,256),Image.Resampling.NEAREST),(x,50),sprite.resize((128,256),Image.Resampling.NEAREST))
 plate.paste(sprite,(x+48,335),sprite)
p.text((32,390),'32 x 64 frames | clean 4x above, native 1x below',fill='#292b34',font=font)
plate.save(OUT/'before-after.png')
grid=Image.new('RGB',(340,590),'#e9e2ca');gd=ImageDraw.Draw(grid); big=im.resize((256,512),Image.Resampling.NEAREST);grid.paste(big,(54,38),big)
for x in range(33):gd.line((54+x*8,38,54+x*8,550),fill='#b9b5a8',width=1)
for row in range(65):gd.line((54,38+row*8,310,38+row*8),fill='#b9b5a8',width=1)
for y in list(range(0,61,10))+[64]:
 yy=550-y*8;gd.line((54,yy,310,yy),fill='#7e827b',width=1);gd.text((22,yy-4),str(y),fill='#292b34')
gd.line((182,38,182,550),fill='#bd5353',width=2);gd.text((55,12),'R1 | 8x | one square = one native pixel',fill='#292b34');gd.text((55,566),'X16 center | Y upward | anchor (16,64)',fill='#292b34');grid.save(OUT/'hero-grid.png')
# Anatomy masks retain hidden scaffold separately from hair/shading.
maskdata={k:[int(v) for v in m.get_flattened_data()] for k,m in masks.items()}
(ROOT/'art/source/hero-redesign-r1/masks.json').write_text(json.dumps(maskdata,separators=(',',':'))+'\n')
used=set(im.get_flattened_data());bbox=im.getbbox()
assert im.size==(32,64) and set(p[3] for p in used)<={0,255}
assert bbox[3]==62 and all(im.getpixel((x,y))[3]==0 for y in (62,63) for x in range(32))
# Exact source-to-export equality and connected silhouette.
assert [rgba[i] for i in pixels]==list(im.get_flattened_data())
pts={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]}
seen={next(iter(pts))};todo=list(seen)
while todo:
 x,y=todo.pop()
 for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
  if q in pts and q not in seen:seen.add(q);todo.append(q)
assert seen==pts
for a,b in [('leftArm','rightArm'),('leftLeg','rightLeg'),('leftShoe','rightShoe')]:
 assert list(masks[a].transpose(Image.Transpose.FLIP_LEFT_RIGHT).get_flattened_data())==list(masks[b].get_flattened_data()),a
for k in ('face','shirt','shorts','neck'):
 assert list(masks[k].get_flattened_data())==list(masks[k].transpose(Image.Transpose.FLIP_LEFT_RIGHT).get_flattened_data()),k
report={'frame':[32,64],'paintedBoundsExclusive':list(bbox),'paintedSize':[bbox[2]-bbox[0],bbox[3]-bbox[1]],'opaqueColors':len(used)-1,'binaryAlpha':True,'sourceEqualsPNG':True,'connectedSilhouette':True,'pairedAnatomyMasks':True,'anchor':[16,64],'approval':'awaiting user review','pngSha256':hashlib.sha256((OUT/'hero-front.png').read_bytes()).hexdigest()}
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
