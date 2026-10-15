"""Actual aligned head overlay. Reference pixels are written ONLY outside repository."""
from PIL import Image,ImageDraw,ImageColor
from pathlib import Path
import json,sys,hashlib
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR5';old=root/'docs/reviews/M1-HR4';ext=Path(sys.argv[1]).resolve()
assert ext!=root and root not in ext.parents
path=ext/'walking.png';assert hashlib.sha256(path.read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
sheet=Image.open(path);rgba=sheet.convert('RGBA');alpha=Image.new('L',sheet.size);alpha.putdata([255 if n else 0 for n in sheet.get_flattened_data()]);rgba.putalpha(alpha)
# Full-frame native correspondence: no translating/cropping a sprite to force fit.
plate=Image.new('RGB',(840,750),'#eee6d0');d=ImageDraw.Draw(plate)
metrics={}
for i,(name,f) in enumerate([('south',0),('north',1),('west',2)]):
 ref=rgba.crop((f*16,0,f*16+16,32)).resize((32,64),Image.Resampling.NEAREST);prev=Image.open(old/f'hero-{name}.png').convert('RGBA');hero=Image.open(out/f'hero-{name}.png').convert('RGBA')
 assert hero.crop((0,46,32,64)).tobytes()==prev.crop((0,46,32,64)).tobytes(), name+' changed protected body'
 def pts(img):return {(x,y) for y in range(20,46) for x in range(32) if img.getpixel((x,y))[3]}
 rr=pts(ref);pp=pts(prev);hh=pts(hero)
 metrics[name]={'before':{'intersection':len(rr&pp),'union':len(rr|pp),'extra':len(pp-rr),'missing':len(rr-pp),'IoU':len(rr&pp)/len(rr|pp)},'after':{'intersection':len(rr&hh),'union':len(rr|hh),'extra':len(hh-rr),'missing':len(rr-hh),'IoU':len(rr&hh)/len(rr|hh)},'rows':[]}
 for y in range(20,46):
  def span(img):
   xs=[x for x in range(32) if img.getpixel((x,y))[3]]
   return [min(xs),max(xs)+1,len(xs)] if xs else None
  metrics[name]['rows'].append({'targetRow':y,'reference2x':span(ref),'HR4':span(prev),'HR5':span(hero)})
 y0=18+i*242;d.text((15,y0),name.upper()+' — REFERENCE / NEW HERO / ACTUAL 50% OVERLAY / SILHOUETTE DIFFERENCE',fill='#292b34')
 overlay=Image.alpha_composite(Image.new('RGBA',(32,64),'#eee6d0'),ref);t=hero.copy();t.putalpha(t.getchannel('A').point(lambda n:round(n*.5)));overlay=Image.alpha_composite(overlay,t)
 diff=Image.new('RGB',(32,64),'#eee6d0')
 for y in range(64):
  for x in range(32):
   a=bool(ref.getpixel((x,y))[3]);b=bool(hero.getpixel((x,y))[3]);c='#53685c' if a and b else '#d85462' if b else '#4588bd' if a else '#eee6d0';diff.putpixel((x,y),ImageColor.getrgb(c))
 for j,img in enumerate((ref,hero,overlay,diff)):
  crop=img.crop((0,18,32,48)).resize((192,180),Image.Resampling.NEAREST)
  if crop.mode=='RGBA':plate.paste(crop,(15+j*205,y0+25),crop)
  else:plate.paste(crop,(15+j*205,y0+25))
 d.text((15,y0+211),'Same scale/anchor. Red: Hero only; blue: reference only; dark green: shared.',fill='#292b34')
plate.save(ext/'head-overlay.png')
# Focused before/after overlays, original vs actual reference stays external.
p=Image.new('RGB',(650,480),'#eee6d0');pd=ImageDraw.Draw(p)
for i,(name,f) in enumerate([('south',0),('west',2)]):
 ref=rgba.crop((f*16,0,f*16+16,32)).resize((32,64),Image.Resampling.NEAREST)
 for j,(label,folder) in enumerate([('HR4 OVERLAY',old),('HR5 OVERLAY',out),('HR5 CLEAN',out)]):
  h=Image.open(folder/f'hero-{name}.png').convert('RGBA')
  if j<2:
   t=h.copy();t.putalpha(t.getchannel('A').point(lambda n:round(n*.5)));img=Image.alpha_composite(ref,t)
  else:img=h
  crop=img.crop((0,18,32,48)).resize((192,180),Image.Resampling.NEAREST);x=15+j*210;y=15+i*235;pd.text((x,y),name.upper()+' '+label,fill='#292b34');p.paste(crop,(x,y+25),crop)
p.save(ext/'before-after-overlay.png')
report={'referenceRevision':'5eff78649e7170a877b961ef0b3da13b81a16038','referenceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'nativeReferenceFrames':[0,1,2],'comparisonRegion':[0,20,32,46],'alignment':'full 32x64 frames; reference exact2x; shared anchor16,64; zero per-sprite translations','sourceOnly':True,'protectedBodyBelow46Exact':True,'heads':metrics,'caution':'Includes reference headwear versus original hair; overlap measures silhouette agreement, not beauty or hidden anatomy.'}
(out/'head-overlay-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({n:{'before':v['before'],'after':v['after']} for n,v in metrics.items()},indent=2))
# Original-only before/after plate may be checked in; it contains no reference pixels.
beforeafter=Image.new('RGB',(850,420),'#eee6d0');bd=ImageDraw.Draw(beforeafter)
for i,name in enumerate(('south','north','west')):
 x=10+i*282;bd.text((x,12),name.upper()+' | HR4 / HR5',fill='#292b34')
 for j,folder in enumerate((old,out)):
  img=Image.open(folder/f'hero-{name}.png').convert('RGBA');large=img.resize((128,256),Image.Resampling.NEAREST);beforeafter.paste(large,(x+138*j,28),large);beforeafter.paste(img,(x+48+138*j,320),img)
bd.text((12,395),'Clean 4x and native1x | all pixels below row46 unchanged',fill='#292b34');beforeafter.save(out/'head-before-after.png')
# Verify saved head geometry, including non-projecting profile face and visible profile eye.
m=json.loads((root/'art/source/hero-redesign-r5/masks.json').read_text());w=Image.open(out/'hero-west.png');e=Image.open(out/'hero-east.png')
left=[min(x for x in range(32) if w.getpixel((x,y))[3]) for y in range(35,43)]
assert left==sorted(left),left
right=[max(x for x in range(32) if e.getpixel((x,y))[3]) for y in range(35,43)]
assert right==sorted(right,reverse=True),right
assert sum(m['west']['eyes'])==8
assert all(w.getpixel((x,y))[:3] in [(36,35,48),(42,52,74)] for y in range(38,42) for x in (10,11))
for name in ('south','north'):
 mask=m[name]['jawContact'];assert all(mask[y*32+x]==mask[y*32+31-x] for y in range(64) for x in range(32))
for name in metrics:
 assert metrics[name]['after']['extra']+metrics[name]['after']['missing'] < metrics[name]['before']['extra']+metrics[name]['before']['missing'],name
report['profileEyeRect']=[10,38,12,42];report['noseFreeProfileContours']={'westRows35To42':left,'eastRows35To42':right};report['jawContactMasksSymmetric']=True
(out/'head-overlay-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: saved profile eye, no-nose contour, jaw masks, protected bodies and reduced head silhouette differences in all three reference views.')
