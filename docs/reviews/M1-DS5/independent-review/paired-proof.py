"""Independent saved-pixel and synchronized presentation proof; no artwork edits."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
root=Path(__file__).resolve().parents[4]
src=root/'docs/reviews/M1-DS5';old=root/'docs/reviews/M1-DS4';out=Path(__file__).parent
order=['A','A','P','P','C','C','P','P'];font=ImageFont.load_default();checks=[]
def ck(name,value):
    assert value,name
    checks.append(name)
def read(s,dr,po,folder=src):
    return Image.open(folder/f'dummy-{s}x-{dr}-{po}.png').convert('RGBA')
for dr in ['west','east']:
    for speed,delay in [('normal',100),('slow',400)]:
        seq=[]
        for slot,po in enumerate(order):
            frame=Image.new('RGB',(352,192),'#eee8d1');d=ImageDraw.Draw(frame);d.fontmode='1'
            d.text((6,3),f'{dr.upper()} | slot {slot+1}/8 | {po} | {speed}',font=font,fill='#292634')
            d.text((6,20),'16x32 at 4x',font=font,fill='#485b78');d.text((186,20),'32x64 at 2x',font=font,fill='#485b78')
            for s,x in [(1,16),(2,192)]:
                q=read(s,dr,po);big=q.resize((64,128),Image.Resampling.NEAREST);frame.paste(big,(x,36),big)
                tx,ty=(104,132) if s==1 else (280,100);frame.paste(q,(tx,ty),q)
                d.text((tx,168),'native',font=font,fill='#485b78');d.line((x,164,x+64,164),fill='#80503d')
            d.text((6,181),'INTERNAL / original review cadence',font=font,fill='#485b78');seq.append(frame)
        path=out/f'paired-{dr}-{speed}-INTERNAL.gif'
        seq[0].save(path,save_all=True,append_images=seq[1:],duration=delay,loop=0,optimize=False,disposal=2)
        gif=Image.open(path);ck(path.name+' 8 physical slots',gif.n_frames==8);ck(path.name+' loop',gif.info['loop']==0)
        for i,expected in enumerate(seq):
            gif.seek(i);ck(path.name+f' slot{i} pixels/hold',gif.convert('RGB').tobytes()==expected.tobytes() and gif.info['duration']==delay)
    for po in ['idle','A','P','C']:
        a=read(1,dr,po);b=read(2,dr,po)
        ck(dr+po+' allocated frames',a.size==(16,32) and b.size==(32,64))
        ck(dr+po+' deliberate refinement',b.tobytes()!=a.resize((32,64),Image.Resampling.NEAREST).tobytes())
        for s,q in [(1,a),(2,b)]:
            cut=(21 if po=='P' else 22)*s
            ck(f'{dr}{po}{s} compact head exact',q.crop((0,0,16*s,cut)).tobytes()==read(s,dr,po,old).crop((0,0,16*s,cut)).tobytes())
            ck(f'{dr}{po}{s} binary alpha',set(q.getchannel('A').get_flattened_data())<={0,255})
            ck(f'{dr}{po}{s} entire lower footprint exact',q.crop((0,28*s,16*s,32*s)).tobytes()==read(s,dr,po,old).crop((0,28*s,16*s,32*s)).tobytes())
            west=read(s,'west',po)
            ck(f'{dr}{po}{s} mirrored geometry',q.tobytes()==(west if dr=='west' else west.transpose(Image.Transpose.FLIP_LEFT_RIGHT)).tobytes())
for folder in ['character-creator','art/source/dummy-resolution-r1','art/source/dummy-resolution-r2','art/source/dummy-resolution-r3','art/source/dummy-resolution-r4','docs/reviews/M1-DS4']:
    ck(folder+' unchanged',subprocess.run(['git','diff','--quiet','HEAD','--',folder],cwd=root).returncode==0)
(out/'paired-saved-checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'pairedActualGIFFrames':32,'normalLoopMs':800,'slowLoopMs':3200,'timingBasis':'Original Critz review cadence, not measured NPC timing','checks':checks},indent=2)+'\n')
print(json.dumps({'checks':len(checks),'pairedActualFrames':32}))
