"""M1.CT1: native translated assemblies; no resampling or gameplay atlas writes."""
from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/review/contact-lab';OUT.mkdir(parents=True,exist_ok=True)
m=json.loads((ROOT/'assets/playable/overworld/master.json').read_text());im=Image.open(ROOT/'assets/playable/overworld/master.png').convert('RGBA');tiles={t['id']:t for t in m['tiles']}
def tile(id):
 t=tiles[id];return im.crop((t['x'],t['y'],t['x']+32,t['y']+32))
def assemble(rows):
 r=Image.new('RGBA',(len(rows[0])*32,len(rows)*32))
 for y,row in enumerate(rows):
  for x,id in enumerate(row):r.alpha_composite(tile(id),(x*32,y*32))
 return r
house=assemble(m['assemblies']['house.cottage'])
# Keep the complete existing skirting material; remove its former ground rows.
wall=Image.new('RGBA',(160,64))
for x in range(5):
 wall.paste(tile('interior.base.wood').crop((0,0,32,20)),(x*32,0))
 wall.paste(tile('interior.base.wood').crop((0,0,32,20)),(x*32,20))
 wall.paste(tile('interior.base.wood').crop((0,4,32,28)),(x*32,40))
cliff=assemble([[f'cliff.{y}.{ "left" if x==0 else "right" if x==4 else "center"}' for x in range(5)] for y in range(3)])
# Cliff.2 has a ground tail; keep native rows but treat that tail as contact ground.
# Replace just the final four preexisting ground rows with the preceding rock row,
# so all three fixture structures have an exact shared terminal material boundary.
for x in range(160):
 for y in range(92,96):cliff.putpixel((x,y),cliff.getpixel((x,90)))
ground={'grass':tile('meadow.grass.0'),'path':tile('meadow.path.255.0'),'paving':tile('paving.255')}
wood=Image.new('RGBA',(32,32),'#dbc298')
from PIL import ImageDraw
d=ImageDraw.Draw(wood);d.line((0,0,31,0),fill='#b89e76');d.line((0,16,31,16),fill='#b89e76');d.line((10,0,10,15),fill='#b89e76');d.line((25,16,25,31),fill='#b89e76');ground['wood']=wood
for key,r in ground.items():r.save(OUT/f'ground-{key}.png')
entries=[];cells=[];sheet=Image.new('RGBA',(640,4*3*4*32))
for option,cut in [('A',8),('B',16),('C',24),('D',28)]:
 for kind,src in [('house',house),('wall',wall),('cliff',cliff)]:
  for surface,g in ground.items():
   r=Image.new('RGBA',(160,src.height+32))
   for x in range(5):r.paste(g,(x*32,src.height))
   r.alpha_composite(src,(0,cut))
   name=f'{kind}-{surface}-{option}.png';r.save(OUT/name)
   row=len(entries);sheet.paste(r.crop((0,src.height,160,src.height+32)),(0,row*32))
   # Include a large single-cell swatch, enlarged only for the optional study sheet.
   entries.append({'id':name[:-4],'image':name,'size':[r.width,r.height],'baseRow':src.height,'materialRows':cut,'groundRows':32-cut,'blockedCell':True,'structureTranslation':[0,cut],'sourceSize':[src.width,src.height]})
   for x in range(5):cells.append({'id':f'{kind}.{surface}.{option}.{x}','rect':[x*32,row*32,32,32],'materialRows':cut,'blocked':True})
sheet=sheet.crop((0,0,160,len(entries)*32));sheet.save(OUT/'transitions.png')
(OUT/'manifest.json').write_text(json.dumps({'format':'critz-contact-lab-v1','approval':'User comparison required; no gameplay replacement','method':'Native source translated in fixed padded frame; full collision cell unchanged','sourceMasterSHA256':hashlib.sha256((ROOT/'assets/playable/overworld/master.png').read_bytes()).hexdigest(),'assets':entries,'transitionSheet':'transitions.png','cells':cells},indent=2)+'\n')
print(json.dumps({'assemblies':len(entries),'transitionCells':len(cells),'sheet':sheet.size}))
