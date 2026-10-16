"""Read-only cast review evidence. Source-colored plates stay ignored locally."""
from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
EXT = ROOT / 'local-review/overnight-cast-qa'
PIN = '5eff78649e7170a877b961ef0b3da13b81a16038'
ledger = {e['file']: e for e in json.loads((ROOT/'docs/reference-data/emerald-sprite-bounds.json').read_text())}
files = [
    ('Brendan', Path('/tmp/ds1-primary-reference/brendan-walking.png'), 'brendan/walking.png', '731ad5bfd6e6f265508d0efcca0ba42f9dcf5881'),
    ('Man1', Path('/tmp/ds1-primary-reference/man_1.png'), None, '731ad5bfd6e6f265508d0efcca0ba42f9dcf5881'),
    ('May', EXT/'may-walking.png', 'may/walking.png', PIN),
    ('Mom', EXT/'mom.png', 'mom.png', PIN),
    ('Birch', EXT/'prof_birch.png', 'prof_birch.png', PIN),
]
report = {'method': 'actual indexed PNG inspection, index 0 transparent; no emulator evidence', 'files': [], 'missing': []}
board = Image.new('RGB', (960, len(files)*245), '#dedfd6')
d = ImageDraw.Draw(board)
for row, (name,path,key,revision) in enumerate(files):
    if not path.exists():
        report['missing'].append(str(path)); continue
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    s = Image.open(path)
    assert s.mode == 'P' and s.size == (144,32), (path,s.mode,s.size)
    entry = {'name':name, 'path':str(path), 'revision':revision, 'sha256':sha, 'frames':[]}
    if key:
        entry['matchesOlder5effLedgerBytes'] = sha == ledger[key]['sha256']
        assert entry['matchesOlder5effLedgerBytes']
    for col,(facing,index,flip) in enumerate([('S',0,False),('N',1,False),('W',2,False),('E',2,True)]):
        p = s.crop((index*16,0,(index+1)*16,32))
        mask = Image.new('L',p.size); mask.putdata([255 if v else 0 for v in p.get_flattened_data()])
        p = p.convert('RGBA'); p.putalpha(mask)
        if flip: p = p.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        rows = []
        for y in range(32):
            xs = [x for x in range(16) if p.getpixel((x,y))[3]]
            if xs: rows.append({'y':y,'xs':xs})
        entry['frames'].append({'facing':facing,'index':index,'hFlip':flip,'bounds':list(p.getbbox()),'occupiedRows':rows,'contactXs':rows[-1]['xs']})
        x,y=col*240,row*245
        d.text((x+8,y+5),f'{name} {facing} index{index} flip{flip}', fill='#222222')
        board.paste(p,(x+10,y+42),p)
        board.paste(p.resize((96,192),Image.Resampling.NEAREST),(x+60,y+35),p.resize((96,192),Image.Resampling.NEAREST))
    report['files'].append(entry)
EXT.mkdir(parents=True,exist_ok=True)
board.save(EXT/'primary-idles-native-6x.png')
(OUT/'reference-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'files':len(report['files']),'missing':report['missing'],'plate':str(EXT/'primary-idles-native-6x.png')}))
