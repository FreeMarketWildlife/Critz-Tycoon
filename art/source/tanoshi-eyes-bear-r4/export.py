"""Register and palette-encode imagegen pixels; never draw eye geometry."""
from pathlib import Path
from PIL import Image
from collections import deque
import json, hashlib

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'art/source/tanoshi-eyes-bear-r4'
DEST=ROOT/'assets/review/tanoshi-eyes-bear-r4'
REVIEW=ROOT/'docs/reviews/M1-TN4'
DEST.mkdir(parents=True,exist_ok=True)
INPUTS=json.loads((SOURCE/'inputs.json').read_text())
RECTS=json.loads((SOURCE/'face-edit-rectangles.json').read_text())
IDS=['blush','mint','apricot','tiny-blush','small-mint','large-lilac']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def empty_regions(im):
    w,h=im.size;todo={(x,y) for y in range(h) for x in range(w) if not im.getpixel((x,y))[3]}
    outside=set();holes=[]
    while todo:
        q=deque([todo.pop()]);region=set()
        while q:
            x,y=q.popleft();region.add((x,y))
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    p=(x+dx,y+dy)
                    if p in todo:todo.remove(p);q.append(p)
        if any(x in [0,w-1] or y in [0,h-1] for x,y in region):outside|=region
        else:holes.append(region)
    return outside,holes

images={};reports=[];atlas=Image.new('RGBA',(192,32));entries=[]
for name in [*IDS,'bear']:
    info=INPUTS[name];original=Image.open(ROOT/info['source']).convert('RGBA')
    family='tanoshi' if name in ['blush','mint','apricot'] else 'tanoshi-sizes'
    indexed=json.loads((ROOT/f'art/source/{family}/{name}.pixels.json').read_text())
    palette=[(0,0,0,0),*[tuple(bytes.fromhex(c[1:]))+(255,) for c in indexed['palette'][1:]]]
    raw_path=SOURCE/f'generated-{name}.png';raw=Image.open(raw_path).convert('RGBA')
    crop=raw.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
    x0,y0,x1,y1=original.getbbox();target=(x1-x0,y1-y0)
    if name=='bear':
        scale=min(64/(crop[2]-crop[0]),36/(crop[3]-crop[1]))
        target=(round((crop[2]-crop[0])*scale),round((crop[3]-crop[1])*scale))
        x0=16+(64-target[0])//2;y0=80-target[1]
    sampled=raw.crop(crop).resize(target,Image.Resampling.NEAREST)
    guide=Image.new('RGBA',original.size);guide.paste(sampled,(x0,y0))
    if name=='bear':
        native=Image.new('RGBA',original.size);allowed={(x,y) for y in range(y0,y0+target[1]) for x in range(x0,x0+target[0])}
    else:
        native=original.copy();outside,old_holes=empty_regions(original)
        # Original outside/background and contour cells stay fixed. This mask
        # protects geometry; empty eye proposals come only from raw alpha.
        boundary={(x,y) for y in range(32) for x in range(32) if original.getpixel((x,y))[3] and any((x+dx,y+dy) in outside for dx in [-1,0,1] for dy in [-1,0,1])}
        a,b,c,d=RECTS[name];allowed={(x,y) for y in range(b,d) for x in range(a,c) if (x,y) not in outside and (x,y) not in boundary}
    for x,y in allowed:
        p=guide.getpixel((x,y))
        k=0 if p[3]<128 else min(range(1,len(palette)),key=lambda i:sum((a-b)**2 for a,b in zip(p[:3],palette[i][:3])))
        native.putpixel((x,y),palette[k])
    outside,holes=empty_regions(native)
    eye_holes=[r for r in holes if min(y for x,y in r)<24] if name!='bear' else []
    hole_info=[{'cells':len(r),'bounds':[min(x for x,y in r),min(y for x,y in r),max(x for x,y in r)+1,max(y for x,y in r)+1]} for r in eye_holes]
    changed=[[x,y] for y in range(native.height) for x in range(native.width) if native.getpixel((x,y))!=original.getpixel((x,y))]
    native.save(DEST/f'{name}.png');images[name]=native
    provenance={'id':name,'rawSource':str(raw_path.relative_to(ROOT)),'rawSHA256':sha(raw_path),'originalSHA256':sha(ROOT/info['source']),'cropAlphaThreshold':128,'rawCrop':list(crop),'nativeTargetSize':list(target),'nativeTargetPosition':[x0,y0],'sampling':'Pillow nearest, whole occupied crop registration; existing material palette','faceRectangle':RECTS.get(name),'allowedNativeCells':sorted([list(p) for p in allowed]),'alphaPolicy':'Generated alpha below128 only; no drawn or carved eye shapes. Original external background/contour and all outside-face pixels protected for Tanoshi. Bear uses generated alpha in aspect-preserved native envelope.','changedCells':changed,'paintedBounds':list(native.getbbox()),'eyeHoles':hole_info,'nativeSHA256':sha(DEST/f'{name}.png')}
    rows=[[palette.index(native.getpixel((x,y))) for x in range(native.width)] for y in range(native.height)]
    (SOURCE/f'{name}.pixels.json').write_text(json.dumps({'width':native.width,'height':native.height,'palette':indexed['palette'],'rows':rows,'provenance':provenance},indent=2)+'\n')
    reports.append(provenance)
    if name in IDS:
        i=IDS.index(name);atlas.paste(native,(i*32,0));entries.append({'id':name,'rect':[i*32,0,32,32],'anchor':[16,32],'sortAnchor':[16,32]})
atlas.save(DEST/'atlas.png')
(DEST/'atlas.json').write_text(json.dumps({'schemaVersion':1,'task':'M1.TN4','image':'atlas.png','size':[192,32],'appearanceStatus':'Unapproved review only; not active gameplay','assets':entries},indent=2)+'\n')
meta=json.loads((ROOT/'assets/playable/tanoshi-outline/bear.json').read_text());meta.update(task='M1.TN4',appearanceStatus='Unapproved review only; not active gameplay',provenance=reports[-1]);(DEST/'bear.json').write_text(json.dumps(meta,indent=2)+'\n')
(REVIEW/'export-checks.json').write_text(json.dumps({'task':'M1.TN4','assets':reports},indent=2)+'\n')
for label,color in [('light','#f4ebd9'),('dark','#29313f'),('world','#80b86b')]:
    plate=Image.new('RGBA',(128,32),color)
    for i,n in enumerate(['tiny-blush','small-mint','apricot','large-lilac']):plate.alpha_composite(images[n],(i*32,0))
    plate.resize((1024,256),Image.Resampling.NEAREST).save(REVIEW/f'after-eyes-{label}-8x.png')
atlas.resize((1536,256),Image.Resampling.NEAREST).save(REVIEW/'all-variants-8x.png')
bear=Image.new('RGBA',(192,96),'#f4ebd9');bear.alpha_composite(Image.open(ROOT/INPUTS['bear']['source']).convert('RGBA'),(0,0));bear.alpha_composite(images['bear'],(96,0));bear.resize((1536,768),Image.Resampling.NEAREST).save(REVIEW/'bear-before-after-8x.png')
print(json.dumps([{'id':r['id'],'bounds':r['paintedBounds'],'eyes':r['eyeHoles'],'changedCells':len(r['changedCells'])} for r in reports],indent=2))
