"""PM1 one focused West A/P/C internal material comparison, fixed geometry."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-PM1';src=Path(__file__).parent;fm=root/'docs/reviews/M1-FM2';navy=(42,52,74,255);slate=(70,86,113,255);records={};ims={};checks=[]
def ck(n,v):assert v,n;checks.append(n)
edits={'A':[(x,54) for x in range(8,11)]+[(x,55) for x in range(8,12)]+[(x,56) for x in range(10,13)],'P':[],'C':[(x,54) for x in range(10,13)]+[(x,55) for x in range(10,14)]+[(x,56) for x in range(9,15)]}
for p in ['A','P','C']:
 old=Image.open(fm/f'hero-west-{p}.png').convert('RGBA');new=old.copy();changed=[]
 for pt in edits[p]:
  ck(p+' original navy '+str(pt),old.getpixel(pt)==navy);new.putpixel(pt,slate);changed.append({'xy':list(pt),'before':'#2a344a','after':'#465671'})
 ck(p+' alpha exact',old.getchannel('A').tobytes()==new.getchannel('A').tobytes());ck(p+' everything through53 exact',old.crop((0,0,32,54)).tobytes()==new.crop((0,0,32,54)).tobytes());ck(p+' all footwear57plus exact',old.crop((0,57,32,64)).tobytes()==new.crop((0,57,32,64)).tobytes());ck(p+' no extra colors',set(new.get_flattened_data())<=set(old.get_flattened_data()));ck(p+' no other cells changed',all(a==b for i,(a,b) in enumerate(zip(old.get_flattened_data(),new.get_flattened_data())) if (i%32,i//32) not in edits[p]));records[p]=changed;ims[p]=(old,new)
 new.save(out/f'west-{p}-pants-material-trial.png')
plate=Image.new('RGB',(1000,720),'#efe9d6');d=ImageDraw.Draw(plate);d.fontmode='1'
for row,p in enumerate(['A','P','C']):
 y=row*235;d.text((8,y+5),'WEST '+p+' / CURRENT | CONNECTED SLATE PLANE TRIAL | LOWER GRID CURRENT / TRIAL',fill='#253340')
 for col,im in enumerate(ims[p]):
  x=20+col*200;q=im.resize((96,192),Image.Resampling.NEAREST);plate.paste(q,(x,y+25),q);plate.paste(im,(x+130,y+130),im)
  xx=440+col*275;q=im.crop((0,52,32,64)).resize((224,84),Image.Resampling.NEAREST);plate.paste(q,(xx,y+100),q)
  for gx in range(33):d.line((xx+gx*7,y+100,xx+gx*7,y+184),fill='#a5aa92')
  for gy in range(13):d.line((xx,y+100+gy*7,xx+224,y+100+gy*7),fill='#a5aa92')
plate.save(out/'west-stride-plane-current-trial.png');(src/'edits.json').write_text(json.dumps({'task':'M1.PM1','state':'ONE WEST STATIC MATERIAL STUDY; NOT APPLIED ELSEWHERE','changes':records,'proposal':'Connected existing slate upper-pants surface, retaining dark projected overlap; not reference-recovered anatomy/seam','north':'No change: pinned05/01/06 already supports broad costume bands; extra divisions not justified'},indent=2)+'\n');(out/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'approval':False},indent=2)+'\n');print('PASS',len(checks),'color/footwear/shape invariants; A',len(edits['A']),'C',len(edits['C']))
