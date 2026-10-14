# M1.WA10 — More brown toward the land

The user asks for a thicker, gentler brown deep-water slope growing toward land, explicitly preserving every water pixel. The exact art contract lives in ART_BIBLE.

The existing water mask and wet-side bank stay exact. The shared coast constructor adds a brown shoulder only over previously dry land, using nearest wet material/depth for corners and the north projection. No added raised shoulder on shallow/sand/depth transitions. The collision grid, map geometry, texture animation, wave cycle and v1 drafts/saves remain unchanged. Existing new Map Studio UI is retained.

[Before left / after right](before-after.png) shows the exact same Rootport deep pond at3× nearest enlargement. [Before native](before-native.png) and [after native](after-native.png) retain the whole map, including grid, for comparison.

## Checks

-316 unit tests and standard syntax checks pass. A frozen WA9 fixture from baseline `cfeedb76641a57c8d32ac58bdfbdd714c47f18f4` proves identical water masks and every wet-side bank byte in four orientations. Tests verify the dry-only band, earth colors, all cardinal sides and excluded shallow/sand materials.
-Actual Rootport browser canvas compared to the baseline PNG:2,857 differing pixels, zero inside the water mask. The project remains Rootport22×16. Synthetic fresh storage only; no real browser draft touched. Desktop and390px captures inspect the actual renderer.
-1,936 rotated/mirrored assembled stencil/bank/wash comparisons pass with binary alpha;266 source texture/prop frames remain exact; all110 wash wraps remain verified at3.2s.
-8 complete-coast browser groups pass:74 material pairs, all15 masks/55 raw contexts, orientations/mirrors, shallow/sand/grass returns, phone layout and actual playable coast. All4,070 colored aliases match the browser renderer pixel-for-pixel.
-Native bank inventory becomes450 tiles/350 unique frames, with100 wash sequences. The colored bank remains1,918 unique tiles. Exact count assertions were updated only after regeneration and native/browser proof.

Reports and screenshots live alongside this file. [Pixel proof](rootport-pixel-check.json), [native proof](native-check.json), [browser](browser/bank-browser-check.json), [complete coast](coast/complete-check.json). Production/release receipts follow. Visual review remains with the user; no physical Safari testing or wider M1/M2 approval is claimed.
