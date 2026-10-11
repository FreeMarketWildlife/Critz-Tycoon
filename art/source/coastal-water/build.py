"""Original coast extension: sand, land/deep banks, wash overlays and shaded rocks."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math
ns={};source=Path('art/source/water-terrain/build.py').read_text();exec(source[:source.index('entries=[]')],ns)
inside,masks,base=ns['inside'],ns['masks'],ns['base'];grounds=['grass','path','soil','paving','cliff','sand'];surfaces=ns['surfaces'];frames=[];entries=[]
def sand(f=0):
 im=Image.new('RGBA',(32,32),'#e6ca8c');d=ImageDraw.Draw(im)
 for x,y in [(4,6),(19,3),(26,17),(9,24),(17,14)]:
  x=(x+f*7)%32;y=(y+f*11)%32;d.line((x,y,x+1,y),fill='#c7a76b');d.point((x+1,y-1),fill='#f3dda5')
 return im
def land(g):return sand() if g=='sand' else base(g)
def emit(id,im,**meta):
 n=len(frames);frames.append(im);entries.append(dict(id=id,x=n%32*32,y=n//32*32,w=32,h=32,**meta))
for f in range(4):emit(f'sand.{f}',sand(f),kind='ground')
for a in surfaces:
 for g in grounds:
  for m in masks:
   im=land(g);front=base(a);bank=Image.new('RGBA',(32,32));d=ImageDraw.Draw(bank)
   def sample(x,y):return inside(max(0,min(31,x)),max(0,min(31,y)),m)
   for y in range(32):
    for x in range(32):
     if not inside(x,y,m):continue
     im.putpixel((x,y),front.getpixel((x,y)))
     if g=='sand':continue
     up=next((n for n in range(1,13) if not sample(x,y-n)),None)
     side=next((n for n in range(1,5) if not sample(x-n,y) or not sample(x+n,y) or not sample(x,y+n)),None)
     if 'shallow' in a:
      if up==1 or side==1:d.point((x,y),fill='#797762')
     elif up:
      colors=['#bcaa7d','#998769','#8a7764','#8a7764','#736455','#736455','#6c6053','#625b50','#5c5b51','#416d70','#365f69','#315768']
      col=colors[up-1]
      if 3<=up<=8 and x%9 in [2,3]:col='#5c554c'
      d.point((x,y),fill=col)
     elif side:d.point((x,y),fill=['#a79778','#746858','#446969','#315768'][side-1])
   im.alpha_composite(bank);emit(f'join.{a}.{g}.{m}',im,kind='transition',inner=a,outer=g,neighborMask=m)
   emit(f'bank.{a}.{g}.{m}',bank,kind='bank',inner=a,outer=g,neighborMask=m)
# Sand/ground contact in either direction: all concave/convex corners and caps.
for a,b in [(a,b) for g in grounds[:-1] for a,b in [('sand',g),(g,'sand')]]:
 for m in masks:
  im=land(b);front=land(a)
  for y in range(32):
   for x in range(32):
    if inside(x,y,m):im.putpixel((x,y),front.getpixel((x,y)))
  emit(f'ground.{a}.{b}.{m}',im,kind='surface-transition',inner=a,outer=b,neighborMask=m)
# A periodic wash front advances over wet sand then withdraws; this is NOT a bank.
for m in masks:
 for f in range(32):
  im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im);advance=round(3*math.sin(f*2*math.pi/32));fade=(1+math.cos(f*2*math.pi/32))/2
  for y in range(32):
   for x in range(32):
    near=[]
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
     dist=next((n for n in range(1,8) if 0<=x+dx*n<32 and 0<=y+dy*n<32 and inside(x+dx*n,y+dy*n,m)!=inside(x,y,m)),None)
     if dist:near.append(dist)
    if not near:continue
    signed=min(near)*(1 if inside(x,y,m) else -1);v=signed-advance
    if abs(v)<=1 and (x+y+advance)%9!=0:d.point((x,y),fill='#edf1cc')
    elif -4<=v<-1:d.point((x,y),fill='#91c8c2' if fade>.35 else '#b7ccaa')
    elif not inside(x,y,m) and min(near)<=4:d.point((x,y),fill='#c3b781')
  emit(f'wash.{m}.{f}',im,kind='beach-wash',neighborMask=m,frame=f)
for variant in range(3):
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 if variant==0:pts=[(5,24),(4,19),(8,12),(14,8),(21,9),(27,15),(28,23),(23,28),(10,28)]
 elif variant==1:pts=[(3,25),(5,18),(10,13),(17,15),(20,8),(26,13),(29,24),(24,29),(8,29)]
 else:pts=[(6,25),(4,18),(9,10),(19,6),(25,12),(28,23),(23,28),(10,29)]
 d.polygon(pts,fill='#314f62');d.polygon([(x,max(5,y-2)) for x,y in pts[:-1]],fill='#617c8c');d.polygon([(7,18),(10,12),(15,9),(20,10),(24,15),(19,18),(11,21)],fill='#a7b7b7');d.polygon([(10,14),(15,10),(19,11),(21,14),(17,15),(12,17)],fill='#d5d5bc');d.line([(17,16),(17,21),(22,24)],fill='#456477',width=2);d.line([(9,23),(14,24),(16,22)],fill='#7898a3');emit(f'rock.{variant}',im,kind='rock',shadowBaked=False)
 # A separate water shadow halo with two crisp stepped tones.
 sh=Image.new('RGBA',(32,32));sd=ImageDraw.Draw(sh);sd.polygon([(2,11),(8,5),(23,5),(30,12),(31,23),(25,30),(7,31),(1,23)],fill='#376a83');sd.polygon([(5,17),(10,11),(25,12),(30,22),(24,29),(9,30),(4,24)],fill='#274f6a');emit(f'rock-shadow.{variant}',sh,kind='cast-shadow',separateLayer=True)
sheet=Image.new('RGBA',(1024,math.ceil(len(frames)/32)*32))
for n,im in enumerate(frames):sheet.paste(im,(n%32*32,n//32*32))
out=Path('assets/review/coastal-water');sheet.save(out/'atlas.png');manifest=dict(image='atlas.png',frame=32,assets=entries,masks=masks,grounds=grounds,surfaces=surfaces,loopSeconds=3.2,waterToWaterBank=False)
(out/'atlas.json').write_text(json.dumps(manifest,indent=2)+'\n')
(out/'coast.tsj').write_text(json.dumps(dict(type='tileset',version='1.10',name='Critz coast · WA6 review',tilewidth=32,tileheight=32,tilecount=len(entries),columns=32,image='atlas.png',imagewidth=sheet.width,imageheight=sheet.height,tiles=[dict(id=n,properties=[dict(name=k,type='bool' if isinstance(v,bool) else 'int' if isinstance(v,int) else 'string',value=v) for k,v in e.items() if k not in ['x','y','w','h']]) for n,e in enumerate(entries)]),indent=2)+'\n')
print(len(entries),'coast assets; 47 masks; all 8 water × 6 ground banks + 10 sand/ground joins + 32-frame beach wash')

# Tiled advances the standalone foam overlay on a separate layer.
tiled=json.loads((out/'coast.tsj').read_text())
for n,e in enumerate(entries):
 if e['kind']=='beach-wash' and e['frame']==0:tiled['tiles'][n]['animation']=[dict(tileid=n+f,duration=100) for f in range(32)]
(out/'coast.tsj').write_text(json.dumps(tiled,indent=2)+'\n')
