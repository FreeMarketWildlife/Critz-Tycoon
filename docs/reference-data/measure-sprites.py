#!/usr/bin/env python3
"""Print Emerald indexed-PNG sprite bounds. Requires Pillow; input is a local pinned repo."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('repository', type=Path)
args = parser.parse_args()
base = args.repository / 'graphics/object_events/pics/people'
paths = ['brendan/walking.png', 'may/walking.png', 'wally.png', 'mom.png', 'prof_birch.png', 'little_boy.png', 'little_girl.png']
results = []
for relative in paths:
    path = base / relative
    with Image.open(path) as im:
        assert im.mode == 'P' and im.width == 144 and im.height in (16, 32), (relative, im.mode, im.size)
        frames = []
        for index in range(9):
            frame = im.crop((index * 16, 0, (index + 1) * 16, im.height))
            # Source PNGs omit alpha metadata; GBA palette index zero is transparent.
            mask = frame.point(lambda value: 255 if value else 0)
            left, top, right, bottom = mask.getbbox()
            frames.append({'frame': index, 'bbox_half_open': [left, top, right, bottom], 'visible_wh': [right-left, bottom-top], 'last_occupied_row': bottom-1})
        results.append({'file': relative, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sheet': list(im.size), 'frame_wh': [16, im.height], 'indexed_transparency_rule': 'palette index 0, not PNG alpha', 'frames': frames})
print(json.dumps(results, indent=2))
