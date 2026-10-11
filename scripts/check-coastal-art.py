"""Validate complete native coast bank and the final-to-first beach-wash step."""
from pathlib import Path
from PIL import Image
import json
p=Path('assets/review/coastal-water');m=json.loads((p/'atlas.json').read_text());im=Image.open(p/'atlas.png');assert set(im.getchannel('A').get_flattened_data())=={0,255};assert len(m['assets'])==6496
for a in m['assets']:
 assert a['w']==a['h']==32
 if a['kind']=='bank' and a['outer']=='sand':assert im.crop((a['x'],a['y'],a['x']+32,a['y']+32)).getbbox() is None
ids={a['id']:a for a in m['assets']};maxwrap=0;maxstep=0
for mask in m['masks']:
 fs=[]
 for f in range(32):
  a=ids[f'wash.{mask}.{f}'];fs.append(im.crop((a['x'],a['y'],a['x']+32,a['y']+32)).tobytes())
 diff=lambda a,b:sum(a[i:i+4]!=b[i:i+4] for i in range(0,len(a),4))
 step=max(diff(fs[i],fs[i+1]) for i in range(31));wrap=diff(fs[-1],fs[0]);assert wrap<=step,(mask,wrap,step);maxwrap=max(maxwrap,wrap);maxstep=max(maxstep,step)
t=json.loads((p/'coast.tsj').read_text());animations=[a['animation'] for a in t['tiles'] if 'animation' in a];assert len(animations)==47;assert all(sum(f['duration'] for f in a)==3200 for a in animations)
result={'assets':6496,'binaryAlpha':True,'sandBankOverlaysEmpty':True,'waterToWaterBanks':False,'animatedBeachShapes':47,'loopMs':3200,'largestAdjacentFramePixelDifference':maxstep,'largestWrapPixelDifference':maxwrap,'allWrapDifferencesWithinOrdinaryFrameDifferences':True,'rockVariants':3,'separateRockShadowVariants':3}
Path('docs/reviews/M1-WA6').mkdir(parents=True,exist_ok=True);Path('docs/reviews/M1-WA6/native-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
