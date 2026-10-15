from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
r=Path(__file__).resolve().parents[4];p=r/'docs/reviews/M1-DS1';checks=[]
def ck(n,v):assert v,n;checks.append(n)
def im(f):return Image.open(f).convert('RGBA')
order=['A','A','P','P','C','C','P','P'];gifFrames=0
for s in [1,2]:
 for dr in ['south','north','west','east']:
  for po in ['idle','A','P','C']:
   q=im(p/f'dummy-{s}x-{dr}-{po}.png');ck(f'{s}{dr}{po} frame',q.size==(16*s,32*s));ck(f'{s}{dr}{po} binary alpha',set(q.getchannel('A').get_flattened_data())<={0,255});ck(f'{s}{dr}{po} empty margin',q.getbbox()[1]>=10*s);ck(f'{s}{dr}{po} frame margins',q.getbbox()[0]>0 and q.getbbox()[2]<16*s)
   if s==2:ck(dr+po+' refined, not nearest output',q.tobytes()!=im(p/f'dummy-1x-{dr}-{po}.png').resize((32,64),Image.Resampling.NEAREST).tobytes())
   if dr=='east':ck(str(s)+po+' mirrored facing',q.tobytes()==im(p/f'dummy-{s}x-west-{po}.png').transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes())
  for display in [1,4]:
   g=Image.open(p/f'dummy-{s}x-{dr}-walk-{display}display.gif');timeline=[];durations=[];gifFrames+=g.n_frames
   ck(str(s)+dr+str(display)+' loop',g.info['loop']==0)
   for frame in range(g.n_frames):
    g.seek(frame);duration=g.info['duration'];ck(f'{s}{dr}{display} hold{frame}',duration%100==0);timeline.extend([g.convert('RGBA').copy()]*(duration//100));durations.append(duration)
   ck(str(s)+dr+str(display)+' 800ms',sum(durations)==800 and len(timeline)==8)
   for slot,po in enumerate(order):
    expected=Image.new('RGBA',(16*s,32*s),'#eee8d1');expected.alpha_composite(im(p/f'dummy-{s}x-{dr}-{po}.png'));ck(f'{s}{dr}{display} actual timeline slot{slot}',timeline[slot].tobytes()==expected.resize((16*s*display,32*s*display),Image.Resampling.NEAREST).tobytes())
base=json.loads(Path(__file__).with_name('baseline-hashes.json').read_text());ck('all previous FM2/BS2 source/reference files preserved',all(hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256'] for x in base));ck('creator wholly unchanged',subprocess.run(['git','diff','--quiet','HEAD','--','character-creator'],cwd=r).returncode==0)
out=p/'independent-review';out.mkdir(exist_ok=True);(out/'saved-audit.json').write_text(json.dumps({'pass':True,'checks':len(checks),'actualDecodedGIFFrames':gifFrames,'logical100msSlots':128,'cadence':'Original presentation800ms; not source NPC timing','records':checks},indent=2)+'\n');print(json.dumps({'checks':len(checks),'actualGIFframes':gifFrames,'logicalSlots':128,'baselineFilesPreserved':len(base)}))
