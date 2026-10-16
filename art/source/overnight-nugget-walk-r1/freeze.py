"""Freeze only the reviewed ON3 packet; refuse temporary reference imagery."""
from pathlib import Path
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[2];O=R/'docs/reviews/M1-ON3'
assert S==R/'art/source/overnight-nugget-walk-r1'
assert not list(S.glob('TEMP-*')),'Remove inspected temporary reference plates before freeze'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((S/'checks.json').read_text());assert audit['pass']
for dr,poses in audit['contactsAndBounds'].items():
    for pose,record in poses.items():assert sha(O/f'{dr}-{pose}.png')==record['sha256']
guard=json.loads((S/'input-guard.json').read_text())
assert all(sha(R/p)==h for p,h in guard['protectedON2'].items())
art={str(p.relative_to(R)):sha(p) for p in sorted(O.iterdir()) if p.is_file() and p.suffix in ['.png','.gif']}
(S/'artwork-lock.json').write_text(json.dumps({'task':'M1.ON3','revision':'v1 bounded far-foot correction','state':'frozen awaiting root/parent visual judgment','appearanceApproval':False,'files':art},indent=2)+'\n')
files={str(p.relative_to(R)):sha(p) for folder in [S,O] for p in sorted(folder.rglob('*')) if p.is_file() and p!=S/'freeze-manifest.json'}
(S/'freeze-manifest.json').write_text(json.dumps({'task':'M1.ON3','revision':'v1 bounded far-foot correction','state':'frozen for root/parent visual review','appearanceApproval':False,'runtimeIntegration':False,'files':files},indent=2)+'\n')
assert all(sha(R/p)==h for p,h in files.items())
print(json.dumps({'frozenFiles':len(files),'imageOutputs':len(art),'freezeSHA256':sha(S/'freeze-manifest.json'),'normalGIFSHA256':sha(O/'four-directions-normal.gif'),'slowGIFSHA256':sha(O/'four-directions-slow4x.gif'),'stripSHA256':sha(O/'all-phases-native-4x.png')}))
