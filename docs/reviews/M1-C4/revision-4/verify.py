"""Independent decoding of native PNGs and every presented native grid cell."""
import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent
layout = json.loads((root / 'grid-layout.json').read_text())
report = {'approval': False, 'frames': [], 'nativeCellComparisons': 0, 'gridCellComparisons': 0}
for slug in ['a-afro', 'b-flat-top', 'c-twists', 'd-cornrows']:
    model = json.loads((root / f'{slug}.json').read_text())
    im = Image.open(root / f'{slug}.png').convert('RGBA')
    assert im.size == (32, 64)
    occupied = set()
    parts = [r.split(',') for r in model['parts']]
    colors = set()
    for y in range(64):
        for x in range(32):
            k = model['rows'][y][x]
            rgb = model['palette'].get(k, '#000000')
            expected = tuple(bytes.fromhex(rgb[1:])) + ((0 if k == '.' else 255),)
            assert im.getpixel((x, y)) == expected, (slug, x, y)
            report['nativeCellComparisons'] += 1
            if k != '.':
                occupied.add((x, y)); colors.add(rgb)
            assert model['skullMask'][y][x] == model['skullMask'][y][31-x]
            if y >= 37:
                assert parts[y][x] == parts[y][31-x], (slug, x, y, 'anatomy')
    assert len(colors) <= 15
    assert im.getbbox()[1::2] == (20, 62)
    assert model['anchor'] == [16, 64]
    eyes = {(x,y) for y in range(64) for x in range(32) if parts[y][x]=='eyes'}
    assert eyes == {(x,y) for x in [12,13,18,19] for y in range(38,42)}
    todo = [next(iter(occupied))]; seen = set(todo)
    while todo:
        x,y = todo.pop()
        for cell in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if cell in occupied and cell not in seen: seen.add(cell); todo.append(cell)
    assert seen == occupied, (slug, 'disconnected pixels')
    mixed = sum(0 < sum((x+i,y+j) in occupied for i in range(2) for j in range(2)) < 4
                for x in range(0,32,2) for y in range(0,64,2))
    assert mixed > 0
    for name, entries in layout.items():
        panel = next(p for p in entries if p['slug']==slug)
        grid = Image.open(root / f'{name}.png').convert('RGB')
        for y in range(64):
            for x in range(32):
                expected = im.getpixel((x,y))[:3] if (x,y) in occupied else (237,240,235)
                actual = grid.getpixel((panel['x'] + 12*x + 6, panel['y'] + 12*y + 6))
                assert actual == expected, (name, slug, x, y, actual, expected)
                report['gridCellComparisons'] += 1
        svg = (root / f'{name}.svg').read_text()
        assert f'M{panel["x"]+192} {panel["y"]-5}v778' in svg
        for row in [0,10,20,30,40,50,60,64]:
            assert f'M{panel["x"]} {panel["y"]+row*12}h384' in svg
    bbox = im.getbbox()
    report['frames'].append({'slug':slug,'frame':[32,64], 'opaqueBBox':bbox,
        'paintedSize':[bbox[2]-bbox[0],bbox[3]-bbox[1]], 'colors':len(colors),
        'mixedAlpha2x2Blocks':mixed,'anatomyMismatchPairs':0,'connected':True,
        'sha256':hashlib.sha256((root/f'{slug}.png').read_bytes()).hexdigest()})
(root/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
