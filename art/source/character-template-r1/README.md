# CHT1 source

Run `build.py` with Pillow for a focused pose (`--direction south|north|west|east --pose idle|A|P|C`, default South idle). Run `proof.py` after the existing16 poses have been generated. Static proofs only; no animation.

This is a **character template**, not anatomy. Actual dressed Hero outfit, waist, hand masses, full shoe shape/contact and RGBA stay exact; only a bald scalp replaces removable hair. Existing appearance PNGs supply independently stored original-material masks. No prior NB anatomical body part or geometry is read. Per-pose registration JSON records actual region sites, original source hashes, lower row occupancy and selected-hair hidden-scalp coverage. Every hair recomposition reproduces source Hero exactly.

Protected lower rows begin44 except north idle/A/C45, whose original hair/nape includes44. This is a declared per-view hair/head boundary, not a relaxed clothing/waist/shoe test: every actual material-region cell, lower RGBA and contact is checked separately. [Proof, current review status and limits](../../../docs/reviews/M1-CHT1/README.md).
