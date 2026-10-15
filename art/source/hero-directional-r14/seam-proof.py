"""Bounded seam row proof, with retained upper-costume differences exposed."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess,io,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR14';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
baseline='f4403d0';report={'task':'M1.HR14 bounded front passing seam correction','baseline':baseline,'exactScope':'all walking lowerrows54..63 plus SOUTH P row53 only','interpretation':'Row53P is a connected hem/dark-costume interface; observed alpha/material pattern does not locate an anatomical waist or leg origin. Row52 and stride row53 include source upper-costume/arm clusters; original Hero shirt/arm design retained there with differences disclosed.','sourceClassProof':{},'retainedSeamDifferences':{},'protectedNativePoses':{},'visualApproval':False}
sourcepath=ext.parent/'brendan-user-reference-original/01agijgmbz561.gif';assert hashlib.sha256(sourcepath.read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e';g=Image.open(sourcepath);assert g.n_frames==8;refs={};seq=[]
for i in range(8):
 g.seek(i);assert g.info['duration']==100;im=Image.new('RGBA',(32,64));im.paste(g.convert('RGBA').crop((0,0,128,192)).resize((32,48),Image.Resampling.NEAREST),(0,14));seq.append(im)
assert seq[0].tobytes()==seq[1].tobytes() and seq[2].tobytes()==seq[3].tobytes()==seq[6].tobytes()==seq[7].tobytes() and seq[4].tobytes()==seq[5].tobytes()
for po,i in [('A',0),('P',2),('C',4)]:refs[po]=seq[i]
def before(kind,d,po):return Image.open(io.BytesIO(subprocess.check_output(['git','show',baseline+f':docs/reviews/M1-HR14/{kind}-{d}-{po}.png'],cwd=root))).convert('RGBA')
def spans(im,y):
 v=[]
 for x in range(32):
  if im.getpixel((x,y))[3]:
   if v and v[-1][1]==x:v[-1][1]=x+1
   else:v.append([x,x+1])
 return v
for d in ('south','north','west','east'):
 for po in ('idle','A','P','C'):
  for kind in ('hero','dummy'):
   b=before(kind,d,po);n=Image.open(out/f'{kind}-{d}-{po}.png').convert('RGBA');changes=[[x,y] for y in range(64) for x in range(32) if b.getpixel((x,y))!=n.getpixel((x,y))]
   assert all(d=='south' and po=='P' and y==53 for x,y in changes),(d,po,kind,changes[:10])
   report['protectedNativePoses'][d+'/'+po+'/'+kind]={'changedCells':changes,'protectedOutsidePassingRow53':True}
for po in ('A','P','C'):
 ref=refs[po];h=Image.open(out/f'hero-south-{po}.png').convert('RGBA');report['retainedSeamDifferences'][po]={}
 for y in (52,53):
  missing=[x for x in range(32) if ref.getpixel((x,y))[3] and not h.getpixel((x,y))[3]];extra=[x for x in range(32) if h.getpixel((x,y))[3] and not ref.getpixel((x,y))[3]]
  report['retainedSeamDifferences'][po][str(y)]={'sourceSpans':spans(ref,y),'heroSpans':spans(h,y),'missingXs':missing,'extraXs':extra,'status':'EXACT source-visible interface' if po=='P' and y==53 else 'RETAINED original upper shirt/arm design; NOT an exact source match'}
  if po=='P' and y==53:
   assert not missing and not extra
   for x in range(32):
    sp=ref.getpixel((x,y));hp=h.getpixel((x,y))
    if not sp[3]:assert not hp[3]
    elif sp[:3]==(0,0,0):assert hp[:3] in [(36,35,48),(42,52,74)]
    else:assert sp[:3]==(123,66,66) and hp[:3]==(70,86,113)
   report['sourceClassProof']={'direction':'south','pose':'P','row':53,'sourceAlphaSpans':spans(ref,y),'alphaMismatchCells':0,'materialMismatchCells':0,'sourceVisibleClasses':['black/dark plane','brown hem/shadow plane'],'CritzMaterials':['ink/navy','slate shadow'],'anatomicalWaistCoordinate':None}
# Source colored grid and prior/current comparisons remain external.
plate=Image.new('RGB',(1440,1070),'#bed4d5');dd=ImageDraw.Draw(plate);ink='#253340'
for col,po in enumerate(('A','P','C')):
 xx=col*480;ref=refs[po];b=before('hero','south',po);h=Image.open(out/f'hero-south-{po}.png').convert('RGBA')
 dd.text((xx+8,5),po+' / FIXED32x64 / rows49..56',fill=ink)
 for row,(label,im) in enumerate([('SOURCE',ref),('BEFORE f4403d0',b),('CURRENT HR14 seam',h)]):
  y=35+row*245;x=xx+34;crop=im.crop((0,49,32,57));big=crop.resize((384,96),Image.Resampling.NEAREST);plate.paste(big,(x,y),big);dd.text((x,y-16),label,fill=ink)
  for sy in range(9):dd.line((x,y+sy*12,x+384,y+sy*12),fill='#748894');dd.text((x-24,y+sy*12),str(sy+49),fill=ink)
  for sx in range(33):dd.line((x+sx*12,y,x+sx*12,y+96),fill='#748894')
  dd.rectangle((x,y+4*12,x+383,y+5*12),outline='#ed745c',width=2)
  thumb=im.resize((64,128),Image.Resampling.NEAREST);plate.paste(thumb,(x+150,y+105),thumb)
 # Explicit native row53 occupancy, without hiding retained differences.
 y=790;dd.text((xx+8,y),'Row53 alpha: SOURCE / BEFORE / CURRENT',fill=ink)
 for k,im in enumerate((ref,b,h)):
  for x in range(32):
   if im.getpixel((x,53))[3]:dd.rectangle((xx+34+x*12,y+25+k*22,xx+45+x*12,y+42+k*22),fill='#253340')
 for n,yrow in enumerate((52,53)):
  e=report['retainedSeamDifferences'][po][str(yrow)];dd.text((xx+8,915+n*35),'Row'+str(yrow)+' source'+str(e['sourceSpans'])+' Hero'+str(e['heroSpans']),fill=ink)
 dd.text((xx+8,996),'P53 corrected; row52 and stride53 NOT exact.',fill=ink);dd.text((xx+8,1015),'Hem/costume seam; hidden waist/leg origin unresolved.',fill=ink);dd.text((xx+8,1034),'All heads, packs and rows54..63 remain exact priorHR14.',fill=ink)
plate.save(ext/'front-waist-seam-context.png')
# Original-only close-up; source boundary facts are numeric, no source RGB.
plate=Image.new('RGB',(960,460),'#bed4d5');dd=ImageDraw.Draw(plate)
for n,(kind,im) in enumerate([('HERO BEFORE',before('hero','south','P')),('HERO CURRENT',Image.open(out/'hero-south-P.png').convert('RGBA')),('DUMMY CURRENT',Image.open(out/'dummy-south-P.png').convert('RGBA'))]):
 x=n*320;dd.text((x+8,8),kind+' / P row53',fill=ink);big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+96,25),big);crop=im.crop((4,50,28,57)).resize((288,84),Image.Resampling.NEAREST);plate.paste(crop,(x+16,305),crop);dd.text((x+8,410),'Observed seam span[7,25); not bone anatomy',fill=ink)
plate.save(out/'passing-seam-before-after.png');report['allSeamChecksPass']=True;(out/'waist-seam-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: only SouthP row53 changes in Hero/dummy; new visible alpha/material interface exact. Retained row52/A,C53 mismatches disclosed; all other native pixels unchanged.')
