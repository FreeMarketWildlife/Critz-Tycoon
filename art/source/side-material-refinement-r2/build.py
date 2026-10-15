"""SR2 material continuation trial, iterative assessment within fixed source silhouette."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-SR2';proposal=json.loads((root/'docs/reviews/M1-SR1/interior-material-proposal.json').read_text());N=(42,52,74,255);B=(70,86,113,255);D=(174,69,74,255);frames={};records={}
fnt=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
for dr in ['west','east']:
 frames[dr]={};records[dr]={}
 for po in ['idle','A','P','C']:
  old=Image.open(root/f'docs/reviews/M1-SR1/{dr}-{po}/trial-hero.png').convert('RGBA');bald=Image.open(root/f'docs/reviews/M1-SR1/{dr}-{po}/trial-template.png').convert('RGBA');shade=old.copy();bs=bald.copy();pts=[(31-x,y) if dr=='east' else (x,y) for x,y in proposal['poses'][po]['proposedCells']]
  for p in pts:assert old.getpixel(p)==N;shade.putpixel(p,B);bs.putpixel(p,B)
  folder=out/(dr+'-'+po);folder.mkdir(exist_ok=True);shade.save(folder/'phase1-plane-only-hero.png');bs.save(folder/'phase1-plane-only-template.png');frames[dr][po]={'before':old,'baldBefore':bald,'plane':shade,'baldPlane':bs};records[dr][po]={'planeContinuationCells':[list(p) for p in pts]}
def sheet(name,columns,dr="west"):
 b=Image.new('RGB',(270*len(columns),1040),'#eee8d1');d=ImageDraw.Draw(b)
 for row,po in enumerate(['idle','A','P','C']):
  for col,(title,key) in enumerate(columns):
   x=col*270;y=row*260;q=frames[dr][po][key];d.text((x+5,y+5),dr+' '+po+' '+title,font=fnt,fill='#242330');big=q.resize((96,192),Image.Resampling.NEAREST);b.paste(big,(x+15,y+28),big);b.paste(q,(x+165,y+90),q)
  d.text((8,row*260+237),'INTERNAL / native32x64 + integer3x / silhouette, footprint and anchors fixed',font=fnt,fill='#465671')
 b.save(out/name)
sheet('phase1-plane-only-evaluation.png',[('SR1 BASELINE','before'),('FIVE-SITE PLANE ONLY','plane')])
print('Phase1 applied to8poses; actual visual assessment required before deciding final surface treatment.')
# Phase2: compact upper surfaces grow from actual pre-existing burgundy cues.
# No outline, alpha, waist or contact sites are recolored.
shoeSurfaceSmall={'idle':[(11,58),(12,58),(11,59),(12,59)],'P':[(11,58),(12,58),(11,59),(12,59)],'A':[(20,60),(21,60),(21,61),(22,61)],'C':[(10,60),(11,60),(9,61),(11,61)]}
for dr in frames:
 for po in frames[dr]:
  q=frames[dr][po]['plane'].copy();b=frames[dr][po]['baldPlane'].copy();sites=[(31-x,y) if dr=='east' else (x,y) for x,y in shoeSurfaceSmall[po]]
  for p in sites:
   assert q.getpixel(p) in [N,B];q.putpixel(p,D);b.putpixel(p,D)
  q.save(out/(dr+'-'+po)/'phase2-small-surface-hero.png');b.save(out/(dr+'-'+po)/'phase2-small-surface-template.png');frames[dr][po]['small']=q;frames[dr][po]['baldSmall']=b
sheet('phase2-small-surface-evaluation.png',[('SR1 BASELINE','before'),('BLUE PLANE ONLY','plane'),('COMPACT SHOE SURFACE','small')])
print('Compact source-cue material surfaces written; evaluate before finalizing.')
# The first small panel is still too spot-like at game1x. Complete a compact
# seven-cell curved surface (not a long rail), preserving dark contact edges.
shoeExtra={'idle':[(11,60),(12,60)],'P':[(11,60),(12,60)],'A':[(20,59),(21,59)],'C':[(9,59),(10,59)]}
for dr in frames:
 for po in frames[dr]:
  q=frames[dr][po]['small'].copy();b=frames[dr][po]['baldSmall'].copy();sites=[(31-x,y) if dr=='east' else (x,y) for x,y in shoeExtra[po]]
  for p in sites:assert q.getpixel(p) in [N,B];q.putpixel(p,D);b.putpixel(p,D)
  folder=out/(dr+'-'+po);q.save(folder/'final-hero.png');b.save(folder/'final-template.png');frames[dr][po]['final']=q;frames[dr][po]['baldFinal']=b
  records[dr][po]['shoeSurfaceAddedCells']=[list((31-x,y) if dr=='east' else (x,y)) for x,y in shoeSurfaceSmall[po]+shoeExtra[po]]
# Two adjacent existing-coral cap cells clarify light-facing footwear material
# at native1x; dark burgundy remains connected to the source cue and underside.
R=(237,116,92,255);caps={'idle':[(11,58),(12,58)],'P':[(11,58),(12,58)],'A':[(20,59),(21,59)],'C':[(9,59),(10,59)]}
for dr in frames:
 for po in frames[dr]:
  q=frames[dr][po]['final'];b=frames[dr][po]['baldFinal'];sites=[(31-x,y) if dr=='east' else (x,y) for x,y in caps[po]]
  for p in sites:assert q.getpixel(p)==D;q.putpixel(p,R);b.putpixel(p,R)
  folder=out/(dr+'-'+po);q.save(folder/'final-hero.png');b.save(folder/'final-template.png');records[dr][po]['coralCapCells']=[list(p) for p in sites]
# Root/game1x inspection: seven-cell warm cue still reads a toe spot on a blue
# wedge. A coherent fuller shoe upper is needed within the fixed footprint.
# These are proposed visible surfaces, not a measured hidden anatomical seam.
nearRows={
 'idle':{58:range(10,17),59:range(11,17),60:range(12,17)},
 'P':{58:range(10,17),59:range(11,17),60:range(12,17)},
 'A':{59:range(20,23),60:range(19,23),61:range(20,23),62:range(21,23)},
 'C':{59:range(8,12),60:range(8,12),61:range(9,12),62:range(9,11)}}
nearLight={'idle':[(11,58),(12,58),(13,58),(14,58)],'P':[(11,58),(12,58),(13,58),(14,58)],'A':[(20,59),(21,59),(20,60)],'C':[(8,59),(9,59),(10,60)]}
farUpper={'idle':[(18,58),(19,58),(18,59)],'P':[(18,58),(19,58),(18,59)],'A':[(9,59),(10,59),(10,60)],'C':[(23,59),(24,59),(24,60)]}
for dr in frames:
 for po in frames[dr]:
  old=frames[dr][po]['before'];q=frames[dr][po]['plane'].copy();b=frames[dr][po]['baldPlane'].copy();mappt=lambda p:(31-p[0],p[1]) if dr=='east' else tuple(p)
  near={mappt((x,y)) for y,xs in nearRows[po].items() for x in xs};far={mappt(p) for p in farUpper[po]};light={mappt(p) for p in nearLight[po]}
  for p in near|far:
   assert q.getpixel(p)[3] and old.getpixel(p)[:3]!=(36,35,48)
   q.putpixel(p,R if p in light else D);b.putpixel(p,R if p in light else D)
  folder=out/(dr+'-'+po);q.save(folder/'final-hero.png');b.save(folder/'final-template.png');frames[dr][po]['final']=q;frames[dr][po]['baldFinal']=b
  records[dr][po]['fullerNearSurfaceCells']=[list(p) for p in sorted(near)];records[dr][po]['coolerFarSurfaceCells']=[list(p) for p in sorted(far)];records[dr][po]['nearCoralLightCells']=[list(p) for p in sorted(light)]
sheet('final-material-before-after.png',[('SR1 BASELINE','before'),('SR2 MATERIAL TRIAL','final'),('SHARED BALD SAME BODY','baldFinal')])
b=Image.new('RGB',(1120,760),'#eee8d1');d=ImageDraw.Draw(b)
for row,po in enumerate(['idle','A','P','C']):
 for col,(title,key) in enumerate([('SR1 lower54..63','before'),('SR2 material candidate','final'),('SHARED BALD identical lower','baldFinal')]):
  x=col*370;y=row*190;im=frames['west'][po][key].crop((0,54,32,64)).resize((320,100),Image.Resampling.NEAREST);d.text((x+7,y+5),po+' '+title,font=fnt,fill='#242330');b.paste(im,(x+10,y+35),im)
  for z in range(33):d.line((x+10+z*10,y+35,x+10+z*10,y+135),fill='#9c9989')
  for z in range(11):d.line((x+10,y+35+z*10,x+330,y+35+z*10),fill='#9c9989')
 d.text((8,row*190+155),'Existing-palette surfaces / outline and full alpha/contact footprint unchanged / no pale sole rail',font=fnt,fill='#465671')
b.save(out/'final-countable-material-grid.png')
print('Final connected planes and compact source-accent surfaces built; inspect atgame1x and actual side cycle.')
sheet('east-final-material-before-after.png',[('SR1 BASELINE','before'),('SR2 MATERIAL TRIAL','final'),('SHARED BALD SAME BODY','baldFinal')],dr='east')
# Actual final source guards and meaningful surface registration, not a fixed count gate.
checks=[];anchors={'idle':(10,58),'P':(10,58),'A':(22,60),'C':(9,60)};changes={};sbmeta=json.loads((root/'art/source/shared-template-restoration-r1/restoration.json').read_text());sourceMeta=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text())
def ck(n,v):assert v,n;checks.append(n)
def rowruns(q,y):
 rr=[]
 for x in range(32):
  if q.getpixel((x,y))[3]:
   if rr and rr[-1][1]==x:rr[-1][1]+=1
   else:rr.append([x,x+1])
 return rr
for dr in frames:
 changes[dr]={}
 for po,data in frames[dr].items():
  old,q,bt=data['before'],data['final'],data['baldFinal'];folder=out/(dr+'-'+po);old.save(folder/'before-hero.png');data['baldBefore'].save(folder/'before-template.png');ck(dr+po+' source alpha/full footprint exact',q.getchannel('A').tobytes()==old.getchannel('A').tobytes());ck(dr+po+' all upper head hands waist pack exact',q.crop((0,0,32,55)).tobytes()==old.crop((0,0,32,55)).tobytes());ck(dr+po+' selected palette exact subset',set(q.get_flattened_data())<=set(old.get_flattened_data()));ck(dr+po+' global frame/source bounds exact',q.size==(32,64) and q.getbbox()==old.getbbox())
  exterior=set()
  for y in range(64):
   for x in range(32):
    if old.getpixel((x,y))[3] and any(not(0<=xx<32 and 0<=yy<64) or not old.getpixel((xx,yy))[3] for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):exterior.add((x,y))
  ck(dr+po+' all exterior colors exact',all(q.getpixel(p)==old.getpixel(p) for p in exterior))
  last=max(y for y in range(64) if rowruns(old,y));ck(dr+po+' contact row spans and colors exact',q.crop((0,last,32,last+1)).tobytes()==old.crop((0,last,32,last+1)).tobytes())
  anchor=(31-anchors[po][0],anchors[po][1]) if dr=='east' else anchors[po];ck(dr+po+' actual preexisting shoe cue retained',old.getpixel(anchor)==q.getpixel(anchor)==D)
  surface={tuple(p) for p in records[dr][po]['fullerNearSurfaceCells']};ck(dr+po+' compact warm surface actual cells match ramp',all(q.getpixel(p) in [D,R] for p in surface));seen={anchor};stack=[anchor]
  while stack:
   x,y=stack.pop()
   for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in surface and p not in seen:seen.add(p);stack.append(p)
  ck(dr+po+' warm surface connects to source cue without detached patch',seen==surface)
  rec=bt.copy()
  for p in sbmeta['poses'][dr][po]['hairHiddenScalpCutoutCells']:rec.putpixel(tuple(p),(0,0,0,0))
  sbdir=root/f'docs/reviews/M1-SB1/{dr}-{po}';rec.alpha_composite(Image.open(sbdir/'hair-dependent-shading.png').convert('RGBA'));rec.alpha_composite(Image.open(sbdir/'original-hair.png').convert('RGBA'));ck(dr+po+' exact shared body original hair recomposition',rec.tobytes()==q.tobytes())
  delta=[{'xy':[x,y],'before':list(old.getpixel((x,y))),'after':list(q.getpixel((x,y)))} for y in range(64) for x in range(32) if old.getpixel((x,y))!=q.getpixel((x,y))]
  cm=Image.new('RGBA',(32,64))
  for item in delta:cm.putpixel(tuple(item['xy']),(216,51,130,255))
  cm.save(folder/'actual-rgba-change-mask.png');changes[dr][po]={'sourceSR1':f'docs/reviews/M1-SR1/{dr}-{po}/trial-hero.png','sourceSHA256':hashlib.sha256((root/f'docs/reviews/M1-SR1/{dr}-{po}/trial-hero.png').read_bytes()).hexdigest(),'finalHeroSHA256':hashlib.sha256((folder/'final-hero.png').read_bytes()).hexdigest(),'finalTemplateSHA256':hashlib.sha256((folder/'final-template.png').read_bytes()).hexdigest(),'changedCells':delta,'alphaChanges':0,'preexistingCue':list(anchor),'actualWarmSurfaceCells':[list(p) for p in sorted(surface)],'coolerFarSurfaceCells':records[dr][po]['coolerFarSurfaceCells'],'surfaceBounds':[min(x for x,y in surface),min(y for x,y in surface),max(x for x,y in surface)+1,max(y for x,y in surface)+1],'surfaceOwnership':'visible existing-cue footwear surface; cooler opposite overlap left source-grounded, no hidden calf/joint claim','contactRow':last,'contactSpans':rowruns(q,last),'fixedPackAnchor':sourceMeta['directions'][dr][po]['canonicalPackAnchor'],'sourceAnchorsUnchanged':True,'hairRecompositionDifference':0}
for po in anchors:ck(po+' final lower materials faithful East mirror',frames['east'][po]['final'].crop((0,54,32,64)).tobytes()==frames['west'][po]['final'].transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,54,32,64)).tobytes())
# Original source8slots/side holds, no new animation design or altered controller.
order=sourceMeta['order'];holds=[70,60,70,70,70,60,70,70];gifproof=[]
for dr in frames:
 for slow in [1,4]:
  seq=[]
  for slot,po in enumerate(order):
   c=Image.new('RGB',(720,244),'#eee8d1');d=ImageDraw.Draw(c);d.fontmode='1';d.text((5,4),f'INTERNAL SR2 {dr} slot{slot+1} {po} / existing source holds x{slow}',font=fnt,fill='#242330')
   for col,(name,key) in enumerate([('SR1 BASELINE','before'),('SR2 MATERIAL CANDIDATE','final'),('SHARED BALD SAME BODY','baldFinal')]):
    x=col*240;q=frames[dr][po][key];big=q.resize((96,192),Image.Resampling.NEAREST);c.paste(big,(x+10,25),big);c.paste(q,(x+145,90),q);d.text((x+5,225),name,font=fnt,fill='#465671')
   seq.append(c)
  path=out/f'{dr}-existing-side-cycle-{"normal" if slow==1 else "slow"}.gif';durations=[t*slow for t in holds];seq[0].save(path,save_all=True,append_images=seq[1:],duration=durations,loop=0,optimize=False,disposal=2);g=Image.open(path);ck(path.name+' original8labeled slots and loop',g.n_frames==8 and g.info.get('loop')==0)
  for i,c in enumerate(seq):g.seek(i);ck(path.name+str(i)+' actual decoded source holds/panels exact',g.convert('RGB').tobytes()==c.tobytes() and g.info['duration']==durations[i])
  gifproof.append({'path':str(path.relative_to(root)),'frames':8,'holdsMs':durations,'loopMs':sum(durations),'actualDecodedPixelsExact':True})
(src/'changes.json').write_text(json.dumps({'task':'M1.SR2','baselineArt':'73eb6c102e3ac928bd013360dfd2c076fdb93bfb','state':'iterated internal material candidate, not appearance approval','poses':changes,'sourceOrder':order,'holdsMs':holds,'gifs':gifproof},indent=2)+'\n');(src/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False},indent=2)+'\n')
print('PASS',len(checks),'meaningful exact source/material/shared-body/GIF guards; final actual visual/cycle judgment remains separate.')
# Art-only review surface. No game/controller/storage imports or installation.
(out/'side-material-motion-review.html').write_text('''<!doctype html><meta charset="utf-8"><title>SR2 internal material cycle</title><style>body{background:#eee8d1;color:#242330;font:13px monospace}.row{display:flex;gap:18px;margin:15px 0}section{width:220px}img{image-rendering:pixelated;vertical-align:bottom}.native{width:32px;height:64px;margin-right:20px}.large{width:96px;height:192px}h1{font-size:17px}</style><h1>INTERNAL SR2 — source silhouette, changed material surfaces</h1><div id="clock"></div><div id="panels"></div><script>const order=['A','A','P','P','C','C','P','P'],holds=[70,60,70,70,70,60,70,70].map(x=>x*4);const total=holds.reduce((a,b)=>a+b,0);const parent=document.getElementById('panels');for(const dr of ['west','east']){const h=document.createElement('h2');h.textContent=dr;parent.append(h);const row=document.createElement('div');row.className='row';for(const pair of [['Before','before-hero.png'],['SR2','final-hero.png'],['Shared bald','final-template.png']]){const s=document.createElement('section');s.textContent=pair[0]+' native1x +3x';for(const k of ['native','large']){const im=document.createElement('img');im.className=k;im.dataset.dr=dr;im.dataset.file=pair[1];s.append(im)}row.append(s)}parent.append(row)}const start=performance.now();let last=-1;function show(){const t=performance.now()-start;let n=0,phase=t%total;while(n<7&&phase>=holds[n])phase-=holds[n++];if(n!==last){for(const im of document.images)im.src=im.dataset.dr+'-'+order[n]+'/'+im.dataset.file;last=n}document.getElementById('clock').textContent='Slow exact source slot '+(n+1)+'/8 '+order[n]+' cycle '+Math.floor(t/total);requestAnimationFrame(show)}show()</script>''')
