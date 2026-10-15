from PIL import Image,ImageDraw
from pathlib import Path
import json
r=Path('/Users/tanoshi/Documents/ChatGPT/Critz-Tycoon/docs/reviews/M1-DS4/independent-review');dirs=['south','north','west','east'];lookup={};examples={}
for dr in dirs:
 g=Image.open(r/f'paired-{dr}-normal-INTERNAL.gif');lookup[dr]={}
 for i in range(g.n_frames):g.seek(i);lookup[dr][g.convert('RGB').tobytes()]=i
seen={dr:set() for dr in dirs};unmatched=[]
for p in sorted(Path('/tmp/ds4-browser-trace').glob('capture-*.png')):
 im=Image.open(p).convert('RGB')
 for j,dr in enumerate(dirs):
  x=(j%2)*352;y=(j//2)*192;q=im.crop((x,y,x+352,y+192));i=lookup[dr].get(q.tobytes())
  if i is None:unmatched.append([p.name,dr])
  else:seen[dr].add(i);examples[(dr,i)]=q
assert not unmatched,unmatched[:3]
assert all(len(v)==8 for v in seen.values()),seen
plate=Image.new('RGB',(704,768),'#eee8d1')
for i in range(8):plate.paste(examples['west',i],((i%2)*352,(i//2)*192))
plate.save(r/'actual-browser-west-eight-slots.png');(r/'browser-playback.json').write_text(json.dumps({'snapshots':36,'matchedImages':144,'unmatched':unmatched,'normalSlotCoverage':{d:sorted(v) for d,v in seen.items()},'scope':'Actual fresh Chrome GIF playback samples cover every labelled slot in each direction; not an uninterrupted human-watch claim. No creator or player storage loaded.'},indent=2)+'\n');print({d:sorted(v) for d,v in seen.items()})
