"""Snapshot currently saved candidate sides, without editing artists' files."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).parent; EXT=ROOT/'local-review/overnight-cast-qa'
jobs=[('Girl','M1-OGH1/west/idle.png','may-walking.png'),('Mom','M1-OM1/idle-west.png','mom.png'),('Nugget','M1-ON1/west-idle.png','prof_birch.png')]
board=Image.new('RGB',(1000,3*300),'#ccd7d1');d=ImageDraw.Draw(board);result=[]
def runs(p,y):
 xs=[x for x in range(p.width) if p.getpixel((x,y))[3]];rr=[]
 for x in xs:
  if rr and rr[-1][1]==x:rr[-1][1]=x+1
  else:rr.append([x,x+1])
 return rr
for row,(name,relative,refname) in enumerate(jobs):
 path=ROOT/'docs/reviews'/relative;p=Image.open(path).convert('RGBA');s=Image.open(EXT/refname);f=s.crop((32,0,48,32));m=Image.new('L',f.size);m.putdata([255 if v else 0 for v in f.get_flattened_data()]);f=f.convert('RGBA');f.putalpha(m);f=f.resize((32,64),Image.Resampling.NEAREST)
 entry={'name':name,'candidatePath':str(path.relative_to(ROOT)),'candidateSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'reference':refname,'referenceIndex':2,'comparison':'exact2x source, no individual fitting; visible lower alpha, not shoe anatomy','candidateRows':{},'referenceRows':{}}
 for y in range(54,64):
  entry['candidateRows'][y]=runs(p,y);entry['referenceRows'][y]=runs(f,y)
 for col,(label,q) in enumerate([('actual primary idle2 x2',f),('current original candidate',p)]):
  x=col*250;y=row*300;d.text((x+5,y+5),name+' '+label,fill='black');board.paste(q,(x+5,y+30),q);z=q.resize((128,256),Image.Resampling.NEAREST);board.paste(z,(x+60,y+30),z)
  crop=q.crop((0,52,32,64)).resize((256,96),Image.Resampling.NEAREST);board.paste(crop,(520+col*240,y+50),crop)
  d.text((520+col*240,y+155),'Rows52..63 / 8x / full canvasX',fill='black')
 result.append(entry)
board.save(EXT/'side-source-candidate-snapshot.png');(OUT/'side-snapshot.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps([{'name':r['name'],'sha':r['candidateSha256'],'rows':r['candidateRows']} for r in result]))
