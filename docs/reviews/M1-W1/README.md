# M1.W1 — Rootport, Mossway and Liarsville

The user's “now that you've made that amazing tile set, please make the world use this tile set” selects M1.E2 for integration and explicitly authorizes the northern route, Liarsville, missing environmental art and animation. This supersedes the old environment-only review restriction. It does not approve unrelated character work or self-approve the new map composition/motion.

Play at [the existing phone URL](https://critz-tycoon.freemarketwildlife.chatgpt.site). From Rootport, go north past the spring, through Mossway's grass meadow, then north again into Liarsville. Walking onto a route threshold travels automatically; A also works nearby. Doors and history markers use A. Return south along the same route. Existing story, five shops, neighboring homes, controls, care menus and Critter systems remain.

## The world

- **Rootport:** cottage lanes, fenced vegetable beds, spring fountain, flower gardens, riverside bridge and workshops. Clay/plaster homes and timber/stone shops share real roof/wall/window/door tiles.
- **Mossway:** a short northbound woodland route, mandatory tall-grass crossing, mossy hollow logs, mushrooms, ferns, old waystones and a cliff spillway. Observing the log leaves its inhabitants undisturbed.
- **Liarsville:** broad stone waterworks, clock plaque, timber millkeeper's house and turning wheel, communal gardens, seed library and river crossing. The old waterworks is enterable and contains three history exhibits. Other homes have individual doorstep observations.
- **Home yard:** rebuilt from the same master sheet while preserving all original rescue/foraging interactions.

The history is original Critz fiction: a shared spring and watercourse, a retired mill and two famously disagreeing clocks. It adds environmental observations, not a new paid economy, animal roster or quest reward.

## Working assets

[Active master PNG](../../../assets/playable/overworld/master.png) · [stable IDs and assemblies](../../../assets/playable/overworld/master.json) · [Tiled tileset](../../../assets/playable/overworld/master.tsj) · [editable append-only authoring](../../../art/source/overworld-live/build.mjs) · [map authoring](../../../src/overworld.js).

The **1024×1024** atlas now has **588 named 32×32 cells**. All **385** selected original cells retain their exact pixels and coordinates. The old review remains a frozen historical revision; the playable world uses one active master PNG. Reserved cells stay transparent. Buildings are tile recipes, never baked building sprites.

Four water phases, four waterfall phases, three flower poses played 0/1/0/2, four contacted-grass poses with foreground blades, fountain droplets and a four-phase waterwheel all come from that PNG. Animation is visual only. Terrain and authored footprints determine collision; tree canopies are depth-sorted independently of trunk occupancy. No encounter mechanic is attached to grass.

The framebuffer is **480×320**. Movement/save coordinates retain their original logical tile units and timing; the new renderer maps each cell to 32 native pixels. Existing gameplay characters and interiors remain at their prior appearance, sampled at 2× nearest-neighbor. Unrelated pending character replacement was deliberately preserved in the workspace and excluded from this release. Phones narrower than 480 CSS pixels use a uniform fit; larger displays use integer scale. No claim of one device pixel per art pixel is made on narrow phones.

## Reference research and boundaries

[Research](RESEARCH.md) describes the pinned Emerald metatile/layer and animation source evidence. Source inspection is not emulator observation. All shipped pixels, maps, architecture and history are original; no reference graphics are copied.

## Verification

[Asset audit](asset-check.json): original-pixel equality, binary alpha, alignment, unique IDs, all animated water-edge invariants and distinct grass frames. Unit tests cover every reachable interaction and footprint, 26 bidirectional door transitions, required grass crossing, every map asset reference, unchanged movement cadence, migration idempotence, original-byte archives, quota failures and new-area save round trips.

[Browser audit](world-browser.json) covers a real keyboard journey Rootport → forest → Liarsville → waterworks → Rootport, history interaction, save/reload, actual animation pixels, all 14 scene renders, missing-atlas recovery and phone/desktop layouts. The existing full chapter browser walkthrough separately exercises both loan choices, all four rescues, all five shops, neighboring homes, care/Manage/Stats/View, Critter posts and save recovery. Final receipts below are recorded only after tests and publication finish.

Chromium phone emulation is not physical iPhone/Safari testing. New layouts, art additions and motion await the user's feedback; successful tests do not constitute visual or movement approval.
