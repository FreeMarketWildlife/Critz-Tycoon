"""OM3 material-only saved-pixel audit; exclusive OM3 outputs only."""
from pathlib import Path
from collections import deque
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=ROOT/'docs/reviews/M1-OM3'
checks=[];deltas={}
def check(n,v):
 assert v,n
 checks.append(n)
def rgba(p):return Image.open(p).convert('RGBA')
def connected(cells):
 if not cells:return False
 seen={next(iter(cells))};q=deque(seen)
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if p in cells and p not in seen:seen.add(p);q.append(p)
 return seen==cells
for p,h in json.loads((HERE/'read-only-guards.json').read_text()).items():check('protected '+p,hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h)
combined=json.loads((HERE/'mom-four-idles.sprite.json').read_text())
for i,direction in enumerate(['south','north','west','east']):
 old=rgba(OUT/'history-om2'/f'idle-{direction}.png');im=rgba(OUT/f'idle-{direction}.png');src=json.loads((HERE/direction/'layers.json').read_text());prev=json.loads((HERE/'history-om2'/direction/'layers.json').read_text())
 check(direction+' anchor and frame exact',src['anchor']==prev['anchor']==[16,64] and src['frame']==prev['frame']==[32,64])
 check(direction+' whole silhouette exact',im.getchannel('A').tobytes()==old.getchannel('A').tobytes())
 check(direction+' full feet exact',im.crop((0,58,32,64)).tobytes()==old.crop((0,58,32,64)).tobytes())
 for n in src['order']:
  layer=rgba(HERE/direction/(n+'.png'));before=rgba(HERE/'history-om2'/direction/(n+'.png'))
  check(direction+' layer alpha exact '+n,layer.getchannel('A').tobytes()==before.getchannel('A').tobytes())
  if direction in ['south','north'] or n!='torso':check(direction+' protected layer '+n,layer.tobytes()==before.tobytes())
 frame=combined['frames'][i];decoded=Image.new('RGBA',(32,64));decoded.putdata([(0,0,0,0) if v==0 else tuple(bytes.fromhex(combined['palette'][v][1:]))+(255,) for v in frame['pixels']]);check(direction+' combined project exact',decoded.tobytes()==im.tobytes())
 changed=[]
 for y in range(64):
  for x in range(32):
   a=old.getpixel((x,y));b=im.getpixel((x,y))
   if a!=b:
    changed.append({'cell':[x,y],'before':'#'+bytes(a[:3]).hex(),'after':'#'+bytes(b[:3]).hex(),'owner':'torso'})
    westx=x if direction=='west' else 31-x
    check(direction+f' bounded torso recolor {x},{y}',direction in ['west','east'] and 12<=westx<=17 and 44<=y<=54 and a[3]==b[3]==255)
 if direction in ['south','north']:check(direction+' PNG bytes exact', (OUT/f'idle-{direction}.png').read_bytes()==(OUT/'history-om2'/f'idle-{direction}.png').read_bytes())
 else:
  cream={(x,y) for x,y,c in src['layers']['torso'] if c in ['#f7edcc','#d9cba7']}
  check(direction+' continuous cream neckline to waist',connected(cream) and min(y for x,y in cream)==44 and max(y for x,y in cream)==54)
  check(direction+' cream separated from leading lobe',all(14<=(x if direction=='west' else 31-x)<=16 for x,y in cream))
 deltas[direction]=changed
west=rgba(HERE/'west/torso.png');east=rgba(HERE/'east/torso.png');check('equivalent East wardrobe turn',west.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()==east.tobytes())
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
board=Image.new('RGB',(900,420),'#e8e4d7');d=ImageDraw.Draw(board)
d.text((15,10),'M1.OM3 MATERIAL ONLY / fixed alpha and body / UNAPPROVED',font=font,fill='#252431')
for i,direction in enumerate(['west','east']):
 for j,sub in enumerate(['history-om2','']):
  im=rgba(OUT/sub/f'idle-{direction}.png');x=20+i*450+j*210
  d.text((x,40),direction.upper()+(' OM2 BEFORE' if j==0 else ' OM3 AFTER'),font=font,fill='#252431')
  big=im.resize((128,256),Image.Resampling.NEAREST);board.paste(big,(x+20,65),big);board.paste(im,(x+65,330),im)
d.text((15,398),'Native1x + nearest4x. Cream becomes continuous neckline-to-waist inset.',font=font,fill='#252431')
board.save(OUT/'before-after.png')
bg=Image.new('RGB',(1050,440));dr=ImageDraw.Draw(bg)
for row,color in enumerate(['#eeeeea','#26303c']):
 dr.rectangle((0,row*220,1049,(row+1)*220),fill=color)
 for i,direction in enumerate(['south','north','west','east']):
  im=rgba(OUT/f'idle-{direction}.png');x=15+i*260;fg='#252431' if row==0 else '#eeeeea';dr.text((x,row*220+8),direction.upper()+' native +3x',font=font,fill=fg);bg.paste(im,(x+8,row*220+45),im);big=im.resize((96,192),Image.Resampling.NEAREST);bg.paste(big,(x+75,row*220+25),big)
bg.save(OUT/'background-inspection.png')
# Material-only map, no reference pixels; magenta marks actual changed cells.
plate=Image.new('RGB',(850,390),'#e8e4d7');dr=ImageDraw.Draw(plate);dr.text((15,10),'Actual visible changed cells / same alpha / torso owner only',font=font,fill='#252431')
for i,direction in enumerate(['west','east']):
 im=rgba(OUT/f'idle-{direction}.png');mask=Image.new('RGBA',(32,64))
 for c in deltas[direction]:mask.putpixel(tuple(c['cell']),(220,40,120,255))
 for j,png in enumerate([im,mask]):
  big=png.resize((160,320),Image.Resampling.NEAREST);x=20+i*420+j*190;plate.paste(big,(x,45),big);dr.text((x,368),direction+(' final' if j==0 else ' changed'),font=font,fill='#252431')
plate.save(OUT/'material-changed-cells.png')
report={'task':'M1.OM3','checksPassed':len(checks),'checks':checks,'deltas':deltas,'scope':'Only profile torso material RGBA; all alpha and other layers fixed','appearanceAccepted':False}
(HERE/'continuation-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checksPassed':len(checks),'changedCells':{k:len(v) for k,v in deltas.items()}}))
