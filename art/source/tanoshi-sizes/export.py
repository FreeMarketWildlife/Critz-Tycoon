"""Deterministic export of unchanged imagegen-authored M1.TN2 rasters.

Only whole fixed crops, nearest sampling, alpha threshold and flat material
encoding are used. This program does not construct silhouettes or eye geometry.
Generated sources remain unchanged. All new appearances await visual review.
"""
from pathlib import Path
from PIL import Image, ImageDraw, __version__ as PILLOW_VERSION
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'art/source/tanoshi-sizes'
DEST = ROOT / 'assets/playable/tanoshi-sizes'
REVIEW = ROOT / 'docs/reviews/M1-TN2/art'
DEST.mkdir(parents=True, exist_ok=True)
REVIEW.mkdir(parents=True, exist_ok=True)

SPECS = [
    {'id': 'tiny-blush', 'source': 'generated-tiny-blush.png',
     'crop': [345, 438, 934, 1079], 'sampleSize': [16, 18], 'placement': [8, 12],
     'palette': ['#32112f', '#c499d8', '#ffe1ed'],
     'faceRegion': [12, 18, 20, 25],
     'limit': 'The original notch is open under eight-neighbor transparency; both authored eye interiors survive as one-by-two pixels.'},
    {'id': 'small-mint', 'source': 'generated-small-mint.png',
     'crop': [283, 340, 964, 1129], 'sampleSize': [20, 22], 'placement': [6, 8],
     'palette': ['#103c46', '#45a8a5', '#baf3d2'],
     'faceRegion': [12, 15, 20, 23],
     'limit': 'Ten source pixels of transparent left crop margin retain both authored unequal eye holes: left one-by-two, right one-by-one. No eye pixels are filled or carved.'},
    {'id': 'large-lilac', 'source': 'generated-large-lilac.png',
     'crop': [98, 79, 1156, 1207], 'sampleSize': [30, 30], 'placement': [1, 0],
     'palette': ['#35123f', '#b88bdf', '#f6d9f3'],
     'faceRegion': [10, 12, 21, 21],
     'limit': 'Both authored face holes survive; a separate small enclosed body/tail cutout is preserved and is not counted as an eye.'},
]
GENERATION_JOBS = {
    'generated-bear.png': 'exec-9b40ce49-ed08-4f66-9c61-522b36370c87',
    'generated-tiny-blush.png': 'exec-c1f4e522-54a3-4dba-88db-8b80866bfc78',
    'generated-small-mint.png': 'exec-93743be4-13e8-4fa3-8948-c7559485e568',
    'generated-large-lilac.png': 'exec-83e6951c-aae3-4675-b6a5-c61fd9966d9b',
}
BEAR = {'id': 'bear', 'source': 'generated-bear.png',
        'crop': [19, 288, 1237, 968], 'sampleSize': [64, 36], 'placement': [16, 44],
        'palette': ['#42271e', '#78432c', '#a65f34', '#c5844f', '#eed2a0', '#554149']}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_bbox(im):
    return im.getchannel('A').point(lambda a: 255 if a >= 128 else 0).getbbox()


def export(spec, size):
    original_path = SOURCE / spec['source']
    original = Image.open(original_path).convert('RGBA')
    sampled = original.crop(spec['crop']).resize(spec['sampleSize'], Image.Resampling.NEAREST)
    colors = [tuple(bytes.fromhex(c[1:])) for c in spec['palette']]
    native = Image.new('RGBA', size)
    indices = [[0] * size[0] for _ in range(size[1])]
    ox, oy = spec['placement']
    for y in range(sampled.height):
        for x in range(sampled.width):
            r, g, b, a = sampled.getpixel((x, y))
            if a < 128:
                continue
            k = min(range(len(colors)), key=lambda i: sum((v - c) ** 2 for v, c in zip((r, g, b), colors[i])))
            native.putpixel((x + ox, y + oy), (*colors[k], 255))
            indices[y + oy][x + ox] = k + 1
    native_path = DEST / (spec['id'] + '.png')
    native.save(native_path)
    data = {'width': size[0], 'height': size[1], 'palette': ['#00000000', *spec['palette']],
            'rows': indices, 'provenance': {'source': 'art/source/tanoshi-sizes/' + spec['source'],
            'sourceSha256': sha(original_path), 'sourceSize': list(original.size),
            'generationJobId': GENERATION_JOBS[spec['source']],
            'sourceBoundsAlpha128': list(alpha_bbox(original)), 'fixedCrop': spec['crop'],
            'sampleSize': spec['sampleSize'], 'placement': spec['placement'], 'alphaThreshold': 128,
            'sampling': 'nearest, no smoothing or dithering',
            'samplingLibrary': 'Pillow ' + PILLOW_VERSION,
            'encoding': 'closest squared-RGB material color, no geometry edits'}}
    (SOURCE / (spec['id'] + '.pixels.json')).write_text(json.dumps(data, indent=2) + '\n')
    report = {'id': spec['id'], **data['provenance'], 'nativeSize': list(size),
              'paintedBounds': list(native.getbbox()),
              'opaquePixels': sum(a > 0 for r, g, b, a in native.get_flattened_data()),
              'opaqueColors': len(set(p for p in native.get_flattened_data() if p[3])),
              'nativeSha256': sha(native_path), 'palette': spec['palette'],
              'limitation': spec.get('limit', 'Integer aspect fit; no shadow or ground patch is baked into the export.')}
    return native, report


atlas = Image.new('RGBA', (96, 32))
assets, reports, natives = [], [], []
for i, spec in enumerate(SPECS):
    native, report = export(spec, (32, 32))
    atlas.paste(native, (i * 32, 0))
    assets.append({'id': spec['id'], 'rect': [i * 32, 0, 32, 32],
                   'anchor': [16, 32], 'sortAnchor': [16, 32]})
    reports.append(report)
    natives.append(native)
atlas.save(DEST / 'atlas.png')
(DEST / 'atlas.json').write_text(json.dumps({'schemaVersion': 1, 'task': 'M1.TN2',
    'image': 'atlas.png', 'size': [96, 32], 'appearanceStatus': 'awaiting user visual review',
    'assets': assets}, indent=2) + '\n')

bear, bear_report = export(BEAR, (96, 96))
bear_meta = {'schemaVersion': 1, 'task': 'M1.TN2', 'id': 'bear', 'image': 'bear.png',
    'size': [96, 96], 'footprint': [0, 32, 96, 32], 'footprintCells': [0, 1, 3, 1],
    'drawOffsetFromFootprintPixels': [0, -32], 'groundAnchor': [48, 80], 'sortAnchor': [48, 64],
    'transparentRows': [[0, 16], [80, 96]], 'lowerContactX': [16, 80], 'contactRule': 'B',
    'sourceAspect': 1218 / 680, 'paintedAspect': 64 / 36,
    'aspectRoundingRelativeError': abs((64 / 36) / (1218 / 680) - 1),
    'appearanceStatus': 'awaiting user visual review',
    'provenance': bear_report}
(DEST / 'bear.json').write_text(json.dumps(bear_meta, indent=2) + '\n')

# Include the accepted regular individual as a byte-unchanged comparison only.
regular_path = ROOT / 'assets/playable/tanoshi/apricot.png'
regular = Image.open(regular_path).convert('RGBA')
comparison = Image.new('RGBA', (128, 32))
for i, im in enumerate([natives[0], natives[1], regular, natives[2]]):
    comparison.paste(im, (i * 32, 0))
comparison.save(REVIEW / 'native.png')
comparison.resize((1024, 256), Image.Resampling.NEAREST).save(REVIEW / 'clean-8x.png')
for color, name in [('#f4ebd9', 'light'), ('#29313f', 'dark')]:
    plate = Image.new('RGBA', (1024, 256), color)
    plate.alpha_composite(comparison.resize((1024, 256), Image.Resampling.NEAREST))
    plate.save(REVIEW / ('clean-' + name + '-8x.png'))
    bp = Image.new('RGBA', (768, 768), color)
    bp.alpha_composite(bear.resize((768, 768), Image.Resampling.NEAREST))
    bp.save(REVIEW / ('bear-' + name + '-8x.png'))
bear.save(REVIEW / 'bear-native.png')

grid = Image.new('RGBA', (1280, 336), '#f4ebd9')
draw = ImageDraw.Draw(grid)
for i, (name, im) in enumerate(zip(['Tiny /16x18', 'Small /20x22', 'Regular unchanged /26x28', 'Large /30x30'], [natives[0], natives[1], regular, natives[2]])):
    left, top = i * 320 + 42, 32
    grid.alpha_composite(im.resize((256, 256), Image.Resampling.NEAREST), (left, top))
    draw.text((left, 10), name, fill='#253b37')
    for x in range(33):
        draw.line((left + x * 8, top, left + x * 8, top + 256), fill='#bac0b0')
    for y in range(33):
        draw.line((left, top + y * 8, left + 256, top + y * 8), fill='#bac0b0')
    for value in [0, 10, 20, 30, 32]:
        yy = top + (32 - value) * 8
        draw.line((left, yy, left + 256, yy), fill='#428d87')
        draw.text((left - 26, yy - 5), str(value), fill='#253b37')
    draw.line((left + 128, top, left + 128, top + 256), fill='#d06d43', width=2)
    draw.text((left + 120, top + 263), 'x16', fill='#a45231')
grid.save(REVIEW / 'grid-8x.png')

bg = Image.new('RGBA', (848, 864), '#f4ebd9')
bd = ImageDraw.Draw(bg)
left, top = 48, 40
bg.alpha_composite(bear.resize((768, 768), Image.Resampling.NEAREST), (left, top))
bd.text((left, 8), 'Original resting bear /96x96 /8x /B /ground y80 /sort y64', fill='#253b37')
for i in range(97):
    color = '#b7beae' if i % 32 else '#477e78'
    bd.line((left + i * 8, top, left + i * 8, top + 768), fill=color)
    bd.line((left, top + i * 8, left + 768, top + i * 8), fill=color)
bd.rectangle((left, top + 256, left + 767, top + 511), outline='#d06d43', width=3)
bd.line((left, top + 640, left + 768, top + 640), fill='#259157', width=3)
bd.line((left, top + 512, left + 768, top + 512), fill='#776ac9', width=3)
for value in [0, 16, 32, 64, 80, 96]:
    bd.text((8, top + value * 8 - 5), str(value), fill='#253b37')
bd.text((left, 825), 'Orange footprint rows32-63; purple sort64; green ground80. Artwork unchanged by guides.', fill='#253b37')
bg.save(REVIEW / 'bear-grid-8x.png')

(REVIEW / 'asset-provenance.json').write_text(json.dumps({'task': 'M1.TN2',
    'method': 'Four completed imagegen originals; fixed crops, nearest sampling and flat material encoding. No procedural silhouette/eye authoring.',
    'generation': {'tool': 'image_gen', 'jobs': GENERATION_JOBS, 'additionalJobs': [],
        'promptDirectionSummary': 'Approved shared Tanoshi flame/notch/rays/transparent eyes, compact pink and mint individuals and fuller lilac individual. Original russet long-bodied resting bear with round ears, cream muzzle and tucked paws; no Snorlax appearance, ground or baked shadow.',
        'promptSummaryIsVerbatim': False},
    'alphaThreshold': 128, 'assets': reports, 'bear': bear_meta,
    'regularApricotSha256': sha(regular_path),
    'visualAcceptance': 'pending user checkpoint; technical checks do not approve appearance'}, indent=2) + '\n')
print(json.dumps({'assets': reports, 'bear': bear_report, 'regularApricotSha256': sha(regular_path)}, indent=2))
