"""Saved v1/v2 comparison independent of authoring operations."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
R=Path(__file__).resolve().parents[3];S=Path(__file__).parent;O=R/'docs/reviews/M1-OGH1'
checks=[];facts={}
def ck(n,v):assert v,n;checks.append(n)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
board=Image.new('RGB',(810,360),'#eee8d1');d=ImageDraw.Draw(board)
d.text((10,8),'OGH1 / v1 -> v2 / PROFILE PUFF ONLY /3x + actual native',font=font,fill='#201008')
for i,dr in enumerate(['south','north','west','east']):
    before=Image.open(O/'history-v1'/dr/'idle.png').convert('RGBA');after=Image.open(O/dr/'idle.png').convert('RGBA')
    x=12+i*200;d.text((x,35),dr.upper(),font=font,fill='#201008')
    for j,q in enumerate([before,after]):
        big=q.resize((96,192),Image.Resampling.NEAREST);board.paste(big,(x+j*98,55),big)
    d.text((x,258),'v1       v2',font=font,fill='#201008');board.paste(after,(x+10,285),after)
    d.rectangle((x+68,280,x+112,352),fill='#24343e');board.paste(after,(x+74,285),after)
    old=json.loads((O/'history-v1/source'/(dr+'.layers.json')).read_text());new=json.loads((S/(dr+'.layers.json')).read_text())
    def decode(layer,pal):return [(0,0,0,0) if not v else tuple(bytes.fromhex(pal[v][1:]))+(255,) for v in layer['pixels']]
    aa={l['id']:decode(l,old['palette']) for l in old['layers']};bb={l['id']:decode(l,new['palette']) for l in new['layers']}
    for name in aa:
        if name not in ('hair','ties'):ck(dr+' protected actual '+name+' layer exact v1',aa[name]==bb[name])
    ck(dr+' all body pixels45plus exact v1',before.crop((0,45,32,64)).tobytes()==after.crop((0,45,32,64)).tobytes())
    changes=[(x,y) for y in range(64) for x in range(32) if before.getpixel((x,y))!=after.getpixel((x,y))]
    if dr in ('south','north'):ck(dr+' entire saved PNG exact v1',before.tobytes()==after.tobytes())
    else:ck(dr+' final edits confined hair field21through34',all(21<=y<=34 for x,y in changes))
    facts[dr]={'changedRGBAFromV1':len(changes),'changedCells':changes,'pngSHA256':sha(O/dr/'idle.png')}
board.save(O/'v1-v2-profile-puff.png')
record={'task':'M1.OGH1','revision':'v2','state':'stable awaiting root visual review; no walks','pass':True,'count':len(checks),'checks':checks,'savedPixelFacts':facts,'boardSHA256':sha(O/'four-idle-board.png'),'boardPath':'docs/reviews/M1-OGH1/four-idle-board.png','appearanceApproval':False,'sourceFreezeCommit':None}
(O/'v2-freeze-checks.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'pass':True,'count':len(checks),'boardSHA256':record['boardSHA256'],'changedRGBAFromV1':{k:v['changedRGBAFromV1'] for k,v in facts.items()}}))
