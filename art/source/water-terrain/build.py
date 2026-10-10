"""Original 32px water extension: every ordered surface pair, all 47 blob masks."""
from PIL import Image,ImageDraw
from pathlib import Path
import json,math
out=Path('assets/review/water-terrain');out.mkdir(parents=True,exist_ok=True)
types=['still','shallow-still','moving','shallow-moving'];grounds=['grass','path','soil','paving','cliff']
surfaces=[f'{i}.{t}' for i in ['fresh','ocean'] for t in types]
def canon(m):
 for a,b,d in [(1,2,16),(2,4,32),(4,8,64),(8,1,128)]:
  if m&a==0 or m&b==0:m&=~d
 return m
masks=sorted(set(canon(m) for m in range(256)))
def inside(x,y,m):
 east=x>=16;south=y>=16;dx=31-x if east else x;dy=31-y if south else y
 vx=bool(m&(2 if east else 8));vy=bool(m&(4 if south else 1));diag=bool(m&((32 if east else 64) if south else (16 if east else 128)))
 if not vx and not vy:return dx>=5 and dy>=5 and (dx>=11 or dy>=11 or (dx-11)**2+(dy-11)**2<=36)
 if not vx:return dx>=5
 if not vy:return dy>=5
 if not diag and dx<8 and dy<8:return dx*dx+dy*dy>=64
 return True
colors={'grass':'#8bc77a','path':'#dfc28d','soil':'#94745c','paving':'#9fa79c','cliff':'#927d72'}
def base(s,f=0):
 if s in grounds:
  im=Image.new('RGBA',(32,32),colors[s]);d=ImageDraw.Draw(im)
  if s=='paving':
   for y in range(0,32,8):d.line((0,y,31,y),fill='#7d8e89')
  else:
   for x,y in [(5,7),(21,19),(9,27)]:d.line((x,y,x+4,y),fill={'grass':'#75ae68','soil':'#795d4d','cliff':'#665c58'}.get(s,'#c5a474'))
  return im
 shallow='shallow' in s;moving='moving' in s;ocean=s.startswith('ocean')
 col=('#89bac0' if shallow else '#578fa9') if ocean else ('#86bfc2' if shallow else '#529ba8')
 im=Image.new('RGBA',(32,32),col);d=ImageDraw.Draw(im)
 if moving:
  for x,y,w in [(1,4,10),(19,19,9),(8,29,6)]:
   for dx,dy,c in [(0,0,'#538eaa' if ocean else '#428d9e'),(1,1,'#b0d8d4')]:
    for n in range(w):d.point(((x+n+f+dx)%32,(y+dy+(1 if (n+f)%8>5 else 0))%32),fill=c)
 else:
  # Long quiet glints, a closed oscillation rather than a directional current.
  shift=round(2*math.sin(f*math.pi/16))
  for x,y,w in [(3,8,7),(19,24,6)]:d.line(((x+shift)%32,y,(x+shift+w)%32,y),fill='#a8d6d4')
 if shallow:
  for x,y in [(7,17),(24,10),(17,29)]:d.line((x,y,x+2,y),fill='#72aaab')
 return im
entries=[];images=[]
def emit(id,im,**meta):
 n=len(images);images.append(im);entries.append(dict(id=id,x=n%32*32,y=n//32*32,w=32,h=32,**meta))
for s in surfaces:
 for f in range(32):emit(f'{s}.{f}',base(s,f),surface=s,frame=f)
for a in surfaces:
 for b in grounds+surfaces:
  if a==b:continue
  for m in masks:
   im=base(b);front=base(a);lip=Image.new('RGBA',(32,32));ld=ImageDraw.Draw(lip)
   for y in range(32):
    for x in range(32):
     if not inside(x,y,m):continue
     im.putpixel((x,y),front.getpixel((x,y)))
     if b in grounds:
      # Earth cap, recessed face and submerged toe; puddles use a low rim.
      edge=any(not inside(max(0,min(31,x+dx)),max(0,min(31,y+dy)),m) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])
      depth=2 if 'shallow' in a else 7
      above=next((n for n in range(1,depth+1) if not inside(x,max(0,y-n),m)),None)
      if edge:ld.point((x,y),fill='#675b57' if 'shallow' in a else '#514e4e')
      elif above:ld.point((x,y),fill=['#a89479','#847561','#6d665c','#625f58','#535e5b','#42777e','#396d79'][min(6,depth-above)])
      elif any(not inside(max(0,min(31,x+dx*2)),max(0,min(31,y+dy*2)),m) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]):ld.point((x,y),fill='#a3c9b4')
   im.alpha_composite(lip);emit(f'join.{a}.{b}.{m}',im,inner=a,outer=b,neighborMask=m)
   if b in grounds:emit(f'bank.{a}.{b}.{m}',lip,inner=a,outer=b,neighborMask=m)
sheet=Image.new('RGBA',(1024,math.ceil(len(images)/32)*32))
for n,im in enumerate(images):sheet.paste(im,(n%32*32,n//32*32))
sheet.save(out/'atlas.png')
(out/'atlas.json').write_text(json.dumps(dict(image='atlas.png',frame=32,assets=entries,surfaces=surfaces,grounds=grounds,masks=masks,loopSeconds=3.2),indent=2)+'\n')
(out/'water.tsj').write_text(json.dumps(dict(type='tileset',version='1.10',name='Critz water extension · WA3 review',tilewidth=32,tileheight=32,tilecount=sheet.width*sheet.height//1024,columns=32,image='atlas.png',imagewidth=sheet.width,imageheight=sheet.height,tiles=[dict(id=n,properties=[dict(name=k,type='int' if isinstance(v,int) else 'string',value=v) for k,v in e.items() if k not in ['x','y','w','h']]) for n,e in enumerate(entries)]),indent=2)+'\n')
print(f'{len(entries)} tiles; {len(masks)} masks; {len(surfaces)} surfaces; all 96 ordered surface/ground pairs')
