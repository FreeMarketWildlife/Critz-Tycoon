"""Common visible-feature registration, no anatomy or sprite pixel changes."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[3];src=Path(__file__).parent;out=root/'docs/reviews/M1-HR14';p=src/'construction.json';meta=json.loads(p.read_text());directions=('south','north','west','east');report={'task':'M1.HR14 common feature/registration supplement','changesCharacterPixels':False,'edgeAnchor':[16,64],'anatomicalLimit':'All hidden hip/knee/ankle/anatomical-foot attachments unresolved/null; visible costume contour is not measured bone anatomy','directions':{}}
def points(im,predicate):return [[i%32,i//32] for i,px in enumerate(im.get_flattened_data()) if px[3] and predicate(px)]
def spans(xs):
 result=[]
 for x in sorted(xs):
  if result and result[-1][1]==x:result[-1][1]=x+1
  else:result.append([x,x+1])
 return result
for d in directions:
 report['directions'][d]={}
 for po in ('idle','A','P','C'):
  h=Image.open(out/f'hero-{d}-{po}.png').convert('RGBA');m=Image.open(out/f'dummy-{d}-{po}.png').convert('RGBA');e=meta['directions'][d][po];bottom=h.getbbox()[3]-1;ss=spans([x for x in range(32) if h.getpixel((x,bottom))[3]])
  features={'head':{'status':'visible authored template mask','mask':e['headMaskDummy']},'ears':{'status':'visible authored ears; profile far ear occluded','cells':points(m,lambda px:px[:3]==(237,140,205))},'eyes':{'status':'occluded back view' if d=='north' else 'visible aligned authored eyes','cells':[]},'arms':{'status':'visible original upper sleeve/limb contours; hidden shoulder/elbow attachments not source measured','hiddenShoulderJoint':None,'hiddenElbowJoint':None},'hands':{'status':'visible original upper hand sites, not inferred from lower costume','cells':points(m,lambda px:px[:3]==(255,212,161))},'torso':{'status':'authored upper-body projection; pack registration anchor is not a bone','packRegistrationAnchor':e['torsoAnchor']},'feet':{'status':'SOURCE-VISIBLE LOWER-COSTUME PLANES; lowest painted contour/contact candidates, not hidden foot anatomy','lastPaintedRow':bottom,'lastPaintedSpans':ss,'edgeAnchor':[16,64],'anatomicalFootAttachment':None},'legs':{'status':'Occluded/inferred under SOURCE-VISIBLE LOWER-COSTUME PLANES; anatomical lengths/joints UNRESOLVED; no added visible length','anatomicalCoordinates':None},'hiddenAttachments':{k:{'status':'UNRESOLVED / occluded; no source bone measurement','xy':None} for k in ('hip','knee','ankle','anatomicalFoot')}}
  # Eye mask is authored Critz feature evidence, not source inferred anatomy.
  old=json.loads((root/'art/source/hero-redesign-r6/masks.json').read_text())[d].get('eyes',[0]*2048);dy=-2 if po=='P' else 0
  features['eyes']['cells']=[[i%32,i//32+dy] for i,on in enumerate(old) if on and 0<=i//32+dy<64 and e['headMaskDummy'][(i//32+dy)*32+i%32]]
  e['commonFeatureRegistration']=features;report['directions'][d][po]={'lastPaintedRow':bottom,'lastPaintedSpans':ss,'edgeAnchor':[16,64],'hiddenAttachments':features['hiddenAttachments'],'visibleEyeCount':len(features['eyes']['cells']),'visibleHandCount':len(features['hands']['cells']),'heroPixelSHA256':hashlib.sha256(h.tobytes()).hexdigest(),'dummyPixelSHA256':hashlib.sha256(m.tobytes()).hexdigest()}
p.write_text(json.dumps(meta,separators=(',',':'))+'\n');(out/'common-feature-registration.json').write_text(json.dumps(report,indent=2)+'\n')
plate=Image.new('RGB',(1600,920),'#bed4d5');dd=ImageDraw.Draw(plate);ink='#253340'
for col,d in enumerate(directions):
 x=col*400;dd.text((x+8,8),d.upper()+' / COMMON VISIBLE FEATURES',fill=ink);dd.text((x+8,25),'SOURCE-VISIBLE LOWER-COSTUME PLANES',fill=ink)
 po='idle';m=Image.open(out/f'dummy-{d}-{po}.png').convert('RGBA');big=m.resize((192,384),Image.Resampling.NEAREST);plate.paste(big,(x+104,45),big);f=meta['directions'][d][po]['commonFeatureRegistration']
 def label(text,cells,tx,ty):
  dd.text((x+tx,ty),text,fill=ink)
  if cells:
   px,py=cells[len(cells)//2];dd.line((x+104+px*6+3,45+py*6+3,x+tx+(0 if tx>200 else 65),ty+5),fill=ink)
 head=[(i%32,i//32) for i,on in enumerate(f['head']['mask']) if on];label('head',head,8,192);label('ears',f['ears']['cells'],310,238);label('eyes hidden' if d=='north' else 'eyes',f['eyes']['cells'],8,268);label('arms/hands',f['hands']['cells'],302,349);label('torso',[[16,49]],8,346)
 b=f['feet']['lastPaintedRow'];ss=f['feet']['lastPaintedSpans'];label('feet/contact*',[[ss[-1][0],b]],302,425)
 # Explicit invariant full-frame edge anchor is distinct from painted contact.
 dd.line((x+104,429,x+296,429),fill='#748894');dd.line((x+200,425,x+200,435),fill='#ed745c');dd.text((x+8,452),'Frame edge anchor(16,64); red marker',fill=ink)
 dd.text((x+8,474),'*Lowest costume contour; bones unresolved',fill=ink)
 dd.text((x+8,496),'Hidden hip/knee/ankle/foot joint: NULL',fill=ink)
 dd.text((x+8,518),'Legs: occluded/inferred under costume',fill=ink)
 for row,pose in enumerate(('A','P','C')):
  y=554+row*112;h=Image.open(out/f'hero-{d}-{pose}.png').convert('RGBA');thumb=h.resize((48,96),Image.Resampling.NEAREST);plate.paste(thumb,(x+12,y),thumb);v=report['directions'][d][pose]
  dd.text((x+73,y+11),pose+' last painted row '+str(v['lastPaintedRow']),fill=ink);dd.text((x+73,y+31),'Observed spans '+str(v['lastPaintedSpans']),fill=ink);dd.text((x+73,y+51),'Coordinates are half-open x ranges.',fill=ink);dd.text((x+73,y+71),'Contact candidates; NOT ankle/bone sites.',fill=ink)
plate.save(out/'four-direction-common-feature-registration.png')
print('Added visible common features/contact spans and explicitNULLhidden joints; NO sprite pixels changed.')
