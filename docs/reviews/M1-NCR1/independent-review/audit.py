"""Independent saved NCR1 pixels/layers/preservation; imports no author builder."""
from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[4];O=Path(__file__).parent;A=O.parent;B=R/'docs/reviews/M1-H4R1';checks=[];facts={};inputs={};skin={(116,69,57,255),(166,104,69,255),(195,138,88,255)};ink=(36,35,48,255)
def ck(n,v):
 checks.append({'check':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
def im(p):
 if str(p).startswith(str(A)):inputs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
 return Image.open(p).convert('RGBA')
def same(a,b):return a.tobytes()==b.tobytes()
def edge(q):
 pts={(x,y) for y in range(q.height) for x in range(q.width) if q.getpixel((x,y))[3]};return {p for p in pts if any((p[0]+dx,p[1]+dy) not in pts for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)])}
def runs(q,y):
 out=[]
 for x in range(q.width):
  if q.getpixel((x,y))[3]:
   if out and out[-1][1]==x:out[-1][1]+=1
   else:out.append([x,x+1])
 return out
restore=json.loads((R/'art/source/shared-template-restoration-r1/restoration.json').read_text());meta=json.loads((R/'art/source/hero-directional-r14/construction.json').read_text());pack={};palette=set()
for dr in ['south','north','west','east']:
 for po in ['idle','A','P','C']:palette|=set(im(B/f'{dr}-{po}/master-hero.png').get_flattened_data())
for dr in ['south','north','west','east']:
 pack[dr]={}
 for po in ['idle','A','P','C']:
  tag=dr+'-'+po;p=A/tag;b=B/tag;h=im(p/'master-hero.png');d=im(p/'master-bald.png');oh=im(b/'master-hero.png');od=im(b/'master-bald.png');dy=-2 if po=='P' else 0;deltas={}
  for name,q,old in [('hero',h,oh),('bald',d,od)]:
   ck(tag+name+' full alpha/footprint',same(q.getchannel('A'),old.getchannel('A')));ck(tag+name+' existing shared palette',set(q.get_flattened_data())<=palette);ck(tag+name+' <=15 opaque colors',len({p for p in q.get_flattened_data() if p[3]})<=15);ck(tag+name+' exterior RGBA exact',all(q.getpixel(pt)==old.getpixel(pt) for pt in edge(old)));last=old.getbbox()[3]-1;ck(tag+name+' entire contact RGBA exact',same(q.crop((0,last,32,last+1)),old.crop((0,last,32,last+1))))
   changed=[(x,y) for y in range(64) for x in range(32) if q.getpixel((x,y))!=old.getpixel((x,y))];deltas[name]=changed
   ck(tag+name+' only authorized shoe/nape regions',all(y>=58 or (dr=='north' and name=='hero' and 42+dy<=y<=44+dy and old.getpixel((x,y)) in skin) for x,y in changed))
   if dr=='south':ck(tag+name+' protected front file bytes exact',(p/('master-'+name+'.png')).read_bytes()==(b/('master-'+name+'.png')).read_bytes())
  ck(tag+' master upper bald exact',same(d.crop((0,0,32,58)),od.crop((0,0,32,58))));q=d.copy()
  for pt in restore['poses'][dr][po]['hairHiddenScalpCutoutCells']:q.putpixel(tuple(pt),(0,0,0,0))
  q.alpha_composite(im(p/'master-hair-shadow.png'));q.alpha_composite(im(p/'master-hair.png'));ck(tag+' master real separate hair exact recomposition',same(q,h))
  nh=im(p/'native-hero.png');nd=im(p/'native-bald.png');q=nd.copy();cut=im(p/'native-scalp-cutout.png')
  for y in range(32):
   for x in range(16):
    if cut.getpixel((x,y))[3]:q.putpixel((x,y),(0,0,0,0))
  q.alpha_composite(im(p/'native-hair-shadow.png'));q.alpha_composite(im(p/'native-hair.png'));ck(tag+' native actual separate hair recomposition',same(q,nh));headend=23-int(po=='P');ck(tag+' native body common',same(nh.crop((0,headend,16,32)),nd.crop((0,headend,16,32))));ck(tag+' native dimensions',nh.size==nd.size==(16,32));ck(tag+' native binary alpha',set(nh.getchannel('A').get_flattened_data())<={0,255});ck(tag+' native palette source family',set(nh.get_flattened_data())<=palette and set(nd.get_flattened_data())<=palette);ck(tag+' native <=15 opaque colors',len({p for p in nh.get_flattened_data() if p[3]})<=15)
  for name,q in [('hero',nh),('bald',nd)]:ck(tag+name+' native lower silhouette preserved',same(q.getchannel('A').crop((0,23,16,32)),im(b/('native-'+name+'.png')).getchannel('A').crop((0,23,16,32))))
  eyes=meta['directions'][dr][po]['commonFeatureRegistration']['eyes']['cells'];sites=sorted({(x//2,y//2) for x,y in eyes});ck(tag+' actual registered bald eyes readable',all(nd.getpixel(pt)==ink for pt in sites))
  if dr in ['south','north']:ck(tag+' outlined ear extremities',all(nd.getpixel((x,19-int(po=='P')))==ink for x in [2,13]))
  my=h.getbbox()[3]-1;ny=nh.getbbox()[3]-1;mr=runs(h,my);nr=runs(nh,ny);ck(tag+' contact row half',ny==my//2);ck(tag+' contact run widths half',len(mr)==len(nr) and all(b-a==2*(d-c) for (a,b),(c,d) in zip(mr,nr)));ck(tag+' contact edge rounding <=1',all(abs(2*c-a)<=1 and abs(2*d-b)<=1 for (a,b),(c,d) in zip(mr,nr)))
  pm=im(p/'native-observed-pack.png');norm=Image.new('RGBA',(16,32));norm.paste(pm,(0,-dy//2));pack[dr][po]=norm
  facts[tag]={'masterHeroChangedSites':deltas['hero'],'masterBaldChangedSites':deltas['bald'],'nativeContact':nr,'masterContact':mr,'nativeEyeSites':sites,'nativeBaldBounds':nd.getbbox()}
 for po,pm in pack[dr].items():ck(dr+po+' native observed pack exact normalized',same(pm,pack[dr]['idle']))
for po in ['idle','A','P','C']:
 for size,y in [('master',54),('native',26 if po=='P' else 27)]:
  for typ in ['hero','bald']:
   w=im(A/f'west-{po}/{size}-{typ}.png');e=im(A/f'east-{po}/{size}-{typ}.png');ck(po+size+typ+' intended lower mirror',same(w.transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,y,w.width,w.height)),e.crop((0,y,e.width,e.height))))
# Old source/history and actual committed baseline are independent of candidate.
for row in json.loads((O/'h4r1-history-before.json').read_text())['files']:ck('history '+row['path'],hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256'])
for dr in ['south','north','west','east']:
 for po in ['idle','A','P','C']:
  for name in ['master-hero.png','master-bald.png','native-hero.png','native-bald.png']:
   path=f'docs/reviews/M1-H4R1/{dr}-{po}/{name}';ck('before pinned '+path,subprocess.check_output(['git','show','2c8fa4f:'+path])==(R/path).read_bytes())
ck('creator no diff',not subprocess.check_output(['git','diff','115cac8','--','character-creator']))
(O/'saved-audit.json').write_text(json.dumps({'beforeSHA':'2c8fa4fef4c6872b05fce294a82b09f873876a6e','checks':checks,'passed':len(checks),'facts':facts,'candidateInputHashes':inputs,'qualityApproval':False},indent=2)+'\n');print(json.dumps({'passed':len(checks),'candidateFilesHashed':len(inputs)}))
