"""Validate exported PNG bytes independently of the native atlas authoring code."""
from pathlib import Path
import hashlib
import json
from PIL import Image

root = Path(__file__).resolve().parents[1]
folder = root / 'assets/review/budget-comparison'
manifest = json.loads((folder / 'atlas.json').read_text())
sheet = Image.open(folder / 'atlas.png').convert('RGBA')
checks = []

def check(name, passed):
    assert passed, name
    checks.append({'name': name, 'pass': True})

assets = manifest['assets']
expected = {f'compare.{role}.{size}.{direction}.{pose}'
            for role in ('mom', 'kaid', 'professor') for size in (16, 24)
            for direction in ('down', 'up', 'left', 'right')
            for pose in ('idle', 'strideA', 'strideB')}
check('exact 72 unique stable IDs cover the full matrix', len(assets) == 72 and {a['id'] for a in assets} == expected)
check('PNG dimensions agree with manifest', list(sheet.size) == manifest['size'] == [288, 192])
check('PNG uses binary alpha including transparent space', set(sheet.getchannel('A').get_flattened_data()) == {0, 255})
occupied = set()
native = {}
for a in assets:
    x, y, w, h = a['rect']
    assert 0 <= x <= sheet.width - w and 0 <= y <= sheet.height - h
    cells = {(xx, yy) for yy in range(y, y+h) for xx in range(x, x+w)}
    assert not occupied.intersection(cells), a['id']
    occupied.update(cells)
    crop = sheet.crop((x, y, x+w, y+h))
    assert hashlib.sha256(crop.tobytes()).hexdigest() == a['sha256'], a['id']
    assert list(crop.getbbox()) == a['opaqueBBox'], a['id']
    assert a['anchor'] == [w//2, 32]
    assert len({p[:3] for p in crop.get_flattened_data() if p[3]}) == a['colorCount'] <= 15
    native[a['id']] = crop
check('all frame rectangles are in bounds and nonoverlapping', True)
check('every decoded PNG crop matches its exact native RGBA hash', True)
check('opaque bounds, colors and bottom-center anchors match metadata', True)
for size in (16, 24):
    for pose in ('idle', 'strideA', 'strideB'):
        left = native[f'compare.kaid.{size}.left.{pose}']
        right = native[f'compare.kaid.{size}.right.{pose}']
        assert left.tobytes() != right.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
check('Kaid side directions are independently authored, never mirrored', True)
report = {'passed': len(checks), 'checks': checks, 'atlasSha256': hashlib.sha256((folder/'atlas.png').read_bytes()).hexdigest()}
(root / 'docs/reviews/M1-C1/png-validation.json').write_text(json.dumps(report, indent=2)+'\n')
print(f"{len(checks)} exported-PNG checks passed.")
