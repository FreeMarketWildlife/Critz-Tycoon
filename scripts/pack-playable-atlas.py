#!/usr/bin/env python3
"""Losslessly combine exported native sheets into the game's single PNG atlas.

Requires Pillow. This copies pixels and adjusts atlas rectangles only; it never
redraws, scales, quantizes, mirrors, or otherwise edits the source artwork.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path

from PIL import Image


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def box(rect: list[int]) -> tuple[int, int, int, int]:
    x, y, width, height = rect
    return x, y, x + width, y + height


def png_bytes(image: Image.Image) -> bytes:
    output = BytesIO()
    image.save(output, format="PNG", optimize=False, compress_level=9)
    return output.getvalue()


def build(source_root: Path, output_root: Path) -> dict:
    checks: list[dict] = []

    def check(name: str, passed: bool, details=None) -> None:
        result = {"name": name, "pass": bool(passed)}
        if details is not None:
            result["details"] = details
        checks.append(result)

    sources = []
    for name in ("environment", "characters"):
        manifest_path = source_root / f"assets/playable/{name}/atlas.json"
        metadata = json.loads(manifest_path.read_text())
        image_path = manifest_path.parent / metadata["image"]
        with Image.open(image_path) as image:
            rgba = image.convert("RGBA")
        if metadata.get("schemaVersion") != 1:
            raise ValueError(f"Unsupported source schema: {name}")
        if list(rgba.size) != metadata["size"]:
            raise ValueError(f"Source image dimensions differ from metadata: {name}")
        sources.append({"name": name, "manifest": metadata, "image": rgba,
                        "manifestPath": manifest_path, "imagePath": image_path})

    width = max(source["image"].width for source in sources)
    height = sum(source["image"].height for source in sources)
    atlas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    entries, source_sheets = [], []
    offset_y = 0
    for source in sources:
        image, metadata = source["image"], source["manifest"]
        source["offset"] = [0, offset_y]
        # Deliberately omit a mask so even transparent source RGBA bytes survive.
        atlas.paste(image, (0, offset_y))
        for entry in metadata["assets"]:
            packed = deepcopy(entry)
            packed["rect"][1] += offset_y
            entries.append(packed)
        source_sheets.append({
            "name": source["name"],
            "manifest": str(source["manifestPath"].relative_to(source_root)),
            "image": str(source["imagePath"].relative_to(source_root)),
            "size": list(image.size),
            "offset": [0, offset_y],
            "imageSha256": digest(source["imagePath"]),
            "manifestSha256": digest(source["manifestPath"]),
        })
        offset_y += image.height

    character_map = deepcopy(sources[1]["manifest"]["characters"])
    manifest = {
        "schemaVersion": 1,
        "image": "atlas.png",
        "size": [width, height],
        "status": "playable-review",
        "baseTile": 8,
        "metatile": 16,
        "packing": "Lossless vertical source-sheet copy, environment then characters.",
        "sourceSheets": source_sheets,
        "assets": entries,
        "characters": character_map,
        "limitations": [
            "Final user art and movement acceptance remains pending.",
            "Atlas rectangles and anchors specify appearance only; collision and interactions remain separate.",
            "Twelve compact chibi designs contain 24 entries each. Runs reuse walk artwork at the existing run cadence.",
            "Technical checks do not establish visual approval or exact reference-game equivalence.",
        ],
    }
    entries_by_id = {entry["id"]: entry for entry in entries}
    characters = sources[1]["manifest"]["assets"]

    check("single-png-runtime-contract", manifest["image"] == "atlas.png" and manifest["schemaVersion"] == 1)
    check("expected-packed-size", atlas.size == (512, 1088), {"actual": list(atlas.size)})
    check("unique-stable-ids", len(entries_by_id) == len(entries), {"assetCount": len(entries)})
    check("integer-positive-inbounds-rectangles", all(
        len(entry["rect"]) == 4 and all(type(n) is int for n in entry["rect"])
        and entry["rect"][0] >= 0 and entry["rect"][1] >= 0
        and entry["rect"][2] > 0 and entry["rect"][3] > 0
        and box(entry["rect"])[2] <= width and box(entry["rect"])[3] <= height
        for entry in entries))

    def overlaps(a, b):
        ax0, ay0, ax1, ay1 = box(a["rect"])
        bx0, by0, bx1, by1 = box(b["rect"])
        return ax0 < bx1 and ax1 > bx0 and ay0 < by1 and ay1 > by0

    check("no-overlapping-asset-rectangles", all(
        not overlaps(a, b) for i, a in enumerate(entries) for b in entries[i + 1:]))
    check("binary-alpha", set(atlas.getchannel("A").tobytes()).issubset({0, 255}))
    check("integer-anchors-preserved", all(
        len(a.get("anchor", [])) == 2 and all(type(v) is int for v in a["anchor"])
        for a in entries))
    for source in sources:
        sx, sy = source["offset"]
        image = source["image"]
        copied = atlas.crop((sx, sy, sx + image.width, sy + image.height))
        check(f"{source['name']}-whole-sheet-rgba-exact", copied.tobytes() == image.tobytes())
        check(f"{source['name']}-every-asset-rgba-exact", all(
            atlas.crop(box(entries_by_id[entry["id"]]["rect"])).tobytes()
            == image.crop(box(entry["rect"])).tobytes()
            for entry in source["manifest"]["assets"]))
        check(f"{source['name']}-nonrectangle-metadata-unchanged", all(
            {k: v for k, v in entry.items() if k != "rect"}
            == {k: v for k, v in entries_by_id[entry["id"]].items() if k != "rect"}
            for entry in source["manifest"]["assets"]))

    check("character-map-preserved", manifest["characters"] == sources[1]["manifest"]["characters"])
    counts = Counter(entry["character"] for entry in characters)
    check("24-frames-per-character", len(counts) == 12 and all(value == 24 for value in counts.values()), dict(counts))
    expected = {(direction, mode, pose) for direction in ("down", "up", "left", "right")
                for mode in ("walk", "run") for pose in ("idle", "strideA", "strideB")}
    check("complete-direction-mode-pose-matrix", all(
        {(a["direction"], a["mode"], a["pose"]) for a in characters if a["character"] == character}
        == expected for character in counts))
    references = [pose for character in character_map.values()
                  for direction in character["directions"].values()
                  for mode in direction.values() for pose in mode.values()]
    check("all-character-map-references-resolve", len(references) == 288 and all(key in entries_by_id for key in references))
    check("character-native-frame-and-foot-anchor", all(
        a["rect"][2:] == [24, 32] and a["anchor"] == [12, 32] for a in characters))
    # Independently decode each canonical source, including the reused run art.
    direction_map = {"down":"south", "up":"north", "left":"west", "right":"east"}
    for character in counts:
        source_path = source_root / f"art/source/characters-walk-v3/{character}.json"
        person = json.loads(source_path.read_text())
        for entry in (a for a in characters if a["character"] == character):
            rows = person["frames"][direction_map[entry["direction"]]][entry["pose"]]
            pixels = bytes(v for row in rows for key in row for v in
                ((0,0,0,0) if key == "." else (*bytes.fromhex(person["palette"][key][1:]),255)))
            check(entry["id"] + "-canonical-native-pixels", atlas.crop(box(entries_by_id[entry["id"]]["rect"])).tobytes() == pixels)
    kaid = [a for a in characters if a["character"] == "kaid"]
    check("kaid-explicit-unmirrored-metadata", len(kaid) == 24 and all(a["mirrored"] is False for a in kaid))
    asymmetry = {}
    for mode in ("walk", "run"):
        for pose in ("idle", "strideA", "strideB"):
            left = atlas.crop(box(entries_by_id[f"char.kaid.left.{mode}.{pose}"]["rect"]))
            right = atlas.crop(box(entries_by_id[f"char.kaid.right.{mode}.{pose}"]["rect"]))
            asymmetry[f"{mode}.{pose}"] = left.transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes() != right.tobytes()
    check("kaid-left-right-not-naive-mirrors", all(asymmetry.values()), asymmetry)

    image_bytes = png_bytes(atlas)
    check("deterministic-png-serialization", image_bytes == png_bytes(atlas))
    encoded = Image.open(BytesIO(image_bytes)).convert("RGBA")
    check("png-encode-decode-rgba-exact", encoded.tobytes() == atlas.tobytes())
    report = {
        "task": "M1.I3",
        "status": "technical-checks-passed-awaiting-user-review" if all(c["pass"] for c in checks) else "failed",
        "atlasSize": [width, height],
        "assetCount": len(entries),
        "environmentAssetCount": len(sources[0]["manifest"]["assets"]),
        "characterFrameCount": len(characters),
        "characterRoleCount": len(counts),
        "atlasSha256": sha256(image_bytes).hexdigest(),
        "checks": checks,
        "passed": sum(check["pass"] for check in checks),
        "total": len(checks),
        "limitations": [
            "This validates packing and source preservation; gameplay and visual/feel acceptance are separate checks.",
            "Kaid asymmetry check proves no naive mirrored east/west frames, not an artistic judgment about his anatomy.",
        ],
    }
    report_path = output_root / "docs/reviews/M1-I3/atlas-validation.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    if any(not check["pass"] for check in checks):
        raise ValueError("Atlas validation failed; see " + str(report_path))
    destination = output_root / "assets/playable"
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "atlas.png").write_bytes(image_bytes)
    (destination / "atlas.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output-root", type=Path, help="Defaults to --source-root.")
    args = parser.parse_args()
    report = build(args.source_root.resolve(), (args.output_root or args.source_root).resolve())
    print(json.dumps({key: report[key] for key in ("status", "atlasSize", "assetCount", "passed", "total", "atlasSha256")}))


if __name__ == "__main__":
    main()
