"""Mechanical export of imagegen-authored art; never constructs sprite geometry.

The approved pet sheet is an identity reference, not a production raster.
Generated inputs are retained unchanged. This export uses one fixed crop/sample
registration for every individual, no smoothing/dithering, and flat material
ramps to remove imagegen's sub-block noise. Native art remains a review proposal.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'art/source/tanoshi'
DEST = ROOT / 'assets/playable/tanoshi'
REVIEW = ROOT / 'docs/reviews/M1-TN1'
PALETTES = {
    'blush': ['#32112f', '#c499d8', '#ffe1ed'],
    'mint': ['#103c46', '#45a8a5', '#baf3d2'],
    'apricot': ['#451e2b', '#f58c76', '#ffe5bd'],
}
atlas = Image.new('RGBA', (96, 32))
report = []
assets = []
for i, (variant, colors) in enumerate(PALETTES.items()):
    path = SOURCE / f'generated-{variant}.png'
    original = Image.open(path).convert('RGBA')
    # Fixed framing retains the same master proportions and cell registration.
    sampled = original.crop((230, 270, 1040, 1136)).resize((26, 28), Image.Resampling.NEAREST)
    palette = [tuple(bytes.fromhex(color[1:])) for color in colors]
    native = Image.new('RGBA', (32, 32))
    indices = [[0] * 32 for _ in range(32)]
    for y in range(28):
        for x in range(26):
            r, g, b, alpha = sampled.getpixel((x, y))
            if alpha < 128:
                continue
            index = min(range(3), key=lambda k: sum((v-c)**2 for v,c in zip((r,g,b),palette[k])))
            native.putpixel((x+3,y+2), (*palette[index],255))
            indices[y+2][x+3] = index+1
    native.save(DEST / f'{variant}.png')
    atlas.paste(native,(i*32,0))
    (SOURCE / f'{variant}.pixels.json').write_text(json.dumps({'width':32,'height':32,'palette':['#00000000',*colors],'rows':indices},indent=2)+'\n')
    report.append({'variant':variant,'generatedSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'nativeSha256':hashlib.sha256((DEST/f'{variant}.png').read_bytes()).hexdigest(),'bounds':native.getbbox(),'opaquePixels':sum(a>0 for *rgb,a in native.getdata()),'opaqueColors':len(set(p for p in native.getdata() if p[3])),'alphaValues':sorted(set(native.getchannel('A').getdata()))})
    assets.append({'id':variant,'rect':[i*32,0,32,32],'anchor':[16,32],'sortAnchor':[16,32]})
atlas.save(DEST/'atlas.png')
(DEST/'atlas.json').write_text(json.dumps({'schemaVersion':1,'image':'atlas.png','size':[96,32],'task':'M1.TN1','appearanceStatus':'awaiting user visual review','assets':assets},indent=2)+'\n')
atlas.save(REVIEW/'native.png')
atlas.resize((768,256),Image.Resampling.NEAREST).save(REVIEW/'clean-8x.png')
grid=Image.new('RGBA',(960,320),'#f4ebd9')
draw=ImageDraw.Draw(grid)
for i,variant in enumerate(PALETTES):
    left=i*320+42;top=32
    grid.alpha_composite(atlas.crop((i*32,0,i*32+32,32)).resize((256,256),Image.Resampling.NEAREST),(left,top))
    draw.text((left,10),variant+' / 32x32 / 8x',fill='#253b37')
    for x in range(33):draw.line((left+x*8,top,left+x*8,top+256),fill='#bac0b0')
    for y in range(33):draw.line((left,top+y*8,left+256,top+y*8),fill='#bac0b0')
    for value in [0,10,20,30,32]:
        y=top+(32-value)*8
        draw.line((left,y,left+256,y),fill='#428d87')
        draw.text((left-26,y-5),str(value),fill='#253b37')
    draw.line((left+128,top,left+128,top+256),fill='#d06d43',width=2)
    draw.text((left+120,top+263),'x16',fill='#a45231')
grid.save(REVIEW/'grid-8x.png')
for background,name in [('#f4ebd9','light'),('#29313f','dark')]:
    plate=Image.new('RGBA',(768,256),background)
    plate.alpha_composite(atlas.resize((768,256),Image.Resampling.NEAREST))
    plate.save(REVIEW/f'clean-{name}-8x.png')
(REVIEW/'asset-check.json').write_text(json.dumps({'task':'M1.TN1','method':'Imagegen creation/edits; fixed-crop nearest sampling and flat palette encoding, no procedural silhouette authoring','sourceCrop':[230,270,1040,1136],'sampleSize':[26,28],'placement':[3,2],'assets':report},indent=2)+'\n')
