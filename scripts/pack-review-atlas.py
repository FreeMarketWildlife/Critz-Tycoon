"""Losslessly package existing original art; no new pixels or reference assets.

Run with Python + Pillow. The runtime needs only the exported PNG and JSON.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/review/integration-v1"
OUT.mkdir(parents=True, exist_ok=True)
env_dir = ROOT / "assets/review/environment-v2"
char_dir = ROOT / "assets/review/characters-v1"
env = json.loads((env_dir / "atlas.json").read_text())
chars = json.loads((char_dir / "source-manifest.json").read_text())
sheet = Image.new("RGBA", (256, 160))
environment = Image.open(env_dir / "atlas.png").convert("RGBA")
sheet.paste(environment, (0, 0))
assets = []
for entry in env["assets"]:
    assets.append({**entry, "source": "environment-v2/atlas.png", "sourceRect": entry["rect"]})

for index, entry in enumerate(chars["assets"]):
    source = char_dir / Path(entry["png"]).name
    assert hashlib.sha256(source.read_bytes()).hexdigest() == entry["pngSha256"]
    image = Image.open(source).convert("RGBA")
    assert image.size == (16, 32)
    x, y = index * 16, 128
    sheet.paste(image, (x, y))
    assets.append({
        "id": entry["assetId"], "candidate": entry["candidate"],
        "description": entry["description"], "rect": [x, y, 16, 32],
        "groundAnchor": entry["groundAnchor"], "sortAnchor": entry["sortAnchor"],
        "direction": "south", "pose": "idle", "frames": 1,
        "status": "awaiting-review", "source": "characters-v1/" + source.name,
        "sourceSha256": entry["pngSha256"], "paletteId": entry["paletteId"],
    })

sheet.save(OUT / "atlas.png")
manifest = {
    "schemaVersion": 1, "id": "critz.review.integration.v1",
    "image": "atlas.png", "size": list(sheet.size), "baseTile": 8, "metatile": 16,
    "status": "awaiting-review", "assets": assets,
    "limitations": [
        "Visual assembly review; not approved production artwork.",
        "Ten character candidates have one south-idle frame each; no walk/run frames.",
        "Revised indoor art, Mom, Kaid and Professor Nugget sheets are not available.",
        "Rejected environment revision 1 and reference-game art are excluded.",
        "Collision, interactions, warps and save data are not encoded in the atlas.",
    ],
}
(OUT / "atlas.json").write_text(json.dumps(manifest, indent=2) + "\n")

# Independent comparisons against the source PNGs, including transparent pixels.
checks = []
ids = [a["id"] for a in assets]
assert len(ids) == len(set(ids)) == 23
checks.append("23 unique stable IDs, including all 13 environment parts and ten candidates")
occupied = set()
for a in assets:
    x, y, w, h = a["rect"]
    assert 0 <= x < x + w <= sheet.width and 0 <= y < y + h <= sheet.height
    cells = {(xx, yy) for xx in range(x, x+w) for yy in range(y, y+h)}
    assert not occupied.intersection(cells)
    occupied.update(cells)
    source = Image.open(ROOT / "assets/review" / a["source"]).convert("RGBA")
    if "sourceRect" in a:
        sx, sy, sw, sh = a["sourceRect"]
        source = source.crop((sx, sy, sx+sw, sy+sh))
    assert sheet.crop((x, y, x+w, y+h)).tobytes() == source.tobytes()
checks += ["Every atlas crop is byte-for-byte equal to its original RGBA pixels", "All rectangles in bounds and nonoverlapping"]
assert set(sheet.getchannel("A").tobytes()) == {0, 255}
checks.append("Binary transparency only")
report = {"checks": checks, "size": list(sheet.size), "assets": len(assets),
          "atlasSha256": hashlib.sha256((OUT / "atlas.png").read_bytes()).hexdigest()}
(ROOT / "docs/reviews/M1-I1/atlas-validation.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report))
