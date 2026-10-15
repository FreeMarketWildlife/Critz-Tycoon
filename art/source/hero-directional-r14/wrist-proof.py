"""Scoped saved-pixel HR14 front material verification and bald-head audit."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR14';dest=out/'wrist-correction';ext=Path(sys.argv[1]).resolve();meta=json.loads((src/'construction.json').read_text());frozen=json.loads((dest/'before-hashes.json').read_text());beforemeta=json.loads((dest/'before-construction.json').read_text());skin={(166,104,69),(195,138,88),(116,69,57)};ink={(36,35,48),(42,52,74)};cream={(249,237,200),(191,192,170)};order=meta['order'];checks={};poses={}
def check(k,v):assert v,k;checks[k]=True
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def oldim(kind,pose):return Image.open(dest/f'before-{kind}-south-{pose}.png').convert('RGBA')
def actual(kind,d,pose):return Image.open(out/f'{kind}-{d}-{pose}.png').convert('RGBA')
def points(im,fn):return [(i%32,i//32) for i,p in enumerate(im.get_flattened_data()) if p[3] and fn(p)]
def cut(im,pts):
 q=Image.new('RGBA',(32,64))
 for p in pts:q.putpixel(p,im.getpixel(p))
 return q
def put(bg,im,x,y,s):
 im=im.resize((32*s,64*s),Image.Resampling.NEAREST);bg.paste(im,(x,y),im)
def anchor(d,x,y,s):d.line((x,y+64*s,x+32*s,y+64*s),fill='#748894');d.line((x+16*s-3,y+64*s,x+16*s+3,y+64*s),fill='#ed745c')
for name,h in frozen.items():
 p=Path(name)
 if 'hero-girl-r1/' in name or '/M1-GH1/' in name or any('-'+d+'-' in name for d in ('north','west','east')):check('unchanged '+name,sha(p)==h)
for po in ('idle','A','P','C'):
 old=oldim('hero',po);new=actual('hero','south',po);dm=actual('dummy','south',po);oldm=oldim('dummy',po);e=meta['directions']['south'][po];changes=[]
 for y in range(64):
  for x in range(32):
   p=(x,y);a=old.getpixel(p);b=new.getpixel(p)
   if a!=b:changes.append({'cell':[x,y],'before':'#%02x%02x%02x'%a[:3],'after':'#%02x%02x%02x'%b[:3]})
   if a[3] and a[:3] in ink:check(po+' protected ink/navy '+str(p),a==b)
   if e['headMaskHero'][y*32+x]:check(po+' protected dressed head '+str(p),a==b)
   if e['headMaskDummy'][y*32+x]:check(po+' bald dummy head unchanged '+str(p),oldm.getpixel(p)==dm.getpixel(p))
 check(po+' alpha exact',old.getchannel('A').tobytes()==new.getchannel('A').tobytes() and oldm.getchannel('A').tobytes()==dm.getchannel('A').tobytes())
 check(po+' rows54+ exact',old.crop((0,54,32,64)).tobytes()==new.crop((0,54,32,64)).tobytes() and oldm.crop((0,54,32,64)).tobytes()==dm.crop((0,54,32,64)).tobytes())
 check(po+' changes only arms',all((c['cell'][0]<10 or c['cell'][0]>21) and 45<=c['cell'][1]<=53 for c in changes))
 if po=='P':check('P exact seam53',old.crop((0,53,32,54)).tobytes()==new.crop((0,53,32,54)).tobytes())
 for kind in ('pack-layer','strap-layer','pack-visible'):check(po+' '+kind+' exact',sha(out/f'{kind}-south-{po}.png')==frozen[str((out/f'{kind}-south-{po}.png').relative_to(root))])
 # Actual visible skin excludes head; all costume highlights are explicitly cloth.
 skinpts=[p for p in points(new,lambda c:c[:3] in skin) if not e['headMaskHero'][p[1]*32+p[0]]];dskin=points(dm,lambda c:c[:3]==(255,212,161));check(po+' actual dummy/hero hands exact',set(skinpts)==set(dskin));check(po+' guide hand cells exact',set(skinpts)=={tuple(p) for p in e['commonFeatureRegistration']['hands']['cells']})
 cuff=[p for p in points(new,lambda c:c[:3] in cream) if not e['headMaskHero'][p[1]*32+p[0]] and (p[0]<10 or p[0]>21) and p[1]<=(48 if po=='idle' else 46 if po=='P' else 49)]
 cloth=[p for p in points(new,lambda c:c[:3] in cream) if not e['headMaskHero'][p[1]*32+p[0]] and p not in cuff and p[1]<54]
 edges=[p for p in points(new,lambda c:c[:3] in ink) if (p[0]<10 or p[0]>21) and 45<=p[1]<=53]
 oldskin=[p for p in points(old,lambda c:c[:3] in skin) if not e['headMaskHero'][p[1]*32+p[0]]]
 poses[po]={'changedCells':changes,'changedCount':len(changes),'skinBefore':len(oldskin),'skinAfter':len(skinpts),'skinCells':skinpts,'retainedUpperSleeveTrimCells':cuff,'otherClothingHighlightCells':cloth,'protectedShadowEdgeCells':edges,'edgeAnchor':[16,64]}
# Native static comparison; reference-bearing version stays external.
for withref in (False,True):
 plate=Image.new('RGB',(1600,1500),'#bed4d5');d=ImageDraw.Draw(plate)
 for row,po in enumerate(('idle','A','P','C')):
  columns=[('BEFORE Hero',oldim('hero',po)),('AFTER Hero',actual('hero','south',po)),('BEFORE dummy',oldim('dummy',po)),('AFTER dummy',actual('dummy','south',po))]
  if withref:
   ref=Image.open(ext/f'reference-south-{po if po!="idle" else "P"}.png').convert('RGBA');columns=[('SOURCE '+('P (idle UNOBSERVED)' if po=='idle' else po),ref)]+columns[:3]+[columns[-1]]
  for col,(label,im) in enumerate(columns):
   x=col*(320 if withref else 400);y=row*370;d.text((x+5,y+4),po+' '+label,fill='#253340');put(plate,im,x+30,y+22,4);anchor(d,x+30,y+22,4);put(plate,im,x+190,y+160,1);anchor(d,x+190,y+160,1)
 d.text((8,1480),'Fixed32x64 / anchor16,64; no pose fitting; native + nearest4x; static comparison, not visual approval.',fill='#253340');plate.save((ext if withref else dest)/('south-source-before-after-allunique.png' if withref else 'south-before-after-allunique.png'))
# Separate original-RGBA actual material ownership, four poses.
plate=Image.new('RGB',(1280,1190),'#bed4d5');d=ImageDraw.Draw(plate)
for row,po in enumerate(('idle','A','P','C')):
 im=actual('hero','south',po);q=poses[po]
 for col,(label,key) in enumerate([('ACTUAL EXPOSED SKIN','skinCells'),('RETAINED UPPER SLEEVE TRIM','retainedUpperSleeveTrimCells'),('OTHER CLOTHING HIGHLIGHTS','otherClothingHighlightCells'),('PROTECTED INK/NAVY EDGES','protectedShadowEdgeCells')]):
  x=col*320;y=row*290;d.text((x+4,y+4),po+' '+label,fill='#253340');put(plate,cut(im,q[key]),x+90,y+22,4);anchor(d,x+90,y+22,4)
d.text((7,1171),'Actual native material masks; skin ramp unchanged; sleeve/skin ownership authored, not measured hidden joints.',fill='#253340');plate.save(dest/'south-actual-skin-trim-highlight-edge-masks.png')
# All16 bald-head comparisons: original smooth contour, no hair/hat overlay.
plate=Image.new('RGB',(1600,1500),'#bed4d5');d=ImageDraw.Draw(plate);bald={}
for row,dr in enumerate(('south','north','west','east')):
 bald[dr]={}
 for col,po in enumerate(('idle','A','P','C')):
  hm=meta['directions'][dr][po]['headMaskDummy'];dm=actual('dummy',dr,po);h=actual('hero',dr,po);pts=[(i%32,i//32) for i,on in enumerate(hm) if on];colors={dm.getpixel(p)[:3] for p in pts if dm.getpixel(p)[3]};check(dr+po+' only bald head/ear/feature colors',colors<={(184,220,224),(37,51,64),(237,140,205)})
  baseline=Image.open(root/f'docs/reviews/M1-HR13/dummy-{dr}-{po}.png').convert('RGBA');# HR14 adds actual eyes, not hair.
  dy=-2 if po=='P' else 0
  top=[(x,y) for x,y in pts if y<37+dy];check(dr+po+' reconstructed smooth crown exact HR13',all(dm.getpixel(p)==baseline.getpixel(p) for p in top))
  bald[dr][po]={'alreadyBald':True,'baldnessCellsChanged':0,'headContour':'Existing smooth authored reconstruction; not source-measured skull','actualHeadColors':[list(c) for c in sorted(colors)]}
  x=col*400;y=row*370;d.text((x+5,y+3),dr+' '+po+' / DRESSED | BALD',fill='#253340');put(plate,h,x+10,y+22,4);put(plate,dm,x+150,y+22,4);put(plate,h,x+290,y+160,1);put(plate,dm,x+334,y+160,1);anchor(d,x+10,y+22,4);anchor(d,x+150,y+22,4)
d.text((5,1480),'All16 existing distinct direction/pose pairs; bald already, zero head edits; hidden skull reconstructed/authored, not observed bones.',fill='#253340');plate.save(dest/'all-directions-allunique-dressed-bald.png')
# Existing eight slots and exact source delays; native/4x synchronized material proof.
for withref in (False,True):
 frames=[]
 for index,po in enumerate(order):
  cols=[oldim('hero',po),actual('hero','south',po),oldim('dummy',po),actual('dummy','south',po)]
  if withref:cols=[Image.open(ext/f'reference-south-{po}.png').convert('RGBA')]+cols
  p=Image.new('RGB',(40*len(cols),96),'#bed4d5');d=ImageDraw.Draw(p);d.fontmode='1';d.text((1,1),str(index)+' '+po+' '+('REF/B/A/b/a' if withref else 'BEFORE/AFTER H/D'),fill='#253340')
  for c,im in enumerate(cols):put(p,im,c*40+4,21,1);anchor(d,c*40+4,21,1)
  frames.append(p)
 for scale in (1,4):
  ims=[p.resize((p.width*scale,p.height*scale),Image.Resampling.NEAREST) for p in frames]
  path=(ext if withref else dest)/f'south-{"source-" if withref else ""}before-after-{scale}x.gif'
  ims[0].save(path,save_all=True,append_images=ims[1:],duration=[100]*8,loop=0,optimize=False,disposal=2)
  gif=Image.open(path);check(str(path)+' eight slots',gif.n_frames==8 and gif.info['loop']==0)
  for i,expected in enumerate(ims):gif.seek(i);check(str(path)+str(i)+' exact decoded panel/delay',gif.convert('RGB').tobytes()==expected.tobytes() and gif.info['duration']==100)
# All existing direction loops, actual source export holds; no new poses.
for dr in ('south','north','west','east'):
 for slow in (False,True):
  delays=([100]*8 if dr=='south' else [70,60,70,70,70,60,70,70]);delays=[v*(4 if slow else 1) for v in delays];panels=[]
  for i,po in enumerate(order):
   p=Image.new('RGB',(80,96),'#bed4d5');dd=ImageDraw.Draw(p);dd.fontmode='1';dd.text((1,1),dr+' '+str(i)+(' SLOW' if slow else ''),fill='#253340');put(p,actual('hero',dr,po),4,21,1);put(p,actual('dummy',dr,po),44,21,1);anchor(dd,4,21,1);anchor(dd,44,21,1);panels.append(p)
  for scale in (1,4):
   ims=[im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST) for im in panels];path=dest/f'{dr}-dressed-bald-{"slow" if slow else "normal"}-{scale}x.gif';ims[0].save(path,save_all=True,append_images=ims[1:],duration=delays,loop=0,optimize=False,disposal=2);g=Image.open(path);check(path.name+' eight exact holds',g.n_frames==8 and g.info['loop']==0)
   for i,im in enumerate(ims):g.seek(i);check(path.name+str(i)+' decoded exact',g.convert('RGB').tobytes()==im.tobytes() and g.info['duration']==delays[i])
# Editable files match actual PNGs and retain every frame name/tick.
for kind in ('hero','dummy'):
 for view in ('idles','south-walk'):
  p=json.loads((src/f'{kind}-{view}.sprite.json').read_text());b=json.loads((dest/f'before-{kind}-{view}.sprite.json').read_text());check(kind+view+' order/ticks exact',[(f['name'],f['ticks']) for f in p['frames']]==[(f['name'],f['ticks']) for f in b['frames']]);pal=[(0,0,0,0)]+[tuple(bytes.fromhex(c[1:]))+(255,) for c in p['palette'][1:]]
  for i,f in enumerate(p['frames']):
   im=actual(kind,('south','north','west','east')[i] if view=='idles' else 'south','idle' if view=='idles' else order[i]);check(kind+view+str(i)+' source exact PNG',list(im.get_flattened_data())==[pal[j] for j in f['pixels']])
report={'scope':'Existing HR14 front wrist material correction only','beforeSourceCommit':'de8393e','bodyGeometry':'All alpha/ink/navy, head/feet/rows54+, pack layers and timing exact','poses':poses,'baldAudit':bald,'baldnessCellsChanged':0,'assertionCount':len(checks),'checks':checks,'allScopedChecksPass':True,'visualApproval':False,'currentMotionEvidence':'New8slot before/after GIFs decoded exact; no new uninterrupted browser-watch claim. Old rendered-cycle trace is historical c98a8cb evidence, not current corrected south SHA.','otherScope':'Girl files and NWE native/export files protected; user later authorized Girl continuation separately; no Girl file changed during this pass.'};(dest/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(checks),'scoped assertions; changed cells',{p:v['changedCount'] for p,v in poses.items()},'bald edits0')
