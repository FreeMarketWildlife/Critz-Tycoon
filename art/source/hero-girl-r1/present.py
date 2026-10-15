"""Front-only still review; native sources and integer enlargements, no walk art."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-GH1';ext=Path(sys.argv[1]).resolve();ext.mkdir(parents=True,exist_ok=True);assert root not in ext.parents
meta=json.loads((src/'construction.json').read_text());girl=Image.open(out/'girl-front-idle.png').convert('RGBA');dummy=Image.open(out/'girl-front-construction.png').convert('RGBA');old=Image.open(root/'assets/review/idle-collection-v1/hero-girl.png').convert('RGBA');c7=Image.open(root/'assets/review/living-collection-v1/hero-girl/frame-1.png').convert('RGBA');boy=Image.open(root/'docs/reviews/M1-HR14/hero-south-idle.png').convert('RGBA');ink='#253340'
def bg(w,h,color='#bed4d5'):return Image.new('RGB',(w,h),color)
def put(canvas,im,x,y,scale=1):
 big=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST);canvas.paste(big,(x,y),big)
def anchor(d,x,y,scale):
 ax=x+16*scale;ay=y+64*scale;d.line((x,ay,x+32*scale,ay),fill='#748894');d.line((ax-4,ay,ax+4,ay),fill='#d84f5b');d.line((ax,ay,ax,ay+5),fill='#d84f5b')
p=bg(1440,560);d=ImageDraw.Draw(p)
concept=Image.open(root/'docs/reviews/M1-C4/revision-11/girl-hero-concept.png').convert('RGB');concept.thumbnail((220,440));p.paste(concept,(8,35));d.text((8,8),'SelectedR11 design preview',fill=ink);d.text((8,491),'887x1774 generated concept',fill=ink);d.text((8,509),'NOT a native measurement',fill=ink)
for n,(label,im) in enumerate([('C6 / exact C7front still',old),('GH1 Girl proposed idle',girl),('GH1 construction map',dummy),('HR14 sharedbody method',boy)]):
 x=240+n*300;d.text((x+5,8),label,fill=ink);put(p,im,x+86,35,4);anchor(d,x+86,35,4);put(p,im,x+134,323);anchor(d,x+134,323,1);d.text((x+5,407),'32x64 / frame edgeanchor16,64',fill=ink)
d.text((246,449),'C6/C7girl identity retained; body is DECLARED HR14visualadaptation, not girl-anatomy measurement.',fill=ink);d.text((246,473),'Onlyfrontidle. No existing runtime assets replaced. Newdirection/walk art held for root review.',fill=ink);d.text((246,497),'Oldskull annotation neck/collar45–46 excluded; originalface through44 +puffs/ties/fringe retained.',fill=ink)
p.save(ext/'front-identity-comparison.png')
# Actual native/nearest on contrasting backgrounds.
p=bg(1280,620);d=ImageDraw.Draw(p)
for n,(label,col) in enumerate([('LIGHT','#eee7d5'),('DARK','#263440'),('GRASS','#83a66c'),('PATH','#c6aa79')]):
 x=n*320;d.rectangle((x,0,x+319,619),fill=col);fg='#ffffff' if n==1 else ink;d.text((x+8,8),label+' / GIRL + CONSTRUCTION',fill=fg)
 for j,im in enumerate((girl,dummy)):put(p,im,x+10+j*155,38,4);anchor(d,x+10+j*155,38,4);put(p,im,x+58+j*155,333);anchor(d,x+58+j*155,333,1)
 d.text((x+8,425),'Actualpixels; no fitted/scaled head',fill=fg);d.text((x+8,447),'Burgundynear-solematerial restored',fill=fg);d.text((x+8,469),'No mouth / no added neck column',fill=fg)
p.save(out/'front-native-light-dark.png')
# Explicit masks. Inherited skull is authored scaffold, not hidden bone fact.
names=[('VISIBLE HEAD','headMask'),('HAIR MATERIAL','hairMask'),('PUFF REGIONS','puffMask'),('CORAL TIES','tieMask'),('C6 AUTHORED SCAFFOLD','inheritedSkullScaffoldMask'),('VISIBLE EARS','earCells'),('VISIBLE EYES','eyeCells'),('VISIBLE HANDS','handCells'),('BURGUNDY MATERIAL','burgundyMaterialCells'),('PALE BAND','paleBandCells')]
p=bg(1500,680);d=ImageDraw.Draw(p)
for n,(label,k) in enumerate(names):
 x=(n%5)*300;y=(n//5)*340;d.text((x+5,y+5),label,fill=ink);q=Image.new('RGBA',(32,64));value=meta[k];points=[(i%32,i//32) for i,b in enumerate(value) if b] if len(value)==2048 and isinstance(value[0],int) else [tuple(v) for v in value]
 for xx,yy in points:q.putpixel((xx,yy),(155,131,212,255) if k=='inheritedSkullScaffoldMask' else girl.getpixel((xx,yy)))
 put(p,q,x+86,y+25,4);anchor(d,x+86,y+25,4);d.text((x+5,y+299),'Authored/inferred; NOT bonefact' if k=='inheritedSkullScaffoldMask' else 'Actual rendered/native cell mask',fill=ink)
p.save(out/'front-feature-material-masks.png')
# Registered head/body overlap and original-to-current ear comparison.
p=bg(1120,440);d=ImageDraw.Draw(p)
for n,(label,im) in enumerate([('C6 head/ears context',old),('GH1 head/ears context',girl),('GH1 layers',dummy)]):
 x=n*370;d.text((x+5,5),label,fill=ink);put(p,im,x+56,25,5);anchor(d,x+56,25,5)
 d.text((x+5,379),'No wholehead mirror; hair/puff asymmetry retained.',fill=ink)
p.save(out/'front-head-ears-join.png')
# World-context mock, using existing32px ground textures. No live renderer/save.
p=bg(1280,690);d=ImageDraw.Draw(p)
for col,(name,asset) in enumerate([('PATH','ground-path.png'),('GRASS','ground-grass.png')]):
 scene=Image.new('RGBA',(192,144));tile=Image.open(root/'assets/review/contact-lab'/asset).convert('RGBA')
 for y in range(0,144,32):
  for x in range(0,192,32):scene.alpha_composite(tile,(x,y))
 scene.alpha_composite(girl,(48,48));scene.alpha_composite(boy,(112,48));x=col*640;d.text((x+8,7),name+' context / GIRL + HR14 at sameframeanchor',fill=ink);put(p,scene,x+32,36,3);put(p,scene,x+32,500,1);d.text((x+240,525),'Existingground texture; review mock only.',fill=ink);d.text((x+240,549),'Native below; nearest3x above.',fill=ink);d.text((x+240,573),'Not runtime integration or collision proof.',fill=ink)
p.save(out/'front-world-context.png');print('Frontcomparison, actualmasks, light/dark and mocked existinggroundcontext ready; no newdirection/walk.')
