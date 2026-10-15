"""Mechanical private comparison from actual pinned before and frozen after PNGs."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[4];O=Path(__file__).parent;A=O.parent;B=R/'docs/reviews/M1-H4R1';D=A/'private-parent-review';D.mkdir(exist_ok=True);BG='#eee8d1';font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12);W=140;H=320;TOP=32;order=['A','A','P','P','C','C','P','P'];panels=[];inputs={};checks=[]
def source(base,dr,po,size,typ):
 p=base/f'{dr}-{po}/{size}-{typ}.png';data=p.read_bytes()
 if base==B:assert data==subprocess.check_output(['git','show','2c8fa4f:'+str(p.relative_to(R))])
 inputs[str(p.relative_to(R))]=hashlib.sha256(data).hexdigest();return Image.open(p).convert('RGBA')
def render(dirs,po,columns,title):
 out=Image.new('RGB',(len(columns)*W,TOP+len(dirs)*H),BG);draw=ImageDraw.Draw(out);draw.fontmode='1';draw.text((5,4),title,font=font,fill='#242330');placements=[]
 for row,dr in enumerate(dirs):
  for col,(base,size,typ,label) in enumerate(columns):
   q=source(base,dr,po,size,typ);x=col*W;y=TOP+row*H;draw.text((x+4,y+2),dr+' '+po+'\n'+label,font=font,fill='#242330');scale=3 if size=='master' else 6;assert q.width*scale==96 and q.height*scale==192;big=q.resize((96,192),Image.Resampling.NEAREST);out.paste(big,(x+12,y+40),big);out.paste(q,(x+50,y+240),q);placements.append({'src':str((base/f'{dr}-{po}/{size}-{typ}.png').relative_to(R)),'big':[x+12,y+40,96,192],'native':[x+50,y+240,*q.size]})
 return out,placements
beforeafter=[(base,size,typ,label) for size in ['master','native'] for base,prefix in [(B,'BEFORE'),(A,'AFTER')] for typ in ['hero','bald'] for label in [prefix+' '+('32' if size=='master' else '16')+' '+typ]]
p,placed=render(['south','north','west','east'],'idle',beforeafter,'PRIVATE NCR1 — before/after; same body, true native + equal integer display');p.save(D/'NCR1-INTERNAL-four-direction-before-after.png');panels.append({'file':'NCR1-INTERNAL-four-direction-before-after.png','panels':placed})
after=[(A,size,typ,'AFTER '+('32' if size=='master' else '16')+' '+typ) for size in ['master','native'] for typ in ['hero','bald']]
for family,dirs,holds in [('south',['south'],[100]*8),('north-west-east',['north','west','east'],[70,60,70,70,70,60,70,70])]:
 for speed,mul in [('normal',1),('slow',4)]:
  ims=[];placements=[]
  for i,po in enumerate(order):
   q,ps=render(dirs,po,after,f'PRIVATE NCR1 {family} / {speed} / slot{i+1}/8 {po}');ims.append(q);placements.append(ps)
  colors=sorted({c for q in ims for c in q.get_flattened_data()});assert len(colors)<=256;pal=Image.new('P',(1,1));pal.putpalette([v for c in colors for v in c]+[0]*(768-len(colors)*3));pp=[q.quantize(palette=pal,dither=Image.Dither.NONE) for q in ims];name=f'NCR1-INTERNAL-{family}-walk-{speed}.gif';pp[0].save(D/name,save_all=True,append_images=pp[1:],duration=[v*mul for v in holds],loop=0,disposal=2,optimize=False);g=Image.open(D/name);assert g.n_frames==8 and g.info.get('loop')==0
  for i,expected in enumerate(ims):g.seek(i);assert g.convert('RGB').tobytes()==expected.tobytes() and g.info['duration']==holds[i]*mul;checks.append({'file':name,'slot':i+1,'allRGBExact':True,'holdMs':holds[i]*mul})
  panels.append({'file':name,'frames':placements,'holdsMs':[v*mul for v in holds],'loopMs':sum(holds)*mul})
# All source files must still match the independent final saved audit.
record=json.loads((O/'saved-audit.json').read_text())['candidateInputHashes']
for path,h in record.items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h
(O/'packet-composition-audit.json').write_text(json.dumps({'qualification':'Original Critz art compositions, no browser/reference pixels','inputHashes':inputs,'files':panels,'decodedFrames':checks},indent=2)+'\n');print(json.dumps({'privateFiles':len(panels),'exactDecodedGifFrames':len(checks),'inputFiles':len(inputs)}))
