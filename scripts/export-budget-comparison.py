#!/usr/bin/env python3
"""Assemble atlas pixels into a lossless palette GIF; never edits source art.

Run from the project root, for example:
  python3 scripts/export-budget-comparison.py --out test-results/budget-animation
Requires Pillow. Source image and metadata paths are configurable.
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, __version__ as PILLOW_VERSION

WIDTH, HEIGHT, SCALE = 400, 610, 4
BACKGROUND = (12, 34, 39)
CARD = (29, 60, 64)
LINE = (56, 91, 92)
TEXT = (240, 236, 218)
MUTED = (180, 201, 192)
ACCENT = (231, 199, 129)
CENTERS = {16: 104, 24: 296}
ROW_TOP = {"mom": 94, "kaid": 254, "professor": 414}
CHARACTERS = [("mom", "Mom"), ("kaid", "Kaid"), ("professor", "Professor Nugget")]
DIRECTIONS = [("down", "Down / front"), ("left", "Left"), ("up", "Up / back"), ("right", "Right")]
CYCLE = ["strideA", "idle", "strideB", "idle"]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas", type=Path, default=Path("assets/review/budget-comparison/atlas.png"))
    parser.add_argument("--metadata", type=Path, default=Path("assets/review/budget-comparison/atlas.json"))
    parser.add_argument("--out", type=Path, default=Path("test-results/budget-animation"))
    parser.add_argument("--cycles-per-direction", type=int, default=3)
    args = parser.parse_args()
    assert args.cycles_per_direction > 0
    args.out.mkdir(parents=True, exist_ok=True)
    metadata = json.loads(args.metadata.read_text())
    atlas = Image.open(args.atlas).convert("RGBA")
    assert list(atlas.size) == metadata["size"]
    assert {p[3] for p in atlas.get_flattened_data()} <= {0, 255}, "Binary alpha required."
    assets = {a["id"]: a for a in metadata["assets"]}
    sprite_colors = {p[:3] for p in atlas.get_flattened_data() if p[3]}
    fonts = {s: ImageFont.load_default(size=s) for s in (13, 15, 16, 21)}
    proofs = []

    def centered(draw, y, label, size=15, color=TEXT, cx=200):
        # The bundled small font lacks multiplication signs. Draw that one glyph
        # directly so the visible dimension labels remain precisely 16×32/24×32.
        font = fonts[size]
        parts = label.split("×")
        widths = [round(draw.textlength(part, font=font)) for part in parts]
        cross = max(5, size // 2 - 1)
        cross_gap = 3
        total = sum(widths) + (len(parts) - 1) * (cross + cross_gap * 2)
        x = cx - total // 2
        for i, part in enumerate(parts):
            bbox = draw.textbbox((0, 0), part or "0", font=font)
            draw.text((x, y - bbox[1]), part, font=font, fill=color)
            x += widths[i]
            if i + 1 < len(parts):
                x += cross_gap
                yy = y + max(1, (bbox[3] - bbox[1] - cross) // 2)
                draw.line((x, yy, x + cross - 1, yy + cross - 1), fill=color)
                draw.line((x, yy + cross - 1, x + cross - 1, yy), fill=color)
                x += cross + cross_gap

    def compose(direction, pose, verify=False):
        frame = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
        draw = ImageDraw.Draw(frame)
        draw.fontmode = "1"  # Exact palette colors: no antialiased label fringes.
        centered(draw, 16, "Character budget comparison", 21)
        centered(draw, 44, "Original Critz artwork  /  review", 13, MUTED)
        direction_label = dict(DIRECTIONS)[direction]
        centered(draw, 60, f"Facing {direction_label}", 13, ACCENT)
        for budget in (16, 24):
            centered(draw, 78, f"{budget}\u00d732", 16, TEXT, CENTERS[budget])
        for character, label in CHARACTERS:
            top = ROW_TOP[character]
            centered(draw, top + 4, label, 15)
            for budget in (16, 24):
                center = CENTERS[budget]
                draw.rounded_rectangle((center - 88, top + 23, center + 87, top + 153), radius=8, fill=CARD)
                baseline = top + 150
                draw.line((center - 66, baseline + 1, center + 65, baseline + 1), fill=LINE)
                item = assets[f"compare.{character}.{budget}.{direction}.{pose}"]
                x, y, w, h = item["rect"]
                anchor_x, anchor_y = item["anchor"]
                assert [w, h] == [budget, 32]
                assert [anchor_x, anchor_y] == [budget // 2, 32]
                native = atlas.crop((x, y, x + w, y + h))
                enlarged = native.resize((w * SCALE, h * SCALE), Image.Resampling.NEAREST)
                left, upper = center - anchor_x * SCALE, baseline - anchor_y * SCALE
                frame.paste(enlarged, (left, upper), enlarged)
                if verify:
                    # Every opaque native pixel becomes exactly one uniform 4×4 block.
                    for sy in range(h):
                        for sx in range(w):
                            pixel = native.getpixel((sx, sy))
                            if pixel[3]:
                                block = frame.crop((left + sx * SCALE, upper + sy * SCALE,
                                                    left + (sx + 1) * SCALE, upper + (sy + 1) * SCALE))
                                assert set(block.get_flattened_data()) == {pixel[:3]}
                    proofs.append({"asset": item["id"], "screenAnchor": [center, baseline], "scale": SCALE})
        centered(draw, 584, "Same 4\u00d7 pixel scale  /  feet aligned", 13, MUTED)
        return frame

    sequence = [(direction, pose) for direction, _ in DIRECTIONS
                for _ in range(args.cycles_per_direction) for pose in CYCLE]
    frames = [compose(direction, pose, verify=True) for direction, pose in sequence]
    poster = compose("down", "idle")
    # One deterministic global palette contains all source RGB values plus UI colors.
    colors = sorted(set().union(*(set(frame.get_flattened_data()) for frame in frames), set(poster.get_flattened_data()), sprite_colors))
    assert len(colors) <= 256, f"Exact palette overflow: {len(colors)} colors"
    palette = Image.new("P", (1, 1))
    packed = [channel for color in colors for channel in color]
    palette.putpalette(packed + [0] * (768 - len(packed)))
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    for source, converted in zip(frames, indexed):
        assert source.tobytes() == converted.convert("RGB").tobytes(), "Palette mapping changed pixels."
    # GIF stores centiseconds. Carry rounding across holds to approximate 133.942 ms
    # without silently claiming unsupported 134 ms timing in the exported GIF.
    hold_ms = metadata["animation"]["tickSeconds"] * metadata["animation"]["holds"][0] * 1000
    ends = [round((i + 1) * hold_ms / 10) * 10 for i in range(len(sequence))]
    durations = [ends[0]] + [b - a for a, b in zip(ends, ends[1:])]
    gif_path = args.out / "character-budget-comparison.gif"
    poster_path = args.out / "character-budget-comparison-poster.png"
    indexed[0].save(gif_path, save_all=True, append_images=indexed[1:],
                    duration=durations, loop=0, disposal=2, optimize=False,
                    comment=b"Original Critz atlas pixels. Same integer 4x scale. Review candidate.")
    poster.save(poster_path, optimize=False)
    decoded = Image.open(gif_path)
    assert decoded.n_frames == len(frames)
    decoded_durations = []
    decoded_colors = set()
    for i, expected in enumerate(frames):
        decoded.seek(i)
        actual = decoded.convert("RGB")
        assert actual.tobytes() == expected.tobytes(), f"GIF roundtrip mismatch at frame {i}"
        decoded_durations.append(decoded.info["duration"])
        decoded_colors.update(actual.get_flattened_data())
    assert decoded_durations == durations
    assert sprite_colors <= decoded_colors
    alt = ("Animated comparison of Mom, Kaid, and Professor Nugget in three rows. "
           "The left column uses 16 by 32 pixel frames and the right uses 24 by 32 pixel frames. "
           "Both columns use the same four-times pixel scale and aligned foot anchors. "
           "Each character walks facing down, left, up, then right, with a visible facing label. "
           "The sequence repeats. This is review artwork awaiting user choice.")
    report = {
        "dimensions": [WIDTH, HEIGHT], "scale": SCALE, "frameCount": len(frames),
        "directions": [d for d, _ in DIRECTIONS], "cycle": CYCLE,
        "cyclesPerDirection": args.cycles_per_direction, "requestedHoldMs": hold_ms,
        "encodedHoldValuesMs": sorted(set(durations)), "averageEncodedHoldMs": sum(durations) / len(durations),
        "loopDurationMs": sum(durations), "gifTimingNote": "GIF centisecond timing uses carried 130/140 ms rounding.",
        "sourceOpaqueColorCount": len(sprite_colors), "globalPaletteColorCount": len(colors),
        "sourcePalettePreserved": True, "gifRoundtripPixelExact": True,
        "spriteBlocksExactNearestNeighbor": True, "sourceAssetsRead": len({p['asset'] for p in proofs}),
        "footAnchorYByRow": {character: ROW_TOP[character] + 150 for character, _ in CHARACTERS},
        "atlasSha256": digest(args.atlas), "metadataSha256": digest(args.metadata),
        "gifSha256": digest(gif_path), "posterSha256": digest(poster_path),
        "gifBytes": gif_path.stat().st_size, "pillowVersion": PILLOW_VERSION,
        "posterPose": {"direction": "down", "pose": "idle"}, "altText": alt,
    }
    (args.out / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.out / "alt-text.txt").write_text(alt + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
