"""Concise HR8 LOCAL critique only. No Library/full-checkpoint acceptance."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib
root=Path(__file__).resolve().parents[3];base=Path(__file__).parent;out=root/'docs/reviews/M1-HR8';old=root/'docs/reviews/M1-HR7';ext=Path(sys.argv[1]).resolve();assert ext!=root and root not in ext.parents
rp=ext/'walking.png';assert hashlib.sha256(rp.read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
new={n:Image.open(out/f'hero-{n}.png').convert('RGBA') for n in ('south','north','west','east')};prior={n:Image.open(old/f'hero-{n}.png').convert('RGBA') for n in new};m=json.loads((base/'masks.json').read_text())
report={'task':'HR8','state':'LOCAL lower-body trial, not full checkpoint','wholeAppearanceAccepted':False,'headUpperBodyRows0To53ExactHR7':True,'earsAcceptedOnly':True,'directions':{}}
for n,img in new.items():
 assert img.crop((0,0,32,54)).tobytes()==prior[n].crop((0,0,32,54)).tobytes(),n+' upper-body drift'
 assert not sum(m[n]['mouth']) and not sum(m[n]['nose'])
 for k in ('leftArm','rightArm','nearArm','sleeve'):
  if k in m[n]:assert all(img.getpixel((i%32,i//32))==prior[n].getpixel((i%32,i//32)) for i,v in enumerate(m[n][k]) if v),n+' arm drift'
 changed=[(x,y) for y in range(64) for x in range(32) if img.getpixel((x,y))!=prior[n].getpixel((x,y))]
 assert all(54<=y<=61 for x,y in changed)
 report['directions'][n]={'changedPixels':len(changed),'changedBounds':[min(x for x,y in changed),min(y for x,y in changed),max(x for x,y in changed)+1,max(y for x,y in changed)+1],'upperBodyExact':True,'sha256':hashlib.sha256((out/f'hero-{n}.png').read_bytes()).hexdigest()}
 if n in ('west','east'):
  gap=19 if n=='west' else 12
  assert all(img.getpixel((gap,y))[3]==0 for y in (57,58)),n+' far/near calves merged'
  report['directions'][n]['visibleCalfGapRows57To58']=True
# Concise lower-body before/after: 5x crops and true native full frames.
p=Image.new('RGB',(900,240),'#eee6d0');d=ImageDraw.Draw(p)
for i,n in enumerate(new):
 x=10+i*225;d.text((x,10),n.upper()+' | HR7 / HR8 LOCAL',fill='#292b34')
 for j,group in enumerate((prior,new)):
  crop=group[n].crop((6,53,26,64)).resize((100,55),Image.Resampling.NEAREST);p.paste(crop,(x+108*j,40),crop);p.paste(group[n],(x+34+108*j,120),group[n])
d.text((12,214),'Cuff -> visible calf -> compact shoe. Native full frames below. LOCAL critique only.',fill='#292b34');p.save(out/'lower-body-local-before-after.png')
p=Image.new('RGB',(900,335),'#eee6d0');d=ImageDraw.Draw(p)
for i,n in enumerate(new):
 x=10+i*225;d.text((x,10),n.upper()+' | HR7 / HR8 LOCAL',fill='#292b34')
 for j,group in enumerate((prior,new)):
  img=group[n];big=img.resize((96,192),Image.Resampling.NEAREST);p.paste(big,(x+110*j,30),big);p.paste(img,(x+32+110*j,250),img)
p.save(out/'whole-body-local-before-after.png')
# Actual source side-by-side, cropped lower bodies AND full registered frames.
sheet=Image.open(rp);r=sheet.convert('RGBA');a=Image.new('L',sheet.size);a.putdata([255 if v else 0 for v in sheet.get_flattened_data()]);r.putalpha(a)
p=Image.new('RGB',(1000,710),'#eee6d0');d=ImageDraw.Draw(p)
for i,(n,f) in enumerate([('south',0),('north',1),('west',2),('east',2)]):
 x=15+(i%2)*500;y=12+(i//2)*350;d.text((x,y),n.upper()+' | REFERENCE2X / HR7 / HR8 LOCAL',fill='#292b34')
 ref=r.crop((16*f,0,16*f+16,32)).resize((32,64),Image.Resampling.NEAREST)
 if n=='east':ref=ref.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 for j,img in enumerate((ref,prior[n],new[n])):
  big=img.resize((96,192),Image.Resampling.NEAREST);p.paste(big,(x+155*j,y+25),big)
  crop=img.crop((6,53,26,64)).resize((120,66),Image.Resampling.NEAREST);p.paste(crop,(x+155*j,y+225),crop)
 d.text((x,y+314),'Fixed frame/anchor. Cuff/skin/shoe are visible materials; bones hidden.',fill='#292b34')
p.save(ext/'lower-body-reference-local.png')
(out/'local-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
# Check shoe overlap/leg attachment from independent saved masks and source pixels.
for n in ('west','east'):
 mm=m[n];overlap=sum(bool(a and b) for a,b in zip(mm['nearFoot'],mm['farFoot']));assert overlap>0,n+' disjoint shoe pads'
 assert any(a and b for a,b in zip(mm['nearCalf'],mm['nearFoot']))
 assert any(a and b for a,b in zip(mm['farCalf'],mm['farFoot']))
 assert any(mm['nearFoot'][61*32+x] for x in range(32))
 assert not any(mm['farFoot'][61*32+x] for x in range(32))
 assert any(mm['farFoot'][60*32+x] for x in range(32))
 gap=20 if n=='west' else 11
 assert all(new[n].getpixel((gap,y))[3]==0 for y in (60,61)),n+' continuous joined low sole'
 report['directions'][n]['nearFarShoeScaffoldOverlapCells']=overlap
 report['directions'][n]['nearSoleRow61RearVisibleHeelRow60']=True
 report['directions'][n]['rearHeelContourNotchRows60To61']=True
 report['directions'][n]['eachCalfTouchesOwnShoe']=True
 report['directions'][n]['materialReview']='Blue cuff, two short skin columns, foreground shoe partly occludes rear shoe; visible rear heel steps up one row. Near sole preserves row61 ground registration; low contour has a notch, not one flat rail.'
p=Image.new('RGB',(600,430),'#eee6d0');d=ImageDraw.Draw(p)
for i,n in enumerate(new):
 x=8+i*150;d.text((x,8),n.upper()+' | LOCAL1X / 2X',fill='#292b34')
 p.paste(new[n],(x+14,109),new[n]);big=new[n].resize((64,128),Image.Resampling.NEAREST);p.paste(big,(x+68,45),big)
 d.rectangle((x,211,x+142,422),fill='#263342');p.paste(new[n],(x+14,320),new[n]);p.paste(big,(x+68,256),big)
p.save(out/'native-light-dark-local.png')
(out/'local-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS local overlap/own-calf attachment/stepped rear heel and native light-dark plate.')

# Second local critique, focused on rear-heel contour. No whole-base acceptance.
p=Image.new('RGB',(680,265),'#eee6d0');d=ImageDraw.Draw(p)
for i,n in enumerate(('west','east')):
 x=12+i*340;d.text((x,10),n.upper()+' | REJECTED LOCAL A / LOCAL B',fill='#292b34')
 for j,folder in enumerate((out/'local-a',out)):
  img=Image.open(folder/f'hero-{n}.png').convert('RGBA');crop=img.crop((8,53,24,64)).resize((128,88),Image.Resampling.NEAREST);p.paste(crop,(x+160*j,40),crop);p.paste(img,(x+48+160*j,162),img)
d.text((12,245),'Near sole61 retained; partly occluded rear heel60 creates a notch. LOCAL critique.',fill='#292b34');p.save(out/'second-local-profile-before-after.png')
