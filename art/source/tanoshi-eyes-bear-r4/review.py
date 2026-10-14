"""Mechanical labeled comparisons from saved native pixels; no sprite edits."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
ROOT=Path(__file__).resolve().parents[3];D=ROOT/'assets/review/tanoshi-eyes-bear-r4';R=ROOT/'docs/reviews/M1-TN4'
names=['tiny-blush','small-mint','apricot','large-lilac']
for label,bg in [('light','#f4ebd9'),('dark','#29313f'),('world','#80b86b')]:
    plate=Image.new('RGBA',(128,64),bg)
    for i,n in enumerate(names):
        plate.alpha_composite(Image.open(ROOT/'assets/playable/tanoshi-outline'/f'{n}.png').convert('RGBA'),(i*32,0))
        plate.alpha_composite(Image.open(D/f'{n}.png').convert('RGBA'),(i*32,32))
    plate.save(R/f'eyes-before-after-{label}-native.png');plate.resize((1024,512),Image.Resampling.NEAREST).save(R/f'eyes-before-after-{label}-8x.png')
    gridded=plate.resize((1024,512),Image.Resampling.NEAREST);draw=ImageDraw.Draw(gridded)
    for x in range(0,1024,8):draw.line((x,0,x,511),fill='#888888')
    for y in range(0,512,8):draw.line((0,y,1023,y),fill='#888888')
    gridded.save(R/f'eyes-before-after-{label}-grid-8x.png')
meta=json.loads((ROOT/'assets/playable/living/atlas.json').read_text());x,y,w,h=next(a['rect'] for a in meta['assets'] if a['id']=='hero-boy.1')
live=Image.open(ROOT/'assets/playable/living/atlas.png').convert('RGBA').crop((x,y,x+w,y+h));hr3=Image.open(ROOT/'docs/reviews/M1-HR3/hero-south.png').convert('RGBA')
font=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',22)
sheet=Image.new('RGBA',(1024,1640),'#f4ebd9');draw=ImageDraw.Draw(sheet)
def label(y,text):draw.text((12,y),text,font=font,fill='#243b37')
def panel(images,size):
    p=Image.new('RGBA',size,'#f4ebd9')
    for im,pos in images:p.alpha_composite(im,pos)
    return p.resize((size[0]*8,size[1]*8),Image.Resampling.NEAREST)
label(8,'M1.TN4 — unapproved eye / bear review · native pixels enlarged exactly8×')
label(40,'BEFORE: tiny Blush · small Mint · Apricot · large Lilac')
sheet.alpha_composite(panel([(Image.open(ROOT/'assets/playable/tanoshi-outline'/f'{n}.png').convert('RGBA'),(i*32,0)) for i,n in enumerate(names)],(128,32)),(0,70))
label(338,'PROPOSED: paired transparent openings; darker outer silhouettes retained')
sheet.alpha_composite(panel([(Image.open(D/f'{n}.png').convert('RGBA'),(i*32,0)) for i,n in enumerate(names)],(128,32)),(0,368))
label(636,'BEAR: before left / proposed right · same64×36 envelope crop / ground edge')
old=Image.open(ROOT/'assets/playable/tanoshi-outline/bear.png').convert('RGBA').crop((16,44,80,80));new=Image.open(D/'bear.png').convert('RGBA').crop((16,44,80,80))
sheet.alpha_composite(panel([(old,(0,0)),(new,(64,0))],(128,36)),(0,666))
label(966,'Proposed bear / live atlas idle unchanged / HR3 idle review unchanged')
scale=panel([(new,(0,28)),(live,(64,0)),(hr3,(96,0))],(128,64));sheet.alpha_composite(scale,(0,996))
label(1520,'HR3 is the latest reference-led boy work; it is still an idle-art review, not live.')
label(1560,'Actual empty alpha through eyes · no Hero replacement · parent review before publish')
sheet.save(R/'Tanoshi-eyes-bear-and-Hero-direction-8x.png')
print('Labeled comparison and three native/grid backgrounds saved.')
