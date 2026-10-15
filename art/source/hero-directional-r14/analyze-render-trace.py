"""Analyze actual browser-rendered pixels/cycles, not human-watch evidence."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib,statistics
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR14';ext=Path(sys.argv[1]).resolve();raw=json.loads((ext/'render-trace-captures.json').read_text())
assert set(raw['traces'])=={'south','north','west','east'}
def sha(im):return hashlib.sha256(im.tobytes()).hexdigest()
r={'task':'M1.HR14 automated continuous rendered-cycle trace','method':raw['method'],'actualImgScreenshots':True,'canvasDrawImageUsed':False,'isolatedContextsNoUserStorage':True,'humanUninterruptedWatchCompleted':False,'humanCompleteCyclesClaimed':0,'identifiabilityLimit':'Duplicated identical GIF holds cannot be distinguished visually. Export decode verifies8slots; render trace verifies observed A->P->C->P->A cycles with allsource/Hero/dummy panel pixels exact.','timingPrecision':'Capturemidpoint/transition midpoint estimates with measured sampling/capture tolerance; not frame-synchronous highprecision instrumentation.','directions':{}}
for d,t in raw['traces'].items():
 samples=t['samples'];gaps=[b['midpointMs']-a['midpointMs'] for a,b in zip(samples,samples[1:])];caps=[s['endMs']-s['startMs'] for s in samples];tol=max(gaps)+max(caps)/2+20;dr={'startedUTC':t['startedUTC'],'finishedUTC':t['finishedUTC'],'elapsedMs':t['elapsedMs'],'actualScreenshotSamples':len(samples),'maxSampleGapMs':max(gaps),'medianSampleGapMs':statistics.median(gaps),'maxCaptureDurationMs':max(caps),'measuredTimingToleranceMs':tol,'speeds':{}}
 imgs=[Image.open(s['file']).convert('RGBA') for s in samples];assert all(im.size==(112,192) for im in imgs)
 for speed,suffix,yy,factor in [('normal','',0,1),('slow','-SLOW4x',96,4)]:
  gif=Image.open(ext/f'source-hero-template-{d}{suffix}-native.gif');lookup={};expected={}
  for i in range(gif.n_frames):gif.seek(i);im=gif.convert('RGBA');lookup.setdefault(sha(im),[]).append(i);expected[i]=im
  runs=[];unknown=[]
  for i,im in enumerate(imgs):
   panel=im.crop((0,yy,112,yy+96));ids=lookup.get(sha(panel))
   if ids is None:unknown.append(i);continue
   state='A' if ids==[0,1] else 'C' if ids==[4,5] else 'P';at=samples[i]['midpointMs']
   if not runs or runs[-1]['state']!=state:runs.append({'state':state,'candidateExportSlots':ids,'firstSample':i,'lastSample':i,'firstMs':at,'lastMs':at})
   else:runs[-1].update(lastSample=i,lastMs=at)
  assert not unknown,(d,speed,'unexpected/unpainted render pixels',unknown)
  assert runs[0]['state']=='A'
  pattern=['A','P','C','P'];assert all(run['state']==pattern[i%4] for i,run in enumerate(runs)),(d,speed,'slip/skipped/extra observed phase')
  boundaries=[(a['lastMs']+b['firstMs'])/2 for a,b in zip(runs,runs[1:])];holds=[];expectedHolds=[200]*4 if d=='south' else [130,140,130,140]
  for i in range(1,len(runs)-1):
   measured=boundaries[i]-boundaries[i-1];want=expectedHolds[i%4]*factor;assert abs(measured-want)<=tol,(d,speed,i,measured,want,tol)
   holds.append({'phase':['A','P1','C','P2'][i%4],'estimatedMs':measured,'expectedGIFms':want,'errorMs':measured-want,'toleranceMs':tol})
  cycles=[]
  for i in range(1,len(runs)-4):
   if i%4:continue
   if [v['state'] for v in runs[i:i+5]]!=['A','P','C','P','A']:continue
   duration=boundaries[i+3]-boundaries[i-1];want=(800 if d=='south' else 540)*factor;assert abs(duration-want)<=tol,(d,speed,'cycle timing',duration,want,tol)
   cycles.append({'firstRun':i,'lastRun':i+4,'estimatedMs':duration,'expectedGIFms':want,'errorMs':duration-want,'toleranceMs':tol})
  need=3 if speed=='normal' else 2;assert len(cycles)>=need,(d,speed,'insufficient complete rendered cycles',len(cycles))
  start=cycles[0]['firstRun'];ink='#253340';plate=Image.new('RGB',(1160,500),'#bed4d5');dd=ImageDraw.Draw(plate)
  for n,run in enumerate(runs[start:start+5]):
   i=(run['firstSample']+run['lastSample'])//2;panel=imgs[i].crop((0,yy,112,yy+96));x=n*232;dd.text((x+3,4),d.upper()+' '+speed+' '+['A','P1','C','P2','A close'][n],fill=ink);plate.paste(panel,(x+60,26));plate.paste(panel.resize((224,192),Image.Resampling.NEAREST),(x+3,147));dd.text((x+3,355),'Actual captured render '+str(i),fill=ink);dd.text((x+3,373),str(round(samples[i]['midpointMs'],1))+' ms fromtrace start',fill=ink)
  dd.text((5,415),'Actual rendered image pixels; native + nearest2x; no per-pose fitting. Automated cycle trace, NOT continuous human watch.',fill=ink);dd.text((5,435),'All source/Hero/dummy pixels match exported frames; identical duplicate slots remain visually indistinguishable.',fill=ink);plate.save(ext/f'rendered-phase-contact-{d}-{speed}.png')
  plate=Image.new('RGB',(1824,270),'#bed4d5');dd=ImageDraw.Draw(plate)
  for n in range(4):
   a,b=runs[start+n],runs[start+n+1]
   for j,i in enumerate((a['lastSample'],b['firstSample'])):
    panel=imgs[i].crop((0,yy,112,yy+96));x=n*456+j*228;plate.paste(panel.resize((224,192),Image.Resampling.NEAREST),(x+2,30));dd.text((x+3,4),d+' '+speed+' '+a['state']+'>'+b['state']+(' before' if j==0 else ' after'),fill=ink);dd.text((x+3,235),'Capture'+str(i)+' at'+str(round(samples[i]['midpointMs'],1))+'ms',fill=ink)
  plate.save(ext/f'rendered-transition-pairs-{d}-{speed}.png')
  dr['speeds'][speed]={'expectedExportGIFsha256':hashlib.sha256((ext/f'source-hero-template-{d}{suffix}-native.gif').read_bytes()).hexdigest(),'unmatchedOrUnpaintedSamples':0,'observedPhaseSequence':''.join(run['state'] for run in runs),'completeRenderedCycles':len(cycles),'cycles':cycles,'phaseHoldEstimates':holds,'allPanelPixelsExactExport':True}
 # Complete captured stack playback, source andHero/dummy normal+slow together.
 # Actual sample-time holds quantized toGIF10ms, not relabelled source timing.
 frames=[im.convert('RGB') for im in imgs];colors=sorted(set(px for im in frames for px in im.get_flattened_data()));assert len(colors)<=256
 pal=[v for c in colors for v in c]+[0]*(768-len(colors)*3);index={c:i for i,c in enumerate(colors)};indexed=[]
 for im in frames:
  pp=Image.new('P',im.size);pp.putpalette(pal);pp.putdata([index[px] for px in im.get_flattened_data()]);indexed.append(pp)
 delays=[max(10,round((samples[i+1]['midpointMs']-s['midpointMs'])/10)*10) if i+1<len(samples) else 50 for i,s in enumerate(samples)]
 indexed[0].save(ext/f'actual-rendered-cycle-trace-{d}.gif',save_all=True,append_images=indexed[1:],duration=delays,loop=0,optimize=False,disposal=2)
 proof=Image.open(ext/f'actual-rendered-cycle-trace-{d}.gif');decoded=[]
 for i in range(proof.n_frames):proof.seek(i);decoded.append((sha(proof.convert('RGBA')),proof.info['duration']))
 target=[]
 for im,duration in zip(imgs,delays):
  key=sha(im)
  if target and target[-1][0]==key:target[-1]=(key,target[-1][1]+duration)
  else:target.append((key,duration))
 actual=[]
 for key,duration in decoded:
  if actual and actual[-1][0]==key:actual[-1]=(key,actual[-1][1]+duration)
  else:actual.append((key,duration))
 assert target==actual,(d,'captured playback GIF pixel/timing drift')
 dr['capturedPlaybackGIF']={'path':str(ext/f'actual-rendered-cycle-trace-{d}.gif'),'kind':'Actual screenshot stack playback; upper normal/lower slow;10ms capture-timingquantization','includesTraceElapsedMs':sum(delays),'decodedPixelAndTimingRLEExact':True,'sha256':hashlib.sha256((ext/f'actual-rendered-cycle-trace-{d}.gif').read_bytes()).hexdigest()};r['directions'][d]=dr
r['allRenderTraceChecksPass']=True;(out/'rendered-cycle-trace.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS rendered cycles/pixels/order/timing: '+', '.join(d+': normal'+str(v['speeds']['normal']['completeRenderedCycles'])+'/slow'+str(v['speeds']['slow']['completeRenderedCycles']) for d,v in r['directions'].items())+'. Not uninterrupted human watch.')
