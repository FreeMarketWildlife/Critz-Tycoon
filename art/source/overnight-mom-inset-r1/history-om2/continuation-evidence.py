"""OM2 bounded source-delta audit and native/integer review evidence; own folders only."""
from pathlib import Path
from collections import deque
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=ROOT/'docs/reviews/M1-OM2'
checks=[];deltas={}
def check(n,v):
 assert v,n
 checks.append(n)
def rgba(p):return Image.open(p).convert('RGBA')
def connected(cells):
 if not cells:return False
 q=deque([next(iter(cells))]);seen=set(q)
 while q:
  x,y=q.popleft()
  for c in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if c in cells and c not in seen:seen.add(c);q.append(c)
 return seen==cells
for p,h in json.loads((HERE/'read-only-guards.json').read_text()).items():check('read-only '+p,hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h)
checkpoint=json.loads((ROOT/'local-review/overnight-continuation-checkpoint/manifest.json').read_text())
for f in checkpoint['files']:
 if f['path'].startswith(('art/source/overnight-mom-r1/','docs/reviews/M1-OM1/')):check('checkpoint '+f['path'],hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256'])
for direction in ['south','north','west','east']:
 old=rgba(OUT/'history-v1'/f'idle-{direction}.png');now=rgba(OUT/f'idle-{direction}.png')
 src=json.loads((HERE/direction/'layers.json').read_text());prev=json.loads((HERE/'history-v1'/direction/'layers.json').read_text())
 check(direction+' registration unchanged',src['anchor']==prev['anchor']==[16,64] and src['frame']==prev['frame']==[32,64])
 for n in src['order']:
  if direction in ['west','east'] and n=='far-arm':
   check(direction+' hidden far-arm empty',not src['layers'][n] and rgba(HERE/direction/(n+'.png')).getbbox() is None)
  else:check(direction+' protected real layer '+n,(HERE/direction/(n+'.png')).read_bytes()==(HERE/'history-v1'/direction/(n+'.png')).read_bytes())
 changed=[];oldfar=rgba(HERE/'history-v1'/direction/'far-arm.png')
 for y in range(64):
  for x in range(32):
   a=old.getpixel((x,y));b=now.getpixel((x,y))
   if a!=b:
    changed.append({'cell':[x,y],'before':list(a),'after':list(b)})
    check(direction+f' delta supported by old far arm {x},{y}',bool(oldfar.getpixel((x,y))[3]))
    check(direction+f' delta only removes unsupported projection {x},{y}',not b[3])
 check(direction+' front/back exact or bounded side removal',not changed if direction in ['south','north'] else bool(changed))
 check(direction+' full shoes exact',old.crop((0,58,32,64)).tobytes()==now.crop((0,58,32,64)).tobytes())
 if direction in ['west','east']:
  union=set()
  for n in ['near-arm','hands']:
   cells={(x,y) for x,y,c in src['layers'][n]};check(direction+' connected '+n,connected(cells));union|=cells
  check(direction+' connected sleeve and palm',connected(union))
 deltas[direction]=changed
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
board=Image.new('RGB',(880,400),'#e8e4d7');d=ImageDraw.Draw(board)
d.text((15,12),'M1.OM2 ONLY CHANGE: unsupported far sleeve fully occluded / UNAPPROVED',font=font,fill='#252431')
for i,direction in enumerate(['west','east']):
 for j,(label,sub) in enumerate([('OM1 corrected checkpoint','history-v1'),('OM2 far arm occluded','')]):
  im=rgba(OUT/sub/f'idle-{direction}.png');x=20+i*430+j*200
  d.text((x,42),direction.upper()+' '+('BEFORE' if j==0 else 'AFTER'),font=font,fill='#252431')
  large=im.resize((128,256),Image.Resampling.NEAREST);board.paste(large,(x+20,62),large);board.paste(im,(x+65,325),im)
  d.text((x,382),label,font=font,fill='#252431')
board.save(OUT/'before-after.png')
bg=Image.new('RGB',(1050,440),'#eeeeea');dr=ImageDraw.Draw(bg)
for row,color in enumerate(['#eeeeea','#26303c']):
 dr.rectangle((0,row*220,1049,(row+1)*220),fill=color)
 for i,direction in enumerate(['south','north','west','east']):
  im=rgba(OUT/f'idle-{direction}.png');x=15+i*260;fg='#252431' if row==0 else '#eeeeea'
  dr.text((x,row*220+8),direction.upper()+' native + 3x',font=font,fill=fg)
  bg.paste(im,(x+8,row*220+45),im);big=im.resize((96,192),Image.Resampling.NEAREST);bg.paste(big,(x+75,row*220+25),big)
bg.save(OUT/'background-inspection.png')
report={'task':'M1.OM2','checksPassed':len(checks),'checks':checks,'deltas':deltas,'scope':'Only unsupported W/E far-arm layer removed; all other real layers exact checkpoint','appearanceAccepted':False}
(HERE/'continuation-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'checksPassed':len(checks),'changedCells':{k:len(v) for k,v in deltas.items()}}))
