from pathlib import Path
from PIL import Image,ImageDraw
import json
out=Path(__file__).parent;trace=Path('/tmp/ds5-browser-trace');expected={};seen={};samples=[]
for speed in ['normal','slow']:
    for dr in ['west','east']:
        key=dr+'-'+speed;gif=Image.open(out/f'paired-{dr}-{speed}-INTERNAL.gif');frames=[]
        for i in range(gif.n_frames):gif.seek(i);frames.append(gif.convert('RGB').tobytes())
        expected[key]=frames;seen[key]={}
for path in sorted(trace.glob('capture-*.png'),key=lambda p:int(p.stem.split('-')[1])):
    im=Image.open(path).convert('RGB');row={}
    for speed,y in [('normal',0),('slow',192)]:
        for dr,x in [('west',0),('east',352)]:
            key=dr+'-'+speed;q=im.crop((x,y,x+352,y+192));blob=q.tobytes()
            assert blob in expected[key],(path,key)
            slot=expected[key].index(blob);seen[key].setdefault(slot,q);row[key]=slot+1
    samples.append({'capture':path.name,'slots':row})
assert all(len(v)==8 for v in seen.values()),{k:len(v) for k,v in seen.items()}
plate=Image.new('RGB',(704,8*192),'#eee8d1')
for i in range(8):
    for col,dr in enumerate(['west','east']):plate.paste(seen[dr+'-slow'][i],(352*col,192*i))
plate.save(out/'actual-browser-side-eight-slots.png')
(out/'browser-playback.json').write_text(json.dumps({'pass':True,'snapshots':len(samples),'imageMatches':len(samples)*4,'allEightSlotsEveryPanel':True,'scope':'Fresh isolated art-only Chrome page; visual sequence inspection, not uninterrupted human watch','samples':samples},indent=2)+'\n')
print(json.dumps({'snapshots':len(samples),'matches':len(samples)*4,'slotsPerPanel':8}))
