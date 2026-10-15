"""Check actual native browser screenshots; not a human uninterrupted-watch claim."""
from pathlib import Path
from PIL import Image, ImageDraw
import json,sys,hashlib,statistics
out=Path(__file__).parent; ext=Path(sys.argv[1]);raw=json.loads((ext/'captures.json').read_text());samples=raw['samples']
report={'method':raw['method'],'source_commit':'bae462f','screenshots':len(samples),'elapsedMs':raw['elapsedMs'],'userStorageUsed':False,'canvasUsed':False,'humanUninterruptedWatchCycles':0,'speeds':{}}
imgs=[Image.open(s['file']).convert('RGB') for s in samples]
gaps=[b['midpointMs']-a['midpointMs'] for a,b in zip(samples,samples[1:])]
report['maxSampleGapMs']=max(gaps);report['medianSampleGapMs']=statistics.median(gaps)
for speed,y,factor in [('normal',0,1),('slow',96,4)]:
    p=out/f'south-dressed-bald-{speed}-1x.gif';im=Image.open(p);lookup={}
    for i in range(im.n_frames):
        im.seek(i);lookup[im.convert('RGB').tobytes()]=['A','A','P','P','C','C','P','P'][i]
    runs=[]
    for i,cap in enumerate(imgs):
        panel=cap.crop((0,y,80,y+96));state=lookup.get(panel.tobytes());assert state is not None,(speed,i,'unmatched rendered pixels')
        if not runs or runs[-1]['phase']!=state:runs.append({'phase':state,'first':i,'last':i})
        else:runs[-1]['last']=i
    sequence=[r['phase'] for r in runs]
    for a,b,c in zip(sequence,sequence[1:],sequence[2:]):
        assert (a,b,c) in [('A','P','C'),('P','C','P'),('C','P','A'),('P','A','P')],(speed,sequence)
    starts=[i for i in range(1,len(runs)-4) if sequence[i:i+5]==['A','P','C','P','A']]
    assert len(starts)>= (3 if speed=='normal' else 2),(speed,'insufficient whole rendered cycles')
    plate=Image.new('RGB',(1600,520),'#bed4d5');draw=ImageDraw.Draw(plate)
    for n,run in enumerate(runs[starts[0]:starts[0]+5]):
        i=(run['first']+run['last'])//2;panel=imgs[i].crop((0,y,80,y+96));x=n*320
        draw.text((x+4,5),f"{speed} / {['A','P1','C','P2','A return'][n]}",fill='#253340')
        plate.paste(panel,(x+120,25));plate.paste(panel.resize((320,384),Image.Resampling.NEAREST),(x,130))
    plate.save(ext/f'actual-current-{speed}-cycle.png')
    report['speeds'][speed]={'exactGifSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'matchedScreenshots':len(samples),'unmatchedScreenshots':0,'completeObservedCycles':len(starts),'observedOrder':'A -> P -> C -> P -> A','fullRuns':sequence,'limitations':'Screenshots sample complete rendered cycles; duplicate holds indistinguishable. No human uninterrupted viewing or frame-synchronous cadence claim.'}
(out/'current-render-trace.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:v['completeObservedCycles'] for k,v in report['speeds'].items()},'complete rendered cycles; no human full-watch claim')
