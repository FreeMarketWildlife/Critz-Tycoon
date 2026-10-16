"""Independent saved-output checks. Writes only the exclusive OGH2 receipt."""
from pathlib import Path
from PIL import Image
import hashlib,json
R=Path(__file__).resolve().parents[3];S=Path(__file__).resolve().parent;O=R/'docs/reviews/M1-OGH2'
assert S==R/'art/source/overnight-girl-continuation-r1'
baseline=json.loads((O/'continuation-baseline.json').read_text());checks=[];facts={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(name,v):
    if not v:raise AssertionError(name)
    checks.append(name)
def rgba(data,palette):return [(0,0,0,0) if v==0 else tuple(bytes.fromhex(palette[v][1:]))+(255,) for v in data]
def mask(q):return {(x,y) for y in range(64) for x in range(32) if q.getpixel((x,y))[3]}
def connected(m):
    if not m:return False
    seen=set();todo=[next(iter(m))]
    while todo:
        p=todo.pop()
        if p in seen:continue
        seen.add(p);todo.extend(q for q in [(p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1)] if q in m-seen)
    return seen==m
for title,key in [('old owner files preserved','originalFiles'),('both archived histories preserved','historyFiles')]:
    ck(title,all((R/p).is_file() and sha(R/p)==h for p,h in baseline[key].items()))
# Board labels intentionally migrate, but every semantic image and actual native lineup stays byte exact.
semantic={p:h for p,h in baseline['candidatePNG'].items() if '/' in p or p=='four-idle-native.png'}
ck('every candidate semantic PNG and native lineup byte exact copied v2',all(sha(O/p)==h for p,h in semantic.items()))
checkpoint=json.loads((R/'local-review/overnight-continuation-checkpoint/manifest.json').read_text())
prior=[v for v in checkpoint['files'] if v['path'].startswith(('art/source/overnight-girl-r1/','docs/reviews/M1-OGH1/'))]
ck('old girl files still exact checkpoint',all(sha(R/v['path'])==v['sha256'] for v in prior))
for dr in ['south','north','west','east']:
    q=Image.open(O/dr/'idle.png').convert('RGBA');spec=json.loads((S/(dr+'.layers.json')).read_text());p=json.loads((S/(dr+'.sprite.json')).read_text());flat=json.loads((S/(dr+'.flat-construction.sprite.json')).read_text())
    ck(dr+' source explicit one native32x64 frame',q.size==(32,64) and spec['canvas']==[32,64] and p['width']==32 and p['height']==64 and len(p['frames'])==1)
    ck(dr+' JSON layer order matches actual order',spec['order']==[v['id'] for v in spec['layers']])
    comp=Image.new('RGBA',(32,64));layer_images={}
    for item in spec['layers']:
        layer=Image.new('RGBA',(32,64));layer.putdata(rgba(item['pixels'],spec['palette']));layer_images[item['id']]=layer
        ck(dr+' saved '+item['id']+' PNG equals semantic JSON',layer.tobytes()==Image.open(O/dr/(item['id']+'.png')).convert('RGBA').tobytes())
        comp.alpha_composite(layer)
    ck(dr+' complete ordered semantic source exactly recomposes',comp.tobytes()==q.tobytes())
    ck(dr+' editable painted frame exact composite',rgba(p['frames'][0]['pixels'],p['palette'])==list(q.get_flattened_data()))
    ck(dr+' editable flat project exact separate diagram',rgba(flat['frames'][0]['pixels'],flat['palette'])==list(Image.open(O/dr/'flat-construction.png').convert('RGBA').get_flattened_data()))
    ck(dr+' single connected whole character',connected(mask(q)))
    ck(dr+' no mixed-grid resampling or partial alpha',set(q.getchannel('A').get_flattened_data())=={0,255})
    ck(dr+' contact61 and empty62plus',max(y for x,y in mask(q))==61 and all(y<62 for x,y in mask(q)))
    shoe=layer_images['shoes'];ck(dr+' full near shoe connected',connected(mask(shoe)))
    ck(dr+' saved near shoe exact copied v2',sha(O/dr/'shoes.png')==baseline['candidatePNG'][dr+'/shoes.png'])
    facts[dr]={'pngSHA256':sha(O/dr/'idle.png'),'bounds':q.getbbox(),'frameEdgeAnchor':[16,64],'lastOpaqueRow':61,'nearShoeCells':len(mask(shoe))}
front=Image.open(O/'south/idle.png').convert('RGBA');gh=Image.open(R/'docs/reviews/M1-GH1/head-layer.png').convert('RGBA');rd=Image.open(R/'docs/reviews/M1-RD1/reference-derived-dummy.png').convert('RGBA')
ck('front GH1 visible head through44 exact RGBA',front.crop((0,0,32,45)).tobytes()==gh.crop((0,0,32,45)).tobytes())
ck('front full RD1 source-posed alpha45plus exact',front.getchannel('A').crop((0,45,32,64)).tobytes()==rd.getchannel('A').crop((0,45,32,64)).tobytes())
ck('front entire shoe envelope58plus exact RD1',front.getchannel('A').crop((0,58,32,64)).tobytes()==rd.getchannel('A').crop((0,58,32,64)).tobytes())
refs=json.loads((R/'docs/reviews/M1-OVQ1/reference-audit.json').read_text())
reference_facts=[]
for v in refs['files']:
    ck(v['name']+' actual reference bytes match pinned audit',sha(Path(v['path']))==v['sha256'])
    reference_facts.append({k:v[k] for k in ['name','path','revision','sha256']})
receipt={'task':'M1.OGH2','revision':'v2-preserved','state':'stable awaiting parent/root visual judgment','pass':True,'count':len(checks),'checks':checks,'facts':facts,'referenceFiles':reference_facts,'oldOwnerFilesGuarded':len(baseline['originalFiles']),'historyFilesGuarded':len(baseline['historyFiles']),'semanticPNGsGuarded':len(semantic),'copiedBoardSHA256':baseline['copiedBoardSHA256'],'boardSHA256':sha(O/'four-idle-board.png'),'boardPath':'docs/reviews/M1-OGH2/four-idle-board.png','labelChangeOnly':True,'appearanceAccepted':False,'walksAuthorized':False,'runtimeChanged':False,'sourceFreezeCommit':None}
(O/'continuation-checks.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['pass','count','oldOwnerFilesGuarded','historyFilesGuarded','semanticPNGsGuarded','boardSHA256']}))
