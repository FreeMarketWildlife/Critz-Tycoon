"""Observed costume planes/near-tip cues, never inferred foot anatomy."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,subprocess,io
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR14';ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
meta=json.loads((src/'construction.json').read_text());dirs=('south','north','west','east');poses=('A','P','C');base='2750f65'
C={'darkPlane':(70,86,113),'slateShadow':(155,131,212),'slateLight':(101,166,222),'warmGray':(166,216,226),'coral':(222,139,103),'paleBand':(241,209,113)};outline=(37,51,64)
r={'task':'M1.HR14 material contrast / visible foot-landmark pass','baseline':base,'anatomyStatus':'Hidden hip/knee/ankle/anatomicalfoot sites remain null. N/W/E black tips join black costume: internal pants/shoe boundary AMBIGUOUS. Never split alpha or infer leg length.','frames':{},'canonicalPackAndStrapsExact':True,'packColumnConnection':{},'chest':{},'visualApproval':False,'maskColorStatus':'SOURCE-DERIVED PLANES / DIAGRAM COLORS; not literal source RGB or anatomy'}
def old(kind,d,p):return Image.open(io.BytesIO(subprocess.check_output(['git','show',base+f':docs/reviews/M1-HR14/{kind}-{d}-{p}.png'],cwd=root))).convert('RGBA')
def spans(im,y):
 v=[]
 for x in range(32):
  if im.getpixel((x,y))[3]:
   if v and v[-1][1]==x:v[-1][1]=x+1
   else:v.append([x,x+1])
 return v
def sourceclass(px):
 a,b,c,z=px
 if not z:return None
 if a==b==c==0 or a<30:return 'darkPlane'
 if b>180 and a<160:return 'warmGray'
 if b>120 and a<100:return 'slateLight'
 if a>240 and b>230:return 'paleBand'
 if a>180 and b<120:return 'coral'
 return 'slateShadow'
for d in dirs:
 for p in ('idle','A','P','C'):
  h=Image.open(out/f'hero-{d}-{p}.png').convert('RGBA');m=Image.open(out/f'dummy-{d}-{p}.png').convert('RGBA');bh=old('hero',d,p);bm=old('dummy',d,p);e=meta['directions'][d][p];dy=-2 if p=='P' else 0
  assert h.getchannel('A').tobytes()==bh.getchannel('A').tobytes() and m.getchannel('A').tobytes()==bm.getchannel('A').tobytes()
  changed=[]
  for y in range(64):
   for x in range(32):
    if h.getpixel((x,y))!=bh.getpixel((x,y)):
     assert d=='south' and 12<=x<=19 and 46+dy<=y<49+dy and bh.getpixel((x,y))[:3]==(249,237,200) and h.getpixel((x,y))[:3]==(237,116,92),(d,p,x,y,'outside bounded chest recolor');changed.append([x,y])
    if y>=54:assert h.getpixel((x,y))==bh.getpixel((x,y)),(d,p,'Hero lowerpixels changed')
  assert all(h.getpixel((i%32,i//32))==bh.getpixel((i%32,i//32)) for i,on in enumerate(e['headMaskHero']) if on)
  planes=e['visibleMaterialPlanes'];planeAt={tuple(pt):name for name,pts in planes.items() for pt in pts}
  for y in range(64):
   for x in range(32):
    if m.getpixel((x,y))!=bm.getpixel((x,y)):
     assert (x,y) in planeAt,(d,p,x,y,'dummy recolor outside observed plane')
    if (x,y) in planeAt:
     expected=outline if h.getpixel((x,y))[:3]==(36,35,48) else C[planeAt[(x,y)]]
     assert m.getpixel((x,y))[:3]==expected,(d,p,x,y,planeAt[(x,y)],m.getpixel((x,y)),expected)
  r['chest'][d+'/'+p]={'changedCells':changed,'creamReduction':len(changed),'alphaAndHeadUnchanged':True,'lowerBandCollarCuffsRetained':True}
  for kind in ('pack-layer','strap-layer'):assert Image.open(out/f'{kind}-{d}-{p}.png').convert('RGBA').tobytes()==old(kind,d,p).tobytes()
  if p=='idle':continue
  ref=Image.open(ext/f'reference-{d}-{p}.png').convert('RGBA');last=ref.getbbox()[3]-1;ss=spans(ref,last);assert spans(h,last)==ss==spans(m,last)
  planeMasks={k:[] for k in C}
  for y in range(54,64):
   for x in range(32):
    cl=sourceclass(ref.getpixel((x,y)))
    assert bool(ref.getpixel((x,y))[3])==bool(h.getpixel((x,y))[3])==bool(m.getpixel((x,y))[3])
    if cl:
     planeMasks[cl].append([x,y]);expected=outline if h.getpixel((x,y))[:3]==(36,35,48) else C[cl];assert m.getpixel((x,y))[:3]==expected,(d,p,x,y,'source material plane lost')
  pale=planeMasks['paleBand'];assert bool(pale)==(d=='south')
  cues=[]
  if d=='south':cues=[{'kind':'observed pale sole band','cells':pale,'confidence':'direct visible pale material; foot/ankle bones not inferred'}]
  else:
   cueRow=58 if p=='P' else 60
   cues=[{'kind':'observed colored near-contact accents','rows':[cueRow,cueRow+1],'cells':[pt for k,pts in planeMasks.items() if k!='darkPlane' for pt in pts if pt[1] in (cueRow,cueRow+1)],'confidence':'direct color planes only; pants/shoe internal boundary unresolved'}]
  r['frames'][d+'/'+p]={'lastPaintedRow':last,'lastPaintedSpans':ss,'lastContourWidths':[b-a for a,b in ss],'widthMeaning':'lowest visible COSTUME contour; not anatomical footwidth','edgeAnchor':[16,64],'sourceHeroDummyContourExact':True,'observedMaterialPlanes':planeMasks,'visibleFootLandmarks':cues,'internalPantsShoeBoundary':'UNRESOLVED except visible pale band itself' if d=='south' else 'AMBIGUOUS black-to-black costume join','hiddenJoints':None}
  if d in ('west','east') and p in ('A','C'):
   x=26 if d=='west' else 5;bag=Image.open(out/f'pack-layer-{d}-{p}.png').convert('RGBA');checks=[]
   for y in (48,49):
    inward=x-1 if d=='west' else x+1;assert bag.getpixel((x,y))[3] and bag.getpixel((inward,y))[3] and h.getpixel((x,y))==bag.getpixel((x,y));checks.append([x,y])
   r['packColumnConnection'][d+'/'+p]={'cells':checks,'description':'ONE additional column overTWOrows; attached to inward canonical bag neighbor','detached':False,'canonicalGeometryChanged':False}
# Current unique-pose explanatory contacts; full frames at shared anchor.
plate=Image.new('RGB',(1728,1600),'#bed4d5');dd=ImageDraw.Draw(plate);ink='#253340'
for row,d in enumerate(dirs):
 for col,p in enumerate(poses):
  x=col*576;y=row*400;dd.text((x+5,y+5),d.upper()+' '+p+' SOURCE | HERO | DUMMY | OBSERVED PLANES',fill=ink)
  ims=[Image.open(ext/f'reference-{d}-{p}.png').convert('RGBA'),Image.open(out/f'hero-{d}-{p}.png').convert('RGBA'),Image.open(out/f'dummy-{d}-{p}.png').convert('RGBA')]
  for n,im in enumerate(ims):
   big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+4+n*138,y+24),big);plate.paste(im,(x+52+n*138,y+304),im)
   ax=x+4+n*138+64;ay=y+24+256;dd.line((x+4+n*138,ay,x+132+n*138,ay),fill='#748894');dd.line((ax-4,ay,ax+4,ay),fill='#d84f5b');dd.line((ax,ay,ax,ay+4),fill='#d84f5b')
   ax=x+52+n*138+16;ay=y+304+64;dd.line((ax-2,ay,ax+2,ay),fill='#d84f5b');dd.line((ax,ay,ax,ay+2),fill='#d84f5b')
  rr=r['frames'][d+'/'+p];mask=Image.new('RGB',(32,10),'#bed4d5')
  for name,pts in rr['observedMaterialPlanes'].items():
   for xx,yy in pts:mask.putpixel((xx,yy-54),ims[2].getpixel((xx,yy))[:3])
  plate.paste(mask.resize((128,40),Image.Resampling.NEAREST),(x+424,y+190));dd.text((x+424,y+236),'x0..31 / y54..63',fill=ink)
  for n,(name,c) in enumerate(C.items()):dd.rectangle((x+424,y+28+n*23,x+434,y+38+n*23),fill=c);dd.text((x+440,y+27+n*23),{'darkPlane':'dark plane','slateShadow':'shadow plane','slateLight':'mid plane','warmGray':'light plane','coral':'accent plane','paleBand':'pale band'}[name],fill=ink)
  dd.text((x+424,y+164),'SOURCE-DERIVED',fill=ink);dd.text((x+424,y+178),'DIAGRAM COLORS',fill=ink)
  dd.text((x+5,y+288),'Costume row'+str(rr['lastPaintedRow'])+' spans'+str(rr['lastPaintedSpans'])+' widths'+str(rr['lastContourWidths']),fill=ink)
  cue=Image.new('RGBA',(32,64));source=ims[0]
  for yy in range(54,64):
   for xx in range(32):
    if source.getpixel((xx,yy))[3]:cue.putpixel((xx,yy),(133,145,158,255))
  for landmark in rr['visibleFootLandmarks']:
   for xx,yy in landmark['cells']:cue.putpixel((xx,yy),(241,209,113,255) if d=='south' else (237,145,100,255))
  cue.save(out/f'contact-cue-mask-{d}-{p}.png');small=cue.crop((0,54,32,64)).resize((128,40),Image.Resampling.NEAREST);plate.paste(small,(x+424,y+263),small)
  dd.text((x+424,y+247),'CUE != ANATOMY',fill=ink);dd.text((x+424,y+312),'Yellow=pale',fill=ink);dd.text((x+424,y+328),'Orange=tipcolor',fill=ink);dd.text((x+424,y+344),'Gray=ambiguous',fill=ink)
  dd.text((x+5,y+375),'P single10px COSTUME mass; shoe split unresolved.' if d in ('west','east') and p=='P' else 'Redcross=edgeanchor16,64; hidden leg/ankle/foot joints=NULL.',fill=ink)
plate.save(ext/'four-direction-material-source-hero-dummy.png')
# Native-context chest before/after reference comparison, original material only.
plate=Image.new('RGB',(1320,390),'#bed4d5');dd=ImageDraw.Draw(plate)
for col,p in enumerate(poses):
 x=col*440;dd.text((x+5,5),p+' SOURCE | BEFORE | QUIET CREAM',fill=ink)
 for n,im in enumerate((Image.open(ext/f'reference-south-{p}.png').convert('RGBA'),old('hero','south',p),Image.open(out/f'hero-south-{p}.png').convert('RGBA'))):
  big=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+4+n*144,25),big);plate.paste(im,(x+52+n*144,300),im)
 dd.text((x+5,373),'Color only; original collar/stripe/cuffs, head+alpha exact.',fill=ink)
plate.save(ext/'chest-source-before-quiet.png')
r['allMaterialChecksPass']=True;(out/'material-landmark-checks.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS: allHeroalpha/head/lowerRGBA protected; dummyalpha exact/distinctsourceplanes; contourspans exact; cream-only quieting; attachedprofilecolumn and canonicalpack unchanged.')
# All eight holds/phase slots with actual lower-plane pixels beside triptychs.
order=meta['order']
for d in dirs:
 plate=Image.new('RGB',(1920,700),'#bed4d5');dd=ImageDraw.Draw(plate)
 for i,p in enumerate(order):
  x=i%4*480;y=i//4*350;dd.text((x+3,y+4),d.upper()+f' frame{i} {p} / REF | HERO | DUMMY | PLANES | CUES',fill=ink)
  ref=Image.open(ext/f'reference-{d}-{p}.png').convert('RGBA');h=Image.open(out/f'hero-{d}-{p}.png').convert('RGBA');m=Image.open(out/f'dummy-{d}-{p}.png').convert('RGBA');mask=Image.new('RGBA',(32,64))
  for yy in range(54,64):
   for xx in range(32):mask.putpixel((xx,yy),m.getpixel((xx,yy)))
  mask.save(out/f'material-plane-pixels-{d}-{p}.png')
  cue=Image.open(out/f'contact-cue-mask-{d}-{p}.png').convert('RGBA')
  for n,im in enumerate((ref,h,m,mask,cue)):
   big=im.resize((96,192),Image.Resampling.NEAREST);plate.paste(big,(x+n*96,y+23),big);plate.paste(im,(x+n*96+32,y+230),im)
   ax=x+n*96+48;ay=y+215;dd.line((x+n*96,ay,x+n*96+95,ay),fill='#748894');dd.line((ax-3,ay,ax+3,ay),fill='#d84f5b');dd.line((ax,ay,ax,ay+3),fill='#d84f5b')
   ax=x+n*96+48;ay=y+294;dd.line((ax-2,ay,ax+2,ay),fill='#d84f5b');dd.line((ax,ay,ax,ay+2),fill='#d84f5b')
  rr=r['frames'][d+'/'+p];dd.text((x+3,y+302),'Row'+str(rr['lastPaintedRow'])+' spans'+str(rr['lastPaintedSpans']),fill=ink);dd.text((x+3,y+319),'16,64redanchor; cue=material only; hidden ankle/leg/foot=NULL.',fill=ink)
 plate.save(ext/f'{d}-all-eight-material-source-hero-dummy.png')
