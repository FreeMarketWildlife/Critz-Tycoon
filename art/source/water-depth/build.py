"""Original submerged depth bank, separate from shadows and from surface motion."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,runpy,math
# Share the native geometry with the full surface bank; build only this extension.
source=Path('art/source/water-terrain/build.py').read_text();source=source[:source.index('entries=[]')]
namespace={};exec(source,namespace);inside=namespace['inside'];masks=namespace['masks']
out=Path('assets/review/water-depth');out.mkdir(parents=True,exist_ok=True)
frames=[];entries=[]
for identity in ['fresh','ocean']:
 for motion in ['still','moving']:
  for mask in masks:
   im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
   def sample(x,y):return inside(max(0,min(31,x)),max(0,min(31,y)),mask)
   for y in range(32):
    for x in range(32):
     if not inside(x,y,mask):continue
     up=next((n for n in range(1,12) if not sample(x,y-n)),None)
     side=next((n for n in range(1,5) if not sample(x-n,y) or not sample(x+n,y) or not sample(x,y+n)),None)
     if up:
      if up==1:col='#bed0a3'
      elif up==2:col='#8da889'
      elif up<=8:col='#6f8d79' if (x//7+up//3)%3 else '#5c7969'
      elif up<=10:col='#456c64'
      else:col='#305963'
      if up in [4,5,6,7] and x%11 in [2,3]:col='#496e64'
      d.point((x,y),fill=col)
     elif side:
      d.point((x,y),fill=['#9aae92','#6f8d79','#456c64','#305963'][side-1])
   n=len(frames);frames.append(im);entries.append(dict(id=f'depth.{identity}.{motion}.{mask}',x=n%16*32,y=n//16*32,w=32,h=32,neighborMask=mask,identity=identity,motion=motion,collision='whole deep cell blocked'))
sheet=Image.new('RGBA',(512,math.ceil(len(frames)/16)*32))
for n,im in enumerate(frames):sheet.paste(im,(n%16*32,n//16*32))
sheet.save(out/'atlas.png');(out/'atlas.json').write_text(json.dumps(dict(image='atlas.png',frame=32,assets=entries,masks=masks),indent=2)+'\n')
(out/'depth.tsj').write_text(json.dumps(dict(type='tileset',version='1.10',name='Critz submerged depth banks · WA5 review',tilewidth=32,tileheight=32,tilecount=sheet.width*sheet.height//1024,columns=16,image='atlas.png',imagewidth=sheet.width,imageheight=sheet.height,tiles=[dict(id=n,properties=[dict(name='assetId',type='string',value=a['id']),dict(name='blocked',type='bool',value=True)]) for n,a in enumerate(entries)]),indent=2)+'\n');print(len(entries),'original depth-bank shapes')
