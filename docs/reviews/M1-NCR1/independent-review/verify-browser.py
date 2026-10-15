from pathlib import Path
from PIL import Image
import json
O=Path(__file__).parent;D=O.parent;r=json.loads((O/'browser.json').read_text());checks=[]
for cap in r['captures']:
 shot=Image.open(O/(cap['name']+'.png')).convert('RGB')
 for panel in cap['panels']:
  x,y,w,h=panel['rect'];assert all(v==int(v) for v in [x,y,w,h]);src=Image.open(D/panel['src']).convert('RGBA');scale=w/src.width;assert scale in [1,3,6] and h/src.height==scale
  bg=Image.new('RGBA',src.size,'#eee8d1');bg.alpha_composite(src);target=bg.convert('RGB').resize((int(w),int(h)),Image.Resampling.NEAREST);actual=shot.crop((int(x),int(y),int(x+w),int(y+h)));assert target.tobytes()==actual.tobytes(),(cap['name'],panel)
  checks.append({'capture':cap['name'],'src':panel['src'],'rect':panel['rect'],'scale':scale,'exactPixels':True})
coverage={}
for speed in ['1','4']:
 coverage[speed]={}
 for dr in ['south','north','west','east']:
  seen=sorted({int(row['text'].split(dr+':')[1].split('/8')[0].split()[-1]) for row in r['live'] if row['speed']==speed});assert seen==list(range(1,9)),(speed,dr,seen);coverage[speed][dr]=seen
assert not r['errors'];assert r['storage']=={'local':0,'session':0}
(O/'browser-pixel-audit.json').write_text(json.dumps({'exactScreenshotPanelComparisons':len(checks),'panels':checks,'liveCoverage':coverage,'liveSamples':len(r['live']),'errors':r['errors'],'storage':r['storage'],'qualification':'Exact all-slot screenshots and observed live DOM coverage; visual screenshots inspected separately. No claim of uninterrupted human viewing or real device test.'},indent=2)+'\n')
print(json.dumps({'exactPanels':len(checks),'liveCoverage':coverage}))
