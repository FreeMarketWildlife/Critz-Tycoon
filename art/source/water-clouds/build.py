"""Original stepped cloud silhouettes, three opaque colors, east-to-west light."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math
out=Path('assets/review/water-clouds');out.mkdir(parents=True,exist_ok=True)
W,H=96,64;palette=['#82b6c0','#b8d9d6','#e3efe4']
shapes=[[(9,43),(4,41),(1,37),(0,32),(2,28),(6,25),(12,25),(12,21),(15,18),(20,17),(26,18),(28,12),(32,9),(38,8),(43,9),(47,14),(52,14),(53,8),(58,4),(65,3),(72,5),(77,10),(78,17),(84,18),(88,22),(87,28),(91,29),(95,34),(95,39),(92,43),(88,46),(77,49),(65,48),(57,50),(46,50),(39,48),(31,50),(20,48),(12,47)],
[(7,40),(3,37),(2,32),(4,27),(9,24),(16,25),(18,20),(22,17),(28,16),(34,18),(37,13),(41,10),(47,9),(54,12),(58,19),(63,18),(69,20),(73,25),(72,29),(79,28),(84,32),(85,37),(82,41),(75,44),(65,44),(58,46),(46,45),(36,47),(25,45),(17,46),(10,43)],
[(12,41),(7,38),(6,33),(8,28),(13,25),(19,26),(20,21),(24,17),(30,16),(36,18),(40,23),(46,23),(48,17),(52,14),(58,14),(64,17),(67,23),(72,23),(77,26),(80,31),(78,37),(73,41),(66,42),(56,44),(47,42),(38,45),(27,44),(19,43)]]
masks=[]
for polygon in shapes:
 m=Image.new('1',(W,H));ImageDraw.Draw(m).polygon(polygon,fill=1);masks.append(m)
frames=[];entries=[]
for variant,mask in enumerate(masks):
 for minute in range(600,901):
  # Proposed Critz solar arc: 6am east, noon overhead, 6pm west.
  angle=math.pi*(minute-360)/720;lx,ly=math.cos(angle),-math.sin(angle)
  im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
  def occupied(x,y):return 0<=x<W and 0<=y<H and mask.getpixel((x,y))
  for y in range(H):
   for x in range(W):
    if not occupied(x,y):continue
    lit=not occupied(round(x+lx*9),round(y+ly*9))
    dark=not occupied(round(x-lx*7),round(y-ly*7))
    # Broad connected lighting clusters, with low scalloped underside accents.
    color=palette[2] if lit else palette[0] if dark else palette[1]
    d.point((x,y),fill=color)
  n=len(frames);frames.append(im);entries.append(dict(id=f'cloud.{variant}.{minute}',x=n%12*W,y=n//12*H,w=W,h=H))
sheet=Image.new('RGBA',(12*W,math.ceil(len(frames)/12)*H))
for n,im in enumerate(frames):sheet.paste(im,(n%12*W,n//12*H))
sheet.save(out/'atlas.png');(out/'atlas.json').write_text(json.dumps(dict(image='atlas.png',width=W,height=H,palette=palette,variants=3,minuteStart=600,minuteEnd=900,assets=entries),indent=2)+'\n')
# Native review strip shows actual vertical inversion at 10,12,14:59.
strip=Image.new('RGBA',(W*3,H*3),'#529ba8')
for v in range(3):
 for col,minute in enumerate([600,720,899]):strip.alpha_composite(frames[v*301+minute-600].transpose(Image.Transpose.FLIP_TOP_BOTTOM),(col*W,v*H))
strip.save(out/'reflected-light-study.png');print(f'{len(frames)} original cloud frames, 3 colors + transparency, 96×64, 3 silhouettes')
