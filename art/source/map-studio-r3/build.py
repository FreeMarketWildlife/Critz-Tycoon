"""Original native revision for Map Studio review. No reference-game pixels."""
from PIL import Image, ImageDraw
from pathlib import Path
import json
root=Path(__file__).resolve().parents[3]
out=root/'assets/review/map-studio-r3';out.mkdir(parents=True,exist_ok=True)
items=[]
def add(id,im,**meta):
    name=id.replace(':','-')+'.png';im.save(out/name);items.append(dict(id=id,image=name,w=im.width,h=im.height,**meta))
def house(kind,w,roof):
    im=Image.new('RGBA',(w,160));d=ImageDraw.Draw(im)
    dark,body,light,ridge=roof
    # Repeating 32px roof centers, stepped end returns and one continuous eave.
    d.polygon([(15,5),(w-16,5),(w-2,80),(w-2,91),(1,91),(1,80)],fill=dark)
    d.polygon([(17,9),(w-18,9),(w-7,79),(6,79)],fill=body)
    for y in range(13,79,8):
        inset=18-(y-9)//7
        d.line((inset,y,w-inset-1,y),fill=light)
        for x in range(16+(4 if (y//8)%2 else 0),w-16,16):
            d.line((x,y+1,x-2,min(y+6,78)),fill=dark)
    d.rectangle((17,5,w-18,8),fill=ridge)
    d.rectangle((4,80,w-5,84),fill=light)
    d.rectangle((7,85,w-8,94),fill=dark)
    d.rectangle((16,95,w-17,156),fill='#eadcb5')
    d.rectangle((16,95,w-17,99),fill='#b0a488')
    d.rectangle((16,150,w-17,159),fill='#857661')
    d.line((17,149,w-18,149),fill='#f5e9c9')
    d.rectangle((16,100,20,149),fill='#bdae88');d.rectangle((w-21,100,w-17,149),fill='#bdae88')
    center=w//2
    for x in range(32,w-32,32):
        if abs(x+16-center)<27:continue
        d.rectangle((x+3,109,x+27,135),fill='#645d50')
        d.rectangle((x+6,112,x+24,132),fill='#507e87')
        d.rectangle((x+8,113,x+13,121),fill='#a8d0ce')
        d.line((x+15,111,x+15,133),fill='#efe1ba')
        d.line((x+5,122,x+25,122),fill='#efe1ba')
        d.rectangle((x+1,136,x+29,139),fill='#b4a077')
    # Full one-cell aperture, with jambs outside it. No wall pixels close the threshold.
    d.rectangle((center-19,104,center+18,159),fill='#76654f')
    d.rectangle((center-16,108,center+15,159),fill='#253b37')
    d.rectangle((center-14,111,center+13,153),fill='#1c302e')
    d.rectangle((center-16,154,center+15,159),fill='#d5bb8c')
    if kind=='shop':
        d.rectangle((center-30,91,center+29,103),fill='#4e786c')
        d.line((center-27,93,center+26,93),fill='#b9d2a0')
        # A graphic sign, not generated tiny illegible lettering.
        d.rectangle((center-13,96,center+12,99),fill='#e8d69f')
    add('building:'+kind,im,footprint=[0,1,w//32,4],overheadRows=3,approval='M1.ME3 visual review')
    # Export real reusable native metatiles, including both eave ends and aperture halves.
    for row in range(5):
        for col in range(w//32):add(f'ME3.{kind}.{row}.{col}',im.crop((col*32,row*32,col*32+32,row*32+32)),label=kind+' '+('roof' if row<3 else 'doorway' if col==w//64 else 'wall'),layer='object',blocked=not(row==0 or col==w//64 and row==4))
house('cottage',160,('#754b3e','#ba7050','#d28b60','#eab180'))
house('garden',160,('#365c58','#5b9080','#78ab8c','#bdd0a0'))
house('shop',224,('#375c66','#56878d','#79a7a2','#b9ccaf'))
for direction in ['down','up','left','right']:
    for mask in range(4):
        im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im)
        a=0 if mask&1 else 8;b=31 if mask&2 else 23
        if direction in ['down','up']:
            top=32 if direction=='down' else 16
            d.rectangle((a,top,b,top+3),fill='#75ae68')
            d.rectangle((a,top+4,b,top+6),fill='#b5ce87')
            d.rectangle((a,top+7,b,top+12),fill='#b79a67')
            d.line((a,top+13,b,top+13),fill='#806c4d')
            d.line((a+1,top+14,b-1,top+14),fill='#699b5e')
            if not mask&1:d.line((a,top+4,a,top+13),fill='#806c4d')
            if not mask&2:d.line((b,top+4,b,top+13),fill='#806c4d')
        else:
            top=16+(0 if mask&1 else 8);bottom=16+(31 if mask&2 else 23)
            d.rectangle((8,top,23,bottom),fill='#b79a67')
            x=8 if direction=='left' else 23
            d.line((x,top,x,bottom),fill='#806c4d')
            d.line((23 if direction=='left' else 8,top,23 if direction=='left' else 8,bottom),fill='#b5ce87')
            if not mask&1:d.line((8,top,23,top),fill='#806c4d')
            if not mask&2:d.line((8,bottom,23,bottom),fill='#806c4d')
        # Small soil clusters and a visible turf lip; keep joining edge pixels exact.
        if direction in ['down','up']:
            for xx,yy in [(11,top+8),(18,top+10),(25,top+7)]:
                if a+2<=xx<=b-3:d.rectangle((xx,yy,xx+2,yy+1),fill='#a58a5d')
            if direction=='up':
                old=im.copy()
                for yy in range(16,32):
                    for xx in range(32):im.putpixel((xx,yy),old.getpixel((xx,47-yy)))
        else:
            lip=21 if direction=='left' else 8
            d.rectangle((lip,top,lip+2,bottom),fill='#75ae68')
            for xx,yy in [(12,27),(16,34),(11,39)]:
                if top+2<=yy<=bottom-2:d.rectangle((xx,yy,xx+2,yy+1),fill='#a58a5d')
        add(f'ledge:{direction}:{mask}',im,registered=True,footprint=[0,0,1,1],contact=dict(x=8,y=16,w=16,h=32),approval='M1.ME3 visual review')
# Append sand joins; preserve all original master pixels and IDs.
world=json.loads((root/'assets/playable/overworld/master.json').read_text());master=Image.open(root/'assets/playable/overworld/master.png').convert('RGBA');tiles={t['id']:t for t in world['tiles']}
def original(id):
    t=tiles[id];return master.crop((t['x'],t['y'],t['x']+32,t['y']+32))
props=json.loads((root/'assets/review/coastal-format/props.json').read_text());sheet=Image.open(root/'assets/review/coastal-format/props.png').convert('RGBA');a=next(a for a in props['assets'] if a['id']=='sand.0');sand=sheet.crop((a['x'],a['y'],a['x']+32,a['y']+32))
base={'grass':original('meadow.grass.0'),'sand':sand,'path':original('meadow.path.255.0'),'paving':original('ground.paving'),'soil':original('ground.soil')}
def normal(m):
    for bit,a,b in [(16,1,2),(32,2,4),(64,4,8),(128,8,1)]:
        if not m&a or not m&b:m&=~bit
    return m
masks=sorted(set(normal(m) for m in range(256)))
def within(x,y,m):
    east=x>=16;south=y>=16;dx=31-x if east else x;dy=31-y if south else y
    vx=bool(m&(2 if east else 8));vy=bool(m&(4 if south else 1));diag=bool(m&((32 if east else 64) if south else (16 if east else 128)))
    if not vx and not vy:return dx>=5 and dy>=5 and (dx>=9 or dy>=9 or (dx-9)**2+(dy-9)**2<=16)
    if not vx:return dx>=5
    if not vy:return dy>=5
    if not diag and dx<5 and dy<5:return dx*dx+dy*dy>=25
    return True
for kind,under in [('sand','grass'),('path','sand'),('paving','sand'),('soil','sand')]:
    for mask in masks:
        im=base[under].copy();pix=im.load();fg=base[kind].load()
        for y in range(32):
            for x in range(32):
                if within(x,y,mask):pix[x,y]=fg[x,y]
        add(f'ME3.blend.{kind}.{under}.{mask}',im,layer='ground',blocked=False,neighborMask=mask)
# Registered connection pieces: no per-piece vertical reanchoring.
for mask in range(16):
    im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im)
    for y in [30,39]:
        if mask&8:d.rectangle((0,y,15,y+3),fill='#af8a58');d.line((0,y,15,y),fill='#e0be7b')
        if mask&2:d.rectangle((16,y,31,y+3),fill='#af8a58');d.line((16,y,31,y),fill='#e0be7b')
    for x in [11,20]:
        if mask&1:d.rectangle((x,16,x+2,34),fill='#af8a58')
        if mask&4:d.rectangle((x,35,x+2,47),fill='#af8a58')
    d.rectangle((13,26,18,46),fill='#927049');d.line((13,27,13,46),fill='#e0be7b');d.rectangle((13,25,18,28),fill='#d4ad6a')
    add(f'fence:{mask}',im,registered=True,footprint=[0,0,1,1],contact=dict(x=8,y=16,w=16,h=32),approval='M1.ME3 visual review')
for mask in masks:
    im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im)
    a=0 if mask&8 else 16 if mask&2 else 8;b=31 if mask&2 else 15 if mask&8 else 23
    d.rectangle((a,16,b,47),fill='#8bc77a')
    if not mask&1:d.line((a,16,b,16),fill='#b5ce87')
    if not mask&4:
        d.rectangle((a,32,b,46),fill='#b4a27b');d.line((a,32,b,32),fill='#d7c69b');d.line((a,47,b,47),fill='#806d51')
        for y in [37,43]:d.line((a,y,b,y),fill='#a18d68')
    if not mask&8:d.rectangle((a,20,min(a+3,b),46),fill='#a18d68')
    if not mask&2:d.rectangle((max(a,b-3),20,b,46),fill='#8b7b5f')
    # Explicit inward returns, including diagonal grass pockets.
    for bit,c1,c2,cx,cy in [(128,1,8,0,16),(16,1,2,31,16),(64,4,8,0,47),(32,4,2,31,47)]:
        if mask&c1 and mask&c2 and not mask&bit:
            for yy in range(5):
                for xx in range(5):
                    if xx*xx+yy*yy<25:im.putpixel((cx+xx if cx==0 else cx-xx,cy+yy if cy==16 else cy-yy),(0,0,0,0))
    add(f'cliff:{mask}',im,registered=True,footprint=[0,0,1,1],neighborMask=mask,approval='M1.ME3 visual review')
for phase in [0,1]:
    im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im)
    left=1 if phase==0 else 24
    d.rectangle((left,13,30,57),fill='#866a4b');d.line((left,13,30,13),fill='#c8a577');d.line((left,14,left,57),fill='#c8a577')
    if phase==0:
        d.rectangle((5,18,25,33),outline='#624f3a');d.rectangle((5,39,25,53),outline='#624f3a');d.rectangle((25,35,27,37),fill='#ead59b')
    add(f'door:{phase}',im,approval='M1.ME3 visual review')
(out/'sources.json').write_text(json.dumps(items,indent=2)+'\n')
print(f'{len(items)} original native source images')
