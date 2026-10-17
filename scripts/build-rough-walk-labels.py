"""Rough editable part-label drafts, NOT sprite artwork or approved anatomy.
Uses Phil's exact completed south anchor and actual reference masks/positions.
Repeated pixel-identical reference poses share one editable cel within each view.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,copy,collections
R=Path(__file__).resolve().parents[1];A=R/'sprite-editor/assets';O=R/'docs/reviews/M1-DC2';O.mkdir(exist_ok=True)
raw=(A/'phil-completed-south-20261017.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='f88b094cf73ff272aaa629cfcc8ef1a9f02f6d01989d11b4e20a6ca3411736d7';anchor=json.loads(raw);base=anchor['directions']['south'][0]['labels'];parts=anchor['parts'];head_ids={14,15,16,17,18,19,1,2,3};body_ids=set(range(28))-head_ids-{0};checks=[]
def rgba(path):return Image.open(path).convert('RGBA')
def mask(im):return {(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]}
def flat(d):return [d.get((x,y),0) for y in range(64) for x in range(32)]
def flip_labels(labels):
 swap={p['id']:next((q['id'] for q in parts if q['category']==p['category'] and q['side']==('right' if p['side']=='left' else 'left' if p['side']=='right' else p['side'])),p['id']) for p in parts}
 return [swap[labels[y*32+31-x]] for y in range(64) for x in range(32)]
def side_id(left,right,x,back=False):return (left if x<16 else right) if back else (right if x<16 else left)
def skin(c):r,g,b,a=c;return a and r>=220 and 140<=g<=220 and 100<=b<=190 and r>g>b

def south(im,slot):
 # Source eye/face sites move down2 in both unique strides, matching actual GIF.
 dy=2;occupied=mask(im);d={}
 for x,y in occupied:
  if y<45:continue
  if y>=58:d[x,y]=side_id(12,13,x)
  elif y>=55:d[x,y]=side_id(10,11,x) if x<12 or x>20 else side_id(22,23,x)
  elif y>=53:d[x,y]=side_id(22,23,x) if x<12 or x>21 else side_id(20,21,x)
  else:d[x,y]=side_id(6,7,x) if x<10 or x>22 else side_id(20,21,x)
 # Visible lower skin patches only, expanded by one occupied-pixel rim for glove volume.
 visible={(x,y) for x,y in occupied if y>=46 and (x<10 or x>21) and skin(im.getpixel((x,y)))}
 for x,y in visible:
  for dx,dy2 in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
   p=(x+dx,y+dy2)
   if p in occupied and p[1]>=46:d[p]=side_id(8,9,p[0])
 # Reuse Phil's head/eyes/ears exactly by rigid translation; covered skull is his design.
 for i,value in enumerate(base):
  if value in head_ids:
   x,y=i%32,i//32
   if y+dy<64:d[x,y+dy]=value
 return flat(d)

def west(im,slot):
 idle=slot in [2,3,6,7];dy=0 if idle else 2;occupied=mask(im);d={}
 # Actual projected clothed lower envelope; coarse internal ownership is a correction draft.
 for x,y in occupied:
  if y<46+dy:continue
  if y>=58:
   if idle:value=12 # the far shoe is occluded in the source passing/idle projection
   elif slot<2:value=12 if x>=15 else 13
   else:value=12 if x<=16 else 13
  elif y>=56:value=10 if idle or (x>=15 if slot<2 else x<=16) else 11
  elif y>=54:value=22
  else:value=20
  d[x,y]=value
 # Source-visible near glove patch/connected sleeve, not a hidden arm completion.
 hand_x=16 if idle or slot<2 else 18;hand_y=52+dy
 for x,y in occupied:
  if 46+dy<=y<hand_y-1 and hand_x-2<=x<=hand_x+1:d[x,y]=6
  if hand_x-2<=x<=hand_x+1 and hand_y-2<=y<=hand_y+1:d[x,y]=8
 # Only small actually exposed opposite sleeve/glove patches, never manufacture far pixels.
 for x,y in occupied:
  if 48+dy<=y<=51+dy and 8<=x<=11:d[x,y]=7 if y<50+dy else 9
 # Compact covered-skull proposal inside the hat/face envelope. No hat flourish or pack as head.
 rows=[(27,11,21),(28,9,23),(29,8,24),(30,7,25),(31,6,26),(32,5,27),(33,5,27),(34,4,28),(35,4,28),(36,4,28),(37,4,28),(38,4,28),(39,4,28),(40,4,26),(41,4,26),(42,6,26),(43,6,26),(44,8,24),(45,8,24)]
 for y,a,b in rows:
  for x in range(a,b):
   p=x,y+dy
   if p in occupied:d[p]=16
 # One actual source pupil, one visible near ear. Never add a second profile eye.
 for y in range(38+dy,42+dy):
  for x in [10,11]:
   if (x,y) in d:d[x,y]=14
 for x,y in [(20,40),(21,40),(20,41),(21,41),(20,42),(21,42)]:
  if (x,y+dy) in d:d[x,y+dy]=18
 return flat(d)

def north(im,slot):
 idle=slot in [2,3,6,7];dy=0 if idle else 2;occupied=mask(im);d={}
 for x,y in occupied:
  if y<44+dy:continue
  if y>=58:value=side_id(12,13,x,True)
  elif y>=56:value=side_id(10,11,x,True)
  elif y>=54:value=side_id(22,23,x,True)
  else:value=side_id(20,21,x,True)
  # Projected edge arms/hands only; pack-occluded center remains rough torso volume.
  if 44+dy<=y<=51+dy and (x<11 or x>21):value=side_id(6,7,x,True)
  if 48+dy<=y<=53+dy and (x<10 or x>23):value=side_id(8,9,x,True)
  d[x,y]=value
 rows=[(25,11,21),(26,9,23),(27,8,24),(28,7,25),(29,6,26),(30,5,27),(31,4,28),(32,4,28),(33,4,28),(34,2,30),(35,2,30),(36,2,30),(37,2,30),(38,2,30),(39,2,30),(40,4,28),(41,4,28),(42,6,26),(43,6,26)]
 for y,a,b in rows:
  for x in range(a,b):
   if (x,y+dy) in occupied:d[x,y+dy]=side_id(16,17,x,True)
 for x,y in list(d):
  sy=y-dy
  if (x<6 or x>25) and 36<=sy<=39:d[x,y]=18 if x<16 else 19
  elif (x<8 or x>23) and 40<=sy<=41:d[x,y]=18 if x<16 else 19
 return flat(d)

project={k:copy.deepcopy(v) for k,v in anchor.items() if k!='directions'};project['version']=2;project['activeFrame']=2;project['directions']={};project['cels']={};audit={};images={};primary=json.loads((A/'emerald-brendan/manifest.json').read_text());tick=primary['tickMs']
for direction in ['south','west','east','north']:
 frames=[];seen={};audit[direction]=[]
 for slot in range(8):
  path=A/(f'refined-south/frame-{slot}.png' if direction=='south' else f'emerald-brendan/{direction}-{slot}.png');im=rgba(path);h=hashlib.sha256(im.tobytes()).hexdigest()
  if h not in seen:
   cel_id=direction+'-'+h[:12];seen[h]=cel_id
   if direction=='south' and slot in [2,3,6,7]:labels=base[:];name='Phil completed south — exact'
   elif direction=='south':labels=south(im,slot);name='Rough south '+('A' if slot<2 else 'C')
   elif direction=='west':labels=west(im,slot);name='Rough west '+('A' if slot<2 else 'idle' if slot in [2,3,6,7] else 'B')
   elif direction=='east':
    west_im=rgba(A/f'emerald-brendan/west-{slot}.png');labels=flip_labels(west(west_im,slot));name='Rough east '+('A' if slot<2 else 'idle' if slot in [2,3,6,7] else 'B')
   else:labels=north(im,slot);name='Rough north '+('A' if slot<2 else 'idle' if slot in [2,3,6,7] else 'B')
   assert len(labels)==2048 and all(isinstance(i,int) and 0<=i<28 for i in labels);assert any(labels)
   if direction=='north':assert not any(i in [3,14,15] for i in labels)
   if direction in ['west','east']:assert not any(i==(15 if direction=='west' else 14) for i in labels)
   project['cels'][cel_id]={'id':cel_id,'name':name,'direction':direction,'labels':labels};images[cel_id]=im
  cel_id=seen[h];frames.append({'id':direction+'-slot-'+str(slot+1),'name':project['cels'][cel_id]['name'],'durationMs':100 if direction=='south' else 4*tick,'referenceIndex':slot,'celId':cel_id})
  audit[direction].append({'slot':slot,'celId':cel_id,'referencePixelSHA256':h,'marked':sum(bool(x) for x in project['cels'][cel_id]['labels'])})
 project['directions'][direction]=frames
 assert len(seen)==3
assert len(project['cels'])==12;assert project['cels'][project['directions']['south'][2]['celId']]['labels']==base
for d in project['directions']:
 assert len({f['celId'] for f in project['directions'][d]})==3
 for a in range(8):
  for b in range(8):assert (audit[d][a]['referencePixelSHA256']==audit[d][b]['referencePixelSHA256'])==(audit[d][a]['celId']==audit[d][b]['celId'])
(A/'phil-rough-walk-20261017.json').write_text(json.dumps(project,separators=(',',':'),ensure_ascii=False))
summary={'status':'ROUGH USER-CORRECTION DRAFT; not appearance approved','approvedAnchorSHA256':hashlib.sha256(raw).hexdigest(),'southAnchorLabelsExact':True,'uniqueEditablePoses':12,'timelineSlots':32,'perDirection':audit,'partCounts':{k:dict(collections.Counter(cel['labels'])) for k,cel in project['cels'].items()},'northNoEyes':True,'profilesOneVisibleEyeSide':True,'eastMirrorRemapsAnatomicalPairs':True,'timing':'Actual fan south100ms slots; original Emerald8-update commands preserved as two4-update UI slots','proposals':['Covered scalp contours under hat are rough reconstructions','Body/arm/hand/clothed volumes and near/far ownership are source-anchored approximations','Reference pack-occluded torso segmentation is proposed, not recovered anatomy','No additional hidden pixels/limbs painted to meet counts; Phil will correct labels']}
(O/'rough-label-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
# Original labels only: reusable review board, no reference raster in public docs.
board=Image.new('RGBA',(3*232,4*300),(23,33,29,255));draw=ImageDraw.Draw(board)
for row,direction in enumerate(['south','west','east','north']):
 for col,f in enumerate([project['directions'][direction][i] for i in [0,2,4]]):
  cel=project['cels'][f['celId']];im=Image.new('RGBA',(32,64));im.putdata([tuple(bytes.fromhex(parts[i]['color'][1:]))+(255,) if i else (0,0,0,0) for i in cel['labels']]);x=col*232;y=row*300;draw.text((x+8,y+8),direction+' '+str(col+1)+' | '+('EXACT ANCHOR' if direction=='south' and col==1 else 'ROUGH'),fill='white');board.alpha_composite(im,(x+8,y+36));board.alpha_composite(im.resize((96,192),Image.Resampling.NEAREST),(x+80,y+36))
board.save(O/'rough-labels-unique-poses.png');print('12 editable unique poses /32 timed slots; exact714southanchor retained')
