"""Independent native export and registration checks for M1.TR2."""
from pathlib import Path
from PIL import Image
import json, hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'assets/review/trees-r2';REVIEW=ROOT/'docs/reviews/M1-TR2'
data=json.loads((OUT/'objects.json').read_text());results=[]
for a in data['assets']:
    name=a['id'].split(':')[1];p=OUT/a['image'];im=Image.open(p).convert('RGBA')
    src=json.loads((Path(__file__).parent/f'{name}.sprite.json').read_text())
    assert im.size==tuple(a['canvasPixels'])
    assert im.size==((96,96) if name in ['soft-willow','old-grove'] else (64,96))
    pixels=list(im.get_flattened_data())
    assert set(p[3] for p in pixels)=={0,255}
    assert im.getbbox()[1]==16 and im.getbbox()[3]==80
    assert a['collisionCells']==[[0,0],[1,0]]
    assert a['collisionRectPixels']==[(im.width-64)//2,32,64,32]
    assert a['groundAnchorPixels']==[im.width//2,80]
    assert a['drawOffsetFromFootprintPixels']==[-(im.width-64)//2,-32]
    assert a['sortAnchorPixels']==[im.width//2,64]
    reconstructed=[tuple(bytes.fromhex(src['palette'][i][1:]))+(255,) if i else (0,0,0,0) for i in src['frames'][0]['pixels']]
    assert reconstructed==pixels,'Indexed editor source must exactly reproduce PNG'
    # Every occupied pixel is connected: no floating trunks/fronds/root scraps.
    filled={(x,y) for y in range(im.height) for x in range(im.width) if im.getpixel((x,y))[3]}
    unseen=set(filled);components=[]
    while unseen:
        todo=[unseen.pop()];count=0
        while todo:
            x,y=todo.pop();count+=1
            for pt in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if pt in unseen:unseen.remove(pt);todo.append(pt)
        components.append(count)
    assert len(components)==1,(name,components)
    # Transparency preserves three distinct ground materials exactly outside sprite.
    for color in ['#a9bb7a','#d6bd84','#9babb0']:
        bg=Image.new('RGBA',im.size,color);composite=Image.alpha_composite(bg,im)
        for xy in [(0,0),(im.width-1,95),(im.width//2,90)]:assert composite.getpixel(xy)==bg.getpixel(xy)
    results.append({'id':a['id'],'size':list(im.size),'bounds':list(im.getbbox()),'opaqueColors':len(set(p[:3] for p in pixels if p[3])),'occupiedPixels':len(filled),'components':components,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'checks':'dimensions, binary alpha, y16..79, middle2-cell collision, anchors, exact source export, connected art, transparent ground pass'})
(REVIEW/'native-checks.json').write_text(json.dumps({'passed':True,'assets':results,'limitations':'Static review assets only; no runtime integration or physical-phone movement check.'},indent=2)+'\n')
print(json.dumps(results,indent=2))
