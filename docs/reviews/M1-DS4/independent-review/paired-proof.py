from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[4];src=root/'docs/reviews/M1-DS4';out=src/'independent-review';out.mkdir(exist_ok=True);order=['A','A','P','P','C','C','P','P'];font=ImageFont.load_default();checks=[]
def ck(s,v):assert v,s;checks.append(s)
def read(s,dr,po):return Image.open(src/f'dummy-{s}x-{dr}-{po}.png').convert('RGBA')
for dr in ['south','north','west','east']:
 for speed,delay in [('normal',100),('slow',400)]:
  seq=[]
  for slot,po in enumerate(order):
   frame=Image.new('RGB',(352,192),'#eee8d1');d=ImageDraw.Draw(frame);d.fontmode='1';d.text((6,3),f'{dr.upper()} | slot {slot+1}/8 | {po} | {speed}',font=font,fill='#292634');d.text((6,20),'16x32 at 4x',font=font,fill='#485b78');d.text((186,20),'32x64 at 2x',font=font,fill='#485b78')
   for s,x,m in [(1,16,4),(2,192,2)]:
    q=read(s,dr,po);big=q.resize((64,128),Image.Resampling.NEAREST);frame.paste(big,(x,36),big);tx,ty=(104,132) if s==1 else (280,100);frame.paste(q,(tx,ty),q);d.text((tx,168),'native',font=font,fill='#485b78');d.line((x,164,x+64,164),fill='#80503d')
   d.text((6,181),'Equal display / original review cadence',font=font,fill='#485b78');seq.append(frame)
  file=out/f'paired-{dr}-{speed}-INTERNAL.gif';seq[0].save(file,save_all=True,append_images=seq[1:],duration=delay,loop=0,optimize=False,disposal=2)
  g=Image.open(file);ck(file.name+'8 labelled slots',g.n_frames==8);ck(file.name+'loop',g.info['loop']==0)
  for i,frame in enumerate(seq):g.seek(i);ck(file.name+str(i)+'pixels/hold',g.convert('RGB').tobytes()==frame.tobytes() and g.info['duration']==delay)
 # Independent native/refined source checks.
 for po in ['idle','A','P','C']:
  a=read(1,dr,po);b=read(2,dr,po);ck(dr+po+'sizes',a.size==(16,32) and b.size==(32,64));ck(dr+po+'refined not simple doubling',b.tobytes()!=a.resize((32,64),Image.Resampling.NEAREST).tobytes());ck(dr+po+'scaled crown',b.getbbox()[1]==a.getbbox()[1]*2)
  ck(dr+po+'binary PNG alpha',all(v in [0,255] for im in [a,b] for v in im.getchannel('A').get_flattened_data()))
ck('native West idle exact parent-reviewed DS3',read(1,'west','idle').tobytes()==Image.open(root/'docs/reviews/M1-DS3/dummy-1x-west-idle.png').convert('RGBA').tobytes())
# Decode actual writer original loops separately; GIF may merge adjacent repeated poses.
actualFrames=0
for s in [1,2]:
 for dr in ['south','north','west','east']:
  for mag in [1,4]:
   g=Image.open(src/f'dummy-{s}x-{dr}-walk-{mag}display.gif');timeline=[];actualFrames+=g.n_frames
   for i in range(g.n_frames):g.seek(i);hold=g.info['duration'];ck(f'{s}{dr}{mag}{i}hold quantum',hold%100==0);timeline.extend([g.convert('RGB').tobytes()]*(hold//100))
   ck(f'{s}{dr}{mag}loop schedule',len(timeline)==8 and g.info['loop']==0)
   for slot,po in enumerate(order):
    q=read(s,dr,po);bg=Image.new('RGBA',q.size,'#eee8d1');bg.alpha_composite(q);ck(f'{s}{dr}{mag}slot{slot}',timeline[slot]==bg.convert('RGB').resize((16*s*mag,32*s*mag),Image.Resampling.NEAREST).tobytes())
# Preserve all previous frozen art and creator, without reading player storage.
import subprocess
ck('creator unchanged',subprocess.run(['git','diff','--quiet','HEAD','--','character-creator'],cwd=root).returncode==0)
for folder in ['dummy-resolution-r1','dummy-resolution-r2','dummy-resolution-r3']:ck(folder+'unchanged',subprocess.run(['git','diff','--quiet','HEAD','--','art/source/'+folder],cwd=root).returncode==0)
(out/'paired-saved-checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'writerActualGIFFrames':actualFrames,'writerLogicalSlots':128,'pairedActualGIFFrames':64,'normalLoopMs':800,'slowLoopMs':3200,'timingBasis':'Original comparison presentation; not Emerald source timing','checks':checks},indent=2)+'\n');print(json.dumps({'checks':len(checks),'writerActualFrames':actualFrames,'pairedActualFrames':64}))
