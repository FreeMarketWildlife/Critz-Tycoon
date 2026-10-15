"""Pinned directional asset/table inspection; source-colored files stay external."""
from pathlib import Path
from PIL import Image
import json,hashlib,re,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR14';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
p=Path('/Users/tanoshi/.codex/visualizations/2026/10/14/hero-hr5-reference/walking.png')
assert hashlib.sha256(p.read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
s=Image.open(p);assert s.mode=='P' and s.size==(144,32)
im=s.convert('RGBA');a=Image.new('L',s.size);a.putdata([255 if n else 0 for n in s.get_flattened_data()]);im.putalpha(a)
code=(ext/'object_event_anims.h').read_text();seqs={}
for direction in ('South','North','West','East'):
 block=re.search(r'sAnim_Go'+direction+r'\[\]\s*=\s*\{(.*?)\};',code,re.S).group(1)
 seqs[direction.lower()]={'frames':list(map(int,re.findall(r'ANIMCMD_FRAME\((\d+),',block))),'holdTicks':list(map(int,re.findall(r'ANIMCMD_FRAME\(\d+, (\d+)',block))),'hFlip':'.hFlip = TRUE' in block}
report={'pinnedRevision':'5eff78649e7170a877b961ef0b3da13b81a16038','PNGsha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tableSha256':hashlib.sha256((ext/'object_event_anims.h').read_bytes()).hexdigest(),'factType':'decoded indexed PNG and pinned source table; not emulator observation','storedFrames':9,'frameCanvas':[16,32],'comparisonScale':2,'comparisonCanvas':[32,64],'groundAnchorConvention':[16,64],'perSpriteFitting':False,'engineWalkTables':seqs,'semanticLimit':'Neck/joint/skull anatomy not encoded in PNG; all Critz hidden-joint guides remain proposed','frames':[]}
for n in range(9):
 f=im.crop((n*16,0,n*16+16,32)).resize((32,64),Image.Resampling.NEAREST);f.save(ext/f'ROM-{n:02}.png')
 rows=[]
 for y in range(38,64):
  runs=[]
  for x in range(32):
   if f.getpixel((x,y))[3]:
    if runs and runs[-1][1]==x:runs[-1][1]=x+1
    else:runs.append([x,x+1])
  rows.append({'y':y,'alphaRuns':runs})
 report['frames'].append({'frame':n,'bounds':list(f.getbbox()),'rows':rows})
(out/'reference-observations.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'storedFrames':9,'engineWalkTables':seqs,'previewCadence':'Front8x100ms; ROM directional8x8-tick phases approximated toGIFcentiseconds separately; phase comparison clockexplicit'},indent=2))
