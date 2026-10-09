"""Original native extension. Existing master is read-only. Deterministic RGBA pixels."""
from PIL import Image, ImageDraw
import json, pathlib, hashlib
root=pathlib.Path(__file__).resolve().parents[3]
out=root/'assets/review/map-editor';out.mkdir(parents=True,exist_ok=True)
m=json.loads((root/'assets/playable/overworld/master.json').read_text());src=Image.open(root/'assets/playable/overworld/master.png').convert('RGBA');by={t['id']:t for t in m['tiles']}
def tile(id):
 t=by[id];return src.crop((t['x'],t['y'],t['x']+32,t['y']+32))
def normal(n):
 for bit,a,b in [(16,1,2),(32,2,4),(64,4,8),(128,8,1)]:
  if not n&a or not n&b:n&=~bit
 return n
masks=sorted(set(normal(n) for n in range(256)))
materials=['grass','path','paving','soil','water','cliff']
base={k:tile('meadow.grass.0' if k=='grass' else 'meadow.path.255.0' if k=='path' else 'ground.'+k) for k in materials if k!='cliff'}
base['cliff']=tile('ground.grass.2')
colors={'path':('#af9369','#e7cc98'),'paving':('#737f85','#e0e2d6'),'soil':('#826e4d','#bca075'),'water':('#4f8372','#b9ddaa'),'cliff':('#766950','#d3bd91')}
entries=[];images=[]
def add(id,im,**meta):
 n=len(entries);entries.append(dict(id=id,x=n%32*32,y=n//32*32,width=32,height=32,**meta));images.append(im)
def within(x,y,m):
 east=x>=16;south=y>=16;dx=31-x if east else x;dy=31-y if south else y
 vx=bool(m&(2 if east else 8));vy=bool(m&(4 if south else 1));diag=bool(m&((32 if east else 64) if south else (16 if east else 128)))
 if not vx and not vy:return dx>=5 and dy>=5 and (dx>=9 or dy>=9 or (dx-9)**2+(dy-9)**2<=16)
 if not vx:return dx>=5
 if not vy:return dy>=5
 if not diag and dx<5 and dy<5:return dx*dx+dy*dy>=25
 return True
for rank,kind in enumerate(materials[1:],1):
 for under in materials[:rank]:
  for mask in masks:
   im=base[under].copy();pix=im.load();fg=base[kind].load()
   for y in range(32):
    for x in range(32):
     if within(x,y,mask):
      pix[x,y]=fg[x,y]
      if any(not within(max(0,min(31,x+dx)),max(0,min(31,y+dy)),mask) for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]):pix[x,y]=tuple(bytes.fromhex(colors[kind][0][1:]))+(255,)
   if kind=='cliff':
    d=ImageDraw.Draw(im)
    # South face is a raised stone retaining wall inside this solid metatile.
    if not mask&4:
     side='left' if not mask&8 else 'right' if not mask&2 else 'center'
     face=tile('cliff.0.'+side)
     # Continuous connected masonry, with a four-pixel ground-contact strip.
     im.paste(face.crop((0,0,32,28)),(0,0))
     d=ImageDraw.Draw(im);d.line((0,27,31,27),fill='#665a43')
    else:
     if not mask&8:
      d.rectangle((3,5,7,31),fill='#8c795e');d.line((7,5,7,31),fill='#d3bd91')
     if not mask&2:
      d.rectangle((24,5,28,31),fill='#766950');d.line((24,5,24,31),fill='#b09b76')
   add(f'blend.{kind}.{under}.{mask}',im,terrain=kind,under=under,neighborMask=mask,blocked=kind in ['water','cliff'])
# Ground-integrated source compositions: renderer bakes these with resolved terrain before use.
for ground in materials:
 for mask in range(16):
  im=base[ground].copy();im.alpha_composite(tile('fence.'+str(mask)));add(f'contact.fence.{ground}.{mask}',im,blocked=True)
# Overlay source tiles remain editable; each is precomposed into a single editor cell cache.
for name in ['stairs','cave','ledge-down','ledge-up','ledge-left','ledge-right']:
 im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
 if name=='stairs':
  d.rectangle((0,0,4,31),fill='#766950');d.rectangle((27,0,31,31),fill='#766950')
  for y in range(0,32,6):d.rectangle((5,y,26,y+4),fill='#cbb994');d.line((5,y,26,y),fill='#efe0b4');d.line((5,y+5,26,y+5),fill='#887d63')
 elif name=='cave':
  d.polygon([(0,31),(0,9),(7,1),(24,1),(31,9),(31,31)],fill='#766950')
  d.polygon([(4,31),(4,12),(10,5),(21,5),(27,12),(27,31)],fill='#303b39')
  d.polygon([(8,31),(8,16),(12,11),(20,11),(23,16),(23,31)],fill='#1e2b2a')
  d.line([(3,9),(8,3),(23,3),(28,9)],fill='#d3bd91',width=2);d.rectangle((6,28,25,31),fill='#b09b76')
 else:
  d.polygon([(0,12),(6,13),(11,11),(20,12),(26,11),(31,12),(31,21),(0,21)],fill='#736449')
  d.polygon([(0,13),(7,15),(13,13),(22,14),(31,13),(31,18),(0,18)],fill='#b49b70')
  d.line([(0,11),(6,12),(11,10),(20,11),(26,10),(31,11)],fill='#d7c28d')
  d.line([(0,22),(31,22)],fill='#65935b')
  im=im.rotate({'ledge-down':0,'ledge-up':180,'ledge-left':270,'ledge-right':90}[name])
 add('feature.'+name,im,behavior=name)
# Full contact sheet variants are available directly in the tile picker.
for ground in materials:
 for name in ['stairs','cave','ledge-down','ledge-up','ledge-left','ledge-right','tallgrass','flowers','bridge']:
  im=base[ground].copy()
  if name in ['tallgrass','flowers','bridge']:over=tile({'tallgrass':'grass.living.0','flowers':'flowers.2','bridge':'bridge.horizontal.center'}[name])
  else:over=images[next(i for i,e in enumerate(entries) if e['id']=='feature.'+name)]
  im.alpha_composite(over);add(f'contact.{name}.{ground}',im,behavior=name,blocked=name.startswith('ledge-'))
sheet=Image.new('RGBA',(1024,((len(entries)+31)//32)*32))
for e,im in zip(entries,images):sheet.paste(im,(e['x'],e['y']))
sheet.save(out/'master.png')
manifest=dict(format='critz-editor-tiles-v1',image='master.png',tileSize=32,sourceSHA256=hashlib.sha256((root/'assets/playable/overworld/master.png').read_bytes()).hexdigest(),approval='M1.ME1 review; not accepted gameplay art',materials=materials,masks=masks,tiles=entries)
(out/'master.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'tiles':len(entries),'masks':len(masks),'size':sheet.size}))
