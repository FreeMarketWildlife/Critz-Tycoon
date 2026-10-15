from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
r=Path(__file__).resolve().parents[4];b=r/'docs/reviews/M1-BS2';fm=r/'docs/reviews/M1-FM2';rec=json.loads((r/'art/source/hero-bald-shading-r2/changes.json').read_text());checks=[]
def ck(s,v):
 assert v,s
 checks.append(s)
def im(p):return Image.open(p).convert('RGBA')
for dr,poses in rec['poses'].items():
 for po,v in poses.items():
  tag=f'{dr}-{po}';p=b/tag;n=im(p/'bald-template.png');old=im(fm/f'template-{tag}.png');hero=im(fm/f'hero-{tag}.png');hair=im(p/'hair-art.png');shade=im(p/'hair-dependent-shading.png');attach=im(p/'optional-hair-attachment.png')
  ck(tag+' alpha',n.getchannel('A').tobytes()==old.getchannel('A').tobytes())
  ck(tag+' actual changed coordinates', {(x,y) for y in range(64) for x in range(32) if n.getpixel((x,y))!=old.getpixel((x,y))}=={tuple(z['xy']) for z in v['changedSkinCells']})
  ck(tag+' features',all(n.getpixel(tuple(x))==old.getpixel(tuple(x)) for x in v['eyesEarsImmutable']))
  ck(tag+' body', n.crop((0,v['skinShadingEndRowExclusive'],32,64)).tobytes()==old.crop((0,v['skinShadingEndRowExclusive'],32,64)).tobytes())
  ck(tag+' independent attachment',Image.alpha_composite(shade,hair).tobytes()==attach.tobytes())
  dressed=n.copy()
  for q in v['selectedHairHiddenScalpCells']:dressed.putpixel(tuple(q),(0,0,0,0))
  dressed.alpha_composite(attach)
  ck(tag+' independent dressed',dressed.tobytes()==hero.tobytes()==im(p/'dressed-exact.png').tobytes())
  if dr in ['south','west']:ck(tag+' BS1 retained',n.tobytes()==im(r/f'docs/reviews/M1-BS1/{tag}/bald-template.png').tobytes())
order=['A','A','P','P','C','C','P','P']
for dr in rec['poses']:
 for speed in ['normal','slow']:
  holds=([100]*8 if dr=='south' else [70,60,70,70,70,60,70,70]);holds=[x*(4 if speed=='slow' else 1) for x in holds]
  for scale in [1,4]:
   name=f'{dr}-existing-walk-{speed}-{scale}x.gif';g=Image.open(b/name)
   ck(name+' slots/loop',g.n_frames==8 and g.info['loop']==0)
   for i,po in enumerate(order):
    g.seek(i);f=g.convert('RGB');ck(name+f' hold{i}',g.info['duration']==holds[i])
    for j,typ in enumerate(['before-template','bald-template','dressed-exact']):
     expected=Image.new('RGB',(32,64),'#bed4d5');a=im(b/f'{dr}-{po}/{typ}.png');expected.paste(a,(0,0),a);expected=expected.resize((32*scale,64*scale),Image.Resampling.NEAREST)
     ck(name+f' saved pose{i}/{typ}',f.crop(((8+j*48)*scale,23*scale,(40+j*48)*scale,87*scale)).tobytes()==expected.tobytes())
out=b/'independent-review';out.mkdir(exist_ok=True);(out/'saved-pixel-audit.json').write_text(json.dumps({'passed':True,'count':len(checks),'checks':checks,'scope':'saved layers and all 128 GIF frames; not user art approval or continuous playback observation'},indent=2)+'\n')
files=[b/'four-direction-current-template.png',b/'four-direction-existing-walk-contact.png',*sorted(b.glob('*.gif'))]
manifest=[]
for f in files:
 prev=r/'docs/reviews/M1-BS1'/f.name
 manifest.append({'path':str(f),'name':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size,'identicalBS1':prev.exists() and prev.read_bytes()==f.read_bytes()})
Path('/tmp/bs2-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'pass':True,'checks':len(checks),'files':manifest}))
