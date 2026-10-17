"""Extract original Emerald reference frames only; never author dummy geometry.
Usage: bundled-python scripts/extract-emerald-directions.py SOURCE_DIRECTORY
SOURCE_DIRECTORY contains emerald-brendan.png and pinned object-event-{anims,pics,info}.h.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,re,sys
root=Path(__file__).resolve().parents[1];src=Path(sys.argv[1]);out=root/'sprite-editor/assets/emerald-brendan';out.mkdir(parents=True,exist_ok=True)
revision='5eff78649e7170a877b961ef0b3da13b81a16038';strip=Image.open(src/'emerald-brendan.png');assert strip.size==(144,32) and strip.mode=='P'
source_hash=hashlib.sha256((src/'emerald-brendan.png').read_bytes()).hexdigest();assert source_hash=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
info=(src/'object-event-info.h').read_text();declaration=info.split('gObjectEventGraphicsInfo_BrendanNormal = {',1)[1].split('};',1)[0];assert '.width = 16' in declaration and '.height = 32' in declaration and '.anims = sAnimTable_BrendanMayNormal' in declaration and '.images = sPicTable_BrendanNormal' in declaration
pics=(src/'object-event-pics.h').read_text().split('sPicTable_BrendanNormal[] = {',1)[1].split('};',1)[0];assert [int(n) for n in re.findall(r'overworld_frame\(gObjectEventPic_BrendanNormal, 2, 4, (\d+)\)',pics)]==list(range(9))
anims=(src/'object-event-anims.h').read_text();table=anims.split('sAnimTable_BrendanMayNormal[]',1)[1].split('};',1)[0]
for name in ['GoNorth','GoWest','GoEast']:assert 'sAnim_'+name in table
families={};checks=[];tick_ms=280896/16777216*1000
for direction,title,expected in [('north','North',[5,1,6,1]),('west','West',[7,2,8,2]),('east','East',[7,2,8,2])]:
 block=anims.split('sAnim_Go'+title+'[]',1)[1].split('};',1)[0];commands=re.findall(r'ANIMCMD_FRAME\((\d+),\s*(\d+)([^)]*)\)',block);assert [int(x[0]) for x in commands]==expected and all(int(x[1])==8 for x in commands);assert all(('hFlip = TRUE' in x[2])==(direction=='east') for x in commands)
 frames=[]
 for slot in range(8):
  index=expected[slot//2];tile=strip.crop((index*16,0,index*16+16,32));rgba=tile.convert('RGBA');mask=Image.new('L',tile.size);mask.putdata([0 if v==0 else 255 for v in tile.get_flattened_data()]);rgba.putalpha(mask)
  if direction=='east':rgba=rgba.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  large=rgba.resize((32,64),Image.Resampling.NEAREST);p=out/f'{direction}-{slot}.png';large.save(p);assert large.resize((16,32),Image.Resampling.NEAREST).tobytes()==rgba.tobytes();assert set(large.getchannel('A').get_flattened_data())<={0,255};checks.append(f'{direction} slot{slot} exact nearest2x, binary alpha, declared frame/flip')
  frames.append({'file':p.name,'sourceFrame':index,'hFlip':direction=='east','sourceCommand':slot//2,'uiHalf':slot%2,'ticks':4,'durationMs':4*tick_ms,'pose':['stride A','idle','stride B','idle'][slot//2],'bounds':list(large.getbbox()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 families[direction]={'kind':'original-emerald-nearest-2x','label':'Original Emerald Brendan · native16×32 enlarged nearest2×','frames':frames,'sourceOrder':expected,'sourceHoldTicks':8,'uiSlots':'Each 8-update source command split into two identical 4-update selectable UI slots; pixels/order/total duration unchanged.','loopMs':32*tick_ms,'anchor':[16,64]}
metadata={name:{'sha256':hashlib.sha256((src/name).read_bytes()).hexdigest()} for name in ['object-event-anims.h','object-event-pics.h','object-event-info.h']}
manifest={'sourceRevision':revision,'sourceURL':f'https://raw.githubusercontent.com/pret/pokeemerald/{revision}/graphics/object_events/pics/people/brendan/walking.png','sourceSHA256':source_hash,'nativeFrame':[16,32],'displayFrame':[32,64],'background':'Source palette index0 transparent; other raw PNG palette RGB retained, not emulator color capture','tickMs':tick_ms,'animationDeclarations':metadata,'notFanRefined':True,'directions':families}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(root/'docs/reviews/M1-DC2/reference-extraction.json').write_text(json.dumps({'pass':True,'checks':checks,'sourceRevision':revision,'sourceSHA256':source_hash,'mapping':{d:f['sourceOrder'] for d,f in families.items()},'eastSourceHFlip':True,'fixedAnchor':[16,64],'notFanRefined':True},indent=2)+'\n')
# Reference-bearing inspection stays ignored.
plate=Image.new('RGBA',(8*104,3*220),(32,38,40,255));draw=ImageDraw.Draw(plate)
for y,(direction,family) in enumerate(families.items()):
 for i,f in enumerate(family['frames']):
  image=Image.open(out/f['file']);plate.alpha_composite(image.resize((96,192),Image.Resampling.NEAREST),(i*104,y*220+24));draw.text((i*104,y*220),direction+' '+str(i+1)+' f'+str(f['sourceFrame']),fill='white')
plate.save(src/'emerald-reference-inspection.png');print('Verified24 reference slots; original8tick commands preserved; source',source_hash)
