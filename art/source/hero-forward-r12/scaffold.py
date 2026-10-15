"""Abstract segmented construction dummy; all hidden joints are PROPOSED."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR12'
order=['A','A','P','P','C','C','P','P']
colors={'outline':'#253340','head':'#b8dce0','ears':'#ed8ccd','torso':'#4ac2b0','pelvis':'#9b83d4','arms':'#f1a566','legs':'#65a6de','feet':'#f1d171','joint':'#f5f1d9'}
frames={};maps={}
def build(pose,bodyDy,headDy,mirror=False):
 im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im)
 points=({'shoulderL':(9,47),'shoulderR':(22,47),'elbowL':(7,50),'elbowR':(24,50),'wristL':(7,51),'wristR':(24,51),'hipL':(13,55),'hipR':(18,55),'kneeL':(12,57),'kneeR':(19,57),'ankleL':(11,59),'ankleR':(20,59),'footL':(11,60),'footR':(20,60),'strapL':(10,46),'strapR':(21,46),'packAttach':(23,47)} if pose=='P' else {'shoulderL':(10,49),'shoulderR':(23,49),'elbowL':(7,51),'elbowR':(24,50),'wristL':(7,53),'wristR':(24,51),'hipL':(14,55),'hipR':(19,55),'kneeL':(12,56),'kneeR':(18,58),'ankleL':(12,58),'ankleR':(18,61),'footL':(12,58),'footR':(18,62),'strapL':(10,49),'strapR':(24,48),'packAttach':(26,48)})
 points={k:(x,y+bodyDy) for k,(x,y) in points.items()}
 points.update({'earL':(6,39+headDy),'earR':(25,39+headDy),'neck':(16,45+headDy),'headCenter':(16,35+headDy),'torsoCenter':(16,50+bodyDy)})
 if pose!='P':points['packAttach']=(27,45+bodyDy+2)
 def poly(pts,key):d.polygon(pts,fill=colors[key]);d.line(pts+[pts[0]],fill=colors['outline'])
 def bar(a,b,key,width=4):d.line([points[a],points[b]],fill=colors['outline'],width=width+2);d.line([points[a],points[b]],fill=colors[key],width=width)
 for side in ('L','R'):
  bar('hip'+side,'knee'+side,'legs',3);bar('knee'+side,'ankle'+side,'legs',3)
  x,y=points['foot'+side];poly([(x-2,y-1),(x+1,y-1),(x+2,y),(x+1,y+1),(x-2,y+1),(x-3,y)],'feet')
 # Neutral geometric torso and hip block; no literal unclothed body details.
 sy=min(points['shoulderL'][1],points['shoulderR'][1]);hy=min(points['hipL'][1],points['hipR'][1])
 poly([(10,sy-1),(21,sy-1),(23,sy+2),(21,hy),(10,hy),(8,sy+2)],'torso')
 poly([(11,hy-1),(20,hy-1),(21,hy+1),(19,hy+2),(12,hy+2),(10,hy+1)],'pelvis')
 for side in ('L','R'):bar('shoulder'+side,'elbow'+side,'arms',3);bar('elbow'+side,'wrist'+side,'arms',3)
 d.rectangle((13,42+headDy,18,sy+1),fill=colors['outline'])
 d.rectangle((14,43+headDy,17,sy),fill=colors['head'])
 # Featureless mechanical head scaffold is an authored proposal under hair,
 # not a recovered skull measurement. Its attachment sites remain fixed.
 poly([(11,27+headDy),(20,27+headDy),(24,30+headDy),(25,34+headDy),(25,40+headDy),(21,44+headDy),(10,44+headDy),(6,40+headDy),(6,34+headDy),(7,30+headDy)],'head')
 for side in ('L',):
  x,y=points['ear'+side];poly([(x-1,y-2),(x,y-2),(x+1,y-1),(x+1,y+1),(x,y+2),(x-1,y+2),(x-2,y+1),(x-2,y-1)],'ears')
 # Explicit bilateral head/ear raster, avoiding polygon-outline asymmetry.
 # This is only the proposed featureless dummy, never a Hero head restyle.
 for yy in range(27+headDy,45+headDy):
  for xx in range(16):im.putpixel((31-xx,yy),im.getpixel((xx,yy)))
 for key,(x,y) in points.items():
  if key not in ('headCenter','torsoCenter','earL','earR','neck','strapL','strapR','packAttach'):d.point((x,y),fill=colors['joint'])
 if mirror:
  im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT);points={k:(31-x,y) for k,(x,y) in points.items()}
  # L/R denote viewer sides for these all-forward poses, stable across phases.
  for stem in ('ear','shoulder','elbow','wrist','hip','knee','ankle','foot','strap'):
   points[stem+'L'],points[stem+'R']=points[stem+'R'],points[stem+'L']
  points['neck']=(16,45+headDy);points['headCenter']=(16,35+headDy);points['torsoCenter']=(16,50+bodyDy)
 return im,points
for pose,bd,hd,mir in [('A',-2,0,False),('P',-2,-2,False),('C',-2,0,True),('idle',0,0,False)]:
 im,points=build('P' if pose in ('P','idle') else 'A',bd,hd,mir);frames[pose]=im;maps[pose]={k:list(v) for k,v in points.items()}
frames['idle'].save(out/'mannequin-idle.png')
for i,p in enumerate(order):frames[p].save(out/f'mannequin-{i:02}.png')
palette=[None]+list(colors.values());rgba=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in palette[1:]]
project={'format':'fmw-sprite','version':1,'name':'HR12 neutral construction mannequin — proposed landmarks','preset':'character','width':32,'height':64,'palette':palette,'bank':'custom','notes':'Abstract segmented featureless drawing dummy, no anatomical/sexual detail. All hidden joints/skull contours PROPOSED for original construction; not measured source anatomy. Same32x64 ground registration. No game integration.','frames':[{'name':f'{i} {p}','ticks':6,'pixels':[rgba.index(px) for px in frames[p].get_flattened_data()]} for i,p in enumerate(order)]}
(src/'mannequin.sprite.json').write_text(json.dumps(project,separators=(',',':'))+'\n')
(src/'scaffold.json').write_text(json.dumps({'status':'PROPOSED construction/attachment landmarks, not measured source anatomy','base':'HR10-BODY d158c3e','canvas':[32,64],'groundAnchor':[16,64],'partColors':colors,'headDy':{'A':0,'P':-2,'C':0,'idle':0},'bodyDy':{'A':-2,'P':-2,'C':-2,'idle':0},'poses':maps},indent=2)+'\n')
print('Neutral mannequin and proposed attachment scaffold saved for all8frames and idle.')
