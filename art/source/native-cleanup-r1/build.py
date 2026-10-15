"""NCR1 bounded family consistency + hand-authored native16. Review only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[3];SRC=Path(__file__).parent;OUT=ROOT/'docs/reviews/M1-NCR1';OUT.mkdir(exist_ok=True)
P={'_':(0,0,0,0),'o':(36,35,48,255),'n':(42,52,74,255),'b':(70,86,113,255),'g':(116,136,148,255),'d':(116,69,57,255),'s':(166,104,69,255),'S':(195,138,88,255),'v':(174,69,74,255),'r':(237,116,92,255),'R':(255,173,122,255),'c':(249,237,200,255),'C':(191,192,170,255),'h':(50,42,49,255),'m':(76,55,57,255),'l':(112,80,68,255)};skin={P[c] for c in 'dsS'};T={v:k for k,v in P.items()};frames={};records={};checks=[];inputs={};pin='2c8fa4fef4c6872b05fce294a82b09f873876a6e';maps=json.loads((SRC/'native-body-maps.json').read_text());meta=json.loads((ROOT/'art/source/hero-directional-r14/construction.json').read_text());f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
def ck(n,v):assert v,n;checks.append(n)
def load(path):
 q=ROOT/path;inputs[str(path)]=hashlib.sha256(q.read_bytes()).hexdigest();return Image.open(q).convert('RGBA')
def pts(q):return {(i%q.width,i//q.width) for i,p in enumerate(q.get_flattened_data()) if p[3]}
def save(q,p):q.save(p);return {'fileSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'rgbaSHA256':hashlib.sha256(q.tobytes()).hexdigest(),'bounds':q.getbbox()}
def exterior(q):
 occupied=pts(q)
 return {p for p in occupied if any((p[0]+dx,p[1]+dy) not in occupied for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)])}
def put(q,x,y,c):q.putpixel((x,y),P[c])
def footwear(q,dr,po):
 if dr=='south':return
 if dr=='east':
  w=q.transpose(Image.Transpose.FLIP_LEFT_RIGHT);footwear(w,'west',po);q.paste(w.transpose(Image.Transpose.FLIP_LEFT_RIGHT));return
 # Shoe material is within existing source lower footprint; never redraw legs.
 rows=range(58,61) if po in ['idle','P'] else range(59,63);edge=exterior(q)
 for y in rows:
  for x in range(32):
   if q.getpixel((x,y))[3] and (x,y) not in edge:put(q,x,y,'n')
 if dr=='west':
  if po in ['idle','P']:
   sites={(10,58):'v',(11,58):'b',(12,58):'C',(13,58):'C',(14,58):'b',(12,59):'C',(13,59):'C',(14,59):'b',(16,60):'b',(17,58):'b',(18,58):'b',(18,59):'b'};sites.update({(x,60):'c' for x in range(12,16)})
  elif po=='A':sites={(20,59):'C',(21,59):'C',(22,59):'b',(20,60):'b',(21,60):'C',(22,60):'v',(21,61):'b',(22,61):'b',(21,62):'c',(22,62):'c',(9,59):'b',(10,59):'b',(10,60):'C'}
  else:sites={(8,59):'b',(9,59):'C',(10,59):'C',(11,59):'b',(8,60):'b',(9,60):'v',(10,60):'C',(9,61):'b',(10,61):'b',(9,62):'c',(10,62):'c',(23,59):'b',(24,59):'b',(24,60):'C'}
 else:
  if po in ['idle','P']:
   sites={(9,58):'b',(10,58):'C',(11,58):'C',(12,58):'b',(10,59):'b',(11,59):'b',(13,59):'b'};sites.update({(x,60):'c' for x in range(9,13)});sites.update({(31-x,y):c for (x,y),c in list(sites.items())})
  elif po=='A':sites={(10,60):'v',(12,60):'C',(13,60):'C',(14,60):'b',(12,61):'b',(13,61):'b',(14,61):'b',(12,62):'c',(13,62):'c'}
  else:sites={(17,60):'b',(18,60):'C',(19,60):'C',(20,60):'b',(21,60):'v',(18,61):'b',(19,61):'b',(20,61):'b',(18,62):'c',(19,62):'c'}
 for (x,y),c in sites.items():
  ck(dr+po+str((x,y))+' footwear material inside existing silhouette',q.getpixel((x,y))[3] and (x,y) not in edge);put(q,x,y,c)
for dr in ['south','north','west','east']:
 frames[dr]={};records[dr]={}
 for po in ['idle','A','P','C']:
  tag=dr+'-'+po;folder=OUT/tag;folder.mkdir(exist_ok=True);base=Path('docs/reviews/M1-H4R1')/tag
  for name in ['master-hero.png','master-bald.png']:ck(tag+name+' pinned H4R1 source bytes',subprocess.check_output(['git','show',pin+':'+str(base/name)])==(ROOT/base/name).read_bytes())
  old=load(base/'master-hero.png');ob=load(base/'master-bald.png');q=old.copy();b=ob.copy();hair=load(base/'master-hair.png');shade=load(base/'master-hair-shadow.png');footwear(q,dr,po);footwear(b,dr,po)
  if dr=='north':
   dy=-2 if po=='P' else 0
   for y,xs in [(42,range(8,24)),(43,range(10,22))]:
    for x in xs:
     p=(x,y+dy);ck(tag+str(p)+' rear overlap replaces existing skin only',old.getpixel(p) in skin);hair.putpixel(p,P['h']);q.putpixel(p,P['h'])
   for x in range(11,22):
    p=(x,44+dy);ck(tag+str(p)+' short rear shadow source skin only',old.getpixel(p) in skin);shade.putpixel(p,P['d']);q.putpixel(p,P['d'])
  rec=b.copy();cutmeta=json.loads((ROOT/'art/source/shared-template-restoration-r1/restoration.json').read_text())['poses'][dr][po]['hairHiddenScalpCutoutCells']
  for p in cutmeta:rec.putpixel(tuple(p),P['_'])
  rec.alpha_composite(shade);rec.alpha_composite(hair);ck(tag+' master real separate hair/shadow exact recomposition',rec.tobytes()==q.tobytes());ck(tag+' master alpha/full footprint exact',q.getchannel('A').tobytes()==old.getchannel('A').tobytes() and b.getchannel('A').tobytes()==ob.getchannel('A').tobytes());last=old.getbbox()[3]-1;ck(tag+' master last contact RGBA exact',q.crop((0,last,32,last+1)).tobytes()==old.crop((0,last,32,last+1)).tobytes());ck(tag+' master exterior RGBA exact',all(q.getpixel(p)==old.getpixel(p) for p in exterior(old)));ck(tag+' master scalp/body upper exact bald',b.crop((0,0,32,58)).tobytes()==ob.crop((0,0,32,58)).tobytes())
  if dr=='south':ck(tag+' master front fully exact',q.tobytes()==old.tobytes() and b.tobytes()==ob.tobytes())
  elif dr!='north':ck(tag+' master all upper head/hands/pack exact',q.crop((0,0,32,58)).tobytes()==old.crop((0,0,32,58)).tobytes())
  else:ck(tag+' master collar/pack/hands exact',q.crop((0,45+(-2 if po=='P' else 0),32,58)).tobytes()==old.crop((0,45+(-2 if po=='P' else 0),32,58)).tobytes())
  # Authored native body maps: no sampling occurs in this builder.
  rows=maps[dr][po];ck(tag+' authored native dimensions',len(rows)==32 and all(len(r)==16 for r in rows));nb=Image.new('RGBA',(16,32));nb.putdata([P[c] for row in rows for c in row]);nh=nb.copy();nHair=load(base/'native-hair.png');oldshade=load(base/'native-hair-shadow.png');nShade=Image.new('RGBA',(16,32));nCut=load(base/'native-scalp-cutout.png');boundary=exterior(nb)
  for p in pts(oldshade):
   if nb.getpixel(p) in skin and oldshade.getpixel(p) in skin and p not in boundary:nShade.putpixel(p,oldshade.getpixel(p))
  if dr=='north':
   dy=-1 if po=='P' else 0
   for x in range(4,12):nHair.putpixel((x,21+dy),P['o' if x in [4,11] else 'h'])
   for x in range(6,10):nShade.putpixel((x,22+dy),P['d'])
  for p in pts(nCut):nh.putpixel(p,P['_'])
  nh.alpha_composite(nShade);nh.alpha_composite(nHair);re=nb.copy()
  for p in pts(nCut):re.putpixel(p,P['_'])
  re.alpha_composite(nShade);re.alpha_composite(nHair);ck(tag+' native separate hair exact recomposition',re.tobytes()==nh.tobytes());headend=23-int(po=='P');ck(tag+' native Hero/bald body exact below head',nh.crop((0,headend,16,32)).tobytes()==nb.crop((0,headend,16,32)).tobytes());ck(tag+' native contact matches master row',nh.getbbox()[3]-1==last//2)
  files={}
  for name,im in [('master-hero.png',q),('master-bald.png',b),('master-hair.png',hair),('master-hair-shadow.png',shade),('native-hero.png',nh),('native-bald.png',nb),('native-hair.png',nHair),('native-hair-shadow.png',nShade),('native-scalp-cutout.png',nCut),('native-recomposed-hero.png',re)]:files[name]=save(im,folder/name)
  delta=lambda a,b:[{'xy':[x,y],'from':T[a.getpixel((x,y))],'to':T[b.getpixel((x,y))]} for y in range(a.height) for x in range(a.width) if a.getpixel((x,y))!=b.getpixel((x,y))]
  records[dr][po]={'files':files,'masterHeroChanges':delta(old,q),'masterBaldChanges':delta(ob,b),'sourceTorsoAnchor':meta['directions'][dr][po]['torsoAnchor'],'sourceCanonicalTorsoLocalPackAnchor':meta['directions'][dr][po]['canonicalPackAnchor']};frames[dr][po]={'oldMaster':old,'oldNative':load(base/'native-hero.png'),'oldNativeBald':load(base/'native-bald.png'),'master':q,'masterBald':b,'native':nh,'nativeBald':nb}
# Review displays intentionally contain unscaled native thumbnails and exact integer zoom.
def plate(name,poses,columns):
 p=Image.new('RGB',(len(columns)*230,len(poses)*225),'#eee8d1');d=ImageDraw.Draw(p)
 for row,(dr,po) in enumerate(poses):
  for col,(key,title,scale) in enumerate(columns):
   q=frames[dr][po][key];x=230*col;y=225*row;d.text((x+4,y+4),dr+' '+po+' '+title,font=f,fill='#242330');im=q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST);p.paste(im,(x+10,y+25),im);p.paste(q,(x+155,y+105),q)
 p.save(OUT/name)
cols=[('oldNative','BEFORE HERO16',6),('oldNativeBald','BEFORE BALD16',6),('native','AFTER HERO16',6),('nativeBald','AFTER BALD16',6),('master','AFTER MASTER32',3)]
plate('four-direction-before-after.png',[(dr,'idle') for dr in frames],cols);plate('all-direction-poses.png',[(dr,po) for dr in frames for po in ['idle','A','P','C']],cols);plate('master-family-before-after.png',[(dr,'idle') for dr in frames],[('oldMaster','H4R1 MASTER',2),('master','NCR1 MASTER',2),('masterBald','SHARED BALD32',2)])
(SRC/'changes.json').write_text(json.dumps({'task':'M1.NCR1','inputs':inputs,'poses':records},indent=2)+'\n');(SRC/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False},indent=2)+'\n');print('PASS',len(checks),'initial master/material/native attachment guards; actual visual evaluation follows')
# Measured native grid/body, actual observed-pack corners and complete source
# preservation checks. These guards do not confer visual acceptance.
def runs(q,y):
 out=[]
 for x in range(q.width):
  if q.getpixel((x,y))[3]:
   if out and out[-1][1]==x:out[-1][1]+=1
   else:out.append([x,x+1])
 return out
quant={};pack={}
for dr in frames:
 quant[dr]={};pack[dr]={}
 for po,data in frames[dr].items():
  tag=dr+'-'+po;folder=OUT/tag;q=data['nativeBald'];mq=data['master'];nb=data['nativeBald'];nh=data['native'];dy=-1 if po=='P' else 0;last=mq.getbbox()[3]-1;mr=runs(mq,last);nr=runs(nh,last//2);ck(tag+' native last-contact same count/halfwidth',len(mr)==len(nr) and all(b-a==2*(d-c) for (a,b),(c,d) in zip(mr,nr)));offsets=[[2*c-a,2*d-b] for (a,b),(c,d) in zip(mr,nr)];ck(tag+' native contact rounding <=1 master pixel',all(abs(v)<=1 for pair in offsets for v in pair));ck(tag+' native contact RGBA/source width retained from H4R1',nh.crop((0,last//2,16,last//2+1)).tobytes()==data['oldNative'].crop((0,last//2,16,last//2+1)).tobytes());ck(tag+' native entire below-head body alpha preserved',nb.crop((0,23+dy,16,32)).getchannel('A').tobytes()==data['oldNativeBald'].crop((0,23+dy,16,32)).getchannel('A').tobytes());ck(tag+' native palette original family subset',set(nh.get_flattened_data())<=set(P.values()));ck(tag+' source master visible pack pixels exact',all(data['master'].getpixel((i%32,i//32))==data['oldMaster'].getpixel((i%32,i//32)) for i,on in enumerate(meta['directions'][dr][po]['visiblePackMask']) if on))
  ex=meta['directions'][dr][po]['commonFeatureRegistration'];ck(tag+' source master registered eyes ears hands exact',all(data['master'].getpixel(tuple(p))==data['oldMaster'].getpixel(tuple(p)) for k in ['eyes','ears','hands'] for p in ex[k]['cells']))
  if dr!='north':
   xs=[6,9] if dr=='south' else [5] if dr=='west' else [10]
   ck(tag+' native registered1x2eyes retained',all(nb.getpixel((x,y+dy))==P['o'] for x in xs for y in [19,20]))
  if dr in ['south','north']:
   ck(tag+' native ear outer rim dark',all(nb.getpixel((x,19+dy))==P['o'] for x in [2,13]));ck(tag+' native visible ear inner warm',all(nb.getpixel((x,19+dy)) in skin for x in [3,12]))
  origmask=load(Path('docs/reviews/M1-H4R1')/tag/'native-observed-pack.png');pm=Image.new('RGBA',(16,32))
  for p in pts(origmask):pm.putpixel(p,nh.getpixel(p))
  save(pm,folder/'native-observed-pack.png');normalized=Image.new('RGBA',(16,32));normalized.paste(pm,(0,-dy));pack[dr][po]={'normalized':normalized,'bounds':pm.getbbox()}
  quant[dr][po]={'masterLastContactRow':last,'nativeLastContactRow':last//2,'masterContactRuns':mr,'nativeContactRuns':nr,'contactEdgeOffsetsMasterPixels':offsets,'torsoAnchor32':meta['directions'][dr][po]['torsoAnchor'],'torsoAnchor16':[v//2 for v in meta['directions'][dr][po]['torsoAnchor']],'canonicalPackAnchor32':meta['directions'][dr][po]['canonicalPackAnchor'],'canonicalPackAnchor16':[8,24],'nativeSoleCompression':'short pale edge retained one native row above dark contact; some sole-material cells shift2master pixels relative to a literal inverse, explicitly authored for readability','notLosslessInverse':True}
for dr in ['south','north']:
 q=frames[dr]['idle']['nativeBald'];ck(dr+' native idle full bald silhouette symmetric',q.getchannel('A').tobytes()==q.transpose(Image.Transpose.FLIP_LEFT_RIGHT).getchannel('A').tobytes())
packjson={}
for dr in pack:
 packjson[dr]={};base=pack[dr]['idle']['normalized']
 for po,d in pack[dr].items():
  im=d['normalized'];different=[{'xy':[x,y],'idle':T[base.getpixel((x,y))],'pose':T[im.getpixel((x,y))]} for y in range(32) for x in range(16) if im.getpixel((x,y))!=base.getpixel((x,y))];packjson[dr][po]={'normalizedObservedDifference':different,'qualification':'observed coarse visibility/material mask, not complete reconstructed rigid native backpack'}
  ck(dr+po+' observed native pack no normalized color blink',not different)
# Existing authored source order and cadence, paired before/after appearances.
order=meta['order'];gifproof=[]
for dr in frames:
 hold=[100]*8 if dr=='south' else [70,60,70,70,70,60,70,70]
 for slow in [1,4]:
  images=[]
  for i,po in enumerate(order):
   p=Image.new('RGB',(1150,235),'#eee8d1');d=ImageDraw.Draw(p);d.fontmode='1';d.text((5,2),f'INTERNAL NCR1 {dr} source slot{i+1}/8 {po} existing holds x{slow}',font=f,fill='#242330')
   for col,(key,title,scale) in enumerate(cols):
    q=frames[dr][po][key];x=230*col;big=q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST);p.paste(big,(x+10,24),big);p.paste(q,(x+155,110),q);d.text((x+5,219),title,font=f,fill='#465671')
   images.append(p)
  filename=f'{dr}-paired-existing-walk-{"normal" if slow==1 else "slow"}.gif';duration=[v*slow for v in hold];images[0].save(OUT/filename,save_all=True,append_images=images[1:],duration=duration,loop=0,optimize=False,disposal=2);g=Image.open(OUT/filename);ck(filename+' actual8slots infinite loop',g.n_frames==8 and g.info.get('loop')==0)
  for i,p in enumerate(images):g.seek(i);ck(filename+str(i)+' decoded frame pixels and hold exact',g.convert('RGB').tobytes()==p.tobytes() and g.info['duration']==duration[i])
  gifproof.append({'file':filename,'order':order,'holdsMs':duration,'loopMs':sum(duration),'actualFramesExact':True,'sha256':hashlib.sha256((OUT/filename).read_bytes()).hexdigest()})
(SRC/'correspondence.json').write_text(json.dumps({'task':'M1.NCR1','poses':quant,'actualNativeObservedPack':packjson},indent=2)+'\n');(SRC/'changes.json').write_text(json.dumps({'task':'M1.NCR1','inputs':inputs,'poses':records,'gifs':gifproof},indent=2)+'\n');(SRC/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False},indent=2)+'\n');print('PASS',len(checks),'master/native body/features/contact/pack/exact64GIFframe checks')
