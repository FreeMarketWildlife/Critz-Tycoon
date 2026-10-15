"""Independent saved-image audit; no writer builder imports or reruns."""
from pathlib import Path
from PIL import Image
import hashlib,json
root=Path(__file__).resolve().parents[4]
out=root/'docs/reviews/M1-SR2/independent-review'
sb=json.loads((root/'art/source/shared-template-restoration-r1/restoration.json').read_text())
checks=[];records=[]
def ck(name,value):
 checks.append({'name':name,'pass':bool(value)})
 assert value,name
def image(path):return Image.open(path).convert('RGBA')
def changes(a,b):return {(x,y) for y in range(64) for x in range(32) if a.getpixel((x,y))!=b.getpixel((x,y))}
def runs(q,y):
 rows=[]
 for x in range(32):
  if q.getpixel((x,y))[3]:
   if rows and rows[-1][1]==x:rows[-1][1]+=1
   else:rows.append([x,x+1])
 return rows
for dr in ['west','east']:
 for po in ['idle','A','P','C']:
  tag=f'{dr}-{po}';before=image(root/f'docs/reviews/M1-SR1/{tag}/trial-hero.png');base=image(root/f'docs/reviews/M1-SR1/{tag}/trial-template.png');p=root/f'docs/reviews/M1-SR2/{tag}';after=image(p/'final-hero.png');bald=image(p/'final-template.png');delta=changes(before,after)
  ck(tag+' native32x64',after.size==bald.size==(32,64))
  ck(tag+' all alpha exact',before.getchannel('A').tobytes()==after.getchannel('A').tobytes() and base.getchannel('A').tobytes()==bald.getchannel('A').tobytes())
  ck(tag+' all source ink exact',all(before.getpixel((x,y))==after.getpixel((x,y)) for y in range(64) for x in range(32) if before.getpixel((x,y))==(36,35,48,255)))
  ck(tag+' upper waist head hands and fixed pack exact',before.crop((0,0,32,55)).tobytes()==after.crop((0,0,32,55)).tobytes() and base.crop((0,0,32,55)).tobytes()==bald.crop((0,0,32,55)).tobytes())
  ck(tag+' selected palette retained',set(after.get_flattened_data())<=set(before.get_flattened_data()))
  ck(tag+' binary alpha',set(after.getchannel('A').get_flattened_data())=={0,255})
  ck(tag+' full frame and lower footprint bounds exact',after.getbbox()==before.getbbox() and after.crop((0,54,32,64)).getbbox()==before.crop((0,54,32,64)).getbbox())
  ck(tag+' every row occupancy exact',all(runs(before,y)==runs(after,y) for y in range(64)))
  last=max(y for y in range(64) if runs(before,y));ck(tag+' contact row RGBA exact',before.crop((0,last,32,64)).tobytes()==after.crop((0,last,32,64)).tobytes())
  ck(tag+' exact shared Hero bald lower body',after.crop((0,46,32,64)).tobytes()==bald.crop((0,46,32,64)).tobytes())
  ck(tag+' same Hero bald change sites and colors',delta==changes(base,bald) and all(before.getpixel(p)==base.getpixel(p) and after.getpixel(p)==bald.getpixel(p) for p in delta))
  comp=bald.copy();layer=root/f'docs/reviews/M1-SB1/{tag}'
  for pt in sb['poses'][dr][po]['hairHiddenScalpCutoutCells']:comp.putpixel(tuple(pt),(0,0,0,0))
  comp.alpha_composite(image(layer/'hair-dependent-shading.png'));comp.alpha_composite(image(layer/'original-hair.png'))
  ck(tag+' real separate hair shadow recomposition',comp.tobytes()==after.tobytes())
  records.append({'pose':tag,'rgbaChanges':len(delta),'sourceSHA256':hashlib.sha256((root/f'docs/reviews/M1-SR1/{tag}/trial-hero.png').read_bytes()).hexdigest(),'heroSHA256':hashlib.sha256((p/'final-hero.png').read_bytes()).hexdigest(),'templateSHA256':hashlib.sha256((p/'final-template.png').read_bytes()).hexdigest(),'contactRow':last,'contactSpansExclusiveEnd':runs(after,last),'changedCells':[{'xy':[x,y],'before':list(before.getpixel((x,y))),'after':list(after.getpixel((x,y)))} for x,y in sorted(delta,key=lambda a:(a[1],a[0]))]})
for po in ['idle','A','P','C']:
 w=image(root/f'docs/reviews/M1-SR2/west-{po}/final-hero.png');e=image(root/f'docs/reviews/M1-SR2/east-{po}/final-hero.png')
 ck(po+' exact saved East lower counterpart',w.transpose(Image.Transpose.FLIP_LEFT_RIGHT).crop((0,54,32,64)).tobytes()==e.crop((0,54,32,64)).tobytes())
result={'task':'M1.SR2','pass':True,'count':len(checks),'checks':checks,'poses':records,'appearanceAcceptance':False,'meaning':'Preservation facts only; actual native-scale material/depth review is recorded separately.'}
(out/'saved-pixel-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'pass':True,'checks':len(checks),'changes':{r['pose']:r['rgbaChanges'] for r in records}}))
