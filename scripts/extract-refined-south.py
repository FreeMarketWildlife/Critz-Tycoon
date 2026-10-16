"""Extract the authorized supplied south reference; input GIF stays external."""
import sys
from PIL import Image
from pathlib import Path
import hashlib,json
src=Path(sys.argv[1])
assert hashlib.sha256(src.read_bytes()).hexdigest()=='5fe7935d9f90afbd23530b7a7f57a5147cd1c5142734e0b4306ca71f5666015e'
out=Path('sprite-editor/assets/refined-south');im=Image.open(src);frames=[]
for i in range(im.n_frames):
 im.seek(i);crop=im.convert('RGBA').crop((0,0,128,192));native=crop.resize((32,48),Image.Resampling.NEAREST)
 assert native.resize((128,192),Image.Resampling.NEAREST).tobytes()==crop.tobytes()
 # The source's solid background is not character art. Exact RGB retained at all non-background sites.
 bg=native.getpixel((0,0));data=[(0,0,0,0) if p==bg else p for p in native.get_flattened_data()];native.putdata(data)
 canvas=Image.new('RGBA',(32,64));canvas.paste(native,(0,16));path=out/f'frame-{i}.png';canvas.save(path)
 frames.append({'file':path.name,'durationMs':im.info.get('duration'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
assert len(frames)==8 and all(f['durationMs']==100 for f in frames)
(out/'manifest.json').write_text(json.dumps({'kind':'supplied-refined-south','sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop':[0,0,128,192],'displayDivisor':4,'translation':[0,16],'anchor':[16,64],'backgroundRemoval':'Exact top-left source background color only; non-background RGBA unchanged','order':['A','A','P','P','C','C','P','P'],'observedIdle':False,'frames':frames},indent=2)+'\n')
