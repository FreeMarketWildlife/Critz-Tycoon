"""User-requested true PNG-alpha demonstration; backgrounds alone move.

Sprites use original saved RGBA, alpha_composite and exact nearest enlargement.
The GIF is opaque by design: each decoded eye must equal the backdrop through
the corresponding PNG's empty alpha, not a painted imitation of an eye.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageSequence
import json,hashlib

ROOT=Path(__file__).resolve().parents[3];D=ROOT/'assets/review/tanoshi-eyes-bear-r4';R=ROOT/'docs/reviews/M1-TN4'
names=['blush','mint','apricot','tiny-blush','small-mint','large-lilac']
sprites=[Image.open(D/f'{n}.png').convert('RGBA') for n in names]
def tile(folder,wanted,fallback):
    m=json.loads((ROOT/folder/'atlas.json').read_text()) if (ROOT/folder/'atlas.json').exists() else json.loads((ROOT/folder/'master.json').read_text())
    entry=next((t for t in m['tiles'] if t['id']==wanted),None) or next(t for t in m['tiles'] if t['id'].startswith(fallback))
    im=Image.open(ROOT/folder/m['image']).convert('RGBA');x,y=entry['x'],entry['y']
    return im.crop((x,y,x+32,y+32)),{'manifest':str(folder),'tile':entry['id'],'rect':[x,y,32,32]}
grass,g_info=tile(Path('assets/playable/overworld'),'ground.grass.0','ground.grass')
path,p_info=tile(Path('assets/playable/overworld'),'path.255','path.')
stone,s_info=tile(Path('assets/playable/overworld'),'paving.0','paving.')
dark=Image.new('RGBA',(32,32),'#182531');draw=ImageDraw.Draw(dark)
for yy in range(0,32,4):
    for xx in range(0,32,4):draw.rectangle((xx,yy,xx+3,yy+3),fill='#182531' if (xx//4+yy//4)%2 else '#3f5866')
backs=[('actual grass tile',grass),('actual path tile',path),('actual paving tile',stone),('dark checkerboard',dark)]
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',16);small=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',13)
frames=[];expected=[];full_native=[]
for bi,(label,bg) in enumerate(backs):
    for step in range(8):
        offset=step*2;field=Image.new('RGBA',(192,32),'#80b86b')
        for y in range(-32,64,32):
            for x in range(-32,224,32):field.alpha_composite(bg,(x-offset,y-offset))
        back=field.convert('RGB');composite=field.copy()
        for i,im in enumerate(sprites):composite.alpha_composite(im,(i*32,0))
        native=composite.convert('RGB');full_native.append(native)
        frame=Image.new('RGB',(768,736),'#203a38');dr=ImageDraw.Draw(frame);dr.fontmode='1'
        dr.text((12,8),'Tanoshi transparent eyes — stationary PNGs / moving backdrops',font=font,fill='#f5f0de')
        dr.text((12,30),'8× nearest pixels · '+label,font=small,fill='#cbdfca')
        for row in [0,1]:
            labels=['regular Blush','regular Mint','Apricot'] if row==0 else ['tiny Blush','small Mint','large Lilac']
            sy=54 if row==0 else 352
            for col,text in enumerate(labels):dr.text((col*256+10,sy),text,font=small,fill='#f5f0de')
            part=native.crop((row*96,0,(row+1)*96,32)).resize((768,256),Image.Resampling.NEAREST)
            frame.paste(part,(0,sy+22))
        dr.text((12,636),'Native comparison: six original32×32 frames at1×',font=small,fill='#f5f0de')
        frame.paste(native,(288,660))
        dr.text((12,708),'Actual saved alpha through eye holes · no smoothing · review only',font=small,fill='#cbdfca')
        frames.append(frame);expected.append(back)

# A single exact palette preserves every sprite and backdrop RGB value.
colors=sorted(set().union(*(set(im.get_flattened_data()) for im in frames)))
assert len(colors)<=256,(len(colors),'GIF palette cannot preserve exact pixels')
lookup={c:i for i,c in enumerate(colors)};palette=[v for c in colors for v in c]+[0]*(768-len(colors)*3)
encoded=[]
for im in frames:
    p=Image.new('P',im.size);p.putpalette(palette);p.putdata([lookup[c] for c in im.get_flattened_data()]);encoded.append(p)
target=R/'Tanoshi-transparent-eyes-moving-backgrounds.gif'
encoded[0].save(target,save_all=True,append_images=encoded[1:],duration=160,loop=0,optimize=False,disposal=2)
native_encoded=[]
for im in full_native:
    p=Image.new('P',im.size);p.putpalette(palette);p.putdata([lookup[c] for c in im.get_flattened_data()]);native_encoded.append(p)
native_target=R/'Tanoshi-transparent-eyes-native.gif'
native_encoded[0].save(native_target,save_all=True,append_images=native_encoded[1:],duration=160,loop=0,optimize=False,disposal=2)

gif=Image.open(target);decoded=[f.convert('RGB').copy() for f in ImageSequence.Iterator(gif)];assert len(decoded)==32
hole_checks=0;opaque_checks=0;hole_colors={n:set() for n in names}
for index,frame in enumerate(decoded):
    assert frame.tobytes()==frames[index].tobytes(),('GIF RGB changed',index)
    assert frame.crop((288,660,480,692)).tobytes()==full_native[index].tobytes()
    for i,(name,sprite) in enumerate(zip(names,sprites)):
        row,col=divmod(i,3);sx=col*256;sy=76 if row==0 else 374
        for y in range(32):
            for x in range(32):
                source=sprite.getpixel((x,y));actual=frame.getpixel((sx+x*8+4,sy+y*8+4))
                if source[3]:assert actual==source[:3];opaque_checks+=1
                else:
                    assert actual==expected[index].getpixel((i*32+x,y));hole_checks+=1
                    if 12<=x<20 and 14<=y<24:hole_colors[name].add(actual)
for name,seen in hole_colors.items():assert len(seen)>=4,(name,'eye backdrop never changes')
native_gif=Image.open(native_target);assert native_gif.n_frames==32 and native_gif.size==(192,32)
for i,f in enumerate(ImageSequence.Iterator(native_gif)):assert f.convert('RGB').tobytes()==full_native[i].tobytes()
frames[3].save(R/'gif-grass-poster.png');frames[27].save(R/'gif-dark-poster.png')
report={'task':'M1.TN4','purpose':'User-authorized GIF demonstrates real saved PNG alpha against moving scenery; no browser screenshots.','file':target.name,'nativeFile':native_target.name,'frames':32,'durationEachMs':160,'loopMs':5120,'size':[768,736],'nativeSize':[192,32],'exactPaletteColors':len(colors),'pngAlphaComposite':True,'nearestEnlargement':8,'nativeAndEnlargedPixelsExact':True,'decodedFramesExact':True,'opaqueSpriteChecks':opaque_checks,'transparentBackgroundChecks':hole_checks,'eyeBackdropColors':{n:len(c) for n,c in hole_colors.items()},'backdropSources':[g_info,p_info,s_info,'generated checkerboard contrast only, not new game art'],'spritePNGHashes':{n:hashlib.sha256((D/f'{n}.png').read_bytes()).hexdigest() for n in names},'gifSHA256':hashlib.sha256(target.read_bytes()).hexdigest(),'nativeGifSHA256':hashlib.sha256(native_target.read_bytes()).hexdigest(),'sourcePNGsPreserved':True}
(R/'gif-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['frames','size','exactPaletteColors','opaqueSpriteChecks','transparentBackgroundChecks','eyeBackdropColors']}))
