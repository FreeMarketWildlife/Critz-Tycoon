"""Read-only comparison renderer; external primary pixels only in ignored output."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[3];O=R/'local-review/overnight-source-comparison';O.mkdir(parents=True,exist_ok=True)
PIN='5eff78649e7170a877b961ef0b3da13b81a16038'
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
small=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',10)
rows=[('Girl Hero','May','may-walking.png','M1-OGH2'),('Mom','Mom','mom.png','M1-OM2'),('Nugget','Birch','prof_birch.png','M1-ON2')]
ledger=json.loads((R/'docs/reviews/M1-OVQ1/reference-audit.json').read_text());pins={x['name']:x['sha256'] for x in ledger['files']}
B=Image.new('RGB',(880,1320),'#e6e4d8');D=ImageDraw.Draw(B)
D.text((16,12),'CURRENT IDLES vs ACTUAL EMERALD SOURCE ASSETS / NO SPRITE EDITS',font=font,fill='#172326')
D.text((16,32),'Raw source-asset palette, NOT game capture. Source16x32 -> exact2x32x64; no fitting.',font=small,fill='#263236')
D.text((16,48),'Candidate authored32x64. Color3x / silhouette2x. Red line below contact61; frame anchor16,64.',font=small,fill='#263236')
meta={'task':'M1.OVC1','referenceRevision':PIN,'method':'Actual primary source idle0South/1North/2West; index0 transparent, exact2x whole frame. Candidate native32x64; no fitting. Matching contact61/anchor16,64. Color display3x and silhouettes2x, integer nearest.','spriteEdits':False,'pairs':[]}
for ri,(name,refname,filename,task) in enumerate(rows):
 y=78+ri*398;D.text((16,y),f'{name} | actual {refname} source vs frozen {task} | silhouettes below',font=font,fill='#172326')
 path=R/'local-review/overnight-cast-qa'/filename;sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha==pins[refname]
 s=Image.open(path);assert s.mode=='P' and s.size==(144,32)
 for ci,(direction,index,label) in enumerate([('south',0,'FRONT'),('west',2,'WEST'),('north',1,'BACK')]):
  x=24+ci*282
  D.text((x,y+22),label,font=font,fill='#172326')
  src=s.crop((index*16,0,(index+1)*16,32));mask=Image.new('L',(16,32));mask.putdata([255 if z else 0 for z in src.get_flattened_data()]);src=src.convert('RGBA');src.putalpha(mask);norm=src.resize((32,64),Image.Resampling.NEAREST)
  cp=R/f'docs/reviews/{task}'/(f'{direction}/idle.png' if task=='M1-OGH2' else f'idle-{direction}.png' if task=='M1-OM2' else f'{direction}-idle.png');cand=Image.open(cp).convert('RGBA')
  for i,(im,kind) in enumerate([(norm,'REF 2x native'),(cand,'CURRENT native')]):
   px=x+i*132;D.text((px,y+41),kind,font=small,fill='#263236');D.rectangle((px,y+57,px+95,y+248),fill='#b9c8c4')
   z=im.resize((96,192),Image.Resampling.NEAREST);B.paste(z,(px,y+57),z);D.line((px,y+57+186,px+95,y+57+186),fill='#9a4444',width=1)
   sil=Image.new('RGBA',(32,64),'#22373b');sil.putalpha(im.getchannel('A'));sil=sil.resize((64,128),Image.Resampling.NEAREST);B.paste(sil,(px+16,y+258),sil);D.line((px+16,y+258+124,px+79,y+258+124),fill='#9a4444')
  assert max(q for q in range(64) if norm.getchannel('A').crop((0,q,32,q+1)).getbbox())==61
  assert max(q for q in range(64) if cand.getchannel('A').crop((0,q,32,q+1)).getbbox())==61
  meta['pairs'].append({'character':name,'reference':refname,'facing':direction,'index':index,'sourceSHA256':sha,'candidate':str(cp.relative_to(R)),'candidateSHA256':hashlib.sha256(cp.read_bytes()).hexdigest(),'referenceBoundsNormalized':norm.getbbox(),'candidateBounds':cand.getbbox(),'referenceLowerWidths58to61':[sum(norm.getpixel((xx,yy))[3]>0 for xx in range(32)) for yy in range(58,62)],'candidateLowerWidths58to61':[sum(cand.getpixel((xx,yy))[3]>0 for xx in range(32)) for yy in range(58,62)]})
meta['recommendations']={'Girl Hero':'Candidate-ready for a separate bounded walking decision; no shared perspective redraw proven.','Mom':'One material integration correction before walking: continuous inset blouse/cardigan plane rather than isolated outlined cream lobe; preserve torso/hand/shoe envelope and height. Original design proposal, not source anatomy proof.','Nugget':'Candidate-ready for separate bounded walking decision; no new idle blocker; motion untested.'}
D.text((16,1284),'Primary revision5eff78649e71 | no emulator capture | outfit/hair differ; no hidden-anatomy claim',font=small,fill='#263236')
D.text((16,1302),'Comparative pose/projection evidence only. Parent appearance/walking decision remains open.',font=small,fill='#263236')
B.save(O/'reference-candidate-idles.png');meta['board']={'path':str(O/'reference-candidate-idles.png'),'sha256':hashlib.sha256((O/'reference-candidate-idles.png').read_bytes()).hexdigest(),'dimensions':B.size}
(R/'docs/reviews/M1-OVC1/comparison.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta['board']))
