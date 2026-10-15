"""Check immutable before/protected32 front without importing the art builder."""
from pathlib import Path
from PIL import Image
import hashlib,json
R=Path(__file__).resolve().parents[4];B=R/'docs/reviews/M1-H4R1';A=R/'docs/reviews/M1-NCR1';O=Path(__file__).parent;checks=[]
def ck(label,value):
 checks.append({'check':label,'pass':bool(value)})
 if not value:raise AssertionError(label)
manifest=json.loads((O/'h4r1-history-before.json').read_text())
for f in manifest['files']:ck('archived before '+f['path'],hashlib.sha256((R/f['path']).read_bytes()).hexdigest()==f['sha256'])
for po in ['idle','A','P','C']:
 for n in ['master-hero.png','master-bald.png','master-hair.png','master-hair-shadow.png']:
  ck('protected32South '+po+n,(A/('south-'+po)/n).read_bytes()==(B/('south-'+po)/n).read_bytes())
print(json.dumps({'passed':len(checks),'scope':'HistoricalH4R1 fullsource/art bytes and protected32South; final quality/audit separate.'}))
