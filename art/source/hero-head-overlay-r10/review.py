"""Fixed-registration head overlays; reference-colored output stays external."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageColor
import json,hashlib,sys
root=Path(__file__).resolve().parents[3];out=root/'docs/reviews/M1-HR10-HEAD'
ext=Path(sys.argv[1]).resolve();assert root not in ext.parents
refs=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/brendan-user-reference-original')
assert hashlib.sha256((refs/'01agijgmbz561.gif').read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e'
bg='#eee6d0';ink='#242330'
plate=Image.new('RGB',(1050,600),bg);d=ImageDraw.Draw(plate)
report={'registration':'full32x64 frames, fixed14px source padding, no per-sprite fitting','region':[0,18,32,46],'approval':'awaiting user','poses':{}}
def overlay(ref,h):
 base=Image.new('RGBA',(32,64),bg);base.alpha_composite(ref)
 t=h.copy();t.putalpha(t.getchannel('A').point(lambda a:round(a*.5)))
 return Image.alpha_composite(base,t)
def sets(im):return {(x,y) for y in range(18,46) for x in range(32) if im.getpixel((x,y))[3]}
for row,idx in enumerate((0,2)):
 ref=Image.open(refs/f'registered-left-{idx:02}.png').convert('RGBA')
 old=Image.open(root/f'docs/reviews/M1-HR9/walk-{idx:02}.png').convert('RGBA')
 new=Image.open(out/f'walk-{idx:02}.png').convert('RGBA')
 y=16+row*285
 for col,(label,im) in enumerate((('SUPPLIED BRENDAN REDRAW',ref),('BEFORE',old),('REVISED',new),('BEFORE 50% OVERLAY',overlay(ref,old)),('REVISED 50% OVERLAY',overlay(ref,new)))):
  x=10+col*208;d.text((x,y),label,fill=ink)
  crop=im.crop((0,18,32,46)).resize((192,168),Image.Resampling.NEAREST)
  plate.paste(crop,(x,y+26),crop if crop.mode=='RGBA' else None)
  full=im.copy();plate.paste(full,(x+78,y+203),full)
 rr=sets(ref);oo=sets(old);nn=sets(new)
 report['poses'][str(idx)]={'beforeExtra':len(oo-rr),'beforeMissing':len(rr-oo),'afterExtra':len(nn-rr),'afterMissing':len(rr-nn),'rows':[{'y':y,'ref':sorted(x for x,yy in rr if yy==y),'before':sorted(x for x,yy in oo if yy==y),'after':sorted(x for x,yy in nn if yy==y)} for y in range(18,46)]}
d.text((10,583),'Same scale and registration. Cap versus hair is an intentional difference; overlap is diagnostic, not approval.',fill=ink)
plate.save(ext/'head-overlay-before-after.png')
# Original-only native light/dark and integer enlargement.
p=Image.new('RGB',(640,400),bg);pd=ImageDraw.Draw(p)
for col,(label,folder) in enumerate((('BEFORE HR9',root/'docs/reviews/M1-HR9'),('HEAD REVISION HR10H',out))):
 im=Image.open(folder/'idle-forward.png').convert('RGBA');x=20+col*320
 pd.text((x,10),label,fill=ink);big=im.resize((128,256),Image.Resampling.NEAREST);p.paste(big,(x+70,32),big)
 p.paste(im,(x+70,315),im);pd.rectangle((x+120,305,x+175,390),fill='#202631');p.paste(im,(x+130,315),im)
p.save(out/'head-before-after.png')
(out/'overlay-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
# Also show the pinned Emerald south-idle head; it is a different pose/source.
stockpath=Path('/Users/tanoshi/.codex/visualizations/2026/10/14/hero-hr5-reference/walking.png')
assert hashlib.sha256(stockpath.read_bytes()).hexdigest()=='f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
stock=Image.open(stockpath);s=stock.convert('RGBA');a=Image.new('L',stock.size);a.putdata([255 if n else 0 for n in stock.get_flattened_data()]);s.putalpha(a)
ref=s.crop((0,0,16,32)).resize((32,64),Image.Resampling.NEAREST)
old=Image.open(root/'docs/reviews/M1-HR9/idle-forward.png').convert('RGBA');new=Image.open(out/'idle-forward.png').convert('RGBA')
p=Image.new('RGB',(1050,290),bg);pd=ImageDraw.Draw(p)
for col,(label,im) in enumerate((('EMERALD PINNED SOUTH IDLE',ref),('BEFORE',old),('REVISED',new),('BEFORE 50% OVERLAY',overlay(ref,old)),('REVISED 50% OVERLAY',overlay(ref,new)))):
 x=10+col*208;pd.text((x,10),label,fill=ink);crop=im.crop((0,18,32,46)).resize((192,168),Image.Resampling.NEAREST);p.paste(crop,(x,36),crop)
 p.paste(im,(x+78,215),im)
p.save(ext/'emerald-head-overlay.png')
print(json.dumps({k:{kk:vv for kk,vv in v.items() if kk!='rows'} for k,v in report['poses'].items()}))
