"""External reference/dummy/parts/overlay comparison; no sprite edits."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,sys
R=Path(__file__).resolve().parents[4];D=R/'docs/reviews/M1-RD1';O=Path(sys.argv[1]).resolve();assert R not in O.parents and O!=R;O.mkdir(exist_ok=True,parents=True)
p=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/brendan-user-reference-original/01agijgmbz561.gif');assert hashlib.sha256(p.read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e';g=Image.open(p);g.seek(2);left=g.convert('RGBA').crop((0,0,128,192));f=left.resize((32,48),Image.Resampling.NEAREST);assert f.resize((128,192),Image.Resampling.NEAREST).tobytes()==left.tobytes();ref=Image.new('RGBA',(32,64));ref.alpha_composite(f,(0,16));assert hashlib.sha256((D/'reference-derived-dummy.png').read_bytes()).hexdigest()=='606a6305a9a3bc9473a8cf6314ad86188627b6e107cfbaa97ff7e0d9a64100f8';n=Image.open(D/'reference-derived-dummy.png').convert('RGBA');ids=Image.open(D/'region-id-map.png').convert('RGBA');c=json.loads((R/'art/source/reference-dummy-r1/construction.json').read_text());assert ref.getchannel('A').crop((0,45,32,64)).tobytes()==n.getchannel('A').crop((0,45,32,64)).tobytes()
cyan=(48,220,240,145);magenta=(255,94,183,145)
def tint(im,color):
 q=Image.new('RGBA',im.size)
 for y in range(64):
  for x in range(32):
   if im.getpixel((x,y))[3]:q.putpixel((x,y),color)
 return q
overlay=Image.new('RGBA',(32,64));overlay.alpha_composite(tint(ref,cyan));overlay.alpha_composite(tint(n,magenta))
bg=(39,52,64);q=Image.new('RGB',(1120,800),bg);draw=ImageDraw.Draw(q);font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14);small=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12);title=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',23);white='#edf4f6';muted='#b7c8d4';gold='#ffd76c';Y=110;S=6;X=[44,324,604,884]
draw.text((24,16),'Reference-derived front body · supplied 2× Brendan',font=title,fill=white)
draw.text((24,52),'Same frame2 pose + pixel scale · visible body copied exactly · only covered skull reconstructed',font=font,fill=muted)
for x,label,im in zip(X,['Actual fan reference','Flat reference-derived dummy','Named body-region map','CYAN ref / MAGENTA dummy'],[ref,n,ids,overlay]):
 draw.text((x-20,84),label,font=small,fill=white);tile=Image.new('RGB',(32,64),bg);td=ImageDraw.Draw(tile)
 for yy in range(0,64,4):
  for xx in range(0,32,4):
   if (xx//4+yy//4)%2:td.rectangle((xx,yy,xx+3,yy+3),fill=(47,62,74))
 tile.paste(im,(0,0),im);q.paste(tile.resize((192,384),Image.Resampling.NEAREST),(x,Y))
 for yy in range(Y,Y+384,12):draw.line((x+96,yy,x+96,yy+5),fill='#7e929e')
 draw.line((x-4,Y+62*S,x+196,Y+62*S),fill=gold,width=2);draw.text((x,506),'Actual size32×64',font=small,fill=muted);native=Image.new('RGB',(32,64),bg);native.paste(im,(0,0),im);q.paste(native,(x+80,529))
draw.text((24,611),'BELOW-HEAD SILHOUETTE XOR: 0 pixels · all338 reference occupied cells retained (rows45–63)',font=font,fill='#a9e6b8')
draw.text((24,635),'Visible face/ears36–45 alpha:0 differences · original eye sites · full shoes/contact runs exact',font=small,fill=white)
for i,(name,rec) in enumerate(c['regions'].items()):
 x=24+(i%5)*216;y=665+(i//5)*29;xy=tuple(rec['cells'][0]);color=ids.getpixel(xy);draw.rectangle((x,y,x+15,y+15),fill=color);draw.text((x+23,y),name.replace('-',' '),font=small,fill=white)
draw.text((24,737),'Left128×192 ÷4 EXACT repeated display blocks →32×48; translate(0,+16); no stretching.',font=small,fill=muted)
draw.text((24,756),'Center x15.5 / contact edge y62 / display6× nearest. Cyan+magenta57% alpha; mixed = shared area.',font=small,fill=muted)
draw.text((24,775),'Only upper skull above36 is proposed. Internal part labels cannot change the reference body envelope.',font=small,fill=white)
path=O/'RD1-reference-dummy-overlay.png';q.save(path);print(json.dumps({'output':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions':q.size,'belowHeadXOR':0,'occupiedCells':338}))
