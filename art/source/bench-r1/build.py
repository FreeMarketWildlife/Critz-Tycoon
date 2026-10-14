"""Native bench construction and seated lower-body poses; existing Hero upper pixels retained."""
from pathlib import Path
from PIL import Image, ImageDraw
import json
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'assets/review/bench-r1';OUT.mkdir(parents=True,exist_ok=True)
dark='#493d32';wood='#997045';light='#d4aa6c';edge='#6d5137';metal='#405a56';shine='#83958a'
for face in ['down','up','left','right']:
    side=face in ['left','right'];im=Image.new('RGBA',(32,96) if side else (64,64));front=Image.new('RGBA',im.size);d=ImageDraw.Draw(im);f=ImageDraw.Draw(front)
    if not side:
        # Real plank seat, four legs, arms and joined backrest: no ground fill.
        for x in [9,49]:
            d.rectangle((x,26,x+5,47),fill=metal);d.line((x+1,28,x+1,46),fill=shine)
        seatY=32 if face=='down' else 25
        d.polygon([(7,seatY),(52,seatY),(57,seatY+5),(4,seatY+5)],fill=dark)
        for y in [seatY,seatY+3]:d.line((8,y,51,y),fill=light);d.line((6,y+1,54,y+1),fill=wood)
        backY=16 if face=='down' else 37
        for y in [backY,backY+6]:
            target=f if face=='up' else d
            target.rectangle((7,y,56,y+4),fill=dark);target.rectangle((8,y+1,55,y+2),fill=wood);target.line((8,y+1,55,y+1),fill=light)
        for x in [7,54]:
            d.rectangle((x,seatY-3,x+3,seatY+5),fill=metal);d.line((x,seatY-3,x+3,seatY-3),fill=shine)
        if face=='down':f.rectangle((5,seatY+5,56,seatY+7),fill=edge);f.line((6,seatY+5,55,seatY+5),fill=light)
    else:
        # Profile is two map cells long, with continuous boards and two supports.
        d.rectangle((22,16,27,72),fill=dark)
        for x in [22,26]:d.line((x,17,x,70),fill=light if x==22 else edge)
        d.rectangle((9,31,22,68),fill=dark)
        for x in [10,14,18]:d.line((x,32,x,66),fill=wood);d.line((x,32,x,34),fill=light)
        for y in [39,71]:
            d.rectangle((10,y,14,y+8),fill=metal);d.line((11,y+1,11,y+7),fill=shine)
        for y in [30,65]:d.rectangle((6,y,25,y+3),fill=metal);d.line((7,y,23,y),fill=shine)
        f.rectangle((8,34,10,68),fill=edge)
        if face=='right':im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT);front=front.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    im.save(OUT/f'bench-{face}.png');front.save(OUT/f'bench-{face}-front.png')

atlas=json.loads((ROOT/'assets/playable/living/atlas.json').read_text());sheet=Image.open(ROOT/'assets/playable/living'/atlas['image']).convert('RGBA')
for face,index in [('down',1),('up',5),('left',9),('right',13)]:
    entry=next(a for a in atlas['assets'] if a['id']==f'hero-boy.{index}');x,y,w,h=entry['rect'];idle=sheet.crop((x,y,x+w,y+h));pose=Image.new('RGBA',(w,h))
    pose.paste(idle.crop((0,0,w,48)),(0,0));d=ImageDraw.Draw(pose)
    # Deliberate bent seated thighs/knees/shoes below the unchanged shirt.
    pants='#4b5541';pantsLight='#728465';ink='#292532';shoe='#eddfb5';skin='#905439'
    if face in ['down','up']:
        for x0 in [8,18]:
            d.rectangle((x0,48,x0+6,52),fill=ink);d.rectangle((x0+1,48,x0+5,50),fill=pantsLight)
            d.rectangle((x0+1,53,x0+4,55),fill=skin if face=='down' else pants)
            d.rectangle((x0,56,x0+6,58),fill=ink);d.line((x0+1,56,x0+5,56),fill=shoe)
    else:
        if face=='left':
            d.polygon([(11,48),(23,48),(23,52),(13,52),(13,57),(7,57),(7,54),(10,54)],fill=ink)
            d.rectangle((11,49,21,50),fill=pantsLight);d.rectangle((10,52,12,55),fill=skin);d.line((7,56,12,56),fill=shoe)
        else:
            d.polygon([(8,48),(20,48),(21,54),(24,54),(24,57),(18,57),(18,52),(8,52)],fill=ink)
            d.rectangle((10,49,20,50),fill=pantsLight);d.rectangle((19,52,21,55),fill=skin);d.line((19,56,24,56),fill=shoe)
    pose.save(OUT/f'hero-sit-{face}.png')
    palette=[None]+sorted({'#%02x%02x%02x'%p[:3] for p in pose.get_flattened_data() if p[3]});lookup={c:i for i,c in enumerate(palette)}
    pixels=[lookup['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in pose.get_flattened_data()]
    (Path(__file__).parent/f'hero-sit-{face}.sprite.json').write_text(json.dumps({'format':'fmw-sprite','version':1,'name':f'Hero seated {face}','preset':'character','width':w,'height':h,'palette':palette,'bank':'wildlife','notes':'Original seated lower-body adaptation; gameplay idle upper pixels unchanged. Review only.','frames':[{'name':'Seated','ticks':8,'pixels':pixels}]},indent=2)+'\n')
print('Four bench orientations, foreground masks and seated Hero poses')
