from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
R=Path(__file__).resolve().parents[4];O=Path(__file__).parent
spec=[('Front Hero reference',R/'docs/reviews/M1-NCR1/south-idle/master-hero.png'),('Front neutral base',R/'docs/reviews/M1-NT1/south/neutral.png'),('West neutral base',R/'docs/reviews/M1-NT1/west/neutral.png')]
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12);title=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',19)
q=Image.new('RGB',(720,310),'#eee8d1');d=ImageDraw.Draw(q);d.text((22,17),'Body construction proposal',font=title,fill='#242330')
checks=[]
for k,(label,p) in enumerate(spec):
 a=Image.open(p).convert('RGBA');x=k*240;d.text((x+12,57),label,font=font,fill='#242330');b=a.resize((96,192),Image.Resampling.NEAREST);q.paste(b,(x+39,80),b);q.paste(a,(x+169,208),a)
 checks.append({'source':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'enlargement':3,'actualSize':[32,64]})
d.text((22,286),'3× enlargement + actual size · construction proposal, not finished art',font=font,fill='#465671');q.save(O/'body-construction-proposal.png');(O/'input-proof.json').write_text(json.dumps({'sourceCommit':'ef43a54f05d78ce448396415f799e7e664f217b4','artworkChanged':False,'inputs':checks},indent=2)+'\n')
