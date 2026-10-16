from pathlib import Path
from PIL import Image
import json,base64,io,hashlib
r=Path('/Users/tanoshi/Documents/ChatGPT/Critz-Tycoon');h=r/'local-review/overnight-walk-qa/root-browser-final';matches=0;fail=[];coverage=set();pins={}
for char,task in [(c,t) for c,t in [('girl','M1-OGH3'),('nugget','M1-ON3'),('mom','M1-OM4')] if (h/f'{c}-samples.json').exists()]:
 samples=json.loads((h/f'{char}-samples.json').read_text())
 for s in samples:
  for c in s['cards']:
   d,p=c['d'],c['pose'];path=r/f'docs/reviews/{task}'/(f'{d}/{"stride-a" if p=="A" else "stride-b" if p=="B" else "idle"}/composite.png' if char=='girl' else f'{d}-{p}.png');target=Image.open(path).convert('RGBA');rendered=Image.open(io.BytesIO(base64.b64decode(c['png'].split(',')[1]))).convert('RGBA')
   ok=target.tobytes()==rendered.tobytes();matches+=ok
   if not ok:fail.append([char,d,p,c['speed'],s['elapsed']])
   coverage.add((char,d,c['speed'],c['slot']));pins[str(path.relative_to(r))]=hashlib.sha256(path.read_bytes()).hexdigest()
report={'method':'Actual live Chrome rAF samples; exact canvas pixels compared with saved author PNGs, all4slot coverage normal/slow; actual screenshot sequence visually inspected, not uninterrupted human watch','matches':matches,'failures':fail,'casesCovered':len(coverage),'coverage':[list(x) for x in sorted(coverage)],'candidatePins':pins,'browser':{c:json.loads((h/f'{c}-browser-report.json').read_text()) for c in ['girl','nugget','mom'] if (h/f'{c}-browser-report.json').exists()},'visualFindings':'All4facings normal/slow sampled. Feet alternate through exact idle with coherent near/far occlusion. Full hands follow alternating arm phases; head/hat/puff shapes stay rigid, with measured2pxYbob onstrides. No lateral torso sway/coat flap seen. Passing idle overlap remains broad; charm/bounce needs parent actual review. No final user appearance acceptance. Mom inset stays continuous under rigid torso bob in the final current capture; no user appearance acceptance.'}
o=r/'docs/reviews/M1-OWR2/independent-review';(o/'rendered-motion-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'matches':matches,'failures':len(fail),'coveredCases':len(coverage)}))
