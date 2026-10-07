"""Reproducible review ZIP; images and source keep repository-relative paths."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
root=Path(__file__).resolve().parents[1]
folder=root/'assets/review/overworld-v1'
files=[p for p in folder.iterdir() if p.is_file() and p.suffix!='.zip']
files += [root/'art/source/overworld-v1'/n for n in ['build.mjs','pixels.json','README.md','design-prompt.txt']]
files += [root/p for p in ['art/source/raster.mjs','art/source/hero-boy-v1/idle.sprite.json','assets/characters/hero-boy-v1/idle-south.png','scripts/check-overworld.py']]
with ZipFile(folder/'critz-overworld-v1.zip','w',ZIP_DEFLATED) as z:
    for p in sorted(files):
        info=ZipInfo(p.relative_to(root).as_posix(),date_time=(1980,1,1,0,0,0))
        info.compress_type=ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,p.read_bytes())
with ZipFile(folder/'critz-overworld-v1.zip') as z:
    assert z.testzip() is None
    for p in files:assert z.read(p.relative_to(root).as_posix())==p.read_bytes()
print(f'PASS ZIP: {len(files)} exact files, {(folder/"critz-overworld-v1.zip").stat().st_size:,} bytes')
