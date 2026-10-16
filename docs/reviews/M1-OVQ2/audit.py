"""Read-only independent saved-pixel audit; writes only this review namespace."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageColor

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
checks=[]
def guard(name, value):
    checks.append({'name':name,'pass':bool(value)})
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for char, src, rev in [('girl','overnight-girl-continuation-r1','M1-OGH2'),('mom','overnight-mom-continuation-r1','M1-OM2'),('nugget','overnight-nugget-continuation-r1','M1-ON2')]:
    s=ROOT/'art/source'/src; r=ROOT/'docs/reviews'/rev
    for d in ['south','north','west','east']:
        jp=s/(d+'/layers.json' if char=='mom' else d+'.layers.json')
        o=json.loads(jp.read_text())
        target=r/(d+'/idle.png' if char=='girl' else 'idle-'+d+'.png' if char=='mom' else d+'-idle.png')
        final=Image.open(target).convert('RGBA'); comp=Image.new('RGBA',(32,64))
        order=o.get('order',o.get('renderOrder')); ls=o['layers']; counts={}
        for name in order:
            im=Image.new('RGBA',(32,64))
            if char=='girl':
                entry=next(x for x in ls if x['id']==name)
                for i,v in enumerate(entry['pixels']):
                    if v: im.putpixel((i%32,i//32),ImageColor.getrgb(o['palette'][v])+(255,))
                lp=r/d/(name+'.png')
            elif char=='mom':
                for x,y,c in ls[name]: im.putpixel((x,y),ImageColor.getrgb(c)+(255,))
                lp=s/d/(name+'.png')
            else:
                for x,y,*rgba in ls[name]['pixels']: im.putpixel((x,y),tuple(rgba))
                lp=s/d/(name+'.png')
            guard(f'{char}/{d}/{name} JSON equals saved PNG',im.tobytes()==Image.open(lp).convert('RGBA').tobytes())
            counts[name]=sum(a>0 for a in im.getchannel('A').getdata())
            comp=Image.alpha_composite(comp,im)
        guard(f'{char}/{d} exact composition',comp.tobytes()==final.tobytes())
        guard(f'{char}/{d} frame',final.size==(32,64))
        guard(f'{char}/{d} binary alpha',set(final.getchannel('A').getdata())<={0,255})
        mask={(x,y) for y in range(64) for x in range(32) if final.getpixel((x,y))[3]}
        seen=set(); stack=[next(iter(mask))]
        while stack:
            q=stack.pop()
            if q in seen: continue
            seen.add(q);x,y=q
            stack.extend(n for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if n in mask and n not in seen)
        guard(f'{char}/{d} single four-connected silhouette',seen==mask)
        guard(f'{char}/{d} contact61 and empty62+',max(y for x,y in mask)==61)
        if d=='south':
            old=ROOT/'docs/reviews'/({'girl':'M1-OGH1','mom':'M1-OM1','nugget':'M1-ON1'}[char])/'history-v0'/('south/idle.png' if char=='girl' else 'idle-south.png' if char=='mom' else 'south-idle.png')
            orig=Image.open(old).convert('RGBA')
            guard(f'{char} full front shoe alpha58+ retained',orig.getchannel('A').crop((0,58,32,64)).tobytes()==final.getchannel('A').crop((0,58,32,64)).tobytes())
        records.append({'character':char,'direction':d,'file':str(target.relative_to(ROOT)),'sha256':sha(target),'layersJson':str(jp.relative_to(ROOT)),'layersJsonSHA256':sha(jp),'bbox':final.getbbox(),'layerOccupiedCounts':counts,'contactXs':[x for x in range(32) if (x,61) in mask]})
refs=json.loads((ROOT/'docs/reviews/M1-OVQ1/reference-audit.json').read_text())['files']
refpins=[]
for f in refs:
    guard(f['name']+' actual reference SHA',sha(Path(f['path']))==f['sha256'])
    refpins.append({k:f[k] for k in ['name','revision','sha256']})
boards=[]
for p in ['M1-OGH2/four-idle-board.png','M1-OM2/idle-comparison.png','M1-ON2/four-idle-board.png']:
    p=ROOT/'docs/reviews'/p; boards.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p)})
report={'task':'M1.OVQ2','method':'Independent actual saved PNG/JSON decoding without running artist builders; source-only reference evidence, no emulator capture.','checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'poses':records,'boards':boards,'references':refpins,'appearanceAccepted':False,'walkingAuthorized':False}
(OUT/'saved-pixel-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'boards':boards},indent=2))
assert report['failed']==0
