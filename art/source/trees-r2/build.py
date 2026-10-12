"""Original integer-grid tree authoring; no sampled/resized concept pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'assets/review/trees-r2'
REVIEW = ROOT / 'docs/reviews/M1-TR2'
OUT.mkdir(parents=True, exist_ok=True)
REVIEW.mkdir(parents=True, exist_ok=True)
LEAF = ['#173f3c', '#245744', '#327347', '#4a914b', '#70ae50', '#a0cc60', '#c6df7a']
WOOD = ['#463b2b', '#6a5134', '#997244', '#c09b62']

def crown(im, cx, cy, rx, ry, ramp=LEAF):
    """Authored stepped lobe with connected upper planes and short leaf facets."""
    d = ImageDraw.Draw(im)
    outline = [(-.15,-1),(.18,-1),(.18,-.88),(.48,-.88),(.48,-.72),(.7,-.72),(.7,-.5),(.87,-.5),(.87,-.2),(1,-.2),(1,.27),(.9,.27),(.9,.55),(.68,.55),(.68,.76),(.36,.76),(.36,.91),(-.1,.91),(-.1,1),(-.38,1),(-.38,.86),(-.66,.86),(-.66,.67),(-.87,.67),(-.87,.42),(-1,.42),(-1,.05),(-.9,.05),(-.9,-.28),(-.74,-.28),(-.74,-.55),(-.52,-.55),(-.52,-.8),(-.15,-.8)]
    p = [(cx+round(x*rx), cy+round(y*ry)) for x,y in outline]
    mask = Image.new('1', im.size); ImageDraw.Draw(mask).polygon(p, fill=1)
    d.polygon(p, fill=ramp[0])
    # Connected hue/value bands describe volume; retain a one-pixel contour.
    for y in range(cy-ry+1, cy+ry):
        for x in range(cx-rx+1,cx+rx):
            if not (0<=x<im.width and 0<=y<im.height and mask.getpixel((x,y))): continue
            if not all(mask.getpixel((x+dx,y+dy)) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]): continue
            u=(x-cx)/rx; v=(y-cy)/ry
            tier = 4 if v<-.25 else 3 if v<.25 else 2 if v<.64 else 1
            if u>.45: tier-=1
            d.point((x,y),fill=ramp[max(1,tier)])
    # Deliberately placed interlocking stair-step leaf planes, clipped to lobe.
    facets=[(-.42,-.40,5),(-.08,-.61,6),(.27,-.32,5),(-.64,-.03,4),(-.21,-.02,5),(.13,.17,4),(.48,.12,3),(-.38,.45,3),(.05,.55,2)]
    for u,v,t in facets:
        x=cx+round(u*rx); y=cy+round(v*ry)
        pts=[(x-2,y),(x,y),(x,y-2),(x+3,y-2),(x+3,y),(x+5,y),(x+5,y+2),(x+2,y+2),(x+2,y+4),(x-1,y+4),(x-1,y+2),(x-2,y+2)]
        patch=Image.new('RGBA',im.size); ImageDraw.Draw(patch).polygon(pts,fill=ramp[t])
        for yy in range(max(0,y-2),min(im.height,y+5)):
            for xx in range(max(0,x-2),min(im.width,x+6)):
                if patch.getpixel((xx,yy))[3] and mask.getpixel((xx,yy)) and im.getpixel((xx,yy))[:3] != tuple(bytes.fromhex(ramp[0][1:])):
                    im.putpixel((xx,yy),patch.getpixel((xx,yy)))

def roots(im, wide=False, palm=False):
    d=ImageDraw.Draw(im)
    d.polygon([(28,42 if palm else 55),(36,42 if palm else 55),(37,70),(40,75),(45 if wide else 41,78),(45 if wide else 41,79),(34,78),(31,79),(20 if wide else 23,79),(23,76),(27,71)],fill=WOOD[0])
    d.polygon([(29,43 if palm else 56),(34,43 if palm else 56),(35,70),(38,75),(40,77),(34,76),(32,78),(26,78),(29,72)],fill=WOOD[1])
    d.polygon([(29,43 if palm else 56),(31,43 if palm else 56),(31,71),(28,76),(26,77),(30,77),(33,74),(33,70),(32,43 if palm else 56)],fill=WOOD[2])
    d.line((29,44 if palm else 60,29,70),fill=WOOD[3]);d.line((28,73,26,76),fill=WOOD[3])
    if palm:
        for y in [44,49,54,59,64,69,74]:
            d.line((29,y,34,y+1),fill=WOOD[3]);d.line((31,y+2,35,y+2),fill=WOOD[0])

def make(name):
    wide=name in ['old-grove','soft-willow']
    im=Image.new('RGBA',(96 if wide else 64,96))
    base=Image.new('RGBA',(64,96));roots(base, name=='old-grove', name=='coastal-palm');im.paste(base,(16 if wide else 0,0))
    if name=='tiered-cedar':
        # Bottom-to-top layers: silhouette stays within y16..79.
        crown(im,32,55,27,14)
        crown(im,31,42,22,13)
        crown(im,32,29,15,13)
    elif name=='old-grove':
        crown(im,48,53,40,16)
        crown(im,22,42,18,15);crown(im,73,42,18,15)
        crown(im,47,34,25,18)
        crown(im,22,53,17,12);crown(im,72,53,18,12)
    elif name=='soft-willow':
        crown(im,48,39,42,20)
        d=ImageDraw.Draw(im)
        curtains=[(7,43,13,68),(18,46,24,72),(30,48,36,67),(59,47,65,70),(73,43,79,73),(84,40,89,64)]
        for x,y,x2,end in curtains:
            d.polygon([(x,y),(x2,y-2),(x2+1,end-8),(x2-1,end-8),(x2-1,end-2),(x+1,end-2),(x+1,end),(x,end),(x-1,end-9)],fill=LEAF[0])
            d.polygon([(x+1,y),(x2-1,y),(x2-1,end-10),(x+2,end-4),(x+1,end-4)],fill=LEAF[3])
            d.line((x+1,y+2,x+1,end-11),fill=LEAF[5])
            for yy in range(y+7,end-10,8):d.line((x+2,yy,x2-1,yy-2),fill=LEAF[4])
        crown(im,43,32,28,16)
    else:
        d=ImageDraw.Draw(im)
        # Six distinct palm fronds, defined as angular folded leaves.
        fronds=[[(31,36),(23,24),(16,19),(9,20),(13,24),(19,27),(24,34),(28,43)],[(31,34),(33,21),(39,16),(45,17),(43,22),(38,25),(35,40)],[(32,36),(45,28),(55,28),(60,32),(60,37),(53,34),(43,35),(35,42)],[(29,38),(18,31),(9,33),(3,40),(3,46),(9,42),(17,39),(27,43)],[(33,40),(43,39),(52,45),(57,55),(57,62),(52,58),(48,51),(39,47),(32,46)],[(29,40),(21,43),(15,53),(12,65),(8,69),(7,61),(10,50),(17,40),(27,37)]]
        for i,p in enumerate(fronds):
            d.polygon(p,fill=LEAF[0])
            cx=sum(x for x,y in p)/len(p);cy=sum(y for x,y in p)/len(p)
            inner=[(round(x*.84+cx*.16),round(y*.84+cy*.16)) for x,y in p]
            d.polygon(inner,fill=LEAF[3 if i<3 else 2])
            # One bright vein with small paired facets; dark underside retained.
            tip=p[2];vein=Image.new('RGBA',im.size);vd=ImageDraw.Draw(vein)
            vd.line((31,39,tip[0],tip[1]+2),fill=LEAF[5],width=2)
            vd.line((31,41,tip[0]+1,tip[1]+4),fill=LEAF[4])
            mask=Image.new('1',im.size);ImageDraw.Draw(mask).polygon(p,fill=1)
            for yy in range(16,70):
                for xx in range(64):
                    if mask.getpixel((xx,yy)) and vein.getpixel((xx,yy))[3]:im.putpixel((xx,yy),vein.getpixel((xx,yy)))
        d.rectangle((28,38,34,44),fill=LEAF[1]);d.rectangle((29,38,32,40),fill=LEAF[4])
    return im

names=['tiered-cedar','soft-willow','old-grove','coastal-palm']
assets=[]
for name in names:
    im=make(name);im.save(OUT/f'{name}.png');width=im.width;offset=(width-64)//2
    palette=[None]+sorted({'#%02x%02x%02x'%p[:3] for p in im.get_flattened_data() if p[3]})
    lookup={c:i for i,c in enumerate(palette)}
    pixels=[lookup['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in im.get_flattened_data()]
    project={'format':'fmw-sprite','version':1,'name':name.replace('-',' ').title(),'preset':'custom','width':width,'height':96,'palette':palette,'bank':'wildlife','notes':'M1.TR2 native review. Ground anchor at (canvasWidth/2,80); explicit middle-row collision in objects.json. No inferred alpha collision.','frames':[{'name':'Static review','ticks':8,'pixels':pixels}]}
    (Path(__file__).parent/f'{name}.sprite.json').write_text(json.dumps(project,indent=2)+'\n')
    assets.append({'id':f'tree-r2:{name}','image':f'{name}.png','canvasPixels':[width,96],'canvasTiles':[width//32,3],'paintBounds':list(im.getbbox()),'groundAnchorPixels':[width//2,80],'sortAnchorPixels':[width//2,64],'collisionCells':[[0,0],[1,0]],'collisionRectPixels':[offset,32,64,32],'placementOrigin':'top-left of2×1 ground footprint; collisionCells relative to that origin','drawOffsetFromFootprintPixels':[-offset,-32],'visualOnlyRows':[0,2],'protruding':True,'approval':'awaiting user visual review'})
(OUT/'objects.json').write_text(json.dumps({'format':'critz-protruding-object-review','version':1,'tileSize':32,'coordinateSystem':'PNG top-left, x right, y down','assets':assets},indent=2)+'\n')
# Native and exact enlarged presentation. Guides never enter asset PNGs.
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
plate=Image.new('RGB',(1472,600),'#f3f0df');d=ImageDraw.Draw(plate)
d.text((24,16),'M1.TR2 — Native protruding tree objects · review',font=font,fill='#23473c')
for i,a in enumerate(assets):
    x=20+i*364; im=Image.open(OUT/a['image'])
    d.text((x,55),names[i].replace('-',' ').title(),font=font,fill='#23473c')
    plate.paste(im,(x,90),im)
    scaled=im.resize((im.width*4,384),Image.Resampling.NEAREST)
    bg=Image.new('RGB',(im.width*4,384),'#a9bb7a');bg.paste(scaled,(0,0),scaled)
    plate.paste(bg,(x,196))
    d.text((x+im.width+10,113),f'1× · {im.width}×96',font=small,fill='#23473c')
    d.text((x+im.width+10,140),'4× below',font=small,fill='#23473c')
plate.save(REVIEW/'trees-native-and-4x.png')
guide=plate.copy();d=ImageDraw.Draw(guide)
for i,a in enumerate(assets):
    x=20+i*364; y=196;w=a['canvasPixels'][0]*4;off=a['collisionRectPixels'][0]*4
    d.rectangle((x+off,y+128,x+off+255,y+255),outline='#df533f',width=3)
    for xx in range(0,w+1,128):d.line((x+xx,y,x+xx,y+384),fill='#faf0d5',width=1)
    for yy in [0,128,256,384]:d.line((x,y+yy,x+w,y+yy),fill='#faf0d5',width=1)
    for yy in [64,320]:d.line((x,y+yy,x+w,y+yy),fill='#3a68a2',width=2)
    d.ellipse((x+w//2-4,y+316,x+w//2+4,y+324),fill='#fbd85d')
guide.save(REVIEW/'registration-proof.png')
print('4 native transparent PNGs (cedar/palm64×96; willow/grove96×96), editable sources, object metadata and exact4× plates')
