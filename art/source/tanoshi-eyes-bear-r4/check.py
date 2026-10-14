"""Independent checks of saved PNGs, transparent windows and preservation."""
from pathlib import Path
from PIL import Image
from collections import deque
import json,hashlib

ROOT=Path(__file__).resolve().parents[3];S=ROOT/'art/source/tanoshi-eyes-bear-r4';D=ROOT/'assets/review/tanoshi-eyes-bear-r4';R=ROOT/'docs/reviews/M1-TN4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs=json.loads((S/'inputs.json').read_text());checks=[]
def empty_groups(im):
    w,h=im.size;todo={(x,y) for y in range(h) for x in range(w) if im.getpixel((x,y))[3]==0};groups=[]
    while todo:
        q=deque([todo.pop()]);g=set()
        while q:
            x,y=q.popleft();g.add((x,y))
            for dy in [-1,0,1]:
                for dx in [-1,0,1]:
                    p=x+dx,y+dy
                    if p in todo:todo.remove(p);q.append(p)
        groups.append(g)
    outside=set().union(*(g for g in groups if any(x in [0,w-1] or y in [0,h-1] for x,y in g)))
    return outside,[g for g in groups if g.isdisjoint(outside)]

for name in ['blush','mint','apricot','tiny-blush','small-mint','large-lilac','bear']:
    original_path=ROOT/inputs[name]['source'];assert sha(original_path)==inputs[name]['sha256']
    old=Image.open(original_path).convert('RGBA');im=Image.open(D/f'{name}.png').convert('RGBA');data=json.loads((S/f'{name}.pixels.json').read_text());p=data['provenance']
    pal=[(0,0,0,0),*[tuple(bytes.fromhex(c[1:]))+(255,) for c in data['palette'][1:]]]
    assert im.tobytes()==bytes(c for row in data['rows'] for i in row for c in pal[i])
    assert set(im.getchannel('A').get_flattened_data())=={0,255}
    assert im.size==old.size
    used=set(c for c in im.get_flattened_data() if c[3]);assert used<=set(pal[1:]);assert len(used)<= (6 if name=='bear' else 3)
    changes={(x,y) for y in range(im.height) for x in range(im.width) if im.getpixel((x,y))!=old.getpixel((x,y))}
    # Regular Blush already has the clean tall pair and remains the exact
    # accepted master; active Blush uses the separate revised tiny frame.
    assert changes or name=='blush'
    if name!='bear':
        x0,y0,x1,y1=p['faceRectangle'];assert all(x0<=x<x1 and y0<=y<y1 for x,y in changes)
        assert changes<=set(map(tuple,p['allowedNativeCells']))
        old_out,_=empty_groups(old);new_out,gaps=empty_groups(im);assert old_out==new_out
        assert im.getbbox()==old.getbbox();assert not any(im.crop((0,30,32,32)).getchannel('A').get_flattened_data())
        for y in range(32):
            for x in range(32):
                if old.getpixel((x,y))[3] and any((x+dx,y+dy) in old_out for dx in [-1,0,1] for dy in [-1,0,1]):assert im.getpixel((x,y))==old.getpixel((x,y))
        eyes=sorted([g for g in gaps if min(y for x,y in g)<24],key=lambda g:min(x for x,y in g));assert len(eyes)==2
        height=2 if name in ['tiny-blush','apricot'] else 3
        bounds=[]
        for g in eyes:
            l,t=min(x for x,y in g),min(y for x,y in g);rr,bb=max(x for x,y in g)+1,max(y for x,y in g)+1
            assert rr-l==2 and bb-t==height and len(g)==2*height
            assert g=={(x,y) for y in range(t,bb) for x in range(l,rr)}
            bounds.append([l,t,rr,bb])
        assert bounds[0][1::2]==bounds[1][1::2]
        for y in range(bounds[0][1],bounds[0][3]):
            for x in range(bounds[0][2],bounds[1][0]):assert im.getpixel((x,y))[3]==255 and im.getpixel((x,y))!=pal[1]
        if name=='blush':
            raw_path=ROOT/p['rawSource'];assert sha(raw_path)==p['rawSHA256'];raw=Image.open(raw_path).convert('RGBA');sample=raw.crop(p['rawCrop']).resize(tuple(p['nativeTargetSize']),Image.Resampling.NEAREST);ox,oy=p['nativeTargetPosition']
            for x,y in changes:
                c=sample.getpixel((x-ox,y-oy));k=0 if c[3]<128 else min(range(1,len(pal)),key=lambda i:sum((a-b)**2 for a,b in zip(c[:3],pal[i][:3])))
                assert im.getpixel((x,y))==pal[k]
        else:
            master_path=ROOT/p['master'];assert sha(master_path)==p['masterSHA256'];assert sha(ROOT/p['masterRawSource'])==p['masterRawSHA256']
            master=Image.open(master_path).convert('RGBA');sp=[(0,0,0,0),*[tuple(bytes.fromhex(c[1:]))+(255,) for c in p['masterSourcePalette'][1:]]];px,py=p['placement']
            for x,y in changes:
                c=master.getpixel((x-px,y-py));k=0 if c[3]<128 else min(range(1,len(sp)),key=lambda i:sum((a-b)**2 for a,b in zip(c[:3],sp[i][:3])))
                assert im.getpixel((x,y))==pal[k],(name,x,y)
        checks.append({'id':name,'modifiedCells':len(changes),'pairedTransparentRectangles':bounds,'eyePixelsEach':2*height,'outsideFaceAndContourExact':True,'allChangedPixelsFromSavedGeneratedSampling':True,'frameBoundsAndEmptyRowsExact':True,'paletteColors':len(used),'sha256':sha(D/f'{name}.png')})
    else:
        l,t,rr,bb=im.getbbox();assert l>=16 and t>=44 and rr<=80 and bb==80
        assert not any(im.crop((0,0,96,16)).getchannel('A').get_flattened_data());assert not any(im.crop((0,80,96,96)).getchannel('A').get_flattened_data())
        old_meta=json.loads((ROOT/'assets/playable/tanoshi-outline/bear.json').read_text());meta=json.loads((D/'bear.json').read_text())
        for k in ['size','footprint','footprintCells','drawOffsetFromFootprintPixels','groundAnchor','sortAnchor','transparentRows','lowerContactX','contactRule']:assert old_meta[k]==meta[k],k
        raw_path=ROOT/p['rawSource'];assert sha(raw_path)==p['rawSHA256'];raw=Image.open(raw_path).convert('RGBA');sample=raw.crop(p['rawCrop']).resize(tuple(p['nativeTargetSize']),Image.Resampling.NEAREST);guide=Image.new('RGBA',(96,96));guide.paste(sample,tuple(p['nativeTargetPosition']))
        for y in range(96):
            for x in range(96):
                c=guide.getpixel((x,y));k=0 if c[3]<128 else min(range(1,len(pal)),key=lambda i:sum((a-b)**2 for a,b in zip(c[:3],pal[i][:3])));assert im.getpixel((x,y))==pal[k]
        checks.append({'id':name,'paintedBounds':[l,t,rr,bb],'paletteColors':len(used),'binaryAlpha':True,'generatedPixelSamplingExact':True,'footprintRegistrationExact':True,'sha256':sha(D/f'{name}.png')})

atlas=Image.open(D/'atlas.png').convert('RGBA');meta=json.loads((D/'atlas.json').read_text());assert atlas.size==(192,32)
for a in meta['assets']:
    x,y,w,h=a['rect'];assert atlas.crop((x,y,x+w,y+h)).tobytes()==Image.open(D/(a['id']+'.png')).convert('RGBA').tobytes();assert a['anchor']==a['sortAnchor']==[16,32]
protected=json.loads((R/'protected-starting-hashes.json').read_text())
for path,expected in protected.items():assert sha(ROOT/path)==expected,path
assert Image.open(S/'tall-face-master-native.png').convert('RGBA').tobytes()==Image.open(D/'blush.png').convert('RGBA').crop((12,14,20,19)).tobytes()
assert Image.open(S/'short-face-master-native.png').convert('RGBA').tobytes()==Image.open(S/'tall-face-master-native.png').convert('RGBA').resize((8,4),Image.Resampling.NEAREST).tobytes()
report={'task':'M1.TN4','assets':checks,'protectedFilesExact':len(protected),'heroOriginalPetAndLiveRuntimeExact':True,'noActiveGameplayReplacement':True,'appearanceApproved':False,'pairedEyeSourceMastersExact':True}
(R/'native-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'assets':len(checks),'protectedFilesExact':len(protected),'passed':True}))
