"""NTC1 PRE-EDIT comparison/measurement ONLY. Never writes character pixels.
Reference-bearing plates are external to repository/build.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[3];SRC=Path(__file__).parent;OUT=ROOT/'docs/reviews/M1-NTC1';EXT=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/neutral-template-preedit');EXT.mkdir(parents=True,exist_ok=True);F=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
M=json.loads((ROOT/'art/source/hero-directional-r14/construction.json').read_text());records={};images={};primary={};pin='0bb4ee4293ec2a76a3b8eb77d5d1fca4441bdcc1';inputs={}
def bb(p):return [min(x for x,y in p),min(y for x,y in p),max(x for x,y in p)+1,max(y for x,y in p)+1] if p else None
def describe(p):return {'cells':len(p),'boundsHalfOpen':bb(p),'coordinates':[list(v) for v in p]}
def runs(q,y):
 out=[]
 for x in range(q.width):
  if q.getpixel((x,y))[3]:
   if out and out[-1][1]==x:out[-1][1]+=1
   else:out.append([x,x+1])
 return out
for dr in ['south','west']:
 e=M['directions'][dr]['idle'];imgs={}
 for kind in ['hero','bald']:
  name=f'docs/reviews/M1-NCR1/{dr}-idle/master-{kind}.png';p=ROOT/name;assert p.read_bytes()==subprocess.check_output(['git','show',pin+':'+name]);inputs[name]=hashlib.sha256(p.read_bytes()).hexdigest();imgs[kind]=Image.open(p).convert('RGBA')
 b=imgs['bald'];h=imgs['hero'];occupied={(x,y) for y in range(64) for x in range(32) if b.getpixel((x,y))[3]};edge={p for p in occupied if 27<=p[1]<45 and any((p[0]+dx,p[1]+dy) not in occupied for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)])};light=sorted(p for p in edge if b.getpixel(p)[:3] in [(166,104,69),(195,138,88)])
 features={k:describe([tuple(p) for p in e['commonFeatureRegistration'][k]['cells']]) for k in ['eyes','ears','hands']};hands=[tuple(p) for p in e['commonFeatureRegistration']['hands']['cells']];features['hands']['leftOfFrameCenter']=describe([p for p in hands if p[0]<16]);features['hands']['rightOfFrameCenter']=describe([p for p in hands if p[0]>=16]);features['hands']['definition']='actual source-registered visible exposed hand skin, not full arm or hidden joints';regions={}
 for y in [45,46,48,49,50,51,52,53,54,55,56,58,59,60,61]:regions[str(y)]=runs(b,y)
 records[dr]={'frame':[32,64],'edgeAnchor':[16,64],'heroBounds':h.getbbox(),'baldBounds':b.getbbox(),'headHeroAuthoredMask':describe([(i%32,i//32) for i,on in enumerate(e['headMaskHero']) if on]),'headBaldAuthoredMask':describe([(i%32,i//32) for i,on in enumerate(e['headMaskDummy']) if on]),'headMaskQualification':'existing authored head envelope includes appearance/projection; not measured hidden skull anatomy','registeredFeatures':features,'actualBaldHeadExteriorLightMidSkin':describe(light),'exteriorDefinition':'actual full-alpha4neighbor exterior restricted to source rows27..44; colored-edge sites are marked for critique, not automatically labelled missing bones','occupiedRowRuns':regions,'torsoRegistration':e['torsoAnchor'],'canonicalPackTorsoLocalRegistration':e['canonicalPackAnchor'],'lastPaintedRow':h.getbbox()[3]-1,'lastPaintedSpans':runs(h,h.getbbox()[3]-1),'hiddenShoulderElbowHipKneeAnkle':None};images[dr]=imgs
for name in ['brendan-walking.png','man_1.png']:
 path=Path('/tmp/ds1-primary-reference')/name;q=Image.open(path);pal=q.getpalette();info={'revision':'731ad5bfd6e6f265508d0efcca0ba42f9dcf5881','sourceFileSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'sheetSize':q.size,'method':'indexed PNG; index0 excluded; source inspection, not emulator observation','frames':{}}
 for dr,idx in [('south',0),('west',2)]:
  im=Image.new('RGBA',(16,32))
  for y in range(32):
   for x in range(16):
    i=q.getpixel((idx*16+x,y));im.putpixel((x,y),tuple(pal[3*i:3*i+3])+(255,) if i else (0,0,0,0))
  data={'index':idx,'frame':[16,32],'occupiedBounds':im.getbbox(),'edgeAnchor':[8,32],'lastPaintedRow':im.getbbox()[3]-1,'lastPaintedSpans':runs(im,im.getbbox()[3]-1),'twiceFrame':[32,64],'twiceOccupiedBounds':[2*v for v in im.getbbox()],'twiceContactRowPair':[2*(im.getbbox()[3]-1),2*(im.getbbox()[3]-1)+1]}
  if name=='brendan-walking.png':
   eye=[(x,y) for x in ([6,9] if dr=='south' else [5]) for y in [19,20]];assert all(q.getpixel((idx*16+x,y))==8 for x,y in eye);data['manuallyAnnotatedVisiblePupil']=describe(eye);data['pupilInterpretation']='visible dark-blue pupil cells manually identified in face, exact indexed values checked; no hidden skull segmentation'
   if dr=='west':
    patch=[(x,y) for y in [25,26] for x in [7,8]];assert all(q.getpixel((idx*16+x,y)) in [12,13] for x,y in patch);data['visibleRedNearLimbCostumePatch']=describe(patch);data['patchQualification']='manual visible gloved/near-limb costume-patch annotation, not a complete measured anatomical hand';data['twicePatchArea']=len(patch)*4;data['twicePatchBounds']=[14,50,18,54]
  elif dr=='west':
   patch=[(x,y) for y in [24,25,26] for x in [7,8]];assert all(q.getpixel((idx*16+x,y)) in [1,2,3] for x,y in patch);data['visibleNearLimbWarmSkinPatch']=describe(patch);data['patchQualification']='adult Man1 source-visible warm near-limb patch; contextual reference, not mandatory child hand budget';data['twicePatchArea']=len(patch)*4;data['twicePatchBounds']=[14,48,18,54]
  info['frames'][dr]=data;images[dr][name]=im
 primary[name]=info
# Exact whole-frame alignment. Reference6x versus current3x gives96x192.
p=Image.new('RGB',(1080,650),'#eee8d1');d=ImageDraw.Draw(p)
for row,dr in enumerate(['south','west']):
 y=row*300+35
 for col,(key,title) in enumerate([('brendan-walking.png','PRIMARY BRENDAN'),('man_1.png','PRIMARY MAN1 / ADULT'),('hero','PROTECTED FRONT' if dr=='south' else 'CURRENT WEST HERO'),('bald','CURRENT BALD / REJECTED')]):
  x=col*270;q=images[dr][key];scale=6 if q.width==16 else 3;d.text((x+6,y),dr.upper()+' '+title,font=F,fill='#242330');d.text((x+6,y+17),('native16x32 / display6x' if q.width==16 else 'native32x64 / display3x'),font=F,fill='#465671');big=q.resize((q.width*scale,q.height*scale),Image.Resampling.NEAREST);p.paste(big,(x+15,y+40),big);p.paste(q,(x+165,y+135),q);d.line((x+10,y+232,x+125,y+232),fill='#887c65')
  text='Source0 / hat is NOT skull' if q.width==16 and dr=='south' else 'Source2 / joints unresolved' if q.width==16 else 'eyes38..41 / contact61'
  d.text((x+6,y+246),text,font=F,fill='#465671')
d.text((8,4),'NTC1 PRE-EDIT: whole frames/edge anchors aligned; exact pixels, no part fitting or artwork changes.',font=F,fill='#242330');d.text((8,627),'Reference pixels external only / current South exact0bb4ee4 / source facts differ from proposed mannequin construction.',font=F,fill='#465671');p.save(EXT/'reference-current-front-west.png')
# Current-pixel diagnostic: no neutral-template/new character drawing.
p=Image.new('RGB',(1040,650),'#eee8d1');d=ImageDraw.Draw(p)
for row,dr in enumerate(['south','west']):
 for col,kind in enumerate(['hero','bald']):
  x=col*350;y=row*300;q=images[dr][kind];big=q.resize((128,256),Image.Resampling.NEAREST);p.paste(big,(x+25,y+25),big);d.text((x+5,y+5),dr+' '+kind+' / exact4x',font=F,fill='#242330')
  e=records[dr]['registeredFeatures']
  for title,key,color in [('EYE','eyes','#6699bb'),('HAND','hands','#6aaf55')]:
   bounds=[e[key]['boundsHalfOpen']]
   if key=='hands' and dr=='south':bounds=[e[key]['leftOfFrameCenter']['boundsHalfOpen'],e[key]['rightOfFrameCenter']['boundsHalfOpen']]
   for bound in bounds:
    if bound:
     a,b0,c,e0=bound;d.rectangle((x+25+a*4,y+25+b0*4,x+25+c*4-1,y+25+e0*4-1),outline=color,width=1)
  if kind=='bald':
   for xx,yy in records[dr]['actualBaldHeadExteriorLightMidSkin']['coordinates']:d.rectangle((x+25+xx*4,y+25+yy*4,x+25+xx*4+3,y+25+yy*4+3),outline='#d13990',width=1)
 y=row*300;d.text((710,y+35),'Eyes: blue box',font=F,fill='#465671');d.text((710,y+55),'Registered hand: green box',font=F,fill='#465671');d.text((710,y+75),'Light/mid skin exterior: magenta',font=F,fill='#465671');d.text((710,y+110),('Front each hand17 /5x5' if dr=='south' else 'West hand6 /2x3'),font=F,fill='#242330');d.text((710,y+130),'VISIBLE regions, not bones',font=F,fill='#242330')
d.text((10,620),'Review overlays only. Existing character pixels untouched. Full face outline/neutral body require parent critique before drawing.',font=F,fill='#465671');p.save(EXT/'current-feature-and-contour-diagnostic.png')
result={'task':'M1.NTC1','state':'PRE-EDIT comparison only, rejected NCR1 not appearance-ready','sourceMasterCommit':pin,'inputs':inputs,'current':records,'primary':primary,'externalPlates':[str(EXT/'reference-current-front-west.png'),str(EXT/'current-feature-and-contour-diagnostic.png')],'referenceFacts':'source frame/index/palette/bounds/selected visible patches; no bone/skull observation','originalProposals':{'neutralTemplate':'flat-region intended body/hand/shoe envelope without hair/costume decoration/pack; no pixels authored yet','packRemoval':'requires explicitly proposed flat body completion in occluded region, not source-observed anatomy','WestArm':'restore readable shoulder/forearm/hand volume against protected front17cell/5x5 visible hand, not defend current6cell/2x3 by metadata equality','faceContour':'complete independent profile contour wherever hair supplied its edge; parent critique pending','numericHandQuota':'unapproved; source red patch16scaled cells/adultwarm patch24scaled cells are comparisons, not mandatory exact child hand anatomy'},'drawingAuthorizedNow':False,'next':'send exact plate/numeric findings to root; HOLD sprite drawing until exact comparison shown/relayed and targeted critique returned'}
(OUT/'landmark-comparison.json').write_text(json.dumps(result,indent=2)+'\n');print('Created external pre-edit plates and numeric landmark comparison. NO sprite edits.')
# Targeted parent critique: mark exact missing FACE contour, not scalp/hair.
missing=[(4,y) for y in range(36,41)]+[(5,41),(6,41),(7,42),(7,43)];h=images['west']['hero'];b=images['west']['bald'];assert all(h.getpixel(p)==(36,35,48,255) and b.getpixel(p)[3]==0 for p in missing)
face=Image.new('RGB',(1050,450),'#eee8d1');d=ImageDraw.Draw(face)
for col,kind in enumerate(['hero','bald']):
 x=col*360+30;y=55;q=images['west'][kind].crop((2,32,27,46)).resize((250,140),Image.Resampling.NEAREST);face.paste(q,(x,y),q);d.text((x,10),'CURRENT WEST '+kind.upper()+' / exact10x face crop',font=F,fill='#242330')
 for xx in range(26):d.line((x+xx*10,y,x+xx*10,y+140),fill='#b7ae98')
 for yy in range(15):d.line((x,y+yy*10,x+250,y+yy*10),fill='#b7ae98')
 for xx,yy in missing:d.rectangle((x+(xx-2)*10,y+(yy-32)*10,x+(xx-2)*10+9,y+(yy-32)*10+9),outline='#d13990',width=2)
 d.text((x,215),'Magenta: SAME9registered face sites',font=F,fill='#465671');d.text((x,235),('Hero has charcoal at every site' if kind=='hero' else 'Bald has alpha0 at every site'),font=F,fill='#242330')
d.text((745,55),'Source coords top-down',font=F,fill='#242330')
for i,p in enumerate(missing):d.text((745,80+20*i),str(p),font=F,fill='#242330')
d.text((20,290),'Visible FACE steps: x4 rows36..40; cheek/jaw(5,41),(6,41),(7,42),(7,43).',font=F,fill='#242330');d.text((20,315),'Restore one shared face beneath hair; do not darken x5skin and shrink it further.',font=F,fill='#242330');d.text((20,340),'This is an exact comparison overlay, NOT a sprite correction or hidden scalp/bone reconstruction.',font=F,fill='#465671');face.save(EXT/'nine-missing-shared-face-sites.png')
result['externalPlates'].append(str(EXT/'nine-missing-shared-face-sites.png'));result['targetedParentCritique']={'exactMissingSharedFaceContour':missing,'actualHeroColor':'#242330','actualBaldAlphaAtSites':0,'parentPlateMapping':{'originY':555,'integerScale':3,'faceSourceRows':[36,40],'cheekJawSourceRows':[41,43]},'armSanityCheck':'Man1 visible2x3 native patch becomes4x6 at32; not a rigid mask/complete arm/bone measurement','lowerConstruction':'coherent hip/thigh,tapered ankle,left-pointing near shoe, front-derived full shoe size; far foot may occlude; old bad wedge alpha editable','neutralFirst':True};result['originalProposals']['WestArm']='connected shoulder/sleeve/forearm/hand near hip, front17-cell5x5 anchor; 4x6 reference-scaled sanity check only';result['originalProposals']['faceContour']='one shared contour includes nine actually absent charcoal source sites; not separately thickened outlines';result['originalProposals']['lowerConstruction']='scoped West shape correction permitted; left-pointing near shoe/front full size; far-foot occlusion valid; no isolated highlights before silhouette';(OUT/'landmark-comparison.json').write_text(json.dumps(result,indent=2)+'\n');print('Verified/marked all9actually missing shared face sites. Drawing still held.')
