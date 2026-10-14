"""Inspect saved native exports independently of their imagegen export helper."""
from PIL import Image
from pathlib import Path
import hashlib, json

root=Path(__file__).resolve().parents[1]
atlas=Image.open(root/'assets/playable/tanoshi/atlas.png').convert('RGBA')
assert atlas.size==(96,32)
results=[]
for i,variant in enumerate(['blush','mint','apricot']):
    native=Image.open(root/f'assets/playable/tanoshi/{variant}.png').convert('RGBA')
    assert native.size==(32,32)
    assert native.tobytes()==atlas.crop((i*32,0,i*32+32,32)).tobytes()
    source=json.loads((root/f'art/source/tanoshi/{variant}.pixels.json').read_text())
    palette=[tuple(bytes.fromhex(c[1:]))+(255,) if len(c)==7 else (0,0,0,0) for c in source['palette']]
    assert list(native.getdata())==[palette[index] for row in source['rows'] for index in row]
    assert set(native.getchannel('A').getdata())=={0,255}
    assert all(native.getpixel((x,y))[3]==0 for y in [30,31] for x in range(32))
    # Find enclosed alpha-transparent components, proving real holes, not ink.
    empty={(x,y) for y in range(32) for x in range(32) if native.getpixel((x,y))[3]==0}
    holes=[]
    while empty:
        queue=[empty.pop()]
        for x,y in queue:
            for point in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if point in empty:empty.remove(point);queue.append(point)
        if all(0<x<31 and 0<y<31 for x,y in queue):
            holes.append([min(x for x,y in queue),min(y for x,y in queue),max(x for x,y in queue)+1,max(y for x,y in queue)+1,len(queue)])
    assert len(holes)==2,(variant,holes)
    assert all(12<=left<20 and 14<=top<18 for left,top,right,bottom,size in holes)
    results.append({'variant':variant,'holes':sorted(holes),'pngSourceAtlasExact':True,'binaryAlpha':True,'twoEmptyFootRows':True,'sha256':hashlib.sha256((root/f'assets/playable/tanoshi/{variant}.png').read_bytes()).hexdigest()})
assert Image.open(root/'docs/reviews/M1-TN1/clean-8x.png').tobytes()==atlas.resize((768,256),Image.Resampling.NEAREST).tobytes()
reference=json.loads((root/'references/tanoshi/manifest.json').read_text())
for entry in reference['files']:
    data=(root/'references/tanoshi'/entry['path']).read_bytes()
    assert len(data)==entry['size_bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
result={'task':'M1.TN1','nativeExports':results,'exact8x':True,'allSixOriginalReferencesUnchanged':True,'visualAcceptance':'pending user/parent checkpoint'}
(root/'docs/reviews/M1-TN1/native-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
