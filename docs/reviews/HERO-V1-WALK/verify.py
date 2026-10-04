from pathlib import Path
from PIL import Image,ImageSequence
import json,hashlib
repo=Path(__file__).resolve().parents[3];root=repo/'art/source/hero-boy-v1';out=repo/'assets/review/hero-boy-v1-walk';official=repo/'assets/characters/hero-boy-v1'
source=json.loads((root/'user-approved.rle.json').read_text());idle=[]
for row in source['frames'][0]['rows']:
 decoded=[]
 for k,n in zip(row[::2],row[1::2]):decoded +=[k]*n
 assert len(decoded)==32;idle+=decoded
p=json.loads((root/'walk.sprite.json').read_text());s=json.loads((root/'idle.sprite.json').read_text());assert s['frames'][0]['pixels']==idle;assert source['palette']==s['palette']==p['palette'];assert p['frames'][1]['pixels']==p['frames'][3]['pixels']==idle
palette=p['palette']
def rgba(pixels):return bytes(channel for k in pixels for channel in (tuple(bytes.fromhex(palette[k][1:]))+(255,) if k else (0,0,0,0)))
assert Image.open(official/'idle-south.png').convert('RGBA').tobytes()==rgba(idle)
manifest=json.loads((official/'manifest.json').read_text());assert manifest['sourceSHA256']==hashlib.sha256((root/'user-approved.rle.json').read_bytes()).hexdigest();assert manifest['pixelSHA256']==hashlib.sha256(rgba(idle)).hexdigest()
report={'idleApproved':True,'walkApproved':False,'nativeFrame':[32,64],'idlePixelsVerified':2048,'walkPixelsVerified':0,'gifPixelsVerified':0,'poses':[]}
for i,f in enumerate(p['frames']):
 pixels=f['pixels'];im=Image.open(out/f'frame-{i}.png').convert('RGBA');assert im.size==(32,64);assert im.tobytes()==rgba(pixels);report['walkPixelsVerified']+=2048
 occ={(x,y)for y in range(64)for x in range(32)if pixels[y*32+x]};seen={next(iter(occ))};stack=list(seen)
 while stack:
  x,y=stack.pop()
  for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if q in occ and q not in seen:seen.add(q);stack.append(q)
 assert seen==occ
 if i%2==0:
  for y in range(45):
   for x in range(32):
    if idle[y*32+x]:assert pixels[(y+2)*32+x]==idle[y*32+x],(i,x,y,'head changed')
  assert im.getbbox()[3]==64
  # Not merely the entire idle translated: limbs/torso have original pose edits.
  translated=[0]*64+idle[:-64];assert sum(a!=b for a,b in zip(pixels,translated))>80
 else:assert im.getbbox()[3]==62
 report['poses'].append({'name':f['name'],'bbox':im.getbbox(),'opaquePixels':len(occ),'connected':True})
for scale,name in [(1,'walk-native.gif'),(6,'walk-preview-6x.gif')]:
 gif=Image.open(out/name);assert gif.size==(32*scale,64*scale);assert gif.info['loop']==0;assert gif.n_frames==4;durations=[]
 for i,frame in enumerate(ImageSequence.Iterator(gif)):
  actual=frame.convert('RGBA');expected=Image.frombytes('RGBA',(32,64),rgba(p['frames'][i]['pixels'])).resize(gif.size,Image.Resampling.NEAREST)
  if scale>1:
   background=Image.new('RGBA',gif.size,'#eee9df');background.alpha_composite(expected);expected=background
  assert actual.tobytes()==expected.tobytes(),(name,i,'GIF pixel mismatch')
  durations.append(frame.info['duration']);report['gifPixelsVerified']+=gif.width*gif.height
 assert durations==[130,140,130,140]
 report[name]={'dimensions':gif.size,'frames':4,'durationsMs':durations,'loopMs':sum(durations),'pixelExact':True}
report['sourceCycleMs']=32*280896/16777216*1000;report['gifCycleRoundingMs']=540-report['sourceCycleMs'];report['paletteRequantized']=False;report['idleSHA256']=hashlib.sha256((official/'idle-south.png').read_bytes()).hexdigest();report['gifSHA256']=hashlib.sha256((out/'walk-native.gif').read_bytes()).hexdigest()
(Path(__file__).parent/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
