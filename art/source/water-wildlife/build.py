"""Original native-pixel tiles. No reference pixels or image resampling."""
from PIL import Image,ImageDraw
from pathlib import Path
import json
out=Path('assets/review/water-wildlife');out.mkdir(parents=True,exist_ok=True)
sheet=Image.new('RGBA',(32*8,32*3));ids=[]
def emit(im,id):
 n=len(ids);sheet.paste(im,((n%8)*32,(n//8)*32));ids.append({'id':id,'x':(n%8)*32,'y':(n//8)*32,'w':32,'h':32})
for f in range(8):
 im=Image.new('RGBA',(32,32),'#438e9b');d=ImageDraw.Draw(im)
 for x,y,w in [(1,4,10),(19,19,9),(8,29,6)]:
  for dx,dy,col in [(0,0,'#337886'),(1,1,'#579fa7'),(3,2,'#73b7b8')]:
   for n in range(w):
    xx=(x+n+f+dx)%32; yy=(y+dy+(1 if (n+f)%8>5 else 0))%32;d.point((xx,yy),fill=col)
 emit(im,f'water.{f}')
rock=Image.new('RGBA',(32,32));d=ImageDraw.Draw(rock)
d.polygon([(3,22),(5,14),(10,9),(20,8),(27,13),(30,22),(26,27),(7,28)],fill='#435e67')
d.polygon([(5,21),(7,14),(11,10),(20,10),(25,14),(27,21),(24,24),(9,25)],fill='#80969a')
d.polygon([(8,16),(12,11),(19,11),(23,15),(20,18),(10,19)],fill='#b1b9a5')
d.line([(10,20),(16,19),(19,22),(24,21)],fill='#617a82',width=1);emit(rock,'rock')
for f in range(4):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 # Paired legs with two small swimming poses; shell and material shading, no cast shadow.
 for x,y in [(9,13),(21,13),(9,22),(21,22)]:d.rectangle((x,y+(f%2),x+2,y+3+(f%2)),fill='#54794d')
 d.rectangle((14,8,18,12),fill='#46694b');d.rectangle((15,7,17,10),fill='#8eae69');d.point((17,8),fill='#262f2c');d.point((18,9),fill='#dfc56e')
 d.polygon([(10,13),(13,11),(20,12),(23,16),(22,22),(18,25),(12,23),(9,19)],fill='#314c40')
 d.polygon([(11,14),(14,12),(19,13),(21,16),(20,21),(17,23),(13,21),(11,18)],fill='#749151')
 d.line([(15,13),(15,17),(11,18)],fill='#465f3d');d.line([(15,17),(20,16)],fill='#465f3d');d.line([(15,17),(17,22)],fill='#465f3d');d.line([(17,20),(20,20)],fill='#465f3d');d.point((13,14),fill='#b0b66b');d.rectangle((15,25,16,27),fill='#688653');emit(im,f'turtle.{f}')
for f in range(3):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 d.polygon([(5,17),(2,12+f),(2,20-f),(6,18)],fill='#425762')
 d.polygon([(6,15),(13,12),(19,13),(23,16),(20,20),(12,21),(6,18)],fill='#2f5865')
 d.polygon([(7,16),(13,13),(19,14),(21,16),(18,18),(12,19)],fill='#b9cab2');d.line([(9,18),(17,19),(19,17)],fill='#79a6a2');d.polygon([(12,13),(15,9),(16,13)],fill='#68868b');d.point((19,15),fill='#293941');d.point((20,16),fill='#e7d4a3');emit(im,f'fish.{f}')
for f in range(4):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im);r=5+f*3
 for x,y,w in [(16-r,20,5),(16+r-4,20,5),(10,18-f,3),(20,15-f*2,2)]:d.rectangle((x,y,x+w-1,y),fill='#b7ded1')
 emit(im,f'splash.{f}')
sheet.save(out/'atlas.png');(out/'atlas.json').write_text(json.dumps({'image':'atlas.png','frame':32,'assets':ids},indent=2)+'\n')
print(f'{len(ids)} original 32px assets, binary alpha')

frames=[sheet.crop((f*32,0,(f+1)*32,32)) for f in range(8)]
frames[0].save(out/"water.gif",save_all=True,append_images=frames[1:],duration=180,loop=0,disposal=2)
