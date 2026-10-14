from PIL import Image,ImageDraw
from pathlib import Path
import hashlib,json,sys
r=Path(__file__).resolve().parents[3];p=Path(sys.argv[1]).resolve()
assert p != r and r not in p.parents, 'Reference images must stay outside the project'
assert (p/'walking.png').is_file(), 'Pass an external folder containing the pinned walking.png'
im=Image.open(p/'walking.png');assert hashlib.sha256((p/'walking.png').read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
rgba=im.convert('RGBA');a=Image.new('L',im.size);a.putdata([255 if v else 0 for v in im.get_flattened_data()]);rgba.putalpha(a)
plate=Image.new('RGB',(760,530),'#eee6d0');d=ImageDraw.Draw(plate)
for i,(n,f) in enumerate([('SOUTH',0),('NORTH',1),('WEST',2)]):
 ref=rgba.crop((f*16,0,f*16+16,32)).resize((32,64),Image.Resampling.NEAREST);hero=Image.open(r/f'docs/reviews/M1-HR4/hero-{n.lower()}.png')
 x=25+i*248;d.text((x,12),n+' | EMERALD 2X / CRITZ 1X',fill='#292b34')
 for j,img in enumerate((ref,hero)):
  big=img.resize((96,192),Image.Resampling.NEAREST);plate.paste(big,(x+j*115,40),big);plate.paste(img,(x+32+j*115,290),img)
  for y,c,label in [(38,'#8d668d','eyes'),(46,'#719e93','shoulder'),(56,'#c3a460','feet band'),(62,'#8b7b68','foot edge')]:
   yy=40+y*3;d.line((x+j*115,yy,x+j*115+96,yy),fill=c)
 d.text((x,370),'Same frame + foot registration',fill='#292b34')
d.text((25,425),'Reference-only comparison. Original Critz hair, skin, costume, pixels.',fill='#292b34')
d.text((25,449),'Guides: eyes row38, shoulder46, lower-body56, painted foot edge62.',fill='#292b34')
d.text((25,473),'Actual source frame analysis; no emulator observation.',fill='#292b34')
plate.save(p/'matched-reference.png')
# Independent annotation windows: these are visible bands, not inferred bone dimensions.
wins={'headwear_band':(0,10,16,18),'face_ear_band':(0,18,16,23),'shoulder_band':(0,23,16,24),'torso_window':(5,23,11,28),'left_arm_window':(1,23,5,27),'right_arm_window':(11,23,15,27),'lower_body_band':(3,28,13,31)}
data={}
hero=Image.open(r/'docs/reviews/M1-HR4/hero-south.png')
for n,(l,t,rr,b) in wins.items():
 pts=[(x,y) for y in range(t,b) for x in range(l,rr) if im.getpixel((x,y))]
 rb=[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts)+1,max(y for x,y in pts)+1]
 target=[v*2 for v in rb]; hp=[(x,y) for y in range(t*2,b*2) for x in range(l*2,rr*2) if hero.getpixel((x,y))[3]]
 hb=[min(x for x,y in hp),min(y for x,y in hp),max(x for x,y in hp)+1,max(y for x,y in hp)+1]
 data[n]={'referenceWindow':[l,t,rr,b],'referenceBounds':rb,'doubleTarget':target,'actualBoundsWithinWindow':hb,'deviation':[a-b for a,b in zip(hb,target)]}
(r/'docs/reviews/M1-HR4/reference-measurements.json').write_text(json.dumps({'referenceSha256':hashlib.sha256((p/'walking.png').read_bytes()).hexdigest(),'sourceRevision':'5eff78649e7170a877b961ef0b3da13b81a16038','framesInspected':[0,1,2],'sourceOnly':True,'bands':data},indent=2)+'\n')
print('PASS: pinned source hash and 7 independently measured annotation windows; reference plate stays external.')
