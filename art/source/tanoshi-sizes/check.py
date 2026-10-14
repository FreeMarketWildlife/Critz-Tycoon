"""Independent checks of saved TN2 native PNGs, indexed data and provenance."""
from pathlib import Path
from PIL import Image
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'art/source/tanoshi-sizes'
DEST = ROOT / 'assets/playable/tanoshi-sizes'
REVIEW = ROOT / 'docs/reviews/M1-TN2/art'
D8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]
RAW_HASHES = {
    'generated-tiny-blush.png': 'f88c05e97af9c910eed42c765b8ac5fd772638d4f9de5138e173dc200473b9a1',
    'generated-small-mint.png': 'a0a5d6e174fb69de717fab10bf6da44b3c76cf6a0827ebf64ad9df7243f9612c',
    'generated-large-lilac.png': '851b41c71b47896f1784955e70bcb773b9e253884313b9fdef27e8f1df92e480',
    'generated-bear.png': '95f5e0a044ec38344ec1fcd1c654cedd0ac4f82d3d5e58984130e05c1e899716',
}
FACE_REGIONS = {'tiny-blush': [12, 18, 20, 25], 'small-mint': [12, 15, 20, 23],
                'large-lilac': [10, 12, 21, 21]}
BOUNDS = {'tiny-blush': [8, 12, 24, 30], 'small-mint': [6, 8, 26, 30],
          'large-lilac': [1, 0, 31, 30], 'bear': [16, 44, 80, 80]}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def components(im, transparent):
    points = {(x, y) for y in range(im.height) for x in range(im.width)
              if (im.getpixel((x, y))[3] == 0) == transparent}
    results = []
    while points:
        queue = [points.pop()]
        for x, y in queue:
            for dx, dy in D8:
                p = (x + dx, y + dy)
                if p in points:
                    points.remove(p)
                    queue.append(p)
        results.append({'bounds': [min(x for x, y in queue), min(y for x, y in queue),
                                  max(x for x, y in queue) + 1, max(y for x, y in queue) + 1],
                        'pixels': len(queue),
                        'touchesCanvasEdge': any(x in (0, im.width - 1) or y in (0, im.height - 1) for x, y in queue)})
    return sorted(results, key=lambda c: tuple(c['bounds']))


atlas = Image.open(DEST / 'atlas.png').convert('RGBA')
assert atlas.size == (96, 32)
manifest = json.loads((DEST / 'atlas.json').read_text())
assert [a['id'] for a in manifest['assets']] == ['tiny-blush', 'small-mint', 'large-lilac']
checks = []
for i, name in enumerate(['tiny-blush', 'small-mint', 'large-lilac', 'bear']):
    im = Image.open(DEST / (name + '.png')).convert('RGBA')
    size = (96, 96) if name == 'bear' else (32, 32)
    assert im.size == size and list(im.getbbox()) == BOUNDS[name]
    data = json.loads((SOURCE / (name + '.pixels.json')).read_text())
    palette = [(0, 0, 0, 0), *[tuple(bytes.fromhex(c[1:])) + (255,) for c in data['palette'][1:]]]
    reconstructed = bytes(v for row in data['rows'] for index in row for v in palette[index])
    assert im.tobytes() == reconstructed, (name, 'saved PNG differs from editable indexed source')
    assert set(im.getchannel('A').get_flattened_data()) == {0, 255}
    source_path = ROOT / data['provenance']['source']
    assert sha(source_path) == RAW_HASHES[source_path.name] == data['provenance']['sourceSha256']
    source = Image.open(source_path).convert('RGBA')
    crop = data['provenance']['fixedCrop']
    sw, sh = data['provenance']['sampleSize']
    ox, oy = data['provenance']['placement']
    # Independently load/resample the source; never invoke export.py or its
    # encoding helpers. The installed Pillow nearest sampler is authoritative:
    # ideal double-precision coordinate formulas differ at exact boundaries.
    sampled = source.crop(crop).resize((sw, sh), Image.Resampling.NEAREST)
    for y in range(size[1]):
        for x in range(size[0]):
            expected = (0, 0, 0, 0)
            if ox <= x < ox + sw and oy <= y < oy + sh:
                r, g, b, a = sampled.getpixel((x - ox, y - oy))
                if a >= 128:
                    k = min(range(1, len(palette)), key=lambda k: sum((a - b) ** 2 for a, b in zip((r, g, b), palette[k][:3])))
                    expected = palette[k]
            assert im.getpixel((x, y)) == expected, (name, x, y, 'source sample differs')
    opaque = components(im, False)
    assert len(opaque) == 1, (name, 'body and extremities are not eight-connected')
    entry = {'id': name, 'size': list(im.size), 'paintedBounds': list(im.getbbox()),
             'opaquePixels': opaque[0]['pixels'], 'opaqueColors': len(set(p for p in im.get_flattened_data() if p[3])),
             'binaryAlpha': True, 'pngIndexedSourceExact': True, 'sourceCropMaterialEncodingExact': True,
             'sourceSha256': sha(source_path), 'nativeSha256': sha(DEST / (name + '.png')),
             'opaqueComponents8': opaque}
    if name != 'bear':
        assert entry['opaqueColors'] == 3
        assert im.tobytes() == atlas.crop((i * 32, 0, i * 32 + 32, 32)).tobytes()
        assert manifest['assets'][i]['anchor'] == [16, 32]
        assert manifest['assets'][i]['sortAnchor'] == [16, 32]
        assert all(im.getpixel((x, y))[3] == 0 for y in (30, 31) for x in range(32))
        holes = [c for c in components(im, True) if not c['touchesCanvasEdge']]
        l, t, r, b = FACE_REGIONS[name]
        eyes = [c for c in holes if l <= c['bounds'][0] < c['bounds'][2] <= r
                and t <= c['bounds'][1] < c['bounds'][3] <= b]
        body = [c for c in holes if c not in eyes]
        assert len(eyes) == 2 and eyes[0]['bounds'][2] <= eyes[1]['bounds'][0]
        entry.update({'atlasPixelsExact': True, 'twoEmptyFootRows': True,
                      'faceRegion': FACE_REGIONS[name], 'faceHoles8': eyes,
                      'otherEnclosedCutouts8': body,
                      'rayContactLimit': 'All occupied pixels form one eight-connected component; native diagonal ray/head contact is preserved rather than procedurally removed.'})
    else:
        meta = json.loads((DEST / 'bear.json').read_text())
        assert meta['footprint'] == [0, 32, 96, 32]
        assert meta['drawOffsetFromFootprintPixels'] == [0, -32]
        assert meta['groundAnchor'] == [48, 80] and meta['sortAnchor'] == [48, 64]
        assert all(im.getpixel((x, y))[3] == 0 for y in [*range(16), *range(80, 96)] for x in range(96))
        assert all(im.getpixel((x, y))[3] == 0 for y in range(32, 80) for x in [*range(16), *range(80, 96)])
        assert any(im.getpixel((x, 79))[3] for x in range(16, 80))
        assert meta['aspectRoundingRelativeError'] < .01
        entry.update({'footprintMetadataExact': True, 'twoEmptyOuterHalfRows': True,
                      'lowerSideContact16Pixels': True, 'finalPaintedPawRow': 79,
                      'groundEdge': 80, 'sortEdge': 64, 'aspectError': meta['aspectRoundingRelativeError']})
    checks.append(entry)

comparison = Image.open(REVIEW / 'native.png').convert('RGBA')
assert comparison.size == (128, 32)
regular = Image.open(ROOT / 'assets/playable/tanoshi/apricot.png').convert('RGBA')
assert comparison.crop((64, 0, 96, 32)).tobytes() == regular.tobytes()
assert Image.open(REVIEW / 'clean-8x.png').convert('RGBA').tobytes() == comparison.resize((1024, 256), Image.Resampling.NEAREST).tobytes()
assert Image.open(REVIEW / 'bear-native.png').convert('RGBA').tobytes() == Image.open(DEST / 'bear.png').convert('RGBA').tobytes()

protected = []
for directory in ['art/source/tanoshi', 'assets/playable/tanoshi']:
    for path in sorted((ROOT / directory).glob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        previous = subprocess.run(['git', 'show', 'HEAD:' + rel], cwd=ROOT, check=True, capture_output=True).stdout
        assert previous == path.read_bytes(), ('changed protected TN1 file', rel)
        protected.append({'path': rel, 'sha256': sha(path)})
references = json.loads((ROOT / 'references/tanoshi/manifest.json').read_text())
for record in references['files']:
    path = ROOT / 'references/tanoshi' / record['path']
    assert path.stat().st_size == record['size_bytes'] and sha(path) == record['sha256']

result = {'task': 'M1.TN2', 'nativeAssets': checks, 'comparisonIncludesExactRegularApricot': True,
          'exactEightTimesEnlargement': True, 'protectedTN1FilesUnchanged': protected,
          'allSixOriginalReferencesUnchanged': True, 'originalGeneratedSourcesUnchanged': RAW_HASHES,
          'visualInspection': ['original four inputs', 'native/light/dark', 'integer grids and registration'],
          'appearanceAcceptance': 'pending user checkpoint; not self-approved'}
(REVIEW / 'native-checks.json').write_text(json.dumps(result, indent=2) + '\n')
files = []
for directory in [SOURCE, DEST, REVIEW]:
    for path in sorted(directory.rglob('*')):
        if path.is_file() and path.name != 'file-manifest.json' and '__pycache__' not in path.parts:
            files.append({'path': path.relative_to(ROOT).as_posix(), 'sizeBytes': path.stat().st_size, 'sha256': sha(path)})
(REVIEW / 'file-manifest.json').write_text(json.dumps({'task': 'M1.TN2', 'files': files}, indent=2) + '\n')
print(json.dumps(result, indent=2))
