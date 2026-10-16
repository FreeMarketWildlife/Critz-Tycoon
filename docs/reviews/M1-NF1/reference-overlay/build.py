"""Read-only exact fan-reference registration. Reference pixels stay outside Git/build."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import hashlib,json,sys,subprocess
R=Path(__file__).resolve().parents[4];D=Path(__file__).parent;O=Path(sys.argv[1]).resolve();assert R not in O.parents and O!=R;O.mkdir(parents=True,exist_ok=True)
p=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/brendan-user-reference-original/01agijgmbz561.gif');sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e';g=Image.open(p);frames=[];info=[]
assert g.size==(256,192) and g.n_frames==8
for i in range(g.n_frames):
 g.seek(i);im=g.convert('RGBA').crop((0,0,128,192));native=im.resize((32,48),Image.Resampling.NEAREST);assert native.resize((128,192),Image.Resampling.NEAREST).tobytes()==im.tobytes();frames.append(native);info.append({'frame':i,'durationMs':g.info['duration'],'nativeBounds':native.getbbox(),'rgbaSHA256':hashlib.sha256(native.tobytes()).hexdigest()})
assert frames[0].tobytes()==frames[1].tobytes() and frames[2].tobytes()==frames[3].tobytes()==frames[6].tobytes()==frames[7].tobytes() and frames[4].tobytes()==frames[5].tobytes()
f=frames[2];nfpath=R/'docs/reviews/M1-NF1/front-neutral.png';nfbytes=nfpath.read_bytes();n=Image.open(nfpath).convert('RGBA');assert hashlib.sha256(nfbytes).hexdigest()=='5958a184d1f9ee05a3f30392c40627a156752a3427a3d82c179d5d0acdb2294b'
r=Image.new('RGBA',(32,64));r.alpha_composite(f,(0,16))
assert r.getbbox()[3]==n.getbbox()[3]==62
assert r.getchannel('A').crop((0,58,32,64)).tobytes()==n.getchannel('A').crop((0,58,32,64)).tobytes()
def xs(im,y):return [x for x in range(32) if im.getpixel((x,y))[3]]
assert all(r.getpixel((x,y))[:3]==(16,33,58) and n.getpixel((x,y))[:3]==(36,35,48) for y in range(38,42) for x in [12,13,18,19])
cyan=(48,220,240);magenta=(255,94,183);bg=(39,52,64)
def tint(im,color):
 a=Image.new('RGBA',im.size)
 for y in range(64):
  for x in range(32):
   if im.getpixel((x,y))[3]:a.putpixel((x,y),color+(145,))
 return a
ov=Image.new('RGBA',(32,64));ov.alpha_composite(tint(r,cyan));ov.alpha_composite(tint(n,magenta))
W,H=1080,805;q=Image.new('RGB',(W,H),bg);draw=ImageDraw.Draw(q)
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14);small=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12);title=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',23);white='#edf4f6';muted='#b7c8d4';gold='#ffd76c'
draw.text((24,16),'Supplied 2× Brendan / corrected NF1 front',font=title,fill=white)
draw.text((24,51),'Closest two-foot walking stance (frame 2) vs neutral idle — pose mismatch remains.',font=font,fill=muted)
X=[76,408,740];Y=110;S=6
for x,label,im in zip(X,['Actual fan-made redraw','NF1 neutral · unchanged','Translucent registered overlay'],[r,n,ov]):
 draw.text((x-22,83),label,font=font,fill=white)
 # Matched native32x64 frames, one shared display factor; no per-body scaling.
 tile=Image.new('RGB',(32,64),bg);td=ImageDraw.Draw(tile)
 for yy in range(0,64,4):
  for xx in range(0,32,4):
   if (xx//4+yy//4)%2:td.rectangle((xx,yy,xx+3,yy+3),fill=(47,62,74))
 tile.paste(im,(0,0),im);q.paste(tile.resize((192,384),Image.Resampling.NEAREST),(x,Y))
 for yy in range(Y,Y+384,12):draw.line((x+96,yy,x+96,yy+5),fill='#7e929e')
 draw.line((x-5,Y+62*S,x+197,Y+62*S),fill=gold,width=2)
 draw.text((x-22,506),'Native size (32×64)',font=small,fill=muted);nativebg=Image.new('RGB',(32,64),bg);nativebg.paste(im,(0,0),im);q.paste(nativebg,(x+78,529))
# Only hat extent is called out above head; no hidden scalp inferred.
draw.line((X[0]+15*S,Y+20*S,X[0]+32*S,Y+20*S),fill=cyan,width=2)
draw.text((X[0]+200,Y+20*S-5),'hat',font=small,fill=cyan)
# Measured row indicators, not inferred joints.
for number,row in [(1,47),(2,51),(3,54),(4,60)]:
 y=Y+row*S+3;draw.line((X[2]+192,y,X[2]+218,y),fill=gold,width=1);draw.text((X[2]+225,y-7),str(number),font=font,fill=gold)
draw.text((24,612),'CYAN = reference (57% alpha)   MAGENTA = NF1 (57%)   PALE MIX = overlap',font=font,fill=white)
draw.text((24,637),'1  Shoulder/upper-arm row47: reference22px wide; NF1 18px. Clothing ≠ naked shoulder.',font=font,fill=muted)
draw.text((24,661),'2  Arm/hand outer span at rows50–52: both26px; glove/hand shape & colors differ.',font=font,fill=muted)
draw.text((24,685),'3  Row54: reference glove/costume22px; NF1 waist14px. Row55:18px vs16px.',font=font,fill=muted)
draw.text((24,709),'4  Shoe alpha rows58+ is EXACT; contact runs x9–12 &19–22 at row61 in both.',font=font,fill=muted)
draw.text((24,741),'Registration: left128×192 crop ÷4 exact repeated display blocks →32×48; shift(0,+16).',font=small,fill=white)
draw.text((24,761),'Center x15.5; contact edge y62. One native pixel = one native pixel; displayed6× nearest.',font=small,fill=white)
draw.text((24,781),'Hat/hair/pack/clothing retained as appearance, not hidden body evidence. No sprite edits.',font=small,fill=white)
q.save(O/'fan-reference-NF1-overlay.png')
report={'task':'M1.NF1 reference overlay only','sourceURL':'https://i.redd.it/01agijgmbz561.gif','sourceGIFSHA256':sha,'sourceGIFDimensions':[256,192],'frames':info,'selectedFrame':2,'selectionReason':'two-foot passing stance closest to neutral front; identical frames2/3/6/7; no true idle in8-frame walk','referenceExtraction':{'crop':[0,0,128,192],'displayBlockFactorRemoved':4,'allEightExactBlockReconstruction':True,'nativeDimensions':[32,48],'notOriginalBrendanUpscale':True},'registration':{'referenceTranslation':[0,16],'dummyTranslation':[0,0],'bodyScaleFactor':1,'centerlinePixelX':15.5,'contactEdgeY':62,'enlargement':6,'interpolation':'nearest','noStretchOrPerPartFit':True},'nf1SourceCommit':'24444dba660577201f3352fcec89a0bb1a315c5f','nf1SHA256':hashlib.sha256(nfbytes).hexdigest(),'measurements':{'referenceRegisteredBounds':r.getbbox(),'nf1Bounds':n.getbbox(),'eyesBoth':{'xRuns':[[12,14],[18,20]],'yRun':[38,42]},'shoulderProjectionRow47':{'referenceXs':xs(r,47),'NF1Xs':xs(n,47)},'armsHandsRows50to52OuterBounds':{'both':[3,29]},'waistCostumeRow54':{'referenceXs':xs(r,54),'NF1Xs':xs(n,54),'qualification':'reference includes glove/costume projections, not anatomical waist'},'row55':{'referenceXs':xs(r,55),'NF1Xs':xs(n,55)},'shoeAlpha58plusExact':True,'contactRow61Both':xs(n,61),'referenceHatTop':20,'NF1BareCrownTop':27,'qualification':'hat/helmet extent is not skull height; clothed/gloved source does not reveal hidden anatomy'},'nf1SourceBytesUnchanged':nfpath.read_bytes()==nfbytes,'outputSHA256':hashlib.sha256((O/'fan-reference-NF1-overlay.png').read_bytes()).hexdigest(),'referencePixelsOutsideGit':True}
(D/'measurements.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['selectedFrame','registration','outputSHA256','nf1SourceBytesUnchanged']}))
