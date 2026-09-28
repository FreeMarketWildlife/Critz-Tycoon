#!/usr/bin/env python3
"""Deterministic still-review plates assembled from the final character atlas.

No sprite art is drawn, recolored, filtered, or trimmed. Pillow only crops exact
RGBA frames and enlarges them at integer nearest-neighbor scale. Diagram guides
are painted before sprites, preserving every opaque source pixel.
"""
from pathlib import Path
import argparse, hashlib, json
from PIL import Image, ImageDraw, ImageFont, __version__ as PILLOW_VERSION

BG='#102a30'; CARD='#1d3b42'; BORDER='#315258'; TEXT='#f0ead7'; MUTED='#b3c8bd'
GOLD='#dfbc70'; HEAD='#7ec6b4'; BODY='#eca491'; STANCE='#aeb9e9'; FRAME='#95adb0'
FONTS={s:ImageFont.load_default(size=s) for s in (12,13,14,15,16,18,21,27,28)}
SHORT={
 'hero.boy':'Relaxed child','hero.girl':'Petite child','mom':'Soft round adult',
 'kaid':'Pitcher child','professor':'Sturdy broad adult','juniper':'Soft pear adult',
 'dr-fern':'Slim adult','mina':'Petite slim adult','ollie':'Broad compact adult',
 'aunt-ember':'Sturdy round adult','rival-mom':'Soft pear adult','rival-dad':'Broad short adult'}

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def ink(draw,x,y,label,size=14,color=TEXT,center=False):
 label=label.replace('\u2019',"'").replace('\u00b7','/')
 parts=label.split('\u00d7');font=FONTS[size]
 widths=[round(draw.textlength(p,font=font))for p in parts]
 cross=max(5,size//2-1);gap=2
 total=sum(widths)+(len(parts)-1)*(cross+2*gap)
 if center:x-=total//2
 for i,p in enumerate(parts):
  b=draw.textbbox((0,0),p or '0',font=font)
  draw.text((x,y-b[1]),p,font=font,fill=color);x+=widths[i]
  if i+1<len(parts):
   x+=gap;yy=y+max(1,(b[3]-b[1]-cross)//2)
   draw.line((x,yy,x+cross-1,yy+cross-1),fill=color)
   draw.line((x,yy+cross-1,x+cross-1,yy),fill=color)
   x+=cross+gap

def dashed(draw,box,color,width=1,dash=5):
 x0,y0,x1,y1=box
 for x in range(x0,x1,dash*2):
  draw.line((x,y0,min(x+dash-1,x1),y0),fill=color,width=width)
  draw.line((x,y1,min(x+dash-1,x1),y1),fill=color,width=width)
 for y in range(y0,y1,dash*2):
  draw.line((x0,y,x0,min(y+dash-1,y1)),fill=color,width=width)
  draw.line((x1,y,x1,min(y+dash-1,y1)),fill=color,width=width)

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--root',type=Path,default=Path.cwd())
 ap.add_argument('--out',type=Path,default=Path('docs/reviews/M1-C2'))
 args=ap.parse_args();out=args.out;out.mkdir(parents=True,exist_ok=True)
 folder=args.root/'assets/review/characters-v2';atlaspath=folder/'atlas.png';metapath=folder/'atlas.json'
 metadata=json.loads(metapath.read_text());atlas=Image.open(atlaspath).convert('RGBA')
 assets=metadata['assets'];assert len(assets)==12
 assert metadata['nativeFrame']==[24,32] and metadata['paintedBudget']==[20,26]
 assert metadata['animation'] is None
 crops={};native_checks=[]
 for a in assets:
  x,y,w,h=a['rect'];assert [w,h]==[24,32]
  crop=atlas.crop((x,y,x+w,y+h));individual=Image.open(folder/a['png']).convert('RGBA')
  assert crop.tobytes()==individual.tobytes(),a['id']
  assert set(p[3]for p in crop.get_flattened_data())=={0,255}
  crops[a['character']]=crop
  native_checks.append({'id':a['id'],'cropMatchesIndividualRgba':True,'rgbaSha256':hashlib.sha256(crop.tobytes()).hexdigest()})
 integrity=[]
 def sprite(target,a,left,top,scale,plate):
  source=crops[a['character']]
  target.alpha_composite(source.resize((24*scale,32*scale),Image.Resampling.NEAREST),(left,top))
  count=0
  for y in range(32):
   for x in range(24):
    pixel=source.getpixel((x,y))
    if pixel[3]:
     block=target.crop((left+x*scale,top+y*scale,left+(x+1)*scale,top+(y+1)*scale))
     assert set(block.get_flattened_data())=={pixel},(plate,a['id'],x,y)
     count+=1
  integrity.append({'plate':plate,'id':a['id'],'scale':scale,'verifiedOpaqueBlocks':count,'screenAnchor':[left+a['anchor'][0]*scale,top+a['anchor'][1]*scale]})
 # Contact sheet: four equal columns, three rows, same 4x native frame scale.
 contact=Image.new('RGBA',(720,748),BG);d=ImageDraw.Draw(contact);d.fontmode='1'
 ink(d,24,22,'Critz character study',28)
 ink(d,24,59,'20\u00d726 painted budget  /  12 original stills',15,MUTED)
 ink(d,669,28,'M1.C2',16,GOLD,True)
 for i,a in enumerate(assets):
  col,row=i%4,i//4;x=24+col*172;y=108+row*206;cx=x+78
  d.rounded_rectangle((x,y,x+155,y+189),radius=10,fill=CARD,outline=BORDER,width=1)
  ink(d,cx,y+12,a['label'],15,TEXT,True)
  # All storage frames share the baseline, regardless of head height.
  left=cx-48;top=y+26;baseline=top+128
  d.line((x+22,baseline+1,x+134,baseline+1),fill=BORDER)
  sprite(contact,a,left,top,4,'contact')
  ink(d,cx,y+168,SHORT[a['character']],12,MUTED,True)
 ink(d,360,720,'One south-facing still each  /  No animation  /  Awaiting art review',13,MUTED,True)
 contact.save(out/'character-still-contact-sheet.png',optimize=False)
 # Framework plate: real Hero, Mom, Nugget frames with guides outside the art.
 framework=Image.new('RGBA',(900,700),BG);d=ImageDraw.Draw(framework);d.fontmode='1'
 ink(d,24,24,'The 20\u00d726 chibi framework',27)
 ink(d,24,63,'Large heads, compact bodies and short connected stances.',15,MUTED)
 legend=[('Storage 24\u00d732',FRAME),('Ink limit 20\u00d726',GOLD),('Head',HEAD),('Body',BODY),('Short stance',STANCE)]
 lx=24
 for label,color in legend:
  d.rectangle((lx,99,lx+10,109),fill=color);ink(d,lx+18,98,label,13,MUTED)
  lx += {'Storage 24\u00d732':181,'Ink limit 20\u00d726':192,'Head':100,'Body':100,'Short stance':150}[label]
 byid={a['character']:a for a in assets}
 framework_assets=[byid[c]for c in ['hero.boy','mom','professor']]
 framework_checks=[]
 for i,a in enumerate(framework_assets):
  x=24+i*292;cx=x+134
  d.rounded_rectangle((x,135,x+267,585),radius=10,fill=CARD,outline=BORDER,width=1)
  ink(d,cx,150,a['label'],18,TEXT,True)
  s=8;left=x+24;top=188;right=left+24*s;bottom=top+32*s
  # Frame edges and maximum allowed painted bounds are exact edge coordinates.
  d.rectangle((left-1,top-1,right,bottom),outline=FRAME,width=1)
  dashed(d,(left+2*s-1,top+5*s-1,left+22*s,top+31*s),GOLD)
  design=a['design'];hb=design['headBounds'];bb=design['bodyBounds']
  assert hb[3]-hb[1]==design['headHeight'] and bb[3]-bb[1]==design['bodyHeight']
  assert hb[3]==bb[1],(a['id'],'head/body boundary')
  boundary=top+bb[1]*s
  d.line((left-8,boundary,right+8,boundary),fill=BODY,width=1)
  # Colored range bars sit wholly outside the 24x32 frame.
  bx=right+8
  d.rectangle((bx,top+hb[1]*s,bx+4,top+hb[3]*s-1),fill=HEAD)
  d.rectangle((bx,top+bb[1]*s,bx+4,top+bb[3]*s-1),fill=BODY)
  ink(d,bx+9,top+(hb[1]+hb[3])*s//2-5,str(design['headHeight']),12,HEAD)
  ink(d,bx+9,top+(bb[1]+bb[3])*s//2-5,str(design['bodyHeight']),12,BODY)
  # The bottom three rows describe the short stance, including hem where present.
  short_top=top+28*s;short_bottom=top+31*s
  d.line((left-11,short_top,left-11,short_bottom-1),fill=STANCE,width=2)
  d.line((left-11,short_top,left-5,short_top),fill=STANCE,width=2)
  d.line((left-11,short_bottom-1,left-5,short_bottom-1),fill=STANCE,width=2)
  # Anchor is outside the storage frame; it never paints over an original pixel.
  ax=left+a['anchor'][0]*s;ay=top+a['anchor'][1]*s
  d.polygon([(ax-4,ay+7),(ax+4,ay+7),(ax,ay+1)],fill=FRAME)
  sprite(framework,a,left,top,s,'framework')
  ink(d,cx,461,'Anchor (12,32)',13,MUTED,True)
  ink(d,cx,489,f"Head {design['headHeight']}px  /  Body {design['bodyHeight']}px",15,TEXT,True)
  ink(d,cx,518,f"Actual ink {a['visibleSize'][0]}\u00d7{a['visibleSize'][1]}",14,GOLD,True)
  ink(d,cx,547,'Short stance: bottom 3 rows',13,STANCE,True)
  framework_checks.append({'id':a['id'],'headBounds':hb,'bodyBounds':bb,'headBodyBoundaryRow':bb[1],
   'paintableRegionXyxy':[2,5,22,31],'storageXyxy':[0,0,24,32],'shortStanceRows':[28,30],
   'shortStanceNote':'Last 3 rows include any garment hem as well as legs and feet; not a measured anatomical limb length.'})
 ink(d,24,612,'Guides describe artwork. The existing 16\u00d716 gameplay cell remains separate.',14,MUTED)
 ink(d,24,639,'Ink stays within x2-21 and y5-30. Row31 is transparent; the anchor is the frame edge.',13,MUTED)
 ink(d,24,669,'Actual atlas pixels at 8\u00d7  /  No animation  /  Awaiting user art review',13,GOLD)
 framework.save(out/'character-framework-annotated.png',optimize=False)
 report={'atlasSha256':digest(atlaspath),'metadataSha256':digest(metapath),'pillowVersion':PILLOW_VERSION,
  'nativeCropCount':len(crops),'nativeRgbaUnchanged':True,'nativeChecks':native_checks,
  'contact':{'dimensions':[720,748],'layout':[4,3],'scale':4,'footAnchorRows':[262,468,674]},
  'framework':{'dimensions':[900,700],'scale':8,'annotations':framework_checks},
  'allOpaqueSpriteBlocksExact':True,'integrityChecks':integrity,
  'guidesPaintedBeforeSprites':True,'contactPngSha256':digest(out/'character-still-contact-sheet.png'),
  'frameworkPngSha256':digest(out/'character-framework-annotated.png'),
  'sourceAssetsMutated':False,'reviewStatus':'awaiting-user-art-review'}
 (out/'plate-validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (out/'alt-text.txt').write_text('Contact sheet: twelve original Critz characters in four columns and three rows: Hero boy, Hero girl, Mom, Kaid; Professor Nugget, Juniper, Dr. Fern, Mina; Ollie, Aunt Ember, Rival\'s mom, Rival\'s dad. Each has one south-facing idle pose at the same four-times pixel scale, a name and a short body-type label.\n\nFramework plate: actual Hero boy, Mom and Professor Nugget sprites at eight-times pixel scale. Outlines mark 24×32 storage and the 20×26 maximum painted area. External range bars mark head and body heights, a bracket marks the bottom three rows of the short stance, and a marker shows the bottom-center anchor. All original opaque sprite pixels remain unchanged.\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ['nativeChecks','integrityChecks']},indent=2))

if __name__=='__main__':main()
