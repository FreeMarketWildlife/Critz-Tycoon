"""Decode final saved walking layers, contacts and GIF holds independently."""
from pathlib import Path
from PIL import Image, ImageColor
import json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
checks=[];records=[];gifs=[]
def guard(n,v):checks.append({'name':n,'pass':bool(v)})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def shift(im):
 out=Image.new('RGBA',(32,64));out.paste(im,(0,2));return out
for ch,source,review,oldreview in [('girl','overnight-girl-walk-r1','M1-OGH3','M1-OGH2'),('nugget','overnight-nugget-walk-r1','M1-ON3','M1-ON2')]:
 s=ROOT/'art/source'/source;r=ROOT/'docs/reviews'/review
 for d in ['south','north','west','east']:
  layersByPhase={}
  for ph in ['idle','A','B']:
   p={'idle':'idle','A':'stride-a','B':'stride-b'}[ph] if ch=='girl' else ph
   jp=s/(d+'-'+p+'.layers.json') if ch=='girl' else s/d/(ph+'.layers.json')
   o=json.loads(jp.read_text()); comp=Image.new('RGBA',(32,64));layers={}
   order=o.get('order',o.get('renderOrder'))
   for n in order:
    im=Image.new('RGBA',(32,64))
    if ch=='girl':
     ent=next(x for x in o['layers'] if x['id']==n)
     for i,v in enumerate(ent['pixels']):
      if v:im.putpixel((i%32,i//32),ImageColor.getrgb(o['palette'][v])+(255,))
     lp=r/d/p/(n+'.png')
    else:
     for x,y,*rgba in o['layers'][n]['pixels']:im.putpixel((x,y),tuple(rgba))
     lp=s/d/ph/(n+'.png')
    guard(f'{ch}/{d}/{ph}/{n} cells equal actual PNG',im.tobytes()==Image.open(lp).convert('RGBA').tobytes())
    layers[n]=im;comp=Image.alpha_composite(comp,im)
   fp=r/d/p/'composite.png' if ch=='girl' else r/(d+'-'+ph+'.png')
   final=Image.open(fp).convert('RGBA')
   guard(f'{ch}/{d}/{ph} exact composition',comp.tobytes()==final.tobytes())
   guard(f'{ch}/{d}/{ph} native frame',final.size==(32,64))
   guard(f'{ch}/{d}/{ph} binary alpha',set(final.getchannel('A').getdata())<={0,255})
   mask={(x,y) for y in range(64) for x in range(32) if final.getpixel((x,y))[3]}
   row=max(y for x,y in mask);guard(f'{ch}/{d}/{ph} contact row',row==(61 if ph=='idle' else 63))
   if ph=='idle':
    old=ROOT/'docs/reviews'/oldreview/(d+'/idle.png' if ch=='girl' else d+'-idle.png')
    guard(f'{ch}/{d} frozen idle bytes',fp.read_bytes()==old.read_bytes())
   records.append({'character':ch,'direction':d,'phase':ph,'file':str(fp.relative_to(ROOT)),'sha256':sha(fp),'layersJsonSHA256':sha(jp),'contactRow':row,'contactXs':[x for x in range(32) if (x,row) in mask]})
   layersByPhase[ph]=layers
  protected=['face','ears','hair','ties','eyes'] if ch=='girl' else ['head','face-light','face-shadow','ears','ear','hair','hair-light','hair-shadow','hair-fringe','glasses','eyes','hat','hat-light','hat-band','hat-brim']
  for ph in ['A','B']:
   for n in protected:
    if n in layersByPhase['idle'] and n in layersByPhase[ph]:
     guard(f'{ch}/{d}/{ph}/{n} rigid +2Y unchanged shape/color',shift(layersByPhase['idle'][n]).tobytes()==layersByPhase[ph][n].tobytes())
 if ch=='girl':
  for d in ['south','north','west','east']:
   for ph in ['idle','stride-a','stride-b']:
    hp=r/'history-v0'/d/ph/'composite.png';cp=r/d/ph/'composite.png'
    old=Image.open(hp).convert('RGBA');new=Image.open(cp).convert('RGBA')
    changed=[(x,y) for y in range(64) for x in range(32) if old.getpixel((x,y))!=new.getpixel((x,y))]
    guard(f'girl/{d}/{ph} correction preserves whole alpha',old.getchannel('A').tobytes()==new.getchannel('A').tobytes())
    expectedCount=3 if d in ['west','east'] and ph=='stride-a' else 0
    guard(f'girl/{d}/{ph} correction exact visible cell count',len(changed)==expectedCount)
    if d in ['west','east'] and ph!='idle':
     guard(f'girl/{d}/{ph} full nearshoe RGBA preserved',Image.open(r/'history-v0'/d/ph/'near-shoe.png').convert('RGBA').tobytes()==Image.open(r/d/ph/'near-shoe.png').convert('RGBA').tobytes())
 if ch=='nugget':
  for d in ['south','north','west','east']:
   for ph in ['idle','A','B']:
    oldfp=r/'history-v0'/(d+'-'+ph+'.png');newfp=r/(d+'-'+ph+'.png')
    old=Image.open(oldfp).convert('RGBA');new=Image.open(newfp).convert('RGBA')
    if d in ['south','north'] or ph=='idle':guard(f'nugget/{d}/{ph} exact v0 preserved pose',oldfp.read_bytes()==newfp.read_bytes())
    else:
     o=json.loads((s/d/(ph+'.layers.json')).read_text())
     for n in o['renderOrder']:
      if n not in ['far-shoe','far-leg']:
       guard(f'nugget/{d}/{ph}/{n} exact v0 protected layer',(s/d/ph/(n+'.png')).read_bytes()==(s/'history-v0'/d/ph/(n+'.png')).read_bytes())
     oldfar=Image.open(s/'history-v0'/d/ph/'far-shoe.png').convert('RGBA');newfar=Image.open(s/d/ph/'far-shoe.png').convert('RGBA')
     guard(f'nugget/{d}/{ph} full farshoe45 cells unscaled',sum(a>0 for a in oldfar.getchannel('A').getdata())==sum(a>0 for a in newfar.getchannel('A').getdata())==45)
 for fp in sorted(r.glob('*.gif')):
  im=Image.open(fp);holds=[]
  for i in range(im.n_frames):im.seek(i);holds.append(im.info.get('duration'))
  slow='slow' in fp.name;expected=[540,530,540,530] if slow else [130,140,130,140]
  guard(f'{ch}/{fp.name} exact four declared GIF holds',holds==expected)
  for j,phase in enumerate(['A','idle','B','idle']):
   im.seek(j);decoded=im.convert('RGBA')
   for k,d in enumerate(['south','north','west','east']):
    p={'idle':'idle','A':'stride-a','B':'stride-b'}[phase]
    png=r/d/p/'composite.png' if ch=='girl' else r/(d+'-'+phase+'.png')
    expectedPNG=Image.open(png).convert('RGBA')
    if ch=='girl':
     regions=[(40*k,0,1)] if 'native' in fp.name else [(20+186*k,48,1),(58+186*k,110,4)]
    elif 'four-directions' in fp.name:regions=[(12+192*k,58,4),(155+192*k,200,1)]
    elif fp.name.startswith(d+'-'):regions=[(0,0,4 if '-4x.gif' in fp.name else 1)]
    else:continue
    for x,y,scale in regions:
     enlarged=expectedPNG.resize((32*scale,64*scale),Image.Resampling.NEAREST)
     crop=decoded.crop((x,y,x+32*scale,y+64*scale))
     if ch=='nugget' and 'four-directions' not in fp.name:
      # Transparent RGB values are undefined; compare visible RGBA and full alpha.
      ok=crop.getchannel('A').tobytes()==enlarged.getchannel('A').tobytes() and all(crop.getpixel((xx,yy))==enlarged.getpixel((xx,yy)) for yy in range(64*scale) for xx in range(32*scale) if enlarged.getpixel((xx,yy))[3])
     else:
      matte=Image.new('RGBA',enlarged.size,'#eee8d1');matte.alpha_composite(enlarged)
      ok=crop.convert('RGB').tobytes()==matte.convert('RGB').tobytes()
     guard(f'{ch}/{fp.name} slot{j}/{d}/{scale}x decoded PNG equality',ok)
  gifs.append({'file':str(fp.relative_to(ROOT)),'sha256':sha(fp),'holdsMs':holds,'size':im.size,'loop':im.info.get('loop')})
report={'task':'M1.OVQ3','passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'checks':checks,'poses':records,'gifs':gifs,'limitations':'Static/GIF file integrity, not acceptance of appearance or movement. Browser observation is separately reported.'}
(OUT/'walk-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'failures':[c for c in checks if not c['pass']],'gifCount':len(gifs)}))
assert not report['failed']
