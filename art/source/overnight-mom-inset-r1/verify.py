"""Independent saved-file checks for OM1; does not import/run the builder."""
from pathlib import Path
import json,hashlib
from collections import deque
from PIL import Image

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=ROOT/'docs/reviews/M1-OM3'
results={};passed=[]
def check(name,value):
 assert value,name
 passed.append(name)
def rgba(path):return Image.open(path).convert('RGBA')
def bounds(cells):
 if not cells:return None
 return [min(x for x,y in cells),min(y for x,y in cells),max(x for x,y in cells)+1,max(y for x,y in cells)+1]
for path,digest in json.loads((HERE/'input-hashes.json').read_text()).items():check('input preserved '+path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest)
for direction in ['south','north','west','east']:
 folder=HERE/direction;im=rgba(OUT/f'idle-{direction}.png');src=json.loads((folder/'layers.json').read_text());project=json.loads((folder/'idle.sprite.json').read_text())
 check(direction+' dimensions',im.size==(32,64));check(direction+' binary alpha',set(im.getchannel('A').get_flattened_data())=={0,255})
 check(direction+' two transparent bottom rows',im.getchannel('A').crop((0,62,32,64)).getbbox() is None)
 check(direction+' complete contact row',im.getchannel('A').crop((0,61,32,62)).getbbox() is not None)
 recompose=Image.new('RGBA',(32,64));visible={};owner={}
 for name in src['order']:
  layer=rgba(folder/f'{name}.png');fromJSON=Image.new('RGBA',(32,64))
  for x,y,c in src['layers'][name]:fromJSON.putpixel((x,y),tuple(bytes.fromhex(c[1:]))+(255,))
  check(direction+' layer JSON '+name,layer.tobytes()==fromJSON.tobytes());recompose.alpha_composite(layer)
  for y in range(64):
   for x in range(32):
    if layer.getpixel((x,y))[3]:owner[(x,y)]=name
 check(direction+' layer recomposition',recompose.tobytes()==im.tobytes())
 indexed=Image.new('RGBA',(32,64));indexed.putdata([(0,0,0,0) if not v else tuple(bytes.fromhex(project['palette'][v][1:]))+(255,) for v in project['frames'][0]['pixels']])
 check(direction+' sprite project exact',indexed.tobytes()==im.tobytes())
 six=rgba(OUT/f'idle-{direction}-6x.png');check(direction+' exact nearest enlargement',six.tobytes()==im.resize((192,384),Image.Resampling.NEAREST).tobytes())
 alpha={(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]};q=deque([next(iter(alpha))]);seen=set(q)
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if p in alpha and p not in seen:seen.add(p);q.append(p)
 check(direction+' one connected silhouette',seen==alpha)
 for name in ['hands','near-arm','torso','feet','legs']:
  cells=[(x,y) for x,y,c in src['layers'][name] if owner.get((x,y))==name]
  warm=[(x,y) for x,y,c in src['layers'][name] if c in ['#a87038','#784820'] and owner.get((x,y))==name]
  visible[name]={'visibleCells':len(cells),'bounds':bounds(cells),'warmCells':len(warm),'warmBounds':bounds(warm)}
 rows={str(y):[x for x in range(32) if im.getpixel((x,y))[3]] for y in range(55,62)}
 old=rgba(OUT/'history-v0'/f'idle-{direction}.png')
 if direction in ['south','north']:check(direction+' full front shoes preserved',old.crop((0,58,32,64)).tobytes()==im.crop((0,58,32,64)).tobytes())
 results[direction]={'sha256':hashlib.sha256((OUT/f'idle-{direction}.png').read_bytes()).hexdigest(),'bounds':im.getbbox(),'visibleParts':visible,'visibleOwnershipMethod':'last nontransparent layer in declared render order, including same-color occlusion','lowerRows':rows,'alphaReflectionMismatches':sum(((31-x,y) in alpha)!=((x,y) in alpha) for y in range(64) for x in range(16))}
board=OUT/'idle-comparison.png'
report={'checksPassed':len(passed),'checks':passed,'directions':results,'boardSHA256':hashlib.sha256(board.read_bytes()).hexdigest(),'appearanceApproval':False,'scope':'four idle candidates only; walking not authored; runtime unchanged'}
(HERE/'saved-file-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checksPassed':len(passed),'boardSHA256':report['boardSHA256'],'hands':{n:v['visibleParts']['hands'] for n,v in results.items()}},indent=2))
