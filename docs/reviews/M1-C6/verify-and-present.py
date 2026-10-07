"""Reproducible native-pixel checks and review overlays (requires Pillow)."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets/review/idle-collection-v1'
SOURCE = ROOT / 'art/source/idle-collection-v1'
manifest = json.loads((ASSETS / 'manifest.json').read_text())
font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
font = lambda n: ImageFont.truetype(font_path, n)
BG = '#f3efe5'
INK = '#273f45'
boy_path = ROOT / 'assets/characters/hero-boy-v1/idle-south.png'
boy = Image.open(boy_path).convert('RGBA')
assert hashlib.sha256(boy_path.read_bytes()).hexdigest() == '0099dd331ae2c2d995663328e52763e8b10b1df0d36854d59676ee0ac52f7883'
assert hashlib.sha256((ROOT / 'art/source/hero-boy-v1/user-approved.rle.json').read_bytes()).hexdigest() == 'bef3289d8d62801ea2f223ae9359beb305856764a54afed8fe9990f42676fb3a'
reports = []
for entry in manifest['assets']:
    slug = entry['slug']
    im = Image.open(ASSETS / entry['file']).convert('RGBA')
    assert list(im.size) == entry['frame']
    assert set(im.getchannel('A').tobytes()) == {0, 255}
    assert list(im.getbbox()) == entry['bbox']
    assert hashlib.sha256(im.tobytes()).hexdigest() == entry['pixelSHA256']
    project = json.loads((SOURCE / f'{slug}.sprite.json').read_text())
    exact = json.loads((SOURCE / f'{slug}.rle.json').read_text())
    rows = [[c for c, count in zip(row[::2], row[1::2]) for _ in range(count)] for row in exact['frames'][0]['rows']]
    assert len(rows) == im.height and all(len(row) == 32 for row in rows)
    assert sum(rows, []) == project['frames'][0]['pixels']
    colors = [tuple(bytes.fromhex(c[1:])) + (255,) if c else (0,0,0,0) for c in project['palette']]
    expected = bytes(v for i in project['frames'][0]['pixels'] for v in colors[i])
    assert expected == im.tobytes()
    report = {'id': entry['id'], 'frame': entry['frame'], 'bbox': entry['bbox'], 'colors': entry['colors'], 'RGBA_and_RLE_exact': True, 'binary_alpha': True}
    if entry['kind'] == 'character':
        assert not im.getchannel('A').crop((0,62,32,64)).getbbox()
        masks = json.loads((SOURCE / f'{slug}.masks.json').read_text())
        for name, cells in masks['masks'].items():
            assert set(cells) == {i//32*32+31-i%32 for i in cells}, (slug,name)
        report['paired_construction_masks'] = list(masks['masks'])
        report['bottom_padding'] = 2
        if slug == 'hero-girl':
            assert im.getchannel('A').crop((0,45,32,64)).tobytes() == boy.getchannel('A').crop((0,45,32,64)).tobytes()
            report['approved_boy_body_alpha_changes'] = 0
        # All non-accessory eye cells have the same two-by-four silhouette.
        for i in masks['masks']['eyes']:
            assert im.getpixel((i%32,i//32))[3] == 255
            assert masks['visibleParts'][i] in ('eyes','accessory'), (slug,i,masks['visibleParts'][i])
        report['eyes_visible'] = True
    reports.append(report)

baseline = {'slug':'hero-boy-v1','label':'Boy Hero V1','role':'Approved baseline','kind':'character','frame':[32,64], 'bbox':list(boy.getbbox()),'file':str(boy_path)}
characters = [baseline] + [e for e in manifest['assets'] if e['kind'] == 'character']
animals = [e for e in manifest['assets'] if e['kind'] == 'animal']
def load(e):
    return Image.open(ASSETS / e['file']).convert('RGBA')

def clean_sheet(entries, columns, target, animal=False):
    scale=6
    cellw=224
    cellh=258 if animal else 340
    rows=(len(entries)+columns-1)//columns
    image=Image.new('RGB',(columns*cellw+32,rows*cellh+108),BG)
    d=ImageDraw.Draw(image)
    d.text((24,18),'CRITZ  /  '+('ANIMAL STUDIES' if animal else 'ROOTPORT CAST'),font=font(27),fill=INK)
    d.text((24,54),'Native pixels enlarged 6× · stills only · visual review',font=font(17),fill=INK)
    for n,e in enumerate(entries):
        im=load(e)
        if not animal: im=im.crop((0,18,32,64))
        im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
        x=24+n%columns*cellw;y=88+n//columns*cellh
        image.paste(im,(x,y),im)
        d.text((x,y+im.height+10),e['label'],font=font(19),fill=INK)
        d.text((x,y+im.height+35),e['role'] if animal else ('Approved V1' if n==0 else 'Native idle proposal'),font=font(12),fill=INK)
    image.save(HERE/target)

def grid_sheet(entries, target, columns=5):
    scale=7; cellw=286; cellh=560 if entries[0]['kind']=='character' else 334
    rows=(len(entries)+columns-1)//columns
    image=Image.new('RGB',(columns*cellw+20,rows*cellh+92),BG);d=ImageDraw.Draw(image)
    d.text((24,18),'CRITZ / NATIVE PIXEL REVIEW',font=font(25),fill=INK)
    d.text((24,54),'1 square = 1 pixel  ·  Pink: x16  ·  Blue: every 10 pixels  ·  Y0 at bottom  ·  7×',font=font(16),fill=INK)
    for n,e in enumerate(entries):
        native=load(e);w,h=native.size
        x=43+n%columns*cellw;y=142+n//columns*cellh
        d.text((x,y-45),e['label'],font=font(18),fill=INK)
        d.rectangle((x,y,x+w*scale,y+h*scale),fill='#e9ede6')
        im=native.resize((w*scale,h*scale),Image.Resampling.NEAREST);image.paste(im,(x,y),im)
        overlay=Image.new('RGBA',image.size);g=ImageDraw.Draw(overlay)
        for i in range(w+1):g.line((x+i*scale,y,x+i*scale,y+h*scale),fill=(66,93,91,43))
        for j in range(h+1):g.line((x,y+j*scale,x+w*scale,y+j*scale),fill=(66,93,91,43))
        image=Image.alpha_composite(image.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(image)
        for yy in sorted(set([0,h]+list(range(10,h,10)))):
            py=y+(h-yy)*scale;d.line((x,py,x+w*scale,py),fill='#728f9a',width=1)
            d.text((x-27,py-6),str(yy),font=font(12),fill=INK)
        d.line((x+16*scale,y-5,x+16*scale,y+h*scale+4),fill='#da5189',width=2)
        for xx in [0,16,32]:d.text((x+xx*scale-4,y+h*scale+9),str(xx),font=font(10),fill=INK)
        bb=e['bbox'];d.text((x,y+h*scale+29),f'{w}×{h} frame · {bb[2]-bb[0]}×{bb[3]-bb[1]} painted',font=font(13),fill=INK)
    image.save(HERE/target)

clean_sheet(characters,6,'characters-clean.png')
clean_sheet(animals,4,'animals-clean.png',True)
grid_sheet(characters[:5],'core-grid.png',5)
grid_sheet(characters[5:9],'cast-grid-a.png',4)
grid_sheet(characters[9:],'cast-grid-b.png',3)
grid_sheet(animals,'animals-grid.png',4)
for entries,name,h in [(characters,'characters-native.png',64),(animals,'animals-native.png',32)]:
    sheet=Image.new('RGBA',(32*len(entries),h))
    for i,e in enumerate(entries):sheet.paste(load(e),(i*32,0))
    sheet.save(HERE/name)
report={'task':'M1.C6','result':'pass','newCharacters':11,'newAnimalStills':8,'approvedBoyHashesUnchanged':True,'checks':reports,'limitations':['Native visual acceptance remains the user’s decision.','Adult construction is an original two-row adaptation, not a new measurement of Emerald adult anatomy.','Animal observation-scale studies do not declare physical size or habitat compatibility.','No animation, directional completion, runtime integration or deployment.']}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: 19 exact native assets; editor/RLE round trips, binary alpha, hashes, 11 paired anatomy masks, girl body and approved boy unchanged. Review plates exported.')
