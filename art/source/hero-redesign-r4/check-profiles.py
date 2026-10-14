"""Read saved PNGs, measure lower-body row shape, protect the corrected face."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR4';old=root/'docs/reviews/M1-HR3';refdir=Path(sys.argv[1]).resolve()
assert root not in refdir.parents and refdir!=root
refpath=refdir/'walking.png';assert hashlib.sha256(refpath.read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
ref=Image.open(refpath)
new={n:Image.open(out/f'hero-{n}.png').convert('RGBA') for n in ('south','north','west','east')}
prior={n:Image.open(old/f'hero-{n}.png').convert('RGBA') for n in new}
for n in ('south','north'):assert new[n].tobytes()==prior[n].tobytes(),n
for n in ('west','east'):assert new[n].crop((0,0,32,46)).tobytes()==prior[n].crop((0,0,32,46)).tobytes(),n+' face changed'
def span(img,y):
 xs=[x for x in range(32) if img.getpixel((x,y))[3]]
 return {'left':min(xs),'rightExclusive':max(xs)+1,'occupied':len(xs)}
rows=[]
for y in range(46,62):
 xs=[x for x in range(32) if ref.getpixel((32+x//2,y//2))]
 rows.append({'targetRow':y,'reference2x':{'left':min(xs),'rightExclusive':max(xs)+1,'occupied':len(xs)},'HR3':span(prior['west'],y),'HR4':span(new['west'],y)})
for row in rows:
 if row['targetRow']>=58:assert row['HR4']==row['reference2x'],row
# Actual opposite-facing lower-body silhouettes have reflected row registration.
for y in range(46,62):
 for x in range(32):assert bool(new['west'].getpixel((x,y))[3])==bool(new['east'].getpixel((31-x,y))[3])
# No disconnected foot/hand regions or return of nose point.
assert all(new['west'].getpixel((x,y))[3]==0 for y in range(35,42) for x in range(6))
assert all(new['east'].getpixel((x,y))[3]==0 for y in range(35,42) for x in range(26,32))
plate=Image.new('RGB',(680,430),'#eee6d0');d=ImageDraw.Draw(plate)
for i,n in enumerate(('west','east')):
 x=24+i*336;d.text((x,14),n.upper()+' | PREVIOUS / CORRECTED',fill='#292b34')
 for j,imgs in enumerate((prior,new)):
  img=imgs[n];big=img.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x+j*154,28),big)
  crop=img.crop((4,46,28,64));large=crop.resize((144,108),Image.Resampling.NEAREST);plate.paste(large,(x+j*154,286),large)
d.text((24,410),'Full 32x64 frames at 4x | lower body at 6x | same foot anchor',fill='#292b34');plate.save(out/'profile-before-after.png')
# Original-only native contrast plate: no screenshots/reference pixels.
plate=Image.new('RGB',(660,235),'#eee6d0');d=ImageDraw.Draw(plate)
for i,(name,bg) in enumerate((('LIGHT','#eee6d0'),('DARK','#263342'),('PATH','#c8aa7c'))):
 x=10+i*218;d.text((x,10),name+' | NATIVE AND 2X',fill='#292b34');d.rectangle((x,30,x+208,230),fill=bg)
 for j,n in enumerate(('west','east')):
  img=new[n];plate.paste(img,(x+32+j*96,35),img);big=img.resize((64,128),Image.Resampling.NEAREST);plate.paste(big,(x+16+j*96,100),big)
plate.save(out/'native-profile-check.png')
# Profile-only reference plate with source at exact2x beside Critz; reference stays external.
r=ref.convert('RGBA');a=Image.new('L',ref.size);a.putdata([255 if v else 0 for v in ref.get_flattened_data()]);r.putalpha(a)
rf=r.crop((32,0,48,32)).resize((32,64),Image.Resampling.NEAREST)
plate=Image.new('RGB',(650,400),'#eee6d0');d=ImageDraw.Draw(plate)
for i,(label,img) in enumerate((('EMERALD 2X',rf),('PREVIOUS HR3',prior['west']),('CORRECTED HR4',new['west']))):
 x=30+i*210;d.text((x,12),label,fill='#292b34');big=img.resize((128,256),Image.Resampling.NEAREST);plate.paste(big,(x,32),big);plate.paste(img,(x+48,318),img)
d.text((30,385),'Matched frame, ground anchor and pixel scale; original Critz character.',fill='#292b34');plate.save(refdir/'profile-reference.png')
report={'referenceRevision':'5eff78649e7170a877b961ef0b3da13b81a16038','referenceFrame':2,'sourceOnly':True,'fullRows46To61':rows,'finalFourFootRowsEqualMeasuredReferenceEnvelope':True,'facePixelsAbove46Unchanged':True,'frontBackExact':True,'noseCorrectionRetained':True,'oppositeLowerBodyMasksReflect':True,'styleApproval':'awaiting user'}
(out/'profile-checks.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: four foot-row envelopes, protected faces/front/back, opposite silhouettes and retained nose correction.')
