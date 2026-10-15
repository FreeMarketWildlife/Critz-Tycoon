"""Original hard-pixel tool overlays, native registration; existing Hero copied exactly."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil
root=Path(__file__).resolve().parents[3];out=root/'assets/review/net-r1';out.mkdir(parents=True,exist_ok=True)
ink='#242330';wood='#a87038';light='#fcd080';rim='#68b0e0';mesh='#c0c0c8';cream='#f8f8f8'
directions=['down','up','left','right'];poses=['carry','ready','windup','sweep','strike','follow','recover']
# Coordinates relative to the Hero's unchanged bottom-center frame anchor.
grips={'down':(10,-14),'up':(10,-14),'left':(-8,-14),'right':(8,-14)}
centers={
'down':[(22,-51),(12,9),(17,-54),(17,-12),(0,22),(-7,22),(8,7)],
'up':[(22,-51),(9,-60),(16,-12),(10,-26),(0,-52),(-7,-52),(9,-53)],
'left':[(-20,-51),(-34,-23),(10,-48),(-24,-27),(-34,-12),(-37,-5),(-28,-18)],
'right':[(20,-51),(34,-23),(-10,-48),(24,-27),(34,-12),(37,-5),(28,-18)]}
sheet=Image.new('RGBA',(128*len(poses),128*4));meta={'task':'M1.NET1','approval':'review only','frame':[128,128],'anchor':[64,80],'heroFrame':[32,64],'heroOrigin':[48,16],'directions':directions,'poses':poses,'grips':grips,'centers':centers,'sourceHeroRevision':'73434fcf42aa4fcaa8ef52b6a73d342a5391832c','heroHashes':{}}
for row,d in enumerate(directions):
 for col,pose in enumerate(poses):
  im=Image.new('RGBA',(128,128));draw=ImageDraw.Draw(im);gx,gy=grips[d];cx,cy=centers[d][col];gx+=64;gy+=80;cx+=64;cy+=80
  # Ground strike uses a flattened opening; carry has a tall upright hoop.
  ry=6 if pose in ['strike','follow'] else 11;rx=13 if pose in ['strike','follow'] else 10
  # Extend transparent mesh bag behind the rim with sparse connected cross threads.
  draw.line([(gx,gy),(cx,cy+ry)],fill=ink,width=5);draw.line([(gx,gy),(cx,cy+ry)],fill=wood,width=3);draw.line([(gx-1,gy),(cx-1,cy+ry)],fill=light,width=1)
  box=(cx-rx,cy-ry,cx+rx,cy+ry)
  mask=Image.new('1',(128,128));ImageDraw.Draw(mask).ellipse(box,fill=1)
  for y in range(cy-ry,cy+ry+1):
   for x in range(cx-rx,cx+rx+1):
    if mask.getpixel((x,y)) and (x+y)%6==0:im.putpixel((x,y),tuple(bytes.fromhex(mesh[1:]))+(255,))
  draw.ellipse(box,outline=ink,width=3);draw.ellipse((cx-rx+1,cy-ry+1,cx+rx-1,cy+ry-1),outline=rim,width=2)
  draw.arc((cx-rx+2,cy-ry+2,cx+rx-2,cy+ry-2),190,290,fill=cream,width=1)
  # Small grip band remains beneath the actual existing hand on the upper pass.
  draw.rectangle((gx-2,gy-1,gx+2,gy+2),fill=ink);draw.line((gx-1,gy,gx+1,gy),fill=wood,width=2)
  sheet.paste(im,(col*128,row*128));im.save(out/f'net-{d}-{pose}.png')
 for phase in ['idle','A','P','C']:
  source=root/f'docs/reviews/M1-FM2/hero-{dict(down="south",up="north",left="west",right="east")[d]}-{phase}.png'
  dest=out/f'hero-{d}-{phase}.png';shutil.copyfile(source,dest);meta['heroHashes'][dest.name]=hashlib.sha256(source.read_bytes()).hexdigest()
sheet.save(out/'net-sheet.png');(out/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
# Inspectable nearest grid plate, no grids baked into native exports.
plate=Image.new('RGB',(7*384,4*384),'#dbe3c4');p=ImageDraw.Draw(plate)
for r,d in enumerate(directions):
 for c,pose in enumerate(poses):
  tile=Image.new('RGBA',(128,128));hero=Image.open(out/f'hero-{d}-idle.png');net=Image.open(out/f'net-{d}-{pose}.png')
  if d=='up':tile.alpha_composite(net)
  tile.alpha_composite(hero,(48,16))
  if d!='up':tile.alpha_composite(net)
  tile=tile.resize((384,384),Image.Resampling.NEAREST);plate.paste(tile,(c*384,r*384),tile)
  for x in range(0,385,3):p.line((c*384+x,r*384,c*384+x,r*384+384),fill='#a9ba9c')
  for y in range(0,385,3):p.line((c*384,r*384+y,c*384+384,r*384+y),fill='#a9ba9c')
  p.line((c*384+192,r*384,c*384+192,r*384+384),fill='#b77766')
  for h in [0,10,20,30,40,50,60,64]:
   yy=r*384+(80-h)*3;p.line((c*384+144,yy,c*384+240,yy),fill='#557b64');p.text((c*384+246,yy-3),str(h),fill=ink)
  p.text((c*384+4,r*384+4),d+' '+pose+' / 3x / Y up',fill=ink)
plate.save(root/'docs/reviews/M1-NET1/tool-grid.png')
print('Wrote 28 native net overlays and 16 exact existing Hero frames.')
