"""Read saved native files independently of build; freeze hashes after audit."""
from pathlib import Path
from PIL import Image
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[2];O=R/'docs/reviews/M1-ON1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[];details={}
def ck(name,v):
 assert v,name
 checks.append(name)
for dr in ['south','north','west','east']:
 src=json.loads((S/f'{dr}.layers.json').read_text());q=Image.open(O/f'{dr}-idle.png').convert('RGBA');re=Image.new('RGBA',(32,64));owners={}
 for n in src['renderOrder']:
  layer=Image.open(S/dr/f'{n}.png').convert('RGBA');cells=Image.new('RGBA',(32,64))
  for x,y,*color in src['layers'][n]['pixels']:cells.putpixel((x,y),tuple(color))
  ck(dr+'/'+n+' saved PNG equals sparse cells',layer.tobytes()==cells.tobytes())
  re.alpha_composite(layer)
  for i,p in enumerate(layer.get_flattened_data()):
   if p[3]:owners[(i%32,i//32)]=n
 ck(dr+' saved ordered PNG layers recompose export',re.tobytes()==q.tobytes())
 ck(dr+' saved native dimensions/binary alpha',q.size==(32,64) and set(q.getchannel('A').get_flattened_data())<={0,255})
 coords=set(owners);remaining=set(coords);components=[]
 while remaining:
  todo=[remaining.pop()];c=set(todo)
  while todo:
   x,y=todo.pop()
   for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in remaining:remaining.remove(p);c.add(p);todo.append(p)
  components.append(len(c))
 ck(dr+' entire visible sprite is one four-connected cluster',len(components)==1)
 if dr in ['west','east']:
  hand={p for p,n in owners.items() if n in ['hand','hand-light'] and q.getpixel(p)[:3] in [(210,155,104),(237,187,131)]}
  sleeve={p for p,n in owners.items() if n=='sleeve'}
  ck(dr+' visible warm hand connects directly to sleeve',any((x+dx,y+dy) in sleeve for x,y in hand for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]))
  ck(dr+' warm near arm descends at least four native rows',max(y for x,y in hand)-min(y for x,y in hand)>=3)
  details[dr]={'visibleWarmHandCells':len(hand),'visibleWarmHandBounds':[min(x for x,y in hand),min(y for x,y in hand),max(x for x,y in hand)+1,max(y for x,y in hand)+1],
               'visibleLayerCells':{n:sum(owner==n for owner in owners.values()) for n in ['coat','sleeve','hand','hand-light','trousers','near-shoe','far-shoe','shoe-highlight','glasses','eyes']},'contact61':[x for x,y in coords if y==61]}
 else:ck(dr+' PNG unchanged from rejected-v0 side-only correction',sha(O/f'{dr}-idle.png')==sha(O/'history-v0'/f'{dr}-idle.png'))
atlas=Image.open(O/'four-idle-native.png').convert('RGBA')
for i,dr in enumerate(['south','north','west','east']):ck(dr+' actual native atlas slot exact',atlas.crop((i*32,0,(i+1)*32,64)).tobytes()==Image.open(O/f'{dr}-idle.png').convert('RGBA').tobytes())
inputs=['art/source/reference-dummy-r1/construction.json','docs/reviews/M1-RD1/reference-derived-dummy.png','assets/review/idle-collection-v1/professor-nugget.png','art/source/idle-collection-v1/professor-nugget.sprite.json','local-review/overnight-cast-qa/prof_birch.png']
record={'task':'M1.ON1','revision':'v1 four idle freeze','pass':True,'count':len(checks),'checks':checks,'visibleOwnership':details,'sourceInputs':{p:sha(R/p) for p in inputs},'appearanceApproval':False,'walksAuthorized':False,'blocker':'None for saved-file integrity; actual root visual verdict pending'}
(S/'saved-file-audit.json').write_text(json.dumps(record,indent=2)+'\n')
files=[p for folder in [S,O] for p in folder.rglob('*') if p.is_file() and p.name!='freeze-manifest.json']
(S/'freeze-manifest.json').write_text(json.dumps({'task':'M1.ON1','revision':'v1 four idle freeze','state':'frozen awaiting root visual verdict','appearanceApproval':False,'walksAuthorized':False,'files':{str(p.relative_to(R)):sha(p) for p in sorted(files)}},indent=2)+'\n')
print(json.dumps({'pass':True,'checks':len(checks),'frozenFiles':len(files),'visibleOwnership':details}))
