"""NCR1: deliberate16x32 cluster authoring from rejected H4R1 native trace.
No master resampling; no master output writing; every native edit recorded.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[3];SRC=Path(__file__).parent
old=json.loads((ROOT/'art/source/four-direction-refinement-r1/native-maps.json').read_text());maps=json.loads(json.dumps(old));changes=[]
def setc(dr,po,x,y,c,why):
 rows=maps[dr][po]['bald'];before=rows[y][x]
 if before!=c:rows[y]=rows[y][:x]+c+rows[y][x+1:];changes.append({'direction':dr,'pose':po,'xy':[x,y],'from':before,'to':c,'reason':why})
# Complete authored cranial/feature rows, shared across existing poses with
# the same original1-native-row P bob. Row22 retains projected collar ownership.
heads={
 'south':[
 '______oooo______','____oSSSSSSo____','___osSSSSSSSo___',
 '___oSSSSSSSSo___','___oSSSSSSSSo___','___oSSSSSSSSo___',
 '__osSSoSSoSSso__','___osSoSSoSso___','____osSSSSso____'],
 'north':[
 '______oooo______','____oSSSSSSo____','___osSSSSSSSo___',
 '___oSSSSSSSSo___','___oSSSSSSSSo___','___oSSSSSSSSo___',
 '__osSSSSSSSSso__','___osSSSSSSso___','____osSSSSso____'],
 'west':[
 '______oooo______','____oSSSSSSo____','___osSSSSSSSo___',
 '___oSSSSSSSSo___','___oSSSSSSSSo___','__oSSSSSSSSso___',
 '__oSSoSSSSdso___','___oSoSSSdso____','____oSSSssso____']}
heads['east']=[r[::-1] for r in heads['west']]
for dr in maps:
 for po in ['idle','A','P','C']:
  dy=-1 if po=='P' else 0
  for i,row in enumerate(heads[dr]):
   assert len(row)==16
   for x,c in enumerate(row):setc(dr,po,x,13+dy+i,c,'authored connected native contour/outlined ear/registered eyes; original head/body envelope correspondence')
  if dr=='south' and po in ['idle','P']:
   for x in [2,13]:setc(dr,po,x,26+dy,'o','dark lower hand rim; preserve warm inner hand and existing alpha')
   setc(dr,po,11,25+dy,'s','restore right inner hand from actual projected source skin, matching left three-cell hand')
  if dr=='north':
   sites=([(3,25+dy,'s'),(4,25+dy,'s'),(11,25+dy,'s'),(12,25+dy,'s')] if po in ['idle','P'] else [(11,25,'s'),(12,25,'d')] if po=='A' else [(3,25,'d'),(4,25,'s')])
   for x,y,c in sites:setc(dr,po,x,y,c,'recover source-registered exposed hand cluster from coarse costume vote; retain frame bounds')
# Deliberate side material clusters. Full painted footprint/contacts retained;
# connected blue diagonal/compact warm upper replaces full-width flat bands.
side={
 'idle':{(9,27):'b',(10,27):'n',(11,27):'n',(5,28):'b',(6,28):'b',(7,28):'b',(8,28):'n',(9,28):'n',(10,28):'o',(5,29):'v',(6,29):'r',(7,29):'v',(8,29):'n',(9,29):'v'},
 'P':{(6,27):'b',(7,27):'b',(8,27):'n',(9,27):'n',(10,27):'n',(5,28):'b',(6,28):'b',(7,28):'n',(8,28):'n',(9,28):'n',(10,28):'o',(5,29):'v',(6,29):'r',(7,29):'v',(8,29):'n',(9,29):'v'},
 'A':{(3,28):'b',(4,28):'b',(5,28):'n',(4,29):'v',(5,29):'n',(6,29):'n',(10,29):'v',(11,29):'r'},
 'C':{(4,29):'r',(5,29):'v',(11,29):'v',(12,29):'n'}}
for po,sites in side.items():
 for (x,y),c in sites.items():
  assert maps['west'][po]['bald'][y][x]!='_'
  setc('west',po,x,y,c,'curved connected blue trouser plane/compact warm near shoe and cooler smaller far cue; no hidden leg split')
 # Lower material structure faithfully reflected, rather than rebuilding feet.
 for y in range(27 if po!='P' else 26,32):
  row=maps['west'][po]['bald'][y][::-1]
  for x,c in enumerate(row):setc('east',po,x,y,c,'same authored side lower geometry/materials reflected at native centerline')
# Existing visible pack interior corner remains navy across gait, never a
# newly reconstructed hidden part. These are the exact three observed toggles.
for dr,po,x,y in [('west','A',12,26),('east','A',3,26),('east','C',3,26)]:setc(dr,po,x,y,'n','stabilize actual visible navy pack corner; remove ink/navy color blink')
# Match the corrected master material hierarchy on this native grid. Thin
# sole and dark contact cannot occupy separate halves of one native cell;
# retain dark contact, compress short pale edge one row above (documented).
shoe={
 'south':{'idle':{(5,28):'C',(10,28):'C',(5,29):'c',(10,29):'c'},'P':{(5,27):'C',(10,27):'C',(5,28):'c',(10,28):'c'},'A':{(9,28):'C',(9,29):'c'},'C':{(6,28):'C',(6,29):'c'}},
 'north':{'idle':{(4,29):'C',(5,29):'c',(6,29):'n',(9,29):'n',(10,29):'c',(11,29):'C'},'P':{(4,29):'C',(5,29):'c',(6,29):'n',(9,29):'n',(10,29):'c',(11,29):'C'},'A':{(6,29):'C',(7,29):'b',(5,30):'n',(6,30):'c',(7,30):'n'},'C':{(8,29):'b',(9,29):'C',(8,30):'n',(9,30):'c',(10,30):'n'}},
 'west':{'idle':{(6,28):'C',(7,28):'b',(5,29):'v',(6,29):'c',(7,29):'c',(8,29):'n',(9,29):'n'},'P':{(6,28):'C',(7,28):'b',(5,29):'v',(6,29):'c',(7,29):'c',(8,29):'n',(9,29):'n'},'A':{(4,29):'b',(5,29):'n',(10,29):'C',(11,29):'v',(10,30):'c',(11,30):'n'},'C':{(4,29):'v',(5,29):'C',(11,29):'b',(12,29):'n',(4,30):'n',(5,30):'c'}}}
for dr,poses in shoe.items():
 for po,sites in poses.items():
  for (x,y),c in sites.items():
   assert maps[dr][po]['bald'][y][x]!='_'
   setc(dr,po,x,y,c,'same dark upper/cool highlight/short pale edge/tiny warm cue as corrected master; material cluster compressed above dark contact')
for po in ['idle','A','P','C']:
 for y in range(27 if po!='P' else 26,32):
  for x,c in enumerate(maps['west'][po]['bald'][y][::-1]):setc('east',po,x,y,c,'same final side footwear hierarchy reflected; full original contact width retained')

(SRC/'native-body-maps.json').write_text(json.dumps({dr:{po:m['bald'] for po,m in ps.items()} for dr,ps in maps.items()},indent=2)+'\n');(SRC/'authored-changes.json').write_text(json.dumps({'task':'M1.NCR1','basis':'manually authored native grid, H4R1 trace for correspondence only, master untouched','changes':changes},indent=2)+'\n');print('Authored native cells',len(changes))
