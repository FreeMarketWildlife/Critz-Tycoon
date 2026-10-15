"""Original-only review goes in repo; source/combined pixels stay external."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR9';ext=Path(sys.argv[1]).resolve();assert ext!=root and root not in ext.parents
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
(ext/'gif-jobs.json').write_text(json.dumps(jobs,indent=2)+'\n');print('Prepared four lossless8-frame GIF jobs and source-versus-Hero all-frame contact.')
