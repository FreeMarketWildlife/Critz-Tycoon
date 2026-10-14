"""Independent saved-PNG preservation and authored-outline validation."""
from pathlib import Path
from PIL import Image
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'art/source/tanoshi-outline'
DEST=ROOT/'assets/playable/tanoshi-outline'
REVIEW=ROOT/'docs/reviews/M1-TN3/art'
inputs=json.loads((SOURCE/'inputs.json').read_text())
manifest=json.loads((DEST/'atlas.json').read_text())
atlas=Image.open(DEST/'atlas.png').convert('RGBA')
assert atlas.size==(192,32)
assert [a['id'] for a in manifest['assets']]==['blush','mint','apricot','tiny-blush','small-mint','large-lilac']
checks=[]
for name,info in inputs.items():
    old_path=ROOT/info['original'];old=Image.open(old_path).convert('RGBA')
    assert hashlib.sha256(old_path.read_bytes()).hexdigest()==info['sha256']
    im=Image.open(DEST/f'{name}.png').convert('RGBA')
    data=json.loads((SOURCE/f'{name}.pixels.json').read_text())
    palette=[(0,0,0,0),*[tuple(bytes.fromhex(c[1:]))+(255,) for c in data['palette'][1:]]]
    assert im.tobytes()==bytes(v for row in data['rows'] for k in row for v in palette[k])
    provenance=data['provenance']
    guide_path=ROOT/provenance['generated']
    assert hashlib.sha256(guide_path.read_bytes()).hexdigest()==provenance['generatedSha256']
    guide=Image.open(guide_path).convert('RGBA')
    bounds=provenance['targetBox'];left,top,right,bottom=bounds
    samples=guide.crop(provenance['generatedCrop']).resize((right-left,bottom-top),Image.Resampling.NEAREST)
    material=palette[1:]
    assert im.size==old.size and im.getbbox()==old.getbbox()
    assert im.getchannel('A').tobytes()==old.getchannel('A').tobytes()
    assert set(im.getchannel('A').get_flattened_data())=={0,255}
    changed=[]
    for y in range(im.height):
        for x in range(im.width):
            before,after=old.getpixel((x,y)),im.getpixel((x,y))
            if before!=after:
                assert before[3]==after[3]==255 and after==palette[1]
                sample=samples.getpixel((x-left,y-top))[:3]
                nearest=min(range(len(material)),key=lambda k:sum((a-b)**2 for a,b in zip(sample,material[k][:3])))
                assert nearest==0,(name,x,y,'change lacks generated dark RGB cue')
                changed.append([x,y])
    assert changed,(name,'outline did not strengthen')
    assert set(p for p in im.get_flattened_data() if p[3])==set(p for p in old.get_flattened_data() if p[3])
    before=sum(p==palette[1] for p in old.get_flattened_data());after=sum(p==palette[1] for p in im.get_flattened_data())
    assert after>=before*1.5,(name,"dark ink did not increase by50%")
    if name!='bear':
        a=next(a for a in manifest['assets'] if a['id']==name);x,y,w,h=a['rect']
        assert a['anchor']==a['sortAnchor']==[16,32]
        assert im.tobytes()==atlas.crop((x,y,x+w,y+h)).tobytes()
        assert not any(im.crop((0,30,32,32)).getchannel('A').get_flattened_data())
    else:
        old_meta=json.loads((ROOT/'assets/playable/tanoshi-sizes/bear.json').read_text())
        meta=json.loads((DEST/'bear.json').read_text())
        for k in ['size','footprint','footprintCells','drawOffsetFromFootprintPixels','groundAnchor','sortAnchor','transparentRows','lowerContactX','contactRule']:
            assert meta[k]==old_meta[k]
    checks.append({'id':name,'nativeSize':list(im.size),'bounds':list(im.getbbox()),'binaryAlpha':True,
                   'alphaSilhouetteAndEveryEyeHoleExact':True,'paletteExact':True,'onlyExistingFillToDarkChanges':True,
                   'generatedSourceHashAndEveryChangedMaterialCueVerified':True,
                   'darkPixelsBefore':before,'darkPixelsAfter':after,'addedInkPixels':len(changed),
                   'sha256':hashlib.sha256((DEST/f'{name}.png').read_bytes()).hexdigest()})
active=['tiny-blush','small-mint','apricot','large-lilac']
hero_meta=json.loads((ROOT/'assets/playable/living/atlas.json').read_text())
hero_rect=next(a['rect'] for a in hero_meta['assets'] if a['id']=='hero-boy.1')
x,y,w,h=hero_rect
hero=Image.open(ROOT/'assets/playable/living/atlas.png').convert('RGBA').crop((x,y,x+w,y+h))
for label,bg in [('light','#f4ebd9'),('dark','#29313f')]:
    plate=Image.new('RGBA',(128,128),bg)
    for i,name in enumerate(active):plate.alpha_composite(Image.open(DEST/f'{name}.png').convert('RGBA'),(i*32,0))
    plate.alpha_composite(Image.open(DEST/'bear.png').convert('RGBA'),(0,32))
    plate.alpha_composite(hero,(96,48))
    assert plate.tobytes()==Image.open(REVIEW/f'contact-{label}-native.png').convert('RGBA').tobytes()
    assert plate.resize((1024,1024),Image.Resampling.NEAREST).tobytes()==Image.open(REVIEW/f'contact-{label}-8x.png').convert('RGBA').tobytes()
# Whole protected directories stay identical to the accepted source commit.
protected=['assets/playable/tanoshi','assets/playable/tanoshi-sizes','assets/playable/living','assets/playable/characters','references/tanoshi']
paths=[]
for directory in protected:
    for p in (ROOT/directory).rglob('*'):
        if not p.is_file():continue
        rel=str(p.relative_to(ROOT));old=subprocess.check_output(['git','show','8e7a2869238d9fec1fc7a19d0d62892a09424cd3:'+rel],cwd=ROOT)
        assert p.read_bytes()==old,rel;paths.append(rel)
report={'task':'M1.TN3','checks':checks,'unchangedProtectedFiles':paths,'bearFootprintAndRegistrationExact':True,
        'bothContactSheetsExactNativeAssemblyAndEightfoldPixels':True,
        'heroAndOriginalPetReferencesUnchanged':True,'chatGPTPetToolsCalled':False,
        'note':'Alpha equality proves every prior eye-hole cell and contour exact. Outline changes are only generated dark-material additions, never alpha edits.'}
(REVIEW/'native-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'assets':len(checks),'protectedFiles':len(paths),'allPassed':True},indent=2))
