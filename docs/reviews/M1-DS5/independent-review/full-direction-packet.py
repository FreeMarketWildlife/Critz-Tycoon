"""Presentation only: frozen DS4 front/rear and corrected DS5 sides."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[4];out=Path(__file__).parent;old=root/'docs/reviews/M1-DS4';new=root/'docs/reviews/M1-DS5'
directions=['south','north','west','east'];order=['A','A','P','P','C','C','P','P'];font=ImageFont.load_default();checks=[]
def ck(name,value):
    assert value,name
    checks.append(name)
def base(dr):return old if dr in ['south','north'] else new
def loop(dr,speed):return base(dr)/'independent-review'/f'paired-{dr}-{speed}-INTERNAL.gif'
def pose(s,dr,p):return Image.open(base(dr)/f'dummy-{s}x-{dr}-{p}.png').convert('RGBA')
def draw(im):
    d=ImageDraw.Draw(im);d.fontmode='1';return d
def text(d,xy,s):d.text(xy,s,font=font,fill='#292634')
board=Image.new('RGB',(960,288),'#eee8d1');d=draw(board)
text(d,(8,4),'CURRENT INTERNAL / DS4 South+North; corrected DS5 West+East / no appearance approval')
for col,dr in enumerate(directions):
    x=240*col;text(d,(x+8,24),dr.upper());text(d,(x+8,40),'16x32 at4x');text(d,(x+112,40),'32x64 at2x')
    for s,dx in [(1,8),(2,112)]:
        q=pose(s,dr,'idle');big=q.resize((64,128),Image.Resampling.NEAREST);board.paste(big,(x+dx,58),big)
        board.paste(q,(x+dx+20,196),q);text(d,(x+dx,264),'true native')
        ck(f'{dr}{s} idle allocation',q.size==(16*s,32*s))
    d.line((x+8,186,x+176,186),fill='#80503d')
board.save(out/'current-four-direction-idle-INTERNAL.png')
sheet=Image.new('RGB',(1176,904),'#eee8d1');d=draw(sheet)
text(d,(8,4),'CURRENT INTERNAL / all eight decoded playback slots / DS4 South+North + DS5 West+East')
text(d,(8,20),'Each pair: native16x32 at4x | refined32x64 at2x. Original review cadence; not measured NPC timing.')
text(d,(8,36),'Normal:100ms/slot,800ms loop. Slow:400ms/slot,3200ms loop. Repeated holds shown explicitly.')
provenance=[]
for row,dr in enumerate(directions):
    y=64+row*210;text(d,(8,y),dr.upper())
    normal=Image.open(loop(dr,'normal'));slow=Image.open(loop(dr,'slow'))
    ck(dr+'8 saved slots',normal.n_frames==slow.n_frames==8);ck(dr+'infinite loops',normal.info.get('loop')==slow.info.get('loop')==0)
    for slot,p in enumerate(order):
        x=8+slot*146;normal.seek(slot);slow.seek(slot);n=normal.convert('RGB');s=slow.convert('RGB')
        ck(f'{dr}{slot}holds',normal.info['duration']==100 and slow.info['duration']==400)
        text(d,(x,y+15),f'{slot+1}/8 {p}');text(d,(x,y+29),f'N {100*slot}-{100*(slot+1)}ms');text(d,(x,y+43),f'S {400*slot}-{400*(slot+1)}ms')
        for scale,box,dx in [(1,(16,36,80,164),0),(2,(192,36,256,164),68)]:
            crop=n.crop(box);ck(f'{dr}{slot}{scale}normal/slow artwork',crop.tobytes()==s.crop(box).tobytes())
            q=pose(scale,dr,p);bg=Image.new('RGBA',q.size,'#eee8d1');bg.alpha_composite(q)
            ck(f'{dr}{slot}{scale}actual GIF matches frozen PNG',crop.tobytes()==bg.convert('RGB').resize((64,128),Image.Resampling.NEAREST).tobytes())
            sheet.paste(crop,(x+dx,y+60))
    for speed in ['normal','slow']:
        path=loop(dr,speed);provenance.append({'direction':dr,'speed':speed,'path':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
sheet.save(out/'current-all-directions-eight-slot-timings-INTERNAL.png')
receipt={'pass':True,'count':len(checks),'sources':{'southNorth':'2f4e39dabfecb601ced507209056b2da12576334','westEast':'fe3cdf94d410ba63738428326b2298551ab1805c'},'scope':'Presentation only, frozen source pixels and existing loops; no creator/runtime/art changes','loopProvenance':provenance,'checks':checks}
(out/'full-direction-packet-checks.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'checks':len(checks),'loops':len(provenance),'timelineSlots':32}))
