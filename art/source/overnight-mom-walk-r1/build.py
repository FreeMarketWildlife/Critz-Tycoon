"""OM4 original walking study. Read-only OM3. Exclusive source/review outputs."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
S=Path(__file__).resolve().parent;R=S.parents[2];O=R/'docs/reviews/M1-OM4';I=R/'art/source/overnight-mom-inset-r1';V=R/'docs/reviews/M1-OM3'
assert S==R/'art/source/overnight-mom-walk-r1'
DIRS=['south','north','west','east'];SEQUENCE=['A','idle','B','idle'];FONT=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
P={'ink':'#201008','navy':'#30476a','navyShadow':'#202e48','skinShadow':'#784820','roseShadow':'#87465e','farShoe':'#423b48'}
def color(n):return tuple(bytes.fromhex(P.get(n,n).lstrip('#')))+(255,)
def blank():return Image.new('RGBA',(32,64))
def load(dr):
 d=json.loads((I/dr/'layers.json').read_text());return {n:Image.open(I/dr/(n+'.png')).convert('RGBA') for n in d['order']}
def comp(ls):
 im=blank()
 for layer in ls.values():im.alpha_composite(layer)
 return im
def cut(im,pred):
 out=blank()
 for y in range(64):
  for x in range(32):
   if pred(x,y):out.putpixel((x,y),im.getpixel((x,y)))
 return out
def move(im,dx=0,dy=0):
 out=blank();out.alpha_composite(im,(dx,dy));return out
def dark(im,kind):
 out=im.copy()
 for y in range(64):
  for x in range(32):
   p=im.getpixel((x,y))
   if p[3] and p!=color('ink'):
    if kind=='shoe':c='farShoe'
    elif p[:3] in [(168,112,56),(196,142,74),(120,72,32)]:c='skinShadow'
    else:c='roseShadow'
    out.putpixel((x,y),color(c))
 return out
def armphase(im,slope,dx=0):
 out=blank()
 for y in range(64):
  for x in range(32):
   p=im.getpixel((x,y))
   if p[3]:
    xx=x+round((y-44)*slope)+dx;yy=y+2
    assert 0<=xx<32 and 0<=yy<64,'arm clipped'
    out.putpixel((xx,yy),p)
 return out
def frontal(dr,phase):
 idle=load(dr);ls={}
 for side,left in [('left',True),('right',False)]:
  lead=left==(phase=='A');dx=1 if left else -1;dy=2 if lead else -1;half=lambda x:x<16 if left else x>=16
  ls[side+'-leg']=move(cut(idle['legs'],lambda x,y:half(x)),dx,dy)
  shoe=cut(idle['feet'],lambda x,y:half(x))
  ls[side+'-shoe']=move(shoe if lead else dark(shoe,'shoe'),dx,dy)
 # Torso material is one rigid registered shape throughout the stride.
 ls['torso']=move(idle['torso'],dy=2)
 for side,left in [('left',True),('right',False)]:
  lead=left==(phase=='A');dy=1 if lead else 3;half=lambda x:x<16 if left else x>=16
  for n in ['near-arm','hands']:ls[side+'-'+n]=move(cut(idle[n],lambda x,y:half(x)),dy=dy)
 for n in ['head','face','hair','jewelry']:ls[n]=move(idle[n],dy=2)
 return ls
def profile(phase,dr='west'):
 idle=load(dr);ls={};sign=1 if dr=='west' else -1
 near_dx=(-3 if phase=='A' else 3)*sign;far_dx=-near_dx
 ls['far-shoe']=move(dark(idle['feet'],'shoe'),far_dx,0)
 for name,dx,dy,fill in [('far-leg',far_dx,0,'navyShadow'),('near-leg',near_dx,2,'navy')]:
  leg=blank();d=ImageDraw.Draw(leg)
  # Original short hidden-trouser connections under the unchanged garment.
  if dr=='west':pts=[(14,54),(22,54),(21+dx,58+dy),(13+dx,58+dy)]
  else:pts=[(9,54),(17,54),(18+dx,58+dy),(10+dx,58+dy)]
  d.polygon(pts,fill=color('ink'))
  if dr=='west':inner=[(15,55),(21,55),(20+dx,57+dy),(14+dx,57+dy)]
  else:inner=[(10,55),(16,55),(17+dx,57+dy),(11+dx,57+dy)]
  d.polygon(inner,fill=color(fill));ls[name]=leg
 ls['near-shoe']=move(idle['feet'],near_dx,2)
 slope=(.35 if phase=='A' else -.35)*sign
 ls['far-sleeve']=armphase(dark(idle['near-arm'],'arm'),-slope,-5*sign)
 ls['far-hand']=armphase(dark(idle['hands'],'arm'),-slope,-5*sign)
 ls['torso']=move(idle['torso'],dy=2)
 ls['near-sleeve']=armphase(idle['near-arm'],slope)
 ls['near-hand']=armphase(idle['hands'],slope)
 for n in ['head','face','hair','jewelry']:ls[n]=move(idle[n],dy=2)
 return ls
def save(dr,pose,ls):
 folder=S/dr/pose;folder.mkdir(parents=True,exist_ok=True)
 sparse={}
 for n,im in ls.items():
  im.save(folder/(n+'.png'));sparse[n]=[[j%32,j//32,'#'+bytes(p[:3]).hex()] for j,p in enumerate(im.get_flattened_data()) if p[3]]
 (S/dr/(pose+'.layers.json')).write_text(json.dumps({'frame':[32,64],'anchor':[16,64],'order':list(ls),'layers':sparse,'torsoTransform':[0,0 if pose=='idle' else 2]},indent=2)+'\n')
 im=comp(ls);im.save(O/(dr+'-'+pose+'.png'));return im
def gif(path,ims,holds,transparent=False):
 colors=sorted({p[:3] for im in ims for p in im.convert('RGBA').get_flattened_data() if p[3]});assert len(colors)<255
 pal=[0,0,0]+[v for c in colors for v in c];pal +=[0]*(768-len(pal));lookup={c:i+1 for i,c in enumerate(colors)};frames=[]
 for im in ims:
  q=Image.new('P',im.size);q.putpalette(pal);q.putdata([lookup[p[:3]] if p[3] else 0 for p in im.convert('RGBA').get_flattened_data()]);frames.append(q)
 kw={'transparency':0} if transparent else {}
 frames[0].save(path,save_all=True,append_images=frames[1:],duration=holds,loop=0,disposal=2,optimize=False,**kw)
def board(poses,phase):
 out=Image.new('RGB',(840,370),'#e8e4d7');d=ImageDraw.Draw(out);d.text((15,8),'MOM OM4 / WALK STUDY / UNAPPROVED / 8 UPDATES PER SLOT',font=FONT,fill='#252431')
 for i,dr in enumerate(DIRS):
  x=15+i*210;im=poses[dr][phase];d.text((x,35),dr.upper()+' '+phase+' /4x+1x',font=FONT,fill='#252431');big=im.resize((128,256),Image.Resampling.NEAREST);out.paste(big,(x,60),big);out.paste(im,(x+150,240),im)
 d.text((15,340),'Rigid +2Y upper stride bob; exact OM3 idle; fixed anchor16,64.',font=FONT,fill='#252431');return out
for path,h in json.loads((S/'protected-inputs.json').read_text()).items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h,path
poses={dr:{} for dr in DIRS}
for dr in DIRS:
 for phase in ['A','idle','B']:
  ls=load(dr) if phase=='idle' else frontal(dr,phase) if dr in ['south','north'] else profile(phase,dr)
  poses[dr][phase]=save(dr,phase,ls)
 pal=[None]+sorted({'#'+bytes(p[:3]).hex() for im in poses[dr].values() for p in im.get_flattened_data() if p[3]})
 project={'format':'fmw-sprite','version':1,'name':'Mom OM4 '+dr+' unapproved','preset':'character','width':32,'height':64,'palette':pal,'bank':'custom','notes':'Source8-update slots; no runtime adoption','frames':[{'name':phase,'ticks':8,'pixels':[pal.index('#'+bytes(p[:3]).hex()) if p[3] else 0 for p in poses[dr][phase].get_flattened_data()]} for phase in SEQUENCE]}
 (S/dr/'walk.sprite.json').write_text(json.dumps(project,indent=2)+'\n')
for speed,holds in [('normal',[130,140,130,140]),('slow4x',[540,530,540,530])]:
 gif(O/('four-directions-'+speed+'.gif'),[board(poses,p) for p in SEQUENCE],holds)
 for dr in DIRS:
  for scale in [1,4]:gif(O/(dr+'-'+speed+'-'+str(scale)+'x.gif'),[poses[dr][p].resize((32*scale,64*scale),Image.Resampling.NEAREST) for p in SEQUENCE],holds,True)
for i,p in enumerate(SEQUENCE):board(poses,p).save(O/('four-directions-slot'+str(i)+'.png'))
strip=Image.new('RGB',(840,4*310),'#e8e4d7');d=ImageDraw.Draw(strip)
for row,dr in enumerate(DIRS):
 for col,p in enumerate(SEQUENCE):
  im=poses[dr][p];x=15+col*210;y=row*310;d.text((x,y+4),dr+' '+p+' / slot'+str(col),font=FONT,fill='#252431');big=im.resize((128,256),Image.Resampling.NEAREST);strip.paste(big,(x,y+30),big);strip.paste(im,(x+150,y+215),im)
strip.save(O/'all-phases-native-4x.png')
atlas=Image.new('RGBA',(128,256))
for row,dr in enumerate(DIRS):
 for col,p in enumerate(SEQUENCE):atlas.alpha_composite(poses[dr][p],(32*col,64*row))
atlas.save(O/'walk-atlas.png')
manifest={'task':'M1.OM4','frame':[32,64],'anchor':[16,64],'sequence':SEQUENCE,'sourceOrder':{'south':[3,0,4,0],'north':[5,1,6,1],'west':[7,2,8,2],'east':['flip7','flip2','flip8','flip2']},'tickSeconds':280896/16777216,'updatesPerSlot':8,'normalGifMs':[130,140,130,140],'slow4xGifMs':[540,530,540,530],'appearanceAccepted':False,'construction':'Exact OM3 idle; rigid +2Y head and torso on strides; original alternating arm/short trouser connections; full near shoe translated intact; constructed dark full far shoe behind near foot, no shrinking. No x/shape sway or flaps.'}
(S/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'uniquePoses':12,'atlas':str(O/'walk-atlas.png')}))
