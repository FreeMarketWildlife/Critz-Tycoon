"""M1.ON1: original four-idle Nugget candidate. No runtime/shared output."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib

S=Path(__file__).resolve().parent
R=S.parents[2]
O=R/'docs/reviews/M1-ON1'
P={'ink':'#302b29','hatDark':'#6c6043','hat':'#bfab77','hatLight':'#e4d09a',
   'band':'#3b5943','bandLight':'#708661','hairDark':'#798987','hair':'#a8b4af','hairLight':'#d2d7c8',
   'skinDark':'#ad714f','skin':'#d29b68','skinLight':'#edbb83','coatDark':'#b9bea9',
   'coat':'#e1e3cf','coatLight':'#f7edcc','shirtDark':'#526a50','shirt':'#78966b',
   'pantsDark':'#514539','pants':'#8b8159','shoeDark':'#343537','shoe':'#60696a','shoeLight':'#9aa6a4','lens':'#e7efeb'}
def rgba(c):return tuple(bytes.fromhex(P[c][1:]))+(255,)
def fresh():return {}
def layer(ls,n):
 if n not in ls:ls[n]=Image.new('RGBA',(32,64))
 return ls[n]
def poly(ls,n,xy,c):ImageDraw.Draw(layer(ls,n)).polygon(xy,fill=rgba(c))
def rect(ls,n,xy,c):ImageDraw.Draw(layer(ls,n)).rectangle(xy,fill=rgba(c))
def point(ls,n,xy,c):layer(ls,n).putpixel(xy,rgba(c))
def frontal(back=False):
 ls=fresh()
 # RD1 external visible body is a construction guide, not accepted segmentation.
 rd=json.loads((R/'art/source/reference-dummy-r1/construction.json').read_text())
 owners={'torso':'coat','arms':'coat','hands':'skin','pelvis':'pants','left-leg':'pants','right-leg':'pants','left-shoe':'shoe','right-shoe':'shoe'}
 for n,c in owners.items():
  for x,y in rd['regions'][n]['cells']:point(ls,('hands' if n=='hands' else 'shoes' if 'shoe' in n else 'trousers' if n in ('pelvis','left-leg','right-leg') else 'coat'),(x,y),c)
 body=set(tuple(p) for n in owners for p in rd['regions'][n]['cells'])
 for x,y in body:
  if any((x+dx,y+dy) not in body for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]):point(ls,'body-outline',(x,y),'ink')
 # Overlapping coat shoulders: compact, under the head, no raised pads.
 poly(ls,'coat',[(8,44),(23,44),(25,47),(23,51),(22,55),(9,55),(8,51),(6,47)],'coatDark')
 poly(ls,'coat',[(9,44),(22,44),(23,47),(21,53),(10,53),(8,47)],'coat')
 for x in [8,23]:rect(ls,'coat-details',(x,48,x,52),'ink')
 for x in [5,26]:rect(ls,'coat-details',(x,49,x,50),'coatLight')
 if not back:
  poly(ls,'shirt',[(12,44),(19,44),(20,48),(19,54),(12,54),(11,48)],'shirtDark')
  rect(ls,'shirt',(14,46,17,53),'shirt')
  poly(ls,'lapels',[(10,44),(12,44),(14,47),(12,48),(12,54),(10,54)],'coatLight')
  poly(ls,'lapels',[(19,44),(21,44),(21,54),(19,54),(19,48),(17,47)],'coatLight')
  rect(ls,'coat-details',(10,51,11,51),'coatDark');rect(ls,'coat-details',(20,51,21,51),'coatDark')
 else:
  rect(ls,'coat-details',(11,47,20,47),'coatLight')
  rect(ls,'coat-details',(15,50,16,54),'coatDark')
  rect(ls,'coat-details',(10,54,21,54),'coat')
 # Material separation retains all full RD1 shoe cells and contact runs.
 for x,y in body:
  if y>=58:
   point(ls,'shoes',(x,y),'shoeDark' if y>=60 else 'shoe')
 for a,b in [(7,12),(19,24)]:rect(ls,'shoe-details',(a,59,b,59),'shoeLight')
 for x,y in body:
  if y>=58 and any((x+dx,y+dy) not in body for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]):point(ls,'shoe-details',(x,y),'ink')
 rect(ls,'trouser-details',(15,56,16,58),'ink')
 # Original silver hair, unchanged established costume cues; no pack.
 poly(ls,'hair',[(6,33),(25,33),(27,36),(26,42),(23,45),(8,45),(5,42),(4,36)],'ink')
 poly(ls,'hair',[(6,34),(25,34),(26,37),(25,41),(22,44),(9,44),(6,41),(5,37)],'hair')
 if back:
  poly(ls,'hair-light',[(7,35),(24,35),(24,39),(21,42),(10,42),(7,39)],'hairLight')
  poly(ls,'hair-shadow',[(7,40),(10,42),(21,42),(24,40),(23,43),(20,45),(11,45),(8,43)],'hairDark')
 else:
  poly(ls,'face',[(9,34),(22,34),(24,37),(24,41),(22,44),(19,46),(12,46),(9,44),(7,41),(7,37)],'ink')
  poly(ls,'face',[(10,34),(21,34),(23,37),(23,41),(21,43),(19,45),(12,45),(10,43),(8,41),(8,37)],'skin')
  poly(ls,'face-light',[(10,35),(20,35),(22,37),(21,40),(11,41),(9,39)],'skinLight')
  rect(ls,'face-shadow',(12,44,19,44),'skinDark')
  for x in [6,25]:rect(ls,'ears',(x,38,x,40),'skin')
  # Brows/glasses sit on the face; quiet bridge, no invented projecting nose.
  for x in [10,18]:
   rect(ls,'glasses',(x,36,x+4,41),'ink');rect(ls,'glasses',(x+1,37,x+3,40),'lens')
   rect(ls,'eyes',(x+2,38,x+2,40),'ink')
  rect(ls,'glasses',(14,37,18,37),'ink')
  rect(ls,'glasses',(7,37,10,37),'ink');rect(ls,'glasses',(22,37,24,37),'ink')
  for x in [6,24]:rect(ls,'hair-fringe',(x,35,x+1,38),'hairLight')
 # Broad field-hat top plane. Native slopes; no huge adult frame.
 poly(ls,'hat',[(11,23),(20,23),(23,25),(25,29),(27,31),(29,33),(28,35),(3,35),(2,33),(5,31),(7,28),(8,25)],'ink')
 poly(ls,'hat',[(11,24),(20,24),(22,26),(24,30),(7,30),(9,26)],'hat')
 poly(ls,'hat',[(11,24),(19,24),(21,26),(10,26),(8,29),(7,29),(9,25)],'hatLight')
 poly(ls,'hat-band',[(7,29),(24,29),(25,31),(6,31)],'band')
 rect(ls,'hat-band',(9,29,21,29),'bandLight')
 poly(ls,'hat-brim',[(5,32),(26,32),(28,33),(27,34),(4,34),(3,33)],'hat')
 rect(ls,'hat-brim',(5,32,24,32),'hatLight')
 for p in [(5,30),(4,31),(3,32)]:point(ls,'hat',p,'ink')
 return ls

def profile():
 ls=fresh()
 # Deliberate original profile: compact torso and leg overlap from primary strips.
 poly(ls,'trousers',[(11,52),(22,52),(23,56),(22,59),(9,59),(8,57)],'ink')
 poly(ls,'trousers',[(12,53),(21,53),(21,57),(18,59),(10,58)],'pants')
 poly(ls,'far-shoe',[(17,58),(23,58),(24,60),(22,61),(16,61),(15,60)],'ink')
 rect(ls,'far-shoe',(18,59,22,60),'shoe')
 poly(ls,'near-shoe',[(10,57),(18,57),(19,59),(18,61),(7,61),(6,60),(7,59)],'ink')
 poly(ls,'near-shoe',[(10,58),(17,58),(18,60),(8,60),(8,59)],'shoe')
 rect(ls,'shoe-highlight',(8,59,12,59),'shoeLight')
 poly(ls,'coat',[(12,43),(20,43),(23,46),(23,52),(21,55),(10,55),(8,52),(9,47)],'ink')
 poly(ls,'coat',[(12,44),(19,44),(22,47),(22,52),(20,54),(11,54),(9,51),(10,47)],'coatDark')
 poly(ls,'coat',[(12,44),(17,44),(18,49),(16,54),(11,54),(10,51)],'coat')
 rect(ls,'shirt',(9,47,10,52),'shirtDark')
 poly(ls,'sleeve',[(16,45),(20,46),(21,49),(20,51),(15,51),(14,49),(14,47)],'ink')
 poly(ls,'sleeve',[(16,46),(19,47),(20,49),(19,50),(15,50),(15,48)],'coatLight')
 poly(ls,'hand',[(16,50),(20,50),(21,52),(20,54),(17,55),(15,53),(15,51)],'ink')
 poly(ls,'hand',[(16,51),(19,51),(20,52),(19,54),(17,54),(16,53)],'skin')
 rect(ls,'hand-light',(16,51,17,52),'skinLight')
 poly(ls,'head',[(10,31),(21,31),(25,34),(26,38),(25,42),(22,45),(14,46),(9,44),(6,41),(6,36)],'ink')
 poly(ls,'head',[(10,32),(20,32),(23,35),(24,39),(22,42),(19,44),(13,45),(9,43),(7,41),(7,36)],'skin')
 poly(ls,'face-light',[(10,34),(17,34),(17,39),(13,42),(9,42),(8,40),(8,36)],'skinLight')
 poly(ls,'hair',[(18,33),(23,33),(25,35),(25,40),(23,43),(20,45),(16,44),(17,40)],'hairDark')
 poly(ls,'hair',[(19,34),(23,34),(24,36),(24,40),(21,43),(18,43),(18,40)],'hair')
 poly(ls,'hair-light',[(19,35),(23,35),(23,38),(21,40),(19,40)],'hairLight')
 poly(ls,'ear',[(17,38),(19,37),(21,38),(21,41),(19,43),(17,42)],'ink')
 poly(ls,'ear',[(18,38),(20,38),(20,41),(18,42)],'skin')
 point(ls,'ear',(19,40),'skinDark')
 rect(ls,'glasses',(6,36,11,41),'ink');rect(ls,'glasses',(7,37,10,40),'lens')
 rect(ls,'eyes',(8,38,8,40),'ink');rect(ls,'glasses',(11,37,18,37),'ink')
 poly(ls,'hat',[(12,23),(20,23),(23,25),(25,29),(26,31),(29,33),(28,35),(4,35),(2,34),(3,32),(7,30),(9,26)],'ink')
 poly(ls,'hat',[(12,24),(20,24),(22,26),(24,30),(8,30),(10,26)],'hat')
 poly(ls,'hat-light',[(12,24),(18,24),(20,26),(12,26),(9,29),(9,27)],'hatLight')
 poly(ls,'hat-band',[(8,29),(24,29),(25,31),(7,31)],'band')
 rect(ls,'hat-band',(10,29,21,29),'bandLight')
 poly(ls,'hat-brim',[(5,32),(26,32),(28,33),(27,34),(4,34),(3,33)],'hat')
 rect(ls,'hat-brim',(5,32,23,32),'hatLight')
 return ls

def composite(ls):
 q=Image.new('RGBA',(32,64))
 for im in ls.values():q.alpha_composite(im)
 return q
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 O.mkdir(exist_ok=True)
 ls={'south':frontal(),'north':frontal(True),'west':profile()}
 ls['east']={n:im.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for n,im in ls['west'].items()}
 record={'task':'M1.ON1','status':'awaiting root four-idle review','appearanceApproval':False,'palette':P,'frame':[32,64],'anchor':[16,64],'directions':{}}
 checks=[]
 for dr,layers in ls.items():
  q=composite(layers);q.save(O/f'{dr}-idle.png');(S/dr).mkdir(exist_ok=True)
  for n,im in layers.items():im.save(S/dr/f'{n}.png')
  # Editable per-layer RGBA rows: lossless sparse native pixels, not guessed part labels.
  src={n:{'pixels':[[i%32,i//32,*p] for i,p in enumerate(im.getdata()) if p[3]]} for n,im in layers.items()}
  (S/f'{dr}.layers.json').write_text(json.dumps({'frame':[32,64],'renderOrder':list(layers),'layers':src},indent=2)+'\n')
  assert set(q.getchannel('A').getdata())<={0,255}
  assert q.getbbox()[3]==62 and q.getchannel('A').crop((0,62,32,64)).getbbox() is None
  assert len({p for p in q.getdata() if p[3]})<=len(P)
  restored=Image.new('RGBA',(32,64))
  for n in src:
   a=Image.new('RGBA',(32,64))
   for x,y,*p in src[n]['pixels']:a.putpixel((x,y),tuple(p))
   restored.alpha_composite(a)
  assert restored.tobytes()==q.tobytes()
  checks.extend([dr+' binary alpha/frame/row61 contact',dr+' sparse layers exactly recompose',dr+' palette bounded'])
  record['directions'][dr]={'bounds':q.getbbox(),'paletteCount':len({p for p in q.getdata() if p[3]}),'pngSHA256':sha(O/f'{dr}-idle.png'),'layers':list(layers)}
 images={dr:composite(layers) for dr,layers in ls.items()}
 for dr in ['south','north']:
  a=images[dr].getchannel('A');assert a.tobytes()==a.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes();checks.append(dr+' bilateral alpha')
 assert images['east'].tobytes()==images['west'].transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes();checks.append('explicit east editable mirrored symmetric costume')
 front=images['south'];ref=Image.open(R/'docs/reviews/M1-RD1/reference-derived-dummy.png').convert('RGBA')
 assert front.getchannel('A').crop((0,46,32,64)).tobytes()==ref.getchannel('A').crop((0,46,32,64)).tobytes();checks.append('front RD1 complete body alpha46+ exact')
 F=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
 board=Image.new('RGB',(780,430),'#eee8d1');d=ImageDraw.Draw(board)
 d.text((12,10),'NUGGET / M1.ON1 / FOUR IDLE CANDIDATES / NOT ACCEPTED',font=F,fill=P['ink'])
 for i,(dr,q) in enumerate(images.items()):
  x=14+i*192;d.text((x,34),dr.upper()+' 32x64 / 4x',font=F,fill=P['ink'])
  board.paste(q.resize((128,256),Image.Resampling.NEAREST),(x,55),q.resize((128,256),Image.Resampling.NEAREST))
  board.paste(q,(x+144,185),q)
  d.text((x+132,259),'1x',font=F,fill=P['ink'])
 d.text((12,329),'Field hat / silver hair / glasses / cream coat / sage shirt',font=F,fill=P['ink'])
 d.text((12,352),'RD1 front body envelope; original side/back construction; no walk/runtime.',font=F,fill=P['ink'])
 d.text((12,375),'Adult cues from costume, silver hair and posture, not elongated limbs.',font=F,fill=P['ink'])
 board.save(O/'four-idle-board.png')
 # Full native sheet, contrasting dark board, and countable guide board.
 atlas=Image.new('RGBA',(128,64))
 for i,q in enumerate(images.values()):atlas.alpha_composite(q,(i*32,0))
 atlas.save(O/'four-idle-native.png')
 dark=Image.new('RGB',(512,256),'#24313b')
 for i,q in enumerate(images.values()):dark.paste(q.resize((128,256),Image.Resampling.NEAREST),(i*128,0),q.resize((128,256),Image.Resampling.NEAREST))
 dark.save(O/'four-idle-dark-4x.png')
 grid=Image.new('RGB',(800,430),'#eee8d1');g=ImageDraw.Draw(grid)
 for i,(dr,q) in enumerate(images.items()):
  x=i*200+22;y=35;g.text((x,8),dr,font=F,fill=P['ink']);big=q.resize((160,320),Image.Resampling.NEAREST);grid.paste(big,(x,y),big)
  for n in range(33):g.line((x+n*5,y,x+n*5,y+320),fill='#a7aa9d' if n%16 else '#ab5c67')
  for n in range(65):
   g.line((x,y+n*5,x+160,y+n*5),fill='#b6b8a9' if (64-n)%10 else '#6d8b9d')
   if (64-n)%10==0:g.text((x-20,y+n*5-5),str(64-n),font=F,fill=P['ink'])
 g.text((12,382),'Native cell grid / x16 centre / Y0 bottom / 5x nearest',font=F,fill=P['ink']);grid.save(O/'four-idle-grid.png')
 (S/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
 (S/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False},indent=2)+'\n')
 print(json.dumps({'checks':len(checks),'board':str(O/'four-idle-board.png')}))
if __name__=='__main__':main()
