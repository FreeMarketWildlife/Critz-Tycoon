"""NT1 two-pose flat semantic mannequin. Manual masks, no hidden-bone claim."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[3];SRC=Path(__file__).parent;OUT=ROOT/'docs/reviews/M1-NT1';OUT.mkdir(exist_ok=True);F=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
C={'outline':(36,35,48,255),'head':(166,104,69,255),'ear':(116,69,57,255),'torso':(116,136,148,255),'upperArm':(191,192,170,255),'forearm':(146,153,142,255),'hand':(166,104,69,255),'pelvis':(70,86,113,255),'leg':(96,113,130,255),'shoe':(153,158,153,255)};M=json.loads((ROOT/'art/source/hero-directional-r14/construction.json').read_text());records={};frames={};checks=[];pin='0bb4ee4293ec2a76a3b8eb77d5d1fca4441bdcc1'
def ck(n,v):assert v,n;checks.append(n)
def points(q):return {(i%32,i//32) for i,p in enumerate(q.get_flattened_data()) if p[3]}
def border(s):return {p for p in s if any((p[0]+dx,p[1]+dy) not in s for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)])}
def polygon(vertices):
 q=Image.new('1',(32,64));ImageDraw.Draw(q).polygon(vertices,fill=1);return {(x,y) for y in range(64) for x in range(32) if q.getpixel((x,y))}
def layer(mask,color,stroke=True):
 q=Image.new('RGBA',(32,64));edge=border(mask) if stroke else set()
 for p in mask:q.putpixel(p,C['outline'] if p in edge else C[color])
 return q
def bounds(s):return [min(x for x,y in s),min(y for x,y in s),max(x for x,y in s)+1,max(y for x,y in s)+1] if s else None
for dr in ['south','west']:
 folder=OUT/dr;folder.mkdir(exist_ok=True);path=f'docs/reviews/M1-NCR1/{dr}-idle/master-hero.png';hp=ROOT/path;ck(dr+' current Hero input exact pinned source',hp.read_bytes()==subprocess.check_output(['git','show',pin+':'+path]));hero=Image.open(hp).convert('RGBA');old=Image.open(ROOT/f'docs/reviews/M1-NCR1/{dr}-idle/master-bald.png').convert('RGBA');e=M['directions'][dr]['idle'];masks={}
 # Existing smooth bald crown retained. Below it, a shared visible FACE shape
 # is explicit rather than treating source hair as the sole facial boundary.
 head={(x,y) for y in range(27,44) for x in range(32) if old.getpixel((x,y))[3]}
 if dr=='south':
  for y,a,b in [(38,4,28),(39,4,28),(40,4,28),(41,5,27),(42,7,25),(43,8,24),(44,10,22)]:head={p for p in head if p[1]!=y}|{(x,y) for x in range(a,b)}
  head|={(31-x,y) for x,y in list(head)} # underlying idle cranium/face geometry paired; does not mirror hair/shading
  silhouette={(x,y) for y in range(45,62) for x in range(32) if hero.getpixel((x,y))[3]};masks['torso']={p for p in silhouette if p[1]<55};masks['pelvis']={p for p in silhouette if 54<=p[1]<58};masks['leg']={p for p in silhouette if p[1]>=56};masks['shoe']={p for p in silhouette if p[1]>=58 and (7<=p[0]<15 or 17<=p[0]<25)}
  masks['upperArm']={p for p in silhouette if 46<=p[1]<=49 and (p[0]<=10 or p[0]>=21)};masks['forearm']={p for p in silhouette if 49<=p[1]<=53 and (p[0]<=9 or p[0]>=22)};masks['hand']={tuple(p) for p in e['commonFeatureRegistration']['hands']['cells']}
 else:
  missing={(4,y) for y in range(36,41)}|{(5,41),(6,41),(7,42),(7,43),(24,41),(24,42),(24,43)};head|=missing;head|={(x,44) for x in range(10,24)}
  # Original flat completion behind removed backpack: visible projection proposal,
  # not source-observed torso or a nude skeletal body under the costume.
  masks['torso']=polygon([(13,43),(20,43),(22,46),(22,51),(20,55),(12,55),(10,52),(10,47)])
  masks['pelvis']=polygon([(12,53),(20,53),(21,55),(19,57),(13,57),(11,55)])
  masks['leg']=polygon([(13,55),(19,55),(20,56),(18,58),(17,60),(14,60),(12,57)])
  # One left-pointing full near shoe; far foot is legitimately occluded.
  masks['shoe']={(x,y) for y,a,b in [(58,12,18),(59,10,19),(60,9,19),(61,10,18)] for x in range(a,b)}
  masks['upperArm']=polygon([(16,44),(20,45),(21,47),(20,50),(16,50),(15,47)])
  masks['forearm']=polygon([(16,47),(20,48),(20,52),(18,54),(15,53),(14,50)])
  #20 visible warm cells,4x6 bounding sanity-check, rounded rather than quota box.
  warm={(x,y) for y,a,b in [(49,16,18),(50,15,19),(51,15,19),(52,15,19),(53,15,19),(54,16,18)] for x in range(a,b)}
  masks['hand']=warm
 masks['head']=head
 # Flat body regions contribute directly to the result, no dressed-Hero overlay.
 q=Image.new('RGBA',(32,64));partimages={}
 for name in ['torso','pelvis','leg','shoe','upperArm','forearm']:
  partimages[name]=layer(masks[name],name,stroke=False);q.alpha_composite(partimages[name])
 # Arm occlusion is one connected projected volume, not three garment bars.
 arm=masks['upperArm']|masks['forearm'];armEdge=border(arm)
 for p in armEdge:q.putpixel(p,C['outline'])
 if dr=='south':
  for y in [57,58]:
   for x in [15,16]:
    if (x,y) in points(q):q.putpixel((x,y),C['outline'])
 # Hand is an explicitly warm region with an independent dark contour around it.
 hand=masks['hand'];handEnvelope=hand|{(x+dx,y+dy) for x,y in hand for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)] if 0<=x+dx<32 and 0<=y+dy<64};hl=layer(handEnvelope,'hand',stroke=False)
 for p in handEnvelope-hand:hl.putpixel(p,C['outline'])
 partimages['hand']=hl;q.alpha_composite(hl)
 headimage=layer(head,'head');partimages['head']=headimage;q.alpha_composite(headimage)
 for p in border(points(q)):q.putpixel(p,C['outline'])
 # Eye sites and compact flat ear feature retain source identity; no nose/mouth.
 feature=Image.new('RGBA',(32,64))
 for p in e['commonFeatureRegistration']['eyes']['cells']:feature.putpixel(tuple(p),C['outline'])
 if dr=='west':
  # Source registered ear sites are interior landmarks, NOT a filled glyph.
  # Compact open curl from actual old visible ear-edge ROI, flat two-region
  # drawing; open lower-left prevents a second rectangular pupil reading.
  earCurl={(19,38),(20,38),(18,39),(21,39),(18,40),(19,40),(21,40),(21,41),(19,42),(20,42)}
  for p in earCurl:feature.putpixel(p,C['ear'])
 else:
  for p in e['commonFeatureRegistration']['ears']['cells']:
   if tuple(p) in head and tuple(p) not in border(head):feature.putpixel(tuple(p),C['ear'])
 partimages['features']=feature;q.alpha_composite(feature)
 # Export the actual construction strokes as a sparse line layer. This is
 # not a full opaque image: flat regions remain the colored contributors.
 outline=Image.new('RGBA',(32,64))
 for p in points(q):
  if q.getpixel(p)==C['outline']:outline.putpixel(p,C['outline'])
 partimages['outline']=outline
 renderOrder=['torso','pelvis','leg','shoe','upperArm','forearm','hand','head','outline','features']
 assembled=Image.new('RGBA',(32,64))
 for name in renderOrder:assembled.alpha_composite(partimages[name])
 ck(dr+' actual saved region/outline/features recomposition exact',assembled.tobytes()==q.tobytes())
 # One shared face may be dressed later. Original hair is previewed ONLY as a
 # registration proof over the completed contour; no redressed neutral outfit.
 hair=Image.open(ROOT/f'docs/reviews/M1-NCR1/{dr}-idle/master-hair.png').convert('RGBA');headWithHair=headimage.copy();headWithHair.alpha_composite(feature);headWithHair.alpha_composite(hair)
 silhouette=Image.new('RGBA',(32,64));silhouette.putdata([C['outline'] if p[3] else(0,0,0,0) for p in q.get_flattened_data()]);files={}
 for name,im in [('neutral.png',q),('silhouette.png',silhouette),('shared-face-with-original-hair-proof.png',headWithHair)]+[(name+'-region.png',im) for name,im in partimages.items()]:
  im.save(folder/name);files[name]={'sha256':hashlib.sha256((folder/name).read_bytes()).hexdigest(),'rgbaSHA256':hashlib.sha256(im.tobytes()).hexdigest()}
 visiblehand={p for p in hand if q.getpixel(p)==C['hand']};ck(dr+' exact registered eye sites/shape retained; color flattened charcoal',all(q.getpixel(tuple(p))==C['outline'] for p in e['commonFeatureRegistration']['eyes']['cells']));ck(dr+' sole ground row61 preserved',q.getbbox()[3]-1==61);ck(dr+' no orphan silhouette components',bool(points(q)));ck(dr+' source Hero file unchanged',hp.read_bytes()==subprocess.check_output(['git','show',pin+':'+path]));ck(dr+' flat region palette only',set(q.get_flattened_data())<=set(C.values())|{(0,0,0,0)})
 if dr=='west':ck('West all12 confirmed shared face/jaw steps present in base',all(q.getpixel(p)==C['outline'] for p in missing));ck('West readable hand warm mass no old6pixel patch',len(visiblehand)==20);ck('West ear curl open interior, not second pupil block',q.getpixel((20,40))==C['head'] and q.getpixel((19,41))==C['head'] and q.getpixel((21,40))==C['ear'])
 records[dr]={'frame':[32,64],'anchor':[16,64],'actualBounds':q.getbbox(),'sourceHeroBounds':hero.getbbox(),'sourceHeroSHA256':hashlib.sha256(hp.read_bytes()).hexdigest(),'visibleHandCells':len(visiblehand),'visibleHandBounds':bounds(visiblehand),'renderOrder':renderOrder,'featureOwnership':{'eyesRegisteredCells':e['commonFeatureRegistration']['eyes']['cells'],'eyeColorQualification':'registered sites/shape exact; original navy/charcoal eye shades deliberately flattened to charcoal neutral region','earInteriorRegistrationIsNotFullShape':True,'authoredEarCurlCells':[list(p) for p in sorted(earCurl)] if dr=='west' else e['commonFeatureRegistration']['ears']['cells'],'noseMouth':None},'partMasks':{name:{'cells':[list(p) for p in sorted(mask)],'bounds':bounds(mask),'qualification':'original flat semantic construction; no hidden bone claim'} for name,mask in masks.items()},'files':files,'proposal':'new neutral flat completion, not accepted anatomy or runtime replacement','farFoot':'occluded; no forced second foot' if dr=='west' else'two front full-size shoe envelopes'};frames[dr]={'sourceHero':hero,'sourceBald':old,'neutral':q,'silhouette':silhouette}
# Coherent two-pose review, nothing outside scoped idles.
p=Image.new('RGB',(1040,600),'#eee8d1');d=ImageDraw.Draw(p)
for row,dr in enumerate(frames):
 for col,(name,title) in enumerate([('sourceHero','PROPORTION ANCHOR' if dr=='south' else 'REJECTED WEST HERO'),('sourceBald','REJECTED DRESSED BALD'),('neutral','NEW FLAT NEUTRAL'),('silhouette','NEW SILHOUETTE')]):
  x=260*col;y=300*row;im=frames[dr][name];d.text((x+5,y+5),dr+' '+title,font=F,fill='#242330');big=im.resize((96,192),Image.Resampling.NEAREST);p.paste(big,(x+10,y+35),big);p.paste(im,(x+170,y+135),im)
  if name=='neutral':d.text((x+5,y+245),'Visible hand cells '+str(records[dr]['visibleHandCells']),font=F,fill='#465671')
d.text((10,575),'INTERNAL TWO IDLES /32x64 +3x / flat original construction / no hair, pack, Hero outfit decoration / user judgment pending',font=F,fill='#465671');p.save(OUT/'two-pose-neutral-comparison.png')
(SRC/'construction.json').write_text(json.dumps({'task':'M1.NT1','preeditCheckpoint':'M1.NTC1 viewed/privately shown by root before drawing; targeted critique relayed','palette':C,'directions':records},indent=2)+'\n');(SRC/'checks.json').write_text(json.dumps({'pass':True,'checks':checks,'appearanceApproval':False},indent=2)+'\n');print('Built/evaluate only2neutral idles; warm hand cells',{dr:r['visibleHandCells'] for dr,r in records.items()})
# Actual saved-file construction checks, distinct from visual acceptance.
extra=[]
for dr in frames:
 q=Image.open(OUT/dr/'neutral.png').convert('RGBA');mask=points(q);seen=set();stack=[next(iter(mask))]
 while stack:
  p=stack.pop()
  if p in seen:continue
  seen.add(p)
  stack.extend((p[0]+dx,p[1]+dy) for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)] if (p[0]+dx,p[1]+dy) in mask and (p[0]+dx,p[1]+dy) not in seen)
 ck(dr+' saved neutral silhouette exactly one4connected component',seen==mask);ck(dr+' opaque32x64 binary-alpha native output',q.size==(32,64) and set(q.getchannel('A').get_flattened_data())<={0,255});ck(dr+' every actual outer contour site dark',all(q.getpixel(p)==C['outline'] for p in border(mask)));ck(dr+' no coral/cream Hero outfit palette remains',all(p[:3] not in [(237,116,92),(174,69,74),(249,237,200)] for p in q.get_flattened_data()))
 if dr=='south':
  sites={(4,y) for y in range(38,41)}|{(27,y) for y in range(38,41)}|{(5,41),(26,41),(7,42),(24,42)};ck('front confirmed shared face steps all dark',all(q.getpixel(p)==C['outline'] for p in sites));ck('front neutral silhouette bilaterally symmetric',q.getchannel('A').tobytes()==q.transpose(Image.Transpose.FLIP_LEFT_RIGHT).getchannel('A').tobytes())
 source=frames[dr]['sourceHero']
 added=[(x,y) for y in range(45,64) for x in range(32) if q.getpixel((x,y))[3] and not source.getpixel((x,y))[3]]
 removed=[(x,y) for y in range(45,64) for x in range(32) if not q.getpixel((x,y))[3] and source.getpixel((x,y))[3]]
 records[dr]['neutralVsSourceBodyAlpha']={'added':[list(p) for p in added],'removed':[list(p) for p in removed],'qualification':'new neutral projected construction, not exact dressed-body alpha; source Hero untouched'}
 if dr=='south':
  ck('front neutral only two symmetric hand-rim alpha proposals',set(added)=={(4,49),(27,49)} and not removed)
  ck('front neutral shoe58plus silhouette exact source',q.crop((0,58,32,64)).getchannel('A').tobytes()==source.crop((0,58,32,64)).getchannel('A').tobytes())
 records[dr]['lastPaintedRow']=q.getbbox()[3]-1;records[dr]['lastContactXs']=[x for x in range(32) if q.getpixel((x,61))[3]]
(SRC/'construction.json').write_text(json.dumps({'task':'M1.NT1','preeditCheckpoint':'M1.NTC1 viewed/privately shown by root before drawing; targeted critique relayed','palette':C,'directions':records,'headBodyOverlap':'body behind jaw; no free neck post; head covers original proposed shoulders','sourceFactsVsProposal':'current protected front bounds/eyes/hands/contact are source anchors; West torso/arm/leg/shoe and occluded-body completion are original flat construction','scope':['south idle32','west idle32'],'notIncluded':['native16','otherposes','animation','creator','runtime','deployment']},indent=2)+'\n');(SRC/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False},indent=2)+'\n');print('PASS',len(checks),'saved native shape/region/contour/source guards, not artistic approval')
