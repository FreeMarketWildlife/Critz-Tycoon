"""BS2 all-direction clean scalp continuation; no shape or dressed changes."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-BS2';fm=root/'docs/reviews/M1-FM2';cht=root/'docs/reviews/M1-CHT1';ref=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text());checks=[];records={};images={}
SKIN={(166,104,69,255),(195,138,88,255),(116,69,57,255)};LIGHT=(195,138,88,255);MID=(166,104,69,255)
def check(n,v):assert v,n;checks.append(n)
def mask(im):return {(i%32,i//32) for i,q in enumerate(im.get_flattened_data()) if q[3]}
for dr in ['south','north','west','east']:
 records[dr]={};images[dr]={}
 for po in ['idle','A','P','C']:
  tag=f'{dr}-{po}';folder=out/tag;folder.mkdir(exist_ok=True);old=Image.open(fm/f'template-{tag}.png').convert('RGBA');hero=Image.open(fm/f'hero-{tag}.png').convert('RGBA');cf=cht if tag=='south-idle' else cht/tag;hair=Image.open(cf/f'hair-{tag}.png').convert('RGBA');new=old.copy();e=ref['directions'][dr][po]['commonFeatureRegistration'];protected={tuple(p) for name in ['eyes','ears'] for p in e[name]['cells']};dy=-2 if po=='P' else 0;changes=[]
  # A continuous forehead plane replaces the hairstyle-shaped light/dark seam.
  # Skin-only edits above eyes. One shaded cell follows the existing round
  # exterior at each side; there is no horizontal cap/fringe division.
  limit=(45 if dr=='north' else 38)+dy
  for y in range(27+dy,limit):
   skin=[x for x in range(32) if old.getpixel((x,y)) in SKIN]
   if not skin:continue
   left,right=min(skin),max(skin)
   for x in skin:
    if (x,y) in protected:continue
    color=MID if x in (left,right) else LIGHT
    if color!=old.getpixel((x,y)):
     new.putpixel((x,y),color);changes.append({'xy':[x,y],'before':'#%02x%02x%02x'%old.getpixel((x,y))[:3],'after':'#%02x%02x%02x'%color[:3]})
  # Optional hair owns its original exposed fringe/cast shading. This is a
  # sparse skin-shading attachment, not body-colored hair or full-Hero overlay.
  shade=Image.new('RGBA',(32,64));shadecells=[]
  for item in changes:
   pt=tuple(item['xy'])
   if not hair.getpixel(pt)[3] and hero.getpixel(pt)[3]:shade.putpixel(pt,hero.getpixel(pt));shadecells.append(item['xy'])
  attachment=Image.alpha_composite(shade,hair);dressed=new.copy();hidden=[]
  for pt in mask(new):
   if not hero.getpixel(pt)[3]:dressed.putpixel(pt,(0,0,0,0));hidden.append(list(pt))
  dressed.alpha_composite(attachment)
  changed={tuple(p['xy']) for p in changes}
  check(tag+' alpha/scalp silhouette exact',new.getchannel('A').tobytes()==old.getchannel('A').tobytes());check(tag+' eyes/ears exact',all(new.getpixel(p)==old.getpixel(p) for p in protected));check(tag+' below eyes/body/footprints exact',new.crop((0,limit,32,64)).tobytes()==old.crop((0,limit,32,64)).tobytes());check(tag+' changes only existing skin',all(old.getpixel(p) in SKIN and new.getpixel(p) in SKIN for p in changed));check(tag+' optional hair reproduces dressed Hero exactly',dressed.tobytes()==hero.tobytes());check(tag+' original hair artwork exact',all(attachment.getpixel(p)==hair.getpixel(p) for p in mask(hair)))
  for n,im in [('before-template',old),('bald-template',new),('hair-art',hair),('hair-dependent-shading',shade),('optional-hair-attachment',attachment),('dressed-exact',dressed)]:im.save(folder/(n+'.png'))
  if dr in ['south','west']:check(tag+' accepted BS1 exact',new.tobytes()==Image.open(root/f'docs/reviews/M1-BS1/{tag}/bald-template.png').convert('RGBA').tobytes())
  records[dr][po]={'frame':[32,64],'anchor':[16,64],'dy':dy,'changedSkinCells':changes,'hairDependentShadingCells':shadecells,'selectedHairHiddenScalpCells':hidden,'eyesEarsImmutable':[list(p) for p in sorted(protected)],'skinShadingEndRowExclusive':limit,'PM1Included':False,'sourceTemplateSHA256':hashlib.sha256((fm/f'template-{tag}.png').read_bytes()).hexdigest(),'sourceDressedSHA256':hashlib.sha256((fm/f'hero-{tag}.png').read_bytes()).hexdigest()};images[dr][po]=(old,new,dressed)
 # Head color edit registration is rigid across existing poses.
 base={(x,y):q for y in range(27,38) for x in range(32) if (q:=images[dr]['idle'][1].getpixel((x,y)))[3]}
 for po in ['A','P','C']:
  dy=-2 if po=='P' else 0;im=images[dr][po][1];check(dr+po+' rigid forehead registration',all(im.getpixel((x,y+dy))==q for (x,y),q in base.items()))
# Concise current four-direction sheet: native1x and integer4x, fixed canvases.
plate=Image.new('RGB',(920,330),'#efe9d6');d=ImageDraw.Draw(plate);d.fontmode='1';d.text((10,8),'BS2 / CURRENT CLEAN BALD TEMPLATES / NATIVE1x + NEAREST4x / FM2 OUTFIT, NO PM1',fill='#253340')
for col,dr in enumerate(['south','north','west','east']):
 x=col*230;d.text((x+10,30),dr.upper(),fill='#253340');im=images[dr]['idle'][1];plate.paste(im,(x+10,210),im);q=im.resize((128,256),Image.Resampling.NEAREST);plate.paste(q,(x+80,50),q);d.text((x+8,288),'1x',fill='#253340');d.text((x+125,310),'4x',fill='#253340')
plate.save(out/'four-direction-current-template.png')
# Existing eight slots, including repeated P and exact exported holds.
order=ref['order'];contact=Image.new('RGB',(1040,750),'#efe9d6');d=ImageDraw.Draw(contact);d.fontmode='1';d.text((8,5),'BS2 EXISTING WALK / 2x BALD + 1x DRESSED / ORIGINAL SLOTS AND HOLDS / NO PM1',fill='#253340')
for row,dr in enumerate(['south','north','west','east']):
 y=25+row*180;d.text((4,y+65),dr.upper(),fill='#253340');holds=[100]*8 if dr=='south' else [70,60,70,70,70,60,70,70]
 for slot,po in enumerate(order):
  x=75+slot*120;d.text((x,y+3),str(slot)+' '+po+' '+str(holds[slot])+'ms',fill='#253340');im=images[dr][po][1];q=im.resize((64,128),Image.Resampling.NEAREST);contact.paste(q,(x+38,y+19),q);im=images[dr][po][2];contact.paste(im,(x,y+83),im)
contact.save(out/'four-direction-existing-walk-contact.png')
# Original existing walk slots/holds, labelled normal and slow, no new poses.
order=ref['order']
for dr in ['south','north','west','east']:
 for slow in [False,True]:
  frames=[]
  for i,po in enumerate(order):
   c=Image.new('RGB',(144,100),'#bed4d5');d=ImageDraw.Draw(c);d.fontmode='1';d.text((2,2),dr+' '+str(i)+' '+po+(' SLOW' if slow else ''),fill='#253340')
   for j,im in enumerate(images[dr][po]):c.paste(im,(8+j*48,23),im)
   d.text((2,88),'BEFORE  BALD   DRESSED',fill='#253340');frames.append(c)
  durations=([100]*8 if dr=='south' else [70,60,70,70,70,60,70,70]);durations=[t*(4 if slow else 1) for t in durations]
  for scale in [1,4]:
   imgs=[im.resize((144*scale,100*scale),Image.Resampling.NEAREST) for im in frames];file=out/f'{dr}-existing-walk-{"slow" if slow else "normal"}-{scale}x.gif';imgs[0].save(file,save_all=True,append_images=imgs[1:],duration=durations,loop=0,optimize=False,disposal=2);g=Image.open(file);check(file.name+' eight original slots',g.n_frames==8 and g.info['loop']==0)
   for i,im in enumerate(imgs):g.seek(i);check(file.name+f' slot{i} exact pixels and holds',g.convert('RGB').tobytes()==im.tobytes() and g.info['duration']==durations[i])
(src/'changes.json').write_text(json.dumps({'task':'M1.BS2','state':'ALL FOUR DIRECTIONS EXISTING POSES; REVIEW PENDING; NO PM1','poses':records},indent=2)+'\n');(out/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'approval':False},indent=2)+'\n');print('PASS',len(checks),'saved shading/shape/feature/recomposition/existingGIF checks')
