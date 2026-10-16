"""M1.OGH3 original walking study. Only exclusive OGH3 source/review writes.
OGH2 idle data is read-only. Native layer articulation, never whole-image resampling.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
R=Path(__file__).resolve().parents[3];S=Path(__file__).resolve().parent;O=R/'docs/reviews/M1-OGH3';I=R/'art/source/overnight-girl-continuation-r1';V=R/'docs/reviews/M1-OGH2'
assert S==R/'art/source/overnight-girl-walk-r1';assert O.is_dir()
P=dict(ink='#201008',skin='#a87038',light='#c48e4a',shade='#784820',hair='#30231d',hairMid='#493020',hairLight='#67462b',coral='#fa8078',coralShade='#c95662',cream='#f7edcc',blue='#184080',blueShade='#142e58',shoe='#80394e',shoeLight='#ad5264')
def blank():return Image.new('RGBA',(32,64))
def col(k):return tuple(bytes.fromhex(P[k][1:]))+(255,)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pts(q):return {(x,y) for y in range(64) for x in range(32) if q.getpixel((x,y))[3]}
def shift(q,dx=0,dy=0):
 z=blank()
 for x,y in pts(q):
  assert 0<=x+dx<32 and 0<=y+dy<64,(x,y,dx,dy)
  z.putpixel((x+dx,y+dy),q.getpixel((x,y)))
 return z

def select(q,f):
 z=blank()
 for x,y in pts(q):
  if f(x,y):z.putpixel((x,y),q.getpixel((x,y)))
 return z

def combine(ls):
 q=blank()
 for l in ls.values():q.alpha_composite(l)
 return q

def load(dr):
 spec=json.loads((I/(dr+'.layers.json')).read_text());ls={}
 for l in spec['layers']:
  im=blank();im.putdata([(0,0,0,0) if v==0 else tuple(bytes.fromhex(spec['palette'][v][1:]))+(255,) for v in l['pixels']]);ls[l['id']]=im
 return ls

def encode(images):
 pal=[None];lookup={}
 def enc(q):
  out=[]
  for px in q.get_flattened_data():
   if not px[3]:out.append(0);continue
   c='#%02x%02x%02x'%px[:3]
   if c not in lookup:lookup[c]=len(pal);pal.append(c)
   out.append(lookup[c])
  return out
 data=[enc(q) for q in images];return pal,data

headnames=['face','ears','hair','ties','eyes']
# Every head/face/hair/tie layer receives the same exact +2Y rigid translation.
# No horizontal head/torso shift, shape change or independent hair motion.
def front_stride(dr,a):
 idle=load(dr);ls={}
 shirt=idle['shirt'];hand=idle['exposed-arms-hands']
 leftshirt=select(shirt,lambda x,y:x<=9);rightshirt=select(shirt,lambda x,y:x>=22);torso=select(shirt,lambda x,y:10<=x<=21)
 ls['torso']=shift(torso,dy=2)
 # May3/5 left planted; opposite (right screen) arm lowers; garment/hand move together.
 for side,cloth,skin,delta in [('left',leftshirt,select(hand,lambda x,y:x<16),0 if a else 2),('right',rightshirt,select(hand,lambda x,y:x>=16),2 if a else 0)]:
  ls[side+'-sleeve']=shift(cloth,dy=delta);ls[side+'-arm-hand']=shift(skin,dy=delta)
 ls['shorts']=shift(idle['shorts'],dy=2)
 shoes=idle['shoes'];left=select(shoes,lambda x,y:x<16);right=select(shoes,lambda x,y:x>=16)
 # Each complete same-size full shoe translates rigidly; rear foot is two rows higher.
 left=shift(left,dx=2,dy=2 if a else 0);right=shift(right,dx=-2,dy=0 if a else 2)
 ls['rear-shoe']=right if a else left;ls['planted-shoe']=left if a else right
 for name in headnames:ls[name]=shift(idle[name],dy=2)
 return ls

def arm_swing(q,sign,far=False):
 z=blank()
 # Shoulder stays fixed in torso coordinates; lower arm follows a compact native arc.
 for x,y in pts(q):
  delta=0 if y<=49 else sign*(1 if y<=51 else 3)
  xx=x+delta;yy=y+2
  assert 0<=xx<32 and yy<64
  c=q.getpixel((x,y))
  if far and c in [col('skin'),col('light')]:c=col('shade')
  z.putpixel((xx,yy),c)
 return z

def west_stride(a):
 idle=load('west');ls={}
 # Canonical full near-foot is also the proposed hidden far-foot completion.
 # Both remain full56-cell source masks before occlusion; never a tiny rear fragment.
 near=shift(idle['shoes'],dx=3 if a else -3,dy=2)
 far=shift(idle['shoes'],dx=-3 if a else 3,dy=0)
 for x,y in pts(far):
  if far.getpixel((x,y))!=col('ink'):far.putpixel((x,y),col('shoe'))
 ls['far-arm-hand']=arm_swing(idle['exposed-arms-hands'],1 if a else -1,True)
 ls['far-shoe']=far
 ls['shirt']=shift(idle['shirt'],dy=2);ls['shorts']=shift(idle['shorts'],dy=2)
 ls['near-shoe']=near
 # Near leg rear/planted in7 => near arm forward; inverse in8.
 ls['near-arm-hand']=arm_swing(idle['exposed-arms-hands'],-1 if a else 1)
 for name in headnames:ls[name]=shift(idle[name],dy=2)
 return ls

D=['south','north','west','east'];poses={};cycle=['stride-a','idle','stride-b','idle'];reference_indices={'south':[3,0,4,0],'north':[5,1,6,1],'west':[7,2,8,2],'east':[7,2,8,2]}
contacts={'south':['screen-left','both','screen-right','both'],'north':['screen-left','both','screen-right','both'],'west':['screen-right/rear','center-overlap','screen-left/front','center-overlap'],'east':['screen-left/rear','center-overlap','screen-right/front','center-overlap']}
for dr in D:
 poses[dr]={'idle':load(dr)}
for dr in ['south','north']:
 poses[dr]['stride-a']=front_stride(dr,True);poses[dr]['stride-b']=front_stride(dr,False)
for phase,a in [('stride-a',True),('stride-b',False)]:
 poses['west'][phase]=west_stride(a)
 poses['east'][phase]={k:v.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for k,v in poses['west'][phase].items()}

manifest={'task':'M1.OGH3','state':'walking study awaiting independent motion review','appearanceAccepted':False,'sourceRevision':'5eff78649e7170a877b961ef0b3da13b81a16038','sourceClock':{'numeratorSeconds':280896,'denominator':16777216,'ticksPerSlot':8,'slots':4,'totalTicks':32,'exactPeriodMs':32*280896/16777216*1000},'gifNormalHoldsMs':[130,140,130,140],'gifSlowHoldsMs':[540,530,540,530],'cycle':cycle,'directions':{},'frameEdgeAnchor':[16,64],'headTorsoTransforms':{'idle':[0,0],'stride-a':[0,2],'stride-b':[0,2]},'proposalNotes':['Original compact limb articulation informed by actual May phases; not traced source graphics or recovered hidden bones.','Full shoe geometry translates unchanged before occlusion. Side hidden far shoe is proposed full-size completion of current near shoe.','Far arm is proposed occluded completion of existing near-arm volume; no new idle geometry.','Screen contact labels are visible source facts, not assertions of hidden anatomical left/right.','Exact browser clock is source-derived; GIF holds use cumulative nearest-centisecond quantization. No emulator observation.']}
images={}
for dr in D:
 images[dr]={};info={}
 for phase in ['idle','stride-a','stride-b']:
  ls=poses[dr][phase];q=combine(ls);out=O/dr/phase;out.mkdir(parents=True,exist_ok=True);q.save(out/'composite.png')
  if phase=='idle':
   assert q.tobytes()==Image.open(V/dr/'idle.png').convert('RGBA').tobytes()
   shutil.copyfile(V/dr/'idle.png',out/'composite.png')
  for name,im in ls.items():im.save(out/(name+'.png'))
  pal,arrays=encode(list(ls.values()));layers=[{'id':name,'visible':True,'pixels':arr} for name,arr in zip(ls,arrays)]
  (S/(dr+'-'+phase+'.layers.json')).write_text(json.dumps({'canvas':[32,64],'order':list(ls),'palette':pal,'layers':layers},separators=(',',':'))+'\n')
  info[phase]={'png':str((out/'composite.png').relative_to(R)),'pngSHA256':sha(out/'composite.png'),'bounds':q.getbbox(),'lastOpaqueRow':max(y for x,y in pts(q)),'layers':list(ls)};images[dr][phase]=q
 pal,arrays=encode([images[dr][phase] for phase in cycle])
 project={'format':'fmw-sprite','version':1,'name':'OGH3 Girl '+dr+' WALK STUDY / UNAPPROVED','preset':'character','width':32,'height':64,'palette':pal,'bank':'custom','frames':[{'name':phase+' / source'+str(reference_indices[dr][i]),'ticks':8,'pixels':arrays[i]} for i,phase in enumerate(cycle)],'notes':'Four-slot ordinary walk:8ticks each at280896/16777216sec per tick. Repeated idle slots exact OGH2; source-normal GIF holds rounded, browser exact. Review only; no appearance acceptance.'}
 (S/(dr+'.walk.sprite.json')).write_text(json.dumps(project,separators=(',',':'))+'\n')
 manifest['directions'][dr]={'sourceFrameIndices':reference_indices[dr],'sourceHorizontalFlip':dr=='east','visibleContactLabels':contacts[dr],'poses':info}
# Reference measurements only; no reference pixels saved in task folders.
refs=[]
for name,path,rev in [('May',R/'local-review/overnight-cast-qa/may-walking.png','5eff78649e7170a877b961ef0b3da13b81a16038'),('Brendan',Path('/tmp/ds1-primary-reference/brendan-walking.png'),'731ad5bfd6e6f265508d0efcca0ba42f9dcf5881'),('Man1',Path('/tmp/ds1-primary-reference/man_1.png'),'731ad5bfd6e6f265508d0efcca0ba42f9dcf5881')]:
 src=Image.open(path);facts=[]
 for i in range(9):
  q=src.crop((i*16,0,(i+1)*16,32));m={(x,y) for y in range(32) for x in range(16) if q.getpixel((x,y))!=0};by=max(y for x,y in m)
  facts.append({'index':i,'bounds':[min(x for x,y in m),min(y for x,y in m),max(x for x,y in m)+1,by+1],'contactY':by,'contactXs':sorted(x for x,y in m if y==by)})
 refs.append({'name':name,'path':str(path),'revision':rev,'sha256':sha(path),'frames':facts})
manifest['referenceFiles']=refs
(S/'construction.json').write_text(json.dumps(manifest,indent=2)+'\n');(O/'study.json').write_text(json.dumps(manifest,indent=2)+'\n')
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
board=Image.new('RGB',(820,1260),'#eee8d1');d=ImageDraw.Draw(board);d.text((12,8),'M1.OGH3 / ALL FOUR WALK SLOTS / 4x + ACTUAL NATIVE / UNAPPROVED',font=font,fill='#201008')
for row,dr in enumerate(D):
 for j,phase in enumerate(cycle):
  x=12+j*202;y=35+row*304;q=images[dr][phase]
  d.text((x,y),dr+' '+str(j)+' '+phase,font=font,fill='#201008');big=q.resize((128,256),Image.Resampling.NEAREST);board.paste(big,(x,y+20),big);board.paste(q,(x+150,y+200),q)
  d.text((x,y+280),'src'+str(reference_indices[dr][j])+' /8 ticks',font=font,fill='#201008')
board.save(O/'phase-board.png')
# Paired same-art cycle previews: native32x64 above integer4x, all directions adjacent.
preview=[];native=[]
for j,phase in enumerate(cycle):
 b=Image.new('RGB',(760,370),'#eee8d1');d=ImageDraw.Draw(b);d.fontmode='1';n=Image.new('RGB',(160,64),'#eee8d1')
 d.text((10,6),'OGH3 / WALK STUDY / NORMAL: exact browser ~535.77ms; GIF rounded540ms',font=font,fill='#201008')
 for i,dr in enumerate(D):
  q=images[dr][phase];x=10+i*186;d.text((x,28),dr+' /slot'+str(j),font=font,fill='#201008');b.paste(q,(x+10,48),q);big=q.resize((128,256),Image.Resampling.NEAREST);b.paste(big,(x+48,110),big);n.paste(q,(i*40,0),q)
 preview.append(b);native.append(n)
for name,frames,holds in [('walk-normal-paired.gif',preview,[130,140,130,140]),('walk-slow-paired.gif',preview,[540,530,540,530]),('walk-normal-native.gif',native,[130,140,130,140]),('walk-slow-native.gif',native,[540,530,540,530])]:
 if name=='walk-slow-paired.gif':
  frames=[q.copy() for q in frames]
  for q in frames:
   label=ImageDraw.Draw(q);label.fontmode='1';label.rectangle((0,0,759,23),fill='#eee8d1');label.text((10,6),'OGH3 / WALK STUDY / SLOW4x: exact browser ~2143.07ms; GIF rounded2140ms',font=font,fill='#201008')
 frames[0].save(O/name,save_all=True,append_images=frames[1:],duration=holds,loop=0,optimize=False,disposal=2)
 # Independent verification compares actual decoded GIF RGB frames to these intended RGB frames.
 (O/(name+'.frames.json')).write_text(json.dumps({'holdsMs':holds,'rgbFrameSHA256':[hashlib.sha256(q.tobytes()).hexdigest() for q in frames],'dimensions':list(frames[0].size)},indent=2)+'\n')
print('Built 12 native poses,16 cycle slots, semantic sources, phase board and4 GIF previews')
