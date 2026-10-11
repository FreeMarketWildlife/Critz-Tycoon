#!/usr/bin/env python3
"""Lossless PNG-frame assembly into labeled, centisecond-timed review GIFs."""
from pathlib import Path
import json, hashlib, os
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
VERSION=os.environ.get('CRITZ_WALK_VERSION','v2')
assert VERSION in ['v2','v3']
OUT=ROOT/f'assets/review/characters-walk-{VERSION}'
REVIEW=ROOT/('docs/reviews/M1-I3' if VERSION=='v3' else 'docs/reviews/M1-C3')
META=json.loads((OUT/'atlas.json').read_text())
ATLAS=Image.open(OUT/'atlas.png').convert('RGBA')
BG='#102a30';CARD='#1d3b42';BORDER='#315258';TEXT='#f0ead7';MUTED='#b3c8bd';GOLD='#dfbc70'
FONTS={size:ImageFont.load_default(size=size) for size in [11,12,13,14,15,18,24,27]}
DIRECTIONS=['south','west','north','east']; LABELS={'south':'Facing down','west':'Facing left','north':'Facing up','east':'Facing right'}
POSES=['strideA','idle','strideB','idle']
TICK_MS=1000*280896/16777216
HOLDS=[round((i+1)*8*TICK_MS/10)*10-round(i*8*TICK_MS/10)*10 for i in range(48)]
FRAMES={a['id']:ATLAS.crop((a['rect'][0],a['rect'][1],a['rect'][0]+24,a['rect'][1]+32)) for a in META['assets']}

def label(draw,x,y,text,size=14,color=TEXT,center=False):
    text=text.replace('’',"'").replace('×','x')
    font=FONTS[size]
    if center:x-=round(draw.textlength(text,font=font)/2)
    bounds=draw.textbbox((0,0),text or ' ',font=font)
    draw.text((x,y-bounds[1]),text,font=font,fill=color)

def make_palette():
    colors=[]
    for value in [BG,CARD,BORDER,TEXT,MUTED,GOLD]:
        rgb=tuple(bytes.fromhex(value[1:]));colors.append(rgb)
    for image in FRAMES.values():
        for color in image.get_flattened_data():
            if color[3] and color[:3] not in colors:colors.append(color[:3])
    assert len(colors)<=256,len(colors)
    p=Image.new('P',(1,1));p.putpalette([v for c in colors for v in c]+[0]*(768-len(colors)*3))
    return p,len(colors)

PALETTE,COLOR_COUNT=make_palette()
PALETTE_BYTES=PALETTE.getpalette()
COLOR_INDEX={tuple(PALETTE_BYTES[i*3:i*3+3]):i for i in range(COLOR_COUNT)}
def indexed(image):
    rgb=image.convert('RGB')
    # Direct RGB lookup avoids Pillow's approximate palette search cache.
    p=Image.frombytes('P',rgb.size,bytes(COLOR_INDEX[c] for c in rgb.get_flattened_data()))
    p.putpalette(PALETTE_BYTES)
    assert p.convert('RGB').tobytes()==rgb.tobytes(),'GIF changed source colors'
    return p

def draw_sprite(image,character,direction,pose,x,y,scale):
    frame=FRAMES[character['frames'][direction][pose]]
    image.alpha_composite(frame.resize((24*scale,32*scale),Image.Resampling.NEAREST),(x,y))

def overview(direction,pose):
    image=Image.new('RGBA',(720,768),BG);draw=ImageDraw.Draw(image);draw.fontmode='1'
    label(draw,24,22,'Critz: the cast in motion',27)
    label(draw,24,59,'12 chibi characters / 20x26 painted pixels / walking review',13,MUTED)
    label(draw,24,85,LABELS[direction],14,GOLD)
    for i,c in enumerate(META['characters']):
        x=24+(i%4)*172;y=116+(i//4)*204;center=x+78
        draw.rounded_rectangle((x,y,x+155,y+187),radius=10,fill=CARD,outline=BORDER)
        label(draw,center,y+11,c['label'],14,center=True)
        draw.line((x+22,y+160,x+134,y+160),fill=BORDER)
        draw_sprite(image,c,direction,pose,center-48,y+28,4)
        label(draw,center,y+169,'Walking / 4x',11,MUTED,True)
    label(draw,360,739,'Original native poses / 4 directions / awaiting visual review',12,MUTED,True)
    return indexed(image)

def individual(c,direction,pose):
    image=Image.new('RGBA',(240,288),BG);draw=ImageDraw.Draw(image);draw.fontmode='1'
    label(draw,120,18,c['label'],18,center=True)
    label(draw,120,46,LABELS[direction],12,GOLD,True)
    draw.line((48,260,192,260),fill=BORDER)
    draw_sprite(image,c,direction,pose,48,66,6)
    label(draw,120,270,'20x26 / exact 6x / walking review',11,MUTED,True)
    return indexed(image)

def save_gif(path,frames):
    frames[0].save(path,save_all=True,append_images=frames[1:],duration=HOLDS,loop=0,disposal=2,optimize=False)
    actual=Image.open(path);assert actual.n_frames==48,(path,actual.n_frames)
    duration=0
    for index,expected in enumerate(frames):
        actual.seek(index);duration+=actual.info['duration']
        assert actual.info['duration']==HOLDS[index],(path,index,'duration')
        assert actual.convert('RGB').tobytes()==expected.convert('RGB').tobytes(),(path,index,'pixels')
    assert actual.info.get('loop')==0
    return {'file':str(path.relative_to(ROOT)),'frames':48,'size':list(actual.size),'durationMs':duration,'expectedDurationMs':48*8*TICK_MS,'timingErrorMs':duration-48*8*TICK_MS,'allDecodedFramesExact':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
    (OUT/'gifs').mkdir(parents=True,exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
    timeline=[(DIRECTIONS[i//12],POSES[i%4])for i in range(48)]
    report=[]
    frames=[overview(d,p)for d,p in timeline]
    frames[0].convert('RGB').save(OUT/'all-characters-poster.png')
    report.append(save_gif(OUT/'all-characters.gif',frames))
    for c in META['characters']:report.append(save_gif(OUT/c['gif'],[individual(c,d,p)for d,p in timeline]))
    (REVIEW/'gif-validation.json').write_text(json.dumps({'gifCount':len(report),'decodedFramesChecked':48*len(report),'globalPaletteColors':COLOR_COUNT,'holdsMs':HOLDS,'timingNote':'GIF delays round cumulative 8-tick holds to 10ms; web review uses fixed ticks. No source colors are quantized.','gifs':report},indent=2)+'\n')
    print(f'{len(report)} GIFs exported; all {48*len(report)} decoded frames and timing holds match.')

if __name__=='__main__':main()
