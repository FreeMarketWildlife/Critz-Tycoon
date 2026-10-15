"""Original forward-only HR12 pixels. No reference pixels/masks are read by this authoring script."""
from PIL import Image,ImageDraw
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR12';src=Path(__file__).parent
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
  # One overlapped cuff/ankle/foot mass per side: no full-width skin ring,
  # separate shoe-top rail or broad rectangular toe under a rectangular cuff.
  poly('leftLeg',[(10,54),(14,54),(14,56),(13,58),(10,59),(9,57)],'b',edge='n')
  poly('rightLeg',[(21,54),(17,54),(17,56),(18,58),(21,59),(22,57)],'b',edge='n')
  fill([(11,57),(13,57),(12,59),(11,58)],'s')
  fill([(20,57),(18,57),(19,59),(20,58)],'s')
  poly('leftShoe',[(11,58),(13,59),(14,60),(12,61),(10,61),(9,60),(9,59)],'n')
  poly('rightShoe',[(20,58),(18,59),(17,60),(19,61),(21,61),(22,60),(22,59)],'n')
  dot(11,60,'b');dot(20,60,'b')
  poly('shorts',[(10,53),(21,53),(22,55),(20,57),(17,56),(16,55),(15,55),(14,56),(11,57),(9,55)],'b',edge='n')
  fill([(16,54),(21,54),(21,55),(19,56),(16,55)],'n')
  poly('leftArm',[(6,48),(8,48),(9,50),(8,52),(6,52),(5,51),(5,49)],'s')
  poly('rightArm',[(25,48),(23,48),(22,50),(23,52),(25,52),(26,51),(26,49)],'s')
  line([(6,49),(6,50)],'S');dot(24,51,'d')
  poly('shirt',[(11,45),(20,45),(24,46),(26,48),(24,49),(22,48),(22,53),(20,55),(11,55),(9,53),(9,48),(7,49),(5,48),(7,46)],'r')
  fill([(7,46),(9,46),(9,47),(7,48),(6,48)],'c');fill([(22,46),(24,46),(25,48),(23,48)],'C')
  fill([(13,46),(18,46),(20,48),(18,50),(13,50),(11,48)],'c')
  fill([(20,49),(21,50),(21,53),(18,54),(17,54),(19,52)],'v')
  poly('collar',[(12,44),(19,44),(19,46),(17,47),(14,47),(12,46)],'d');line([(14,46),(17,46)],'c')
 else:
  # A: right lower/forward foot, left upper/overlapped foot; left arm forward.
  poly('trailingLeg',[(10,54),(15,54),(16,57),(14,59),(11,59),(10,57)],'b',edge='n')
  poly('trailingShoe',[(12,57),(14,58),(13,59),(11,59),(10,58)],'n');dot(12,58,'b')
  poly('leadingLeg',[(16,55),(21,55),(21,58),(20,60),(17,61),(16,59)],'b',edge='n')
  fill([(18,59),(20,59),(19,61),(18,60)],'s')
  poly('leadingShoe',[(18,60),(20,61),(20,62),(19,63),(17,63),(16,62),(17,61)],'n')
  dot(18,62,'C')
  poly('shorts',[(12,54),(22,54),(23,57),(20,59),(16,58),(13,58),(10,56)],'b',edge='n')
  fill([(17,55),(21,55),(22,57),(20,58),(17,57)],'n')
  # High side cluster adapts original daypack; not an inferred bare hand raised to jaw.
  poly('daypackEdge',[(25,45),(27,45),(28,47),(28,50),(26,52),(24,50),(24,47)],'b')
  line([(26,47),(26,49)],'B')
  poly('farArm',[(22,48),(25,48),(26,50),(25,52),(23,52),(22,50)],'d')
  poly('nearArm',[(6,50),(8,49),(9,50),(9,53),(7,54),(5,53),(5,51)],'s')
  line([(6,51),(6,52)],'S')
  poly('shirt',[(12,47),(21,47),(25,49),(25,51),(23,52),(22,56),(19,58),(13,57),(10,55),(9,52),(6,51),(6,49),(9,48)],'r')
  fill([(8,49),(10,49),(10,50),(8,51),(7,51)],'c')
  fill([(23,49),(24,50),(23,51),(22,50)],'C')
  fill([(14,48),(19,48),(21,50),(19,52),(13,51),(12,49)],'c')
  fill([(21,51),(22,52),(21,55),(18,57),(16,56),(18,54)],'v')
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
def source(name,frames):return {'format':'fmw-sprite','version':1,'name':name,'preset':'character','width':32,'height':64,'palette':colors,'bank':'custom','notes':'HR12 FORWARD ONLY, confirmed user GIF compact motion reference. HR9 head/ears preserved exactly with existing translations. No mouth/nose. Source eight100ms frames; editor6 ticks approximate100.456ms, GIF review exact100ms. Original outfit. Unapproved review, no live integration.','frames':frames}
walk=[]
for i,k in enumerate(order):
 im=poses[k];im.save(out/f'walk-{i:02}.png');walk.append({'name':f'{i} forward {k}','ticks':6,'durationMs':100,'pixels':[rgba.index(p) for p in im.get_flattened_data()]})
idle.save(out/'idle-forward.png')
(src/'hero-forward-walk.sprite.json').write_text(json.dumps(source('HR12 boy Hero forward walk',walk),separators=(',',':'))+'\n')
(src/'hero-forward-idle.sprite.json').write_text(json.dumps(source('HR12 boy Hero proposed idle',[{'name':'Proposed idle, not observed reference idle','ticks':6,'pixels':[rgba.index(p) for p in idle.get_flattened_data()]}]),separators=(',',':'))+'\n')
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
