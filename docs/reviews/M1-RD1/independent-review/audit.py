from pathlib import Path
from PIL import Image
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[4];D=R/'docs/reviews/M1-RD1';candidate=D/sys.argv[1] if len(sys.argv)>1 else D/'front-dummy.png';n=Image.open(candidate).convert('RGBA')
p=Path('/Users/tanoshi/.codex/visualizations/2026/10/15/brendan-user-reference-original/01agijgmbz561.gif');g=Image.open(p);g.seek(2);crop=g.convert('RGBA').crop((0,0,128,192));f=crop.resize((32,48),Image.Resampling.NEAREST);assert f.resize((128,192),Image.Resampling.NEAREST).tobytes()==crop.tobytes();r=Image.new('RGBA',(32,64));r.alpha_composite(f,(0,16));checks=[]
def ck(name,v):assert v,name;checks.append(name)
ck('exact actual supplied fan-GIF SHA',hashlib.sha256(p.read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e');ck('native32x64/binary alpha',n.size==(32,64) and set(n.getchannel('A').get_flattened_data())=={0,255})
for y0 in [45,46]:ck('actual reference alpha'+str(y0)+'plus exact',n.crop((0,y0,32,64)).getchannel('A').tobytes()==r.crop((0,y0,32,64)).getchannel('A').tobytes())
ck('all338 reference occupied cells45plus retained',sum(n.getpixel((x,y))[3]>0 for y in range(45,64) for x in range(32))==338)
ck('source face/ears36through45 alpha exact',n.crop((0,36,32,46)).getchannel('A').tobytes()==r.crop((0,36,32,46)).getchannel('A').tobytes())
ck('registered source eye rectangles retained',all(n.getpixel((x,y))[3] and n.getpixel((x,y))[:3] in [(36,35,48),(0,0,0)] for y in range(38,42) for x in [12,13,18,19]))
ck('ground edge62/painted61',n.getbbox()[3]==62);ck('complete source shoe alpha58plus',n.crop((0,58,32,64)).getchannel('A').tobytes()==r.crop((0,58,32,64)).getchannel('A').tobytes())
for title,path,pin in [('NF1','docs/reviews/M1-NF1/front-neutral.png','24444dba660577201f3352fcec89a0bb1a315c5f'),('Hero','docs/reviews/M1-NCR1/south-idle/master-hero.png','ef43a54f05d78ce448396415f799e7e664f217b4'),('West','docs/reviews/M1-NT1/west/neutral.png','ef43a54f05d78ce448396415f799e7e664f217b4')]:ck(title+' frozen source bytes unchanged',(R/path).read_bytes()==subprocess.check_output(['git','show',pin+':'+path]))
c=json.loads((R/'art/source/reference-dummy-r1/construction.json').read_text());coverage=set();total=0
for name,rec in c['regions'].items():
 layer=Image.open(D/(name+'-region.png')).convert('RGBA');mask={(x,y) for y in range(64) for x in range(32) if layer.getpixel((x,y))[3]};declared=set(map(tuple,rec['cells']));ck(name+' actual named mask matches source record',mask==declared);total+=len(mask);coverage|=mask
ck('all named region memberships disjoint',total==len(coverage));ck('named region union exactly covers dummy',coverage=={(x,y) for y in range(64) for x in range(32) if n.getpixel((x,y))[3]})
assembled=Image.new('RGBA',(32,64))
for name in c['renderOrder']:assembled.alpha_composite(Image.open(D/(name+'-region.png')).convert('RGBA'))
ck('actual flat part/outline/eye layers exactly recompose dummy',assembled.tobytes()==n.tobytes())
ck('no source costume green/red/white graphics colors',not any(v[:3] in [(115,206,115),(74,148,82),(255,99,90),(197,66,66),(248,248,248),(222,230,239)] for v in n.get_flattened_data()))
ck('all source alpha changes confined above36',all(n.getpixel((x,y))[3]==r.getpixel((x,y))[3] for y in range(36,64) for x in range(32)))
report={'task':'M1.RD1','pass':True,'count':len(checks),'checks':checks,'candidate':str(candidate.relative_to(R)),'candidateSHA256':hashlib.sha256(candidate.read_bytes()).hexdigest(),'body45plusAlphaXor':sum(bool(n.getpixel((x,y))[3])!=bool(r.getpixel((x,y))[3]) for y in range(45,64) for x in range(32)),'face36through45AlphaXor':0,'bodyVisiblePixelCount45plus':338,'appearanceApproval':False};(D/'independent-review/saved-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
