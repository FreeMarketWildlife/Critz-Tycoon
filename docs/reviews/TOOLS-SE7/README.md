# TOOLS.SE7 — Character construction studio

Published editor revision **07** from source `e0baaed081305e0f53947ab3b1f862ea0da400a7`, pushed to origin/main with exact remote SHA verified. [Deployment receipt](deployment.json) reports succeeded; existing owner-only audience preserved. [Open the editor](https://critz-tycoon.freemarketwildlife.chatgpt.site/sprite-editor/). This tool update treats the supplied pixel data as the user's basic character construction model. [Exact input](user-skeleton.pixels.json), [measurements](measurements.json), [editor guide](../../../sprite-editor/README.md), [Art Bible](../../ART_BIBLE.md).

## Interpretation

Blue: rounded cranium/face. Medium/deep blue: lower face and recessed side shading. White: paired 2×4 eye landmarks. Gray: torso; darker gray: shoulder/neck shading beneath the head. Pink: arms/hands. Green: pelvis/upper-leg connection. Coral: lower legs/feet. Dark brown: contour and internal separations, distinct from shadows. Pink/green/coral are structural region colors without independent shading ramps in this template, not a finished outfit or alien design.

All 2048 cells and palette entries are preserved. 720 are opaque, using ten colors, within `[3,26,29,62]`; all pairs mirror exactly about x16. The supplied external Brendan screenshot reconstruction matches every occupied/empty cell in rows36–61 (832 cells). Eye positions and feet align with pinned Emerald doubled landmarks. The rounded head above row36 is user construction; Brendan's concealed skull is not observable. No reference-game PNG is shipped.

## Authoring changes

- Undoable exact starter and independent opacity/layer guide, with semantic region selection and anatomy map.
- Pencil/eraser/fill/line/rectangle/shade/recolor respect optional fixed region masks, template-outline protection and alpha lock. Mirrored cells are checked independently.
- Shade/Lighten steps one exact palette-ramp color per pixel per stroke; off-ramp colors remain unchanged.
- Color replacement supports current/all animation frames and one-step undo, preserving masks.
- Clean view, hover anatomy labels and silhouette/color mirror-pair diagnostics. These do not certify anatomical correctness.
- Open/paste supports bounded validated exact RLE and existing project JSON, with undoable workspace replacement; guide pixels remain excluded from exports.

## Scope and validation

No new finished sprite or animation is authored or accepted. Construction masks use this fixed front-idle 32×64 template; they do not track arbitrary shifted poses or infer anatomy from colors in imported art. Nonmatching canvas dimensions disable template masks. All drawing colors remain in existing palette banks; no off-palette blending enters artwork. Existing save keys remain unchanged. Testing uses isolated contexts and synthetic state.

The editor retains freely placed references, reference-only cropping, four center-column treatments, cursor-anchored zoom, collapsible/resizable docks, animation and exact exports. All **67 unit tests and 60 isolated Chromium browser scenarios passed**, with zero runtime errors. The eleven new construction scenarios verify the exact starter/undo, guide/export separation, each paint tool under masks, outline/alpha/mirror guards, per-stroke ramp steps, all-frame recolor undo, valid/invalid RLE paste, anatomy map/labels, alternate canvas sizes and mobile layouts. The other 49 scenarios cover existing editor, reference, crop/centering, workspace and zoom behavior. [Unit results](unit-tests.txt), [construction](construction-browser-report.json), [editor](browser-report.json), [reference](reference-browser-report.json), [workspace](workspace-browser-report.json), [crop/centering](symmetry-sides-report.json), [zoom](zoom-browser-report.json).

Visually inspected [anatomy map](anatomy-map.png), [desktop](construction-desktop.png) and [phone](construction-390.png). All **627 tested build files** match the uploaded archive by SHA-256; the only helper-added file is an identical hosting manifest. [Tested hashes](tested-build-sha256.json). The clean release includes the already-committed R9 review work that arrived during development; unrelated unfinished M1.I3 changes were excluded and preserved. No new gameplay artwork or saves were modified by this task.

Next action: refresh to revision 07 and click **Skeleton → Start from skeleton** or **Use as guide**. Select a region and optional paint limits, then use **Shade (D) / Lighten (U)** or scoped color replacement. The user retains final artwork approval.
