"""M1.OGH1 original native idle candidates. Writes ONLY the two assigned folders.
Run using bundled Python/Pillow. No game, shared generator or Git mutations.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib

R = Path(__file__).resolve().parents[3]
S = Path(__file__).parent
O = R / 'docs/reviews/M1-OGH1'
O.mkdir(exist_ok=True)
P = dict(ink='#201008', skin='#a87038', light='#c48e4a', shade='#784820',
         hair='#30231d', hairMid='#493020', hairLight='#67462b',
         coral='#fa8078', coralShade='#c95662', cream='#f7edcc',
         blue='#184080', blueShade='#142e58', shoe='#80394e', shoeLight='#ad5264')

def blank(): return Image.new('RGBA', (32,64))
def rgba(k): return tuple(bytes.fromhex(P.get(k,k)[1:]))+(255,)
def points(im): return {(x,y) for y in range(64) for x in range(32) if im.getpixel((x,y))[3]}
def layer(mask, key):
    q=blank()
    for p in mask:q.putpixel(p,rgba(key))
    return q
def paint(q, xy, key):
    for p in xy:q.putpixel(p,rgba(key))
def rows(spec): return {(x,y) for y,a,b in spec for x in range(a,b)}
def boundary(mask):return {p for p in mask if any((p[0]+dx,p[1]+dy) not in mask for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)])}
def combine(ls):
    q=blank()
    for im in ls.values():q.alpha_composite(im)
    return q
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

rd=json.loads((R/'art/source/reference-dummy-r1/construction.json').read_text())
gh=json.loads((R/'art/source/hero-girl-r1/construction.json').read_text())
oldhead=Image.open(R/'docs/reviews/M1-GH1/head-layer.png').convert('RGBA')
headpoints=points(oldhead)
bodymask=set().union(*[{tuple(p) for p in v['cells']} for k,v in rd['regions'].items() if k not in ['head','ears']])
# Add original source row45 shoulder wings; RD1 central jaw is head owned.
bodymask|={(x,45) for x in range(7,25)}

def frontbody(back=False):
    # Color ownership is original wardrobe construction, NOT frozen RD1 labels.
    cloth=blank();hands=blank();legs=blank();shoes=blank()
    for x,y in bodymask:
        if y>=58:
            color='ink' if (x,y) in boundary(bodymask) else 'shoe'
            if y==59 and 9<=x<=22:color='shoeLight'
            if y==60 and ((8<=x<=13) or (18<=x<=23)):color='cream'
            shoes.putpixel((x,y),rgba(color))
        elif y>=55:
            legs.putpixel((x,y),rgba('ink' if (x,y) in boundary(bodymask) else 'blueShade' if x in (14,15,16,17) or y==57 else 'blue'))
        elif y>=49 and (x<=8 or x>=23):
            hands.putpixel((x,y),rgba('ink' if (x,y) in boundary(bodymask) else 'light' if y==49 else 'shade' if y==54 else 'skin'))
        else:
            color='ink' if (x,y) in boundary(bodymask) else 'coralShade' if x>=21 or y==54 else 'coral'
            if y in (48,51) and 10<=x<=21:color='cream'
            if y==47 and (x<=9 or x>=22) and (x,y) not in boundary(bodymask):color='cream'
            cloth.putpixel((x,y),rgba(color))
    # One native separator at each visible arm/body join, no stacked black rails.
    paint(cloth,[(9,y) for y in range(49,54)]+[(22,y) for y in range(49,54)],'ink')
    return {'shirt':cloth,'exposed-arms-hands':hands,'shorts':legs,'shoes':shoes}

def inheritedfront():
    hairmask={ (i%32,i//32) for i,v in enumerate(gh['hairMask']) if v }
    tiemask={ (i%32,i//32) for i,v in enumerate(gh['tieMask']) if v }
    eyemask={tuple(p) for p in gh['eyeCells']}
    earmask={tuple(p) for p in gh['earCells']}
    masks={'face':headpoints-hairmask-tiemask-eyemask-earmask,'ears':earmask,'hair':hairmask,'ties':tiemask,'eyes':eyemask}
    result={}
    for name,m in masks.items():
        q=blank()
        for p in m:q.putpixel(p,oldhead.getpixel(p))
        result[name]=q
    assert combine(result).tobytes()==oldhead.tobytes()
    return result

fronthead=inheritedfront()
south={**frontbody(),**fronthead}
# Back shares front body VOLUME, not face; rear hair is original proposal.
northhead={k:blank() for k in ['face','ears','hair','ties','eyes']}
earmask=points(fronthead['ears'])
northhead['ears']=fronthead['ears'].copy()
for x,y in headpoints-earmask:
    color='ink' if (x,y) in boundary(headpoints) else 'hair'
    if y<32 and x<15 and (x+y)%5!=0:color='hairMid'
    if 30<=y<=33 and 10<=x<=21:color='hairMid'
    if 33<=y<=35 and 13<=x<=18:color='hairLight'
    northhead['hair'].putpixel((x,y),rgba(color))
# Selected twin puffs/ties retain their actual authored contour; back surface inferred.
for p in points(fronthead['ties']):
    northhead['hair'].putpixel(p,(0,0,0,0));northhead['ties'].putpixel(p,oldhead.getpixel(p))
north={**frontbody(True),**northhead}

def profile():
    ls={k:blank() for k in ['far-arm','far-shoe','shirt','shorts','shoes','exposed-arms-hands','face','ears','hair','ties','eyes']}
    bm=rows([(45,12,22),(46,11,23),(47,10,24),(48,10,24),(49,10,24),(50,10,24),(51,10,24),(52,10,24),(53,10,23),(54,11,23),(55,12,23),(56,12,23),(57,12,23)])
    for x,y in bm:
        if y>=55: key='shorts';col='blueShade' if x>=20 else 'blue'
        else:key='shirt';col='coralShade' if x>=21 else 'cream' if y in (48,51) else 'coral'
        if (x,y) in boundary(bm):col='ink'
        ls[key].putpixel((x,y),rgba(col))
    # Far shoe is small because it is occluded, never a separately shrunken foot.
    far=rows([(57,10,16),(58,9,17),(59,9,17),(60,10,16)])
    ls['far-shoe']=layer(far,'shoe')
    paint(ls['far-shoe'],boundary(far),'ink')
    shoe=rows([(57,15,22),(58,11,23),(59,9,23),(60,9,22),(61,11,21)])
    ls['shoes']=layer(shoe,'shoe');paint(ls['shoes'],boundary(shoe),'ink')
    paint(ls['shoes'],[(x,59) for x in range(11,21)],'shoeLight')
    paint(ls['shoes'],[(x,60) for x in range(10,21)],'cream')
    # Rest arm descends from shoulder beside hip; cuff stays above brown palm.
    arm=rows([(47,17,22),(48,16,23),(49,16,23),(50,16,23),(51,16,23),(52,16,23),(53,17,23),(54,18,22)])
    ls['exposed-arms-hands']=layer(arm,'skin')
    paint(ls['exposed-arms-hands'],boundary(arm),'ink')
    paint(ls['exposed-arms-hands'],[(x,48) for x in range(17,22)],'cream')
    paint(ls['exposed-arms-hands'],[(x,49) for x in range(17,22)],'light')
    paint(ls['exposed-arms-hands'],[(x,53) for x in range(18,22)],'shade')
    hm=rows([(26,12,20),(27,10,22),(28,8,24),(29,7,25),(30,6,26),(31,5,27),(32,5,27),(33,5,27),(34,5,27),(35,5,27),(36,5,27),(37,5,27),(38,5,27),(39,5,26),(40,6,26),(41,7,25),(42,8,24),(43,9,23),(44,11,22),(45,13,20)])
    ls['face']=layer(hm,'skin');paint(ls['face'],boundary(hm),'ink')
    paint(ls['face'],[(x,y) for x,y in hm-boundary(hm) if x<11 and y<41],'light')
    paint(ls['face'],[(x,y) for x,y in hm-boundary(hm) if y>=43],'shade')
    # Back of head, crown and short front temple lock; no inferred hat contour.
    hair={(x,y) for x,y in hm if y<=33 or (x>=16 and y<=36) or (x>=23 and y<=42) or (x>=20 and y>=42)}
    # Original two puffs overlap in profile; near/far placement is provisional.
    farpuff=rows([(22,10,15),(23,8,17),(24,7,18),(25,7,18),(26,8,18),(27,9,17),(28,10,16)])
    nearpuff=rows([(21,20,24),(22,18,26),(23,17,27),(24,16,28),(25,16,28),(26,16,28),(27,17,28),(28,18,27),(29,19,26),(30,20,25)])
    hair |= farpuff|nearpuff|rows([(34,7,10),(35,7,10),(36,8,10),(37,8,10)])
    ls['hair']=layer(hair,'hair');paint(ls['hair'],boundary(hair),'ink')
    paint(ls['hair'],[(x,y) for x,y in hair-boundary(hair) if (y<28 and x<22) or (29<=y<=31 and x<18)],'hairMid')
    paint(ls['hair'],[(20,23),(21,23),(19,24),(20,24),(10,25),(11,25)],'hairLight')
    ls['ties']=layer({(19,30),(20,30),(20,31),(21,31)},'coral')
    ear=rows([(37,19,21),(38,18,22),(39,18,22),(40,18,22),(41,19,21)])
    ls['ears']=layer(ear,'skin');paint(ls['ears'],{(19,38),(20,38),(19,39)},'shade')
    paint(ls['ears'],{(18,38),(18,39),(18,40),(19,41),(20,41)},'ink')
    ls['eyes']=layer({(8,y) for y in range(38,42)}|{(9,y) for y in range(38,42)},'ink')
    return ls

west=profile()
# Same symmetric clothing/no bag; actual per-view lighting stays hand-owned.
east={k:im.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for k,im in west.items()}
directions={'south':south,'north':north,'west':west,'east':east}
manifest={'task':'M1.OGH1','state':'four idle candidates awaiting root visual review','appearanceApproval':False,
 'canvas':[32,64],'frameEdgeAnchor':[16,64],'directions':{},
 'sources':{str(p.relative_to(R)):digest(p) for p in [R/'docs/reviews/M1-C4/revision-11/girl-hero-concept.png',R/'docs/reviews/M1-C4/revision-11/user-girl-design-reference.png',R/'docs/reviews/M1-GH1/head-layer.png',R/'art/source/reference-dummy-r1/construction.json']},
 'referenceRevision':'731ad5bfd6e6f265508d0efcca0ba42f9dcf5881',
 'referenceInspection':'Actual local primary Brendan/Man1 native and integer sixfold strips; not emulator observation. Fan GIF front only. No reference pixels in candidate.',
 'proposals':['RD1 source-posed passing envelope adapted as still candidate, not observed idle','RD1 internal part segmentation not accepted','North rear hair and clothing material, West/East geometry and puff occlusion are original inferred proposals','East profile mirrors symmetric clothing/ear/face and proposed profile hair; not proof of asymmetric physical hair arrangement','Hidden skull, joints and garment boundaries are not source-recovered anatomy'],
 'pack':None,'noMouthNose':True,'runtimeChanged':False}
checks=[]
def ck(n,v): assert v,n;checks.append(n)
images={}
for dr,ls in directions.items():
    folder=O/dr;folder.mkdir(exist_ok=True)
    q=combine(ls);images[dr]=q;q.save(folder/'idle.png')
    pal=[None];colors={}
    def encode(im):
        arr=[]
        for px in im.get_flattened_data():
            if not px[3]:arr.append(0);continue
            c='#%02x%02x%02x'%px[:3]
            if c not in colors:colors[c]=len(pal);pal.append(c)
            arr.append(colors[c])
        return arr
    pixels=encode(q);layers=[]
    for name,im in ls.items():
        im.save(folder/(name+'.png'));layers.append({'id':name,'visible':True,'pixels':encode(im)})
    project={'format':'fmw-sprite','version':1,'name':'OGH1 Girl '+dr+' idle / UNAPPROVED','preset':'character','width':32,'height':64,'palette':pal,'bank':'custom','frames':[{'name':dr+' idle','ticks':8,'pixels':pixels}], 'notes':'Original review candidate only. Layered source lives in sibling layers JSON. No runtime adoption.'}
    (S/(dr+'.sprite.json')).write_text(json.dumps(project,separators=(',',':'))+'\n')
    (S/(dr+'.layers.json')).write_text(json.dumps({'canvas':[32,64],'palette':pal,'order':list(ls),'layers':layers},separators=(',',':'))+'\n')
    ck(dr+' native32x64/binary alpha',q.size==(32,64) and set(q.getchannel('A').get_flattened_data())<={0,255})
    ck(dr+' bottom two padding rows',not q.getchannel('A').crop((0,62,32,64)).getbbox())
    re=blank()
    for l in layers:
        im=blank();im.putdata([(0,0,0,0) if not i else tuple(bytes.fromhex(pal[i][1:]))+(255,) for i in l['pixels']]);re.alpha_composite(im)
    ck(dr+' actual saved semantic layers exactly recompose PNG',re.tobytes()==Image.open(folder/'idle.png').convert('RGBA').tobytes())
    seen=set();todo=[next(iter(points(q)))];mask=points(q)
    while todo:
        p=todo.pop()
        if p in seen:continue
        seen.add(p);todo.extend([(p[0]+dx,p[1]+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if (p[0]+dx,p[1]+dy) in mask-seen])
    ck(dr+' opaque silhouette orthogonally connected',seen==mask)
    manifest['directions'][dr]={'bounds':q.getbbox(),'opaqueCells':len(mask),'paletteColors':len(pal)-1,'layers':list(ls),'pngSHA256':digest(folder/'idle.png')}
ck('South identity head exact historical GH1',combine(fronthead).tobytes()==oldhead.tobytes())
rdpng=Image.open(R/'docs/reviews/M1-RD1/reference-derived-dummy.png').convert('RGBA')
ck('South RD1 envelope exact45plus',images['south'].getchannel('A').crop((0,45,32,64)).tobytes()==rdpng.getchannel('A').crop((0,45,32,64)).tobytes())
ck('North has no eye feature pixels',not north['eyes'].getbbox())
ck('all four saved PNGs distinct',len({q.tobytes() for q in images.values()})==4)
(S/'construction.json').write_text(json.dumps(manifest,indent=2)+'\n')
(O/'checks.json').write_text(json.dumps({'pass':True,'checks':checks,'count':len(checks),'appearanceApproval':False},indent=2)+'\n')
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
board=Image.new('RGB',(760,430),'#eee8d1');d=ImageDraw.Draw(board)
d.text((12,8),'M1.OGH1 | Girl Hero | FOUR IDLE CANDIDATES / UNAPPROVED',fill='#201008',font=font)
for i,(dr,q) in enumerate(images.items()):
    x=14+i*186
    d.text((x,33),dr.upper()+' / native +4x',fill='#201008',font=font)
    d.rectangle((x,55,x+149,320),fill='#d6dfd2')
    big=q.resize((128,256),Image.Resampling.NEAREST);board.paste(big,(x+10,59),big)
    board.paste(q,(x+12,333),q)
    d.rectangle((x+70,330,x+115,400),fill='#24343e');board.paste(q,(x+77,333),q)
d.text((12,410),'RD1 volume / original R11 identity | N/W/E inferred | no walk or game adoption',fill='#201008',font=font)
board.save(O/'four-idle-board.png')
native=Image.new('RGBA',(160,64))
for i,q in enumerate(images.values()):native.alpha_composite(q,(i*40,0))
native.save(O/'four-idle-native.png')
# Actual one-native-pixel review grid, coordinate Y rises bottom0 to top64.
grid=Image.new('RGB',(820,455),'#eee8d1');g=ImageDraw.Draw(grid)
for i,(dr,q) in enumerate(images.items()):
    x=34+i*200;y=40;k=6
    grid.paste(q.resize((192,384),Image.Resampling.NEAREST),(x,y),q.resize((192,384),Image.Resampling.NEAREST))
    for v in range(33):g.line((x+v*k,y,x+v*k,y+384),fill='#c6c3b0',width=1)
    for v in range(65):g.line((x,y+v*k,x+192,y+v*k),fill='#c6c3b0',width=1)
    for h in [0,10,20,30,40,50,60,64]:
        yy=y+(64-h)*k;g.line((x,yy,x+192,yy),fill='#83979e',width=1)
        if i==0:g.text((2,yy-5),str(h),font=font,fill='#201008')
    g.line((x+96,y,x+96,y+384),fill='#d54671',width=2);g.text((x,15),dr+' /6x x16 axis',font=font,fill='#201008')
grid.save(O/'four-idle-grid.png')
print('Built FOUR original layered idle candidates;',len(checks),'checks pass; awaiting actual root visual review')
