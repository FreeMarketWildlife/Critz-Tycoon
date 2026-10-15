"""Compose existing saved sprites for review, without authoring sprite pixels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[4];out=Path(__file__).parent
order=['A','A','P','P','C','C','P','P'];holds=[70,60,70,70,70,60,70,70]
keys=['before-hero','final-hero','before-template','final-template'];labels=['SR1 HERO','SR2 HERO','SR1 BALD','SR2 BALD'];font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',9)
images={};files=[];checks=[]
def ck(name,value):
 checks.append({'name':name,'pass':bool(value)})
 assert value,name
for dr in ['west','east']:
 for po in ['idle','A','P','C']:
  for key in keys:
   p=root/(f'docs/reviews/M1-SR1/{dr}-{po}/{key}.png' if key.startswith('before') else f'docs/reviews/M1-SR2/{dr}-{po}/{key}.png')
   images[dr,po,key]=Image.open(p).convert('RGBA')
   files.append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
def strip(dr,po,bg,header):
 b=Image.new('RGB',(352,104),bg);d=ImageDraw.Draw(b);d.fontmode='1';d.text((4,2),header,font=font,fill='#242330')
 for col,key in enumerate(keys):
  x=col*88;d.text((x+3,16),labels[col],font=font,fill='#242330');im=images[dr,po,key];b.paste(im,(x+28,29),im)
 return b
plate=Image.new('RGB',(704,848),'#eee8d1');d=ImageDraw.Draw(plate);d.fontmode='1';d.text((4,2),'ART-ONLY GAME-SCALE COMPARISON / TRUE1X / GRASS LEFT, PATH RIGHT',font=font,fill='#242330')
row=0
for dr in ['west','east']:
 for po in ['idle','A','P','C']:
  for col,bg in enumerate(['#79a85e','#bbbc7d']):plate.paste(strip(dr,po,bg,f'{dr.upper()} {po} / fixed source anchor'),(col*352,16+row*104))
  row+=1
plate.save(out/'game-scale-artwork-1x.png')
for dr in ['west','east']:
 for speed,name in [(1,'normal'),(4,'slow')]:
  frames=[strip(dr,po,'#79a85e',f'{dr.upper()} SLOT{i+1}/8 {po} HOLD{holds[i]*speed}ms / {name}').resize((1056,312),Image.Resampling.NEAREST) for i,po in enumerate(order)]
  colors=sorted({rgb for frame in frames for rgb in frame.resize((352,104),Image.Resampling.NEAREST).get_flattened_data()});assert len(colors)<=256;palette=Image.new('P',(1,1));palette.putpalette([n for rgb in colors for n in rgb]+[0]*(768-len(colors)*3));encoded=[q.quantize(palette=palette,dither=Image.Dither.NONE) for q in frames]
  dest=out/f'{dr}-paired-{name}-3x.gif';encoded[0].save(dest,save_all=True,append_images=encoded[1:],duration=[v*speed for v in holds],loop=0,optimize=False,disposal=2)
  q=Image.open(dest);ck(dest.name+' eight actual frames',q.n_frames==8);ck(dest.name+' infinite loop',q.info.get('loop')==0)
  for i,expected in enumerate(frames):
   q.seek(i);ck(dest.name+f' frame{i} full composed RGB exact',q.convert('RGB').tobytes()==expected.tobytes());ck(dest.name+f' frame{i} exact original hold',q.info.get('duration')==holds[i]*speed)
(out/'composition-checks.json').write_text(json.dumps({'task':'M1.SR2','pass':True,'count':len(checks),'checks':checks,'sourceFiles':files,'order':order,'recordedHoldsMs':holds,'cadenceMeaning':'Existing selected Hero exports; not measured NPC/emulator timing.','visualAcceptance':False,'gameScalePlateMeaning':'Direct unmodified sprite composition on existing meadow grass/path colors; not a browser screenshot or runtime adoption.'},indent=2)+'\n');print('PASS',len(checks),'actual saved paired-GIF frame/RGB/hold/loop checks; no sprite author pixels changed.')
