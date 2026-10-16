"""RD1 exact supplied fan-frame visible body; only skull cap reconstructed.
Original flat source-derived dummy/masks only in repo. Reference raster external.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[3];S=Path(__file__).parent;O=R/'docs/reviews/M1-RD1';O.mkdir(exist_ok=True);gif=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/brendan-user-reference-original/01agijgmbz561.gif');sha='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e';assert hashlib.sha256(gif.read_bytes()).hexdigest()==sha;g=Image.open(gif);g.seek(2);crop=g.convert('RGBA').crop((0,0,128,192));f=crop.resize((32,48),Image.Resampling.NEAREST);assert f.resize((128,192),Image.Resampling.NEAREST).tobytes()==crop.tobytes();ref=Image.new('RGBA',(32,64));ref.alpha_composite(f,(0,16));P={'outline':(36,35,48,255),'head':(166,104,69,255),'ear':(116,69,57,255),'torso':(116,136,148,255),'arms':(146,153,142,255),'hands':(166,104,69,255),'pelvis':(70,86,113,255),'legs':(96,113,130,255),'shoes':(153,158,153,255)};checks=[]
def ck(n,v):assert v,n;checks.append(n)
def pts(q):return {(i%32,i//32) for i,p in enumerate(q.get_flattened_data()) if p[3]}
def edge(mask):return {p for p in mask if any((p[0]+dx,p[1]+dy) not in mask for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)])}
def bounds(mask):return [min(x for x,y in mask),min(y for x,y in mask),max(x for x,y in mask)+1,max(y for x,y in mask)+1] if mask else None
def make(mask,color):
 q=Image.new('RGBA',(32,64))
 for p in mask:q.putpixel(p,color)
 return q
def runs(q,y):
 rr=[]
 for x in range(32):
  if q.getpixel((x,y))[3]:
   if rr and rr[-1][1]==x:rr[-1][1]+=1
   else:rr.append([x,x+1])
 return rr
protected={}
for name,commit in [('docs/reviews/M1-NF1/front-neutral.png','24444dba660577201f3352fcec89a0bb1a315c5f'),('docs/reviews/M1-NCR1/south-idle/master-hero.png','0bb4ee4293ec2a76a3b8eb77d5d1fca4441bdcc1'),('docs/reviews/M1-NT1/west/neutral.png','ef43a54f05d78ce448396415f799e7e664f217b4')]:
 blob=(R/name).read_bytes();ck(name+' exact preserved source bytes',blob==subprocess.check_output(['git','show',commit+':'+name]));protected[name]={'commit':commit,'sha256':hashlib.sha256(blob).hexdigest()}
source=pts(ref);face={p for p in source if 36<=p[1]<=44}|{(x,45) for x in range(10,22)}
# ONLY covered skull/forehead: original rounded cap, not NF1 head mask or hat
# flourish. Proposed crown25 is declared, not a reference-measured bare skull.
cap={(x,y) for y,a,b in [(25,12,20),(26,10,22),(27,8,24),(28,7,25),(29,6,26),(30,5,27),(31,4,28),(32,4,28),(33,4,28),(34,4,28),(35,4,28)] for x in range(a,b)}
head=face|cap;body={p for p in source if p[1]>=45}-face;mask=head|body;regions={k:set() for k in ['head','ears','torso','arms','hands','pelvis','left-leg','right-leg','left-shoe','right-shoe']};regions['head']=head
# Whole visible external volume. Internal region labels are documented original
# interpretations; they never subtract the source's glove/cloth thickness.
for x,y in body:
 if y>=58 and (x<15 or x>=17):name='left-shoe' if x<16 else 'right-shoe'
 elif y>=56:name='left-leg' if x<16 else 'right-leg'
 elif 50<=y<=54 and (x<9 or x>=23):name='hands'
 elif 46<=y<=54 and (x<10 or x>=22):name='arms'
 elif y>=54:name='pelvis'
 else:name='torso'
 regions[name].add((x,y))
# Two visible front ear patches/inner rims from actual face ROI. Eye registered
# source coordinates retained; flatten graphics, not position or external shape.
innerEar={(6,y) for y in range(37,40)}|{(25,y) for y in range(37,40)}
regions['ears']=innerEar;regions['head']-=innerEar
q=Image.new('RGBA',(32,64));layers={}
for name,region in regions.items():
 key='ear' if name=='ears' else 'legs' if name.endswith('leg') else 'shoes' if name.endswith('shoe') else name;layers[name]=make(region,P[key]);q.alpha_composite(layers[name])
out=edge(mask);outline=make(out,P['outline'])
# Source-anchored segmentation/readability proposals inside visible volume;
# NOT exact tracing of each reference material/black-contour pixel.
internal={(9,y) for y in range(48,55)}|{(22,y) for y in range(48,55)}|{(15,y) for y in range(56,59)}|{(16,y) for y in range(56,59)}
for p in internal&mask:outline.putpixel(p,P['outline'])
layers['outline']=outline;q.alpha_composite(outline)
eyes={(x,y) for x in [12,13,18,19] for y in range(38,42)};ck('actual reference eye locations source dark blue',all(ref.getpixel(p)==(16,33,58,255) for p in eyes));features=make(eyes,P['outline']);layers['eyes']=features;q.alpha_composite(features)
# Source face outline at y44 is a visible jaw row over the body interface, not
# a new neck pedestal. Keep original alpha45 exactly including shoulder wings.
for y in range(36,46):ck(str(y)+' visible face/interface alpha exact',runs(q,y)==runs(ref,y))
ck('source body has338occupied cells45plus',len({p for p in source if p[1]>=45})==338);ck('native32x64 binary alpha',q.size==(32,64) and set(q.getchannel('A').get_flattened_data())<={0,255});ck('inclusive45plus alpha XOR0',q.getchannel('A').crop((0,45,32,64)).tobytes()==ref.getchannel('A').crop((0,45,32,64)).tobytes());ck('unambiguous46plus alpha XOR0',q.getchannel('A').crop((0,46,32,64)).tobytes()==ref.getchannel('A').crop((0,46,32,64)).tobytes());ck('full source shoes58plus alpha XOR0',q.getchannel('A').crop((0,58,32,64)).tobytes()==ref.getchannel('A').crop((0,58,32,64)).tobytes());ck('registered eye sites shape retained',all(q.getpixel(p)==P['outline'] for p in eyes));ck('body row54source width22 retained',runs(q,54)==[[5,27]]);ck('source contact61 exact runs',runs(q,61)==runs(ref,61)==[[9,13],[19,23]]);ck('no head flourish',q.getbbox()[1]==25 and not any(y<25 for x,y in pts(q)));ck('no source costume red/green/white palette',all(p[:3] not in [(255,99,90),(197,66,66),(74,148,82),(115,206,115),(248,248,248),(222,230,239)] for p in q.get_flattened_data()))
re=Image.new('RGBA',(32,64))
for layer in layers.values():re.alpha_composite(layer)
ck('real named flat regions/outline/eyes exact saved recomposition',re.tobytes()==q.tobytes())
# All actual template cells carry a source-visible or reconstructed-skull owner.
ck('region coverage exact mask',set().union(*regions.values())==mask);ck('region memberships disjoint',sum(map(len,regions.values()))==len(mask));ck('skull reconstruction only above36',(mask^source)<={p for p in mask|source if p[1]<36})
bodyDiff={p for p in pts(q)^source if p[1]>=45};difference=make(bodyDiff,(220,30,150,255));ck('actual computed body XOR mask empty',not bodyDiff)
files={}
for name,im in [('reference-derived-dummy.png',q),('dummy-silhouette.png',make(mask,P['outline'])),('body-alpha-difference.png',difference)]+[(name+'-region.png',im) for name,im in layers.items()]:
 im.save(O/name);files[name]={'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest(),'rgbaSHA256':hashlib.sha256(im.tobytes()).hexdigest()}
# Writer-only original flat region/silhouette sheet; NO source reference colors.
F=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12);plate=Image.new('RGB',(1080,390),'#eee8d1');d=ImageDraw.Draw(plate)
show=[('FLAT REFERENCE-POSED DUMMY',q),('SILHOUETTE',make(mask,P['outline'])),('NAMED REGION MAP',None),('BODY ALPHA DIFFERENCE =0',difference)];labelcolors={k:((80+i*37)%200+35,(100+i*53)%200+35,(60+i*29)%200+35,255) for i,k in enumerate(regions)};idmap=Image.new('RGBA',(32,64))
for name,m in regions.items():
 for p in m:idmap.putpixel(p,labelcolors[name])
for col,(title,im) in enumerate(show):
 if im is None:im=idmap
 x=270*col;d.text((x+5,5),title,font=F,fill=P['outline']);big=im.resize((96,192),Image.Resampling.NEAREST);plate.paste(big,(x+10,35),big);plate.paste(im,(x+170,125),im)
d.text((8,255),'RD1 / actual frame2 passing pose, not idle /32x64 native +3x / exact source body alpha45+; only skull reconstructed',font=F,fill=P['outline']);d.text((8,280),'Source reference/registered overlay stays external and is composed/inspected by root before private Library return.',font=F,fill=P['outline']);
for i,(name,color) in enumerate(labelcolors.items()):
 x=10+(i%5)*215;y=325+(i//5)*28;d.rectangle((x,y,x+12,y+12),fill=color);d.text((x+18,y),name,font=F,fill=P['outline'])
plate.save(O/'original-dummy-region-proof.png');idmap.save(O/'region-id-map.png')
rows={str(y):{'source':runs(ref,y),'dummy':runs(q,y)} for y in range(36,64)};record={'task':'M1.RD1','protectedSources':protected,'sourceBodyCells45plus':len({p for p in source if p[1]>=45}),'actualSource':{'gifSHA256':sha,'frame':2,'crop':[0,0,128,192],'exactDisplayMagnificationRemoved':4,'native':[32,48],'translation':[0,16],'pose':'actual front passing, not idle','bodyScale':1},'headBodyInterface':{'inclusiveAlphaGuard':45,'unambiguousBodyGuard':46,'visibleFaceExactRows':[36,45],'centralJaw45':[10,22],'shoulderWings45':[[7,10],[22,25]],'labelsAreNotAnatomy':True},'skullProposal':{'onlyAboveRow':36,'crownRow':25,'roundCapCoordinates':[list(p) for p in sorted(cap)],'qualification':'original reconstruction of hat/hair-covered skull, omits flourish; not source-measured skull'},'internalBoundaryProposal':{'cells':[list(p) for p in sorted(internal&mask)],'armTorsoX':[9,22],'armTorsoRows':[48,54],'interlegX':[15,16],'interlegRows':[56,58],'qualification':'source-anchored projected part labels/readability lines, not pixel-identical reference internal contours or recovered hidden boundaries'},'flatPalette':P,'regionLabelColors':labelcolors,'regions':{k:{'cells':[list(p) for p in sorted(m)],'bounds':bounds(m),'interpretation':'flat source-visible projected volume; hidden internal boundary proposal cannot change external alpha'} for k,m in regions.items()},'eyes':{'cells':[list(p) for p in sorted(eyes)],'sourceColor':[16,33,58,255],'dummyColor':P['outline'],'shapeAndSitesExact':True},'rowRuns':rows,'alphaXOR45plus':0,'alphaXOR46plus':0,'alphaXORShoes58plus':0,'files':files,'renderOrder':list(layers),'notIncluded':['NF1 or Hero change','otherposes','West','native16','animation','creator','deployment'],'appearanceApproval':False};(S/'construction.json').write_text(json.dumps(record,indent=2)+'\n');(S/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False},indent=2)+'\n');print('Built original one posed dummy, exact body45+XOR0; checks',len(checks))
