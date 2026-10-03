"""Render editable native sources and integer grids. Optional references stay external."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,sys,math
ROOT=Path(__file__).resolve().parent
EXTERNAL=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else None
REPO=ROOT.parents[3]
if EXTERNAL:assert not EXTERNAL.is_relative_to(REPO)
NAMES=[('a-afro','A · Rounded afro','Teal shirt / cream sleeves'),('b-flat-top','B · Flat-top','Gold vest / cream shirt'),('c-twists','C · Short twists','Red stripes / navy shorts'),('d-cornrows','D · Cornrows','Blue jacket / olive shorts')]
def font(n,bold=False):return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial'+(' Bold' if bold else '')+'.ttf',n)
def render(m):
 im=Image.new('RGBA',(32,64))
 for y,row in enumerate(m['rows']):
  for x,k in enumerate(row):
   if k!='.':im.putpixel((x,y),tuple(bytes.fromhex(m['palette'][k][1:]))+(255,))
 return im
models=[]
for slug,title,subtitle in NAMES:
 m=json.loads((ROOT/f'{slug}.json').read_text());m.update(title=title,subtitle=subtitle)
 im=render(m);im.save(ROOT/f'{slug}.png');models.append(m)

def panel(plate,m,x,y,z=12,reference_overlay=False):
 d=ImageDraw.Draw(plate);w=32*z;h=64*z
 d.text((x+w/2,y-61),m['title'],font=font(21,True),fill='#253438',anchor='mm')
 d.text((x+w/2,y-35),m['subtitle'],font=font(16),fill='#253438',anchor='mm')
 d.rectangle((x,y,x+w,y+h),fill='#edf0eb')
 native=render(m)
 if reference_overlay and EXTERNAL:
  ref=render(reference).resize((w,h),Image.Resampling.NEAREST)
  ref.putalpha(ref.getchannel('A').point(lambda a:round(a*.25)));plate.paste(ref,(x,y),ref)
  # The actual supplied design is positioned with the same uniform transform as the native trace.
  cut=Image.open(EXTERNAL/(m['slug']+'-reference-cutout.png')).convert('RGBA')
  t=m['registration'];crop=t['sourceCrop'];origin=t['sourceFrameOrigin'];scale=t['sourcePixelsPerNativePixel']
  registered=cut.transform((w,h),Image.Transform.AFFINE,(scale/z,0,origin[0]-crop[0],0,scale/z,origin[1]-crop[1]),resample=Image.Resampling.NEAREST)
  plate.paste(registered,(x,y),registered)
 else:
  zoom=native.resize((w,h),Image.Resampling.NEAREST);plate.paste(zoom,(x,y),zoom)
 overlay=Image.new('RGBA',plate.size);g=ImageDraw.Draw(overlay)
 for col in range(33):g.line((x+col*z,y,x+col*z,y+h),fill=(70,94,99,49),width=1)
 for row in range(65):
  value=64-row;yy=y+row*z;major=value%10==0 or value==64
  g.line((x,yy,x+w,yy),fill=(62,101,120,190) if major else (70,94,99,49),width=2 if major else 1)
  if major:d.text((x-10,yy),str(value),font=font(16),fill='#253438',anchor='rm')
 g.line((x+w/2,y-5,x+w/2,y+h+5),fill=(196,57,118,255),width=2)
 if reference_overlay:
  for row in [40,46,62]:g.line((x,y+row*z,x+w,y+row*z),fill=(169,83,25,185),width=1)
 plate=Image.alpha_composite(plate.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(plate)
 for col in [0,10,16,20,30,32]:d.text((x+col*z,y+h+18),str(col),font=font(13),fill='#253438',anchor='mm')
 d.text((x+w/2,y+h+47),'32 × 64 · 0 at bottom · symmetry x=16',font=font(15),fill='#253438',anchor='mm')
 return plate

def sheet(models,name,destination,cols=None,overlay=False):
 cols=cols or len(models);rows=math.ceil(len(models)/cols);W=cols*446+35;H=170+rows*915
 plate=Image.new('RGB',(W,H),'#faf7ef');d=ImageDraw.Draw(plate)
 heading='REFERENCE ALIGNMENT · WHOLE FIGURES, UNIFORM SCALE' if overlay else 'BRENDAN + FOUR REFERENCE-TRACED DESIGNS' if len(models)==5 else 'FOUR REFERENCE-TRACED HERO DESIGNS'
 d.text((42,26),heading,font=font(27,True),fill='#253438')
 subtitle='Actual references over a faint Brendan guide. Brown lines: eyes, neck, feet.' if overlay else 'One square = one native pixel. Full 32×64 canvases. Pink: centerline. Blue: every 10 pixels.'
 d.text((42,69),subtitle,font=font(19),fill='#253438')
 entries=[]
 for i,m in enumerate(models):
  x=48+(i%cols)*446;y=176+(i//cols)*915
  plate=panel(plate,m,x,y,reference_overlay=overlay and i>0);entries.append({'slug':m['slug'],'x':x,'y':y,'scale':12})
 plate.save(destination/(name+'.png'));return entries
layouts={}
layouts['four-heroes-grid']=sheet(models,'four-heroes-grid',ROOT)
layouts['four-heroes-grid-2x2']=sheet(models,'four-heroes-grid-2x2',ROOT,2)
for m in models:
 im=Image.new('RGB',(480,995),'#faf7ef');im=panel(im,m,48,102);im.save(ROOT/(m['slug']+'-grid.png'))
# Both intended-density (1×) and integer enlargement are saved for visual inspection.
clean=Image.new('RGB',(1040,480),'#faf7ef');d=ImageDraw.Draw(clean)
d.text((24,20),'NATIVE + 6× INSPECTION',font=font(23,True),fill='#253438')
for i,m in enumerate(models):
 im=render(m);d.text((30+255*i,70),m['title'],font=font(18),fill='#253438')
 clean.paste(im,(112+255*i,90),im);zoom=im.resize((192,384),Image.Resampling.NEAREST);clean.paste(zoom,(32+255*i,80),zoom)
clean.save(ROOT/'native-and-clean-check.png')
if EXTERNAL:
 reference=json.loads((EXTERNAL/'brendan-reference.json').read_text());reference.update(slug='brendan',title='BRENDAN · REFERENCE',subtitle='Your supplied pixel reconstruction')
 layouts['five-character-grid']=sheet([reference]+models,'five-character-grid',EXTERNAL)
 sheet([reference]+models,'reference-registration',EXTERNAL,overlay=True)
 (EXTERNAL/'five-character-native.png').parent.mkdir(exist_ok=True,parents=True)
 native_line=Image.new('RGBA',(32*5,64))
 for i,m in enumerate([reference]+models):native_line.paste(render(m),(32*i,0))
 native_line.save(EXTERNAL/'five-character-native.png')
(ROOT/'grid-layout.json').write_text(json.dumps(layouts,indent=2)+'\n')
print('Rendered four native sources, full grids, clean/native view, and optional five-grid reference alignment.')
