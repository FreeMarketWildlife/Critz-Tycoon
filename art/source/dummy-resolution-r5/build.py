"""DS5 side arm/torso revision. Native side gait first; compact heads/shoes protected."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import ast,json,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-DS5';src=Path(__file__).parent
mod=ast.parse((root/'art/source/dummy-resolution-r1/build.py').read_text());pal=next(ast.literal_eval(n.value) for n in mod.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='pal');rgba={k:tuple(bytes.fromhex(v[1:]))+(255,) for k,v in pal.items()}
feet={'idle':[(6,10,29)],'P':[(6,10,29)],'A':[(4,7,28),(10,12,29)],'C':[(5,7,29),(10,13,28)]}
frames={1:{'west':{},'east':{}}};records={}
for po in ['idle','A','P','C']:
 old=Image.open(root/f'docs/reviews/M1-DS4/dummy-1x-west-{po}.png').convert('RGBA');im=old.copy();d=ImageDraw.Draw(im);dy=-1 if po=='P' else 0;cut=22+dy;shoe={(x,y) for a,b,y0 in feet[po] for y in [y0,y0+1] for x in range(a,b+1)}
 d.rectangle((0,cut,15,31),fill=(0,0,0,0))
 def r(box,c):d.rectangle(box,fill=pal[c])
 def p(pts,c):d.polygon(pts,fill=pal[c])
 def up(pts,c):p([(x,y+dy) for x,y in pts],c)
 def ur(box,c):a,b,cx,de=box;r((a,b+dy,cx,de+dy),c)
 # Far arm is behind garment: only its contact-side sliver may remain visible.
 if po=='A':ur((11,24,12,25),'s')
 if po=='C':ur((5,24,5,25),'s')
 # Three-row visible shirt with a tapered hem, no horizontal sleeve/skin bridge.
 up([(6,22),(10,22),(11,23),(11,24),(10,25),(6,25),(5,24),(5,23)],'i');ur((6,22,10,23),'r');ur((6,24,10,24),'d');ur((10,22,10,23),'d')
 # Existing complete clothed legs/feet remain the lower construction basis.
 for y in range(26,29):
  for x in range(16):
   q=old.getpixel((x,y))
   if q in {rgba[k] for k in ['i','n','b','a']}:im.putpixel((x,y),q)
 r((6,25,10,25),'b');r((6,26,10,26),'b')
 # Fixed projected shoulder(8,22) -> sleeve -> hanging palm. Swing pivots here.
 if po in ['idle','P']:
  ur((8,22,9,22),'w');ur((8,23,9,23),'g');ur((8,24,9,25),'m');ur((10,24,10,25),'s');ur((8,24,8,24),'l');ur((9,26,9,26),'s')
 elif po=='A':
  up([(8,22),(9,22),(8,24),(6,25),(5,24),(7,23)],'g');up([(8,22),(8,23),(7,23)],'w');ur((5,25,6,26),'m');ur((4,25,4,26),'s');ur((5,25,5,25),'l');ur((5,27,5,27),'s')
 else:
  up([(8,22),(9,22),(11,24),(11,25),(9,24),(8,23)],'g');up([(8,22),(8,23),(9,23)],'w');ur((10,25,11,26),'m');ur((12,25,12,26),'s');ur((10,25,10,25),'l');ur((11,27,11,27),'s')
 # Authoritative original foot regions, never shrunk to compensate for torso.
 for xy in shoe:im.putpixel(xy,old.getpixel(xy))
 assert im.crop((0,0,16,cut)).tobytes()==old.crop((0,0,16,cut)).tobytes()
 assert all(im.getpixel(xy)==old.getpixel(xy) for xy in shoe)
 assert im.crop((0,28,16,32)).tobytes()==old.crop((0,28,16,32)).tobytes()
 frames[1]['west'][po]=im;frames[1]['east'][po]=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT);records[po]={'protectedAboveRow':cut,'headExactDS4':True,'shoePixelsExactDS4':True,'nearShoulder':[8,22+dy],'nativeShirtVisibleRows':[22+dy,24+dy],'sourceContactPair':{'A':[7,8],'P':[2,2],'C':[8,7],'idle':[2,2]}[po]}
fnt=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',13)
def save(s):
 for dr in frames[s]:
  for po,q in frames[s][dr].items():q.save(out/f'dummy-{s}x-{dr}-{po}.png')
def sheet(scales,name):
 b=Image.new('RGB',(480*len(scales),560),'#eee8d1');d=ImageDraw.Draw(b)
 for row,dr in enumerate(['west','east']):
  for col,(s,po) in enumerate((s,p) for s in scales for p in ['idle','A','P','C']):
   x=col*120;y=row*280;q=frames[s][dr][po];d.text((x+4,y+5),f'{dr} {s}x {po}',font=fnt,fill=pal['i']);big=q.resize((64,128),Image.Resampling.NEAREST);b.paste(big,(x+10,y+35),big);b.paste(q,(x+10,y+200),q)
 b.save(out/name)
save(1);sheet([1],'native-side-gait-internal.png');(src/'construction.json').write_text(json.dumps(records,indent=2)+'\n')
print('Native8sideposes written. Compacthead/shoes exactDS4. Inspect native motion before refinement.')
order=['A','A','P','P','C','C','P','P']
def loops(scales):
 for s in scales:
  for dr in ['west','east']:
   for slow in [1,4]:
    seq=[]
    for po in order:
     q=frames[s][dr][po];bg=Image.new('RGBA',q.size,'#eee8d1');bg.alpha_composite(q);seq.append(bg.convert('RGB').resize((16*s*4,32*s*4),Image.Resampling.NEAREST))
    seq[0].save(out/(f'dummy-{s}x-{dr}-walk-'+('normal' if slow==1 else 'slow')+'.gif'),save_all=True,append_images=seq[1:],duration=100*slow,loop=0,optimize=False,disposal=2)
loops([1])
(out/'native-motion-review.html').write_text('''<!doctype html><meta charset="utf-8"><title>DS5 internal native motion</title><style>body{background:#eee8d1;color:#292634;font:16px monospace}section{display:inline-block;margin:24px}img{width:96px;height:192px;image-rendering:pixelated}h1{font-size:18px}</style><h1>INTERNAL DS5 native side cycle — no game/storage</h1><div id="label"></div><section>West<br><img id="west"></section><section>East<br><img id="east"></section><script>const seq=['A','A','P','P','C','C','P','P'];const start=performance.now();function show(){const t=performance.now()-start;const n=Math.floor(t/400)%8;for(const dr of ['west','east'])document.getElementById(dr).src='dummy-1x-'+dr+'-'+seq[n]+'.png';document.getElementById('label').textContent='Slow review slot '+(n+1)+'/8 · '+seq[n]+' · cycle '+Math.floor(t/3200);requestAnimationFrame(show)}show()</script>''')
# After actual native full-side/static and browser playback inspection: deliberate2x.
frames[2]={'west':{},'east':{}}
feet2={'idle':[(12,21,58)],'P':[(12,21,58)],'A':[(8,15,56),(20,25,58)],'C':[(10,15,58),(20,27,56)]}
for po in ['idle','A','P','C']:
 old=Image.open(root/f'docs/reviews/M1-DS4/dummy-2x-west-{po}.png').convert('RGBA');im=old.copy();d=ImageDraw.Draw(im);dy=-2 if po=='P' else 0;cut=44+dy
 mask=Image.new('L',(32,64));md=ImageDraw.Draw(mask)
 for a,b,y in feet2[po]:md.polygon([(a+1,y),(b-1,y),(b,y+1),(b,y+2),(b-1,y+3),(a,y+3),(a-1,y+2),(a,y+1)],fill=255)
 shoe={(x,y) for y in range(64) for x in range(32) if mask.getpixel((x,y))}
 d.rectangle((0,cut,31,63),fill=(0,0,0,0))
 def r(box,c):d.rectangle(box,fill=pal[c])
 def p(pts,c):d.polygon(pts,fill=pal[c])
 def up(pts,c):p([(x,y+dy) for x,y in pts],c)
 def ur(box,c):a,b,cx,de=box;r((a,b+dy,cx,de+dy),c)
 # Far arm precedes garment; its residual edge is naturally partially occluded.
 if po=='A':up([(22,47),(25,48),(25,51),(23,52),(22,50)],'s')
 if po=='C':up([(10,47),(12,48),(12,51),(10,52),(9,50)],'s')
 up([(12,44),(20,44),(22,45),(23,47),(22,49),(20,51),(12,51),(10,48),(10,46)],'i');up([(12,44),(20,44),(21,46),(20,49),(12,49),(11,47)],'r');ur((20,45,21,48),'d');ur((12,48,20,49),'d')
 for y in range(52,58):
  for x in range(32):
   q=old.getpixel((x,y))
   if q in {rgba[k] for k in ['i','n','b','a']}:im.putpixel((x,y),q)
 p([(12,50),(20,50),(22,51),(21,53),(12,53),(11,52)],'b');r((13,51,17,51),'a')
 # Same pivot16,44 and low-resolution arm ownership, refined native boundaries.
 if po in ['idle','P']:
  up([(16,44),(18,44),(19,45),(19,47),(16,47)],'g');ur((16,44,18,45),'w');up([(16,48),(19,48),(20,49),(20,51),(18,53),(16,52),(15,50)],'s');ur((16,48,18,51),'m');ur((16,48,17,49),'l')
 elif po=='A':
  up([(16,44),(18,44),(18,46),(15,49),(12,51),(10,49),(12,47),(14,46)],'g');up([(16,44),(17,44),(17,46),(15,47),(14,46)],'w');up([(10,50),(13,50),(14,51),(13,54),(11,55),(9,53),(9,51)],'s');ur((10,50,12,53),'m');ur((10,50,11,51),'l')
 else:
  up([(16,44),(18,44),(20,46),(23,49),(23,51),(20,51),(18,48),(16,47)],'g');up([(16,44),(17,44),(18,46),(19,47),(17,47),(16,46)],'w');up([(21,50),(23,50),(25,51),(25,53),(23,55),(21,54),(20,52)],'s');ur((21,50,23,53),'m');ur((21,50,22,51),'l')
 for xy in shoe:im.putpixel(xy,old.getpixel(xy))
 # Lower gait is outside the shoulder/torso edit, including navy join cells.
 im.paste(old.crop((0,56,32,64)),(0,56))
 assert im.crop((0,56,32,64)).tobytes()==old.crop((0,56,32,64)).tobytes()
 assert im.crop((0,0,32,cut)).tobytes()==old.crop((0,0,32,cut)).tobytes()
 assert all(im.getpixel(xy)==old.getpixel(xy) for xy in shoe)
 frames[2]['west'][po]=im;frames[2]['east'][po]=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 records[po]['refinedProtectedAbove']=cut;records[po]['refinedShoeExactDS4']=True;records[po]['refinedShoulder']=[16,44+dy]
save(2);sheet([1,2],'side-gait-native-refined-internal.png');loops([2]);(src/'construction.json').write_text(json.dumps(records,indent=2)+'\n')
# Idle equal display old/new roles, native thumbnails for both resolutions.
b=Image.new('RGB',(960,460),'#eee8d1');d=ImageDraw.Draw(b)
for row,dr in enumerate(['west','east']):
 for col,(s,oldnew) in enumerate([(1,'old'),(1,'new'),(2,'old'),(2,'new')]):
  x=col*240;y=row*230;q=Image.open(root/f'docs/reviews/{"M1-DS4" if oldnew=="old" else "M1-DS5"}/dummy-{s}x-{dr}-idle.png').convert('RGBA');d.text((x+4,y+4),f'{dr} {s}x {oldnew} / INTERNAL',font=fnt,fill=pal['i']);big=q.resize((64,128),Image.Resampling.NEAREST);b.paste(big,(x+20,y+30),big);b.paste(q,(x+150,y+100),q)
b.save(out/'idle-arm-role-before-after.png')
print('16sideposes nowbuilt; actual complete/refined and motion inspection required.')
(out/'paired-motion-review.html').write_text('''<!doctype html><meta charset="utf-8"><title>DS5 internal paired side motion</title><style>body{background:#eee8d1;color:#292634;font:16px monospace}section{display:inline-block;margin:18px}img{width:64px;height:128px;image-rendering:pixelated}h1{font-size:18px}</style><h1>INTERNAL DS5 synchronized side cycle</h1><div id="label"></div><section>West16x32<br><img id="west1"></section><section>West32x64<br><img id="west2"></section><section>East16x32<br><img id="east1"></section><section>East32x64<br><img id="east2"></section><script>const seq=['A','A','P','P','C','C','P','P'];const start=performance.now();function show(){const t=performance.now()-start;const n=Math.floor(t/400)%8;for(const dr of ['west','east'])for(const s of [1,2])document.getElementById(dr+s).src='dummy-'+s+'x-'+dr+'-'+seq[n]+'.png';document.getElementById('label').textContent='Slow review slot '+(n+1)+'/8 · '+seq[n]+' · cycle '+Math.floor(t/3200);requestAnimationFrame(show)}show()</script>''')
# Verify actual saved artwork/animations rather than asserting visual approval.
manifest={};gifproof=[]
for s in [1,2]:
 for dr in ['west','east']:
  for po,q in frames[s][dr].items():
   assert q.size==(16*s,32*s)
   assert set(q.get_flattened_data())<=set(rgba.values())|{(0,0,0,0)}
   points={(x,y) for y in range(q.height) for x in range(q.width) if q.getpixel((x,y))[3]};left=set(points);stack=[left.pop()]
   while stack:
    x,y=stack.pop()
    for k in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if k in left:left.remove(k);stack.append(k)
   assert not left,(s,dr,po,'detached skin or cloth')
   if dr=='east':assert q.tobytes()==frames[s]['west'][po].transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
   path=out/f'dummy-{s}x-{dr}-{po}.png';manifest[path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bounds':q.getbbox(),'dimensions':q.size,'connectedSilhouette':True}
  for slow in [1,4]:
   path=out/(f'dummy-{s}x-{dr}-walk-'+('normal' if slow==1 else 'slow')+'.gif');g=Image.open(path);actual=[];holds=[]
   for n in range(g.n_frames):
    g.seek(n);hold=g.info.get('duration',0);assert hold>0 and hold%(100*slow)==0;holds.append(hold);actual.extend([g.convert('RGB').tobytes()]*(hold//(100*slow)))
   expected=[]
   for po in order:
    q=frames[s][dr][po];bg=Image.new('RGBA',q.size,'#eee8d1');bg.alpha_composite(q);expected.append(bg.convert('RGB').resize((16*s*4,32*s*4),Image.Resampling.NEAREST).tobytes())
   assert actual==expected and sum(holds)==800*slow and g.info.get('loop')==0
   gifproof.append({'file':path.name,'savedFrames':g.n_frames,'holdsMs':holds,'loopMs':sum(holds),'logicalSlots':8,'actualDecodedPixelsExact':True})
(src/'native-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(src/'gif-checks.json').write_text(json.dumps(gifproof,indent=2)+'\n')
print('16 connected sideposes;8 actualGIFs decoded exact (64 logical slots). Compacthead/shoes protected.')
