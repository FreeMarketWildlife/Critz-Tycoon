"""Read-only pixel regression against the source immediately before M1.E3."""
import io,json,hashlib,subprocess,argparse
from pathlib import Path
from PIL import Image
parser=argparse.ArgumentParser();parser.add_argument('--output',default='test-results/terrain-assets.json');args=parser.parse_args()
root=Path(__file__).resolve().parents[1];baseline='e0f1624b81ef90b67e643279223d7b82fe5c985f'
def before(name):return subprocess.check_output(['git','show',f'{baseline}:assets/playable/overworld/{name}'],cwd=root)
old=json.loads(before('master.json'));original=Image.open(io.BytesIO(before('master.png'))).convert('RGBA')
new=json.loads((root/'assets/playable/overworld/master.json').read_text());sheet=Image.open(root/'assets/playable/overworld/master.png').convert('RGBA');by={t['id']:t for t in new['tiles']};checks=[]
assert sheet.size==(new['imageWidth'],new['imageHeight']);assert sheet.width==1024 and sheet.height%32==0
assert set(sheet.getchannel('A').get_flattened_data())=={0,255};checks.append('Master dimensions match metadata; hard native pixels with binary alpha')
def crop(t):return sheet.crop((t['x'],t['y'],t['x']+32,t['y']+32))
for t in old['tiles']:
 n=by[t['id']];assert (n['index'],n['x'],n['y'])==(t['index'],t['x'],t['y']);assert crop(n).tobytes()==original.crop((t['x'],t['y'],t['x']+32,t['y']+32)).tobytes(),t['id']
checks.append(f"All {len(old['tiles'])} previous tiles retain exact pixels, IDs and coordinates, including flowers and water animation")
coords=set()
for t in new['tiles']:
 x,y=t['x'],t['y'];assert x%32==y%32==0 and 0<=x<=sheet.width-32 and 0<=y<=sheet.height-32;assert (x,y) not in coords;coords.add((x,y));assert crop(t).getbbox(),t['id']
checks.append(f"All {len(new['tiles'])} tile cells are aligned, unique, nonempty and inside the master")
for prefix,count in [('meadow.grass.',16),('meadow.path.255.',4),('meadow.sward.255.',2)]:
 tiles=[t for t in new['tiles'] if t['id'].startswith(prefix)];assert len(tiles)==count;assert len({crop(t).tobytes() for t in tiles})==count
checks.append('All sixteen turf, four dirt-center and two sward-center variants have distinct native pixels')
palette=json.loads((root/'assets/playable/overworld/palette.json').read_text());allowed={c.lower() for values in palette.values() for c in values}
for t in new['tiles']:
 if not t['id'].startswith('meadow.'):continue
 for r,g,b,a in set(crop(t).get_flattened_data()):assert a==255 and f'#{r:02x}{g:02x}{b:02x}' in allowed,t['id']
checks.append('Every new terrain pixel is opaque and belongs to the named checked-in palette')
report={'baseline':baseline,'checks':checks,'tiles':len(new['tiles']),'newTiles':len(new['tiles'])-len(old['tiles']),'size':list(sheet.size),'masterSha256':hashlib.sha256((root/'assets/playable/overworld/master.png').read_bytes()).hexdigest()}
p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
