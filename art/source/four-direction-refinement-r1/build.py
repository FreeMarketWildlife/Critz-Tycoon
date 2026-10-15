"""H4R1 source-preserving master and explicitly lossy source-derived native counterpart."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from collections import Counter
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[3];SRC=Path(__file__).parent;OUT=ROOT/'docs/reviews/M1-H4R1';OUT.mkdir(exist_ok=True)
M=json.loads((ROOT/'art/source/hero-directional-r14/construction.json').read_text());SM=json.loads((ROOT/'art/source/shared-template-restoration-r1/restoration.json').read_text());checks=[];records={};frames={};inputs={}
COLORS={'_':(0,0,0,0),'o':(36,35,48,255),'n':(42,52,74,255),'b':(70,86,113,255),'g':(116,136,148,255),'d':(116,69,57,255),'s':(166,104,69,255),'S':(195,138,88,255),'v':(174,69,74,255),'r':(237,116,92,255),'R':(255,173,122,255),'c':(249,237,200,255),'C':(191,192,170,255),'h':(50,42,49,255),'m':(76,55,57,255),'l':(112,80,68,255)}
TOK={v:k for k,v in COLORS.items()}
def ck(n,v):
 if not v:raise AssertionError(n)
 checks.append(n)
def load(path):
 f=ROOT/path;inputs[path]=hashlib.sha256(f.read_bytes()).hexdigest();return Image.open(f).convert('RGBA')
def put(q,p,c):q.putpixel(p,COLORS[c])
def mask(q):return { (i%q.width,i//q.width) for i,p in enumerate(q.get_flattened_data()) if p[3] }
def save(q,p):q.save(p);return {'fileSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'rgbaSHA256':hashlib.sha256(q.tobytes()).hexdigest(),'size':list(q.size),'bounds':q.getbbox()}
def north_refine(q,po):
 # Existing lower gray plane is body, never canonical pack. Keep all outline,
 # alpha, contact pixels and source-visible body landmarks.
 for y in range(54,60):
  for x in range(32):
   if q.getpixel((x,y))==COLORS['g']:put(q,(x,y),'b')
 # Short connected lower trouser planes replace repeated rectangular rails.
 for x,y in ({'idle':[(10,57),(21,57)],'P':[(10,57),(21,57),(13,55),(18,55)],'A':[(13,57),(14,57),(15,57),(16,57),(17,57)],'C':[(14,57),(15,57),(16,57),(17,57),(18,57)]}[po]):
  if q.getpixel((x,y)) in [COLORS['b'],COLORS['n']]:put(q,(x,y),'b' if y==57 else 'n')
 if po in ['idle','P']:
  warm=[(x,y) for y,xs in [(58,range(10,13)),(59,range(9,13))] for x in xs];warm+= [(31-x,y) for x,y in warm]
 elif po=='A':warm=[(x,y) for y,xs in [(60,range(11,16)),(61,range(11,15))] for x in xs]
 else:warm=[(x,y) for y,xs in [(60,range(18,23)),(61,range(19,23))] for x in xs]
 for p in warm:
  if q.getpixel(p) in [COLORS['n'],COLORS['b'],COLORS['v']]:put(q,p,'v')
 return q
for dr in ['south','north','west','east']:
 frames[dr]={};records[dr]={}
 for po in ['idle','A','P','C']:
  folder=OUT/(dr+'-'+po);folder.mkdir(exist_ok=True)
  if dr in ['west','east']:hp=f'docs/reviews/M1-SR2/{dr}-{po}/final-hero.png';bp=f'docs/reviews/M1-SR2/{dr}-{po}/final-template.png'
  else:hp=f'docs/reviews/M1-SB1/{dr}-{po}/recomposed-hero.png';bp=f'docs/reviews/M1-SB1/{dr}-{po}/restored-bald.png'
  pin='3b6270e93c8cead6a9d450c603697094741c4967' if dr in ['west','east'] else 'ebccf4cfe894d69af3c6dfda6e3fe58caa313f31'
  for path in [hp,bp]:ck(dr+po+path+' input bytes exact pinned source',subprocess.check_output(['git','show',pin+':'+path])==(ROOT/path).read_bytes())
  old=load(hp);ob=load(bp);hero=old.copy();bald=ob.copy()
  if dr=='north':north_refine(hero,po);north_refine(bald,po)
  hair=load(f'docs/reviews/M1-SB1/{dr}-{po}/original-hair.png');shade=load(f'docs/reviews/M1-SB1/{dr}-{po}/hair-dependent-shading.png');rec=bald.copy()
  for p in SM['poses'][dr][po]['hairHiddenScalpCutoutCells']:rec.putpixel(tuple(p),(0,0,0,0))
  rec.alpha_composite(shade);rec.alpha_composite(hair)
  ck(dr+po+' master separate hair recomposes exact',rec.tobytes()==hero.tobytes());ck(dr+po+' master alpha exact',hero.getchannel('A').tobytes()==old.getchannel('A').tobytes());ck(dr+po+' master full source bounds exact',hero.getbbox()==old.getbbox());ck(dr+po+' master head upper hands fixed pack exact',hero.crop((0,0,32,54)).tobytes()==old.crop((0,0,32,54)).tobytes());last=old.getbbox()[3]-1;ck(dr+po+' master full contact RGBA exact',hero.crop((0,last,32,last+1)).tobytes()==old.crop((0,last,32,last+1)).tobytes());ck(dr+po+' master existing palette',set(hero.get_flattened_data())<=set(old.get_flattened_data()))
  if dr!='north':ck(dr+po+' frozen front/SR2 side exact',hero.tobytes()==old.tobytes() and bald.tobytes()==ob.tobytes())
  files={}
  for name,im in [('master-hero.png',hero),('master-bald.png',bald),('master-hair.png',hair),('master-hair-shadow.png',shade)]:files[name]=save(im,folder/name)
  deltas=[{'xy':[x,y],'from':TOK[old.getpixel((x,y))],'to':TOK[hero.getpixel((x,y))]} for y in range(64) for x in range(32) if hero.getpixel((x,y))!=old.getpixel((x,y))]
  records[dr][po]={'heroInput':hp,'baldInput':bp,'masterChanges':deltas,'files':files,'torsoAnchor32':M['directions'][dr][po]['torsoAnchor'],'fixedPackAnchor32':M['directions'][dr][po]['canonicalPackAnchor'],'contactRow32':last};frames[dr][po]={'masterHero':hero,'masterBald':bald,'masterHair':hair,'masterShade':shade,'before':old}
# Coarse scaffold is NOT final art: source semantic cells chosen within2x2,
# not interpolated RGB. Native maps are editable text; refinements recorded.
def coarse(q,outline=True):
 out=Image.new('RGBA',(16,32))
 for y in range(32):
  for x in range(16):
   block=[q.getpixel((2*x+dx,2*y+dy)) for dy in range(2) for dx in range(2)];opaque=[p for p in block if p[3]]
   if len(opaque)<2:continue
   count=Counter(opaque);p=count.most_common()[0][0]
   if outline and COLORS['o'] in count and len(opaque)<4:p=COLORS['o']
   out.putpixel((x,y),p)
 return out
maps_path=SRC/'native-maps.json';existing=json.loads(maps_path.read_text()) if maps_path.exists() else {}
scaffolds={}
for dr in frames:
 scaffolds[dr]={}
 for po,data in frames[dr].items():
  bald=coarse(data['masterBald']);hero=coarse(data['masterHero']);rows=lambda im:[''.join(TOK[im.getpixel((x,y))] for x in range(16)) for y in range(32)]
  scaffolds[dr][po]={'bald':rows(bald),'hero':rows(hero)}
(SRC/'source-derived-scaffold.json').write_text(json.dumps(scaffolds,indent=2)+'\n')
if not existing:maps_path.write_text(json.dumps(scaffolds,indent=2)+'\n');existing=scaffolds
for dr in frames:
 for po,data in frames[dr].items():
  def parse(rows):
   ck(dr+po+' native dimensions',len(rows)==32 and all(len(r)==16 for r in rows));q=Image.new('RGBA',(16,32));q.putdata([COLORS[c] for r in rows for c in r]);return q
  nb=parse(existing[dr][po]['bald']);nh=parse(existing[dr][po]['hero']);data['nativeBald']=nb;data['nativeHero']=nh
  folder=OUT/(dr+'-'+po)
  for name,q in [('native-bald.png',nb),('native-hero.png',nh)]:records[dr][po]['files'][name]=save(q,folder/name)
# Clean construction preview for actual assessment, equal display: master3x/native6x.
f=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
def plate(path,poses):
 p=Image.new('RGB',(1040,260*len(poses)),'#eee8d1');d=ImageDraw.Draw(p)
 for row,(dr,po) in enumerate(poses):
  for col,(key,title,scale) in enumerate([('masterHero','MASTER32 HERO',3),('masterBald','MASTER32 SHARED BALD',3),('nativeHero','NATIVE16 HERO',6),('nativeBald','NATIVE16 SHARED BALD',6)]):
   q=frames[dr][po][key];x=260*col;y=260*row;d.text((x+6,y+5),dr+' '+po+' '+title,font=f,fill='#242330');big=q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST);p.paste(big,(x+15,y+27),big);p.paste(q,(x+163,y+120),q);d.line((x+10,y+219,x+125,y+219),fill='#b3aa94')
  d.text((8,260*row+235),'INTERNAL candidate / true native + integer enlargement / native16 is explicitly lossy source-derived art',font=f,fill='#465671')
 p.save(OUT/path)
plate('four-direction-idles.png',[(dr,'idle') for dr in frames]);plate('all-direction-poses.png',[(dr,po) for dr in frames for po in ['idle','A','P','C']]);plate('north-all-poses.png',[('north',po) for po in ['idle','A','P','C']])
(SRC/'changes.json').write_text(json.dumps({'task':'M1.H4R1','source':records,'inputs':inputs,'checks':checks},indent=2)+'\n')
print('Master guards',len(checks),'North changes',{p:len(records['north'][p]['masterChanges']) for p in records['north']})
# Separate actual native attachment, with explicit scalp cutout for hair-only
# silhouette holes; not a dressed full-figure overlay.
correspondence={};native_source_choices={};packproof={}
for dr in frames:
 correspondence[dr]={};native_source_choices[dr]={};packproof[dr]={}
 for po,data in frames[dr].items():
  tag=dr+'-'+po;folder=OUT/tag;nb=data['nativeBald'];nh=data['nativeHero'];hair=Image.new('RGBA',(16,32));shade=hair.copy();cut=hair.copy();re=nb.copy();hpts=mask(data['masterHair']);spts=mask(data['masterShade']);parts=[];cutcells=[];shadecells=[];haircells=[];choice=[]
  for y in range(32):
   for x in range(16):
    pos=(x,y);a=nb.getpixel(pos);b=nh.getpixel(pos);block={(2*x+dx,2*y+dy) for dy in range(2) for dx in range(2)};sourcecolors={data['masterHero'].getpixel(p) for p in block};sourcebald={data['masterBald'].getpixel(p) for p in block}
    choice.append({'xy':[x,y],'masterBlock':[2*x,2*y,2*x+2,2*y+2],'hero':TOK[b],'bald':TOK[a],'heroColorInSourceBlock':b in sourcecolors,'baldColorInSourceBlock':a in sourcebald})
    if b==a:continue
    if not b[3]:cut.putpixel(pos,(255,255,255,255));re.putpixel(pos,(0,0,0,0));cutcells.append([x,y]);continue
    if block & hpts and b in [COLORS[c] for c in 'ohml']:
     hair.putpixel(pos,b);haircells.append([x,y])
    else:
     # Coarse skin-shadow/edge decision arises only within original head zone.
     ck(tag+str(pos)+' native nonhair difference limited to original head',y<23-(po=='P'))
     shade.putpixel(pos,b);shadecells.append([x,y])
  re.alpha_composite(shade);re.alpha_composite(hair);ck(tag+' native original hair/shadow exact recomposition',re.tobytes()==nh.tobytes());headbottom=23-int(po=='P');ck(tag+' native shared body below head exact RGBA',nh.crop((0,headbottom,16,32)).tobytes()==nb.crop((0,headbottom,16,32)).tobytes());ck(tag+' native binary alpha',set(nh.getchannel('A').get_flattened_data())<={0,255} and set(nb.getchannel('A').get_flattened_data())<={0,255});ck(tag+' native existing master palette subset',set(nh.get_flattened_data())<=set(data['masterHero'].get_flattened_data()) and set(nb.get_flattened_data())<=set(data['masterBald'].get_flattened_data()));ck(tag+' native contact row corresponds master floor',nh.getbbox()[3]-1==records[dr][po]['contactRow32']//2)
  for name,q in [('native-hair.png',hair),('native-hair-shadow.png',shade),('native-scalp-cutout.png',cut),('native-recomposed-hero.png',re)]:records[dr][po]['files'][name]=save(q,folder/name)
  records[dr][po]['nativeAttachment']={'hairCells':haircells,'hairDependentShadeAndCoarseEdgeCells':shadecells,'scalpCutoutCells':cutcells,'recompositionRGBADifference':0,'bodyBelowRow':headbottom,'bodyRGBADifference':0,'qualification':'coarse original-hair/shadow representation; shared body is never covered by the attachment'}
  e=M['directions'][dr][po];registration={}
  for feature in ['eyes','ears','hands']:
   actual=e['commonFeatureRegistration'][feature]['cells'];cells=sorted({(x//2,y//2) for x,y in actual});registration[feature]={'masterSites':actual,'nativeRegisteredSites':[list(p) for p in cells],'nativeBaldColors':[[*p,TOK[nb.getpixel(p)]] for p in cells],'quantizationRule':'floor each source cell coordinate /2; individual boundary/occlusion detail may collapse; this is not a count-preserving inverse','masterCellRoundingOffsets':sorted({(2*(x//2)-x,2*(y//2)-y) for x,y in actual})}
  registration['baldPaintedBounds32']=data['masterBald'].getbbox();registration['baldPaintedBounds16']=nb.getbbox();registration['canonicalFrameAnchor32']=[16,64];registration['canonicalFrameAnchor16']=[8,32];registration['torsoAnchor32']=e['torsoAnchor'];registration['torsoAnchor16']=[v//2 for v in e['torsoAnchor']];registration['canonicalTorsoLocalPackAnchor32']=e['canonicalPackAnchor'];registration['canonicalTorsoLocalPackAnchor16']=[v//2 for v in e['canonicalPackAnchor']];registration['torsoTransform32']=e['torsoTransform'];registration['torsoTransform16']=[v//2 for v in e['torsoTransform']];registration['renderedPackRegistration32']=[e['canonicalPackAnchor'][0]+e['torsoTransform'][0],e['canonicalPackAnchor'][1]+e['torsoTransform'][1]];registration['renderedPackRegistration16']=[v//2 for v in registration['renderedPackRegistration32']];registration['contactRow32']=records[dr][po]['contactRow32'];registration['contactRow16']=nh.getbbox()[3]-1
  correspondence[dr][po]=registration;native_source_choices[dr][po]=choice
  # Actual archived pack raster, proven independently of metadata. Normalize
  # torso translation and compare all RGBA pixels to idle layer.
  pack=load(f'docs/reviews/M1-HR14/pack-layer-{tag}.png');idlepack=load(f'docs/reviews/M1-HR14/pack-layer-{dr}-idle.png');norm=Image.new('RGBA',(32,64));norm.paste(pack,(-e['torsoTransform'][0],-e['torsoTransform'][1]));ck(tag+' actual pack layer rigid torso-relative raster',norm.tobytes()==idlepack.tobytes());packproof[dr][po]={'archivedRasterBounds':pack.getbbox(),'torsoTransform':e['torsoTransform'],'normalizedRGBAExactToIdle':True,'renderedAnchor':registration['renderedPackRegistration32'],'absoluteFrameFixed':False,'contract':'rigid torso-local attachment, moves with P bob; never mirrored between A/C'}
  # Coarse pack is an observed material mask, NOT a hidden torso completion.
  packcells={ (i%32//2,i//32//2) for i,v in enumerate(e['visiblePackMask']) if v};np=Image.new('RGBA',(16,32))
  for p in packcells:
   if nh.getpixel(p) in [COLORS[c] for c in 'onbg']:np.putpixel(p,nh.getpixel(p))
  save(np,folder/'native-observed-pack.png');packproof[dr][po]['nativeObservedPackCells']=[list(p) for p in sorted(mask(np))]
# Front/back idle scalp/body geometry reflected; shading remains asymmetric.
for dr in ['south','north']:
 q=frames[dr]['idle']['nativeBald'];ck(dr+' native idle bald alpha bilateral',q.getchannel('A').tobytes()==q.transpose(Image.Transpose.FLIP_LEFT_RIGHT).getchannel('A').tobytes())
for po in ['idle','A','P','C']:
 for key in ['masterHero','masterBald']:
  ck(po+key+' frozen side lower mirrored',frames['east'][po][key].crop((0,54,32,64)).tobytes()==frames['west'][po][key].transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,54,32,64)).tobytes())
 for key in ['nativeHero','nativeBald']:
  ck(po+key+' native side lower mirrored',frames['east'][po][key].crop((0,27 if po!='P' else 26,16,32)).tobytes()==frames['west'][po][key].transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,27 if po!='P' else 26,16,32)).tobytes())
# Before/after North: complete poses not tiny unexplained crops.
p=Image.new('RGB',(780,1040),'#eee8d1');d=ImageDraw.Draw(p)
for row,po in enumerate(['idle','A','P','C']):
 for col,(key,title) in enumerate([('before','SB1 BEFORE'),('masterHero','H4R1 NORTH MATERIAL'),('masterBald','SHARED BALD')]):
  q=frames['north'][po][key];x=260*col;y=260*row;d.text((x+5,y+5),po+' '+title,font=f,fill='#242330');big=q.resize((96,192),Image.Resampling.NEAREST);p.paste(big,(x+15,y+27),big);p.paste(q,(x+160,y+120),q)
p.save(OUT/'north-before-after.png')
# Countable guide: one cell per native pixel, Y up, center distinct. Never
# baked into native art. Bottom crop is intentionally not a head/bone measure.
p=Image.new('RGB',(1120,760),'#eee8d1');d=ImageDraw.Draw(p)
for col,dr in enumerate(frames):
 x=col*280+20;d.text((x,8),dr+' master32 idle',font=f,fill='#242330');q=frames[dr]['idle']['masterBald'];big=q.resize((192,384),Image.Resampling.NEAREST);p.paste(big,(x,28),big)
 for z in range(33):d.line((x+z*6,28,x+z*6,412),fill='#bdb5a2' if z!=16 else '#bb6699')
 for z in range(65):d.line((x,28+z*6,x+192,28+z*6),fill='#bdb5a2' if (64-z)%10 else '#748894')
 for edge in [0,10,20,30,40,50,60,64]:d.text((x+197,28+(64-edge)*6-5),str(edge),font=f,fill='#465671')
 d.text((x,435),'native16 / one cell per px',font=f,fill='#242330');q=frames[dr]['idle']['nativeBald'];big=q.resize((128,256),Image.Resampling.NEAREST);p.paste(big,(x,460),big)
 for z in range(17):d.line((x+z*8,460,x+z*8,716),fill='#bdb5a2' if z!=8 else '#bb6699')
 for z in range(33):d.line((x,460+z*8,x+128,460+z*8),fill='#bdb5a2' if (32-z)%10 else '#748894')
p.save(OUT/'countable-idle-grid.png')
# Contact correspondence is measured from actual final PNG runs, not bbox.
def runs(q,y):
 rr=[]
 for x in range(q.width):
  if q.getpixel((x,y))[3]:
   if rr and rr[-1][1]==x:rr[-1][1]+=1
   else:rr.append([x,x+1])
 return rr
for dr in frames:
 for po,data in frames[dr].items():
  a=runs(data['masterHero'],records[dr][po]['contactRow32']);b=runs(data['nativeHero'],data['nativeHero'].getbbox()[3]-1);ck(dr+po+' native contact same run count',len(a)==len(b));ck(dr+po+' native contact exact half source widths',all(2*(bb-aa)==d-c for (c,d),(aa,bb) in zip(a,b)));dev=[{'masterRun':m,'nativeRun':n,'edgeOffsetsMasterPixels':[2*n[0]-m[0],2*n[1]-m[1]],'centerOffsetMasterPixels':sum(n)-sum(m)/2} for m,n in zip(a,b)];ck(dr+po+' contact edges at most1 master pixel rounding',all(abs(v)<=1 for r in dev for v in r['edgeOffsetsMasterPixels']));correspondence[dr][po]['contactRunsAndRounding']=dev
  q=data['masterBald'].getbbox();n=data['nativeBald'].getbbox();correspondence[dr][po]['baldBoundsEdgeOffsetsMasterPixels']=[2*b-a for a,b in zip(q,n)]
  # Explicit coarser material motif, not an added master clothing division.
  if dr=='south':correspondence[dr][po]['nativeCreamMotif']={'sourceMasterRow':47 if po=='P' else 49,'sourceSpan':[13,19],'nativeRow':23 if po=='P' else 24,'nativeSpan':[6,9],'widthExactHalf':True,'centerOffsetMasterPixels':-1,'qualification':'source cream motif retained by explicit material ownership; no master edits'}

# Original per-direction cadence preserved, no new animator/controller.
order=M['order'];gifrecords=[]
for dr in frames:
 baseholds=[100]*8 if dr=='south' else [70,60,70,70,70,60,70,70]
 for slow in [1,4]:
  images=[]
  for slot,po in enumerate(order):
   c=Image.new('RGB',(1040,250),'#eee8d1');d=ImageDraw.Draw(c);d.fontmode='1';d.text((7,4),f'INTERNAL H4R1 {dr} slot {slot+1}/8 {po} / existing holds x{slow} / native16 explicitly lossy',font=f,fill='#242330')
   for col,(key,title,scale) in enumerate([('masterHero','MASTER32 HERO',3),('masterBald','MASTER32 SAME BODY',3),('nativeHero','NATIVE16 HERO',6),('nativeBald','NATIVE16 SAME BODY',6)]):
    q=frames[dr][po][key];x=col*260;big=q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST);c.paste(big,(x+15,27),big);c.paste(q,(x+163,120),q);d.text((x+6,225),title,font=f,fill='#465671')
   images.append(c)
  fn=f'{dr}-paired-existing-walk-{"normal" if slow==1 else "slow"}.gif';dur=[t*slow for t in baseholds];images[0].save(OUT/fn,save_all=True,append_images=images[1:],duration=dur,loop=0,optimize=False,disposal=2);g=Image.open(OUT/fn);ck(fn+' eight labeled slots infinite loop',g.n_frames==8 and g.info['loop']==0)
  for i,c in enumerate(images):g.seek(i);ck(fn+str(i)+' actual decode exact source panels and hold',g.convert('RGB').tobytes()==c.tobytes() and g.info['duration']==dur[i])
  gifrecords.append({'file':fn,'frames':8,'order':order,'holdsMs':dur,'loopMs':sum(dur),'sha256':hashlib.sha256((OUT/fn).read_bytes()).hexdigest(),'decodedAllFramesExact':True})
(SRC/'correspondence.json').write_text(json.dumps({'qualification':'new source-derived16x32 coarse representation; not inverse, not accepted replacement','poses':correspondence,'nativeCellChoices':native_source_choices,'packRasterAudit':packproof},indent=2)+'\n')
(SRC/'changes.json').write_text(json.dumps({'task':'M1.H4R1','source':records,'inputs':inputs,'gifs':gifrecords},indent=2)+'\n');(SRC/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False},indent=2)+'\n')
print('PASS',len(checks),'master/source/shared-native-body/attachment/pack-raster/decoded-GIF checks')
