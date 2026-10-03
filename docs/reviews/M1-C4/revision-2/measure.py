"""Read-only analysis of a locally supplied pinned Emerald sheet and native PNGs.
Usage: python measure.py /path/to/brendan/walking.png
Reference artwork is never exported or copied into this review directory.
"""
from pathlib import Path
from PIL import Image
import sys, json, hashlib

root = Path(__file__).resolve().parent
source = Path(sys.argv[1])
sha = hashlib.sha256(source.read_bytes()).hexdigest()
assert sha == 'f33ec07a5fd17f4422455f8bc55cd3d3522fa65c3bf740ecbdc00da705eaa0d1'
im = Image.open(source)
assert im.mode == 'P' and im.size == (144, 32)

def bbox(points):
    return [min(x for x, y in points), min(y for x, y in points),
            max(x for x, y in points) + 1, max(y for x, y in points) + 1]

regions = {
    'full figure': [0, 0, 16, 32],
    'headwear / original hair envelope': [0, 10, 16, 18],
    'face and ear band, with borders': [0, 18, 16, 23],
    'head and face combined': [0, 10, 16, 23],
    'shoulder row': [0, 23, 16, 24],
    'central torso region': [5, 23, 11, 28],
    'left arm and hand region': [1, 23, 5, 27],
    'right arm and hand region': [11, 23, 15, 27],
    'left distal limb region': [1, 24, 5, 27],
    'right distal limb region': [11, 24, 15, 27],
    'shorts and feet band': [3, 28, 13, 31],
    'left leg and shoe region': [3, 28, 7, 31],
    'right leg and shoe region': [9, 28, 13, 31],
}
models = [json.loads((root / f'hero-{w}x{h}.json').read_text()) for w,h in [(16,32),(32,64)]]
measurements=[]
for name, (l,t,r,b) in regions.items():
    pts=[(x,y) for y in range(t,b) for x in range(l,r) if im.getpixel((x,y)) != 0]
    ref=bbox(pts); target=[v*2 for v in ref];actuals=[];areas=[]
    for scale,model in zip([1,2],models):
        p=[(x,y) for y in range(t*scale,b*scale) for x in range(l*scale,r*scale) if model['rows'][y][x]!='.']
        actuals.append(bbox(p));areas.append(len(p))
    assert actuals==[ref,target],name
    measurements.append({'region':name,'annotationWindow': [l,t,r,b], 'referenceBBox':ref,'referenceSize':[ref[2]-ref[0],ref[3]-ref[1]],'target2xBBox':target,'actual1xBBox':actuals[0],'actual2xBBox':actuals[1],'bboxDeviation':[0,0,0,0],'referenceOccupiedCells':len(pts),'actualOccupiedCells':areas})

eyes=[(x,y) for y in [19,20] for x in range(4,12) if im.getpixel((x,y))==8]
assert eyes==[(6,19),(9,19),(6,20),(9,20)]
body_shape=[]
for y in range(18,31):
    mask=''.join('#' if im.getpixel((x,y)) else '.' for x in range(16))
    assert mask==''.join('#' if c!='.' else '.' for c in models[0]['rows'][y])
    body_shape.append(mask)

for scale,model in zip([1,2],models):
    expected={(x*scale+dx,y*scale+dy) for x,y in eyes for dx in range(scale) for dy in range(scale)}
    actual={(x,y) for y,row in enumerate(model['partLabels']) for x,k in enumerate(row) if k=='eyes'}
    assert expected==actual

out={'reference':{'repository':'pret/pokeemerald','revision':'5eff78649e7170a877b961ef0b3da13b81a16038','path':'graphics/object_events/pics/people/brendan/walking.png','sha256':sha,'frame':0,'direction':'south','pose':'idle','method':'Palette index != 0; manually identified semantic regions, half-open coordinates. Source-only, no emulator observation.'},'measurements':measurements,'referenceEyePixels':eyes,'referenceBodyMaskFromRow18':body_shape,'groundAnchor':{'reference':[8,32],'target':[16,64],'actual':[16,64]},'lastFootRow':{'reference':30,'targetRows':[60,61],'actual':61},'limitations':['The hidden skull and exact anatomical boundaries beneath headwear/clothes cannot be recovered from this raster. Symmetric construction is required for Critz; it is not an observed hidden bone shape.','Arm/hand and distal-limb windows include their outline and sleeve/glove overlap. Original Hero clothing changes their color/material partition without changing the measured occupied silhouette.','Original afro occupies the measured headwear envelope but has a different contour and fill area (78 vs 66 cells at 1x). This is an explicit hairstyle adaptation, not exact copying of the pointed cap.','The newly supplied montage is a visual preference reference, not a provenance-verified Emerald source sheet.']}
(root/'measurements.json').write_text(json.dumps(out,indent=2)+'\n')
lines=['# Measured front-idle construction — revision 2','','All coordinates are half-open `(left, top, right, bottom)`. Measurements use the pinned source, not inferred screenshot scaling.','','| Annotated region | Reference size | 2× target size | Actual 2× | Bounds deviation |','| --- | --- | --- | --- | --- |']
for m in measurements:
    w,h=m['referenceSize'];lines.append(f"| {m['region']} | {w}×{h} | {2*w}×{2*h} | {2*w}×{2*h} | 0 |")
lines+=['','Eyes: `(6,19)…(6,20)` and `(9,19)…(9,20)` become rectangles `[12,38,14,42]` and `[18,38,20,42]`. Actual labeled eye masks match exactly.','', 'Anchor: `(8,32)` → `(16,64)`. Idle final row: 30 → 60–61. Actual last row: 61.','', 'The face/ear and complete body occupancy from reference rows 18–30 matches the 1× Hero exactly and is doubled exactly in the 2× Hero. Costume, skin, palette and hairstyle are original.','','## Definitions and deviations','']
lines += ['- '+s for s in out['limitations']]
lines += ['', 'Source: [pinned Brendan sheet](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/graphics/object_events/pics/people/brendan/walking.png). The complete source revision, SHA-256, bounds and occupied-cell counts are in [measurements.json](measurements.json).', '']
(root/'MEASUREMENTS.md').write_text('\n'.join(lines))
print('PASS: 13 region targets, eye rectangles, body occupancy, anchor and foot baseline match.')
