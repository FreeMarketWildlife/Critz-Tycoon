"""Original Critz pixels, manually authored on 32x64 grid; no reference-image input.
Optional reference comparisons are produced by a separate read-only analysis script.
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'docs/reviews/M1-HR4'
P={'O':'#242330','h':'#322a31','m':'#4c3739','l':'#705044','s':'#a66845','S':'#c38a58','d':'#744539','r':'#ed745c','R':'#ffad7a','v':'#ae454a','c':'#f9edc8','C':'#bfc0aa','b':'#465671','B':'#748894','n':'#2a344a','t':'#748894'}
frames={}; masks={}
def start(name):
 global im,d,parts
 im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im);parts={};frames[name]=im;masks[name]=parts

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
shape('leftFoot',[(7,57),(13,57),(14,59),(13,61),(8,61),(6,60),(6,59)],'n')
shape('rightFoot',[(18,57),(24,57),(25,59),(25,60),(23,61),(18,61),(17,59)],'n')
line([(7,60),(12,60)],'C');line([(19,60),(24,60)],'C')
line([(8,58),(11,58)],'t');line([(20,58),(23,58)],'t')
shape('shorts',[(8,53),(23,53),(24,57),(19,58),(16,56),(15,56),(12,58),(7,57)],'b')
fill([(16,54),(22,54),(23,56),(19,57),(16,55)],'n');line([(9,55),(12,55)],'B')
shape('leftArm',[(6,46),(9,48),(8,50),(9,52),(7,54),(4,53),(3,50),(4,48)],'s')
shape('rightArm',[(25,46),(27,48),(28,50),(27,53),(24,54),(22,52),(23,50),(22,48)],'s')
fill([(4,49),(6,48),(7,49),(6,51),(7,52),(5,52)],'S')
fill([(25,49),(27,50),(26,52),(24,53),(23,52),(25,51)],'d')
shape('shirt',[(10,45),(21,45),(25,46),(27,48),(24,50),(22,49),(22,54),(20,55),(11,55),(9,54),(9,49),(7,50),(4,48),(6,46)],'r')
fill([(5,48),(7,46),(9,46),(9,48),(7,49)],'c')
fill([(22,46),(24,46),(26,48),(24,49),(22,48)],'C')
line([(10,47),(11,46),(13,46)],'R')
# Cream inset chest with coral side panels; follows tapered torso rather than broad stripe.
fill([(13,46),(18,46),(20,48),(19,51),(12,51),(11,48)],'c')
line([(12,50),(18,50)],'C')
fill([(20,47),(21,48),(21,53),(19,54),(16,54),(17,52),(19,52)],'v')
line([(10,52),(12,53),(15,53)],'R');line([(10,54),(13,54)],'v')
# collar pocket and dark contact make neck overlap distinct from full shirt outline.
shape('neck',[(12,43),(19,43),(20,45),(18,47),(13,47),(11,45)],'d')
line([(13,45),(14,46),(17,46),(18,45)],'c')
shape('face',[(7,34),(24,34),(26,36),(28,37),(28,40),(26,41),(25,42),(23,43),(21,45),(10,45),(8,43),(6,42),(5,41),(3,40),(3,37),(5,36)],'s')
fill([(7,35),(12,34),(20,35),(23,37),(23,41),(20,43),(12,43),(9,42),(7,40)],'S')
fill([(24,36),(25,37),(25,40),(23,42),(21,44),(11,44),(9,43),(19,43),(22,41),(23,39)],'s')
line([(6,38),(6,39)],'d');line([(25,38),(25,39)],'d')
# Four-pixel reference eye height; restrained skin-adjacent border and no doll sparkle.
for x in (12,18):
 rect((x,38,x+1,41),'O');dot(x,38,'n')
eyes=Image.new('1',im.size);eyed=ImageDraw.Draw(eyes)
for x in (12,18):eyed.rectangle((x,38,x+1,41),fill=1)
parts['eyes']=eyes
line([(10,37),(13,37)],'d');line([(18,37),(21,37)],'d')
# Unmarked center-face plane: no explicit front nose or lip cluster.
shape('hair',[(10,23),(12,22),(15,22),(16,23),(19,22),(21,23),(21,24),(24,24),(25,26),(24,27),(27,28),(27,31),(26,33),(24,34),(24,37),(22,36),(21,35),(19,36),(17,35),(16,37),(14,36),(13,35),(11,37),(9,36),(8,37),(6,36),(5,34),(4,32),(4,29),(5,27),(7,27),(7,25),(9,25)],'h')
fill([(8,26),(11,24),(15,23),(17,24),(15,26),(12,27),(11,30),(8,31),(7,29)],'m')
fill([(18,25),(21,25),(23,27),(22,30),(19,31),(17,29)],'m')
fill([(24,29),(25,30),(25,33),(23,34),(22,32)],'m')
line([(10,26),(12,25),(14,25)],'l');line([(18,26),(20,26)],'l')
line([(12,28),(13,30),(12,33),(11,35)],'O');line([(17,28),(17,31),(16,33),(16,35)],'O')
line([(8,28),(9,30),(8,33)],'O');line([(22,27),(23,29),(22,32)],'O')
line([(9,32),(10,33),(10,34)],'m');line([(20,32),(20,33),(19,34)],'m')
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
shape('face',[(7,34),(24,34),(26,36),(28,37),(28,40),(26,41),(25,42),(23,43),(21,45),(10,45),(8,43),(6,42),(5,41),(3,40),(3,37),(5,36)],'s')
line([(7,39),(8,41),(11,43),(20,43),(23,41),(24,39)],'d')
shape('hair',[(9,23),(13,22),(18,22),(22,23),(24,25),(25,27),(27,28),(27,33),(26,35),(25,38),(23,40),(21,41),(10,41),(8,40),(6,38),(5,35),(4,33),(4,29),(6,27),(7,25)],'h')
fill([(8,27),(11,25),(15,24),(17,25),(15,28),(12,29),(10,32),(7,32)],'m')
fill([(18,26),(21,26),(24,29),(23,33),(20,34),(18,32)],'m')
line([(10,27),(12,26),(14,26)],'l');line([(19,28),(21,28)],'l')
line([(12,30),(13,34),(12,37)],'O');line([(17,29),(17,33),(18,36)],'O')
line([(8,35),(10,37),(13,38)],'m');line([(20,37),(23,35)],'m')
# Profile: smooth forehead-to-cheek plane without projecting nose; pack belongs rear.
start('west')
# Far foot is mostly occluded under shorts/near shoe, never a second long sole.
shape('farFoot',[(17,56),(20,56),(21,58),(19,59),(17,59),(16,58)],'n')
shape('shorts',[(11,53),(21,53),(23,54),(22,56),(20,57),(11,57),(10,55)],'n')
fill([(12,54),(16,54),(17,56),(12,56)],'b')
shape('pack',[(21,46),(24,46),(26,48),(27,49),(27,51),(25,53),(22,53),(21,51)],'b')
line([(23,48),(25,49),(25,51)],'t')
shape('shirt',[(13,45),(19,44),(22,46),(22,52),(20,55),(12,55),(10,52),(10,48)],'r')
fill([(11,48),(13,46),(15,46),(15,51),(11,51)],'c')
fill([(19,47),(21,48),(21,52),(19,54),(16,54),(17,51)],'v')
line([(12,53),(15,53)],'R')
# Forward arm overlaps chest; cuff and hand give a compact bent elbow.
shape('nearArm',[(10,47),(13,48),(14,50),(13,53),(10,54),(8,52),(8,49)],'s')
fill([(10,49),(11,48),(12,50),(11,52),(9,51)],'S')
line([(11,53),(13,52)],'d')
shape('sleeve',[(10,46),(14,46),(16,48),(14,50),(10,49),(9,48)],'c')
line([(11,47),(13,47)],'C')
# Compact tucked shoe: short forward toe, heel under hips, narrow contact.
shape('nearFoot',[(11,57),(17,57),(20,58),(21,58),(21,59),(19,59),(19,61),(10,61),(10,59),(8,59),(8,58)],'n')
line([(11,59),(14,59)],'B');line([(10,58),(11,58)],'t')
shape('neck',[(12,42),(18,42),(19,45),(17,47),(13,46),(11,45)],'d')
shape('face',[(9,33),(18,33),(22,36),(23,39),(21,42),(18,44),(12,45),(9,43),(7,41),(6,39),(6,35)],'s')
fill([(9,35),(13,34),(16,35),(16,39),(13,42),(10,42),(7,40),(6,38),(8,37)],'S')
line([(8,38),(9,38),(9,41)],'O')
# Small attached ear, no oversized dark cheek/muzzle patch.
fill([(18,38),(20,38),(21,40),(20,42),(18,42),(17,40)],'s')
line([(20,39),(20,41),(18,42)],'d');line([(18,39),(19,39)],'S')
shape('hair',[(12,22),(17,21),(21,22),(23,24),(25,26),(27,29),(27,33),(26,36),(24,38),(21,39),(19,37),(17,36),(16,34),(13,35),(11,33),(9,35),(7,34),(6,32),(5,30),(6,27),(8,25),(10,24)],'h')
fill([(9,27),(12,25),(16,24),(18,25),(16,27),(12,28),(11,31),(8,31)],'m')
fill([(19,26),(22,26),(24,29),(24,33),(21,35),(19,33)],'m')
line([(11,26),(13,25),(15,25)],'l');line([(20,28),(22,29)],'l')
line([(14,29),(14,32),(13,34)],'O');line([(18,29),(18,33),(19,35)],'O')
line([(23,34),(22,36)],'m')
frames['east']=frames['west'].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
masks['east']={k:v.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for k,v in masks['west'].items()}
# Explicitly stored profile opposite; costume is bilateral, lighting is not blindly mirrored.
e=frames['east'];ed=ImageDraw.Draw(e)
# Remove the mirrored brightest crown points; shift equivalent highlight to screen-left.
for x,y in [(20,26),(18,25),(16,25),(11,28),(9,29)]:
 if e.getpixel((x,y))[:3]==tuple(bytes.fromhex(P['l'][1:])):ed.point((x,y),fill=P['m'])
ed.line([(9,28),(10,27),(12,26)],fill=P['l'])
# Export exact native sprites and editable indexed frames.
colors=[None]+list(dict.fromkeys(P.values())); rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in colors[1:]]
source={'format':'fmw-sprite','version':1,'name':'Boy Hero HR4 — directional construction','preset':'character','width':32,'height':64,'palette':colors,'bank':'custom','notes':'Original Critz native idles; source-derived scale guides, no reference pixels. Anchor [16,64]. Review only.','frames':[]}
for name,img in frames.items():
 img.save(OUT/f'hero-{name}.png');source['frames'].append({'name':name+' idle','ticks':8,'pixels':[rgba.index(p) for p in img.get_flattened_data()]})
(ROOT/'art/source/hero-redesign-r4/hero-boy.sprite.json').write_text(json.dumps(source,separators=(',',':'))+'\n')
(ROOT/'art/source/hero-redesign-r4/masks.json').write_text(json.dumps({n:{k:[int(v) for v in m.get_flattened_data()] for k,m in ms.items()} for n,ms in masks.items()},separators=(',',':'))+'\n')
font=ImageFont.load_default()
# Original-only clean lineup, with 4x above / exact 1x beneath.
plate=Image.new('RGB',(720,410),'#eee6d0');pd=ImageDraw.Draw(plate)
for i,(name,img) in enumerate(frames.items()):
 x=32+i*174;pd.text((x,15),name.upper()+' — HR4 REVIEW',fill='#292b34',font=font)
 big=img.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x,35),big);plate.paste(img,(x+48,320),img)
pd.text((32,391),'Original 32x64 idles | 4x and native 1x | no animation or gameplay replacement',fill='#292b34');plate.save(OUT/'directional-review.png')
# Native grid and labels stay separate from production pixels.
grid=Image.new('RGB',(340,590),'#eee6d0');gd=ImageDraw.Draw(grid);big=frames['west'].resize((256,512),Image.Resampling.NEAREST);grid.paste(big,(54,38),big)
for x in range(33):gd.line((54+x*8,38,54+x*8,550),fill='#b6b3aa')
for row in range(65):gd.line((54,38+row*8,310,38+row*8),fill='#b6b3aa')
for y in list(range(0,61,10))+[64]:
 yy=550-y*8;gd.line((54,yy,310,yy),fill='#757e77');gd.text((22,yy-4),str(y),fill='#292b34')
gd.line((182,38,182,550),fill='#c35151',width=2);gd.text((55,12),'HR4 WEST | 8x | one cell = native pixel',fill='#292b34');gd.text((55,566),'X16 center | Y upward | anchor (16,64)',fill='#292b34');grid.save(OUT/'hero-grid.png')
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
