"""Exact native-animation checks and independent Pillow GIF decoding."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import hashlib, json

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
ASSETS=ROOT/'assets/review/living-collection-v1'
SOURCE=ROOT/'art/source/living-collection-v1'
M=json.loads((ASSETS/'manifest.json').read_text())
BG='#f3efe5';INK='#273f45'
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def font(n):return ImageFont.truetype(FONT,n)
def rgba(project,frame):
    colors=[bytes.fromhex(c[1:])+b'\xff' if c else bytes(4) for c in project['palette']]
    return b''.join(colors[i] for i in project['frames'][frame]['pixels'])
def load(e,i):return Image.open(ASSETS/e['slug']/f'frame-{i}.png').convert('RGBA')
def components(im):
    occ={(i%im.width,i//im.width) for i,c in enumerate(im.getchannel('A').tobytes()) if c};sizes=[]
    while occ:
        todo=[occ.pop()];n=0
        while todo:
            x,y=todo.pop();n+=1
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    point=(x+dx,y+dy)
                    if point in occ:occ.remove(point);todo.append(point)
        sizes.append(n)
    return sorted(sizes,reverse=True)
checks=[];png_cells=gif_cells=0
for e in M['characters']+M['critters']+M['habitats']:
    p=json.loads((ROOT/e['source']).read_text());rle=json.loads((SOURCE/(e['slug']+'.rle.json')).read_text())
    assert len(p['palette'])<256
    decoded=[]
    for j,f in enumerate(p['frames']):
        im=load(e,j);raw=rgba(p,j)
        assert im.size==(p['width'],p['height'])
        assert im.tobytes()==raw
        assert set(im.getchannel('A').tobytes())<={0,255}
        assert hashlib.sha256(raw).hexdigest()==e['frames'][j]['rgbaSHA256']
        rows=[[c for c,n in zip(row[::2],row[1::2]) for _ in range(n)] for row in rle['frames'][j]['rows']]
        assert len(rows)==p['height'] and all(len(row)==p['width'] for row in rows)
        assert sum(rows,[])==f['pixels']
        decoded.append(im);png_cells+=im.width*im.height
        if e['kind']=='character':
            assert len(components(im))==1,(e['slug'],j,components(im))
            assert im.getbbox()[3]==(64 if j%2==0 else 62),(e['slug'],j,im.getbbox())
    gif=Image.open(ASSETS/e['slug']/'motion.gif')
    assert gif.info['loop']==0 and gif.n_frames==len(decoded)
    delays=[];elapsed=rounded=0
    for j,f in enumerate(ImageSequence.Iterator(gif)):
        assert f.convert('RGBA').tobytes()==decoded[j].tobytes(),(e['slug'],j,'GIF differs')
        elapsed+=p['frames'][j]['ticks']*M['characters'][0]['tickMs']/10
        nxt=int(elapsed+0.5);expected=max(2,nxt-rounded)*10;rounded=nxt
        assert f.info['duration']==expected
        delays.append(expected);gif_cells+=f.width*f.height
    if e['kind']=='character':
        source=json.loads((ROOT/e['stillSource']).read_text())
        assert rgba(p,1)==rgba(p,3)==rgba(source,0)
        assert hashlib.sha256(rgba(p,1)).hexdigest()==e['frontIdleRGBA']
        for d,direction in enumerate(e['directions']):
            g=Image.open(ASSETS/e['slug']/(direction+'.gif'))
            assert g.n_frames==4 and g.info['loop']==0
            assert rgba(p,d*4+1)==rgba(p,d*4+3)
            assert rgba(p,d*4)!=rgba(p,d*4+2)
            for j,f in enumerate(ImageSequence.Iterator(g)):
                assert f.convert('RGBA').tobytes()==rgba(p,d*4+j)
        if e['slug']=='hero-boy':
            old=json.loads((ROOT/'art/source/hero-boy-v1/walk.sprite.json').read_text())
            for j in range(4):assert rgba(p,j)==rgba(old,j)
        if e['slug']=='kaid':assert load(e,9).transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()!=load(e,13).tobytes()
    if e['kind']=='critter':
        assert len(set(im.tobytes() for im in decoded))>=3
        assert all(len(components(im))==1 for im in decoded),(e['slug'],[components(im) for im in decoded])
        if e['stillSource']:
            src=json.loads((ROOT/e['stillSource']).read_text());assert rgba(p,0)==rgba(src,0)
    checks.append({'slug':e['slug'],'frame':e['frame'],'frames':len(decoded),'paletteColors':len(p['palette'])-1,'pngAndEditorAndRLEExact':True,'gifDecodedExact':True,'gifDelaysMs':delays,'connectedAllFrames':True if e['kind'] in ['character','critter'] else 'layered habitat'})

def save_gif(frames,name,durations):
    # Only labeled gallery plates may be quantized to GIF's palette. Native GIFs
    # above are independently checked as exact; galleries never replace them.
    pal=frames[0].convert('RGB').quantize(colors=256)
    result=[f.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE) for f in frames]
    result[0].save(HERE/name,save_all=True,append_images=result[1:],duration=durations,loop=0,disposal=2,optimize=False)
def character_plate(frame,direction=None,grid=False):
    zoom=4;cols=6;cw=166;ch=316;plate=Image.new('RGB',(cols*cw+24,ch*2+88),BG);d=ImageDraw.Draw(plate)
    d.text((18,14),'CRITZ / WALKING CAST',font=font(26),fill=INK)
    d.text((18,50),f'{direction or "Front"} · native 32×64 frames at 4× · original idle retained',font=font(16),fill=INK)
    for n,e in enumerate(M['characters']):
        x=24+n%cols*cw;y=95+n//cols*ch
        im=load(e,frame).resize((128,256),Image.Resampling.NEAREST);plate.paste(im,(x,y),im)
        if grid:
            g=ImageDraw.Draw(plate)
            for xx in range(33):g.line((x+xx*4,y,x+xx*4,y+256),fill='#d4dbcf')
            for yy in range(65):
                if yy%10==4:g.line((x,y+yy*4,x+128,y+yy*4),fill='#6c8c97')
            g.line((x+64,y,x+64,y+256),fill='#d24c83')
        d=ImageDraw.Draw(plate);d.text((x-2,y+266),e['label'],font=font(16),fill=INK)
    return plate
front=[character_plate(j) for j in range(4)]
save_gif(front,'characters-front.gif',[130,140,130,140]);front[1].save(HERE/'characters-poster.png')
turns=[]
for d,label in enumerate(['Front','Back','Left','Right']):
    for cycle in range(3):
        for j in range(4):turns.append(character_plate(d*4+j,label))
save_gif(turns,'characters-four-directions.gif',[130,140,130,140]*12)

# Individual readable nearest-neighbor GIF previews retain each native palette.
for e in M['characters']+M['critters']:
    frames=[];p=json.loads((ROOT/e['source']).read_text())
    indices=range(4) if e['kind']=='character' else range(len(p['frames']))
    for j in indices:
        im=load(e,j).resize((p['width']*6,p['height']*6),Image.Resampling.NEAREST)
        bg=Image.new('RGBA',im.size,BG);bg.alpha_composite(im);frames.append(bg)
    delays=next(c['gifDelaysMs'] for c in checks if c['slug']==e['slug'])[:len(frames)]
    save_gif(frames,e['slug']+'-6x.gif',delays)

animals=[]
for j in range(12):
    a=Image.new('RGB',(1000,590),BG);d=ImageDraw.Draw(a)
    d.text((20,15),'CRITZ / MOVING CRITTERS',font=font(26),fill=INK)
    d.text((20,50),'Ten original motion studies · individual GIFs preserve their own timing',font=font(16),fill=INK)
    for n,e in enumerate(M['critters']):
        phase=(j//3)%4 if e['slug']=='button-snail' else j%4
        im=load(e,phase).resize((160,160),Image.Resampling.NEAREST);x=20+n%5*198;y=90+n//5*244
        a.paste(im,(x,y),im);d.text((x,y+175),e['label'],font=font(17),fill=INK);d.text((x,y+200),e['movement'],font=font(13),fill=INK)
    animals.append(a)
save_gif(animals,'critters.gif',[130,140,130,140]*3);animals[0].save(HERE/'critters-poster.png')

habitats=[]
for j in range(16):
    a=Image.new('RGB',(1184,406),BG);d=ImageDraw.Draw(a)
    d.text((20,14),'CRITZ / LIVING HABITATS',font=font(26),fill=INK)
    for n,e in enumerate(M['habitats']):
        x=16+n*390;d.text((x+4,58),e['label'],font=font(20),fill=INK)
        im=load(e,j).resize((384,288),Image.Resampling.NEAREST);a.paste(im,(x,89),im)
    habitats.append(a)
save_gif(habitats,'habitats.gif',[130,140,130,140]*4);habitats[0].save(HERE/'habitats-poster.png')

props=Image.new('RGB',(640,320),BG);d=ImageDraw.Draw(props)
d.text((16,15),'Separate native 96×96 world props · 2× view',font=font(22),fill=INK)
for n,e in enumerate(M['habitats']):
    im=Image.open(ASSETS/e['slug']/'world-prop.png').convert('RGBA');assert im.size==(96,96)
    p=json.loads((SOURCE/(e['slug']+'-world-prop.sprite.json')).read_text());assert im.tobytes()==rgba(p,0)
    im=im.resize((192,192),Image.Resampling.NEAREST);props.paste(im,(16+n*208,58),im)
    d.text((16+n*208,270),e['slug'].title(),font=font(18),fill=INK)
props.save(HERE/'world-props.png')

direction_plate=Image.new('RGB',(800,990),BG);d=ImageDraw.Draw(direction_plate)
for n,e in enumerate(M['characters']):
    x=n%2*400;y=n//2*165;d.text((x+8,y+6),e['label']+' — front / back / left / right',font=font(16),fill=INK)
    for k,j in enumerate([1,5,9,13]):
        im=load(e,j).crop((0,16,32,64)).resize((96,144),Image.Resampling.NEAREST);direction_plate.paste(im,(x+k*98,y+21),im)
direction_plate.save(HERE/'directions-poster.png')
critter_plate=Image.new('RGB',(800,690),BG);d=ImageDraw.Draw(critter_plate)
for n,e in enumerate(M['critters']):
    x=n%2*400;y=n//2*138;d.text((x+8,y+6),e['label'],font=font(16),fill=INK)
    for j in range(4):
        im=load(e,j).resize((96,96),Image.Resampling.NEAREST);critter_plate.paste(im,(x+j*98,y+28),im)
critter_plate.save(HERE/'critter-poses.png')

# Countable main-cast contact plate: both strides and unchanged passing pose.
core=M['characters'][:5];g=Image.new('RGB',(1320,1210),BG);d=ImageDraw.Draw(g)
d.text((22,16),'CORE WALK / native cells, x16, Y0 at bottom',font=font(25),fill=INK)
for row,j in enumerate([0,1,2]):
    for n,e in enumerate(core):
        x=36+n*263;y=88+row*370;scale=5;im=load(e,j).resize((160,320),Image.Resampling.NEAREST)
        g.paste(im,(x,y),im);d.text((x,y+345),['Stride A','Passing','Stride B'][row],font=font(14),fill=INK)
        if row==0:d.text((x,y-26),e['label'],font=font(16),fill=INK)
        overlay=Image.new('RGBA',g.size);od=ImageDraw.Draw(overlay)
        for xx in range(33):od.line((x+xx*scale,y,x+xx*scale,y+320),fill=(70,100,90,42),width=1)
        for yy in range(65):od.line((x,y+yy*scale,x+160,y+yy*scale),fill=(70,100,90,42),width=1)
        g=Image.alpha_composite(g.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(g)
        for yy in [0,10,20,30,40,50,60,64]:
            py=y+(64-yy)*scale;d.line((x,py,x+160,py),fill='#648b98');d.text((x-21,py-5),str(yy),font=font(9),fill=INK)
        d.line((x+80,y,x+80,y+320),fill='#d44d87')
        for xx in [0,16,32]:d.text((x+xx*scale-3,y+326),str(xx),font=font(10),fill=INK)
g.save(HERE/'core-walk-grid.png')

report={'task':'M1.C7','result':'pass','characterCount':12,'directionalWalkCycles':48,'critterCount':10,'animatedHabitatCount':3,'worldPropCount':3,'nativePNGCellsVerified':png_cells,'decodedNativeGIFCellsVerified':gif_cells,'frontIdlesUnchanged':True,'boyExistingFrontWalkUnchanged':True,'checks':checks,'limitations':['Original back/profile constructions require visual review; they are not reference-exact Emerald pose measurements.','Critter motion is stylized, not a biological gait measurement.','Gallery GIFs may share a reduced palette and normalized timing; individual native GIFs are verified exact.','Habitats are layered art demos with one featured species each; no care, gallon capacity or compatibility claim.','No runtime integration or deployment.']}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: 48 character walk cycles, 10 critters, 3 habitats. {png_cells:,} native PNG cells and {gif_cells:,} native GIF cells match exact editor sources.')
