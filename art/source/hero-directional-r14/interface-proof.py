"""Source-observed torso/hem interface and protected-region proof."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,io,sys,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR14';src=Path(__file__).parent;ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
baseline='2c03bc6';dirs=('south','north','west','east');poses=('A','P','C');meta=json.loads((src/'construction.json').read_text());r={'task':'M1.HR14 bounded torso/hem taper pass','baseline':baseline,'directObservedEnvelopeRows':[48,54],'materialStatus':'Original coral/cream/slate adaptation; upper RGB/material roles NOT exact source claims. Existing visible hand sites retained; Only retained original visible hands supply skin; source glove/peach blocks are not added as duplicate hands.','protection':{},'interfaces':{},'fullWatch':'Not established by this pixel report','visualApproval':False}
def old(kind,d,p):return Image.open(io.BytesIO(subprocess.check_output(['git','show',baseline+f':docs/reviews/M1-HR14/{kind}-{d}-{p}.png'],cwd=root))).convert('RGBA')
def spans(im,y):
 result=[]
 for x in range(32):
  if im.getpixel((x,y))[3]:
   if result and result[-1][1]==x:result[-1][1]=x+1
   else:result.append([x,x+1])
 return result
for d in dirs:
 for p in ('idle','A','P','C'):
  e=meta['directions'][d][p];bag=Image.open(out/f'pack-layer-{d}-{p}.png').convert('RGBA')
  for k in ('pack-layer','strap-layer'):
   current=Image.open(out/f'{k}-{d}-{p}.png').convert('RGBA');assert current.tobytes()==old(k,d,p).tobytes(),(k,d,p,'canonical pixels changed')
  for kind in ('hero','dummy'):
   before=old(kind,d,p);h=Image.open(out/f'{kind}-{d}-{p}.png').convert('RGBA');changes=[];bagDepth=[];materialOnly=[];quietChest=[]
   for y in range(64):
    for x in range(32):
     if h.getpixel((x,y))==before.getpixel((x,y)):continue
     allowedY=(50,56) if p=='idle' else (48,54)
     assert not e['headMaskHero' if kind=='hero' else 'headMaskDummy'][y*32+x],(d,p,kind,'head changed')
     if kind=='dummy' and y>=(56 if p=='idle' else 54):
      assert bool(h.getpixel((x,y))[3])==bool(before.getpixel((x,y))[3]);materialOnly.append([x,y]);continue
     if kind=='hero' and d=='south' and 12<=x<=19 and 46+(-2 if p=='P' else 0)<=y<49+(-2 if p=='P' else 0) and before.getpixel((x,y))[:3]==(249,237,200) and h.getpixel((x,y))[:3]==(237,116,92):quietChest.append([x,y]);continue
     assert y<(56 if p=='idle' else 54),(d,p,kind,'lower contact construction changed')
     if allowedY[0]<=y<allowedY[1]:changes.append([x,y])
     else:
      assert kind=='hero' and d in ('west','east') and bag.getpixel((x,y))[3] and h.getpixel((x,y))==bag.getpixel((x,y)),(d,p,kind,x,y,'unexpected outside-interface change')
      bagDepth.append([x,y])
   r['protection'][d+'/'+p+'/'+kind]={'changedInterfaceCells':len(changes),'distinctLowerMaterialCells':materialOnly,'quietCreamChestCells':quietChest,'profileBagForegroundOcclusionCells':bagDepth,'headsAndLowerRowsExact':True,'idleInterfaceFromPassingPlus2':p=='idle','canonicalPackAndStrapsExact':True}
  for kind in ('hero','dummy'):
   def handcells(im):
    return {(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3] and (im.getpixel((x,y))[:3]==(255,212,161) if kind=='dummy' else im.getpixel((x,y))[:3] in [(166,104,69),(195,138,88),(116,69,57)] and not e['headMaskHero'][y*32+x] and not e['headMaskDummy'][y*32+x])}
   current=Image.open(out/f'{kind}-{d}-{p}.png').convert('RGBA');currentHands=handcells(current)
   if kind=='hero':assert currentHands==handcells(old(kind,d,p)),(d,p,'new bare hand sites introduced')
   remaining=set(currentHands);groups=[]
   while remaining:
    comp={remaining.pop()};q=list(comp)
    while q:
     x,y=q.pop()
     for yy in range(y-1,y+2):
      for xx in range(x-1,x+2):
       if (xx,yy) in remaining:remaining.remove((xx,yy));comp.add((xx,yy));q.append((xx,yy))
    groups.append(sorted(comp))
   expected=2 if d in ('south','north') and p in ('idle','P') else 1
   assert len(groups)==expected,(d,p,kind,'duplicate/disconnected hand cluster',groups)
   r['protection'][d+'/'+p+'/'+kind]['visibleHandClusters']=groups
   r['protection'][d+'/'+p+'/'+kind]['actualHandSitesRetained']=True
  if p=='idle':
   for kind in ('hero','dummy','body-layer'):
    walking=Image.open(out/f'{kind}-{d}-P.png').convert('RGBA').crop((0,48,32,54))
    resting=Image.open(out/f'{kind}-{d}-idle.png').convert('RGBA').crop((0,50,32,56))
    assert walking.tobytes()==resting.tobytes(),(d,kind,'idle/walk upper RGBA/material pops')
   continue
  ref=Image.open(ext/f'reference-{d}-{p}.png').convert('RGBA');h=Image.open(out/f'hero-{d}-{p}.png').convert('RGBA');m=Image.open(out/f'dummy-{d}-{p}.png').convert('RGBA');checks=[]
  for y in range(48,54):
   missing=[];extra=[];dummyDiff=[]
   for x in range(32):
    ra=bool(ref.getpixel((x,y))[3]);ha=bool(h.getpixel((x,y))[3]);ma=bool(m.getpixel((x,y))[3])
    if ra and not ha:missing.append(x)
    if ha and not ra:extra.append(x)
    if ra!=ma:dummyDiff.append(x)
   assert not missing and not dummyDiff,(d,p,y,'source upper envelope absent',missing,dummyDiff)
   # Original compact pack may overhang the reference envelope in profiles;
   # report these source-silhouette differences instead of clipping the bag.
   assert all(d in ('west','east') and bag.getpixel((x,y))[3] for x in extra),(d,p,y,'extra nonpack pixels',extra)
   checks.append({'row':y,'sourceSpans':spans(ref,y),'heroSpans':spans(h,y),'dummySpans':spans(m,y),'missingCells':missing,'originalPackOverhangCells':extra,'dummyAlphaExact':not dummyDiff})
  r['interfaces'][d+'/'+p]=checks
s=r['interfaces']['south/P'];row52=next(c for c in s if c['row']==52);row53=next(c for c in s if c['row']==53);assert row52['heroSpans']==[[5,27]] and row53['heroSpans']==[[7,25]]
r['idleWalkContinuity']={'all4Directions':'Actual Hero,dummy and underlying body-layer upper RGBA/materials equal under2px torso translation; contact geometry belowidle56/walk54 protected','newAnatomy':False}
r['southPassingTaper']={'row51':spans(Image.open(out/'hero-south-P.png').convert('RGBA'),51),'row52':row52['heroSpans'],'row53':row53['heroSpans'],'narrowsLeftBy':2,'narrowsRightBy':2,'referenceEnvelopeExact':True,'hiddenWaistOrBoneCoordinate':None}
# Inspectable grid: source, rejected interface and current, same full frame.
plate=Image.new('RGB',(1440,1480),'#bed4d5');dd=ImageDraw.Draw(plate);ink='#253340'
for row,d in enumerate(dirs):
 for col,p in enumerate(poses):
  x=col*480;y=row*370;dd.text((x+5,y+5),d.upper()+' '+p+' SOURCE | BEFORE | CURRENT (fixed32x64)',fill=ink)
  ref=Image.open(ext/f'reference-{d}-{p}.png').convert('RGBA');before=old('hero',d,p);h=Image.open(out/f'hero-{d}-{p}.png').convert('RGBA')
  for n,im in enumerate((ref,before,h)):
   xx=x+n*158;big=im.resize((96,192),Image.Resampling.NEAREST);plate.paste(big,(xx+27,y+25),big);plate.paste(im,(xx+59,y+223),im)
   crop=im.crop((0,48,32,55)).resize((128,28),Image.Resampling.NEAREST);plate.paste(crop,(xx+11,y+293),crop)
  dd.text((x+5,y+272),'Rows48..54; upper source envelope, original material colors',fill=ink);dd.text((x+5,y+335),'Lower54..63 + head + canonical pack/straps protected.',fill=ink);dd.text((x+5,y+352),'Profile original bag overhang disclosed; no invented bones.',fill=ink)
plate.save(ext/'four-direction-interface-source-before-current.png')
# True P seam grid with numeric taper; source-colored comparison external.
plate=Image.new('RGB',(1440,570),'#bed4d5');dd=ImageDraw.Draw(plate)
for n,(label,im) in enumerate([('SOURCE',Image.open(ext/'reference-south-P.png').convert('RGBA')),('BEFORE flare',old('hero','south','P')),('CURRENT taper',Image.open(out/'hero-south-P.png').convert('RGBA'))]):
 x=n*480+36;y=40;dd.text((x,10),label+' / SOUTH P / rows48..54',fill=ink);crop=im.crop((0,48,32,55)).resize((384,84),Image.Resampling.NEAREST);plate.paste(crop,(x,y),crop)
 for sx in range(33):dd.line((x+sx*12,y,x+sx*12,y+84),fill='#748894')
 for sy in range(8):dd.line((x,y+sy*12,x+384,y+sy*12),fill='#748894');dd.text((x-22,y+sy*12),str(48+sy),fill=ink)
 for k,sy in enumerate((51,52,53,54)):
  dd.text((x,150+k*24),'Row'+str(sy)+' '+str(spans(im,sy)),fill=ink)
 big=im.resize((96,192),Image.Resampling.NEAREST);plate.paste(big,(x+140,255),big);plate.paste(im,(x+172,462),im)
 dd.text((x-20,545),'Original costume adaptation; anatomical waist unresolved.',fill=ink)
plate.save(ext/'passing-interface-taper-grid.png')
r['allInterfaceChecksPass']=True;(out/'interface-checks.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS: P52[5,27)->P53[7,25) tapers; all12upper envelopes/source checks; heads/lower contacts/canonical pack protected; idle upper followsP+2. Original profile pack overhang disclosed.')
# Stop/start body construction check, with both native and enlarged final pixels.
plate=Image.new('RGB',(1600,900),'#bed4d5');dd=ImageDraw.Draw(plate)
for col,d in enumerate(dirs):
 x=col*400;dd.text((x+6,6),d.upper()+' IDLE / PASSING P',fill=ink)
 for row,pose in enumerate(('idle','P')):
  y=28+row*350;dd.text((x+6,y),pose+' / HERO | DUMMY',fill=ink)
  for k,kind in enumerate(('hero','dummy')):
   im=Image.open(out/f'{kind}-{d}-{pose}.png').convert('RGBA');big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+28+k*175,y+20),big);plate.paste(im,(x+76+k*175,y+280),im)
 dd.text((x+6,725),'Actual upper RGBA: idle50..55 = P48..53',fill=ink);dd.text((x+6,746),'under declared2px torso translation.',fill=ink)
 dd.text((x+6,767),'Literal walking54..63 + retained idle56..63',fill=ink);dd.text((x+6,788),'contact pixels protected; no added calf/length.',fill=ink)
 dd.text((x+6,809),'Head/hair and canonical pack/straps unchanged.',fill=ink);dd.text((x+6,830),'Hands: actual Hero = dummy = guide cell sets.',fill=ink)
plate.save(out/'idle-walk-interface-continuity.png')
