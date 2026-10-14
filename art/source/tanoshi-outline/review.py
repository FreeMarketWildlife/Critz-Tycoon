"""Mechanical QA views only; never changes an authored sprite."""
from pathlib import Path
from PIL import Image, ImageDraw
import json

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'docs/reviews/M1-TN3/art'
DEST=ROOT/'assets/playable/tanoshi-outline'
inputs=json.loads((ROOT/'art/source/tanoshi-outline/inputs.json').read_text())
ids=['blush','mint','apricot','tiny-blush','small-mint','large-lilac']
for label in ['light','dark']:
    contact=Image.open(OUT/f'contact-{label}-8x.png').convert('RGBA')
    grid=contact.copy();draw=ImageDraw.Draw(grid)
    for p in range(0,1024,8):
        draw.line((p,0,p,1023),fill=(128,128,128,255))
        draw.line((0,p,1023,p),fill=(128,128,128,255))
    grid.save(OUT/f'contact-{label}-grid-8x.png')
plate=Image.new('RGBA',(192,64),'#f4ebd9')
for i,name in enumerate(ids):
    plate.alpha_composite(Image.open(ROOT/inputs[name]['original']).convert('RGBA'),(i*32,0))
    plate.alpha_composite(Image.open(DEST/f'{name}.png').convert('RGBA'),(i*32,32))
plate.resize((1536,512),Image.Resampling.NEAREST).save(OUT/'all-variants-before-after-8x.png')
bear=Image.new('RGBA',(192,96),'#f4ebd9')
bear.alpha_composite(Image.open(ROOT/inputs['bear']['original']).convert('RGBA'),(0,0))
bear.alpha_composite(Image.open(DEST/'bear.png').convert('RGBA'),(96,0))
bear.resize((1536,768),Image.Resampling.NEAREST).save(OUT/'bear-before-after-8x.png')
Image.open(OUT/'contact-light-8x.png').save(OUT/'Tanoshi-sizes-and-route-bear-8x.png')
print('Native, grid, before/after and final Library sheet assembled without editing sprites.')
