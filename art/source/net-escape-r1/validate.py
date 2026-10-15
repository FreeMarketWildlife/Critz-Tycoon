from pathlib import Path
from PIL import Image
import hashlib,json
root=Path(__file__).resolve().parents[3];out=root/'assets/review/net-escape-r1';meta=json.loads((out/'manifest.json').read_text());checks=[]
def check(name,value):
 assert value,name
 checks.append(name)
for name,info in meta['files'].items():
 p=out/name;im=Image.open(p).convert('RGBA');check(name+' native frame',list(im.size)==info['size']);check(name+' hash',hashlib.sha256(p.read_bytes()).hexdigest()==info['sha256']);check(name+' binary alpha',set(im.getchannel('A').get_flattened_data())=={0,255})
for name,info in meta['preparedSources'].items():check(name+' exact original tool source',hashlib.sha256((root/info['source']).read_bytes()).hexdigest()==info['sha256'])
check('original beetle preserved',hashlib.sha256((root/'assets/review/living-collection-v1/stag-beetle/frame-0.png').read_bytes()).hexdigest()==meta['sourceBeetleSHA256'])
report={'task':'M1.NET3','checksPassed':len(checks),'checks':checks,'visualApproval':False};(root/'docs/reviews/M1-NET3/native-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(checks),'saved native asset checks')
