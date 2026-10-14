"""Assemble two imagegen-authored expression bands across the shared family.

Crop/nearest/palette correspondence only. No eye cells, masks or outlines are
drawn. Existing source-derived interior masks protect the accepted contour.
"""
from pathlib import Path
from PIL import Image
from collections import deque
import json,hashlib

ROOT=Path(__file__).resolve().parents[3]
S=ROOT/'art/source/tanoshi-eyes-bear-r4';D=ROOT/'assets/review/tanoshi-eyes-bear-r4';R=ROOT/'docs/reviews/M1-TN4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ids=['blush','mint','apricot','tiny-blush','small-mint','large-lilac']
inputs=json.loads((S/'inputs.json').read_text())
reports=json.loads((R/'export-checks.json').read_text())
blush=Image.open(D/'blush.png').convert('RGBA');tall=blush.crop((12,14,20,19));tall.save(S/'tall-face-master-native.png')
short=tall.resize((8,4),Image.Resampling.NEAREST);short.save(S/'short-face-master-native.png')
blush_palette=json.loads((S/'blush.pixels.json').read_text())['palette'];apricot_palette=json.loads((S/'apricot.pixels.json').read_text())['palette']
styles={'mint':('tall',(12,14)),'apricot':('short',(12,15)),'tiny-blush':('short',(12,19)),'small-mint':('tall',(12,17)),'large-lilac':('tall',(12,14))}
images={'blush':blush}

def palette_colors(data):return [(0,0,0,0),*[tuple(bytes.fromhex(c[1:]))+(255,) for c in data[1:]]]
def holes(im):
    todo={(x,y) for y in range(32) for x in range(32) if not im.getpixel((x,y))[3]};found=[]
    while todo:
        q=deque([todo.pop()]);area=[]
        while q:
            x,y=q.popleft();area.append((x,y))
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    v=x+dx,y+dy
                    if v in todo:todo.remove(v);q.append(v)
        if any(x in [0,31] or y in [0,31] for x,y in area) or min(y for x,y in area)>=24:continue
        found.append({'cells':len(area),'bounds':[min(x for x,y in area),min(y for x,y in area),max(x for x,y in area)+1,max(y for x,y in area)+1]})
    return sorted(found,key=lambda a:a['bounds'][0])

for name,(style,position) in styles.items():
    data=json.loads((S/f'{name}.pixels.json').read_text());old_info=data['provenance'];allowed=set(map(tuple,old_info['allowedNativeCells']))
    original=Image.open(ROOT/inputs[name]['source']).convert('RGBA');native=original.copy();dest_palette=palette_colors(data['palette'])
    band=tall if style=='tall' else short;source_palette=palette_colors(blush_palette)
    for y in range(band.height):
        for x in range(band.width):
            target=x+position[0],y+position[1]
            if target not in allowed:continue
            pixel=band.getpixel((x,y));k=0 if pixel[3]<128 else min(range(1,len(source_palette)),key=lambda i:sum((a-b)**2 for a,b in zip(pixel[:3],source_palette[i][:3])))
            native.putpixel(target,dest_palette[k])
    native.save(D/f'{name}.png');images[name]=native
    source_raw='generated-blush.png'
    provenance={'id':name,'method':'Imagegen-authored shared expression crop, native assembly and existing three-material correspondence; no procedural eye drawing','originalSHA256':inputs[name]['sha256'],'master':str((S/f'{style}-face-master-native.png').relative_to(ROOT)),'masterSHA256':sha(S/f'{style}-face-master-native.png'),'masterRawSource':str((S/source_raw).relative_to(ROOT)),'masterRawSHA256':sha(S/source_raw),'masterRecipe':'Blush first-pass native crop[12,14,20,19]' if style=='tall' else 'Blush tall8x5 face master nearest resized to8x4; no alpha cells painted','masterSourcePalette':blush_palette,'faceRectangle':old_info['faceRectangle'],'allowedNativeCells':old_info['allowedNativeCells'],'placement':list(position),'paintedBounds':list(native.getbbox()),'eyeHoles':holes(native),'changedCells':[[x,y] for y in range(32) for x in range(32) if native.getpixel((x,y))!=original.getpixel((x,y))],'nativeSHA256':sha(D/f'{name}.png')}
    data.update(rows=[[dest_palette.index(native.getpixel((x,y))) for x in range(32)] for y in range(32)],provenance=provenance)
    (S/f'{name}.pixels.json').write_text(json.dumps(data,indent=2)+'\n')
    reports['assets']=[provenance if a['id']==name else a for a in reports['assets']]
atlas=Image.new('RGBA',(192,32))
for i,name in enumerate(ids):atlas.paste(images[name],(i*32,0))
atlas.save(D/'atlas.png');atlas.resize((1536,256),Image.Resampling.NEAREST).save(R/'all-variants-8x.png')
(R/'export-checks.json').write_text(json.dumps(reports,indent=2)+'\n')
for label,color in [('light','#f4ebd9'),('dark','#29313f'),('world','#80b86b')]:
    plate=Image.new('RGBA',(128,32),color)
    for i,n in enumerate(['tiny-blush','small-mint','apricot','large-lilac']):plate.alpha_composite(images[n],(i*32,0))
    plate.resize((1024,256),Image.Resampling.NEAREST).save(R/f'after-eyes-{label}-8x.png')
(S/'selected-masters.json').write_text(json.dumps({'task':'M1.TN4','tall':'Existing regular Blush has the clean paired2x3 construction; imagegen r1 reproduces it exactly in the protected native face.','short':'Same authored tall8x5 face band nearest resized to8x4, yielding paired2x2 openings without painting alpha.','otherAttempts':'Retained as iteration evidence; first-pass holes shrank/shifted. Face-crop trials added unwanted header gaps or dark bridges. Reuse one coherent intact authored face master and existing material correspondence.','noAlphaCarving':True,'palettes':'Existing material correspondence; only permitted interior cells changed.','bear':'Imagegen bear r1 aspect-preserving envelope, unchanged registration.'},indent=2)+'\n')
print(json.dumps([{'id':n,'eyes':holes(images[n])} for n in ids],indent=2))
