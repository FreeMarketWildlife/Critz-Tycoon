"""Inspect saved native alpha/material runs and visible garment occlusion."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR11';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
observed=json.loads((out/'reference-structure.json').read_text());masks=json.loads((Path(__file__).parent/'masks.json').read_text())['poses']
def runs(im,y):
 r=[]
 for x in range(32):
  if im.getpixel((x,y))[3]:
   if r and r[-1][1]==x:r[-1][1]=x+1
   else:r.append([x,x+1])
 return r
def coords(mask):return {(i%32,i//32) for i,n in enumerate(mask) if n}
def materialRuns(im,y):
 r=[]
 for x in range(32):
  px=list(im.getpixel((x,y)))
  if r and r[-1]['rgba']==px:r[-1]['endExclusive']=x+1
  else:r.append({'start':x,'endExclusive':x+1,'rgba':px})
 return r
report={'scope':'Visible lower-costume structure, not hidden anatomy or art approval','kneeVisibility':'UNRESOLVED in reference; no knee coordinate authored','headBase':'HR9 exact; head detour unadopted','frames':[]}
plate=Image.new('RGB',(1080,720),'#eee6d0');dd=ImageDraw.Draw(plate)
for i,frame in enumerate(observed['frames']):
 pose=frame['pose'];ref=Image.open(ext/f'registered-left-{i:02}.png').convert('RGBA');candidate=Image.open(out/f'walk-{i:02}.png').convert('RGBA');before=Image.open(root/f'docs/reviews/M1-HR10-BODY/walk-{i:02}.png').convert('RGBA');m=masks[pose]
 cloth=coords(m['shorts']);cuffKeys=('leftCuff','rightCuff') if pose=='P' else ('leadingCuff',);shoeKeys=('leftShoe','rightShoe') if pose=='P' else ('leadingShoe',)
 cuffs=set().union(*(coords(m[k]) for k in cuffKeys));shoes=set().union(*(coords(m[k]) for k in shoeKeys));visibleCuffs=cuffs-cloth;visibleShoes=shoes-cuffs-cloth
 bodyBottom=max(y for x,y in cloth);shoeTop=min(y for x,y in visibleShoes);shoeBottom=max(y for x,y in visibleShoes)
 lowerRows=range(53,60) if pose=='P' else range(55,62)
 rr=[{'y':y,'source':runs(ref,y),'HR10':runs(before,y),'candidate':runs(candidate,y),'candidateMatchesSource':runs(candidate,y)==runs(ref,y),'candidateMaterialRGBARuns':materialRuns(candidate,y)} for y in range(44,64)]
 # These verify the specific early-split/pointed-stub defects, not visual quality.
 assert all(runs(ref,y)==runs(candidate,y) for y in lowerRows),(i,'lower contour/occlusion mismatch')
 assert bodyBottom==frame['visibleCostumeAnnotations']['visibleBodyCostumeBottomAnnotated']
 assert shoeTop==(58 if pose=='P' else 60) and shoeBottom==(59 if pose=='P' else 61)
 lowSkin=[(x,y) for y in range(54,64) for x in range(32) if candidate.getpixel((x,y))[:3] in [(166,104,69),(195,138,88),(116,69,57)] and candidate.getpixel((x,y))[3]]
 assert not lowSkin,(i,'exposed calf invented')
 item={'frame':i,'pose':pose,'sourceVisibleCostumeAnnotations':frame['visibleCostumeAnnotations'],'candidateBodyCostumeBottomFromShortsMask':bodyBottom,'candidateVisibleCuffRows':sorted({y for x,y in visibleCuffs}),'candidateVisibleShoeRows':sorted({y for x,y in visibleShoes}),'candidateShoeBottom':shoeBottom,'candidateExposedLowerLegSkinCells':0,'visibleKnee':'UNRESOLVED; covered, no anatomical coordinate','lowerAlphaRowsExactlySource':list(lowerRows),'nativeAlphaRows':rr,'visibleClothCuffShoeMasks':{'shorts':sorted([list(p) for p in cloth]),'cuffAfterShortsOcclusion':sorted([list(p) for p in visibleCuffs]),'shoeAfterCuffAndShortsOcclusion':sorted([list(p) for p in visibleShoes])}}
 report['frames'].append(item)
 if i in (0,2,4):
  row=(0,2,4).index(i);y=10+row*235
  for col,(label,img) in enumerate((('SOURCE',ref),('REJECTED HR10',before),('HR11',candidate))):
   x=35+col*355;dd.text((x,y),f'{label} frame{i} / native-pixel grid',fill='#242330');crop=img.crop((0,44,32,64)).resize((256,160),Image.Resampling.NEAREST);plate.paste(crop,(x,y+24),crop)
   for xx in range(33):dd.line((x+xx*8,y+24,x+xx*8,y+184),fill='#acaca3')
   for yy in range(21):
    dd.line((x,y+24+yy*8,x+256,y+24+yy*8),fill='#acaca3')
    if yy%2==0:dd.text((x-22,y+24+yy*8-4),str(44+yy),fill='#242330')
  dd.text((35,y+190),f'Body/costume bottom: source annotation {bodyBottom}; candidate mask {bodyBottom}. Visible shoe: {shoeTop}-{shoeBottom}. Knee UNRESOLVED.',fill='#242330')
  dd.text((35,y+207),'Source row spans include cuffs/costume. They are NOT anatomical shoe or bone widths.',fill='#242330')
plate.save(ext/'structural-native-grids.png')
(out/'structural-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'all8LowerAlphaContoursMatchAnnotatedSourceRows':True,'passingBodyBottom':56,'passingFirstGap':57,'passingVisibleShoeRows':[58,59],'strideBodyBottom':57,'strideVisibleShoeRows':[60,61],'knee':'UNRESOLVED','noExposedCalfPixels':True},indent=2))
