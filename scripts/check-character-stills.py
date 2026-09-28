"""Independent verification of native still PNGs and exact atlas/lineup exports."""
from pathlib import Path
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parents[1]
out = root / 'assets/review/characters-v2'
review = root / 'docs/reviews/M1-C2'
manifest = json.loads((out/'atlas.json').read_text())
sheet = Image.open(out/'atlas.png').convert('RGBA')
checks, measurements = [], []

def check(name, passed):
    assert passed, name
    checks.append({'name': name, 'pass': True})

check('one still only; no animation metadata', manifest['animation'] is None and all(a['pose']=='idle' and a['direction']=='south' for a in manifest['assets']))
check('atlas dimensions agree with metadata', list(sheet.size)==manifest['size'])
check('12 unique native IDs for the confirmed cast', len(manifest['assets'])==len({a['id'] for a in manifest['assets']})==12)
occupancy = set()
silhouettes = set()
for a in manifest['assets']:
    native = Image.open(out/a['png']).convert('RGBA')
    name = a['label']
    x,y,w,h = a['rect']
    check(name+': native PNG equals atlas crop', native.size==(24,32) and native.tobytes()==sheet.crop((x,y,x+w,y+h)).tobytes())
    cells = {(xx,yy) for yy in range(y,y+h) for xx in range(x,x+w)}
    check(name+': frame in bounds without overlap', 0<=x<=sheet.width-w and 0<=y<=sheet.height-h and not occupancy.intersection(cells))
    occupancy.update(cells)
    pixels = list(native.get_flattened_data())
    check(name+': binary transparent PNG', {p[3] for p in pixels}=={0,255})
    bbox = native.getbbox()
    check(name+': measured budget and planted feet', list(bbox)==a['opaqueBBox'] and bbox[0]>=2 and bbox[1]>=5 and bbox[2]<=22 and bbox[3]==31 and a['anchor']==[12,32])
    colors = {p[:3] for p in pixels if p[3]}
    check(name+': color count and exact decoded hash', len(colors)==a['colorCount']<=15 and hashlib.sha256(native.tobytes()).hexdigest()==a['sha256'])
    mask={(xx,yy) for yy in range(32) for xx in range(24) if native.getpixel((xx,yy))[3]}
    visited={next(iter(mask))};stack=list(visited)
    while stack:
        xx,yy=stack.pop()
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                point=(xx+dx,yy+dy)
                if point in mask and point not in visited:visited.add(point);stack.append(point)
    check(name+': one connected silhouette', visited==mask)
    source=json.loads((root/a['source']).read_text())
    expected=[]
    for row in source['rows']:
        for k in row:
            value=source['palette'].get(k)
            expected.append(tuple(int(value[i:i+2],16) for i in (1,3,5))+(255,) if value else (0,0,0,0))
    check(name+': every exported pixel equals editable source', pixels==expected)
    silhouettes.add(native.getchannel('A').tobytes())
    measurements.append({'id':a['character'],'visible':a['visibleSize'],'colors':len(colors),'headHeight':a['design']['headHeight'],'bodyHeight':a['design']['bodyHeight'],'connected':True})
check('all12 drawings also have distinct silhouette masks', len(silhouettes)==12)
base=Image.open(review/'lineup-native.png').convert('RGBA')
for scale in (4,8):
    enlarged=Image.open(review/f'lineup-{scale}x.png').convert('RGBA')
    check(f'lineup {scale}× is exact nearest-neighbor enlargement', enlarged.tobytes()==base.resize((base.width*scale,base.height*scale),Image.Resampling.NEAREST).tobytes())
report={'passed':len(checks),'characterCount':len(measurements),'checks':checks,'measurements':measurements,'atlasSha256':hashlib.sha256((out/'atlas.png').read_bytes()).hexdigest()}
(review/'png-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(f"{len(checks)} decoded-PNG checks passed for{len(measurements)} stills.")
