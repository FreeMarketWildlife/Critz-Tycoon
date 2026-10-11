from PIL import Image
from pathlib import Path
import json,base64,math
m=json.loads(Path('/tmp/critz-coastal-format-pixels.json').read_text());out=Path('assets/review/coastal-format');images=[];unique={};entries=[]
for e in m['entries']:
 rgba=base64.b64decode(e.pop('rgba'))
 if rgba not in unique:unique[rgba]=len(images);images.append(rgba)
 entries.append(dict(e,tileId=unique[rgba],empty=not any(rgba),w=32,h=32))
lookup={a['id']:a for a in entries};animations={}
for side in ['inner','outer']:
 for mask in m['contexts']:
  seq=[lookup[f'shore.{side}.wash.{mask}.{f}'] for f in range(32)]
  if all(a['empty'] for a in seq):continue
  # Sequence heads need distinct Tiled IDs even when their first pixels match.
  n=len(images);images.append(images[seq[0]['tileId']]);animations[n]=[dict(tileid=a['tileId'],duration=100) for a in seq];seq[0]['animationTileId']=n
sheet=Image.new('RGBA',(512,math.ceil(len(images)/16)*32))
for n,rgba in enumerate(images):sheet.paste(Image.frombytes('RGBA',(32,32),rgba),(n%16*32,n//16*32))
for a in entries:a.update(x=a['tileId']%16*32,y=a['tileId']//16*32)
sheet.save(out/'atlas.png');manifest=dict(image='atlas.png',format=m['format'],masks=m['masks'],contexts=m['contexts'],assets=entries,nativeTileCount=len(images),uniquePixelFrames=len(unique),loopSeconds=3.2,thinCaps=False)
(out/'atlas.json').write_text(json.dumps(manifest,indent=2)+'\n');tiles=[]
for n in range(len(images)):
 ids=[a['id'] for a in entries if a['tileId']==n];t=dict(id=n,properties=[dict(name='aliases',type='string',value=json.dumps(ids))]);
 if n in animations:t['animation']=animations[n]
 tiles.append(t)
tiled=dict(type='tileset',version='1.10',name='Critz shared coast format · WA8',tilewidth=32,tileheight=32,tileoffset=dict(x=0,y=16),tilecount=len(images),columns=16,image='atlas.png',imagewidth=sheet.width,imageheight=sheet.height,tiles=tiles)
(out/'format.tsj').write_text(json.dumps(tiled,indent=2)+'\n');tiled.update(name='Critz shared surface format · WA8',tileoffset=dict(x=0,y=0));(out/'surface.tsj').write_text(json.dumps(tiled,indent=2)+'\n');print(len(images),'native tiles;',len(unique),'unique pixel frames;',len(animations),'wash sequences; no thin caps or strips')
