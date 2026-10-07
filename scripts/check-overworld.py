"""Independent PNG / adjacency / assembly checks. Requires Pillow, never browser storage."""
from pathlib import Path
from PIL import Image
import hashlib, json, itertools

root=Path(__file__).resolve().parents[1]
out=root/'assets/review/overworld-v1'
review=root/'docs/reviews/M1-E2'
review.mkdir(parents=True,exist_ok=True)
manifest=json.loads((out/'master.json').read_text())
im=Image.open(out/'master.png').convert('RGBA')
palette=json.loads((out/'palette.json').read_text())
allowed={tuple(bytes.fromhex(c[1:]))+(255,) for ramp in palette.values() for c in ramp}|{(0,0,0,0)}
checks=[]
def check(name,condition):
    assert condition,name
    checks.append(name)
    print('PASS',name)
check('1024×1024 native atlas; binary alpha; declared palette only', im.size==(1024,1024) and set(im.getdata())<=allowed)
tiles=manifest['tiles']; by={t['id']:t for t in tiles}
check('Stable unique tile IDs and slots',len(by)==len(tiles)==len({t['index'] for t in tiles}))
check('All rectangles aligned; four valid 16×16 subtiles per 32×32 tile',all(t['x']%32==t['y']%32==0 and t['x']+32<=1024 and t['y']+32<=1024 and t['subtiles']==[{'x':t['x']+x,'y':t['y']+y} for y in [0,16] for x in [0,16]] for t in tiles))
def crop(id):
    t=by[id];return im.crop((t['x'],t['y'],t['x']+32,t['y']+32))
source=json.loads((root/'art/source/overworld-v1/pixels.json').read_text())
sp=[(0,0,0,0) if c=='#00000000' else tuple(bytes.fromhex(c[1:]))+(255,) for c in source['colors']]
check('Every exported tile matches editable source pixels exactly',all(list(crop(t['id']).getdata())==[sp[n] for row in t['rows'] for n in row] for t in source['tiles']))
check('Exact 2× nearest-neighbor atlas preview',Image.open(out/'master-2x.png').convert('RGBA').tobytes()==im.resize((2048,2048),Image.Resampling.NEAREST).tobytes())
check('Exact 3× native viewport enlargement',Image.open(out/'viewport-3x.png').tobytes()==Image.open(out/'viewport.png').resize((1440,960),Image.Resampling.NEAREST).tobytes())
def norm(m):
    for diagonal,a,b in [(16,1,2),(32,2,4),(64,4,8),(128,8,1)]:
        if not(m&a and m&b): m&=~diagonal
    return m
masks=sorted({norm(m) for m in range(256)})
check('Each of four terrain families contains all 47 normalized neighbor masks',len(masks)==47 and all(f'{kind}.{m}' in by for kind in ['path','water','paving','soil'] for m in masks))
dirs=[(0,-1,1),(1,0,2),(0,1,4),(-1,0,8),(1,-1,16),(1,1,32),(-1,1,64),(-1,-1,128)]
edgechecks=0
for vertical in [False,True]:
    w,h=(3,4) if vertical else (4,3)
    cells=list(itertools.product(range(w),range(h)))
    a=(1,1);b=(1,2) if vertical else (2,1)
    optional=[c for c in cells if c not in [a,b]]
    for bits in range(1<<len(optional)):
        occupied={a,b}|{c for i,c in enumerate(optional) if bits>>i&1}
        def mask(p):return norm(sum(bit for dx,dy,bit in dirs if (p[0]+dx,p[1]+dy) in occupied))
        ma,mb=mask(a),mask(b)
        for kind in ['path','water','paving','soil']:
            ia,ib=crop(f'{kind}.{ma}'),crop(f'{kind}.{mb}')
            ea=ia.crop((0,31,32,32) if vertical else (31,0,32,32))
            eb=ib.crop((0,0,32,1) if vertical else (0,0,1,32))
            assert ea.tobytes()==eb.tobytes(),(kind,vertical,ma,mb)
            edgechecks+=1
check(f'{edgechecks:,} exhaustive compatible terrain edge comparisons',True)
check('Fence and hedge connectivity inventories each include all 16 masks',all(f'{kind}.{m}' in by for kind in ['fence','hedge'] for m in range(16)))
check('Building / prop assemblies reference only existing atlas tiles',all(id in by for rows in manifest['assemblies'].values() for row in rows for id in row))
houses=[manifest['assemblies'][id] for id in ['house.cottage','house.garden','house.shop']]
check('5×5 / 7×5 buildings genuinely repeat roof centers and use split door tiles',all(len(house)==5 and len(house[0])==w and len(set(house[1][1:-1]))==1 and house[3][w//2]=='door.wood.closed.0.0' and house[4][w//2]=='door.wood.closed.0.1' for house,w in zip(houses,[5,5,7])))
for n in range(3):
    data=json.loads((out/f'map-{n}.json').read_text());r=Image.new('RGBA',(data['width']*32,data['height']*32))
    for layer in ['ground','decal','object','foreground']:
        check(f'Map {n} / {layer}: exact dimensions and no missing IDs',len(data['layers'][layer])==data['width']*data['height'] and all(id is None or id in by for id in data['layers'][layer]))
        for i,id in enumerate(data['layers'][layer]):
            if id:r.alpha_composite(crop(id),(i%data['width']*32,i//data['width']*32))
    check(f'Map {n} reproduced independently, pixel-for-pixel, from master PNG',r.tobytes()==Image.open(out/f'proof-{n}.png').convert('RGBA').tobytes())
town=Image.open(out/'proof-0.png').convert('RGBA');hero=Image.open(root/'assets/characters/hero-boy-v1/idle-south.png').convert('RGBA');town.alpha_composite(hero,(224,272))
check('Hero context uses exact approved V1 PNG, unmodified',town.tobytes()==Image.open(out/'town-with-hero.png').convert('RGBA').tobytes())
check('Native 480×320 cottage context is exact assembled crop',town.crop((96,64,576,384)).tobytes()==Image.open(out/'viewport.png').convert('RGBA').tobytes())
report={'passed':len(checks),'checks':checks,'terrainEdgeComparisons':edgechecks,'tiles':len(tiles),'actualOpaqueColors':len({p for p in im.getdata() if p[3]}),'binaryAlpha':True,'masterSHA256':hashlib.sha256((out/'master.png').read_bytes()).hexdigest(),'scope':'Independent raster checks, not visual approval or gameplay collision/animation validation.'}
(review/'pixel-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
