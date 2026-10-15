"""Original DS1 bald dressed child. Independent native contour/feature maps per resolution."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-DS1';src=Path(__file__).parent
pal={'i':'#292634','s':'#80503d','m':'#ac724b','l':'#d19662','h':'#e2ad79','r':'#e87560','d':'#b6494d','w':'#f7e3b8','g':'#b7b6a1','b':'#485b78','n':'#2d3a55','a':'#7b91a3'}
# Hand-drawn independent contour maps, ranges inclusive; frame empty upper margin deliberate.
head1=[(6,9),(4,11),(3,12),(3,12),(2,13),(2,13),(2,13),(3,12),(3,12),(4,11),(5,10)]
head2=[(13,18),(10,21),(8,23),(7,24),(6,25),(6,25),(5,26),(5,26),(5,26),(4,27),(4,27),(4,27),(4,27),(5,26),(5,26),(6,25),(6,25),(7,24),(8,23),(9,22),(11,20),(13,18)]
side1=[(6,10),(4,11),(4,12),(3,12),(3,12),(3,13),(3,13),(4,12),(4,11),(5,10),(6,9)]
side2=[(13,20),(10,22),(9,23),(8,24),(7,25),(7,25),(6,25),(6,26),(6,26),(6,26),(6,27),(6,27),(6,26),(6,26),(7,25),(7,25),(8,24),(9,23),(10,22),(11,21),(12,20),(13,19)]
def render(dr,po,scale):
 im=Image.new('RGBA',(16*scale,32*scale));d=ImageDraw.Draw(im);s=scale
 def rect(box,c):d.rectangle(box,fill=pal[c])
 def poly(pts,c):d.polygon(pts,fill=pal[c])
 # source-like slight head bob, original authored cloth and feet below.
 dy=-s if po=='P' else 0
 side=dr in ('west','east');rows=(side1 if side else head1) if s==1 else (side2 if side else head2)
 for j,(x0,x1) in enumerate(rows):
  y=11*s+j+dy;rect((x0,y,x1,y),'i')
  if x1-x0>=3:
   rect((x0+1,y,x1-1,y),'m')
   if j>0 and j<len(rows)-2:
    rect((x0+1,y,max(x0+1,x1-2*s),y),'l')
    if j<4*s:rect((x0+2,y,max(x0+2,x1-3*s),y),'h')
 # Rear scalp no face or hair. Front/side eyes/ear drawn explicitly, no nose.
 if s==1:
  if dr=='south':
   rect((4,17+dy,4,18+dy),'i');rect((10,17+dy,10,18+dy),'i');rect((2,17+dy,2,18+dy),'m');rect((13,17+dy,13,18+dy),'m')
  elif side:
   rect((6,17+dy,6,18+dy),'i');rect((11,17+dy,12,19+dy),'s');rect((11,18+dy,11,18+dy),'m')
  else:rect((2,17+dy,2,18+dy),'m');rect((13,17+dy,13,18+dy),'m')
 else:
  if dr=='south':
   for x in (9,21):rect((x,34+dy,x+1,37+dy),'i')
   rect((5,34+dy,5,37+dy),'m');rect((26,34+dy,26,37+dy),'m')
  elif side:
   rect((12,34+dy,13,37+dy),'i');poly([(23,34+dy),(25,35+dy),(25,38+dy),(23,40+dy),(22,38+dy),(22,35+dy)],'s');rect((23,36+dy,23,37+dy),'m')
  else:rect((5,34+dy,5,37+dy),'m');rect((26,34+dy,26,37+dy),'m')
 # Distinct native body maps, preserving paired resolution landmarks.
 if s==1:
  t=21+dy
  if not side:
   poly([(4,t),(11,t),(13,t+2),(13,25),(11,27),(4,27),(2,25),(2,t+2)],'i')
   rect((4,t+1,11,25),'r');rect((5,t+1,10,t+1),'w');rect((4,t+3,11,t+3),'w');rect((3,t+2,4,t+3),'w');rect((11,t+2,12,t+3),'g')
   lh=1 if po=='C' else 0;rh=1 if po=='A' else 0
   rect((2,24-lh,3,25-lh),'m');rect((12,24-rh,13,25-rh),'s')
   rect((4,26,11,28),'n');rect((4,26,10,26),'b');rect((7,28,8,28),'i')
   if po in ('idle','P'):
    rect((4,29,6,29),'d');rect((9,29,11,29),'d');rect((3,30,6,30),'i');rect((9,30,12,30),'i');rect((4,30,6,30),'g');rect((9,30,11,30),'g')
   else:
    lead=(3,7) if po=='A' else (8,12);back=(9,11) if po=='A' else (4,6)
    rect((back[0],28,back[1],29),'d');rect((lead[0],29,lead[1],30),'i');rect((lead[0]+1,29,lead[1]-1,29),'d');rect((lead[0]+1,30,lead[1]-1,30),'g')
  else:
   poly([(6,t),(10,t),(12,t+2),(12,26),(11,27),(5,27),(4,25),(4,t+2)],'i')
   rect((6,t+1,10,25),'r');rect((5,t+1,7,t+2),'w');rect((8,t+3,10,t+3),'w');rect((10,t+1,11,25),'d')
   hx=3 if po=='A' else 10 if po=='C' else 4;hy=24 if po!='P' else 23
   poly([(hx,hy-1),(hx+1,hy-1),(hx+2,hy),(hx+2,hy+1),(hx+1,hy+2),(hx,hy+2),(hx-1,hy+1),(hx-1,hy)],'i');rect((hx,hy-1,hx+1,hy-1),'w');rect((hx,hy,hx+1,hy+1),'m');rect((hx,hy,hx,hy),'l')
   if po in ('idle','P'):
    rect((6,26,11,28),'n');rect((6,26,10,27),'b');rect((6,29,10,30),'i');rect((6,29,9,29),'d');rect((7,30,9,30),'g')
   else:
    poly([(6,26),(11,26),(12,28),(10,29),(6,28),(4,28)],'n');rect((6,26,10,27),'b')
    if po=='A':
     rect((9,29,11,30),'i');rect((10,29,10,29),'d');rect((3,28,6,29),'i');rect((4,28,5,28),'d');rect((4,29,5,29),'g')
    else:
     rect((4,29,6,30),'i');rect((5,29,5,29),'d');rect((10,28,13,29),'i');rect((11,28,12,28),'d');rect((11,29,12,29),'g')
 else:
  t=42+dy
  if not side:
   poly([(9,t),(22,t),(25,t+2),(27,t+5),(27,50),(24,53),(8,53),(4,50),(4,t+5),(6,t+2)],'i')
   poly([(9,t+1),(22,t+1),(24,t+4),(24,50),(22,52),(9,52),(7,49),(7,t+4)],'r');rect((10,t+1,21,t+2),'w');rect((8,t+6,23,t+7),'w');poly([(7,t+3),(10,t+3),(10,t+6),(5,t+6),(6,t+4)],'w');poly([(22,t+3),(24,t+3),(26,t+6),(22,t+6)],'g')
   for x,shift in [(5,2 if po=='C' else 0),(24,2 if po=='A' else 0)]:
    poly([(x,48-shift),(x+2,48-shift),(x+3,50-shift),(x+2,52-shift),(x,52-shift),(x-1,50-shift)],'s');rect((x,48-shift,x+1,50-shift),'l' if x<10 else 'm')
   poly([(8,52),(23,52),(24,56),(22,58),(18,58),(16,56),(14,58),(9,58),(7,56)],'n');rect((9,52,21,53),'b');rect((10,54,13,54),'a');rect((17,54,21,54),'b')
   pairs=[(7,13,58),(18,24,58)] if po in ('idle','P') else ([(6,14,59),(18,23,56)] if po=='A' else [(7,12,56),(17,25,59)])
  else:
   poly([(13,t),(21,t),(24,t+3),(25,49),(24,52),(21,54),(11,54),(8,51),(8,t+4),(10,t+2)],'i');poly([(13,t+1),(21,t+1),(23,t+4),(23,50),(20,52),(11,51),(10,t+4)],'r');poly([(11,t+2),(16,t+2),(16,t+5),(9,t+5)],'w');rect((16,t+7,21,t+8),'w');rect((22,t+4,23,50),'d')
   hx=7 if po=='A' else 21 if po=='C' else 9;hy=48 if po!='P' else 46
   poly([(hx-1,hy-2),(hx+3,hy-2),(hx+5,hy+1),(hx+4,hy+5),(hx,hy+5),(hx-1,hy+3)],'i');rect((hx,hy-2,hx+3,hy-1),'w');poly([(hx,hy),(hx+3,hy),(hx+4,hy+2),(hx+3,hy+4),(hx+1,hy+4),(hx,hy+3)],'s');rect((hx+1,hy,hx+2,hy+2),'l')
   if po in ('idle','P'):
    poly([(12,52),(23,52),(23,55),(21,58),(12,58),(10,56)],'n');poly([(13,52),(21,52),(21,55),(12,55)],'b');rect((14,53,18,53),'a');pairs=[(12,21,58)]
   else:
    poly([(12,52),(22,52),(25,55),(24,57),(20,59),(13,57),(8,57),(7,55)],'n');poly([(12,52),(21,52),(22,54),(16,56),(10,55)],'b');rect((13,53,17,53),'a');pairs=[(6,13,56),(19,24,59)] if po=='A' else [(8,13,59),(21,27,56)]
  # Connect each shoe to its visible clothed limb; do not leave floating tips.
  if side and po=='C':
   poly([(10,55),(14,56),(14,58),(12,60),(9,60),(9,57)],'n')
  for x0,x1,y in pairs:
   poly([(x0+1,y),(x1-1,y),(x1,y+1),(x1,y+2),(x1-1,y+3),(x0,y+3),(x0-1,y+2),(x0,y+1)],'i');rect((x0+1,y+1,x1-1,y+1),'d');rect((x0+1,y+2,x1-1,y+2),'g')
 if dr=='east':im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 return im
frames={};records={}
for s in (1,2):
 frames[s]={}
 for dr in ('south','north','west','east'):
  frames[s][dr]={}
  for po in ('idle','A','P','C'):
   im=render(dr,po,s);frames[s][dr][po]=im;p=out/f'dummy-{s}x-{dr}-{po}.png';im.save(p);records[p.name]={'size':im.size,'paintedBounds':im.getbbox(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
fnt=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',14)
def plate(directions,poses,name):
 b=Image.new('RGB',(960,len(directions)*len(poses)*220),'#eee8d1');d=ImageDraw.Draw(b)
 for j,(dr,po) in enumerate((d,p) for d in directions for p in poses):
  y=j*220;d.text((10,y+7),dr.upper()+' '+po+' — original bald dressed child / unapproved',font=fnt,fill='#292634')
  for k,s in enumerate((1,2)):
   q=frames[s][dr][po];x=30+k*480;big=q.resize((80,160),Image.Resampling.NEAREST);b.paste(big,(x,y+32),big);b.paste(q,(x+150,y+80),q);d.text((x+250,y+60),f'{16*s}x{32*s}\nnative + equal\ndisplay size',font=fnt,fill='#485b78')
 return b
plate(['south','north','west','east'],['idle'],'idles').save(out/'four-direction-resolution-comparison.png')
plate(['west'],['idle','A','P','C'],'gait').save(out/'west-gait-resolution-comparison.png')
(src/'native-checks.json').write_text(json.dumps(records,indent=2)+'\n')
print('32 original native poses written. Visual review pending, no creator/runtime changes.')
# Reproducible all-pose sheet; each frame shown native and at matched display size.
b=Image.new('RGB',(960,1000),'#eee8d1');d=ImageDraw.Draw(b)
for row,dr in enumerate(['south','north','west','east']):
 for col,(s,po) in enumerate((s,p) for s in [1,2] for p in ['idle','A','P','C']):
  q=frames[s][dr][po];x=col*120;y=row*250;d.text((x+5,y+5),f'{dr} {s}x {po}',font=fnt,fill='#292634');big=q.resize((80,160),Image.Resampling.NEAREST);b.paste(big,(x+10,y+40),big);b.paste(q,(x+15,y+180),q)
b.save(out/'all-poses-internal.png')
# Standalone art review animations only; no creator code involved.
order=['A','A','P','P','C','C','P','P']
for s in [1,2]:
 for dr in ['south','north','west','east']:
  for mag in [1,4]:
   seq=[]
   for po in order:
    q=frames[s][dr][po];bg=Image.new('RGBA',q.size,'#eee8d1');bg.alpha_composite(q);bg=bg.convert('RGB').resize((16*s*mag,32*s*mag),Image.Resampling.NEAREST);seq.append(bg)
   seq[0].save(out/f'dummy-{s}x-{dr}-walk-{mag}display.gif',save_all=True,append_images=seq[1:],duration=100,loop=0,optimize=False,disposal=2)
# Actual geometric/frame checks, distinct from appearance acceptance.
checks=[]
for s in [1,2]:
 for dr in frames[s]:
  for po,q in frames[s][dr].items():
   assert q.size==(16*s,32*s)
   assert q.getbbox()[1]>=10*s
   assert q.getbbox()[3]<=32*s
   assert set(q.get_flattened_data()) <= {(0,0,0,0)} | {tuple(bytes.fromhex(v[1:]))+(255,) for v in pal.values()}
   pts={(x,y) for y in range(q.height) for x in range(q.width) if q.getpixel((x,y))[3]};left=set(pts);stack=[left.pop()]
   while stack:
    x,y=stack.pop()
    for k in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if k in left:left.remove(k);stack.append(k)
   assert not left,(s,dr,po,'detached pixels')
   if dr=='east':assert q.tobytes()==frames[s]['west'][po].transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
   checks.append({'scale':s,'direction':dr,'pose':po,'singleConnectedClothedSilhouette':True,'frameAndPaletteCorrect':True})
(src/'checks.json').write_text(json.dumps({'poseChecks':checks,'appearanceApproval':False,'scope':'original art review only; no creator/runtime modifications'},indent=2)+'\n')
# Decode the saved GIFs; compare actual rendered pixel/hold sequence to authored poses.
gifchecks=[]
for s in [1,2]:
 for dr in frames[s]:
  for mag in [1,4]:
   p=out/f'dummy-{s}x-{dr}-walk-{mag}display.gif';g=Image.open(p);actual=[];holds=[]
   for n in range(g.n_frames):
    g.seek(n);hold=g.info.get('duration',0);assert hold>0 and hold%100==0;holds.append(hold);actual.extend([g.convert('RGB').tobytes()]*(hold//100))
   expected=[]
   for po in order:
    q=frames[s][dr][po];bg=Image.new('RGBA',q.size,'#eee8d1');bg.alpha_composite(q);expected.append(bg.convert('RGB').resize((16*s*mag,32*s*mag),Image.Resampling.NEAREST).tobytes())
   assert actual==expected,(s,dr,mag,'encoded pose mismatch')
   assert g.info.get('loop')==0
   gifchecks.append({'path':p.name,'frames':g.n_frames,'durationsMs':holds,'loopMs':sum(holds),'decoded8SlotPixelsExact':True,'loop':0})
(src/'gif-checks.json').write_text(json.dumps(gifchecks,indent=2)+'\n')
# Specific side-eye readability check on both authored eye rows.
for s in [1,2]:
 for po in frames[s]['west']:
  q=frames[s]['west'][po];dy=-s if po=='P' else 0;x=6 if s==1 else 12
  for y in range(17*s+dy,19*s+dy):
   assert q.getpixel((x,y))[:3]==tuple(bytes.fromhex(pal['i'][1:]))
   assert q.getpixel((x-1,y))[:3] in [tuple(bytes.fromhex(pal[k][1:])) for k in ['s','m','l','h']]
print('32 connected native poses;16 decoded art GIFs match all128 timeline slots; side eye has skin separation.')
