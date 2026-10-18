"""SV1 original native West body-overlap trial. Existing South/creator untouched."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-SV1';src=Path(__file__).parent
P={'.':'#242330','n':'#2a344a','b':'#465671','h':'#748894','w':'#f9edc8','s':'#bfc0aa','r':'#ed745c','d':'#ae454a','k':'#a66845','l':'#c38a58','v':'#744539'}
C={k:tuple(bytes.fromhex(v[1:]))+(255,) for k,v in P.items()}
# Each row is authored native pixels, no whole-sprite scaling or fitting.
# Full cloth masses overlap. Only their visible contours/planes are proposed.
rows={
'idle':[(11,'.wwwrrnnnnnn..'),(10,'.wwrrrrrnnbbb..'),(10,'.wrrrrrrnnbhb.'),(10,'.wrrrwwrnnbhb.'),(10,'.drrrwwrnnbhb.'),(10,'.drrrkkrrnbbb.'),(10,'.drrrlkrrrnn..'),(11,'.rrrkkrrrnn.'),(11,'.ddrdddddnn.'),(11,'.bbbbbbbbn.'),(11,'.bbbhbbbn.'),(11,'.nbbbbbn.'),(10,'.nnbbbbn.'),(10,'.dddddnn.'),(11,'.dddrdn.'),(11,'.wsssss.'),(12,'.......')],
'A':[(11,'.wwwrrnnnnnn..'),(10,'.wwrrrrrnnbbb..'),(10,'.wrrrrrrnnbhb.'),(9,'.wwrrrrrnnbhb.'),(9,'.dkrrrrrrnbhb.'),(9,'.klrrrrrrnbbb.'),(9,'.kkrrrrrrrnn..'),(10,'.drrrrrrrnn.'),(9,'.bdddddddnn.'),(8,'.bbbbbbnnnn.'),(7,'.bbbhbbnnnnn.'),(7,'.nbbbbnnnbbn.'),(7,'.ddddnnnbbbn.'),(8,'.dddn..nbbn.'),(8,'.wss.  .dddn.'),(9,'...    .dddn.'),(17,'.ss.'),(17,'....')],
'C':[(11,'.wwwrrnnnnnn..'),(10,'.wwrrrrrnnbbb..'),(10,'.wrrrrrrnnbhb.'),(10,'.wrrrrrrnnbhb.'),(10,'.drrrwwrnnbhb.'),(10,'.drrrrwkk nbb.'),(10,'.drrrrrlk nn..'),(10,'.drrrrrkk nn.'),(10,'.bdddddddnn.'),(9,'.nbbbbbbbnn.'),(8,'.nnbbbhbbnnn.'),(7,'.nnbbbbbnnnbbn.'),(7,'.nnbbbnnnndddn.'),(7,'.ddddn...nddd.'),(8,'.dddn.   .ss.'),(8,'.dddn.    ..'),(9,'.ss.'),(9,'....')]}
# Idle is17rows starting45; stride18rows starting46? all must end63.
# A/C starts46 and has18rows; shoulder row45 added separately.
records={};made={}
for po in ['idle','A','P','C']:
 folder=root/f'docs/reviews/M1-BS2/west-{po}';base=Image.open(folder/'bald-template.png').convert('RGBA');dressed=Image.open(folder/'dressed-exact.png').convert('RGBA');hair=Image.open(folder/'optional-hair-attachment.png').convert('RGBA')
 trial=base.copy()
 for y in range(45,64):
  for x in range(32):trial.putpixel((x,y),(0,0,0,0))
 rr=rows['idle' if po=='P' else po];start=45 if po in ['idle','P'] else 46
 for j,(x0,s) in enumerate(rr):
  for k,ch in enumerate(s):
   if ch!=' ':trial.putpixel((x0+k,start+j),C[ch])
 if po in ['A','C']:
  for x,ch in enumerate('.wwwrrnnnnnn..',11):trial.putpixel((x,45),C[ch])
 # Passing pose keeps original head raised2px, shoulder and shirt raised2px;
 # shoe contact remains fixed as in actual current P/idle.
 if po=='P':
  frozen=trial.copy()
  for y in range(43,54):
   for x in range(32):
    # Raised shirt inside the existing neck region, no face/nose alteration.
    if y>=45 or x>=11:trial.putpixel((x,y),frozen.getpixel((x,y+2)))
  for y in (54,55):
   for x in range(11,22):trial.putpixel((x,y),C['b'] if x not in (11,21) else C['.'])
 # Head/scalp remains exact through42; normal head retained through44.
 protected=43 if po=='P' else 45
 assert trial.crop((0,0,32,protected)).tobytes()==base.crop((0,0,32,protected)).tobytes()
 dressedTrial=trial.copy();dressedTrial.alpha_composite(hair)
 made[po]=(trial,dressedTrial)
 for name,im in [('bald',trial),('hero',dressedTrial)]:im.save(out/f'west-{po}-{name}.png')
 records[po]={'changedCells':sum(a!=b for a,b in zip(base.get_flattened_data(),trial.get_flattened_data())),'canvas':[32,64],'headExactAbove':protected,'baseSHA256':hashlib.sha256((folder/'bald-template.png').read_bytes()).hexdigest()}
# Display native +4x together, transparent sprites on a single matte.
fnt=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',13)
def board(withref=False):
 cols=['OLD HR14','CURRENT FM2/BS2']+(['PINNED ROM 2x'] if withref else [])+['PROPOSED SV1'];w=250*len(cols);im=Image.new('RGB',(w,1160),'#eee8d1');d=ImageDraw.Draw(im)
 ref=Image.open('/Users/tanoshi/.codex/visualizations/2026/10/14/hero-hr5-reference/walking.png') if withref else None
 for j,po in enumerate(['idle','A','P','C']):
  for i,label in enumerate(cols):
   x=i*250;y=j*290;d.text((x+8,y+8),label+' / '+po,font=fnt,fill='#242330')
   if label=='OLD HR14':hero=Image.open(root/f'docs/reviews/M1-HR14/hero-west-{po}.png').convert('RGBA');bald=None
   elif label=='CURRENT FM2/BS2':hero=Image.open(root/f'docs/reviews/M1-BS2/west-{po}/dressed-exact.png').convert('RGBA');bald=Image.open(root/f'docs/reviews/M1-BS2/west-{po}/bald-template.png').convert('RGBA')
   elif label=='PROPOSED SV1':bald,hero=made[po]
   else:
    n={'idle':2,'P':2,'A':7,'C':8}[po];q=ref.crop((n*16,0,(n+1)*16,32));hero=q.convert('RGBA');hero.putalpha(q.point(lambda n:255 if n else 0).convert('L'));hero=hero.resize((32,64),Image.Resampling.NEAREST);bald=None
   # Two3x comparisons for bald + clothed, native under each.
   for offset,q in [(8,hero),(126,bald)]:
    if q is None:
     d.text((x+offset,y+90),'No bald\nreference' if label.startswith('PINNED') else 'No bald\nsource',font=fnt,fill='#465671');continue
    big=q.resize((96,192),Image.Resampling.NEAREST);im.paste(big,(x+offset,y+32),big);im.paste(q,(x+offset+32,y+225),q)
  d.line((0,j*290+289,w,j*290+289),fill='#bfc0aa')
 return im
board().save(out/'west-old-current-proposed.png')
external=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/side-sv1');external.mkdir(exist_ok=True)
board(True).save(external/'west-old-current-reference-proposed.png')
(src/'changes.json').write_text(json.dumps(records,indent=2)+'\n')
print(records)
