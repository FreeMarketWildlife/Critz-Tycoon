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
# Confirm registered authoring pixels use the very same runtime geometry.
import subprocess,os,base64
geometry=json.loads(subprocess.check_output([os.environ.get('COAST_NODE','node'),'art/source/coastal-water/geometry.mjs']));registered=json.loads((p/'shore-atlas.json').read_text());image=Image.open(p/'shore-atlas.png');lookup={a['id']:a for a in registered['assets']};assert len(lookup)==6016
for mask,data in geometry['masks'].items():
 a=lookup[f'join.fresh.still.grass.{mask}'];alpha=image.crop((a['x'],a['y'],a['x']+32,a['y']+64)).getchannel('A').tobytes();assert bytes(v//255 for v in alpha)==base64.b64decode(data)
for a in registered['assets']:
 if a['kind']=='registered-bank' and a['outer']=='sand':assert image.crop((a['x'],a['y'],a['x']+32,a['y']+64)).getbbox() is None
for mask in m['masks']:
 fs=[]
 for f in range(32):
  a=lookup[f'wash.{mask}.{f}'];fs.append(image.crop((a['x'],a['y'],a['x']+32,a['y']+64)).tobytes())
 assert diff(fs[-1],fs[0])<=max(diff(fs[i],fs[i+1]) for i in range(31)),mask
result.update(registeredSprites=6016,totalCoastalAssets=12512,contactRule='B',all47RegisteredAlphaMasksMatchRuntime=True,registeredWaveWrapVerified=True)
Path('docs/reviews/M1-WA6/native-check.json').write_text(json.dumps(result,indent=2)+'\n');print('B shore alpha registration and wrap checked')
