"""NF1 front-only corrected construction. Clean masks first, then exact reflection."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[3];S=Path(__file__).parent;O=R/'docs/reviews/M1-NF1';O.mkdir(exist_ok=True);pin='ef43a54f05d78ce448396415f799e7e664f217b4';P={'outline':(36,35,48,255),'body':(116,136,148,255),'hand':(166,104,69,255),'pelvis':(70,86,113,255),'leg':(96,113,130,255)};checks=[]
def ck(n,v):assert v,n;checks.append(n)
def pts(q):return {(i%32,i//32) for i,p in enumerate(q.get_flattened_data()) if p[3]}
def edge(mask):return {p for p in mask if any((p[0]+dx,p[1]+dy) not in mask for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)])}
def mirror(mask):return mask|{(31-x,y) for x,y in mask}
def bounds(mask):return [min(x for x,y in mask),min(y for x,y in mask),max(x for x,y in mask)+1,max(y for x,y in mask)+1] if mask else None
def image(mask,color):
 q=Image.new('RGBA',(32,64))
 for p in mask:q.putpixel(p,color)
 return q
def save(q,name):q.save(O/name);return hashlib.sha256((O/name).read_bytes()).hexdigest()
source='docs/reviews/M1-NT1/south/neutral.png';old=Image.open(R/source).convert('RGBA');ck('NT1 input exact committed bytes',(R/source).read_bytes()==subprocess.check_output(['git','show',pin+':'+source]));west='docs/reviews/M1-NT1/west/neutral.png';protected='docs/reviews/M1-NCR1/south-idle/master-hero.png';protectedHash={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in [source,west,protected]}
for path,commit in [(west,pin),(protected,'0bb4ee4293ec2a76a3b8eb77d5d1fca4441bdcc1')]:ck(path+' exact protected committed input',(R/path).read_bytes()==subprocess.check_output(['git','show',commit+':'+path]))
head=old.copy()
for y in range(45,64):
 for x in range(32):head.putpixel((x,y),(0,0,0,0))
# Fresh simple shoulder slope under retained jaw: no pale separate cap/strap.
# These rows are corrected choices, not a mirrored old half.
body={(x,y) for y,a,b in [(45,10,22),(46,9,23),(47,8,24),(48,8,24),(49,9,23),(50,9,23),(51,9,23),(52,9,23),(53,9,23)] for x in range(a,b)}
armLeft={(x,y) for y,a,b in [(47,7,11),(48,6,11),(49,5,10),(50,4,10),(51,4,10),(52,5,10)] for x in range(a,b)};arm=mirror(armLeft)
# Full17-cell warm mass retained; compact lower rim now ends53, so it cannot
# recreate the rejected waist-row54 spikes. Construct, then reflect31-x.
handLeft={(x,y) for y,a,b in [(49,5,8),(50,4,9),(51,4,9),(52,4,8)] for x in range(a,b)};hand=mirror(handLeft);handEnvelope=hand|{(x+dx,y+dy) for x,y in hand for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]};handRim=handEnvelope-hand
# Correct actual pelvis/upper-leg width, not only the adjacent hand-rim pixels.
# Old material ran7..24; new waist/thigh runs9..22 (two cells each side removed).
pelvis={(x,54) for x in range(9,23)}|{(x,55) for x in range(8,24)};leg={(x,y) for y in [56,57] for x in range(7,25)}
q=Image.new('RGBA',(32,64));layers={};masks={'torso':body,'arms':arm,'hands':hand,'hand-rim':handRim,'pelvis':pelvis,'legs':leg}
for name,mask,color in [('torso',body,P['body']),('arms',arm,P['body']),('pelvis',pelvis,P['pelvis']),('legs',leg,P['leg']),('hand-rim',handEnvelope,P['outline']),('hands',hand,P['hand'])]:
 layers[name]=image(mask,color);q.alpha_composite(layers[name])
shoes=Image.new('RGBA',(32,64))
for y in range(58,64):
 for x in range(32):shoes.putpixel((x,y),old.getpixel((x,y)))
layers['shoes']=shoes;q.alpha_composite(shoes);q.alpha_composite(head);layers['head']=head
# One global border and short semantic inter-leg overlap, no shoulder straps.
outline=image(edge(pts(q)),P['outline'])
for x in [15,16]:outline.putpixel((x,57),P['outline'])
layers['outline']=outline;q.alpha_composite(outline)
# Preserve the exact accepted-scope neutral head/eyes/ears and shoes, including
# colors: only the rejected shoulders/arms/waist construction changes.
ck('head rows0..44 exact NT1 RGBA',q.crop((0,0,32,45)).tobytes()==old.crop((0,0,32,45)).tobytes());ck('full shoes58plus exact NT1 RGBA',q.crop((0,58,32,64)).tobytes()==old.crop((0,58,32,64)).tobytes())
order=list(layers);re=Image.new('RGBA',(32,64))
for name in order:re.alpha_composite(layers[name])
ck('actual flat region/outline layer exact recomposition',re.tobytes()==q.tobytes())
def asym(im,alpha=False):
 return [(x,y) for y in range(64) for x in range(16) if (bool(im.getpixel((x,y))[3])!=bool(im.getpixel((31-x,y))[3]) if alpha else im.getpixel((x,y))!=im.getpixel((31-x,y)))]
regions={}
for name,im in layers.items():
 ck(name+' reflected flat RGBA exact',not asym(im));ck(name+' reflected alpha/mask exact',not asym(im,True));regions[name]={'bounds':im.getbbox(),'RGBAReflectionMismatchedPairs':0,'alphaReflectionMismatchedPairs':0};save(im,name+'-region.png')
ck('whole neutral reflected RGBA exact',not asym(q));ck('whole neutral reflected alpha exact',not asym(q,True));ck('both warm hands17cells',[sum(q.getpixel((x,y))==P['hand'] for x,y in hand if (x<16)==left) for left in [True,False]]==[17,17]);ck('no old pale shoulder-pad material',all(p[:3]!=(191,192,170) for p in q.get_flattened_data()));ck('waist54 no flare beyond9..22',[x for x in range(32) if q.getpixel((x,54))[3]]==list(range(9,23)));ck('hand rim ends53 before waist',not any(y>=54 for x,y in handEnvelope));ck('all external border pixels charcoal',all(q.getpixel(p)==P['outline'] for p in edge(pts(q))));ck('last painted row61/frame32x64',q.size==(32,64) and q.getbbox()[3]-1==61)
seen=set();stack=[next(iter(pts(q)))];allpts=pts(q)
while stack:
 p=stack.pop()
 if p in seen:continue
 seen.add(p);stack.extend((p[0]+dx,p[1]+dy) for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)] if (p[0]+dx,p[1]+dy) in allpts and (p[0]+dx,p[1]+dy) not in seen)
ck('one connected silhouette',seen==allpts)
for p,h in protectedHash.items():ck(p+' immutable source SHA',hashlib.sha256((R/p).read_bytes()).hexdigest()==h)
newHash=save(q,'front-neutral.png');silhouette=image(pts(q),P['outline']);save(silhouette,'front-silhouette.png')
changes=[{'xy':[x,y],'before':list(old.getpixel((x,y))),'after':list(q.getpixel((x,y)))} for y in range(64) for x in range(32) if old.getpixel((x,y))!=q.getpixel((x,y))];rows={str(y):{'before':[x for x in range(32) if old.getpixel((x,y))[3]],'after':[x for x in range(32) if q.getpixel((x,y))[3]]} for y in range(45,58)}
F=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12);plate=Image.new('RGB',(1040,330),'#eee8d1');d=ImageDraw.Draw(plate)
hero=Image.open(R/protected).convert('RGBA')
for col,(title,im) in enumerate([('PROTECTED FRONT HERO',hero),('REJECTED NT1 NEUTRAL',old),('NF1 CORRECTED NEUTRAL',q),('CORRECTED SILHOUETTE',silhouette)]):
 x=260*col;d.text((x+5,6),title,font=F,fill=P['outline']);big=im.resize((96,192),Image.Resampling.NEAREST);plate.paste(big,(x+12,35),big);plate.paste(im,(x+170,135),im)
d.text((8,260),'NF1 front idle32x64 / actual native +3x / corrected shoulders, hand-rim/waist construction THEN mirrored',font=F,fill=P['outline']);d.text((8,282),'Whole image AND every flat layer:0 RGBA/mask reflection mismatches / shoes+head/source Hero/West unchanged',font=F,fill='#465671');plate.save(O/'corrected-front-comparison.png')
(S/'construction.json').write_text(json.dumps({'task':'M1.NF1','beforeSourceCommit':pin,'protectedSources':protectedHash,'centerline':{'edgeX':16,'pixelCenterX':15.5,'reflection':'31-x'},'constructionChoicesBeforeReflection':'fresh connected shoulder slope; no separate pale cap; corrected waist54 x9..22/55 x8..23, full lower legs/shoes and compact full17cell hands/rim ending53; then reflected clean regions','renderOrder':order,'regions':regions,'changes':changes,'rowEvidence':rows,'handWarmCellsEach':17,'handWarmBoundsLeft':bounds(handLeft),'handEnvelopeBoundsLeft':bounds({p for p in handEnvelope if p[0]<16}),'frontOutputSHA256':newHash,'appearanceApproval':False},indent=2)+'\n');(S/'symmetry.json').write_text(json.dumps({'before':{'alphaMismatchedPairs':asym(old,True),'RGBAMismatchedPairs':asym(old)},'after':{'alphaMismatchedPairs':asym(q,True),'RGBAMismatchedPairs':asym(q)},'regions':regions},indent=2)+'\n');(S/'checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'checks':checks,'appearanceApproval':False},indent=2)+'\n');print('Built corrected front only; before/after RGBA pair mismatches',len(asym(old)),len(asym(q)),'changedRGBAcells',len(changes),'checks',len(checks))
