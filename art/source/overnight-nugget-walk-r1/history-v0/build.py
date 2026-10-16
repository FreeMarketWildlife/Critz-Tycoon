"""ON3 original walk study. ON2 inputs read-only; no runtime/shared writes."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib, json

S=Path(__file__).resolve().parent; R=S.parents[2]
O=R/'docs/reviews/M1-ON3'; I=R/'art/source/overnight-nugget-continuation-r1'; P=R/'docs/reviews/M1-ON2'
assert S==R/'art/source/overnight-nugget-walk-r1' and O==R/'docs/reviews/M1-ON3'
F=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',12)
INK=(48,43,41,255); PANTS=(139,129,89,255)
DIRECTIONS=['south','north','west','east']; ORDER={'south':[3,0,4,0],'north':[5,1,6,1],'west':[7,2,8,2],'east':[7,2,8,2]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blank():return Image.new('RGBA',(32,64))
def compose(ls):
    q=blank()
    for im in ls.values():q.alpha_composite(im)
    return q
def cut(q,predicate):
    out=blank()
    for y in range(64):
        for x in range(32):
            if predicate(x,y):out.putpixel((x,y),q.getpixel((x,y)))
    return out
def translate(q,dx=0,dy=0):
    out=blank();out.alpha_composite(q,(dx,dy));return out
def shear_arm(q,slope,pivot=(17,46),dx=0):
    out=blank()
    for y in range(64):
        for x in range(32):
            if q.getpixel((x,y))[3]:
                xx=x+round((y-pivot[1])*slope)+dx; yy=y+2
                assert 0<=xx<32 and 0<=yy<64,'Arm clipped'
                out.putpixel((xx,yy),q.getpixel((x,y)))
    return out
def load(dr):
    src=json.loads((I/f'{dr}.layers.json').read_text())
    return {n:Image.open(I/dr/f'{n}.png').convert('RGBA') for n in src['renderOrder']}
def frontal(dr,phase):
    idle=load(dr)
    body_names=['coat','hands','trousers','shoes','body-outline','coat-details','shirt','lapels','shoe-details','trouser-details']
    body=compose({n:im for n,im in idle.items() if n in body_names})
    # Preserve complete source shoes and short leg cells, moving each whole volume.
    # Image-left leads in Birch3/5, image-right in Birch4/6. No whole-sprite mirroring.
    ls={}
    for side,left in [('left',True),('right',False)]:
        lead=left==(phase=='A'); dx=1 if left else -1;dy=2 if lead else -2
        half=lambda x:(x<16 if left else x>=16)
        ls[side+'-leg']=translate(cut(body,lambda x,y:half(x) and 56<=y<58),dx,dy)
        ls[side+'-shoe']=translate(cut(body,lambda x,y:half(x) and y>=58),dx,dy)
    # Fixed width torso and palette, only the measured rigid vertical stride bob.
    for n in body_names:
        if n in idle and n not in ['shoes','shoe-details','trouser-details']:
            ls['torso-'+n]=translate(cut(idle[n],lambda x,y:9<=x<=22 and 44<=y<=55),0,2)
    for side,left in [('left',True),('right',False)]:
        lead=left==(phase=='A')
        arm=cut(body,lambda x,y:(x<9 if left else x>22) and 44<=y<55)
        # Opposed arm elevation: arm behind planted foot is raised one target cell.
        ls[side+'-arm']=translate(arm,0,1 if lead else 3)
    for n,im in idle.items():
        if n not in body_names:ls[n]=translate(im,0,2)
    return ls
def profile(phase):
    idle=load('west');ls={}
    # Complete hidden far shoe is an explicit original construction from the
    # unchanged full near-shoe shape, never enlargement of the idle heel fragment.
    shoe=compose({n:idle[n] for n in ['near-shoe','shoe-highlight']})
    near_dx,far_dx=(-3,4) if phase=='A' else (4,-3)
    far=shoe.copy()
    for y in range(64):
        for x in range(32):
            p=far.getpixel((x,y))
            if p[3] and p!=INK:far.putpixel((x,y),(52,53,55,255))
    ls['far-shoe']=translate(far,far_dx,0)
    # Two short trouser connections under the rigid coat; no added shin length.
    for n,dx,dy in [('far-leg',far_dx,0),('near-leg',near_dx,2)]:
        im=blank();d=ImageDraw.Draw(im)
        d.polygon([(12,54),(20,54),(18+dx,58+dy),(13+dx,58+dy)],fill=INK)
        d.polygon([(13,55),(19,55),(17+dx,57+dy),(14+dx,57+dy)],fill=PANTS)
        ls[n]=im
    ls['near-shoe']=translate(shoe,near_dx,2)
    arm=compose({n:idle[n] for n in ['sleeve','hand','hand-light']})
    fararm=arm.copy()
    for y in range(64):
        for x in range(32):
            p=fararm.getpixel((x,y))
            if p[:3] in [(210,155,104),(237,187,131)]:fararm.putpixel((x,y),(173,113,79,255))
            elif p[3] and p!=INK:fararm.putpixel((x,y),(185,190,169,255))
    # Near arm opposes near leg about its unchanged shoulder; far arm is behind coat.
    slope=.45 if phase=='A' else -.45
    ls['far-arm']=shear_arm(fararm,-slope,dx=-4)
    for n in ['coat','shirt']:ls[n]=translate(idle[n],0,2)
    ls['near-arm']=shear_arm(arm,slope)
    for n,im in idle.items():
        if n not in ['trousers','far-shoe','near-shoe','shoe-highlight','coat','shirt','sleeve','hand','hand-light']:ls[n]=translate(im,0,2)
    return ls
def save_layers(dr,pose,ls):
    folder=S/dr/pose;folder.mkdir(parents=True,exist_ok=True)
    sparse={}
    for n,im in ls.items():
        im.save(folder/f'{n}.png')
        sparse[n]={'pixels':[[j%32,j//32,*p] for j,p in enumerate(im.get_flattened_data()) if p[3]]}
    (S/dr/f'{pose}.layers.json').write_text(json.dumps({'frame':[32,64],'anchor':[16,64],'renderOrder':list(ls),'layers':sparse},indent=2)+'\n')
    q=compose(ls);q.save(O/f'{dr}-{pose}.png');return q
def board(images):
    q=Image.new('RGB',(780,365),'#eee8d1');d=ImageDraw.Draw(q);d.fontmode='1'
    d.text((12,8),'NUGGET / ON3 WALK STUDY / NOT ACCEPTED / SOURCE 8-TICK SLOTS',font=F,fill='#302b29')
    for i,dr in enumerate(DIRECTIONS):
        x=12+192*i;im=images[dr];big=im.resize((128,256),Image.Resampling.NEAREST)
        d.text((x,33),dr.upper()+' / 4x + native',font=F,fill='#302b29');q.paste(big,(x,58),big);q.paste(im,(x+143,200),im)
    d.text((12,332),'Rigid +2Y strides; exact idle holds; full shoes; fixed anchor16,64.',font=F,fill='#302b29')
    return q
def gif(path,frames,holds,transparent=False):
    # Single explicit palette retains all authored colors; no quantizer fitting.
    colors=sorted({p[:3] for im in frames for p in im.convert('RGBA').get_flattened_data() if p[3]})
    assert len(colors)<255
    palette=[0,0,0]+[v for c in colors for v in c];palette +=[0]*(768-len(palette));mapping={c:i+1 for i,c in enumerate(colors)}
    indexed=[]
    for im in frames:
        q=Image.new('P',im.size);q.putpalette(palette)
        q.putdata([mapping[p[:3]] if p[3] else 0 for p in im.convert('RGBA').get_flattened_data()]);indexed.append(q)
    kw={'transparency':0} if transparent else {}
    indexed[0].save(path,save_all=True,append_images=indexed[1:],duration=holds,loop=0,disposal=2,optimize=False,**kw)
def main():
    guard=json.loads((S/'input-guard.json').read_text())
    assert all(sha(R/p)==h for p,h in guard['protectedON2'].items()),'ON2 changed'
    poses={dr:{} for dr in DIRECTIONS};layers={}
    for dr in DIRECTIONS:
        for pose in ['A','idle','B']:
            if pose=='idle':ls=load(dr)
            elif dr in ['south','north']:ls=frontal(dr,pose)
            elif dr=='west':ls=profile(pose)
            else:ls={n:im.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for n,im in profile(pose).items()}
            poses[dr][pose]=save_layers(dr,pose,ls)
    frames=[]
    for phase in ['A','idle','B','idle']:frames.append(board({dr:poses[dr][phase] for dr in DIRECTIONS}))
    for speed,holds in [('normal',[130,140,130,140]),('slow4x',[540,530,540,530])]:
        gif(O/f'four-directions-{speed}.gif',frames,holds)
        for dr in DIRECTIONS:
            for scale in [1,4]:
                ims=[poses[dr][p].resize((32*scale,64*scale),Image.Resampling.NEAREST) for p in ['A','idle','B','idle']]
                gif(O/f'{dr}-{speed}-{scale}x.gif',ims,holds,True)
    for j,phase in enumerate(['A','idle','B','idle']):frames[j].save(O/f'four-directions-slot{j}.png')
    strip=Image.new('RGB',(780,4*305),'#eee8d1');d=ImageDraw.Draw(strip);d.fontmode='1'
    for row,dr in enumerate(DIRECTIONS):
        for col,phase in enumerate(['A','idle','B','idle']):
            im=poses[dr][phase];x=15+col*192;y=row*305
            d.text((x,y+5),f'{dr} {phase} / src{ORDER[dr][col]}',font=F,fill='#302b29')
            b=im.resize((128,256),Image.Resampling.NEAREST);strip.paste(b,(x,y+27),b);strip.paste(im,(x+145,y+205),im)
    strip.save(O/'all-phases-native-4x.png')
    atlas=Image.new('RGBA',(128,256))
    for row,dr in enumerate(DIRECTIONS):
        for col,p in enumerate(['A','idle','B','idle']):atlas.alpha_composite(poses[dr][p],(col*32,row*64))
    atlas.save(O/'walk-atlas.png')
    manifest={'task':'M1.ON3','state':'in progress, actual visual/playback review required','appearanceApproval':False,'frame':[32,64],'anchor':[16,64],'directions':DIRECTIONS,'poses':['A','idle','B','idle'],'sourceFrames':ORDER,'sourceRevision':'5eff78649e7170a877b961ef0b3da13b81a16038','sourceTickSeconds':280896/16777216,'holdTicks':[8,8,8,8],'cycleTicks':32,'cycleMilliseconds':32*280896/16777216*1000,'gifNormalMilliseconds':[130,140,130,140],'gifSlow4xMilliseconds':[540,530,540,530],'sourceBasis':'Actual Birch PNG plus root-verified sAnim_Go* commands; not emulator observation','construction':'Original clipped ON2 garment/limb layers; full front shoes translated intact; full profile near shoe translated intact; hidden far full shoe completion explicitly proposed. Rigid +2Y head/upperbody bob; no sway/flap/deformation.','sourceInputs':{str(p.relative_to(R)):sha(p) for p in [I/'manifest.json',P/'four-idle-native.png',R/'local-review/overnight-cast-qa/prof_birch.png']}}
    (S/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'poses':12,'nativeAtlas':str(O/'walk-atlas.png'),'strip':str(O/'all-phases-native-4x.png')}))
if __name__=='__main__':main()
