# Native tree objects — M1.TR2

Original integer-grid authoring, independent of the generated concept sheet. No reference or concept pixels are sampled. `build.py` exports PNGs, editable `fmw-sprite` indexed projects, object metadata and review plates. `check.py` independently verifies exports, registration and connected pixels. Requires Python with Pillow; the Codex bundled Python supplies it.

Art specifications and terminology live in [ART_BIBLE](../../../docs/ART_BIBLE.md#protruding-objects--sprite-overhang-and-ground-footprint-m1tr2). Placement metadata lives in [objects.json](../../../assets/review/trees-r2/objects.json). The editor's generic RLE description currently assumes canvas-bottom anchoring; use the object metadata for these protruding sprites rather than treating that generic anchor as authoritative.

Open any `*.sprite.json` through the existing Sprite Editor's project import. Custom palette colors and all native pixels are preserved. Static appearances await user visual review; assets are not registered into gameplay.
