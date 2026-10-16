"""Saved-file continuation guards; never rebuild or write another owner's files."""
from pathlib import Path
from PIL import Image
import hashlib, json

S = Path(__file__).resolve().parent
R = S.parents[2]
O = R / 'docs/reviews/M1-ON2'
assert S == R / 'art/source/overnight-nugget-continuation-r1'
checks = []
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name, value):
    assert value, name
    checks.append(name)

guard = json.loads((S/'continuation-guard.json').read_text())
for p, expected in guard['protectedFiles'].items():
    ck('old checkpoint unchanged: '+p, sha(R/p) == expected)
for p, expected in guard['copiedCurrentFiles'].items():
    if '/history-v0/' in p:
        ck('copied v0 unchanged: '+p, sha(R/p) == expected)

details = {}
for dr in ['south','north','west','east']:
    q = Image.open(O/f'{dr}-idle.png').convert('RGBA')
    old = Image.open(O/'history-v1'/f'{dr}-idle.png').convert('RGBA')
    ck(dr+' corrected v1 PNG bytes preserved', sha(O/f'{dr}-idle.png') == sha(O/'history-v1'/f'{dr}-idle.png'))
    ck(dr+' corrected v1 RGBA preserved', q.tobytes() == old.tobytes())
    ck(dr+' anchor padding remains two rows', q.getchannel('A').crop((0,62,32,64)).getbbox() is None and q.getbbox()[3] == 62)
    src = json.loads((S/f'{dr}.layers.json').read_text())
    prior = json.loads((S/'history-v1'/f'{dr}.layers.json').read_text())
    ck(dr+' semantic source unchanged', src == prior)
    ck(dr+' frame registration declared', src['frame'] == [32,64])
    if dr in ['west','east']:
        eye = Image.open(S/dr/'eyes.png').convert('RGBA')
        sites = [(x,y) for y in range(64) for x in range(32) if eye.getpixel((x,y))[3]]
        ck(dr+' two actual eye cells survive glasses compositing', len(sites)==2 and all(q.getpixel(p)==eye.getpixel(p) for p in sites))
        details[dr] = {'visibleEyeCells':sites, 'eyeRGBA':[list(q.getpixel(p)) for p in sites], 'bounds':q.getbbox()}

front = Image.open(O/'south-idle.png').convert('RGBA')
ref = Image.open(R/'docs/reviews/M1-RD1/reference-derived-dummy.png').convert('RGBA')
ck('full front shoe envelope58+ exact RD1', front.getchannel('A').crop((0,58,32,64)).tobytes()==ref.getchannel('A').crop((0,58,32,64)).tobytes())
ck('full front visible body46+ exact RD1', front.getchannel('A').crop((0,46,32,64)).tobytes()==ref.getchannel('A').crop((0,46,32,64)).tobytes())
manifest=json.loads((S/'manifest.json').read_text())
ck('current task metadata ON2',manifest['task']=='M1.ON2')
ck('shared anchor stays16,64',manifest['anchor']==[16,64])
for name in ['build.py','audit-freeze.py']:
    t=(S/name).read_text()
    ck(name+' active output path migrated', "O=R/'docs/reviews/M1-ON2'" in t and "O=R/'docs/reviews/M1-ON1'" not in t)

result={'task':'M1.ON2','pass':True,'count':len(checks),'checks':checks,'visibleEyeEvidence':details,'appearanceApproval':False,'walksAuthorized':False,'referenceLimit':'RD1 is front passing-frame visible volume only; original side/back construction remains proposed.'}
(S/'continuation-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':True,'checks':len(checks),'visibleEyeEvidence':details}))
