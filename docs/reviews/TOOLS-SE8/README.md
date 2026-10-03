# TOOLS.SE8 — Reference, color and trackpad workflow

Revision **08** published from source `9141b2738df31154af10c662e945065838d48f64`, pushed to origin/main and remote SHA verified. [Deployment receipt](deployment.json) reports succeeded; existing owner-only audience preserved. [Open editor](https://critz-tycoon.freemarketwildlife.chatgpt.site/sprite-editor/). [Editor guide](../../../sprite-editor/README.md).

## Behavior

**Copy reference** paints the currently positioned reference onto the active animation frame at 100% opacity, preserving exact sampled RGB, current crop, scaling/sampling, offset and background removal. Out-of-canvas portions clip; fully transparent cells leave existing artwork intact. Any nonzero source alpha becomes opaque in the binary-alpha pixel model. Copy intentionally covers the whole visible reference footprint, independently of drawing masks or mirror mode. It is one undoable edit; other frames are unchanged. The overlay hides afterward so the actual copied pixels are visible. An entirely out-of-canvas/transparent reference produces an explanatory no-op without an undo entry.

**Eyedropper** is labeled in the toolbar and Colors panel; I or Alt-click also works. Choose Visible layer, Artwork or Reference. Visible respects artwork/reference order and Clean mode. Reference RGB is sampled before guide opacity, avoiding faded/tinted picks. Picking returns to Pencil. Custom colors may be entered with a color picker or six-digit hex; 14 selectable palette collections include unchanged Wildlife, character/environment collections, Portraits/skin/hair and Grayscale. Palette switching changes choices without recoloring pixels. The used-color tray exposes current sprite colors, bounded to the first 256 swatches; eyedropper can sample all others.

The reference dropdown includes the user's exact **Basic character skeleton**. Loading the preset does not paint anything; Copy reference is explicit. Existing crop, move/resize, sampling, background removal and center-column tools work with it. Reference/color panels come first; construction and shading panels remain collapsible and the Skeleton launcher opens anatomy tools.

**Two-finger trackpad scroll pans**, including horizontal and diagonal motion. Pinch (Chromium Ctrl-wheel / Safari gesture events), Ctrl/Command-scroll, +/−, Fit and Space-drag remain available. Ordinary wheel no longer changes zoom. Integer zoom preserves pixel edges. Gesture events are tested synthetically; physical MacBook hardware/Safari were not available for direct testing.

## Exact color and export policy

The user explicitly requested unrestricted reference colors and more palette choices. Editor validation now accepts valid six-digit RGB beyond predefined banks and the prior 31-color character limit. All existing projects remain readable; no migration or silent recoloring. PNG, saved JSON and exact RLE are lossless. GIF has 255 opaque slots plus transparency: unused palette indexes are compacted first; when artwork actually exceeds that, the GIF export keeps the most-used colors and maps the rest to nearest RGB, with a visible export message. The project is never quantized by GIF export. PNG imports retain their pre-existing selected-palette quantization behavior; reference copying is the new exact-color path.

No reference-game asset is bundled, no new finished artwork accepted and no gameplay/save changes made. Existing art stays excluded until Copy is clicked. No user's real browser storage is used for testing.

## Verification

All **71 unit tests and 70 isolated Chromium browser scenarios passed**, with zero runtime errors, on the clean committed release. [Unit results](unit-tests.txt), [reference/color/navigation](reference-copy-browser-report.json), [construction](construction-browser-report.json), [editor](browser-report.json), [reference](reference-browser-report.json), [workspace](workspace-browser-report.json), [crop/centering](symmetry-sides-report.json), [zoom](zoom-browser-report.json). New scenarios cover skeleton/reference separation, exact copy/undo, active-frame isolation, transparent/clipped/cropped references, full-color area-average results, reference and artwork eyedropper, Alt-click, 14 palettes, custom-color save/open, off-canvas no-op, two-axis pan, modified wheel and Safari gesture handling, and bounded desktop/mobile layouts. Independent Pillow GIF decoding matched every output pixel, transparency and both animation frames against the reduced export model.

All **651 tested build files** match the deployment archive by SHA-256; the only additional helper file is the identical hosting manifest. [Hashes](tested-build-sha256.json). [Desktop](studio-1366.png) and [phone](studio-390.png) layouts visually inspected. [Independent GIF decoder result](gif-decoder.txt). All unrelated opening file hashes remain unchanged; shared status/plan changes were staged separately and unfinished M1.I3 work excluded. No gameplay changes or game save accesses.

Next action: refresh to revision 08. Choose a reference or skeleton preset, position it, then Copy reference. Use Eyedropper (I/Alt-click), select a palette or enter a hex, and pan with two-finger scrolling. Physical MacBook/Safari gesture verification remains a user-device check; synthetic wheel and gesture tests pass.
