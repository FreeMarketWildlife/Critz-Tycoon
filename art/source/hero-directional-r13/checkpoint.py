"""First concrete four-direction still checkpoint, before walk proof acceptance."""
from pathlib import Path
from PIL import Image,ImageDraw
import sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR13';ext=Path(sys.argv[1]).resolve()
dirs=('south','north','west','east');bg='#9dbac8';ink='#253340'
comparison=Image.new('RGB',(1600,380),bg);cd=ImageDraw.Draw(comparison)
original=Image.new('RGB',(1120,380),bg);od=ImageDraw.Draw(original)
for col,direction in enumerate(dirs):
 ref=Image.open(ext/f'ROM-{dict(south=0,north=1,west=2,east=2)[direction]:02}.png').convert('RGBA')
 if direction=='east':ref=ref.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 h=Image.open(out/f'hero-{direction}-idle.png').convert('RGBA');m=Image.open(out/f'dummy-{direction}-idle.png').convert('RGBA')
 x=col*400;cd.text((x+8,5),direction.upper()+' / PINNED ROM | HERO | TEMPLATE',fill=ink)
 for i,im in enumerate((ref,h,m)):
  big=im.resize((128,256),Image.Resampling.NEAREST);comparison.paste(big,(x+4+i*132,25),big);comparison.paste(im,(x+52+i*132,300),im)
 x=col*280;od.text((x+8,5),direction.upper()+' / HERO | TEMPLATE',fill=ink)
 for i,im in enumerate((h,m)):
  big=im.resize((128,256),Image.Resampling.NEAREST);original.paste(big,(x+4+i*140,25),big);original.paste(im,(x+52+i*140,300),im)
cd.text((8,365),'FIRST PROJECTION / IDLE CHECKPOINT. Full32x64 at4x + native. Walk proofs pending checks. No appearance approval.',fill=ink)
od.text((8,365),'Head over upper torso; no separate neck cylinder. Hidden joints PROPOSED. Walk proofs pending checks.',fill=ink)
comparison.save(ext/'four-direction-idle-source-hero-template.png');original.save(out/'four-direction-idle-hero-template.png')
p=Image.new('RGB',(1040,360),bg);pd=ImageDraw.Draw(p)
for row,(kind,oldname,newname) in enumerate([('CLOTHED HERO','walk-00.png','hero-south-A.png'),('NEUTRAL TEMPLATE','mannequin-00.png','dummy-south-A.png')]):
 y=12+row*175;pd.text((10,y),kind+' / HR12 BEFORE | HR13 PROJECTION',fill=ink)
 for col,(folder,name) in enumerate([(root/'docs/reviews/M1-HR12',oldname),(out,newname)]):
  im=Image.open(folder/name).convert('RGBA');c=im.crop((2,36,30,53)).resize((224,136),Image.Resampling.NEAREST);p.paste(c,(25+col*450,y+22),c)
p.save(out/'projection-before-after.png')
print(str(ext/'four-direction-idle-source-hero-template.png'));print(str(out/'four-direction-idle-hero-template.png'));print(str(out/'projection-before-after.png'))
