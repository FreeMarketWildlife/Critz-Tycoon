"""Bounded native-grid side/back body refinement; front exact. Review only."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-PS1';base=root/'docs/reviews/M1-HR14';meta=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());P={'ink':(36,35,48,255),'navy':(42,52,74,255),'slate':(70,86,113,255),'light':(116,136,148,255)};records={};frames={};bodies={}
# Deliberate native silhouette steps; no frame fitting or image resampling.
spans={
'north':{'P':[[(6,26)],[(6,26)],[(6,26)],[(6,26)],[(7,25)],[(7,25)],[(8,14),(18,24)],[(8,14),(18,24)],[],[]],
'A':[[(6,25)],[(7,25)],[(8,24)],[(8,23)],[(8,22)],[(8,21)],[(9,18)],[(9,17)],[(10,16)],[(10,16)]],
'C':[[(5,24)],[(5,24)],[(6,24)],[(8,24)],[(10,24)],[(12,24)],[(14,23)],[(15,23)],[(16,22)],[(16,22)]]},
'west':{'P':[[(10,24)],[(10,23)],[(10,22)],[(9,22)],[(8,22)],[(9,21)],[(10,20)],[(10,20)],[],[]],
'A':[[(5,24)],[(4,24)],[(4,25)],[(5,26)],[(6,26)],[(7,25)],[(8,12),(18,24)],[(9,12),(19,24)],[(20,24)],[(20,24)]],
'C':[[(6,25)],[(5,26)],[(4,27)],[(4,28)],[(4,28)],[(5,27)],[(6,14),(22,26)],[(7,13),(23,25)],[(8,12)],[(8,12)]]}}
def export(name,ims,ticks):
 pal=[None];lookup={}
 for im in ims:
  for p in im.get_flattened_data():
   if p[3]:
    c='#%02x%02x%02x'%p[:3]
    if c not in lookup:lookup[c]=len(pal);pal.append(c)
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'character','width':32,'height':64,'palette':pal,'bank':'custom','notes':'PS1 native-grid side/back body trial UNAPPROVED. Front/head/pack exact; no runtime change.','frames':[{'name':str(n),'ticks':ticks,'pixels':[lookup['#%02x%02x%02x'%p[:3]] if p[3] else 0 for p in im.get_flattened_data()]} for n,im in enumerate(ims)]}
for dr in ('south','north','west','east'):
 records[dr]={};frames[dr]={};bodies[dr]={}
 for po in ('A','P','C','idle'):
  original=Image.open(base/f'hero-{dr}-{po}.png').convert('RGBA');im=original.copy();body=Image.open(base/f'body-layer-{dr}-{po}.png').convert('RGBA');e=meta['directions'][dr][po]
  if dr!='south':
   canonical='west' if dr=='east' else dr;rows=spans[canonical]['P' if po=='idle' else po]
   for iy,runs in enumerate(rows):
    y=54+iy;allowed={31-x if dr=='east' else x for a,b in runs for x in range(a,b)}
    for x in range(32):
     if x not in allowed:body.putpixel((x,y),(0,0,0,0))
     elif not body.getpixel((x,y))[3]:
      # One new native edge site follows neighboring costume material.
      candidates=[body.getpixel((xx,y)) for xx in (x-1,x+1) if 0<=xx<32 and body.getpixel((xx,y))[3]];body.putpixel((x,y),candidates[0] if candidates else P['navy'])
   interfaceY=50 if po=='idle' else 48
   # Retain one native highlight row instead of doubled white sleeve slabs.
   # Original hand RGB remains protected; only original fabric whites change.
   beforeTrim=body.copy()
   for y in range(interfaceY,interfaceY+6):
    for x in range(32):
     px=beforeTrim.getpixel((x,y))
     if (y-interfaceY)%2==1 and px[:3] in ((249,237,200),(191,192,170)) and beforeTrim.getpixel((x,y-1))==px:body.putpixel((x,y),(237,116,92,255))
   # Original starter-shirt material ownership: coarse imported navy/cream
   # patches inside the upper torso are cloth, not extra hands or anatomy.
   # Keep native sleeve highlights, one-row hem shadow, and rigid straps later.
   for yy in range(4):
    y=interfaceY+yy
    for x in range(32):
     px=body.getpixel((x,y));canonicalX=31-x if dr=='east' else x
     if not px[3] or px[:3] in ((166,104,69),(195,138,88),(116,69,57)):continue
     if (10<=x<=21 if dr=='north' else 12<=canonicalX<=21):
      if px[:3] in ((42,52,74),(191,192,170)):body.putpixel((x,y),(237,116,92,255))
      if px[:3]==(249,237,200) and yy>0:body.putpixel((x,y),(237,116,92,255))
   # Deliberate one-native-pixel near-tip material cues, not doubled2x2 slots.
   if canonical=='west':
    nativeCues={'P':{(10,58):'accent',(17,58):'light',(18,59):'slate'},'A':{(22,60):'accent',(22,59):'light',(10,60):'slate'},'C':{(9,60):'accent',(10,61):'light',(24,60):'slate'}}['P' if po=='idle' else po]
    for y in range(56,64):
     for x in range(32):
      px=body.getpixel((x,y));cx=31-x if dr=='east' else x
      if px[3] and px[:3] in ((174,69,74),(116,136,148)):body.putpixel((x,y),P['slate'] if px[:3]==(116,136,148) else P['navy'])
    for (cx,y),material in nativeCues.items():
     x=31-cx if dr=='east' else cx
     if body.getpixel((x,y))[3]:body.putpixel((x,y),(174,69,74,255) if material=='accent' else P[material])
   # Literal single-native-pixel exterior: an internal dark costume plane is
   # navy material, not a second black boundary. Hair and pack are excluded.
   frozen=body.copy()
   for y in range(46 if po!='P' else 44,64):
    for x in range(32):
     px=frozen.getpixel((x,y))
     if not px[3]:continue
     neighbors=[frozen.getpixel((xx,yy))[3] if 0<=xx<32 and 0<=yy<64 else 0 for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))]
     if px==P['ink'] and all(neighbors):body.putpixel((x,y),P['navy'])
     if y>=interfaceY and not all(neighbors) and px[:3] not in ((166,104,69),(195,138,88),(116,69,57)):body.putpixel((x,y),P['ink'])
   if po=='idle':
    for yy in range(6):
     for x in range(32):body.putpixel((x,50+yy),bodies[dr]['P'].getpixel((x,48+yy)))
   # Recompose exact original head, canonical bag/straps and visibility order.
   bag=Image.open(base/f'pack-layer-{dr}-{po}.png').convert('RGBA');straps=Image.open(base/f'strap-layer-{dr}-{po}.png').convert('RGBA');im=bag.copy() if dr=='south' else body.copy()
   if dr in ('north','west','east'):im.alpha_composite(bag)
   else:im.alpha_composite(body)
   skin={(166,104,69),(195,138,88),(116,69,57)}
   for y in range(42+e['torsoTransform'][1],54):
    for x in range(32):
     p=straps.getpixel((x,y));bp=body.getpixel((x,y))
     if p[3] and bp[3] and bp[:3] not in skin:im.putpixel((x,y),p)
   for i,on in enumerate(e['headMaskHero']):
    if on:im.putpixel((i%32,i//32),original.getpixel((i%32,i//32)))
  im.save(out/f'hero-{dr}-{po}.png');frames[dr][po]=im;bodies[dr][po]=body;body.save(out/f'body-{dr}-{po}.png')
  changed=[{'xy':[x,y],'old':list(original.getpixel((x,y))),'new':list(im.getpixel((x,y)))} for y in range(64) for x in range(32) if original.getpixel((x,y))!=im.getpixel((x,y))]
  last=original.getbbox()[3]-1;assert im.getbbox()[3]-1==last
  assert [x for x in range(32) if im.getpixel((x,last))[3]]==[x for x in range(32) if original.getpixel((x,last))[3]],(dr,po,'contact')
  if dr=='south':assert im.tobytes()==original.tobytes()
  for i,on in enumerate(e['headMaskHero']):
   if on:assert im.getpixel((i%32,i//32))==original.getpixel((i%32,i//32))
  records[dr][po]={'changedCells':changed,'contactRow':last,'contactExact':True,'headExact':True,'frontExact':dr=='south','canvas':[32,64],'anchor':[16,64]}
order=meta['order']
for dr in frames:(src/f'hero-{dr}-walk.sprite.json').write_text(json.dumps(export('PS1 '+dr,[frames[dr][p] for p in order],6 if dr=='south' else 4),separators=(',',':'))+'\n')
(src/'hero-idles.sprite.json').write_text(json.dumps(export('PS1 idles',[frames[dr]['idle'] for dr in frames],6),separators=(',',':'))+'\n')
(src/'changes.json').write_text(json.dumps(records,separators=(',',':'))+'\n');print('PS1 side/back native-grid trial; front/head/contact exact. Changes:',{d:{p:len(v['changedCells']) for p,v in ps.items()} for d,ps in records.items()})
# Focused before/after native +4x, including actual front as fixed style target.
plate=Image.new('RGB',(1280,690),'#bed4d5');d=ImageDraw.Draw(plate)
for row,dr in enumerate(('north','west')):
 for col,(name,im) in enumerate([('FIXED FRONT',frames['south']['idle']),('BEFORE '+dr,Image.open(base/f'hero-{dr}-idle.png').convert('RGBA')),('AFTER '+dr,frames[dr]['idle']),('AFTER '+dr+' P',frames[dr]['P'])]):
  x=col*320;y=row*340;d.text((x+5,y+5),name,fill='#253340');big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+20,y+30),big);plate.paste(im,(x+210,y+150),im);d.line((x+20,y+286,x+148,y+286),fill='#748894')
plate.save(out/'native-scale-before-after.png')
