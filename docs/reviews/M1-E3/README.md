# M1.E3 — Richer terrain and clear walking routes

The user asks for more beautiful grass/dirt, preserving moving flowers and removing flowers/fences from paths. This is a refinement of the existing playable world; visual feedback remains with the user.

The master gains 298 original native tiles: 16 turf variations, four material variations for each of 47 path shapes, and two variations for each of 47 connected grass-patch shapes. Warm compressed dirt, restrained pebbles/scuffs, worn verges and grass clusters replace the flat ground. Deliberate turf islands add larger areas of color without painting over roads or crops. Existing forest art fills the non-playable background around small maps in tall views. All 644 prior tiles retain exact pixels and coordinates, including flowers, water, fruit trees and buildings.

Thirty-three misplaced fence cells are removed (32 Rootport, one Liarsville). Remaining rail ends are rebuilt to match their neighbors. Flower patches move into verges, and a placement rule excludes rooted flowers/ferns from roads and solid props. Zero new blocked cells; doors, required tall-grass crossing, fruit, story, save keys and positions remain.

Source is the editable integer-pixel generator in `art/source/overworld-live/terrain.mjs`; the output is one 1024×1472 master PNG with 942 named cells and stable metadata. These are original Critz pixel/material choices, not copied Emerald artwork or new reference measurements.

Working-tree validation: 120 unit tests, five independent native pixel checks, nine terrain-browser scenarios, full native-map and phone screenshot inspection. Early texture drafts were revised for overly regular speckles and square turf corners. Exact clean-release checks and publication are pending. Fresh isolated Chromium contexts use synthetic saves only. No physical Safari test or user art approval is claimed.

Next: complete clean-release regression checks and publish the exact tested build, then user reviews terrain/layout.
