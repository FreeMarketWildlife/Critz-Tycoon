from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[4];A=Path(__file__).parent.parent;B=R/'docs/reviews/M1-H4R1';order=['A','A','P','P','C','C','P','P'];checks=[]
for dr in ['south','north','west','east']:
 for speed,mul in [('normal',1),('slow',4)]:
  p=A/f'{dr}-paired-existing-walk-{speed}.gif';g=Image.open(p);assert g.n_frames==8 and g.info.get('loop')==0
  for i,po in enumerate(order):
   g.seek(i);fr=g.convert('RGB');hold=([100]*8 if dr=='south' else [70,60,70,70,70,60,70,70])[i]*mul;assert g.info['duration']==hold
   for col,(base,file,scale) in enumerate([(B,'native-hero.png',6),(B,'native-bald.png',6),(A,'native-hero.png',6),(A,'native-bald.png',6),(A,'master-hero.png',3)]):
    q=Image.open(base/f'{dr}-{po}'/file).convert('RGBA');bg=Image.new('RGBA',q.size,'#eee8d1');bg.alpha_composite(q)
    for rect,sz in [((col*230+10,24,col*230+106,216),(96,192)),((col*230+155,110,col*230+155+q.width,110+q.height),q.size)]:assert fr.crop(rect).tobytes()==bg.convert('RGB').resize(sz,Image.Resampling.NEAREST).tobytes()
   checks.append({'file':p.name,'frame':i+1,'holdMs':hold,'all5NativeAndEnlargedPanelsExact':True})
(A/'independent-review/source-gif-audit.json').write_text(json.dumps({'sourceSHA':'0bb4ee4293ec2a76a3b8eb77d5d1fca4441bdcc1','decodedFrames':64,'exactSourcePanelComparisons':640,'checks':checks},indent=2)+'\n');print('64 actual sourceGIFframes,640 native/enlarged panel comparisons exact')
