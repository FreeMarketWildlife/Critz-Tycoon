"""Deterministic complete seven-asset export and shared-face assembly."""
from pathlib import Path
import subprocess,sys
here=Path(__file__).resolve().parent
for script in ['export.py','assemble_faces.py']:
    subprocess.run([sys.executable,str(here/script)],check=True)
