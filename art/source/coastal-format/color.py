from PIL import Image,ImageChops
from pathlib import Path
import json,math
root=Path('assets/review/coastal-format');fmt=json.loads((root/'atlas.json').read_text());fi=Image.open(root/'atlas.png');fm={a['id']:a for a in fmt['assets']}
def piece(id):
 a=fm[id];return fi.crop((a['x'],a['y'],a['x']+32,a['y']+32))
def bank(path,key='assets'):
 m=json.loads(Path(path).read_text());im=Image.open(Path(path).parent/m['image']);ids={a['id']:a for a in m[key]};return m,lambda id:im.crop((ids[id]['x'],ids[id]['y'],ids[id]['x']+32,ids[id]['y']+32))
water,w=bank('assets/review/water-terrain/atlas.json');base,b=bank('assets/review/coastal-water/atlas.json');env,e=bank('assets/playable/overworld/master.json','tiles')
materials={s:w(s+'.0') for s in water['surfaces']};materials.update(grass=e('meadow.grass.0'),sand=b('sand.0'))
pairs=[(a,g,'shore') for a in water['surfaces'] for g in ['grass','sand']]+[('sand','grass','surface'),('grass','sand','surface')]+[(a,g,'surface') for a in water['surfaces'] for g in water['surfaces'] if a!=g]
images=[];unique={};entries=[]
for a,g,kind in pairs:
 for mask in fmt['contexts']:
  im=ImageChops.offset(materials[g],0,-16) if kind=='shore' else materials[g].copy();alpha=piece(f'{kind}.inner.mask.{mask}').getchannel('A');im.paste(materials[a],(0,0),alpha)
  if kind=='shore' and g!='sand':im.alpha_composite(piece(f'shore.inner.{"rim" if "shallow" in a else "bank"}.{mask}'))
  if kind=='shore' and g=='sand' and a.endswith('moving'):im.alpha_composite(piece(f'shore.inner.wash.{mask}.0'))
  rgba=im.tobytes()
  if rgba not in unique:unique[rgba]=len(images);images.append(im)
  n=unique[rgba];entries.append(dict(id=f'join.{a}.{g}.{mask}',inner=a,outer=g,kind=kind,rawNeighborMask=mask,tileId=n,x=n%32*32,y=n//32*32,w=32,h=32,registrationY=16 if kind=='shore' else 0))
sheet=Image.new('RGBA',(1024,math.ceil(len(images)/32)*32))
for n,im in enumerate(images):sheet.paste(im,(n%32*32,n//32*32))
sheet.save(root/'colored.png');(root/'colored.json').write_text(json.dumps(dict(image='colored.png',assets=entries,contexts=fmt['contexts'],formatMasks=fmt['masks'],pairs=74,nativeTileCount=len(images),frame=0,animatedRuntimeLoopSeconds=3.2,thinCaps=False),indent=2)+'\n')
for kind,offset in [('shore',16),('surface',0)]:
 tiles=[]
 for n in range(len(images)):
  aliases=[a['id'] for a in entries if a['tileId']==n and a['kind']==kind]
  if aliases:tiles.append(dict(id=n,properties=[dict(name='aliases',type='string',value=json.dumps(aliases)),dict(name='frame',type='int',value=0)]))
 (root/f'colored-{kind}.tsj').write_text(json.dumps(dict(type='tileset',version='1.10',name=f'Critz {kind} colors · WA8',tilewidth=32,tileheight=32,tileoffset=dict(x=0,y=offset),tilecount=len(images),columns=32,image='colored.png',imagewidth=sheet.width,imageheight=sheet.height,tiles=tiles),indent=2)+'\n')
print(len(entries),'colored references;',len(images),'deduplicated native tiles; raw context retained; no caps')
# Current runtime texture/prop banks contain no retired transition/cap art.
for name,source,get,selected,meta in [
 ('props',base,b,[a for a in base['assets'] if a['kind'] in ['rock','cast-shadow'] or a['id'].startswith('sand.')],dict(grounds=base['grounds'],surfaces=water['surfaces'])),
 ('water',water,w,[a for a in water['assets'] if a['id'] in {s+'.'+str(f) for s in water['surfaces'] for f in range(32)}],dict(surfaces=water['surfaces'],loopSeconds=3.2))]:
 atlas=Image.new('RGBA',(1024,math.ceil(len(selected)/32)*32));assets=[]
 for n,a in enumerate(selected):
  x=n%32*32;y=n//32*32;atlas.paste(get(a['id']),(x,y));assets.append(dict(a,x=x,y=y,w=32,h=32))
 atlas.save(root/(name+'.png'));(root/(name+'.json')).write_text(json.dumps(dict(image=name+'.png',assets=assets,**meta),indent=2)+'\n')
 print(name,len(assets),'exact original texture/prop frames')
