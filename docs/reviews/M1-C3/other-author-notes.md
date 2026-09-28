# M1.C3 — Kaid, Ollie, rival parents walking frames

The four ready source files are `characters/kaid.json`, `characters/ollie.json`, `characters/rival-mom.json`, and `characters/rival-dad.json`. Each has 12 frames: south/north/west/east × idle/strideA/strideB. Every storage frame is 24×32, anchored at `[12,32]`, within the 20×26 painted ceiling. Original v2 south idle rows and palette maps are preserved exactly.

Idle feet finish on row30. Both strides use a one-row downward head bob, with independently articulated short arms and opposite planted/lifted feet; they do not just translate an idle sprite. The walking order is strideA, idle, strideB, idle with eight simulation updates each, from the pinned reference table. No running set or emulator-observed equivalence is claimed.

Kaid has explicit physical-side direction notes. The spout is on his right and the handle on his left: south shows spout screen-left and loop screen-right; north reverses those screen sides. West exposes the character-left near handle at the rear and a compressed far spout; east exposes the character-right near spout and occludes the far handle. The profiles are different side drawings, not a mirrored pair. Validation checks closed loop holes in south/north/west and proves east cannot be obtained by mirroring west.

Four individually requested built-in imagegen pose guides are retained in `guides/`, along with their exact prompts and source/provenance records. The guides are references only; no generated bitmap was resized or sampled into production pixels. Canonical references were viewed before generation. Native head/profile/back and body poses were individually authored in `author.py`, with final frame rows exported as the JSONs above.

`export.py` rebuilds every individual PNG and native/4×/8×/light-dark/room proof from the final JSONs. `export-manifest.json` records source and image hashes so stale sheets can be detected. `validate.py` records technical checks in `validation.json`. Run with Python and Pillow. The local authoring/validation scripts use this task's recorded source checkout; production consumption uses the portable JSON rows.

All 48 frames were inspected at native, 4× and 8×; light/dark and floor backgrounds were inspected. The first side-face pass placed eyes too close to the nose outline; final profile eyes were moved two native pixels inward, then all evidence was regenerated from final JSON. Kaid handle openings, outline continuity, compact child body, short parent trousers, Ollie's cap and cargo silhouette were checked.

Technical validation passes do not constitute user visual/animation approval. The pose guides contain illustrative rendering and labeling imperfections and are not production sheets. Physical phone playback and gameplay integration are outside this four-character authoring component; root integration supplies the shared atlas and walking review.

Independent review caught a reversed near-side interpretation in the first Kaid profile guide. The final native west shows the near character-left handle; east shows the near character-right spout. South/north were unchanged. The first guide is explicitly superseded in provenance, a corrected built-in guide is retained, and every proof was regenerated after this correction.
