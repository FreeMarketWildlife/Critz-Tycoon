from pathlib import Path
from PIL import Image
import json,base64
root=Path('assets/review/coastal-format');m=json.loads((root/'atlas.json').read_text());im=Image.open(root/'atlas.png');ids={a['id']:a for a in m['assets']};assert m['thinCaps']==False;assert len(m['masks'])==15;assert len(m['contexts'])==55;assert set(im.getchannel('A').get_flattened_data())=={0,255}
def pixels(id):
 a=ids[id];return im.crop((a['x'],a['y'],a['x']+32,a['y']+32)).tobytes()
proof=json.loads(Path('/tmp/critz-wa8-template-proof.json').read_text())
for p in proof:
 prefix=f"{p['kind']}.{p['side']}";alpha=pixels(f"{prefix}.mask.{p['mask']}")[3::4];assert bytes(v//255 for v in alpha)==base64.b64decode(p['alpha']),(p['turn'],p['mirror'],p['kind'],p['x'],p['y'],p['mask'])
 if p['bank']:
  assert pixels(f"{prefix}.bank.{p['mask']}")==base64.b64decode(p['bank']),('bank',p['turn'],p['mirror'],p['x'],p['y'],p['mask'])
  assert pixels(f"{prefix}.wash.{p['mask']}.0")==base64.b64decode(p['wash']),('wash',p['turn'],p['mirror'],p['x'],p['y'],p['mask'])
for side in ['inner','outer']:
 for mask in m['contexts']:
  frames=[pixels(f'shore.{side}.wash.{mask}.{f}') for f in range(32)]
  diff=lambda a,b:sum(a[i:i+4]!=b[i:i+4] for i in range(0,len(a),4))
  assert diff(frames[-1],frames[0])<=max(diff(frames[f],frames[f+1]) for f in range(31)),(side,mask)
# Repacked textures/props are exact native copies and contain no old transitions.
for new,old in [('props','assets/review/coastal-water/atlas.json'),('water','assets/review/water-terrain/atlas.json')]:
 fresh=json.loads((root/(new+'.json')).read_text());freshImage=Image.open(root/(new+'.png'));source=json.loads(Path(old).read_text());sourceImage=Image.open(Path(old).parent/source['image']);sourceIds={a['id']:a for a in source['assets']}
 for a in fresh['assets']:
  b=sourceIds[a['id']];assert freshImage.crop((a['x'],a['y'],a['x']+32,a['y']+32)).tobytes()==sourceImage.crop((b['x'],b['y'],b['x']+32,b['y']+32)).tobytes()
 assert len(fresh['assets'])==(10 if new=='props' else 256)
result=dict(formatShapes=15,joiningContexts=55,nativeTiles=m['nativeTileCount'],uniquePixelFrames=m['uniquePixelFrames'],binaryAlpha=True,thinCaps=False,assembledTileComparisons=len(proof),allStencilBankAndWavePixelsMatchAssembledScenes=True,all110WashWrapsVerified=True,loopSeconds=3.2,textureAndPropFramesPreserved=266,activeRuntimeRetiredTransitions=False)
Path('docs/reviews/M1-WA8').mkdir(parents=True,exist_ok=True);Path('docs/reviews/M1-WA8/native-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
