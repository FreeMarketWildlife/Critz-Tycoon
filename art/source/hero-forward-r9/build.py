"""Original forward-only HR9 pixels. No reference pixels/masks are read by this authoring script."""
from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR9';src=Path(__file__).parent
old=json.loads((root/'art/source/hero-redesign-r6/hero-boy.sprite.json').read_text());oldm=json.loads((root/'art/source/hero-redesign-r6/masks.json').read_text())['south'];accepted=Image.open(root/'docs/reviews/M1-HR6/hero-south.png').convert('RGBA').crop((0,0,32,46))
P={'O':'#242330','h':'#322a31','m':'#4c3739','l':'#705044','s':'#a66845','S':'#c38a58','d':'#744539','r':'#ed745c','R':'#ffad7a','v':'#ae454a','c':'#f9edc8','C':'#bfc0aa','b':'#465671','B':'#748894','n':'#2a344a'}
assert set(P.values())==set(old['palette'][1:])
def body(pose):
 im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im);parts={}
 def poly(k,pts,col,edge='O'):
  assert all(0<=x<32 and 0<=y<64 for x,y in pts)
  d.polygon(pts,fill=P[col]);d.line(pts+[pts[0]],fill=P[edge]);m=Image.new('1',(32,64));md=ImageDraw.Draw(m);md.polygon(pts,fill=1);md.line(pts+[pts[0]],fill=1);parts[k]=m
 def fill(pts,c):d.polygon(pts,fill=P[c])
 def line(pts,c):d.line(pts,fill=P[c])
 def dot(x,y,c):d.point((x,y),fill=P[c])
 if pose=='P':
  # Upper leg/cuff clusters56..58; small shoe blocks59..61. No long exposed calves.
  poly('leftLeg',[(9,54),(14,54),(14,57),(13,58),(9,58),(8,57)],'b',edge='n')
  poly('rightLeg',[(22,54),(17,54),(17,57),(18,58),(22,58),(23,57)],'b',edge='n')
  line([(10,58),(12,58)],'s');line([(19,58),(21,58)],'s')
  poly('leftShoe',[(9,59),(13,59),(14,60),(13,61),(9,61),(8,60)],'n',edge='n')
  poly('rightShoe',[(22,59),(18,59),(17,60),(18,61),(22,61),(23,60)],'n',edge='n')
  # Ink the exterior toe/contact only, not an extra horizontal top border.
  line([(9,59),(8,60),(9,61),(13,61),(14,60),(13,59)],'O')
  line([(22,59),(23,60),(22,61),(18,61),(17,60),(18,59)],'O')
  dot(10,60,'b');dot(11,60,'C');dot(20,60,'C');dot(21,60,'b')
  poly('shorts',[(10,53),(21,53),(23,56),(20,57),(17,56),(16,55),(15,55),(14,56),(11,57),(8,56)],'b',edge='n')
  fill([(16,54),(21,54),(22,56),(19,56),(16,55)],'n')
  poly('leftArm',[(6,47),(9,48),(9,50),(8,52),(6,53),(4,51),(4,49)],'s')
  poly('rightArm',[(25,47),(22,48),(22,50),(23,52),(25,53),(27,51),(27,49)],'s')
  line([(5,49),(6,51)],'S');dot(25,51,'d')
  poly('shirt',[(11,45),(20,45),(24,46),(26,48),(25,49),(22,49),(22,53),(20,55),(11,55),(9,53),(9,49),(6,49),(5,48),(7,46)],'r')
  fill([(7,46),(10,46),(10,48),(6,48)],'c');fill([(21,46),(24,46),(25,48),(21,48)],'C')
  fill([(13,46),(18,46),(20,48),(18,50),(12,50),(11,48)],'c');line([(13,50),(18,50)],'C')
  fill([(20,49),(21,49),(21,53),(18,54),(16,54),(18,52)],'v');line([(10,52),(14,53)],'R')
  poly('collar',[(12,44),(19,44),(19,46),(17,47),(14,47),(12,46)],'d');line([(14,46),(17,46)],'c')
 else:
  # A: right lower/forward foot, left upper/overlapped foot; left arm forward.
  poly('trailingLeg',[(10,54),(15,54),(16,57),(14,59),(11,59),(10,57)],'b',edge='n')
  poly('trailingShoe',[(11,57),(14,57),(15,58),(14,59),(11,59),(10,58)],'n');dot(12,58,'b')
  poly('leadingLeg',[(16,55),(21,55),(22,58),(20,61),(16,61),(15,58)],'b',edge='n')
  line([(17,60),(19,60)],'s')
  poly('leadingShoe',[(17,61),(20,61),(21,62),(20,63),(17,63),(16,62)],'n')
  line([(18,62),(19,62)],'C')
  poly('shorts',[(12,54),(22,54),(23,57),(20,59),(16,58),(13,58),(10,56)],'b',edge='n')
  fill([(17,55),(21,55),(22,57),(20,58),(17,57)],'n')
  # High side cluster adapts original daypack; not an inferred bare hand raised to jaw.
  poly('daypackEdge',[(25,45),(27,45),(28,47),(28,50),(26,52),(24,50),(24,47)],'b')
  line([(26,47),(26,49)],'B')
  poly('farArm',[(22,48),(25,48),(26,50),(25,52),(23,52),(22,50)],'d')
  poly('nearArm',[(6,49),(9,49),(10,51),(9,54),(7,55),(5,53),(5,51)],'s')
  line([(6,51),(7,53)],'S')
  poly('shirt',[(12,47),(21,47),(25,49),(25,51),(23,52),(22,56),(19,58),(13,57),(10,55),(9,52),(6,51),(6,49),(9,48)],'r')
  fill([(7,49),(10,49),(11,51),(8,52),(6,51)],'c')
  fill([(22,49),(24,49),(24,51),(22,51)],'C')
  fill([(14,48),(19,48),(21,50),(19,52),(13,51),(12,49)],'c')
  fill([(21,51),(22,52),(21,55),(18,57),(16,56),(18,54)],'v');line([(11,53),(14,55)],'R')
  poly('collar',[(13,46),(19,46),(20,48),(18,49),(15,48)],'d')
 return im,parts
rawP,partsP=body('P');rawA,partsA=body('A')
def translate(im,dy):
 target=Image.new(im.mode,(32,64));target.paste(im,(0,dy));return target
# Head shape is never redrawn; only the documented whole-head translation differs.
def compose(raw,parts,headDy,bodyDy,mirror=False):
 raw=raw.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if mirror else raw.copy()
 if mirror:parts={k:v.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for k,v in parts.items()}
 result=translate(raw,bodyDy);mp={k:translate(v,bodyDy) for k,v in parts.items()}
 h=Image.new('RGBA',(32,64));h.paste(accepted,(0,headDy),accepted);result.alpha_composite(h)
 for k in ('hair','face','eyes','leftEar','rightEar','jawContact','mouth','nose'):
  mask=Image.new('1',(32,64));mask.putdata(oldm[k]);mask.paste(0,(0,46,32,64));mp[k]=translate(mask,headDy)
 return result,mp
poses={};poseMasks={}
poses['P'],poseMasks['P']=compose(rawP,partsP,-2,-2)
poses['A'],poseMasks['A']=compose(rawA,partsA,0,-2)
poses['C'],poseMasks['C']=compose(rawA,partsA,0,-2,True)
# Keep lighting on Hero identity; mirrored pose geometry does not mirror the head.
idle,idleMask=compose(rawP,partsP,0,0)
order=['A','A','P','P','C','C','P','P'];colors=old['palette'];rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in colors[1:]]
def source(name,frames):return {'format':'fmw-sprite','version':1,'name':name,'preset':'character','width':32,'height':64,'palette':colors,'bank':'custom','notes':'HR9 FORWARD ONLY, confirmed user GIF compact motion reference. Accepted head/ears translate only. No mouth/nose. Source eight100ms frames; editor6 ticks approximate100.456ms, GIF review exact100ms. Original outfit. Unapproved review, no live integration.','frames':frames}
walk=[]
for i,k in enumerate(order):
 im=poses[k];im.save(out/f'walk-{i:02}.png');walk.append({'name':f'{i} forward {k}','ticks':6,'durationMs':100,'pixels':[rgba.index(p) for p in im.get_flattened_data()]})
idle.save(out/'idle-forward.png')
(src/'hero-forward-walk.sprite.json').write_text(json.dumps(source('HR9 boy Hero forward walk',walk),separators=(',',':'))+'\n')
(src/'hero-forward-idle.sprite.json').write_text(json.dumps(source('HR9 boy Hero proposed idle',[{'name':'Proposed idle, not observed reference idle','ticks':6,'pixels':[rgba.index(p) for p in idle.get_flattened_data()]}]),separators=(',',':'))+'\n')
(src/'masks.json').write_text(json.dumps({'idle':{k:[int(v) for v in a.get_flattened_data()] for k,a in idleMask.items()},'poses':{n:{k:[int(v) for v in a.get_flattened_data()] for k,a in mp.items()} for n,mp in poseMasks.items()}},separators=(',',':'))+'\n')
report={'scope':'forward only; original proposed idle plus walk, unapproved','order':order,'frameDurationMs':[100]*8,'cycleMs':800,'editorTicksPerFrame':6,'editorActualMsPerFrame':6*280896/16777216*1000,'referenceRegistrationTopPadding':14,'headWholeTranslationFromHR6':{'P':-2,'A':0,'C':0,'idle':0},'idleStatus':'Original balanced passing-derived body moved to rest height; no idle pose observed in reference','headReshaped':False,'directionsAdded':False}
for n,im in list(poses.items())+[('idle',idle)]:
 pts={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]};seen={next(iter(pts))};todo=list(seen)
 while todo:
  x,y=todo.pop()
  for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if q in pts and q not in seen:seen.add(q);todo.append(q)
 assert seen==pts,n+' disconnected'
 assert len({p for p in im.get_flattened_data() if p[3]})<=15
report['connectedOriginalPoses']=True
(out/'authoring-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
