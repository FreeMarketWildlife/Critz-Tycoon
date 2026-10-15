"""DS4 coherent internal set; native base first. Historical assets are read-only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,ast,argparse,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-DS4';src=Path(__file__).parent
mod=ast.parse((root/'art/source/dummy-resolution-r1/build.py').read_text());old={}
for n in mod.body:
 if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['pal','head1','side1']:old[n.targets[0].id]=ast.literal_eval(n.value)
pal=old['pal'];heads={'south':old['head1'],'north':[(5,10),(4,11),(3,12),(2,13),(2,13),(2,13),(2,13),(2,13),(3,12),(3,12),(4,11)],'west':old['side1']}
baseline=Image.open(root/'docs/reviews/M1-DS3/dummy-1x-west-idle.png').convert('RGBA')
def native(dr,po):
 if dr=='east':return native('west',po).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if dr=='west' and po=='idle':return baseline.copy()
 im=Image.new('RGBA',(16,32));d=ImageDraw.Draw(im);dy=-1 if po=='P' else 0
 def r(box,c):d.rectangle(box,fill=pal[c])
 def p(pts,c):d.polygon(pts,fill=pal[c])
 def upper(pts,c):p([(x,y+dy) for x,y in pts],c)
 def ur(box,c):a,b,cx,de=box;r((a,b+dy,cx,de+dy),c)
 # Upper garment volume precedes the compact head, which occludes it.
 if dr=='west':
  upper([(7,19),(10,19),(12,21),(12,25),(11,27),(5,27),(4,25),(4,22),(5,21)],'i');ur((6,20,10,25),'r');ur((11,21,11,25),'d');ur((5,22,5,23),'r');ur((8,24,10,24),'w')
  # Full short legs overlap at the waist; pose shifts explain near/far contacts.
  if po in ('idle','P'):
   p([(5,26),(11,26),(11,28),(6,29),(5,28)],'n');r((6,26,10,27),'b');feet=[(6,10,29)]
  elif po=='A':
   p([(5,26),(11,26),(12,28),(10,29),(7,28),(4,28),(4,27)],'n');r((6,26,10,27),'b');feet=[(4,7,28),(10,12,29)]
  else:
   p([(5,26),(11,26),(12,27),(12,28),(9,28),(7,29),(5,29),(4,28)],'n');r((6,26,10,27),'b');feet=[(5,7,29),(10,13,28)]
  hx=3 if po=='A' else 10 if po=='C' else 4;hy=24+dy
  ur((hx,23,hx+2,23),'w');r((hx,hy,hx,hy+1),'s');r((hx+1,hy,hx+2,hy+1),'m');r((hx+1,hy,hx+1,hy),'l');r((hx+1,hy+2,hx+1,hy+2),'s')
  for a,b,y in feet:
   r((a,y,b,y+1),'i');r((a,y,b-1,y),'d');r((a+1,y+1,b-1,y+1),'g')
 else:
  upper([(5,19),(10,19),(12,21),(13,24),(13,26),(11,27),(4,27),(2,26),(2,24),(3,21)],'i');ur((4,20,11,25),'r');ur((3,23,4,24),'w');ur((11,23,12,24),'g');ur((5,24,10,24),'w')
  r((4,26,11,28),'n');r((5,26,10,26),'b');r((7,28,8,28),'i')
  for x,shift in [(2,-1 if po=='A' else 0),(12,-1 if po=='C' else 0)]:
   y=25+dy+shift;r((x,y,x+1,y+1),'m' if x==2 else 's');r((x,y,x,y),'l' if x==2 else 'm')
  feet=[(4,6,29),(9,11,29)] if po in ('idle','P') else ([(3,6,29),(9,11,28)] if po=='A' else [(4,6,28),(9,12,29)])
  for a,b,y in feet:r((a,y,b,y+1),'i');r((a,y,b,y),'d');r((a,y+1,b,y+1),'g')
 # Eleven-row head in all directions; rear crown/nape width changes projection.
 for j,(a,b) in enumerate(heads[dr]):
  y=11+j+dy;r((a,y,b,y),'i')
  if b-a>=3:
   r((a+1,y,b-1,y),'m')
   if j>0 and j<9:r((a+1,y,max(a+1,b-2),y),'l')
   if 0<j<4:r((a+2,y,max(a+2,b-3),y),'h')
 if dr=='west':ur((6,17,6,18),'i');ur((11,17,12,19),'s');ur((11,18,11,18),'m')
 elif dr=='south':
  for x in (4,10):ur((x,17,x,18),'i')
  ur((2,17,2,18),'m');ur((13,17,13,18),'m')
 else:ur((2,17,2,18),'m');ur((13,17,13,18),'m')
 return im
frames={1:{dr:{po:native(dr,po) for po in ['idle','A','P','C']} for dr in ['south','north','west','east']}}
fnt=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',13)
def save(s):
 for dr in frames[s]:
  for po,q in frames[s][dr].items():q.save(out/f'dummy-{s}x-{dr}-{po}.png')
def sheet(scales,name):
 b=Image.new('RGB',(480*len(scales),1120),'#eee8d1');d=ImageDraw.Draw(b)
 for row,dr in enumerate(['south','north','west','east']):
  for col,(s,po) in enumerate((s,p) for s in scales for p in ['idle','A','P','C']):
   x=col*120;y=row*280;q=frames[s][dr][po];d.text((x+4,y+5),f'{dr} {s}x {po}',font=fnt,fill=pal['i']);big=q.resize((80,160),Image.Resampling.NEAREST);b.paste(big,(x+10,y+35),big);b.paste(q,(x+10,y+200),q)
 b.save(out/name)
save(1);sheet([1],'native-all-poses-internal.png')
assert frames[1]['west']['idle'].tobytes()==baseline.tobytes()
print('Native16pose set written. Inspect actual native silhouettes before refinement.')
# Deliberate32x64 counterpart follows actual native inspection; independent native maps.
# No resampling is used to author the final pixels.
highHeads={
'south':[(13,18),(11,20),(9,22),(8,23),(7,24),(6,25),(6,25),(6,25),(5,26),(4,27),(4,27),(4,27),(4,27),(4,27),(4,27),(5,26),(6,25),(6,25),(8,23),(9,22),(10,21),(11,20)],
'north':[(11,20),(10,21),(8,23),(7,24),(6,25),(6,25),(5,26),(4,27),(4,27),(4,27),(4,27),(4,27),(4,27),(4,27),(4,27),(5,26),(6,25),(6,25),(6,25),(7,24),(8,23),(9,22)],
'west':[(13,20),(12,21),(9,23),(8,24),(8,25),(8,25),(7,25),(6,25),(6,26),(6,26),(6,27),(6,27),(6,27),(7,26),(8,25),(8,24),(8,23),(9,22),(10,21),(10,21),(12,19),(13,18)]}
def refined(dr,po):
 if dr=='east':return refined('west',po).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 im=Image.new('RGBA',(32,64));d=ImageDraw.Draw(im);dy=-2 if po=='P' else 0
 def r(box,c):d.rectangle(box,fill=pal[c])
 def p(pts,c):d.polygon(pts,fill=pal[c])
 def up(pts,c):p([(x,y+dy) for x,y in pts],c)
 def ur(box,c):a,b,cx,de=box;r((a,b+dy,cx,de+dy),c)
 if dr=='west':
  up([(14,38),(20,38),(23,41),(25,43),(25,50),(23,54),(10,54),(8,50),(8,44),(11,41)],'i');up([(14,40),(20,40),(23,43),(23,50),(21,52),(11,52),(10,49),(11,44)],'r');ur((22,43,23,50),'d');ur((16,48,20,49),'w')
  if po in ['idle','P']:
   p([(10,52),(23,52),(23,56),(21,58),(13,58),(10,56)],'n');p([(12,52),(21,52),(21,55),(12,55)],'b');r((13,53,17,53),'a');feet=[(12,21,58)]
  elif po=='A':
   p([(10,52),(22,52),(25,56),(23,59),(20,59),(16,57),(9,57),(7,56),(8,54)],'n');p([(12,52),(21,52),(22,54),(16,56),(10,55)],'b');r((13,53,17,53),'a');feet=[(8,15,56),(20,25,58)]
  else:
   p([(10,52),(22,52),(25,54),(25,57),(21,57),(16,58),(14,59),(10,59),(8,56)],'n');p([(12,52),(21,52),(21,54),(15,56),(10,55)],'b');r((13,53,17,53),'a');feet=[(10,15,58),(20,27,56)]
  hx=6 if po=='A' else 20 if po=='C' else 8;hy=48+dy
  # Warm contour at skin edge, two-dimensional palm beneath cuff, no ink cage.
  ur((hx,46,hx+5,47),'w');p([(hx,hy),(hx+4,hy),(hx+5,hy+1),(hx+5,hy+3),(hx+3,hy+5),(hx+1,hy+5),(hx,hy+3)],'s');r((hx+1,hy,hx+4,hy+3),'m');r((hx+2,hy,hx+3,hy+1),'l')
 else:
  up([(10,38),(21,38),(25,42),(27,47),(27,51),(24,54),(7,54),(4,51),(4,47),(6,42)],'i');up([(10,40),(21,40),(24,43),(24,50),(22,52),(9,52),(7,49),(7,44)],'r');up([(6,46),(10,46),(10,49),(5,49)],'w');up([(22,46),(25,46),(26,49),(22,49)],'g');ur((10,48,21,49),'w')
  p([(8,52),(23,52),(24,55),(22,58),(18,58),(16,56),(14,58),(9,58),(7,56)],'n');r((10,52,21,53),'b');r((11,54,13,54),'a')
  for x,shift in [(4,-2 if po=='A' else 0),(24,-2 if po=='C' else 0)]:
   y=50+dy+shift;p([(x,y),(x+3,y),(x+3,y+3),(x+2,y+4),(x,y+3)],'s');r((x+1,y,x+2,y+2),'m');r((x+1,y,x+1,y+1),'l')
  feet=[(8,13,58),(18,23,58)] if po in ['idle','P'] else ([(6,13,58),(18,23,56)] if po=='A' else [(8,13,56),(18,25,58)])
 for a,b,y in feet:
  p([(a+1,y),(b-1,y),(b,y+1),(b,y+2),(b-1,y+3),(a,y+3),(a-1,y+2),(a,y+1)],'i');r((a+1,y+1,b-1,y+1),'d');r((a+1,y+2,b-1,y+2),'g')
 for j,(a,b) in enumerate(highHeads[dr]):
  y=22+j+dy;r((a,y,b,y),'i')
  if b-a>=3:
   r((a+1,y,b-1,y),'m')
   if 1<=j<18:r((a+1,y,max(a+1,b-4),y),'l')
   if 2<=j<7 and b-a>=8:r((a+3,y,b-5,y),'h')
 if dr=='west':ur((12,34,13,37),'i');up([(22,34),(24,34),(25,35),(25,38),(23,40),(22,39)],'s');ur((23,35,24,37),'m')
 elif dr=='south':
  for x in (8,20):ur((x,34,x+1,37),'i')
  ur((4,34,5,37),'m');ur((26,34,27,37),'m')
 else:ur((4,34,5,37),'m');ur((26,34,27,37),'m')
 return im
frames[2]={dr:{po:refined(dr,po) for po in ['idle','A','P','C']} for dr in ['south','north','west','east']}
save(2);sheet([1,2],'all-poses-native-refined-internal.png')
# Same display size and true native thumbnails; fully transparent source PNGs.
def compare(poses,dirs,name):
 b=Image.new('RGB',(960,len(poses)*len(dirs)*220),'#eee8d1');d=ImageDraw.Draw(b)
 for j,(dr,po) in enumerate((dr,po) for dr in dirs for po in poses):
  y=j*220;d.text((10,y+5),f'INTERNAL {dr.upper()} {po} / same compact construction',font=fnt,fill=pal['i'])
  for k,s in enumerate([1,2]):
   q=frames[s][dr][po];x=30+k*480;big=q.resize((80,160),Image.Resampling.NEAREST);b.paste(big,(x,y+35),big);b.paste(q,(x+150,y+90),q);d.text((x+250,y+60),f'{16*s}x{32*s}\nNative + equal display',font=fnt,fill=pal['b'])
 b.save(out/name)
compare(['idle'],['south','north','west','east'],'four-direction-resolution-comparison.png')
compare(['idle','A','P','C'],['west'],'west-gait-resolution-comparison.png')
print('Refined32x64 independent maps written. Actual full-set visual check required.')
# Art-only temporal review files. Hold order/cadence is a proposed presentation.
order=['A','A','P','P','C','C','P','P'];manifest={};gifProof=[]
for s in [1,2]:
 for dr in frames[s]:
  for po,q in frames[s][dr].items():
   path=out/f'dummy-{s}x-{dr}-{po}.png';manifest[path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':q.size,'paintedBounds':q.getbbox(),'headCrownRow':(10 if po=='P' else 11)*s,'headChinRow':(21 if po!='P' else 20)*s+(s-1),'eyeRows':[(16 if po=='P' else 17)*s,(18 if po=='P' else 19)*s-1] if dr!='north' else None,'headHeight':11*s,'shoulderHiddenStart':(18 if po=='P' else 19)*s,'soleMaxRow':31*s-1}
   assert q.size==(16*s,32*s)
   rgba={tuple(bytes.fromhex(v[1:]))+(255,) for v in pal.values()}|{(0,0,0,0)};assert set(q.get_flattened_data())<=rgba
   assert q.getbbox()[1]==(10 if po=='P' else 11)*s
   pts={(x,y) for y in range(q.height) for x in range(q.width) if q.getpixel((x,y))[3]};left=set(pts);stack=[left.pop()]
   while stack:
    x,y=stack.pop()
    for k in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if k in left:left.remove(k);stack.append(k)
   assert not left,(s,dr,po,'detached silhouette')
   if dr=='east':assert q.tobytes()==frames[s]['west'][po].transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
  for mag in [1,4]:
   seq=[]
   for po in order:
    q=frames[s][dr][po];bg=Image.new('RGBA',q.size,'#eee8d1');bg.alpha_composite(q);seq.append(bg.convert('RGB').resize((16*s*mag,32*s*mag),Image.Resampling.NEAREST))
   path=out/f'dummy-{s}x-{dr}-walk-{mag}display.gif';seq[0].save(path,save_all=True,append_images=seq[1:],duration=100,loop=0,optimize=False,disposal=2)
   saved=Image.open(path);actual=[];holds=[]
   for n in range(saved.n_frames):
    saved.seek(n);hold=saved.info.get('duration',0);assert hold>0 and hold%100==0;holds.append(hold);actual.extend([saved.convert('RGB').tobytes()]*(hold//100))
   assert actual==[q.tobytes() for q in seq] and sum(holds)==800 and saved.info.get('loop')==0
   gifProof.append({'path':path.name,'savedFrames':saved.n_frames,'holdsMs':holds,'loopMs':800,'decodedPixelsExact':True,'logicalSlots':8})
assert frames[1]['west']['idle'].tobytes()==baseline.tobytes()
(src/'native-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(src/'gif-checks.json').write_text(json.dumps(gifProof,indent=2)+'\n')
print('32connected native PNGs;16 saved GIFs decoded exact at128logical slots. No appearance acceptance implied.')
