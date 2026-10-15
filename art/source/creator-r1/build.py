"""Freeze NB3's actual independent body/costume pixels for the review-only creator.
No new poses, hidden-body changes or runtime assets. Palette indexing is lossless.
"""
from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[3]
nb=json.loads((root/'art/source/hero-neutral-r3/construction.json').read_text())
ref=json.loads((root/'art/source/hero-directional-r14/construction.json').read_text())
palette=[None];lookup={};poses={}
def encode(im):
 out=[]
 for p in im.convert('RGBA').get_flattened_data():
  if not p[3]:out.append(0);continue
  c='#%02x%02x%02x'%p[:3]
  if c not in lookup:lookup[c]=len(palette);palette.append(c)
  out.append(lookup[c])
 return out
for dr in ('south','north','west','east'):
 poses[dr]={}
 for po in ('idle','A','P','C'):
  folder=root/f'docs/reviews/M1-NB3/{dr}-{po}';entry=nb['directions'][dr][po];features=ref['directions'][dr][po]['commonFeatureRegistration']
  names=['body-render-with-selected-skin','neutral-body']+['overlay-'+n for n in ('hair','shirt','shorts','shoes','pack','straps')]
  layers={name:encode(Image.open(folder/f'{name}.png')) for name in names}
  # Explicit immutable view registration. Optional features stay on existing skin,
  # inside the face contour; no added profile protrusion or far-ear invention.
  dy=-2 if po=='P' else 0
  nose=[] if dr=='north' else [[15,41+dy]] if dr=='south' else [[8,40+dy]] if dr=='west' else [[23,40+dy]]
  mouth=[] if dr=='north' else [[15,43+dy],[16,43+dy]] if dr=='south' else [[9,43+dy]] if dr=='west' else [[22,43+dy]]
  poses[dr][po]={'layers':layers,'expected':encode(Image.open(folder/'recomposed-hero.png')),'eyes':features['eyes']['cells'],'ears':features['ears']['cells'],'nose':nose,'mouth':mouth,'anchor':[16,64],'dy':dy}
data={'task':'M1.CC1','source':'NB3 / PS1 8726c9a; original registered feature evidence HR14','width':32,'height':64,'palette':palette,'order':nb['order'],'poses':poses}
(root/'character-creator/data.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
print('CC1 actual body and six appearance layers,16 poses;',len(palette)-1,'lossless colors')
