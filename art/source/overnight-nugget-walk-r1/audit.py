"""Independent saved-layer, registered source-shape, contact and GIF audit."""
from pathlib import Path
from PIL import Image
import hashlib,json
S=Path(__file__).resolve().parent;R=S.parents[2];O=R/'docs/reviews/M1-ON3'
I=R/'art/source/overnight-nugget-continuation-r1'; P=R/'docs/reviews/M1-ON2'
assert S==R/'art/source/overnight-nugget-walk-r1'
checks=[];details={};D=['south','north','west','east']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(n,v):
    assert v,n
    checks.append(n)
def image(p):return Image.open(p).convert('RGBA')
def compose(ls):
    q=Image.new('RGBA',(32,64))
    for im in ls.values():q.alpha_composite(im)
    return q
def normalized(im):
    return im.crop(im.getbbox())
def count(im):return sum(bool(p[3]) for p in im.get_flattened_data())
def rgbaeq(a,b):
    return a.size==b.size and all(x==y if x[3] or y[3] else True for x,y in zip(a.get_flattened_data(),b.get_flattened_data()))
guard=json.loads((S/'input-guard.json').read_text())
for p,h in guard['protectedON2'].items():ck('protected ON2 exact '+p,sha(R/p)==h)
manifest=json.loads((S/'manifest.json').read_text())
ck('ordinary source8tick holds',manifest['holdTicks']==[8,8,8,8])
ck('exact hardware tick',manifest['sourceTickSeconds']==280896/16777216)
ck('four slots source order',manifest['sourceFrames']=={'south':[3,0,4,0],'north':[5,1,6,1],'west':[7,2,8,2],'east':[7,2,8,2]})
ck('fixed canvas and anchor',manifest['frame']==[32,64] and manifest['anchor']==[16,64])
atlas=image(O/'walk-atlas.png');ck('native atlas dimensions',atlas.size==(128,256))
allposes={}
for row,dr in enumerate(D):
    idle=image(P/f'{dr}-idle.png');allposes[dr]={};details[dr]={}
    idle_src=json.loads((I/f'{dr}.layers.json').read_text())
    for pose in ['A','idle','B']:
        src=json.loads((S/dr/f'{pose}.layers.json').read_text());q=image(O/f'{dr}-{pose}.png');allposes[dr][pose]=q;layers={}
        ck(dr+pose+' frame anchor',src['frame']==[32,64] and src['anchor']==[16,64])
        for n in src['renderOrder']:
            im=image(S/dr/pose/f'{n}.png');cells=Image.new('RGBA',(32,64))
            coords=[(x,y) for x,y,*c in src['layers'][n]['pixels']]
            ck(dr+pose+n+' unique authored cells',len(coords)==len(set(coords)))
            ck(dr+pose+n+' registered native frame',im.size==(32,64) and all(0<=x<32 and 0<=y<64 for x,y in coords))
            for x,y,*c in src['layers'][n]['pixels']:cells.putpixel((x,y),tuple(c))
            ck(dr+pose+n+' cell JSON equals saved layer',rgbaeq(im,cells));layers[n]=im
        ck(dr+pose+' saved layers exact final RGBA',rgbaeq(compose(layers),q))
        ck(dr+pose+' binary alpha',set(q.getchannel('A').get_flattened_data())<={0,255})
        coords={(x,y) for y in range(64) for x in range(32) if q.getpixel((x,y))[3]};remaining=set(coords);components=[]
        while remaining:
            todo=[remaining.pop()];size=1
            while todo:
                x,y=todo.pop()
                for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if p in remaining:remaining.remove(p);todo.append(p);size+=1
            components.append(size)
        ck(dr+pose+' one connected visible figure',len(components)==1)
        last=q.getbbox()[3]-1;contact=sorted(x for x,y in coords if y==last)
        ck(dr+pose+' painted contact61idle63stride',last==(61 if pose=='idle' else 63))
        details[dr][pose]={'bounds':q.getbbox(),'contactRow':last,'contactXs':contact,'components':components,'sha256':sha(O/f'{dr}-{pose}.png')}
        if pose=='idle':
            ck(dr+' exact frozen ON2 idle PNG bytes',sha(O/f'{dr}-idle.png')==sha(P/f'{dr}-idle.png'))
            ck(dr+' exact frozen ON2 semantic idle source',src['layers']==idle_src['layers'] and src['renderOrder']==idle_src['renderOrder'])
        else:
            # Head, hat, hair, eyes and glasses are actual saved source rasters
            # translated rigidly2Y. No deformation/phase-dependent recoloring.
            for n in idle_src['renderOrder']:
                if n in layers and n in ['head','face','face-light','face-shadow','ears','glasses','eyes','hair-fringe','hat','hat-band','hat-brim','hat-light','hair-light','ear','hair','hair-shadow']:
                    source=image(I/dr/f'{n}.png');expect=Image.new('RGBA',(32,64));expect.alpha_composite(source,(0,2))
                    ck(dr+pose+n+' rigid source raster +2Y no sway',rgbaeq(layers[n],expect))
            if dr in ['south','north']:
                for side,left in [('left',True),('right',False)]:
                    source=Image.new('RGBA',(32,64))
                    for y in range(58,64):
                        for x in range(32):
                            if (x<16)==left:source.putpixel((x,y),idle.getpixel((x,y)))
                    shoe=layers[side+'-shoe'];ck(dr+pose+side+' full shoe normalized RGBA exact',rgbaeq(normalized(shoe),normalized(source)))
            else:
                base=compose({n:image(I/dr/f'{n}.png') for n in ['near-shoe','shoe-highlight']})
                ck(dr+pose+' full near shoe normalized RGBA exact',rgbaeq(normalized(layers['near-shoe']),normalized(base)))
                ck(dr+pose+' full hidden far shoe completion retains volume',count(layers['far-shoe'])==count(base))
                ck(dr+pose+' full far shoe contour unchanged no scaling', normalized(layers['far-shoe']).getchannel('A').tobytes()==normalized(base).getchannel('A').tobytes())
                owners={}
                for n,im in layers.items():
                    for y in range(64):
                        for x in range(32):
                            if im.getpixel((x,y))[3]:owners[x,y]=n
                ck(dr+pose+' far upper gray actually survives final occlusion',any(n=='far-shoe' and q.getpixel(p)[:3]==(96,105,106) for p,n in owners.items()))
    # Actual front/side final contact changes screen side in the primary order.
    a=details[dr]['A']['contactXs'];b=details[dr]['B']['contactXs']
    ck(dr+' planted contact alternates screen side', (sum(a)/len(a)<16 and sum(b)/len(b)>15) if dr!='east' else (sum(a)/len(a)>15 and sum(b)/len(b)<16))
    for col,pose in enumerate(['A','idle','B','idle']):ck(dr+str(col)+' atlas slot exact',rgbaeq(atlas.crop((col*32,row*64,col*32+32,row*64+64)),allposes[dr][pose]))
for pose in ['A','idle','B']:ck('East '+pose+' explicit West reflection',rgbaeq(allposes['east'][pose],allposes['west'][pose].transpose(Image.Transpose.FLIP_LEFT_RIGHT)))
for speed,holds in [('normal',[130,140,130,140]),('slow4x',[540,530,540,530])]:
    for dr in D:
        for scale in [1,4]:
            p=O/f'{dr}-{speed}-{scale}x.gif';g=Image.open(p);ck(p.name+' four decoded frames',g.n_frames==4)
            for j,pose in enumerate(['A','idle','B','idle']):
                g.seek(j);expect=allposes[dr][pose].resize((32*scale,64*scale),Image.Resampling.NEAREST)
                ck(p.name+str(j)+' exact decoded RGBA no trails',rgbaeq(g.convert('RGBA'),expect))
                ck(p.name+str(j)+' cumulative-rounded duration',g.info['duration']==holds[j])
    p=O/f'four-directions-{speed}.gif';g=Image.open(p);ck(p.name+' four decoded paired frames',g.n_frames==4)
    for j in range(4):
        g.seek(j);ck(p.name+str(j)+' paired board decoded exact',rgbaeq(g.convert('RGBA'),image(O/f'four-directions-slot{j}.png')))
        ck(p.name+str(j)+' rounded hold',g.info['duration']==holds[j])
history=json.loads((S/'history-v0'/'checks.json').read_text())
for dr in D:
    for pose in ['A','idle','B']:
        old=O/'history-v0'/f'{dr}-{pose}.png';current=O/f'{dr}-{pose}.png'
        ck(dr+pose+' initial PNG history matches pre-correction audit',sha(old)==history['contactsAndBounds'][dr][pose]['sha256'])
        if dr in ['south','north'] or pose=='idle':
            ck(dr+pose+' protected PNG byte-exact initial history',sha(current)==sha(old))
        for p in (S/dr/pose).glob('*.png'):
            if pose=='idle' or dr in ['south','north'] or p.stem not in ['far-shoe','far-leg']:
                ck(dr+pose+p.stem+' protected source layer byte-exact initial history',sha(p)==sha(S/'history-v0'/dr/pose/p.name))
        if dr in ['west','east'] and pose!='idle':
            before=image(old);after=image(current)
            ck(dr+pose+' no upper body pixel changed',rgbaeq(before.crop((0,0,32,54)),after.crop((0,0,32,54))))
            ck(dr+pose+' no new palette or wardrobe color',set(after.get_flattened_data())<=set(before.get_flattened_data()))
record={'task':'M1.ON3','pass':True,'count':len(checks),'checks':checks,'contactsAndBounds':details,'appearanceApproval':False,'limitation':'Raster/source/GIF integrity checks do not establish artistic or user acceptance; original far shoe/arm/leg completions are proposals.'}
(S/'checks.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'pass':True,'count':len(checks),'contactsAndBounds':details}))
