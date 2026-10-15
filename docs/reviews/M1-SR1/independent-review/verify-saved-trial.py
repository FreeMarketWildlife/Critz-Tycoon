from pathlib import Path
from PIL import Image
import json,hashlib
root=Path(__file__).resolve().parents[4]
review=root/'docs/reviews/M1-SR1'; data=json.loads((root/'art/source/side-curve-refinement-r1/changes.json').read_text()); sb=json.loads((root/'art/source/shared-template-restoration-r1/restoration.json').read_text());checks=[];summary=[]
def check(name,value):
 checks.append({'name':name,'pass':bool(value)})
 assert value,name
def im(p):return Image.open(p).convert('RGBA')
def diff(a,b):return {(x,y) for y in range(64) for x in range(32) if a.getpixel((x,y))!=b.getpixel((x,y))}
def spans(q,y):
 r=[]
 for x in range(32):
  if q.getpixel((x,y))[3]:
   if r and r[-1][1]==x:r[-1][1]=x+1
   else:r.append([x,x+1])
 return r
for direction,poses in data['poses'].items():
 for pose,record in poses.items():
  label=direction+' '+pose;folder=review/(direction+'-'+pose); before=im(folder/'before-hero.png'); after=im(folder/'trial-hero.png'); base=im(folder/'before-template.png'); trial=im(folder/'trial-template.png'); source=im(root/f'docs/reviews/M1-PS1/hero-{direction}-{pose}.png');expected={tuple(c['xy']) for c in record['changedCells']}; actual=diff(before,after)
  check(label+' actual source baseline',before.tobytes()==source.tobytes())
  check(label+' native32x64',all(q.size==(32,64) for q in [before,after,base,trial]))
  check(label+' exact recorded change sites',actual==expected)
  check(label+' exact recorded before after colors',all(list(before.getpixel(tuple(c['xy'])))==c['before'] and list(after.getpixel(tuple(c['xy'])))==c['after'] for c in record['changedCells']))
  check(label+' only55 through57 edited',all(55<=y<=57 for x,y in actual))
  check(label+' same template delta',diff(base,trial)==actual and all(trial.getpixel(p)==after.getpixel(p) and base.getpixel(p)==before.getpixel(p) for p in actual))
  check(label+' upper head hands waist exact',before.crop((0,0,32,55)).tobytes()==after.crop((0,0,32,55)).tobytes())
  check(label+' full shoe region58plus exact',before.crop((0,58,32,64)).tobytes()==after.crop((0,58,32,64)).tobytes())
  check(label+' bounds unchanged',before.getbbox()==after.getbbox() and before.crop((0,54,32,64)).getbbox()==after.crop((0,54,32,64)).getbbox())
  alpha={(x,y) for x,y in actual if before.getpixel((x,y))[3]!=after.getpixel((x,y))[3]}
  check(label+' exact two declared alpha changes',alpha=={tuple(c['xy']) for c in record['alphaChanges']} and len(alpha)==2)
  check(label+' recorded row runs match saved PNG',all(spans(before,int(y))==r['before'] and spans(after,int(y))==r['after'] for y,r in record['contourRuns'].items()))
  check(label+' palette subset',set(after.get_flattened_data())<=set(before.get_flattened_data()))
  check(label+' binary alpha',set(after.getchannel('A').get_flattened_data())=={0,255})
  contact=max(y for y in range(64) if spans(before,y));check(label+' last occupied contact exact',contact==record['contactRow'] and spans(before,contact)==spans(after,contact)==record['contactSpans'])
  composed=trial.copy();layerdir=root/f'docs/reviews/M1-SB1/{direction}-{pose}'
  for p in sb['poses'][direction][pose]['hairHiddenScalpCutoutCells']:composed.putpixel(tuple(p),(0,0,0,0))
  composed.alpha_composite(im(layerdir/'hair-dependent-shading.png'));composed.alpha_composite(im(layerdir/'original-hair.png'));check(label+' actual separate hair recomposition',composed.tobytes()==after.tobytes())
  mask=im(folder/'actual-changed-rgba-mask.png');check(label+' actual delta mask sites', {(x,y) for y in range(64) for x in range(32) if mask.getpixel((x,y))[3]}==actual)
  summary.append({'pose':label,'rgbaChanges':len(actual),'alphaChanges':len(alpha),'alphaSites':sorted(alpha),'contactRow':contact,'contactSpans':spans(after,contact)})
for pose in data['poses']['west']:
 a=im(review/('west-'+pose)/'trial-hero.png').crop((0,54,32,64));b=im(review/('east-'+pose)/'trial-hero.png').crop((0,54,32,64));check(pose+' saved lower East mirror',a.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()==b.tobytes())
result={'task':'M1.SR1','pass':True,'count':len(checks),'method':'Independent saved PNG audit; no builder import or rerun. End-exclusive horizontal runs.','checks':checks,'poses':summary,'visualAcceptance':False,'remainingConcern':'Modest curve improvement; broad dark lower mass remains. Exact praised historical artifact unresolved.'}
(review/'independent-review/saved-pixel-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'pass':True,'count':len(checks),'poses':summary}))
