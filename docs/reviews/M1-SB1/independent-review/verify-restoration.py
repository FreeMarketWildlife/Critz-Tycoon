"""Independent saved-file audit. Does not execute the restoration builder."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess
root=Path(__file__).resolve().parents[4];out=Path(__file__).parent;task=out.parent;checks=[];records=[];font=ImageFont.load_default()
meta=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text())['directions']
prior=json.loads((out/'archive-current-measurements.json').read_text())['poses']
def ck(s,v):
    assert v,s
    checks.append(s)
def read(p):return Image.open(p).convert('RGBA')
def pts(q):return {(x,y) for y in range(64) for x in range(32) if q.getpixel((x,y))[3]}
def runs(xs):
    o=[]
    for x in sorted(xs):
        if o and x==o[-1][1]:o[-1][1]=x+1
        else:o.append([x,x+1])
    return o
board=Image.new('RGB',(1024,1260),'#eee8d1');d=ImageDraw.Draw(board);d.fontmode='1'
d.text((8,4),'INTERNAL / restoration to verified preserve-front archive; exact earlier praise artifact unresolved',font=font,fill='#292634')
d.text((8,18),'Actual32x64,4x display + native thumbnails / unchanged frame origin0,0 and ground anchor16,64',font=font,fill='#292634')
d.text((8,32),'Body overlay: real hair/skin-shadow/scalp-cutout/pack excluded; green=identical visible source RGBA',font=font,fill='#292634')
nativeOverlay=Image.new('RGBA',(128,64));nativeDiff=Image.new('RGBA',(128,64))
for row,dr in enumerate(['south','north','west','east']):
    for po in ['idle','A','P','C']:
        tag=dr+'-'+po;folder=task/tag;sourcePath=root/f'docs/reviews/M1-PS1/hero-{tag}.png';s=read(sourcePath);b=read(folder/'restored-bald.png');h=read(folder/'original-hair.png');shade=read(folder/'hair-dependent-shading.png');cut=read(folder/'hair-scalp-cutout-mask.png');pack=read(folder/'source-visible-pack-mask.png');recomposed=read(folder/'recomposed-hero.png');appearance=pts(h)|pts(shade)|pts(cut)
        ck(tag+'native frames',all(q.size==(32,64) for q in [s,b,h,shade,cut,pack]))
        ck(tag+'binary alpha',all(set(q.getchannel('A').get_flattened_data())<={0,255} for q in [s,b,h,shade,cut,pack]))
        z=b.copy()
        for xy in pts(cut):z.putpixel(xy,(0,0,0,0))
        z.alpha_composite(shade);z.alpha_composite(h)
        ck(tag+'actual independent hair reconstruction',z.tobytes()==s.tobytes()==recomposed.tobytes())
        ck(tag+'all appearance exceptions confined above body',all(y<46 for x,y in appearance))
        ck(tag+'all waist hands legs shoe RGBA46onward exact',s.crop((0,46,32,64)).tobytes()==b.crop((0,46,32,64)).tobytes())
        outsideDiff=[(x,y) for y in range(64) for x in range(32) if (x,y) not in appearance and s.getpixel((x,y))!=b.getpixel((x,y))]
        ck(tag+'every pixel outside appearance exact',not outsideDiff)
        ck(tag+'bald geometry reuses BS2 without new body drawing',b.getchannel('A').tobytes()==read(root/f'docs/reviews/M1-BS2/{tag}/bald-template.png').getchannel('A').tobytes())
        ck(tag+'cutout removes only otherwise empty source sites',all(not s.getpixel(p)[3] for p in pts(cut)))
        features=meta[dr][po]['commonFeatureRegistration'];visible={}
        for name in ['eyes','ears','hands']:
            cells={tuple(p) for p in features[name]['cells']};actual=cells-appearance
            ck(tag+name+'source-visible pixels exact',all(s.getpixel(p)==b.getpixel(p) for p in actual));visible[name]=sorted(actual)
        last=s.getbbox()[3]-1;lastB=b.getbbox()[3]-1;sourceContact=runs([x for x in range(32) if s.getpixel((x,last))[3]]);baldContact=runs([x for x in range(32) if b.getpixel((x,lastB))[3]])
        ck(tag+'full actual contact spans equal',last==lastB and sourceContact==baldContact)
        observed=(pts(s)-appearance)-pts(pack)
        ck(tag+'actual visible body includes same full RGBA',all(s.getpixel(p)==b.getpixel(p) for p in observed))
        diff=Image.new('RGBA',(32,64));over=Image.new('RGBA',(32,64))
        for p in observed:diff.putpixel(p,(43,155,99,180));over.putpixel(p,s.getpixel(p)[:3]+(192,))
        a=next(x for x in prior if x['direction']==dr and x['pose']==po)['anchors'];eyeCells=visible['eyes'];eyeRows=sorted({p[1] for p in eyeCells});handRows=sorted({p[1] for p in visible['hands']})
        record={'direction':dr,'pose':po,'selectedSourceSHA256':hashlib.sha256(sourcePath.read_bytes()).hexdigest(),'restoredFileSHA256':hashlib.sha256((folder/'restored-bald.png').read_bytes()).hexdigest(),'outsideAppearanceRGBADifferences':len(outsideDiff),'observedBodyComparedCells':len(observed),'observedBodyRGBADifferences':0,'below46AllRGBADifferences':0,'eyeRows':eyeRows,'handRows':handRows,'sourceCrownIncludesHair':s.getbbox()[1],'baldScalpCrown':b.getbbox()[1],'sourceVisibleAnchors':a,'contactRow':last,'fullContactSpans':sourceContact,'registeredVisibleFeatures':{k:[list(p) for p in v] for k,v in visible.items()}}
        records.append(record)
        if po=='idle':
            nativeOverlay.paste(over,(32*row,0));nativeDiff.paste(diff,(32*row,0));y=52+300*row;current=read(root/f'docs/reviews/M1-DS{4 if dr in ["south","north"] else 5}/dummy-2x-{tag}.png')
            for col,(label,q) in enumerate([('ARCHIVE '+dr,s),('REJECTED DS '+dr,current),('RESTORED SHARED '+dr,b),('Actual shared-body overlay',diff)]):
                x=256*col;d.text((x+4,y),label,font=font,fill='#292634');big=q.resize((128,256),Image.Resampling.NEAREST);board.paste(big,(x+8,y+24),big);board.paste(q,(x+172,y+180),q)
                if col==2:
                    labels=[f'C scalp: {b.getbbox()[1]}',f'E: {eyeRows[0] if eyeRows else "hidden"}',f'J: {a["chin"]["heroRow"] if dr!="north" else "hidden"}',f'S: {a["shoulder"]["heroRow"]}',f'W: {a["waist"]["heroRow"]}',f'H: {handRows[0] if handRows else "hidden"}',f'F: {last}']
                    for i,t in enumerate(labels):d.text((x+148,y+38+14*i),t,font=font,fill='#292634')
                if col==3:d.text((x+4,y+282),'Visible body RGBA difference:0',font=font,fill='#292634')
for path in ['art/source/dummy-resolution-r4','art/source/dummy-resolution-r5','docs/reviews/M1-PS1','docs/reviews/M1-HR14','character-creator']:
    ck(path+'unchanged',subprocess.run(['git','diff','--quiet','HEAD','--',path],cwd=root).returncode==0)
board.save(out/'verified-source-current-restored-overlays-INTERNAL.png');nativeOverlay.save(out/'native32-restored-transparent-body-overlays-SNWE.png');nativeDiff.save(out/'native32-restored-transparent-body-matches-SNWE.png')
(out/'restoration-independent-checks.json').write_text(json.dumps({'pass':True,'count':len(checks),'sourceSelection':'Direct preserve-front lineage, not proven amazing-praise image','scope':'16 static poses; no acceptance or new animation','poses':records,'checks':checks},indent=2)+'\n');print(json.dumps({'checks':len(checks),'poses':len(records),'sourceRGBARecompositionDifferences':0,'allObservedBodyRGBADifferences':0}))
