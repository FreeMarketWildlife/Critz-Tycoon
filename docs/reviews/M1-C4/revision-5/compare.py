"""Recover this user-supplied enlarged pixel reference and compose review-only grids.
Usage: python compare.py /path/to/screenshot.png /absolute/external/output/directory
Reference-containing outputs MUST stay outside the project/build tree.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
import hashlib, json, sys
repo=Path(__file__).resolve().parents[4]
source=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
assert not out.is_relative_to(repo), 'Reference artwork must remain outside the shipped project'
out.mkdir(parents=True,exist_ok=True)
im=Image.open(source).convert('RGB')
assert im.size==(454,768)
bg=(14,17,19); palette={};rows=[]; source_checks=0
for y in range(64):
    row=''
    for x in range(32):
        sx=-18+16*x+8;sy=-311+16*y+8
        if 1<=sx<453 and 1<=sy<767:
            rgb=im.getpixel((sx,sy))
            assert all(im.getpixel((sx+dx,sy+dy))==rgb for dx in [-1,0,1] for dy in [-1,0,1]),(x,y)
            source_checks+=9
        else:rgb=bg
        if rgb==bg:row+='.'
        else:
            if rgb not in palette:palette[rgb]=chr(65+len(palette))
            row+=palette[rgb]
    rows.append(row)
ref={'slug':'brendan-reference','title':'BRENDAN · YOUR REFERENCE','subtitle':'26 × 42 painted · screenshot reconstruction','frame':[32,64], 'rows':rows,
    'palette':{k:'#%02x%02x%02x'%rgb for rgb,k in palette.items()},'referenceOnly':True,
    'screenshotSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'recovery':{'pitch':16,'frameOriginInScreenshot':[-18,-311], 'sampling':'3×3 center block, all nine values identical', 'sampleChecks':source_checks,
    'limitation':'Exact recovered flat-cell pattern/colors; screenshot edge blur is not reproduced. This supplied refined version is not asserted to be an unmodified Emerald ROM sprite.'}}
assert len(palette)==13
(out/'brendan-reference.json').write_text(json.dumps(ref,indent=2)+'\n')
models=[ref]
for slug in ['a-afro','b-flat-top','c-twists','d-cornrows']:
    model=json.loads((repo/f'docs/reviews/M1-C4/revision-4/{slug}.json').read_text())
    models.append(model)
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
boldpath='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(n,bold=False):return ImageFont.truetype(boldpath if bold else fontpath,n)
def native(m):
    r=Image.new('RGBA',(32,64))
    for y,row in enumerate(m['rows']):
        for x,k in enumerate(row):
            if k!='.':r.putpixel((x,y),tuple(bytes.fromhex(m['palette'][k][1:]))+(255,))
    return r
natives=[native(m) for m in models]
natives[0].save(out/'brendan-reference-32x64.png')
assert natives[0].getbbox()==(3,20,29,62)
for m,r in zip(models[1:],natives[1:]):
    old=Image.open(repo/f'docs/reviews/M1-C4/revision-4/{m["slug"]}.png').convert('RGBA')
    assert r.tobytes()==old.tobytes(), 'Hero pixels must remain unchanged'
report={'source':ref['recovery'],'sourceSHA256':ref['screenshotSHA256'],'referenceColors':13,'heroesUnchanged':True,'nativeCellsVerified':4*32*64,'gridCellsVerified':0,'figures':[]}
for m,r in zip(models,natives):
    report['figures'].append({'id':m['slug'],'bbox':r.getbbox(),'sha256RGBA':hashlib.sha256(r.tobytes()).hexdigest()})
for name,startrow in [('five-character-grid',0),('five-character-detail-grid',20)]:
    z=12;stride=446;x0=46;y0=214;h=(64-startrow)*z;W=2250;H=y0+h+90
    plate=Image.new('RGB',(W,H),'#faf7ef');d=ImageDraw.Draw(plate)
    d.text((38,24),'BRENDAN + FOUR UNCHANGED HERO OPTIONS',font=font(29,True),fill='#253438')
    d.text((38,66),'Same pixel scale · one square = one native pixel · pink = x16 symmetry · blue = every 10 rows',font=font(22),fill='#253438')
    if startrow:d.text((38,98),'Rows 20–64 shown; empty rows 0–19 omitted equally for all five. Full frames: 32×64.',font=font(18),fill='#536165')
    for i,(m,r) in enumerate(zip(models,natives)):
        x=x0+stride*i;center=x+16*z
        title=m['title'];d.text((center,y0-58),title,font=font(19,True),fill='#253438',anchor='mm')
        subtitle='Screenshot pixels' if i==0 else m['outfit']
        d.text((center,y0-34),subtitle,font=font(16),fill='#253438',anchor='mm')
        d.rectangle((x,y0,x+32*z,y0+h),fill='#edf0eb')
        crop=r.crop((0,startrow,32,64)).resize((384,h),Image.Resampling.NEAREST)
        plate.paste(crop,(x,y0),crop)
        # Fine lines stay translucent over art, so they remain countable without hiding colors.
        overlay=Image.new('RGBA',plate.size);g=ImageDraw.Draw(overlay)
        for col in range(33):g.line((x+col*z,y0,x+col*z,y0+h),fill=(88,103,106,65),width=1)
        for row in range(startrow,65):
            yy=y0+(row-startrow)*z;major=row%10==0 or row==64
            g.line((x,yy,x+384,yy),fill=(71,110,128,210) if major else (88,103,106,65),width=2 if major else 1)
            if major:d.text((x-8,yy),str(row),font=font(16),fill='#253438',anchor='rm')
        g.line((center,y0-5,center,y0+h+5),fill=(204,60,131,255),width=2)
        plate=Image.alpha_composite(plate.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(plate)
        for col in [0,10,16,20,30,32]:d.text((x+col*z,y0-11),str(col),font=font(13),fill='#253438',anchor='mm')
        d.text((center,y0+h+29),'32 × 64 frame · 12× display',font=font(17),fill='#253438',anchor='mm')
        for yy in range(startrow,64):
            for xx in range(32):
                p=r.getpixel((xx,yy));expected=p[:3] if p[3] else (237,240,235)
                assert plate.getpixel((x+xx*z+6,y0+(yy-startrow)*z+6))==expected
                report['gridCellsVerified']+=1
    plate.save(out/(name+'.png'))
(out/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
