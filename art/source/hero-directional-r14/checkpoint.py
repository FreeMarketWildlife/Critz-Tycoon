"""Independent saved-pixel boundary and torso-registration checkpoint.
Reference-colored proof files are external, never included in build/repo.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR14';ext=Path(sys.argv[1]).resolve();old=ext.parent/'hero-hr13-review';assert root not in ext.parents
meta=json.loads((src/'construction.json').read_text());dirs=('south','north','west','east');order=meta['order'];r={'task':'M1.HR14 first aligned boundary/pack checkpoint','lowerComparedRows':[54,64],'sourceGIFFact':'8x100ms;SHA pinned;fixed14top/2bottom32x64;front only','boundaryChecks':{},'packChecks':{},'projection':'head unchanged from HR13, no visible neck column introduced','hiddenBones':'UNRESOLVED / inferred and occluded; no added visible calf','visualApproval':False}
gifpath=ext.parent/'brendan-user-reference-original/01agijgmbz561.gif';assert hashlib.sha256(gifpath.read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e';gif=Image.open(gifpath);front=[]
for i in range(8):
 gif.seek(i);assert gif.info['duration']==100;im=Image.new('RGBA',(32,64));im.paste(gif.convert('RGBA').crop((0,0,128,192)).resize((32,48),Image.Resampling.NEAREST),(0,14));front.append(im)
assert gif.n_frames==8
refs={};ids={'north':[5,1,6],'west':[7,2,8],'east':[7,2,8]}
for d in dirs:
 refs[d]={}
 for n,p in enumerate(('A','P','C')):
  im=front[[0,2,4][n]] if d=='south' else Image.open(old/f'ROM-{ids[d][n]:02}.png').convert('RGBA')
  if d=='east':im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  refs[d][p]=im;im.save(ext/f'reference-{d}-{p}.png')
 def norm(im,dy):
  q=Image.new('RGBA',(32,64));q.paste(im,(0,-dy));return q
 canonpack=None;canonstraps=None
 for p in ('idle','A','P','C'):
  e=meta['directions'][d][p];dy=e['torsoTransform'][1];pack=Image.open(out/f'pack-layer-{d}-{p}.png').convert('RGBA');strap=Image.open(out/f'strap-layer-{d}-{p}.png').convert('RGBA')
  pn=norm(pack,dy).tobytes();sn=norm(strap,dy).tobytes()
  if canonpack is None:canonpack,canonstraps=pn,sn
  assert canonpack==pn and canonstraps==sn,(d,p,'rigid layer changes')
  assert e['torsoAnchor']==[16,48+dy]
  h=Image.open(out/f'hero-{d}-{p}.png').convert('RGBA')
  vis=Image.open(out/f'pack-visible-{d}-{p}.png').convert('RGBA')
  for y in range(64):
   for x in range(32):
    if vis.getpixel((x,y))[3]:assert h.getpixel((x,y))==pack.getpixel((x,y))
  r['packChecks'][d+'/'+p]={'torsoAnchor':e['torsoAnchor'],'torsoLocalLayerRGBAsha256':hashlib.sha256(pn).hexdigest(),'torsoLocalStrapRGBAsha256':hashlib.sha256(sn).hexdigest(),'visiblePackPixels':sum(bool(px[3]) for px in vis.get_flattened_data()),'rigid':True,'compositeChecked':True}
  if p=='idle':continue
  ref=refs[d][p];delta=[];materialDelta=[]
  for y in range(54,64):
   for x in range(32):
    if bool(ref.getpixel((x,y))[3])!=bool(h.getpixel((x,y))[3]):delta.append([x,y])
  assert not delta,(d,p,delta)
  r['boundaryChecks'][d+'/'+p]={'alphaMismatchCells':len(delta),'paintedBottomHero':h.getbbox()[3]-1,'paintedBottomSource':ref.getbbox()[3]-1,'lowerAlphaExact':True}
# Complete firstcheckpoint3posesx4directions with grid registered lower overlay.
plate=Image.new('RGB',(1440,1280),'#bed4d5');dd=ImageDraw.Draw(plate)
for row,d in enumerate(dirs):
 for col,p in enumerate(('A','P','C')):
  xx=col*480;yy=row*320;dd.text((xx+6,yy+5),f'{d.upper()} {p} / SOURCE | HERO | DUMMY / SAME32x64',fill='#253340')
  for n,im in enumerate((refs[d][p],Image.open(out/f'hero-{d}-{p}.png').convert('RGBA'),Image.open(out/f'dummy-{d}-{p}.png').convert('RGBA'))):
   plate.paste(im.resize((96,192),Image.Resampling.NEAREST),(xx+8+n*100,yy+22),im.resize((96,192),Image.Resampling.NEAREST));plate.paste(im,(xx+40+n*100,yy+228),im)
  # Matching silhouettes white; missing red; excess blue, no per-pose fitting.
  crop=Image.new('RGB',(32,10),'#bed4d5');h=Image.open(out/f'hero-{d}-{p}.png').convert('RGBA');ref=refs[d][p]
  for y in range(54,64):
   for x in range(32):
    a=ref.getpixel((x,y))[3]>0;b=h.getpixel((x,y))[3]>0
    if a or b:crop.putpixel((x,y-54),(248,248,248) if a==b else (230,70,70) if a else (70,90,230))
  plate.paste(crop.resize((160,50),Image.Resampling.NEAREST),(xx+312,yy+131));dd.text((xx+312,yy+188),'Rows54..63: exact alpha',fill='#253340');dd.text((xx+312,yy+204),'white=both;red/blue=diff',fill='#253340')
  dd.text((xx+8,yy+306),'Hidden knees/calf not inferred from costume. No visual approval.',fill='#253340')
plate.save(ext/'first-native-aligned-boundary-checkpoint.png')
# Actual bag layers, all8 registered at torso. Canonical white vs visible blue.
plate=Image.new('RGB',(1280,760),'#bed4d5');dd=ImageDraw.Draw(plate)
for row,d in enumerate(dirs):
 dd.text((6,row*190+4),d.upper()+' / PACK registered to torso16,48 / A,A,P,P,C,C,P,P',fill='#253340')
 for i,p in enumerate(order):
  e=meta['directions'][d][p];dy=e['torsoTransform'][1];h=Image.open(out/f'hero-{d}-{p}.png').convert('RGBA');bag=Image.open(out/f'pack-layer-{d}-{p}.png').convert('RGBA');vis=Image.open(out/f'pack-visible-{d}-{p}.png').convert('RGBA');h=norm(h,dy);bag=norm(bag,dy);vis=norm(vis,dy)
  im=Image.new('RGBA',(32,64),'#bed4d5');im.alpha_composite(h)
  for y in range(64):
   for x in range(32):
    if bag.getpixel((x,y))[3]:im.putpixel((x,y),(70,180,230,255) if vis.getpixel((x,y))[3] else (248,248,248,255))
  ImageDraw.Draw(im).point((16,48),fill='#ed745c');plate.paste(im.resize((64,128),Image.Resampling.NEAREST),(i*160+40,row*190+23));dd.text((i*160+6,row*190+155),f'frame{i}; dy{dy}',fill='#253340')
plate.save(out/'torso-registered-pack-all-eight.png')
r['allCheckpointChecksPass']=True;(out/'first-checkpoint-checks.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS: all12 unique loweralpha masks exact to actual fixed source;16 pack/strap/composite checks rigid. Firstcheckpoint READY, UNAPPROVED.')
