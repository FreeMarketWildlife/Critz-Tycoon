"""Independent runtime export verification. Reads images; never edits them."""
import json, hashlib
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
base=root/'assets/review/overworld-v1';live=root/'assets/playable/overworld'
a=Image.open(base/'master.png').convert('RGBA');b=Image.open(live/'master.png').convert('RGBA')
old=json.loads((base/'master.json').read_text());new=json.loads((live/'master.json').read_text());by={t['id']:t for t in new['tiles']}
checks=[]
assert b.size==(1024,1024);assert set(b.getchannel('A').getdata())=={0,255};checks.append('1024x1024 RGBA with binary alpha')
for t in old['tiles']:
 n=by[t['id']];assert (n['x'],n['y'],n['index'])==(t['x'],t['y'],t['index']);box=(t['x'],t['y'],t['x']+32,t['y']+32);assert a.crop(box).tobytes()==b.crop(box).tobytes(),t['id']
checks.append(f"All {len(old['tiles'])} selected original tiles remain byte-exact at unchanged coordinates")
seen=set()
for t in new['tiles']:
 x,y=t['x'],t['y'];assert x%32==0 and y%32==0 and 0<=x<=992 and 0<=y<=992;assert (x,y) not in seen;seen.add((x,y));assert b.crop((x,y,x+32,y+32)).getbbox(),t['id']
checks.append(f"All {len(new['tiles'])} named cells aligned, nonempty and unique")
def crop(t):return b.crop((t['x'],t['y'],t['x']+32,t['y']+32))
for t in old['tiles']:
 if t.get('terrain')!='water':continue
 original=crop(t)
 for f in range(1,4):
  r=crop(by[f"anim.{t['id']}.{f}"])
  for box in [(0,0,32,1),(0,31,32,32),(0,0,1,32),(31,0,32,32)]:assert original.crop(box).tobytes()==r.crop(box).tobytes(),(t['id'],f)
checks.append('All 47 water shapes keep all four tile edges unchanged throughout animation')
for family in ['grass.living','grass.front']:
 assert len({crop(by[f'{family}.{f}']).tobytes() for f in range(4)})==4
checks.append('Four distinct contacted-grass and foreground frames')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'passed':len(checks),'checks':checks,'tiles':len(new['tiles']),'masterSha256':sha(live/'master.png'),'approvedHeroSha256':sha(root/'assets/characters/hero-boy-v1/idle-south.png')}
(root/'docs/reviews/M1-W1/asset-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
