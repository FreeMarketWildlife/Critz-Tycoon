"""Read-only comparisons: preserved archive versus independently drawn DS study."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
root=Path(__file__).resolve().parents[4];out=Path(__file__).parent;out.mkdir(exist_ok=True)
dirs=['south','north','west','east'];poses=['idle','A','P','C'];font=ImageFont.load_default()
features=json.loads((root/'docs/reviews/M1-HR14/wrist-correction/before-construction.json').read_text())['directions']
skin={(128,80,61),(172,114,75),(209,150,98),(226,173,121)}
def image(p):return Image.open(p).convert('RGBA')
def mask(im):return {(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]}
def spans(xs):
    out=[]
    for x in sorted(xs):
        if out and x==out[-1][1]:out[-1][1]=x+1
        else:out.append([x,x+1])
    return out
def bounds(cells):return [min(x for x,y in cells),min(y for x,y in cells),max(x for x,y in cells)+1,max(y for x,y in cells)+1] if cells else None
def txt(d,xy,s):d.text(xy,s,font=font,fill='#292634')
def region(folder,name):return image(folder/f'region-{name}.png')
def pair(dr,po):
    heroPath=root/f'docs/reviews/M1-PS1/hero-{dr}-{po}.png';currentPath=root/f'docs/reviews/M1-DS{4 if dr in ["south","north"] else 5}/dummy-2x-{dr}-{po}.png'
    hero=image(heroPath);current=image(currentPath);folder=root/'docs/reviews/M1-CHT1';folder=folder if (dr,po)==('south','idle') else folder/f'{dr}-{po}'
    hair=image(folder/f'hair-{dr}-{po}.png');pack=region(folder,'pack');straps=region(folder,'straps')
    excluded=mask(hair)|mask(pack)|mask(straps);start=45 if dr=='north' and po!='P' else 44
    hm={(x,y) for x,y in mask(hero) if y>=start and (x,y) not in excluded};cm={(x,y) for x,y in mask(current) if y>=start and (x,y) not in excluded}
    h=hero.copy();c=current.copy()
    for y in range(64):
        for x in range(32):
            if (x,y) in excluded:h.putpixel((x,y),(0,0,0,0));c.putpixel((x,y),(0,0,0,0))
    # Transparent actual-RGBA superposition, fixed frame origin and no fitting.
    for im in [h,c]:im.putalpha(im.getchannel('A').point(lambda v:v//2))
    overlay=Image.alpha_composite(h,c)
    diff=Image.new('RGBA',(32,64))
    for pt in hm|cm:diff.putpixel(pt,(230,85,142,255) if pt in hm-cm else (48,185,220,255) if pt in cm-hm else (125,130,133,160))
    sourceFeature=mask(region(folder,'skin-face-features'));sourceHands={p for p in sourceFeature if p[1]>=46};sourceFace={p for p in sourceFeature if p[1]<46}
    currentHands={(x,y) for x,y in mask(current) if y>=44 and current.getpixel((x,y))[:3] in skin};currentFace={(x,y) for x,y in mask(current) if y<44 and current.getpixel((x,y))[:3] in skin}
    sourceEyes=features[dr][po].get('commonFeatureRegistration',{}).get('eyes',{}).get('cells',[])
    sourceEyes=[tuple(p) for p in sourceEyes if hero.getpixel(tuple(p))[:3]==(36,35,48)]
    # Only isolated source-registered eyes, not all dark head boundary pixels.
    eyeXs=[(8,9),(20,21)] if dr=='south' else [(12,13)] if dr=='west' else [(18,19)] if dr=='east' else []
    dy=-2 if po=='P' else 0;currentEyes=[(x,y+dy) for a,b in eyeXs for x in range(a,b+1) for y in range(34,38) if current.getpixel((x,y+dy))[:3]==(41,38,52)]
    shirt=mask(region(folder,'shirt'));shorts=mask(region(folder,'shorts'))
    currentShirt={(x,y) for x,y in mask(current) if y>=44 and current.getpixel((x,y))[:3] in [(232,117,96),(182,73,77),(247,227,184),(183,182,161)]}
    currentShorts={(x,y) for x,y in mask(current) if y>=44 and current.getpixel((x,y))[:3] in [(72,91,120),(45,58,85),(123,145,163)]}
    lastH=hero.getbbox()[3]-1;lastC=current.getbbox()[3]-1
    anchors={'crown':{'hero':[16,hero.getbbox()[1]],'dummy':[16,current.getbbox()[1]],'status':'Visible hair crown versus authored bald scalp; NOT a shared skull measurement'},'eyes':{'heroBounds':bounds(sourceEyes),'dummyBounds':bounds(currentEyes),'status':'Actual visible registered feature cells; north occluded'},'chin':{'heroRow':max(y for x,y in sourceFace) if dr!='north' else None,'dummyRow':max(y for x,y in currentFace) if dr!='north' else None,'status':'Lowest visible face-skin row, not hidden skeletal chin; North chin is occluded'},'shoulder':{'heroRow':min(y for x,y in shirt),'dummyRow':min(y for x,y in currentShirt),'status':'First visible shirt-material row, not a hidden shoulder joint'},'waist':{'heroRow':min(y for x,y in shorts),'dummyRow':min(y for x,y in currentShorts),'status':'First visible shorts-material row, not anatomical waist'},'hands':{'heroBounds':bounds(sourceHands),'dummyBounds':bounds(currentHands),'status':'Actual visible skin cells below face; no hidden arm bones'},'foot':{'heroRow':lastH,'dummyRow':lastC,'heroSpans':spans([x for x in range(32) if hero.getpixel((x,lastH))[3]]),'dummySpans':spans([x for x in range(32) if current.getpixel((x,lastC))[3]]),'edgeAnchor':[16,64],'status':'Lowest painted costume/contact, not measured anatomical feet'}}
    row={'direction':dr,'pose':po,'heroPath':str(heroPath.relative_to(root)),'dummyPath':str(currentPath.relative_to(root)),'frame':[32,64],'registration':'Same top-left0,0 and bottom-center16,64; no resampling or per-pose fitting','sourceSelection':'Explicit preserve-front archive lineage; separate amazing-praise artifact unresolved','heroSHA256':hashlib.sha256(heroPath.read_bytes()).hexdigest(),'dummySHA256':hashlib.sha256(currentPath.read_bytes()).hexdigest(),'comparisonBodyStartRow':start,'hairPackStrapExcludedCells':len(excluded),'sharedVisibleBodyAlphaXOR':len(hm^cm),'lower54plusAlphaXOR':sum(bool(hero.getpixel((x,y))[3])!=bool(current.getpixel((x,y))[3]) for y in range(54,64) for x in range(32)),'anchors':anchors}
    return hero,current,overlay,diff,row
records=[];board=Image.new('RGB',(960,1260),'#eee8d1');d=ImageDraw.Draw(board);d.fontmode='1'
txt(d,(8,4),'INTERNAL / preserved Hero archive vs current DS study /32x64 native,4x display / no approval claim')
txt(d,(8,18),'Same frame origin + baseline; real hair/pack/strap pixels excluded from shared-body alpha comparison.')
txt(d,(8,32),'Magenta=archive only; cyan=current only; gray=overlap. Lower masks cannot be excused by hair/backpack.')
nativeOverlay=Image.new('RGBA',(128,64));nativeDiff=Image.new('RGBA',(128,64))
for r,dr in enumerate(dirs):
    hero,current,overlay,diff,record=pair(dr,'idle');nativeOverlay.paste(overlay,(32*r,0));nativeDiff.paste(diff,(32*r,0));y=52+r*300
    for col,(title,im) in enumerate([('ARCHIVE PS1 '+dr,hero),('CURRENT DS '+dr,current),('50%+50% fixed overlay',overlay),('Shared-body alpha',diff)]):
        x=col*240;txt(d,(x+4,y),title);big=im.resize((128,256),Image.Resampling.NEAREST);board.paste(big,(x+8,y+24),big);board.paste(im,(x+156,y+180),im)
        if col in [0,1]:
            a=record['anchors'];kind='hero' if col==0 else 'dummy';lines=[('C',a['crown'][kind][1]),('E',(a['eyes'][kind+'Bounds'] or [0,0])[1]),('J',a['chin'][kind+'Row']),('S',a['shoulder'][kind+'Row']),('W',a['waist'][kind+'Row']),('H',(a['hands'][kind+'Bounds'] or [0,0])[1]),('F',a['foot'][kind+'Row'])]
            for i,(tag,row) in enumerate(lines):
                txt(d,(x+150,y+38+14*i),f'{tag}: y{row}' if row is not None and (tag!='E' or dr!='north') else f'{tag}: hidden')
        if col==3:txt(d,(x+4,y+282),f'Body XOR: {record["sharedVisibleBodyAlphaXOR"]} cells')
for dr in dirs:
    for po in poses:records.append(pair(dr,po)[4])
board.save(out/'archive-versus-current-anchors-INTERNAL.png');nativeOverlay.save(out/'native32-transparent-overlays-SNWE.png');nativeDiff.save(out/'native32-transparent-body-differences-SNWE.png')
# Show plausible historical praise candidates without selecting one as approved.
lineage=Image.new('RGB',(1000,340),'#eee8d1');dd=ImageDraw.Draw(lineage);dd.fontmode='1';txt(dd,(8,4),'PRAISE ARTIFACT UNRESOLVED / factual candidates + direct preserve-front archive; no guessed approval')
for i,(label,path) in enumerate([('HR9 source9d1d159',root/'docs/reviews/M1-HR9/idle-forward.png'),('HR10-BODY d158c3e',root/'docs/reviews/M1-HR10-BODY/idle-forward.png'),('Preserved HR14/PS1',root/'docs/reviews/M1-PS1/hero-south-idle.png'),('Current DS4 South',root/'docs/reviews/M1-DS4/dummy-2x-south-idle.png')]):
    q=image(path);x=i*250;txt(dd,(x+8,24),label);big=q.resize((128,256),Image.Resampling.NEAREST);lineage.paste(big,(x+8,52),big);lineage.paste(q,(x+164,240),q)
lineage.save(out/'south-archive-candidates-not-approval-INTERNAL.png')
(out/'archive-current-measurements.json').write_text(json.dumps({'scope':'Read-only comparison; current DS is independently authored, not shared Hero preservation','praisedArtifactIdentified':False,'preservationMessageId':'msg_01a13fcd-a1c7-70a3-a1e4-3ba83126fc35','preservedSouthSHA256':'f959249734d6c588e433bb84f1de9435820b738235d568d15c8cbf8964fdb4ae','anchorLegend':'C visible crown,E eyes,J lowest visible face skin,S shirt upper,W shorts upper,H hand skin bounds,F last painted contact; no hidden anatomy claims','poses':records},indent=2)+'\n')
print(json.dumps({'poses':len(records),'bodyAlphaXorRange':[min(r['sharedVisibleBodyAlphaXOR'] for r in records),max(r['sharedVisibleBodyAlphaXOR'] for r in records)],'lower54plusRange':[min(r['lower54plusAlphaXOR'] for r in records),max(r['lower54plusAlphaXOR'] for r in records)]}))
