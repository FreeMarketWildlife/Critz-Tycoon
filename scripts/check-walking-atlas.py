#!/usr/bin/env python3
"""Independently decode all new walk frames and verify native sources/identity."""
from pathlib import Path
import json,hashlib,os
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
VERSION=os.environ.get('CRITZ_WALK_VERSION','v2')
assert VERSION in ['v2','v3']
FOLDER=ROOT/f'assets/review/characters-walk-{VERSION}'
REVIEW=ROOT/('docs/reviews/M1-I3' if VERSION=='v3' else 'docs/reviews/M1-C3')
meta=json.loads((FOLDER/'atlas.json').read_text());atlas=Image.open(FOLDER/'atlas.png').convert('RGBA');checks=[]
def check(condition,name):
    assert condition,name
    checks.append({'name':name,'pass':True})
check(len(meta['assets'])==144 and len(meta['characters'])==12,'12 characters, all 144 native frames')
check(len({a['id']for a in meta['assets']})==144,'stable unique asset IDs')
sources={c['id']:json.loads((ROOT/f'art/source/characters-walk-{VERSION}'/f"{c['id']}.json").read_text())for c in meta['characters']}
for a in meta['assets']:
    p=sources[a['character']];rows=p['frames'][a['direction']][a['pose']];x,y,w,h=a['rect'];native=atlas.crop((x,y,x+w,y+h));label=a['id']
    pixels=[(0,0,0,0)if k=='.'else tuple(bytes.fromhex(p['palette'][k][1:]))+(255,)for row in rows for k in row]
    check(list(native.get_flattened_data())==pixels,label+': decoded PNG equals source pixels')
    check(hashlib.sha256(native.tobytes()).hexdigest()==a['sha256'],label+': native hash')
    bbox=native.getbbox();check(list(bbox)==a['opaqueBBox'] and bbox[2]-bbox[0]<=20 and bbox[3]-bbox[1]<=26,label+': tight 20x26 bounds')
    check(a['anchor']==[12,32] and bbox[3]==(31 if a['pose']=='idle'else 32),label+': anchor and foot baseline')
    check(set(native.getchannel('A').get_flattened_data())=={0,255},label+': binary transparency')
    points={(xx,yy)for yy in range(32)for xx in range(24)if native.getpixel((xx,yy))[3]}
    reached={next(iter(points))};pending=list(reached)
    while pending:
        xx,yy=pending.pop()
        for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
            q=(xx+dx,yy+dy)
            if q in points and q not in reached:reached.add(q);pending.append(q)
    check(reached==points,label+': connected figure')
for c in meta['characters']:
    p=sources[c['id']];still=Image.open(ROOT/'assets/review/characters-v2/individual'/f"{c['id']}.png").convert('RGBA')
    entry=next(a for a in meta['assets']if a['id']==c['frames']['south']['idle']);x,y,_,_=entry['rect']
    if VERSION=='v2':check(atlas.crop((x,y,x+24,y+32)).tobytes()==still.tobytes(),c['id']+': exact original front idle')
    else:
        baseline=json.loads((ROOT/'art/source/characters-walk-v2'/f"{c['id']}.json").read_text())
        check(p['palette']==baseline['palette'],c['id']+': correction preserves palette')
    sheet=Image.open(FOLDER/c['sheet']).convert('RGBA');check(sheet.tobytes()==atlas.crop((0,y,288,y+32)).tobytes(),c['id']+': individual sheet equals atlas row')
    for direction in meta['directions']:
        poses=p['frames'][direction]
        check(len({''.join(rows)for rows in poses.values()})==3,c['id']+'.'+direction+': three distinct poses')
        shifted=['.'*24]+poses['idle'][:-1]
        check(poses['strideA']!=shifted and poses['strideB']!=shifted,c['id']+'.'+direction+': strides change anatomy, not only translation')
report={'passed':len(checks),'frameCount':144,'characterCount':12,'checks':checks}
(REVIEW/'png-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(f"{len(checks)} independent decoded-PNG checks passed.")
