from pathlib import Path
from PIL import Image
import json,hashlib
O=Path(__file__).parent;r=json.loads((O/'browser-raw.json').read_text());allowed=json.loads((O/'gif-frame-hashes.json').read_text());rows=[]
for row in r['samples']:
 im=Image.open(O/row['file']).convert('RGBA');sha=hashlib.sha256(im.tobytes()).hexdigest();assert sha in allowed,(row['file'],sha);rows.append({**row,'rgbaSHA256':sha,'poses':allowed[sha],'exactGifFrame':True})
for d in range(4):assert {x['poses'][d] for x in rows}=={'A','P','C'},(d,{x['poses'][d] for x in rows})
(O/'browser-checks.json').write_text(json.dumps({'exactActualPlaybackFrames':len(rows),'allFourDirectionsObservedPoses':['A','P','C'],'samples':rows,'errors':r['errors'],'storage':r['storage'],'qualification':'Actual animated GIF screenshot pixels, not canvas default-frame sampling; fresh isolated Chrome, sampled not uninterrupted human viewing. No physical-phone test.'},indent=2)+'\n');print('20 actual playback screenshots exact; A/P/C observed in all4directions')
