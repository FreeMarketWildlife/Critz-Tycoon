"""Encode imagegen-authored outline edits without changing native geometry.

Only a generated darkest-material sample may recolor an already occupied cell.
All original alpha, eye-hole cells, existing dark ink and non-dark colors remain
exact otherwise. No dilation, contour construction or procedural eye drawing.
"""
from pathlib import Path
from PIL import Image
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'art/source/tanoshi-outline'
DEST = ROOT / 'assets/playable/tanoshi-outline'
REVIEW = ROOT / 'docs/reviews/M1-TN3/art'
DEST.mkdir(parents=True, exist_ok=True)
REVIEW.mkdir(parents=True, exist_ok=True)
INPUTS = json.loads((SOURCE / 'inputs.json').read_text())
IDS = ['blush', 'mint', 'apricot', 'tiny-blush', 'small-mint', 'large-lilac']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

images, reports, assets = {}, [], []
atlas = Image.new('RGBA', (len(IDS) * 32, 32))
for name in [*IDS, 'bear']:
    info = INPUTS[name]
    original = Image.open(ROOT / info['original']).convert('RGBA')
    family = 'tanoshi' if name in ['blush', 'mint', 'apricot'] else 'tanoshi-sizes'
    indexed = json.loads((ROOT / f'art/source/{family}/{name}.pixels.json').read_text())
    palette = [tuple(bytes.fromhex(c[1:])) + (255,) for c in indexed['palette'][1:]]
    original_colors = set(p for p in original.get_flattened_data() if p[3])
    assert original_colors <= set(palette)
    generated_path = SOURCE / f'generated-{name}.png'
    generated = Image.open(generated_path).convert('RGBA')
    # The generated border may expand its own alpha. Register that color
    # proposal to the original occupied box; original geometry stays exact.
    generated_box=generated.getchannel('A').point(lambda a:255 if a>=128 else 0).getbbox()
    box=original.getbbox();x0,y0,x1,y1=box
    # Fixed color-guide margin brings the generated line weight inward; it
    # never expands or constructs the original alpha silhouette.
    padding=0 if name=='bear' else 1
    mx=round((generated_box[2]-generated_box[0])/(x1-x0)*padding)
    my=round((generated_box[3]-generated_box[1])/(y1-y0)*padding)
    registered_crop=[generated_box[0]-mx,generated_box[1]-my,generated_box[2]+mx,generated_box[3]+my]
    sampled=Image.new('RGBA',original.size)
    sampled.paste(generated.crop(registered_crop).resize((x1-x0,y1-y0),Image.Resampling.NEAREST),(x0,y0))
    native = original.copy()
    changed = []
    for y in range(original.height):
        for x in range(original.width):
            old, proposed = original.getpixel((x, y)), sampled.getpixel((x, y))
            if not old[3] or old == palette[0]:
                continue
            k = min(range(len(palette)), key=lambda i: sum((a-b)**2 for a,b in zip(proposed[:3],palette[i][:3])))
            if k == 0:
                native.putpixel((x, y), palette[0])
                changed.append([x, y])
    assert native.getchannel('A').tobytes() == original.getchannel('A').tobytes()
    assert native.getbbox() == original.getbbox()
    before = sum(p == palette[0] for p in original.get_flattened_data())
    after = sum(p == palette[0] for p in native.get_flattened_data())
    native_path = DEST / f'{name}.png'
    native.save(native_path)
    rows = [[0 if not native.getpixel((x,y))[3] else palette.index(native.getpixel((x,y)))+1 for x in range(native.width)] for y in range(native.height)]
    provenance = {'original': info['original'], 'originalSha256': sha(ROOT / info['original']),
                  'generated': str(generated_path.relative_to(ROOT)), 'generatedSha256': sha(generated_path),
                  'generatedSize': list(generated.size), 'sampling': 'generated alpha128 occupied crop to original occupied box, Pillow nearest; original alpha fixes geometry', 'generatedCrop':registered_crop, 'generatedAlphaBounds':list(generated_box), 'guidePaddingNativeCells':padding, 'targetBox':list(box), 'proposalAlphaPolicy':'Original native alpha alone owns opacity; sampled transparent guide RGB may classify as dark under occupied stencil cells.',
                  'encoding': 'accept imagegen darkest-material additions only on original occupied cells; preserve all original alpha, ink and other colors',
                  'geometryEdits': False, 'darkPixelsBefore': before, 'darkPixelsAfter': after, 'changedCells': changed}
    (SOURCE / f'{name}.pixels.json').write_text(json.dumps({'width':native.width,'height':native.height,'palette':indexed['palette'],'rows':rows,'provenance':provenance},indent=2)+'\n')
    reports.append({'id':name,'size':list(native.size),'bounds':list(native.getbbox()),'nativeSha256':sha(native_path),**provenance})
    images[name] = native
    if name in IDS:
        i = IDS.index(name)
        atlas.paste(native, (i*32, 0))
        assets.append({'id':name,'rect':[i*32,0,32,32],'anchor':[16,32],'sortAnchor':[16,32]})
atlas.save(DEST / 'atlas.png')
(DEST / 'atlas.json').write_text(json.dumps({'schemaVersion':1,'task':'M1.TN3','image':'atlas.png','size':list(atlas.size),'appearanceStatus':'awaiting parent visual review','assets':assets},indent=2)+'\n')
bear_meta = json.loads((ROOT / 'assets/playable/tanoshi-sizes/bear.json').read_text())
bear_meta.update(task='M1.TN3', appearanceStatus='awaiting parent visual review', provenance=reports[-1])
(DEST / 'bear.json').write_text(json.dumps(bear_meta,indent=2)+'\n')
(REVIEW / 'export-checks.json').write_text(json.dumps({'task':'M1.TN3','method':'imagegen outline edits, disclosed alpha/palette-preserving material encoding','assets':reports},indent=2)+'\n')
active = ['tiny-blush','small-mint','apricot','large-lilac']
for label, color in [('light','#f4ebd9'),('dark','#29313f')]:
    plate = Image.new('RGBA',(128,128),color)
    for i,name in enumerate(active):plate.alpha_composite(images[name],(i*32,0))
    plate.alpha_composite(images['bear'],(0,32))
    hero_manifest=json.loads((ROOT/'assets/playable/living/atlas.json').read_text())
    a=next(a for a in hero_manifest['assets'] if a['id']=='hero-boy.1')
    x,y,w,h=a['rect'];hero=Image.open(ROOT/'assets/playable/living/atlas.png').convert('RGBA').crop((x,y,x+w,y+h))
    plate.alpha_composite(hero,(96,48))
    plate.save(REVIEW/f'contact-{label}-native.png')
    plate.resize((1024,1024),Image.Resampling.NEAREST).save(REVIEW/f'contact-{label}-8x.png')
atlas.resize((1536,256),Image.Resampling.NEAREST).save(REVIEW/'all-variants-8x.png')
print(json.dumps([{'id':r['id'],'darkBefore':r['darkPixelsBefore'],'darkAfter':r['darkPixelsAfter'],'addedInk':len(r['changedCells'])} for r in reports],indent=2))
