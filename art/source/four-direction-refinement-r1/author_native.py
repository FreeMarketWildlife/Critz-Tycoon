"""Deliberate coarse-grid edits after actual scaffold inspection; never edits master."""
from pathlib import Path
import json
p=Path(__file__).parent;m=json.loads((p/'source-derived-scaffold.json').read_text());edits=[]
def setc(dr,po,kind,x,y,c,reason):
 rows=m[dr][po][kind];old=rows[y][x]
 if old!=c:rows[y]=rows[y][:x]+c+rows[y][x+1:];edits.append({'direction':dr,'pose':po,'part':kind,'xy':[x,y],'before':old,'after':c,'reason':reason})
for dr in m:
 for po in m[dr]:
  shift=-1 if po=='P' else 0;bottom=22+shift;skin=set('sSd');rows=m[dr][po]['bald'][:]
  # Master one-pixel contour often loses ties in a2x2 majority. Choose a
  # coherent one-native-pixel edge, retaining the same occupied coarse cells.
  for y in range(12+shift,bottom+1):
   xs=[x for x,c in enumerate(rows[y]) if c!='_']
   for x in xs:
    if rows[y][x] in skin and (x==min(xs) or x==max(xs)):
     # Actual projected ears remain skin; don't convert them to black prongs.
     if y==19+shift and x in ([2,13] if dr in ['south','north'] else ([2] if dr=='west' else [13])):continue
     setc(dr,po,'bald',x,y,'o','restore source contour lost in coarse color vote; within occupied block')
  # Fixed source eye sites quantize to 1x2 at19..20 (P18..19).
  if dr=='south':
   for x in [6,9]:
    for y in [19+shift,20+shift]:setc(dr,po,'bald',x,y,'o','source eyes x12..13/18..19, y38..41 divided by2')
  elif dr in ['west','east']:
   x=5 if dr=='west' else 10
   for y in [19+shift,20+shift]:setc(dr,po,'bald',x,y,'o','source profile eye landmark divided by2')
  # Native hair is simplified source clusters: merge internal black pinholes
  # into existing darkest hair, keep exterior and actual forehead occlusion.
  hrows=m[dr][po]['hero'][:]
  for y in range(10+shift,18+shift):
   for x,c in enumerate(hrows[y]):
    if c=='o' and 0<x<15 and hrows[y][x-1] in 'hml' and hrows[y][x+1] in 'hml':setc(dr,po,'hero',x,y,'h','merge sub-grid lock separator into connected darkest-hair cluster')
  # Coherent scalp/source-ear boundary must also persist wherever hair does
  # not actually occupy the projected cell. Hair-covered ear remains occluded.
  for y in range(12+shift,bottom+1):
   for x,c in enumerate(m[dr][po]['bald'][y]):
    if m[dr][po]['hero'][y][x] in skin and rows[y][x] in skin:
     if c=='o':setc(dr,po,'hero',x,y,c,'same visible source head contour on Hero and bald')
  # Full last-contact row comes from MASTER last painted row, not a2x2 tie.
  # Apply identical body cells to both; this chooses dark underside instead
  # of retaining pale sole and ink in one coarse cell.
  contact={'south':{'idle':30,'A':30,'P':29,'C':30},'north':{'idle':30,'A':31,'P':30,'C':31},'west':{'idle':30,'A':31,'P':30,'C':31},'east':{'idle':30,'A':31,'P':30,'C':31}}[dr][po]
  for kind in ['bald','hero']:
   for x,c in enumerate(m[dr][po][kind][contact]):
    if c!='_':setc(dr,po,kind,x,contact,'o','retain complete source dark contact underside; coarse sole detail loss declared')
  # Keep reflected lower SR2 material structure despite directional tie-order.
  if dr=='east':
   for kind in ['bald','hero']:
    for y in range(27 if po!='P' else 26,32):
     target=m['west'][po][kind][y][::-1]
     for x,c in enumerate(target):setc(dr,po,kind,x,y,c,'mirror frozen SR2 lower material geometry; eliminate vote tie handedness')
for po in m['south']:
 stripe_y=23 if po=='P' else 24
 for kind in ['bald','hero']:
  for x in [6,7,8]:setc('south',po,kind,x,stripe_y,'c','preserve actual source row49 central cream shirt motif; three-cell width with declared -1 master-pixel center rounding')
 y=20 if po=='P' else 21
 setc('south',po,'bald',3,y,'o','paired jaw contour: resolve sub-grid one-cell occupancy asymmetry, one master-pixel rounding')
for po in m['south']:
 y=29 if po=='P' else 30
 spans=[(4,6),(10,12)] if po in ['idle','P'] else [(9,11)] if po=='A' else [(5,7)]
 keep={x for a,b in spans for x in range(a,b)}
 for kind in ['bald','hero']:
  for x in range(16):setc('south',po,kind,x,y,'o' if x in keep else '_','exact half-width South last-contact spans; paired-axis and +/-1 master-pixel edge/center rounding; upper shoe unchanged')
(p/'native-maps.json').write_text(json.dumps(m,indent=2)+'\n');(p/'native-authored-edits.json').write_text(json.dumps({'basis':'actual visual scaffold audit; source-derived cell authoring, master unchanged','edits':edits},indent=2)+'\n');print('Authored',len(edits),'native cell choices')
