# TOOLS.SE8 — Reference, color and trackpad workflow

Revision **08**, release verification in progress. [Editor guide](../../../sprite-editor/README.md).

## Behavior

**Copy reference** paints the currently positioned reference onto the active animation frame at 100% opacity, preserving exact sampled RGB, current crop, scaling/sampling, offset and background removal. Out-of-canvas portions clip; fully transparent cells leave existing artwork intact. Any nonzero source alpha becomes opaque in the binary-alpha pixel model. Copy intentionally covers the whole visible reference footprint, independently of drawing masks or mirror mode. It is one undoable edit; other frames are unchanged. The overlay hides afterward so the actual copied pixels are visible. An entirely out-of-canvas/transparent reference produces an explanatory no-op without an undo entry.

**Eyedropper** is labeled in the toolbar and Colors panel; I or Alt-click also works. Choose Visible layer, Artwork or Reference. Visible respects artwork/reference order and Clean mode. Reference RGB is sampled before guide opacity, avoiding faded/tinted picks. Picking returns to Pencil. Custom colors may be entered with a color picker or six-digit hex; 14 selectable palette collections include unchanged Wildlife, character/environment collections, Portraits/skin/hair and Grayscale. Palette switching changes choices without recoloring pixels. The used-color tray exposes current sprite colors, bounded to the first 256 swatches; eyedropper can sample all others.

The reference dropdown includes the user's exact **Basic character skeleton**. Loading the preset does not paint anything; Copy reference is explicit. Existing crop, move/resize, sampling, background removal and center-column tools work with it. Reference/color panels come first; construction and shading panels remain collapsible and the Skeleton launcher opens anatomy tools.

**Two-finger trackpad scroll pans**, including horizontal and diagonal motion. Pinch (Chromium Ctrl-wheel / Safari gesture events), Ctrl/Command-scroll, +/−, Fit and Space-drag remain available. Ordinary wheel no longer changes zoom. Integer zoom preserves pixel edges. Gesture events are tested synthetically; physical MacBook hardware/Safari were not available for direct testing.

## Exact color and export policy

The user explicitly requested unrestricted reference colors and more palette choices. Editor validation now accepts valid six-digit RGB beyond predefined banks and the prior 31-color character limit. All existing projects remain readable; no migration or silent recoloring. PNG, saved JSON and exact RLE are lossless. GIF has 255 opaque slots plus transparency: unused palette indexes are compacted first; when artwork actually exceeds that, the GIF export keeps the most-used colors and maps the rest to nearest RGB, with a visible export message. The project is never quantized by GIF export. PNG imports retain their pre-existing selected-palette quantization behavior; reference copying is the new exact-color path.

No reference-game asset is bundled, no new finished artwork accepted and no gameplay/save changes made. Existing art stays excluded until Copy is clicked. No user's real browser storage is used for testing.

## Verification

Initial model and browser tests pass; complete clean-release results and publication receipt will be recorded after validation. New scenarios cover skeleton/reference separation, exact copy/undo, active-frame isolation, transparent/clipped/cropped references, full-color area-average results, reference and artwork eyedropper, Alt-click, 14 palettes, custom-color save/open, off-canvas no-op, two-axis pan, modified wheel and Safari gesture handling, and bounded desktop/mobile layouts. Independent Pillow GIF decoding matched every output pixel, transparency and both animation frames against the reduced export model.
