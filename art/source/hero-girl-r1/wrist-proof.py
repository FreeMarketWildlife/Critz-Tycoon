"""Bounded wrist recolor proof: actual pixels, distinct material ownership."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-GH1';dest=out/'wrist-correction';meta=json.loads((Path(__file__).parent/'construction.json').read_text());before=Image.open(dest/'before.png').convert('RGBA');after=Image.open(out/'girl-front-idle.png').convert('RGBA');c6=Image.open(root/'assets/review/idle-collection-v1/hero-girl.png').convert('RGBA');hr14=Image.open(root/'docs/reviews/M1-HR14/hero-south-idle.png').convert('RGBA');dummy=Image.open(out/'girl-front-construction.png').convert('RGBA')
skin={(168,112,56),(196,142,74),(120,72,32)};cream=(247,237,204);ink=(32,16,8);dark=(17,17,26)
region={(x,y) for y in range(47,54) for x in list(range(3,10))+list(range(22,29))}
def count(im):
 from collections import Counter
 c=Counter('#%02x%02x%02x'%im.getpixel(p)[:3] for p in region if im.getpixel(p)[3]);return dict(sorted(c.items()))
def mask(im,points):
 q=Image.new('RGBA',(32,64))
 for p in points:q.putpixel(p,im.getpixel(p))
 return q
def put(im,q,x,y,scale):
 q=q.resize((32*scale,64*scale),Image.Resampling.NEAREST);im.paste(q,(x,y),q)
def anchor(d,x,y,s):
 d.line((x,y+64*s,x+32*s,y+64*s),fill='#748894');d.line((x+16*s-3,y+64*s,x+16*s+3,y+64*s),fill='#d84f5b')
p=Image.new('RGB',(1600,870),'#bed4d5');d=ImageDraw.Draw(p)
for n,(name,im) in enumerate([('SELECTED C6 native',''),('HR14 shared-body source',''),('GH1 before / 3a94f48',''),('GH1 wrist correction',''),('CURRENT construction map','')]):
 q=[c6,hr14,before,after,dummy][n];x=n*320;d.text((x+8,8),name,fill='#253340');put(p,q,x+92,38,4);anchor(d,x+92,38,4);put(p,q,x+140,315,1);anchor(d,x+140,315,1)
# Five distinct current material masks; none manufactures a hidden joint.
hand=[tuple(v) for v in meta['palmCells']];arm=[tuple(v) for v in meta['exposedArmCells']];trim=[tuple(v) for v in meta['cuffCells']];high=[tuple(v) for v in meta['garmentHighlightCells']];edge=[p for p in region if after.getpixel(p)[:3] in (ink,dark)]
for n,(name,pts) in enumerate([('EXPOSED ARM material',arm),('HAND material',hand),('RETAINED sleeve trim',trim),('OTHER clothing highlights',high),('UNCHANGED ink/navy edges',edge)]):
 x=n*320;d.text((x+8,415),name,fill='#253340');put(p,mask(after,pts),x+92,443,4);anchor(d,x+92,443,4);d.text((x+8,717),str(len(pts))+' actual cells / original RGBA',fill='#253340')
d.text((10,767),'One front only; fixed32x64 / edgeanchor16,64; native + nearest4x. Alpha, head/ears and rows54+ unchanged.',fill='#253340');d.text((10,790),'Skin uses selected C6 ramp. Upper cream sleeve trim retained; below-sleeve wrist islands become coherent brown skin.',fill='#253340');d.text((10,813),'Arm/hand are authored visible material regions, not measured joints. Two inward row53 pale cloth cells become shirt coral.',fill='#253340');p.save(dest/'source-before-after-actual-masks.png')
p=Image.new('RGB',(1200,660),'#eee7d5');d=ImageDraw.Draw(p)
for col,im in enumerate((before,after)):
 x=col*600;d.text((x+8,8),('BEFORE','AFTER')[col]+' / actual exposed skin, cream, coral, edges',fill='#253340');put(p,im,x+80,30,4);anchor(d,x+80,30,4)
 for i,(name,pts) in enumerate([('skin',[p for p in region if im.getpixel(p)[:3] in skin]),('cream',[p for p in region if im.getpixel(p)[:3]==cream]),('coral',[p for p in region if im.getpixel(p)[:3] in ((250,128,120),(201,86,98))]),('ink/navy',[p for p in region if im.getpixel(p)[:3] in (ink,dark)])]):
  xx=x+i*145;d.text((xx+4,328),name+' '+str(len(pts)),fill='#253340');put(p,mask(im,pts),xx+8,354,4);anchor(d,xx+8,354,4)
p.save(dest/'before-after-region-materials.png')
changes=[{'cell':list(p),'before':'#%02x%02x%02x'%before.getpixel(p)[:3],'after':'#%02x%02x%02x'%after.getpixel(p)[:3]} for y in range(64) for x in range(32) if before.getpixel(p:=(x,y))!=after.getpixel(p)]
assert all(tuple(c['cell']) in region for c in changes)
assert before.getchannel('A').tobytes()==after.getchannel('A').tobytes()
assert before.crop((0,0,32,45)).tobytes()==after.crop((0,0,32,45)).tobytes()
assert before.crop((0,54,32,64)).tobytes()==after.crop((0,54,32,64)).tobytes()
assert all(before.getpixel(pt)==after.getpixel(pt) for pt in edge)
assert all(after.getpixel(pt)[:3] in skin for pt in hand+arm)
report={'scope':'M1.GH1 bounded front wrist material correction only','beforeSource':'3a94f482e6b6d152b58e4e90e371ee314731feb8','region':'x3..9 and22..28, y47..53 inclusive','regionCounts':{'selectedC6':count(c6),'before':count(before),'after':count(after)},'changedCells':changes,'armCells':arm,'handCells':hand,'retainedCuffCells':trim,'otherClothingHighlightCells':high,'protectedShadowEdgeCells':edge,'checks':{'onlyBoundedMaterialCellsChanged':True,'allAlphaExact':True,'headEarsThrough44Exact':True,'lowerRows54PlusExact':True,'allInkNavyEdgesExact':True,'armHandOnlyC6SkinRamp':True},'decision':'Keep upper cream sleeve/cuff at47-48. Below it49-53 coherent C6 skin at non-ink/non-navy outer arm/hand sites, shaded bottom. Two inward pale garment cells22,53/23,53 become coral cloth. No global cream recolor or complexion change.','approval':'Awaiting independent visual review; directions/walks denied; no Library/runtime/save/deployment changes'}
(dest/'material-decision.json').write_text(json.dumps(report,indent=2)+'\n');print(len(changes),'changed material cells; hand/arm',len(hand),len(arm),'retained cuff',len(trim))
