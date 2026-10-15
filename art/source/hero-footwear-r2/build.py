"""FM2 existing STATIC NWE shoe material study. Source shapes never change."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-FM2';old=root/'docs/reviews/M1-PS1';templates=root/'docs/reviews/M1-CHT1';ink=(36,35,48,255);records={};checks=[];images={}
def rgba(c):return tuple(bytes.fromhex(c[1:]))+(255,)
def check(n,v):assert v,n;checks.append(n)
def row(e,y,xs,c):
 for x in xs:e[x,y]=c
base=json.loads((root/'art/source/hero-footwear-r1/edits.json').read_text());edits={('west',p):{tuple(e['xy']):e['after'] for e in base['poses'][p]['changedCells']} for p in ['idle','P']}
# Each visible surface has a connected upper and sole; no far leg is invented.
e={};row(e,57,range(7,11),'#ae454a');row(e,58,range(7,12),'#ae454a');e[7,57]='#ed745c';row(e,59,range(8,12),'#bfc0aa');e[8,59]='#f9edc8';row(e,60,range(9,11),'#bfc0aa');row(e,59,range(20,24),'#ae454a');row(e,60,range(19,23),'#ae454a');e[19,60]='#ed745c';row(e,61,range(20,23),'#ae454a');row(e,62,range(21,23),'#bfc0aa');edits['west','A']=e
e={};row(e,59,range(6,14),'#ae454a');row(e,60,range(7,13),'#ae454a');e[7,60]='#ed745c';row(e,61,range(8,12),'#ae454a');row(e,62,range(9,11),'#bfc0aa');row(e,58,range(23,27),'#ae454a');row(e,59,range(22,26),'#ae454a');e[22,59]='#ed745c';row(e,60,range(23,25),'#bfc0aa');edits['west','C']=e
for p in ['idle','A','P','C']:edits['east',p]={(31-x,y):c for (x,y),c in edits['west',p].items()}
for p in ['idle','P']:
 e={}
 for start in [8,18]:
  row(e,58,range(start+1,start+5),'#ae454a');row(e,59,range(start,start+6),'#ae454a');e[start+2,59]='#ed745c';row(e,60,range(start+1,start+5),'#bfc0aa')
 edits['north',p]=e
e={};row(e,60,range(10,17),'#ae454a');row(e,61,range(10,16),'#ae454a');e[12,61]='#ed745c';row(e,62,range(11,15),'#bfc0aa');edits['north','A']=e;edits['north','C']={(31-x,y):c for (x,y),c in e.items()}
south=Image.open(old/'hero-south-idle.png').convert('RGBA');palette={q for q in south.get_flattened_data() if q[3]}
for dr in ['south','north','west','east']:
 images[dr]={};records[dr]={}
 for po in ['idle','A','P','C']:
  tag=dr+'-'+po;hero=Image.open(old/('hero-'+tag+'.png')).convert('RGBA');tf=templates if tag=='south-idle' else templates/tag;body=Image.open(tf/('template-'+tag+'.png')).convert('RGBA');new=hero.copy();bt=body.copy();ee=edits.get((dr,po),{});changed=[]
  for pt,c in ee.items():
   check(tag+' existing non-ink surface '+str(pt),hero.getpixel(pt)[3] and hero.getpixel(pt)!=ink)
   if hero.getpixel(pt)!=rgba(c):changed.append({'xy':list(pt),'before':'#%02x%02x%02x'%hero.getpixel(pt)[:3],'after':c})
   new.putpixel(pt,rgba(c));bt.putpixel(pt,rgba(c))
  last=hero.getbbox()[3]-1
  check(tag+' alpha exact',new.getchannel('A').tobytes()==hero.getchannel('A').tobytes());check(tag+' template alpha exact',bt.getchannel('A').tobytes()==body.getchannel('A').tobytes());check(tag+' waist exact',new.crop((0,51,32,56)).tobytes()==hero.crop((0,51,32,56)).tobytes());check(tag+' all other pixels exact',all(a==b for i,(a,b) in enumerate(zip(hero.get_flattened_data(),new.get_flattened_data())) if (i%32,i//32) not in ee));check(tag+' exterior ink exact',all(a==b for a,b in zip(hero.get_flattened_data(),new.get_flattened_data()) if a==ink));check(tag+' contact RGBA exact',hero.crop((0,last,32,64)).tobytes()==new.crop((0,last,32,64)).tobytes());check(tag+' selected shared palette only',all(q in palette for q in new.get_flattened_data() if q[3]));check(tag+' template same source body region',new.crop((0,46,32,64)).tobytes()==bt.crop((0,46,32,64)).tobytes())
  if dr=='south':check(po+' South source all pixels exact',new.tobytes()==hero.tobytes())
  if dr=='west' and po in ['idle','P']:check(po+' focusedFM1 exact',new.tobytes()==Image.open(root/f'docs/reviews/M1-FM1/west-{po}-trial-hero.png').convert('RGBA').tobytes())
  new.save(out/('hero-'+tag+'.png'));bt.save(out/('template-'+tag+'.png'));images[dr][po]=(hero,new,body,bt)
  records[dr][po]={'changedCells':changed,'contactRow':last,'sourceHeroSHA256':hashlib.sha256((old/('hero-'+tag+'.png')).read_bytes()).hexdigest(),'projection':'heel only; no inferred far foot' if dr=='north' else 'visible side upper/sole; source overlap kept' if dr!='south' else 'protected original, unchanged'}
 for kind in ['full','grid']:
  plate=Image.new('RGB',(1120,710),'#efe9d6');d=ImageDraw.Draw(plate);d.fontmode='1';d.text((10,5),dr.upper()+' / EXISTING STATIC POSES / CURRENT HERO | TRIAL HERO | CURRENT TEMPLATE | TRIAL TEMPLATE',fill='#253340')
  for r,po in enumerate(['idle','A','P','C']):
   y=25+r*170;d.text((4,y+3),po,fill='#253340')
   for j,im in enumerate(images[dr][po]):
    x=25+j*275
    if kind=='full':
     q=im.resize((96,192),Image.Resampling.NEAREST).crop((0,48,96,192));plate.paste(q,(x,y+8),q);plate.paste(im,(x+160,y+65),im)
    else:
     q=im.crop((0,54,32,64)).resize((224,70),Image.Resampling.NEAREST);plate.paste(q,(x,y+35),q)
     for gx in range(33):d.line((x+gx*7,y+35,x+gx*7,y+105),fill='#9ba391')
     for gy in range(11):d.line((x,y+35+gy*7,x+224,y+35+gy*7),fill='#9ba391')
     # Native full silhouette remains adjacent to the crop.
     plate.paste(im,(x+80,y+108),im)
  plate.save(out/(dr+'-static-'+kind+'.png'))
(src/'edits.json').write_text(json.dumps({'task':'M1.FM2','scope':'EXISTING STATIC16 / NWE materials only / South unchanged','state':'REVIEW PENDING; NO ANIMATIONS OR CREATOR','poses':records},indent=2)+'\n');(out/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'approval':False},indent=2)+'\n');print('PASS',len(checks),'source/shape/material invariants; STATIC ONLY')
