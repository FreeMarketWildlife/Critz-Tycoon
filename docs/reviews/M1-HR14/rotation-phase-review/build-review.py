"""Review composition only: existing HR14 pixels, no new character poses."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, subprocess

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).parent
SOURCE = ROOT / 'docs/reviews/M1-HR14'
DIRECTIONS = ['south', 'north', 'west', 'east']
ROTATION = ['south', 'west', 'north', 'east']
PHASES = ['A', 'A', 'P', 'P', 'C', 'C', 'P', 'P']
BG = (190, 212, 213)
inputs = {}

def read(kind, direction, phase):
    p = SOURCE / f'{kind}-{direction}-{phase}.png'
    inputs[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    im = Image.open(p).convert('RGBA')
    assert im.size == (32, 64)
    return im

def panel(images, columns):
    canvas = Image.new('RGB', (columns * 40, ((len(images) + columns - 1) // columns) * 72), BG)
    draw = ImageDraw.Draw(canvas)
    for i, im in enumerate(images):
        x, y = (i % columns) * 40 + 4, (i // columns) * 72
        canvas.paste(im, (x, y), im)
        # Marker is OUTSIDE the 32x64 source rectangle.
        draw.line((x, y+64, x+31, y+64), fill=(116,136,148))
        draw.line((x+14, y+64, x+18, y+64), fill=(216,79,91))
        draw.point((x+16, y+65), fill=(216,79,91))
        crop = canvas.crop((x,y,x+32,y+64)).convert('RGBA')
        expected = Image.new('RGBA',(32,64),BG+(255,))
        expected.alpha_composite(im)
        assert crop.tobytes() == expected.tobytes()
    return canvas

rot = [panel([read(k,d,'idle') for k in ('hero','dummy')],2) for d in ROTATION]
gait = [panel([read(k,d,p) for k in ('hero','dummy') for d in DIRECTIONS],4) for p in PHASES]
idle = panel([read(k,d,'idle') for k in ('hero','dummy') for d in DIRECTIONS],4)
contact = panel([read(k,d,p) for d in DIRECTIONS for k in ('hero','dummy') for p in ('A','P','C')],6)

def save_gif(name, frames, durations, scale):
    frames = [f.resize((f.width*scale,f.height*scale),Image.Resampling.NEAREST) for f in frames]
    colors = sorted(set().union(*(set(f.get_flattened_data()) for f in frames)))
    assert len(colors) <= 256
    lookup = {c:i for i,c in enumerate(colors)}
    palette = [v for c in colors for v in c] + [0] * (768-3*len(colors))
    indexed=[]
    for frame in frames:
        im=Image.new('P',frame.size); im.putpalette(palette)
        im.putdata([lookup[c] for c in frame.get_flattened_data()]); indexed.append(im)
    p=OUT/name
    indexed[0].save(p,save_all=True,append_images=indexed[1:],duration=durations,loop=0,optimize=False,disposal=2)
    # Pillow may coalesce duplicate holds. Check the exact visible schedule.
    decoded=Image.open(p); observed=[]
    for i in range(decoded.n_frames):
        decoded.seek(i); observed.append((decoded.convert('RGB').tobytes(),decoded.info['duration']))
    expected=[]
    for frame,duration in zip(frames,durations):
        b=frame.tobytes()
        if expected and expected[-1][0]==b: expected[-1]=(b,expected[-1][1]+duration)
        else: expected.append((b,duration))
    assert observed==expected and decoded.info.get('loop')==0
    return {'name':name,'dimensions':list(frames[0].size),'encoded_frames':decoded.n_frames,'loop_ms':sum(durations),'exact_visible_schedule':True}

exports=[]
for scale in (1,4):
    exports.append(save_gif(f'turn-in-place-{scale}x.gif',rot,[500]*4,scale))
    exports.append(save_gif(f'synchronized-PHASE-{scale}x.gif',gait,[100]*8,scale))
    exports.append(save_gif(f'synchronized-PHASE-SLOW-{scale}x.gif',gait,[400]*8,scale))
    idle.resize((idle.width*scale,idle.height*scale),Image.Resampling.NEAREST).save(OUT/f'idle-directions-{scale}x.png')
    contact.resize((contact.width*scale,contact.height*scale),Image.Resampling.NEAREST).save(OUT/f'unique-phase-contact-{scale}x.png')

source_commit=subprocess.check_output(['git','log','-1','--format=%H','--',*inputs],cwd=ROOT,text=True).strip()
for name in inputs:
    assert (ROOT/name).read_bytes()==subprocess.check_output(['git','show',source_commit+':'+name],cwd=ROOT)
report={'task':'HR14 existing-frame rotation/phase review','source_commit':source_commit,'previous_material_source':'c98a8cbd8d85e160e9080d6690964c3c3deb3ef1','input_frozen_check':'All32 PNGs exact to current source commit','rotation_order':ROTATION,'rotation_role_order':['hero','dummy'],'phase_direction_order':DIRECTIONS,'phase_role_rows':['hero','dummy'],'phase_order':PHASES,'phase_clock':'100ms per source slot; common phase comparison, NOT ROM native timing','slow_clock':'400ms per source slot; diagnosis only','source_pixels':'All source rectangles exact alpha-composited pixels; fixed32x64 frame/16,64 anchor; markers outside source rectangle','input_hashes':inputs,'exports':exports,'output_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.suffix in ('.png','.gif')}}
(OUT/'composition-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'Composed {len(inputs)} unchanged source PNGs; six exact GIF schedules and four nearest PNG plates.')
