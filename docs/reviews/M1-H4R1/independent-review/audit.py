from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import json,hashlib,subprocess,io
R=Path(__file__).resolve().parents[4]; O=Path(__file__).parent; D=R/'docs/reviews/M1-H4R1'; S=R/'art/source/four-direction-refinement-r1'; checks=[]; facts={}
def ck(n,v):
 checks.append({'check':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
def load(p):return Image.open(p).convert('RGBA')
def raw(q):return q.tobytes()
def same(a,b):return raw(a)==raw(b)
def runs(q,y):
 xs=[x for x in range(q.width) if q.getpixel((x,y))[3]]; rr=[]
 for x in xs:
  if rr and rr[-1][1]==x:rr[-1][1]+=1
  else:rr.append([x,x+1])
 return rr
rec=json.loads((S/'changes.json').read_text())['source']; corr=json.loads((S/'correspondence.json').read_text()); restore=json.loads((R/'art/source/shared-template-restoration-r1/restoration.json').read_text())
for dr in ['south','north','west','east']:
 for po in ['idle','A','P','C']:
  tag=dr+'-'+po; p=D/tag; rr=rec[dr][po]; hero=load(p/'master-hero.png'); bald=load(p/'master-bald.png'); oh=load(R/rr['heroInput']); ob=load(R/rr['baldInput']); pin='3b6270e93c8cead6a9d450c603697094741c4967' if dr in ['west','east'] else 'ebccf4cfe894d69af3c6dfda6e3fe58caa313f31'
  for f in ['heroInput','baldInput']:ck(tag+' pinned input '+f,subprocess.check_output(['git','show',pin+':'+rr[f]])==(R/rr[f]).read_bytes())
  for name,q,old in [('hero',hero,oh),('bald',bald,ob)]:
   ck(tag+name+' alpha preserved',same(q.getchannel('A'),old.getchannel('A')));ck(tag+name+' top54 exact',same(q.crop((0,0,32,54)),old.crop((0,0,32,54))));ck(tag+name+' palette source',set(q.get_flattened_data())<=set(old.get_flattened_data()));y=old.getbbox()[3]-1;ck(tag+name+' contact RGBA exact',same(q.crop((0,y,32,y+1)),old.crop((0,y,32,y+1))))
   if dr!='north':ck(tag+name+' protected entire RGBA',same(q,old))
  changes=[(x,y) for y in range(64) for x in range(32) if hero.getpixel((x,y))!=oh.getpixel((x,y))];ck(tag+' actual declared changes',changes==[tuple(e['xy']) for e in rr['masterChanges']]);ck(tag+' identical bald material delta',all(bald.getpixel(pt)==hero.getpixel(pt) and ob.getpixel(pt)==oh.getpixel(pt) for pt in changes))
  if dr=='north':
   ink=(36,35,48,255);exterior=[]
   for y in range(64):
    for x in range(32):
     if oh.getpixel((x,y))[3] and any(not(0<=x+dx<32 and 0<=y+dy<64) or oh.getpixel((x+dx,y+dy))[3]==0 for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]):exterior.append((x,y))
   ck(tag+' exterior pixels exact',all(hero.getpixel(pt)==oh.getpixel(pt) for pt in exterior));ck(tag+' ink pixels exact',all(hero.getpixel((x,y))==ink for y in range(64) for x in range(32) if oh.getpixel((x,y))==ink))
  q=bald.copy()
  for pt in restore['poses'][dr][po]['hairHiddenScalpCutoutCells']:q.putpixel(tuple(pt),(0,0,0,0))
  q.alpha_composite(load(p/'master-hair-shadow.png'));q.alpha_composite(load(p/'master-hair.png'));ck(tag+' master actual layer recomposition',same(q,hero))
  nh=load(p/'native-hero.png');nb=load(p/'native-bald.png');q=nb.copy();cut=load(p/'native-scalp-cutout.png')
  for y in range(32):
   for x in range(16):
    if cut.getpixel((x,y))[3]:q.putpixel((x,y),(0,0,0,0))
  for f in ['native-hair-shadow.png','native-hair.png']:q.alpha_composite(load(p/f))
  ck(tag+' native real layers recompose',same(q,nh));hb=23-int(po=='P');ck(tag+' native shared body',same(nh.crop((0,hb,16,32)),nb.crop((0,hb,16,32))));ck(tag+' native size',nh.size==nb.size==(16,32));ck(tag+' native binary alpha',set(nh.getchannel('A').get_flattened_data())<=set([0,255]));ck(tag+' native palette source',set(nh.get_flattened_data())<=set(hero.get_flattened_data()) and set(nb.get_flattened_data())<=set(bald.get_flattened_data()));my=hero.getbbox()[3]-1;ny=nh.getbbox()[3]-1;mr=runs(hero,my);nr=runs(nh,ny);ck(tag+' contact row floor',ny==my//2);ck(tag+' contact exact half widths',len(mr)==len(nr) and all((b-a)==2*(d-c) for (a,b),(c,d) in zip(mr,nr)));ck(tag+' contact edge <=1',all(abs(2*c-a)<=1 and abs(2*d-b)<=1 for (a,b),(c,d) in zip(mr,nr)))
  facts[tag]={'masterChanges':len(changes),'masterContact':mr,'nativeContact':nr,'masterBaldBounds':bald.getbbox(),'nativeBaldBounds':nb.getbbox(),'nativePackBounds':load(p/'native-observed-pack.png').getbbox()}
# Explicit original front hash, historical fruit and creator archives.
ck('protected South idle file hash',hashlib.sha256((D/'south-idle/master-hero.png').read_bytes()).hexdigest()=='f959249734d6c588e433bb84f1de9435820b738235d568d15c8cbf8964fdb4ae')
for f in subprocess.check_output(['git','ls-tree','-r','--name-only','22204fc','docs/reviews/M1-FR1']).decode().splitlines():ck('historical fruit '+f,subprocess.check_output(['git','show','22204fc:'+f])==(R/f).read_bytes())
ck('creator no changes since pre-H4R1',not subprocess.check_output(['git','diff','22204fc','--','character-creator']))
# Validate ALL actual GIF pixels via their source panel placements, holds and loops.
order=['A','A','P','P','C','C','P','P']; gif_count=0
for dr in ['south','north','west','east']:
 for speed,mul in [('normal',1),('slow',4)]:
  f=D/(dr+'-paired-existing-walk-'+speed+'.gif');g=Image.open(f);ck(f.name+' 8 slots',g.n_frames==8);ck(f.name+' loop',g.info.get('loop')==0)
  for i,po in enumerate(order):
   g.seek(i);im=g.convert('RGB');ck(f.name+str(i)+' hold',g.info['duration']==mul*([100]*8 if dr=='south' else [70,60,70,70,70,60,70,70])[i])
   for j,(name,sc) in enumerate([('master-hero.png',3),('master-bald.png',3),('native-hero.png',6),('native-bald.png',6)]):
    src=load(D/(dr+'-'+po)/name);bg=Image.new('RGBA',src.size,'#eee8d1');bg.alpha_composite(src);expected=bg.convert('RGB').resize((96,192),Image.Resampling.NEAREST)
    ck(f.name+str(i)+name+' saved panel exact',im.crop((j*260+15,27,j*260+111,219)).tobytes()==expected.tobytes())
   gif_count+=1
(O/'saved-audit.json').write_text(json.dumps({'sourceSHA':'2c8fa4fef4c6872b05fce294a82b09f873876a6e','passed':len(checks),'checks':checks,'poses':facts,'decodedGifFrames':gif_count},indent=2)+'\n')
# Crops are mechanical review aids, not art modifications.
big=Image.open(D/'all-direction-poses.png')
for j,dr in enumerate(['south','north','west','east']):big.crop((0,j*1040,1040,(j+1)*1040)).save('/tmp/h4r1-'+dr+'-poses.png')
# Actual external indexed source; palette index0 removed, all North poses shown.
plate=Image.new('RGBA',(768,290),'#eee8d1');draw=ImageDraw.Draw(plate)
for row,file in enumerate(['brendan-walking.png','man_1.png']):
 strip=Image.open('/tmp/ds1-primary-reference/'+file)
 for col,idx in enumerate([1,5,6]):
  q=strip.crop((idx*16,0,idx*16+16,32)).convert('RGBA');indices=strip.crop((idx*16,0,idx*16+16,32));alpha=Image.new('L',(16,32));alpha.putdata([0 if v==0 else 255 for v in indices.get_flattened_data()]);q.putalpha(alpha);plate.alpha_composite(q.resize((64,128),Image.Resampling.NEAREST),(col*256+40,row*145+15));draw.text((col*256+110,row*145+45),file+' index'+str(idx),fill='#242330')
plate.convert('RGB').save('/tmp/h4r1-actual-primary-north.png')
print(json.dumps({'checks':len(checks),'GIFframes':gif_count,'source': '2c8fa4f'}))
