"""Original Critz pixels, manually authored on 32x64 grid; no reference-image input.
Optional reference comparisons are produced by a separate read-only analysis script.
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'docs/reviews/M1-HR7'
P={'O':'#242330','h':'#322a31','m':'#4c3739','l':'#705044','s':'#a66845','S':'#c38a58','d':'#744539','r':'#ed745c','R':'#ffad7a','v':'#ae454a','c':'#f9edc8','C':'#bfc0aa','b':'#465671','B':'#748894','n':'#2a344a','t':'#748894'}
frames={}; masks={}
def start(name):
 global im,d,parts
 im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im);parts={'mouth':Image.new('1',im.size),'nose':Image.new('1',im.size)};frames[name]=im;masks[name]=parts

def shape(name,pts,c,edge='O'):
 d.polygon(pts,fill=P[c]);d.line(pts+[pts[0]],fill=P[edge],width=1)
 m=Image.new('1',im.size);ImageDraw.Draw(m).polygon(pts,fill=1);parts[name]=m

def line(pts,c):d.line(pts,fill=P[c],width=1)
def fill(pts,c):d.polygon(pts,fill=P[c])
def rect(box,c):d.rectangle(box,fill=P[c])
def dot(x,y,c):d.point((x,y),fill=P[c])
# Original front anatomy. Reference guides: eyes38-41, jaw44-45, shoulder46,
# arm/hand46-53, central torso46-55, foot contact61. No source mask copying.
start('south')
# Straight, compact sneakers. No bright sole rails or splayed toes.
shape('leftFoot',[(9,57),(13,57),(13,60),(12,61),(8,61),(8,59)],'n')
shape('rightFoot',[(22,57),(18,57),(18,60),(19,61),(23,61),(23,59)],'n')
line([(9,59),(10,59)],'B');line([(21,59),(22,59)],'b')
shape('shorts',[(10,54),(21,54),(22,57),(18,58),(16,56),(15,56),(13,58),(9,57)],'b')
fill([(16,55),(20,55),(21,57),(18,57),(16,56)],'n')
# Relaxed forearms descend from short sleeves, separate from the torso.
shape('leftArm',[(5,48),(8,48),(9,50),(8,54),(6,55),(4,53),(4,50)],'s')
shape('rightArm',[(26,48),(23,48),(22,50),(23,54),(25,55),(27,53),(27,50)],'s')
line([(5,50),(5,52),(6,53)],'S');line([(25,51),(25,53)],'d')
shape('shirt',[(10,46),(21,46),(24,47),(26,48),(25,50),(22,50),(22,54),(20,55),(11,55),(9,54),(9,50),(6,50),(5,48),(7,47)],'r')
fill([(7,47),(9,47),(9,49),(6,49),(6,48)],'c')
fill([(22,47),(24,47),(25,48),(25,49),(22,49)],'C')
# Same cream inset panel and coral side panels, fitted to upright torso.
fill([(13,47),(18,47),(20,48),(19,50),(12,50),(11,48)],'c')
line([(13,50),(18,50)],'C')
fill([(20,48),(21,49),(21,53),(19,54),(17,54),(18,52),(20,52)],'v')
line([(10,52),(12,53),(15,53)],'R')
# collar pocket and dark contact make neck overlap distinct from full shirt outline.
shape('neck',[(12,43),(19,43),(20,45),(18,47),(13,47),(11,45)],'d')
line([(13,45),(14,46),(17,46),(18,45)],'c')
shape('jawContact',[(7,42),(24,42),(25,44),(25,45),(6,45),(6,44)],'n')
# Ears are independent rounded lobes; cheek contour no longer contains wedges.
shape('leftEar',[(5,37),(6,37),(7,38),(7,40),(6,41),(5,41),(4,40),(4,38)],'s')
shape('rightEar',[(26,37),(25,37),(24,38),(24,40),(25,41),(26,41),(27,40),(27,38)],'s')
dot(5,38,'S');dot(5,39,'d');dot(26,39,'d')
shape('face',[(8,34),(23,34),(25,36),(25,40),(24,42),(22,44),(20,45),(11,45),(9,44),(7,42),(6,40),(6,36)],'s')
fill([(7,35),(12,34),(20,35),(23,37),(23,41),(20,43),(12,43),(9,42),(7,40)],'S')
fill([(24,36),(25,37),(25,40),(23,42),(21,44),(11,44),(9,43),(19,43),(22,41),(23,39)],'s')
# Side planes remain skin; inner ear marks live in the ear feature masks.
# Four-pixel reference eye height; restrained skin-adjacent border and no doll sparkle.
for x in (12,18):
 rect((x,38,x+1,41),'O');dot(x,38,'n')
eyes=Image.new('1',im.size);eyed=ImageDraw.Draw(eyes)
for x in (12,18):eyed.rectangle((x,38,x+1,41),fill=1)
parts['eyes']=eyes
line([(10,37),(13,37)],'d');line([(18,37),(21,37)],'d')
# Unmarked center-face plane: no explicit front nose or lip cluster.
shape('hair',[(18,22),(20,21),(22,22),(22,24),(24,25),(26,27),(25,29),(26,30),(27,32),(27,35),(25,36),(24,35),(23,37),(21,36),(19,37),(17,35),(16,37),(14,36),(12,37),(10,35),(8,37),(6,36),(4,34),(4,32),(5,30),(6,28),(8,27),(9,25),(12,24),(17,24)],'h')
# Sloping connected lock clusters follow the sweep; no circular dark pads.
fill([(11,26),(15,25),(19,24),(21,25),(19,27),(14,28),(11,30),(8,31),(8,29)],'m')
fill([(20,28),(23,27),(24,29),(24,32),(22,34),(20,33),(18,34),(18,31)],'m')
fill([(6,32),(10,30),(12,30),(11,33),(9,35),(7,34)],'m')
line([(13,26),(16,26),(18,25)],'l');line([(21,29),(23,29)],'l')
line([(14,28),(15,30),(14,33),(13,35)],'O')
line([(18,28),(19,30),(18,32),(17,34)],'O')
line([(9,31),(9,33),(8,34)],'h')
# Back: same shoulders, hands, shorts and foot stance; crown viewed from behind,
# jacket yoke and centered small daypack are original costume adaptations.
front=frames['south'].copy();frontparts=parts.copy()
start('north')
for name in ('leftFoot','rightFoot','shorts','leftArm','rightArm','shirt'):
 mask=frontparts[name];im.paste(front,(0,0),mask);parts[name]=mask.copy()
# Repaint torso rather than leave the front chest visible.
fill([(10,46),(13,45),(18,45),(21,46),(21,53),(19,54),(12,54),(10,53)],'r')
line([(10,47),(13,46),(18,46),(21,47)],'R')
shape('pack',[(12,46),(19,46),(21,48),(21,53),(19,55),(12,55),(10,53),(10,48)],'b')
fill([(12,48),(18,47),(19,48),(19,51),(12,51)],'B');line([(12,52),(19,52)],'n');line([(13,53),(18,53)],'t')
shape('neck',[(11,42),(20,42),(20,45),(18,46),(13,46),(11,45)],'s')
shape('jawContact',[(7,42),(24,42),(25,44),(25,45),(6,45),(6,44)],'n')
# Ears are independent rounded lobes; cheek contour no longer contains wedges.
shape('leftEar',[(5,37),(6,37),(7,38),(7,40),(6,41),(5,41),(4,40),(4,38)],'s')
shape('rightEar',[(26,37),(25,37),(24,38),(24,40),(25,41),(26,41),(27,40),(27,38)],'s')
dot(5,38,'S');dot(5,39,'d');dot(26,39,'d')
shape('face',[(8,34),(23,34),(25,36),(25,40),(24,42),(22,44),(20,45),(11,45),(9,44),(7,42),(6,40),(6,36)],'s')
line([(7,39),(8,41),(11,43),(20,43),(23,41),(24,39)],'d')
shape('hair',[(10,21),(12,22),(13,24),(18,24),(22,25),(24,27),(26,29),(27,31),(27,35),(26,37),(25,39),(23,41),(8,41),(6,39),(5,37),(4,35),(4,31),(5,29),(4,27),(6,25),(8,24),(8,22)],'h')
fill([(9,24),(12,25),(16,26),(20,27),(22,29),(20,31),(17,29),(12,28),(8,27)],'m')
fill([(7,29),(11,30),(14,32),(13,35),(10,36),(7,34)],'m')
fill([(19,32),(22,31),(24,33),(23,36),(20,38),(18,36)],'m')
line([(9,25),(11,26),(14,26)],'l');line([(19,28),(21,29)],'l')
line([(14,29),(16,31),(16,34),(15,37)],'O')
line([(9,35),(11,38),(14,39)],'m');line([(19,39),(22,37)],'m')
# Profile: smooth forehead-to-cheek plane without projecting nose; pack belongs rear.
start('west')
# Far foot is mostly occluded under shorts/near shoe, never a second long sole.
# Upright side view: compact hip/shoe mass beneath vertical torso.
shape('farFoot',[(17,57),(20,57),(21,59),(20,60),(17,60),(16,59)],'n',edge='n')
shape('shorts',[(12,54),(21,54),(22,56),(20,58),(12,58),(11,56)],'n',edge='n')
fill([(13,55),(15,55),(16,56),(14,57),(12,56)],'b')
shape('pack',[(22,46),(25,47),(26,49),(26,52),(24,54),(22,53)],'b')
line([(24,48),(24,51)],'B')
shape('shirt',[(12,46),(20,46),(22,48),(22,54),(20,55),(12,55),(11,54),(11,48)],'r')
# Small front-facing inset, not a tall pale strip resembling a second arm.
fill([(12,48),(13,48),(13,49),(12,49)],'c')
fill([(20,48),(21,49),(21,53),(19,54),(17,54),(18,52)],'v')
# Side arm hangs from shoulder: shoulder/sleeve -> elbow -> wrist/hand vertically.
shape('nearArm',[(15,48),(18,48),(19,50),(18,54),(16,55),(14,53),(14,50)],'s')
line([(15,50),(15,52),(16,53)],'S');dot(17,53,'d')
shape('sleeve',[(15,46),(18,46),(20,48),(19,50),(15,50),(14,48)],'c')
line([(16,49),(18,49)],'C')
# No internal horizontal pant/shoe rail: only the outer toe/sole silhouette is inked.
shape('nearFoot',[(11,58),(18,58),(20,59),(20,60),(18,61),(10,61),(9,60),(9,59)],'n',edge='n')
line([(11,58),(9,59),(9,60),(10,61),(18,61),(20,60),(20,59)],'O')
dot(11,60,'b')
shape('neck',[(12,42),(18,42),(19,45),(17,47),(13,46),(11,45)],'d')
shape('face',[(8,33),(21,33),(25,36),(26,39),(25,41),(24,43),(22,45),(10,45),(8,44),(7,42),(5,41),(4,39),(4,35)],'s')
fill([(7,35),(12,34),(17,35),(19,38),(17,41),(14,43),(9,42),(6,40),(5,38)],'S')
rect((10,38,11,41),'O');dot(10,38,'n')
profileEye=Image.new('1',im.size);ImageDraw.Draw(profileEye).rectangle((10,38,11,41),fill=1);parts['eyes']=profileEye
# Small attached ear, no oversized dark cheek/muzzle patch.
shape('nearEar',[(19,38),(20,38),(21,39),(21,41),(20,42),(19,42),(18,41),(18,39)],'s',edge='d')
dot(19,39,'S');dot(19,40,'d')
shape('hair',[(19,22),(21,21),(23,23),(23,25),(25,26),(27,27),(29,29),(29,31),(28,32),(28,34),(27,35),(27,38),(26,40),(24,41),(23,39),(22,38),(21,36),(18,36),(16,35),(14,36),(12,35),(10,36),(9,35),(7,36),(5,35),(4,33),(4,30),(5,28),(6,27),(8,26),(10,25),(14,24),(18,24)],'h')
fill([(10,26),(15,25),(19,24),(21,25),(20,27),(16,28),(11,29),(7,31),(6,30)],'m')
fill([(21,28),(24,27),(26,29),(27,31),(25,33),(23,34),(21,33),(19,34),(19,31)],'m')
fill([(7,32),(11,30),(13,31),(12,33),(10,34),(7,34)],'m')
line([(12,26),(15,26),(18,25)],'l');line([(22,29),(24,29)],'l')
line([(14,29),(16,30),(16,33),(15,35)],'O')
line([(19,29),(20,31),(19,34)],'O')
line([(25,35),(25,37),(24,38)],'m')
frames['east']=frames['west'].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
masks['east']={k:v.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for k,v in masks['west'].items()}
# Explicitly stored profile opposite; costume is bilateral, lighting is not blindly mirrored.
e=frames['east'];ed=ImageDraw.Draw(e)
# Remove the mirrored brightest crown points; shift equivalent highlight to screen-left.
for x,y in [(20,26),(18,25),(16,25),(11,28),(9,29)]:
 if e.getpixel((x,y))[:3]==tuple(bytes.fromhex(P['l'][1:])):ed.point((x,y),fill=P['m'])
ed.line([(9,28),(10,27),(12,26)],fill=P['l'])
# HR7 authorization is body only. Exact HR6 rows0..45 are protected in every view.
for direction,image in frames.items():
 protected=Image.open(ROOT/f'docs/reviews/M1-HR6/hero-{direction}.png').convert('RGBA')
 image.paste(protected.crop((0,0,32,46)),(0,0))
# Export exact native sprites and editable indexed frames.
colors=[None]+list(dict.fromkeys(P.values())); rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in colors[1:]]
source={'format':'fmw-sprite','version':1,'name':'Boy Hero HR7 — directional construction','preset':'character','width':32,'height':64,'palette':colors,'bank':'custom','notes':'HR7 NORMAL body review. HR6 head and accepted ears pixel-exact; no mouth/nose. Upright arms/torso and simple shoes, same outfit. Anchor [16,64]. No variants/customization UI.','defaultFeatures':{'mouth':None,'nose':None,'body':'normal'},'frames':[]}
for name,img in frames.items():
 img.save(OUT/f'hero-{name}.png');source['frames'].append({'name':name+' idle','ticks':8,'pixels':[rgba.index(p) for p in img.get_flattened_data()]})
(ROOT/'art/source/hero-redesign-r7/hero-boy.sprite.json').write_text(json.dumps(source,separators=(',',':'))+'\n')
(ROOT/'art/source/hero-redesign-r7/masks.json').write_text(json.dumps({n:{k:[int(v) for v in m.get_flattened_data()] for k,m in ms.items()} for n,ms in masks.items()},separators=(',',':'))+'\n')
font=ImageFont.load_default()
# Original-only clean lineup, with 4x above / exact 1x beneath.
plate=Image.new('RGB',(720,410),'#eee6d0');pd=ImageDraw.Draw(plate)
for i,(name,img) in enumerate(frames.items()):
 x=32+i*174;pd.text((x,15),name.upper()+' — HR7 REVIEW',fill='#292b34',font=font)
 big=img.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x,35),big);plate.paste(img,(x+48,320),img)
pd.text((32,391),'Original 32x64 idles | 4x and native 1x | no animation or gameplay replacement',fill='#292b34');plate.save(OUT/'directional-review.png')
# Native grid and labels stay separate from production pixels.
grid=Image.new('RGB',(340,590),'#eee6d0');gd=ImageDraw.Draw(grid);big=frames['west'].resize((256,512),Image.Resampling.NEAREST);grid.paste(big,(54,38),big)
for x in range(33):gd.line((54+x*8,38,54+x*8,550),fill='#b6b3aa')
for row in range(65):gd.line((54,38+row*8,310,38+row*8),fill='#b6b3aa')
for y in list(range(0,61,10))+[64]:
 yy=550-y*8;gd.line((54,yy,310,yy),fill='#757e77');gd.text((22,yy-4),str(y),fill='#292b34')
gd.line((182,38,182,550),fill='#c35151',width=2);gd.text((55,12),'HR7 WEST | 8x | one cell = native pixel',fill='#292b34');gd.text((55,566),'X16 center | Y upward | anchor (16,64)',fill='#292b34');grid.save(OUT/'hero-grid.png')
# Actual foreground anatomy proof, paired regions independently checked.
proof=Image.new('RGB',(520,290),'#eee6d0');pp=ImageDraw.Draw(proof)
for i,k in enumerate(['face','shirt','shorts','leftArm','leftFoot']):
 m=masks['south'][k];color=Image.new('RGBA',(32,64),'#cc705c');color.putalpha(m.convert('L').point(lambda v:255 if v else 0));b=color.resize((96,192),Image.Resampling.NEAREST);proof.paste(b,(8+i*103,35),b);pp.text((8+i*103,12),k,fill='#292b34')
proof.save(OUT/'anatomy-proof.png')
report={'approval':'awaiting user visual review','animation':'not authored; directional-idle construction review only','frames':{}}
for name,img in frames.items():
 pts={(x,y) for y in range(64) for x in range(32) if img.getpixel((x,y))[3]};seen={next(iter(pts))};todo=list(seen)
 while todo:
  x,y=todo.pop()
  for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if q in pts and q not in seen:seen.add(q);todo.append(q)
 assert pts==seen,name+' disconnected silhouette'
 assert set(p[3] for p in img.get_flattened_data())=={0,255}
 assert img.getbbox()[3]==62
 assert [rgba[j] for j in source['frames'][list(frames).index(name)]['pixels']]==list(img.get_flattened_data())
 bb=img.getbbox(); report['frames'][name]={'boundsExclusive':bb,'opaqueColors':len(set(img.get_flattened_data()))-1,'connected':True,'binaryAlpha':True,'sourceEquality':True,'anchor':[16,64],'sha256':hashlib.sha256((OUT/f'hero-{name}.png').read_bytes()).hexdigest()}
for name in ('south','north'):
 ms=masks[name]
 for a,b in [('leftArm','rightArm'),('leftFoot','rightFoot')]:assert list(ms[a].transpose(Image.Transpose.FLIP_LEFT_RIGHT).get_flattened_data())==list(ms[b].get_flattened_data()),a
 for k in ('face','shirt','shorts','neck'):assert list(ms[k].get_flattened_data())==list(ms[k].transpose(Image.Transpose.FLIP_LEFT_RIGHT).get_flattened_data()),k
report['pairedAnatomyMasks']=True
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
