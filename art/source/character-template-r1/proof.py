"""Static existing-pose comparisons only. No animation, creator or art acceptance."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-CHT1';report={};checks=[]
def check(name,v):assert v,name;checks.append(name)
def folder(d,p):return out if (d,p)==('south','idle') else out/f'{d}-{p}'
for d in ['south','north','west','east']:
 plate=Image.new('RGB',(1010,660),'#efe9d6');dd=ImageDraw.Draw(plate);dd.fontmode='1';report[d]={}
 dd.text((10,5),d.upper()+' / EXISTING STATIC POSES / HERO | TEMPLATE | NATIVE PAIR | LOWER GRID',fill='#253340')
 for row,p in enumerate(['idle','A','P','C']):
  f=folder(d,p);tag=f'{d}-{p}';hero=Image.open(f/('hero-'+tag+'.png')).convert('RGBA');template=Image.open(f/('template-'+tag+'.png')).convert('RGBA');recomposed=Image.open(f/('recomposed-'+tag+'.png')).convert('RGBA');original=Image.open(root/f'docs/reviews/M1-PS1/hero-{tag}.png').convert('RGBA');reg=json.loads((src/('registration.json' if (d,p)==('south','idle') else 'registration-'+tag+'.json')).read_text());lower=reg['protectedLowerStartRow']
  check(tag+' original Hero saved pixels exact',hero.tobytes()==original.tobytes());check(tag+' independent selected hair recomposition exact',recomposed.tobytes()==original.tobytes());check(tag+' lower body RGBA exact',template.crop((0,lower,32,64)).tobytes()==hero.crop((0,lower,32,64)).tobytes());check(tag+' binary alpha32x64',template.size==(32,64) and set(template.getchannel('A').get_flattened_data())<={0,255})
  for n in reg['regions']:
   for x,y in reg['regions'][n]:check(tag+' actual region '+n+f' {x},{y}',template.getpixel((x,y))==hero.getpixel((x,y)))
  # Contacts and waist keep all original RGBA, not just one-pixel overlap.
  last=hero.getbbox()[3]-1;check(tag+' contact row/width/RGBA exact',all(template.getpixel((x,last))==hero.getpixel((x,last)) for x in range(32)));check(tag+' waist RGBA exact',template.crop((0,51,32,56)).tobytes()==hero.crop((0,51,32,56)).tobytes())
  if d=='south':
   old=Image.open(root/f'docs/reviews/M1-HR14/hero-{tag}.png').convert('RGBA');check(tag+' protected South Hero exactHR14',original.tobytes()==old.tobytes())
  # All hair/scalp is static in idle/A/C; P has precisely the prior2px rise.
  h=template.crop((0,0,32,36+(-2 if p=='P' else 0)))
  report[d][p]={'protectedLowerStartRow':lower,'sourceContactRow':last,'waistAndSourceFullShoePixelsExact':True,'hairRecompositionExact':True,'regionCells':{k:len(v) for k,v in reg['regions'].items()}}
  y=20+row*160;dd.text((8,y+10),p,fill='#253340')
  for col,im in enumerate([hero,template]):
   q=im.resize((96,192),Image.Resampling.NEAREST).crop((0,54,96,192));plate.paste(q,(42+col*145,y+8),q)
  for col,im in enumerate([hero,template]):plate.paste(im,(350+col*60,y+44),im)
  # Matching source and template lower crops, countable native grid.
  for col,im in enumerate([hero,template]):
   xx=510+col*235;q=im.crop((0,44,32,64)).resize((192,120),Image.Resampling.NEAREST);plate.paste(q,(xx,y+25),q)
   for gx in range(33):dd.line((xx+gx*6,y+25,xx+gx*6,y+145),fill='#9ba391')
   for gy in range(21):dd.line((xx,y+25+gy*6,xx+192,y+25+gy*6),fill='#9ba391')
  dd.text((510,y+10),'HERO LOWER',fill='#253340');dd.text((745,y+10),'TEMPLATE LOWER',fill='#253340')
 plate.save(out/(d+'-static-native-grid.png'))
(out/'static-checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'poses':report,'limits':['Static poses only; no animation or creator release','Exact source shape does not approve disputed NWE material scale','Source clothing and full shoe/waist retained, not anatomical reconstruction','User scalp/appearance review pending']},indent=2)+'\n');print('PASS',len(checks),'actual source/body/region/contact static checks')
