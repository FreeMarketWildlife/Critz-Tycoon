from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[4]; D=R/'docs/reviews/M1-NT1'; C=json.loads((R/'art/source/neutral-template-r1/construction.json').read_text()); checks=[]; facts={}
def ck(n,b):
 assert b,n
 checks.append(n)
def pixels(i):return {(x,y) for y in range(64) for x in range(32) if i.getpixel((x,y))[3]}
for dr in ['south','west']:
 p=D/dr;q=Image.open(p/'neutral.png').convert('RGBA');s=pixels(q);rec=C['directions'][dr]
 ck(dr+' dimensions/binary alpha',q.size==(32,64) and {v[3] for v in q.get_flattened_data()}=={0,255})
 ck(dr+' only declared flat colors',set(v for v in q.get_flattened_data() if v[3])<=set(map(tuple,C['palette'].values())))
 a=Image.new('RGBA',(32,64))
 for name in rec['renderOrder']:a.alpha_composite(Image.open(p/(name+'-region.png')).convert('RGBA'))
 ck(dr+' saved region and sparse outline composite exact',a.tobytes()==q.tobytes())
 ck(dr+' sparse outline layer',len(pixels(Image.open(p/'outline-region.png').convert('RGBA')))<len(s))
 seen=set();pending=[next(iter(s))]
 while pending:
  x,y=pending.pop()
  if (x,y) in seen:continue
  seen.add((x,y));pending.extend(v for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if v in s and v not in seen)
 ck(dr+' one four-connected silhouette',seen==s)
 ck(dr+' ground row61',max(y for x,y in s)==61)
 hp=R/f'docs/reviews/M1-NCR1/{dr}-idle/master-hero.png';old=Image.open(hp).convert('RGBA')
 ck(dr+' source file exact committed NCR1',hp.read_bytes()==subprocess.check_output(['git','show','0bb4ee4293ec2a76a3b8eb77d5d1fca4441bdcc1:'+str(hp.relative_to(R))]))
 eyes=rec['featureOwnership']['eyesRegisteredCells'];ck(dr+' registered eye sites preserved with flat charcoal color',all(q.getpixel(tuple(v))==tuple(C['palette']['outline']) and old.getpixel(tuple(v))[3]==255 for v in eyes))
 hand=Image.open(p/'hand-region.png').convert('RGBA');warm={v for v in pixels(hand) if hand.getpixel(v)==tuple(C['palette']['hand'])}
 ck(dr+' actual warm hand count',len(warm)==(34 if dr=='south' else 20))
 facts[dr]={'neutralSHA256':hashlib.sha256((p/'neutral.png').read_bytes()).hexdigest(),'bounds':q.getbbox(),'handWarmCells':len(warm),'groundXs':sorted(x for x,y in s if y==61),'fileCount':len(list(p.glob('*.png')))}
 if dr=='south':
  ck('protected Front Hero exact known SHA',hashlib.sha256(hp.read_bytes()).hexdigest()=='f959249734d6c588e433bb84f1de9435820b738235d568d15c8cbf8964fdb4ae')
  delta={(x,y) for y in range(45,64) for x in range(32) if q.getpixel((x,y))[3]!=old.getpixel((x,y))[3]}; facts[dr]['bodyAlphaChanges']=sorted(delta); ck('front body alpha differs only two paired hand-rim cells',delta=={(4,49),(27,49)})
  ck('front full shoe alpha58+ exact source',all(q.getpixel((x,y))[3]==old.getpixel((x,y))[3] for y in range(58,64) for x in range(32)))
  ck('front bilateral alpha',all(((31-x,y) in s)==((x,y) in s) for y in range(64) for x in range(32)))
 else:
  missing={(4,y) for y in range(36,41)}|{(5,41),(6,41),(7,42),(7,43),(24,41),(24,42),(24,43)}
  ck('all12 shared West face contour sites present dark',all(q.getpixel(v)==tuple(C['palette']['outline']) for v in missing))
  ck('West ear curl has open skin interior',q.getpixel((20,40))==tuple(C['palette']['head']) and q.getpixel((19,41))==tuple(C['palette']['head']))
  ck('West full left shoe envelope',Image.open(p/'shoe-region.png').getbbox()==(9,58,19,62))
  ck('West rounded hand4x6', (min(x for x,y in warm),min(y for x,y in warm),max(x for x,y in warm)+1,max(y for x,y in warm)+1)==(15,49,19,55))
ck('two directions only',set(C['directions'])=={'south','west'})
report={'task':'M1.NT1','pass':True,'count':len(checks),'checks':checks,'facts':facts,'appearanceAcceptance':False,'scope':'two idle32x64 construction candidates only; no motion claim'}
(D/'independent-review/saved-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'pass':True,'count':len(checks),'facts':facts}))
