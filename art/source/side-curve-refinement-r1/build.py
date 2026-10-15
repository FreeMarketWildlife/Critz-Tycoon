"""SR1 one bounded native lower-costume curve trial, no overall resizing."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-SR1';sb=json.loads((root/'art/source/shared-template-restoration-r1/restoration.json').read_text());meta=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());pal={'ink':(36,35,48,255),'navy':(42,52,74,255),'slate':(70,86,113,255)};checks=[];records={};frames={}
def ck(n,v):assert v,n;checks.append(n)
def runs(xs):
 rr=[]
 for x in sorted(xs):
  if rr and rr[-1][1]==x:rr[-1][1]+=1
  else:rr.append([x,x+1])
 return rr
def alphaRuns(q,y):return runs(x for x in range(32) if q.getpixel((x,y))[3])
editsets={
'idle':{'add':[(9,56),(22,56)],'remove':[],'ink':[],'slate':[(10,56),(21,56)],'navy':[(11,57),(12,57)]},
'P':{'add':[(9,56),(22,56)],'remove':[],'ink':[],'slate':[(10,56),(21,56)],'navy':[(11,57),(12,57)]},
'A':{'add':[],'remove':[(4,55),(25,57)],'ink':[(5,55),(24,57)],'slate':[(8,55),(10,56),(10,57)],'navy':[]},
'C':{'add':[],'remove':[(4,56),(27,57)],'ink':[(5,56),(26,57)],'slate':[(10,55),(9,56),(10,56),(9,57),(10,57),(11,57)],'navy':[]}}
for dr in ['west','east']:
 frames[dr]={};records[dr]={}
 for po in ['idle','A','P','C']:
  folder=out/(dr+'-'+po);folder.mkdir(exist_ok=True);old=Image.open(root/f'docs/reviews/M1-PS1/hero-{dr}-{po}.png').convert('RGBA');bald=Image.open(root/f'docs/reviews/M1-SB1/{dr}-{po}/restored-bald.png').convert('RGBA');trial=old.copy();bt=bald.copy();mapping=lambda p:(31-p[0],p[1]) if dr=='east' else tuple(p)
  for action,pts in editsets[po].items():
   for pt in pts:
    p=mapping(pt);before=old.getpixel(p)
    if action=='add':ck(dr+po+' added site originally clear '+str(p),not before[3]);q=pal['ink']
    elif action=='remove':ck(dr+po+' removed site original exterior ink '+str(p),before==pal['ink']);q=(0,0,0,0)
    else:
     ck(dr+po+' existing costume plane site '+str(p),before in pal.values());q=pal[action]
    trial.putpixel(p,q);bt.putpixel(p,q)
  ck(dr+po+' all upper waist hands head pack pixels exact',trial.crop((0,0,32,55)).tobytes()==old.crop((0,0,32,55)).tobytes())
  ck(dr+po+' every lower shoe/contact pixel58+ exact',trial.crop((0,58,32,64)).tobytes()==old.crop((0,58,32,64)).tobytes())
  ck(dr+po+' overall source bounds exact',trial.getbbox()==old.getbbox())
  ck(dr+po+' lower source extrema exact',trial.crop((0,54,32,64)).getbbox()==old.crop((0,54,32,64)).getbbox())
  last=max(y for y in range(64) if alphaRuns(old,y));ck(dr+po+' original last contact spans exact',alphaRuns(trial,last)==alphaRuns(old,last))
  ck(dr+po+' no palette addition',set(trial.get_flattened_data())<=set(old.get_flattened_data()))
  rec=bt.copy();pdir=root/f'docs/reviews/M1-SB1/{dr}-{po}'
  for p in sb['poses'][dr][po]['hairHiddenScalpCutoutCells']:rec.putpixel(tuple(p),(0,0,0,0))
  rec.alpha_composite(Image.open(pdir/'hair-dependent-shading.png').convert('RGBA'));rec.alpha_composite(Image.open(pdir/'original-hair.png').convert('RGBA'));ck(dr+po+' same lower delta keeps exact hair recomposition',rec.tobytes()==trial.tobytes())
  changed=[{'xy':[x,y],'before':list(old.getpixel((x,y))),'after':list(trial.getpixel((x,y)))} for y in range(64) for x in range(32) if old.getpixel((x,y))!=trial.getpixel((x,y))];ad=[c for c in changed if c['before'][3]!=c['after'][3]]
  changedMask=Image.new('RGBA',(32,64));alphaMask=Image.new('RGBA',(32,64))
  for c in changed:changedMask.putpixel(tuple(c['xy']),(213,51,125,255))
  for c in ad:alphaMask.putpixel(tuple(c['xy']),(51,166,132,255) if c['after'][3] else (230,96,45,255))
  for n,q in [('before-hero',old),('trial-hero',trial),('before-template',bald),('trial-template',bt),('actual-changed-rgba-mask',changedMask),('actual-alpha-change-mask',alphaMask)]:q.save(folder/(n+'.png'))
  records[dr][po]={'frame':[32,64],'anchor':[16,64],'sourcePS1Hash':hashlib.sha256((root/f'docs/reviews/M1-PS1/hero-{dr}-{po}.png').read_bytes()).hexdigest(),'trialSHA256':hashlib.sha256((folder/'trial-hero.png').read_bytes()).hexdigest(),'changedCells':changed,'alphaChanges':ad,'contourRuns':{str(y):{'before':alphaRuns(old,y),'after':alphaRuns(trial,y)} for y in range(54,64)},'materialRuns':{str(y):{name:{'before':runs(x for x in range(32) if old.getpixel((x,y))==rgba),'after':runs(x for x in range(32) if trial.getpixel((x,y))==rgba)} for name,rgba in pal.items()} for y in range(55,58)},'protectedUpperEndExclusive':55,'protectedWholeShoeStart':58,'contactRow':last,'contactSpans':alphaRuns(old,last),'packAnchor':meta['directions'][dr][po]['canonicalPackAnchor'],'packStatus':'actual separate source layer untouched; fixed canonical anchor, all pixels above55 exact'}
  frames[dr][po]={'before':old,'trial':trial,'baldBefore':bald,'baldTrial':bt,'mask':changedMask}
for po in editsets:
 ck(po+' lower trial is faithful East mirror',frames['east'][po]['trial'].crop((0,54,32,64)).tobytes()==frames['west'][po]['trial'].transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,54,32,64)).tobytes())
f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
for dr in frames:
 b=Image.new('RGB',(1040,1040),'#eee8d1');d=ImageDraw.Draw(b)
 for row,po in enumerate(['idle','A','P','C']):
  for col,(title,key) in enumerate([('BEFORE HERO','before'),('SR1 HERO TRIAL','trial'),('BEFORE SHARED BALD','baldBefore'),('SR1 SHARED BALD','baldTrial')]):
   x=col*260;y=row*260;q=frames[dr][po][key];d.text((x+5,y+5),dr+' '+po+' '+title,font=f,fill='#242330');big=q.resize((96,192),Image.Resampling.NEAREST);b.paste(big,(x+15,y+30),big);b.paste(q,(x+155,y+100),q);d.line((x+5,y+222,x+120,y+222),fill='#80503d')
  d.text((8,row*260+240),'INTERNAL one curve trial / native+3x / whole55..57 edit only; waist, shoes and contact exact',font=f,fill='#465671')
 b.save(out/(dr+'-native-before-after.png'))
# Countable original grid: eachcell1nativepixel; no reference art copied into Git.
b=Image.new('RGB',(1120,760),'#eee8d1');d=ImageDraw.Draw(b)
for row,po in enumerate(['idle','A','P','C']):
 y=row*190
 for col,(title,key) in enumerate([('BEFORE lower54..63','before'),('TRIAL lower54..63','trial'),('ACTUAL delta mask','mask')]):
  x=col*370;q=frames['west'][po][key].crop((0,54,32,64)).resize((320,100),Image.Resampling.NEAREST);d.text((x+8,y+5),po+' '+title,font=f,fill='#242330');b.paste(q,(x+10,y+35),q)
  for a in range(33):d.line((x+10+a*10,y+35,x+10+a*10,y+135),fill='#9c9989')
  for a in range(11):d.line((x+10,y+35+a*10,x+330,y+35+a*10),fill='#9c9989')
 d.text((8,y+153),f"RGBA changes {len(records['west'][po]['changedCells'])}; alphachanges {len(records['west'][po]['alphaChanges'])}; exactsites/runs in changes.json",font=f,fill='#465671')
b.save(out/'west-countable-lower-grid.png')
(src/'changes.json').write_text(json.dumps({'task':'M1.SR1','state':'one unapproved native side lower-curve trial; no animation','poses':records},indent=2)+'\n');(src/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'visualApproval':False},indent=2)+'\n');print('PASS',len(checks),'bounded source checks; changed West cells:',{p:len(r['changedCells']) for p,r in records['west'].items()})
