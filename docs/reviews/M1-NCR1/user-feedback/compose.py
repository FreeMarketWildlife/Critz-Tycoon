"""Presentation only: frozen NCR1 art; no author pixels or source files modified."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,math
R=Path(__file__).resolve().parents[4];D=Path(__file__).parent;A=D.parent;BG='#cbd2d6';INK='#242330';PIN='0bb4ee4293ec2a76a3b8eb77d5d1fca4441bdcc1';dirs=[('south','Front'),('north','Back'),('west','Left'),('east','Right')];f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14);bigfont=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',23);small=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12);inputs={};checks=[]
def src(dr,po,size,typ):
 p=A/f'{dr}-{po}/{size}-{typ}.png';data=p.read_bytes();assert data==subprocess.check_output(['git','show',PIN+':'+str(p.relative_to(R))]);inputs[str(p.relative_to(R))]=hashlib.sha256(data).hexdigest();return Image.open(p).convert('RGBA')
def paste(out,q,xy,scale):
 assert isinstance(scale,int);im=q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST);out.paste(im,xy,im);bg=Image.new('RGBA',q.size,BG);bg.alpha_composite(q);x,y=xy;assert out.crop((x,y,x+im.width,y+im.height)).tobytes()==bg.convert('RGB').resize(im.size,Image.Resampling.NEAREST).tobytes();checks.append({'spritePixelsExact':True,'scale':scale})
def centered(draw,x,y,text,font=f):draw.text((x-draw.textlength(text,font=font)/2,y),text,font=font,fill=INK)
# Current only. All four appearances have equal96x192 integer enlargement.
p=Image.new('RGB',(830,1110),BG);draw=ImageDraw.Draw(p);draw.fontmode='1';draw.text((24,20),'Hero and bald template',font=bigfont,fill=INK);draw.text((24,57),'Four directions',font=f,fill=INK)
for center,title in [(270,'32 × 64'),(630,'16 × 32')]:centered(draw,center,87,title)
cols=[('master','hero','Hero'),('master','bald','Bald template'),('native','hero','Hero'),('native','bald','Bald template')]
for j,(_,_,label) in enumerate(cols):centered(draw,180+j*180,111,label)
for row,(dr,label) in enumerate(dirs):
 y=135+row*210;draw.text((15,y+110),label,font=f,fill=INK)
 for j,(size,typ,_) in enumerate(cols):paste(p,src(dr,'idle',size,typ),(132+j*180,y),3 if size=='master' else 6)
draw.text((24,985),'Actual size',font=f,fill=INK)
for j,(size,typ,_) in enumerate(cols):
 q=src('south','idle',size,typ);paste(p,q,(180+j*180-q.width//2,1014),1)
p.save(D/'Critz-Hero-four-directions.png')
# One combined GIF: preserve each direction's repeating source timeline, sampled
# at20ms to avoid10ms inter-panel event gaps/clamping in common GIF players.
order=['A','A','P','P','C','C','P','P'];holds={'south':[100]*8,'north':[70,60,70,70,70,60,70,70],'west':[70,60,70,70,70,60,70,70],'east':[70,60,70,70,70,60,70,70]};period=math.lcm(*(sum(v) for v in holds.values()));tick=20
frames={dr:{po:[src(dr,po,'master',typ) for typ in ['hero','bald']] for po in ['A','P','C']} for dr,_ in dirs}
def pose(dr,t):
 local=t%sum(holds[dr]);i=0
 while local>=holds[dr][i]:local-=holds[dr][i];i+=1
 return order[i]
def render(sig):
 q=Image.new('RGB',(904,340),BG);dd=ImageDraw.Draw(q);dd.fontmode='1';dd.text((24,16),'Walking — four directions',font=bigfont,fill=INK);dd.text((24,51),'32 × 64 · Hero and bald template',font=f,fill=INK)
 for j,(dr,label) in enumerate(dirs):
  gx=20+j*216;centered(dd,gx+102,80,label);centered(dd,gx+48,103,'Hero',small);centered(dd,gx+156,103,'Template',small)
  for k,sp in enumerate(frames[dr][sig[j]]):paste(q,sp,(gx+k*108,125),3)
 return q
cache={};sequence=[];durations=[];signatures=[]
for t in range(0,period,tick):
 sig=tuple(pose(dr,t) for dr,_ in dirs)
 if signatures and sig==signatures[-1]:durations[-1]+=tick
 else:
  if sig not in cache:cache[sig]=render(sig)
  sequence.append(cache[sig]);durations.append(tick);signatures.append(sig)
colors=sorted({c for q in cache.values() for c in q.get_flattened_data()});assert len(colors)<=256;palette=Image.new('P',(1,1));palette.putpalette([v for c in colors for v in c]+[0]*(768-len(colors)*3));indexed=[q.quantize(palette=palette,dither=Image.Dither.NONE) for q in sequence];indexed[0].save(D/'Critz-Hero-walk.gif',save_all=True,append_images=indexed[1:],duration=durations,loop=0,disposal=2,optimize=False)
g=Image.open(D/'Critz-Hero-walk.gif');assert g.n_frames==len(sequence) and g.info.get('loop')==0;decoded=[]
for i,q in enumerate(sequence):g.seek(i);assert g.convert('RGB').tobytes()==q.tobytes();assert g.info['duration']==durations[i];decoded.append({'frame':i,'poses':signatures[i],'durationMs':durations[i],'allFrameRGBExact':True})
assert sum(durations)==21600 and min(durations)>=20
# Re-evaluate every sampled moment independently against actual saved GIF timing.
t=0;i=0;end=durations[0]
for t in range(0,period,tick):
 while t>=end:i+=1;end+=durations[i]
 assert signatures[i]==tuple(pose(dr,t) for dr,_ in dirs)
(D/'presentation-checks.json').write_text(json.dumps({'sourceSHA':PIN,'scope':'Current original-art compositions only; no author/source modification','pngSize':list(p.size),'gifSize':list(g.size),'background':BG,'inputFiles':inputs,'spritePanelChecks':len(checks),'gifFrames':len(decoded),'gifDurationMs':sum(durations),'gifMinHoldMs':min(durations),'gifLoop':0,'combinedTimelineSamplingMs':tick,'maxSourceTransitionDisplayRoundingMs':10,'timingQualification':'Original South800ms and NWE540ms timelines combined on20ms sampling grid for GIF compatibility; no cumulative drift; original source timing metadata unchanged. This presentation is not an exact10ms timing oracle.','frames':decoded,'userAppearanceApproval':False},indent=2)+'\n');print(json.dumps({'sourceFiles':len(inputs),'spritePanelsExact':len(checks),'GIFframes':len(decoded),'periodMs':sum(durations),'maxGIFTransitionRoundingMs':10}))
