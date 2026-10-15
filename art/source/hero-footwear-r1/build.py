"""FM1 bounded original West idle/P shoe MATERIAL trial. No geometry changes."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-FM1';pal=lambda c:tuple(bytes.fromhex(c[1:]))+(255,)
# Exact original South shoe ramp, view-specific side upper/sole. Native cells.
edits={}
for x in range(10,20):edits[x,58]='#ae454a' if x<19 else '#2a344a'
edits[10,58]='#ed745c';edits[11,58]='#ed745c';edits[14,58]='#bfc0aa'
for x in range(10,20):edits[x,59]='#ae454a' if x<18 else '#2a344a'
for x in range(11,19):edits[x,60]='#bfc0aa'
edits[11,60]='#f9edc8';edits[12,60]='#f9edc8'
checks={};record={};images={}
south=Image.open(root/'docs/reviews/M1-PS1/hero-south-idle.png').convert('RGBA');allowed={p for p in south.get_flattened_data() if p[3]}
for pose in ['idle','P']:
 tag='west-'+pose;hero=Image.open(root/f'docs/reviews/M1-PS1/hero-{tag}.png').convert('RGBA');folder=root/'docs/reviews/M1-CHT1'/tag;body=Image.open(folder/f'template-{tag}.png').convert('RGBA');trial=hero.copy();bt=body.copy();changed=[]
 for pt,c in edits.items():
  assert hero.getpixel(pt)[3] and hero.getpixel(pt)!=pal('#242330'),pt
  if hero.getpixel(pt)!=pal(c):changed.append({'xy':list(pt),'before':'#%02x%02x%02x'%hero.getpixel(pt)[:3],'after':c})
  trial.putpixel(pt,pal(c));bt.putpixel(pt,pal(c))
 checks[tag+' exact alpha']=hero.getchannel('A').tobytes()==trial.getchannel('A').tobytes()
 checks[tag+' exact contact row61']=hero.crop((0,61,32,64)).tobytes()==trial.crop((0,61,32,64)).tobytes()
 checks[tag+' all other pixels exact']=all(a==b for i,(a,b) in enumerate(zip(hero.get_flattened_data(),trial.get_flattened_data())) if (i%32,i//32) not in edits)
 checks[tag+' original shared palette only']=all(q in allowed for q in trial.get_flattened_data() if q[3])
 checks[tag+' template same material cells']=all(bt.getpixel(pt)==trial.getpixel(pt) for pt in edits)
 checks[tag+' template alpha exact']=body.getchannel('A').tobytes()==bt.getchannel('A').tobytes()
 record[pose]={'sourceSHA256':hashlib.sha256((root/f'docs/reviews/M1-PS1/hero-{tag}.png').read_bytes()).hexdigest(),'changedCells':changed,'contactRow':61,'scope':'Existing source-visible shoe material surface, not recovered hidden foot anatomy'}
 for name,im in [('current-hero',hero),('trial-hero',trial),('current-template',body),('trial-template',bt)]:im.save(out/(tag+'-'+name+'.png'))
 images[pose]=[hero,trial,body,bt]
assert all(checks.values()),checks
# Native/full comparison; only two requested poses.
plate=Image.new('RGB',(1160,620),'#efe9d6');d=ImageDraw.Draw(plate);d.fontmode='1'
for row,pose in enumerate(['idle','P']):
 y=row*300;d.text((10,y+5),'WEST '+pose+' / CURRENT HERO | SHOE MATERIAL TRIAL | SAME CHARACTER TEMPLATE / CURRENT | TRIAL',fill='#253340')
 for j,im in enumerate(images[pose]):
  x=j*285+15;q=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(q,(x,y+30),q);plate.paste(im,(x+170,y+150),im)
plate.save(out/'west-idle-P-material-trial.png')
grid=Image.new('RGB',(1120,470),'#efe9d6');d=ImageDraw.Draw(grid);d.fontmode='1'
for row,pose in enumerate(['idle','P']):
 for col,im in enumerate(images[pose][:2]):
  x=col*350+15;y=row*220+35;d.text((x,y-20),pose+' / '+('CURRENT' if col==0 else 'TRIAL')+' / ROWS54-63',fill='#253340');q=im.crop((0,54,32,64)).resize((320,100),Image.Resampling.NEAREST);grid.paste(q,(x,y),q)
  for gx in range(33):d.line((x+gx*10,y,x+gx*10,y+100),fill='#909986')
  for gy in range(11):d.line((x,y+gy*10,x+320,y+gy*10),fill='#909986')
q=south.crop((0,54,32,64)).resize((320,100),Image.Resampling.NEAREST);grid.paste(q,(750,35),q);d.text((750,15),'PROTECTED SOUTH / SAME SHOE COLOR RAMP',fill='#253340')
for gx in range(33):d.line((750+gx*10,35,750+gx*10,135),fill='#909986')
for gy in range(11):d.line((750,35+gy*10,1070,35+gy*10),fill='#909986')
d.text((750,180),'No silhouette/contact/waist change.',fill='#253340');d.text((750,200),'Original view-specific material proposal.',fill='#253340');d.text((750,220),'No source anatomy inference.',fill='#253340');d.text((750,240),'South/source artifacts unchanged.',fill='#253340')
grid.save(out/'west-idle-P-native-grid.png')
(src/'edits.json').write_text(json.dumps({'task':'M1.FM1','state':'ONE WEST IDLE/P MATERIAL TRIAL; UNAPPROVED','frame':[32,64],'anchor':[16,64],'source':'PS1 8726c9a; template CHT1 c600c29','poses':record,'checks':checks,'appearanceApproval':False},indent=2)+'\n')
(out/'checks.json').write_text(json.dumps({'pass':True,'checks':checks,'approval':False},indent=2)+'\n');print('FM1 trial',len(record['idle']['changedCells']),'idle /',len(record['P']['changedCells']),'P material cells;',len(checks),'checks pass')
