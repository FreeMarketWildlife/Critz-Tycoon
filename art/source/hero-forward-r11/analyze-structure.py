"""Actual supplied all8 reference rows; no hidden knee/bone coordinates inferred."""
from pathlib import Path
from PIL import Image
import hashlib,json,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR11';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
original=ext.parent/'brendan-user-reference-original/01agijgmbz561.gif'
sha=hashlib.sha256(original.read_bytes()).hexdigest();assert sha=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e'
gif=Image.open(original);assert gif.n_frames==8
def runs(values):
 result=[]
 for x,v in enumerate(values):
  if result and result[-1]['value']==v:result[-1]['endExclusive']=x+1
  else:result.append({'start':x,'endExclusive':x+1,'value':v})
 return result
report={'sourceSha256':sha,'registration':'32x48 logical left crop at(0,14),32x64 comparison; no per-frame fit','annotationStatus':'Visible costume/overlap interpretation, not measured bone anatomy','kneeVisibility':'UNRESOLVED: no visible knee landmark in any frame','frames':[]}
for i in range(8):
 gif.seek(i);assert gif.info['duration']==100
 im=Image.new('RGBA',(32,64));im.paste(gif.convert('RGBA').crop((0,0,128,192)).resize((32,48),Image.Resampling.NEAREST),(0,14));im.save(ext/f'registered-left-{i:02}.png')
 pose=['A','A','P','P','C','C','P','P'][i]
 notes={'P':{'visibleBodyCostumeBottomAnnotated':56,'lowerColoredClusterStartAnnotated':55,'firstSeparatedLowerAlphaRuns':57,'feetBottom':59,'centralBridgeAt56':[14,18],'lowerClusterSideBoundsAt57':[[7,15],[17,25]]},'A':{'visibleBodyCostumeBottomAnnotated':57,'lowerColoredClusterStartAnnotated':56,'leadingOnlyAlphaBandStart':58,'feetBottom':61,'lowerClusterBoundsAt58':[[15,23]],'rearFootVisibility':'Not separately identifiable; do not invent a detached rear shoe'},'C':{'visibleBodyCostumeBottomAnnotated':57,'lowerColoredClusterStartAnnotated':56,'leadingOnlyAlphaBandStart':58,'feetBottom':61,'lowerClusterBoundsAt58':[[9,17]],'rearFootVisibility':'Not separately identifiable; do not invent a detached rear shoe'}}[pose]
 rows=[{'y':y,'alphaRuns':[[r['start'],r['endExclusive']] for r in runs([bool(im.getpixel((x,y))[3]) for x in range(32)]) if r['value']],'materialRGBARuns':runs([list(im.getpixel((x,y))) for x in range(32)])} for y in range(44,64)]
 report['frames'].append({'frame':i,'pose':pose,'durationMs':100,'visibleCostumeAnnotations':notes,'rows':rows})
(ext/'reference-material-runs.json').write_text(json.dumps(report,indent=2)+'\n')
# Exact source-colored cell runs stay external like the reference PNGs.
# Repository observations retain alpha intervals and visible annotations only.
numeric=json.loads(json.dumps(report))
for frame in numeric['frames']:
 for row in frame['rows']:row.pop('materialRGBARuns')
(out/'reference-structure.json').write_text(json.dumps(numeric,indent=2)+'\n')
print(json.dumps({'referenceHash':sha,'uniqueAnnotations':{f['pose']:f['visibleCostumeAnnotations'] for f in report['frames']},'kneeVisibility':report['kneeVisibility']},indent=2))
