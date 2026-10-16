"""M1.OM2: original native-cell Mom idle candidates, isolated review only.

Run with bundled workspace Python/Pillow. No runtime/editor/shared output.
RD1 visible FRONT envelope is a construction reference; part labels are provisional.
"""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=ROOT/'docs/reviews/M1-OM2'
OUT.mkdir(exist_ok=True)
P={
 'ink':'#201008','skin':'#a87038','skinShadow':'#784820','skinLight':'#c48e4a',
 'cream':'#f7edcc','creamShadow':'#d9cba7','rose':'#ba7082','roseShadow':'#87465e',
 'roseLight':'#cf8b99','navy':'#30476a','navyShadow':'#202e48','shoe':'#67464f',
 'sole':'#4d414e','hair':'#28252b','hairMid':'#3b3030','hairLight':'#64545e',
 'gold':'#dfad49','goldShadow':'#a67436',
}
ORDER=['feet','legs','far-arm','torso','near-arm','hands','head','face','hair','jewelry']
def blank():return Image.new('RGBA',(32,64))
def rgb(c):return tuple(bytes.fromhex(P.get(c,c).lstrip('#')))+(255,)
class Pose:
 def __init__(self):self.layers={n:blank() for n in ORDER};self.geometry={}
 def p(self,n,x,y,c):
  assert 0<=x<32 and 0<=y<64,(n,x,y)
  self.layers[n].putpixel((x,y),rgb(c))
 def r(self,n,l,t,r,b,c):
  for y in range(t,b):
   for x in range(l,r):self.p(n,x,y,c)
 def span(self,n,y,l,r,c):self.r(n,l,y,r,y+1,c)
 def comp(self):
  o=blank()
  for n in ORDER:o.alpha_composite(self.layers[n])
  return o
 def outline(self,n):
  a=self.layers[n].copy()
  for y in range(64):
   for x in range(32):
    if not a.getpixel((x,y))[3]:continue
    if any(not (0<=u<32 and 0<=v<64) or not a.getpixel((u,v))[3] for u,v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):self.p(n,x,y,'ink')
 def snapshot(self,n,layer):self.geometry[n]=[(x,y) for y in range(64) for x in range(32) if self.layers[layer].getpixel((x,y))[3]]

RD=json.loads((ROOT/'art/source/reference-dummy-r1/construction.json').read_text())
OLD=json.loads((ROOT/'art/source/idle-collection-v1/mom.sprite.json').read_text())
MASK=json.loads((ROOT/'art/source/idle-collection-v1/mom.masks.json').read_text())
def front(back=False):
 a=Pose()
 # Keep the actual RD1 projected volume, rather than subtracting glove/garment fit.
 for n,rec in RD['regions'].items():
  if n in ['head','ears']:continue
  for x,y in rec['cells']:
   if n in ['left-shoe','right-shoe']:
    layer='feet';c='shoe' if y<60 else 'sole'
   elif n in ['left-leg','right-leg','pelvis']:layer='legs';c='navy'
   elif n=='hands':layer='hands';c='skin' if x<16 else 'skinShadow'
   elif n=='arms':layer='near-arm';c='rose'
   else:layer='torso';c='rose' if back or x<13 or x>18 else 'cream'
   a.p(layer,x,y,c)
 for layer in ['feet','legs','near-arm','hands']:a.outline(layer)
 # Source-anchored segmentation is editable, not recovered skeletal anatomy.
 for y in range(43,55):
  l=8 if y<45 else 9;r=32-l
  for x in range(l,r):
   if y>=45 and not any((x,y) in rec['cells'] for n,rec in RD['regions'].items() if n=='torso'):continue
   c='rose' if back or x<13 or x>18 else 'cream'
   if x in [12,19]:c='roseShadow'
   if y==54:c='roseShadow' if back or x<13 or x>18 else 'creamShadow'
   a.p('torso',x,y,c)
 # Only a short collar beneath the adult face; no exposed long neck.
 a.r('torso',13,43,19,45,'creamShadow' if not back else 'roseShadow')
 # Adult head translated upward leaves the former RD1 central jaw row vacant.
 # Complete that garment junction explicitly; a transparent rail is a defect.
 for y in [44,45]:
  for x in range(10,22):
   a.p('torso',x,y,'rose' if back or x<13 or x>18 else 'creamShadow')
 for n in ['head','ears']:
  for x,y in RD['regions'][n]['cells']:
   a.p('head',x,y-2,'skinShadow' if n=='ears' else 'skin')
 a.outline('head');a.snapshot('head-envelope','head')
 if not back:
  for x in [12,18]:
   a.r('face',x,36,x+2,40,'ink');a.p('face',x,36,'cream')
  a.geometry['eyes']=[(x,y) for x in [12,13,18,19] for y in range(36,40)]
 # Preserve established original front hair clusters as appearance, not anatomy.
 for i,part in enumerate(MASK['visibleParts']):
  x=i%32;y=i//32;v=OLD['frames'][0]['pixels'][i]
  if part=='hair' and v:a.layers['hair'].putpixel((x,y),rgb(OLD['palette'][v]))
 if back:
  # Rounded rear hair planes, not the former striped flat rectangle.
  for y,l,r in [(31,5,27),(32,4,28),(33,4,28),(34,4,28),(35,4,28),(36,4,28),(37,5,27),(38,5,27),(39,6,26),(40,7,25),(41,8,24),(42,10,22)]:
   for x in range(l,r):a.p('hair',x,y,'hairMid' if x<20 else 'hair')
  # Broad swept planes with short highlights, no vertical barcode bands.
  for y,l,r in [(31,7,16),(32,6,14),(33,6,12),(34,6,10),(35,7,9)]:a.span('hair',y,l,r,'hairLight')
  for y,l,r in [(35,10,21),(36,9,20),(37,9,19),(38,10,18),(39,11,17)]:a.span('hair',y,l,r,'hairMid')
  # Outline only the exposed lower edge, avoiding internal black material bars.
  for x,y in [(5,36),(5,37),(6,38),(6,39),(7,40),(8,41),(9,41),(10,42),(11,42),(12,42),(13,42),(14,42),(15,42),(16,42),(17,42),(18,42),(19,42),(20,42),(21,42),(22,41),(23,41),(24,40),(25,39),(25,38),(26,37),(26,36)]:a.p('hair',x,y,'ink')
 for x in [5,25]:a.r('jewelry',x,39,x+2,41,'gold');a.p('jewelry',x+1,40,'goldShadow')
 return a

def puff(a,x,y,far=False):
 rows=['...oooo...','..olllmo..','.olllmmdo.','olllmmmddo','ollmmmmddo','olmmmdddmo','ommmdddmoo','.omdddmoo.','..omddoo..','...ooo....']
 pal={'o':'ink','l':'hairLight','m':'hairMid','d':'hair'}
 for j,row in enumerate(rows):
  for i,k in enumerate(row):
   if k!='.':a.p('hair',x+i,y+j,pal[k] if not far or k!='l' else 'hairMid')

def west():
 a=Pose()
 # Full projected side shoe; far toe remains partly visible behind the near foot.
 for y,l,r in [(55,13,23),(56,13,23),(57,13,23),(58,12,23),(59,11,22),(60,11,21),(61,13,19)]:
  for x in range(l,r):a.p('legs' if y<58 else 'feet',x,y,'navy' if y<58 else 'shoe')
 a.outline('legs');a.outline('feet')
 a.span('feet',58,14,21,'navyShadow')
 a.span('feet',59,12,17,'shoe');a.span('feet',60,13,18,'sole')
 # Profile far arm is fully occluded by the garment in this idle proposal.
 # Keep its semantic layer empty; do not invent a tiny forward sleeve/hand.
 for y,l,r in [(43,13,22),(44,12,23),(45,12,24),(46,11,24),(47,11,24),(48,11,24),(49,11,24),(50,12,24),(51,12,24),(52,13,24),(53,13,23),(54,14,23)]:
  for x in range(l,r):a.p('torso',x,y,'cream' if 12<=x<=14 and 46<=y<=51 else 'rose')
 a.outline('torso')
 for y in range(46,53):a.p('torso',15,y,'roseShadow')
 for y,l,r in [(44,21,24),(45,20,25),(46,20,26),(47,20,26),(48,20,26),(49,20,25)]:a.span('near-arm',y,l,r,'rose')
 a.outline('near-arm');a.span('near-arm',48,21,25,'roseShadow')
 for y,l,r in [(49,21,25),(50,20,26),(51,20,26),(52,20,26),(53,20,26),(54,21,25)]:a.span('hands',y,l,r,'skin')
 a.outline('hands');a.r('hands',21,50,25,54,'skin');a.p('hands',24,53,'skinShadow')
 # Broad rounded head overlaps shoulder: all coordinates original construction.
 for y,l,r in [(26,12,22),(27,10,24),(28,9,25),(29,8,26),(30,7,27),(31,6,27),(32,6,27),(33,5,27),(34,5,27),(35,5,27),(36,5,26),(37,5,26),(38,5,25),(39,4,25),(40,5,24),(41,6,23),(42,8,22),(43,10,21)]:a.span('head',y,l,r,'skin')
 a.outline('head');a.snapshot('head-envelope','head')
 a.r('face',8,36,10,40,'ink');a.p('face',8,36,'cream')
 a.r('face',19,37,22,41,'skinShadow');a.r('face',19,38,21,40,'skin')
 # Hair follows the skull; lower jaw contour stays visible.
 for y,l,r in [(26,12,22),(27,10,24),(28,9,25),(29,8,26),(30,7,27),(31,6,27),(32,6,27),(33,6,27),(34,17,27),(35,20,27),(36,22,26),(37,23,26),(38,23,25),(39,23,25),(40,22,24),(41,21,23)]:
  for x in range(l,r):a.p('hair',x,y,'hairMid' if x<19 else 'hair')
 for y,l,r in [(28,10,18),(29,9,16),(30,8,14),(31,7,12),(32,7,10)]:a.span('hair',y,l,r,'hairLight')
 puff(a,9,21,True);puff(a,18,20)
 a.r('jewelry',19,40,21,42,'gold');a.p('jewelry',20,41,'goldShadow')
 return a

poses={'south':front(),'north':front(True),'west':west()}
east=Pose()
# Opposite view is an explicit symmetric outfit adaptation; highlights are relit.
for n,im in poses['west'].layers.items():
 east.layers[n]=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if n=='hair':
  for y in range(64):
   for x in range(32):
    if east.layers[n].getpixel((x,y))==rgb('hairLight'):east.layers[n].putpixel((x,y),rgb('hairMid'))
east.geometry={n:[(31-x,y) for x,y in cells] for n,cells in poses['west'].geometry.items()}
poses['east']=east

font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
title=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',16)
def text(d,xy,s,fill='#252431',f=font):d.text(xy,s,fill=fill,font=f)
board=Image.new('RGB',(1030,670),'#e8e4d7');d=ImageDraw.Draw(board)
text(d,(20,12),'M1.OM2 — Mom / four idle candidates / UNAPPROVED',f=title)
text(d,(20,39),'Native 32×64; nearest 6×. Fixed frame/anchor. RD1 is passing construction, not observed idle.')
checks={};assets={};project={'format':'fmw-sprite','version':1,'name':'Mom OM2 — unapproved four idle review','preset':'character','width':32,'height':64,'palette':[None]+list(P.values()),'bank':'custom','notes':'Four idle candidates only. No runtime adoption. Layered source in per-direction JSON/PNG.','frames':[]}
for k,(name,a) in enumerate(poses.items()):
 out=HERE/name;out.mkdir(exist_ok=True)
 im=a.comp();im.save(OUT/f'idle-{name}.png');im.resize((192,384),Image.Resampling.NEAREST).save(OUT/f'idle-{name}-6x.png')
 layerdata={}
 for n,png in a.layers.items():
  png.save(out/f'{n}.png')
  layerdata[n]=[[x,y,'#'+bytes(png.getpixel((x,y))[:3]).hex()] for y in range(64) for x in range(32) if png.getpixel((x,y))[3]]
 (out/'layers.json').write_text(json.dumps({'frame':[32,64],'anchor':[16,64],'order':ORDER,'layers':layerdata,'geometryProposals':a.geometry},indent=2)+'\n')
 pixels=list(im.get_flattened_data());pal=[None]+list(dict.fromkeys('#'+bytes(p[:3]).hex() for p in pixels if p[3]))
 indexed=[pal.index('#'+bytes(p[:3]).hex()) if p[3] else 0 for p in pixels]
 (out/'idle.sprite.json').write_text(json.dumps(dict(project,palette=pal,frames=[{'name':name+' idle','ticks':8,'pixels':indexed}]),indent=2)+'\n')
 pp=project['palette']
 for col in pal[1:]:
  if col not in pp:pp.append(col)
 project['frames'].append({'name':name+' idle','ticks':8,'pixels':[pp.index('#'+bytes(p[:3]).hex()) if p[3] else 0 for p in pixels]})
 reopened=Image.open(OUT/f'idle-{name}.png').convert('RGBA')
 recomposed=blank()
 for n in ORDER:recomposed.alpha_composite(Image.open(out/f'{n}.png').convert('RGBA'))
 assert recomposed.tobytes()==reopened.tobytes()
 assert all(p[3] in [0,255] for p in pixels)
 assert all(not im.getpixel((x,y))[3] for y in [62,63] for x in range(32))
 checks[name]={'bounds':im.getbbox(),'opaqueCells':sum(bool(p[3]) for p in pixels),'colors':len(pal)-1,'layerRecomposition':True,'binaryAlpha':True,'bottomTwoRowsTransparent':True,'pngSHA256':hashlib.sha256((OUT/f'idle-{name}.png').read_bytes()).hexdigest()}
 x=18+k*251;text(d,(x+5,70),name.upper(),f=title)
 board.paste(im.resize((192,384),Image.Resampling.NEAREST),(x+8,100),im.resize((192,384),Image.Resampling.NEAREST))
 d.rectangle((x+7,99,x+200,484),outline='#b6b4aa')
 board.paste(im,(x+85,505),im);text(d,(x+10,580),'Actual native 1× above')
 text(d,(x+10,607),str(im.getbbox()))
assets['sourceCommit']='a25379df5c76fc1d4bf88c02525aef5affa4781c'
(HERE/'mom-four-idles.sprite.json').write_text(json.dumps(project,indent=2)+'\n')
(HERE/'validation.json').write_text(json.dumps({'task':'M1.OM2','directions':checks,'appearanceApproval':False,'walking':'not authored','runtime':'unchanged'},indent=2)+'\n')
board.save(OUT/'idle-comparison.png')
# Direct native montage, full64 rows; no image-space fitting.
native=Image.new('RGBA',(128,64))
for k,a in enumerate(poses.values()):native.alpha_composite(a.comp(),(32*k,0))
native.save(OUT/'idle-native.png')
# Countable inspection grid, Y upward. This is a review overlay only.
grid=Image.new('RGB',(1040,620),'#eee9dd');gd=ImageDraw.Draw(grid)
text(gd,(15,12),'OM2 native-cell grid: Y0 bottom; x16 center; each square = one native pixel',f=title)
for k,(name,a) in enumerate(poses.items()):
 x=45+k*255;y=75;s=7;im=a.comp().resize((224,448),Image.Resampling.NEAREST);grid.paste(im,(x,y),im)
 text(gd,(x,y-25),name.upper())
 for col in range(33):gd.line((x+col*s,y,x+col*s,y+448),fill='#cac7bd',width=1)
 for row in range(65):gd.line((x,y+row*s,x+224,y+row*s),fill='#cac7bd',width=1)
 for Y in [0,10,20,30,40,50,60,64]:
  yy=y+(64-Y)*s;gd.line((x,yy,x+224,yy),fill='#98968b');text(gd,(x-27,yy-6),str(Y))
 gd.line((x+16*s,y,x+16*s,y+448),fill='#b34767',width=2)
 text(gd,(x,y+462),'0              16             32')
grid.save(OUT/'idle-grid.png')
print(json.dumps(checks,indent=2))
