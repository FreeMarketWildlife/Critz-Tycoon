"""Original-only review goes in repo; source/combined pixels stay external."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR11';ext=Path(sys.argv[1]).resolve();assert ext!=root and root not in ext.parents
hero=[Image.open(out/f'walk-{i:02}.png').convert('RGBA') for i in range(8)];ref=[Image.open(ext/f'registered-left-{i:02}.png').convert('RGBA') for i in range(8)]
# All8, including paired duplicate frames, source/candidate at identical pixel scale.
p=Image.new('RGB',(1024,640),'#eee6d0');d=ImageDraw.Draw(p);d.fontmode='1'
for i in range(8):
 x=(i%4)*256;y=(i//4)*320;d.text((x+10,y+8),f'{i} / 100ms | SOURCE / HERO',fill='#242330')
 for j,im in enumerate((ref[i],hero[i])):
  big=im.resize((96,192),Image.Resampling.NEAREST);p.paste(big,(x+15+j*125,y+35),big);p.paste(im,(x+47+j*125,y+242),im)
p.save(ext/'source-hero-all-eight-contact.png')
p=Image.new('RGB',(1024,360),'#eee6d0');d=ImageDraw.Draw(p);d.fontmode='1'
for i,im in enumerate(hero):
 x=i*128;d.text((x+6,8),f'{i} / 100ms',fill='#242330');big=im.resize((128,256),Image.Resampling.NEAREST);p.paste(big,(x,28),big);p.paste(im,(x+48,285),im)
p.save(out/'hero-all-eight-contact.png')
# Stable proposed-idle/three-key-pose contact, current PNGs only.
p=Image.new('RGB',(660,360),'#eee6d0');d=ImageDraw.Draw(p);d.fontmode='1'
for i,(label,name) in enumerate([('PROPOSED IDLE','idle-forward.png'),('STRIDE A','walk-00.png'),('PASSING','walk-02.png'),('STRIDE C','walk-04.png')]):
 x=15+i*160;d.text((x,10),label,fill='#242330');im=Image.open(out/name).convert('RGBA');big=im.resize((128,256),Image.Resampling.NEAREST);p.paste(big,(x,30),big);p.paste(im,(x+48,290),im)
p.save(out/'draft-poses.png')

# Opaque labeled native comparison then exact4x enlargement of the entire panel.
comp=[]
for i in range(8):
 im=Image.new('RGBA',(88,82),'#eee6d0');d=ImageDraw.Draw(im);d.fontmode='1';d.text((7,1),'REF',fill='#242330');d.text((45,1),'HERO',fill='#242330');im.alpha_composite(ref[i],(4,16));im.alpha_composite(hero[i],(48,16));comp.append(im);im.save(ext/f'comparison-native-{i:02}.png')
def project(frames,name):
 w,h=frames[0].size;values=[];lookup={}
 for im in frames:
  for rgba in im.get_flattened_data():
   if rgba[3]:
    c='#%02x%02x%02x'%rgba[:3]
    if c not in lookup:lookup[c]=len(values)+1;values.append(c)
 assert len(values)<=255
 pixels=[]
 for i,im in enumerate(frames):pixels.append({'name':str(i),'ticks':6,'pixels':[lookup['#%02x%02x%02x'%c[:3]] if c[3] else 0 for c in im.get_flattened_data()]})
 return {'format':'fmw-sprite','version':1,'name':name,'preset':'custom','width':w,'height':h,'palette':[None]+values,'bank':'custom','notes':'Review raster only; exact100ms GIF using6 editor ticks rounded to GIF centiseconds. No native asset resampling.','frames':pixels}
jobs=[]
for frames,name,path in [(hero,'original-native',out/'hero-forward-walk-native.gif'),([im.resize((128,256),Image.Resampling.NEAREST) for im in hero],'original-4x',out/'hero-forward-walk-4x.gif'),(comp,'reference-hero-native',ext/'source-hero-native.gif'),([im.resize((352,328),Image.Resampling.NEAREST) for im in comp],'reference-hero-4x',ext/'source-hero-4x.gif')]:
 tmp=ext/(name+'.review-project.json');tmp.write_text(json.dumps(project(frames,name),separators=(',',':')));jobs.append({'project':str(tmp),'output':str(path)})
# Separate slow panels have the speed label baked into every frame.
slow=[];native=[]
for i in range(8):
 im=Image.new('RGBA',(112,100),'#eee6d0');dd=ImageDraw.Draw(im);dd.fontmode='1'
 dd.text((2,0),'SLOW4x 400ms/frame',fill='#242330');dd.text((8,17),'REF',fill='#242330');dd.text((64,17),'HERO',fill='#242330')
 im.alpha_composite(ref[i],(8,32));im.alpha_composite(hero[i],(64,32));slow.append(im);im.save(ext/f'slow-native-{i:02}.png')
 im=Image.new('RGBA',(128,100),'#eee6d0');dd=ImageDraw.Draw(im);dd.fontmode='1';dd.text((4,0),'TRUE 32x64 / 100ms',fill='#242330');dd.rectangle((64,25,127,99),fill='#202631');im.alpha_composite(hero[i],(8,32));im.alpha_composite(hero[i],(72,32));native.append(im);im.save(ext/f'light-dark-native-{i:02}.png')
for frames,name,path,delay in [(slow,'source-hero-SLOW4x-native',ext/'source-hero-SLOW4x-native.gif',400),([im.resize((448,400),Image.Resampling.NEAREST) for im in slow],'source-hero-SLOW4x-4x',ext/'source-hero-SLOW4x-4x.gif',400),(native,'hero-light-dark-native',out/'hero-light-dark-native.gif',100)]:
 tmp=ext/(name+'.review-project.json');tmp.write_text(json.dumps(project(frames,name),separators=(',',':')));jobs.append({'project':str(tmp),'output':str(path),'delayMs':delay})
(ext/'gif-jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
# Compact anatomy/cluster critique: source / HR9 / this body pass, fixed crop.
p=Image.new('RGB',(810,600),'#eee6d0');dd=ImageDraw.Draw(p)
for row,i in enumerate((0,2,4)):
 before=Image.open(root/f'docs/reviews/M1-HR10-BODY/walk-{i:02}.png').convert('RGBA')
 for col,(label,im) in enumerate((('CONFIRMED SOURCE',ref[i]),('HR10 BEFORE',before),('HR11 STRUCTURAL CANDIDATE',hero[i]))):
  x=10+col*270;y=10+row*196;dd.text((x,y),label+f' / frame{i}',fill='#242330')
  crop=im.crop((0,44,32,64)).resize((256,160),Image.Resampling.NEAREST);p.paste(crop,(x,y+24),crop)
p.save(ext/'body-clusters-source-before-after.png')
print('Prepared all8/contact/cluster plates and seven lossless GIF jobs, including labelled slow4x and native light/dark.')
