"""Original swept-twist head. No reference raster is used for authoring."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
root=Path(__file__).resolve().parents[3]
out=root/'docs/reviews/M1-HR10-HEAD'
# Reuse the original layered face/ears/eyes before the old foreground hair.
# This prefix only constructs pixels in memory; it executes no file exports.
author=(root/'art/source/hero-redesign-r6/build.py').read_text()
ns={'__file__':str(root/'art/source/hero-redesign-r6/build.py')}
exec(compile(author.split("shape('hair'")[0],'<original-face-layers>','exec'),ns)
im=ns['im'];d=ns['d'];parts=ns['parts'];P=ns['P']
shape=ns['shape'];fill=ns['fill'];line=ns['line']
# Broad continuous sweep, stepped temples and grouped locks. The short raised
# crest belongs to the hair design; no cap peak is converted to a skull target.
backing=im.copy()
contour=[(19,23),(21,22),(22,24),(23,25),(24,26),(24,28),
 (25,30),(25,31),(26,32),(26,34),(27,35),
 (26,36),(25,36),(24,35),(23,37),
 (21,36),(19,37),(17,35),(16,37),(14,36),(12,37),(10,35),
 (8,37),(6,36),(5,35),(5,32),(6,30),(7,29),(8,28),(9,27),
 (11,26),(13,25),(16,25),(18,24)]
shape('hair',contour,'h')
ImageDraw.Draw(parts['hair']).line(contour+[contour[0]],fill=1)
# Three interlocking color masses, rather than outlined individual strands.
fill([(9,27),(13,25),(18,24),(21,24),(22,26),(19,28),
 (14,28),(11,30),(7,31),(6,30)],'m')
fill([(21,28),(24,28),(26,31),(26,34),(24,35),(22,33),
 (19,34),(19,31)],'m')
fill([(5,32),(8,31),(11,30),(12,32),(10,35),(7,34),(5,35)],'m')
line([(11,27),(14,26),(17,26)],'l')
line([(15,29),(15,32),(14,34)],'h')
line([(20,30),(20,32),(19,34)],'h')
line([(23,30),(24,31)],'l')
# Texture stays inside its authored mass. Reassert the continuous outer edge.
for y in range(64):
 for x in range(32):
  if not parts['hair'].getpixel((x,y)):im.putpixel((x,y),backing.getpixel((x,y)))
d.line(contour+[contour[0]],fill=P['O'])
head=Image.new('RGBA',(32,64));head.paste(im.crop((0,0,32,46)),(0,0))
head.save(out/'head-forward.png')
(Path(__file__).parent/'head-masks.json').write_text(json.dumps({k:[int(v) if i//32<46 else 0 for i,v in enumerate(m.get_flattened_data())] for k,m in parts.items() if k in ('hair','face','eyes','leftEar','rightEar','jawContact','mouth','nose')},separators=(',',':'))+'\n')
