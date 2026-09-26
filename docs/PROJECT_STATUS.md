# Project status

Updated **2026-09-26 (America/Los_Angeles)**. Current milestone: **M1 visual review**. Active task: **M1.E1 — environment tiles and location proposals**, **awaiting review of revision 2**. M0 remains complete. M1/G1 and M2/G2 are not complete or approved.

## Current deliverable and user feedback

The user authorized original indoor/outdoor tiles, placeable map trees and houses; research to fill the art Bible; and visual proposals for Rootport, Liarsville and their short connecting forest route. This extends earlier M1 review scope without approving production integration. The user clarified that trees are placeable scenery.

Revision 1 produced a 162-entry original kit, modular buildings, furniture, trees, terrain edges, four static map compositions and a generated three-location concept board. **The user rejected its style:** it did not look like Pokémon Emerald. All revision-1 assets/maps are retained as clearly labeled rejected review history and must not enter the accepted game.

Revision 2 returns to a focused original **240×160 house/tree scene**, with exact **960×640** enlargement, a 13-piece draft atlas and editable sources. Roof planes/eaves, short facade, material colors and leaf clusters were revised after visually inspecting the pinned source assemblies. A separate generated style study is labeled illustrative and not a production tileset. No response approving either revised image has been received.

- [Current review packet](reviews/M1-E1/README.md)
- [Native revision-2 proof](../assets/review/environment-v2/house-tree-native.png)
- [Exact 4× proof](reviews/M1-E1/revision-2/house-tree-4x.png)
- [Local review page](../art-review/index.html), served at `http://localhost:5173/art-review/` while the local server is running.
- [Updated art Bible](ART_BIBLE.md), [pinned environment research](reference-data/EMERALD_ENVIRONMENT_RESEARCH.md)

## Actual validation

- **23/23 revision-2 asset checks passed:** native dimensions; exact integer enlargement; binary alpha; 13 unique atlas IDs in bounds with no overlap; standalone house/tree PNGs equal atlas crops; 44 part references resolve and fit. [Report](reviews/M1-E1/revision-2/validation.json). Reference images are not read by either deterministic authoring source.
- Native and enlarged revised images visually inspected. The local review page opened successfully in the in-app browser and its current image/labels were inspected. This does not establish user style approval or phone usability.
- **10/10 existing domain/world tests passed**; both authoring-script syntax checks and static game build passed; whitespace checks passed.
- Existing `src/`, root `index.html`, `style.css`, `scripts/build.mjs`, save keys/schema and `GAME_VISION.md` are unchanged. Review files are excluded from the playable build. No user browser storage was read or modified.
- Physical phone/Safari, Hero/Mom scale, movement, camera and occlusion behavior remain untested in this art proof. No collision, warp, animation or production Tiled pipeline is claimed.

## Approval and exact next action

**Await the user's response to the focused revision-2 proof.** If it still misses the target, revise this small example. Only after the visual direction is accepted should the indoor/outdoor kit and Rootport/route/Liarsville proposals be rebuilt in the revised style. The original broader environment request is unfinished at this visual review boundary.

No M1.1 character lineup or M1.2 Hero/Mom bedroom scale proof is complete. The separate ten shared Hero/rival candidate assignment remains pending. G1 and G2 are explicitly unapproved; no playable-world expansion, M2 movement, save migration or new story content is authorized by this artwork delivery.

## Git and hosting delivery

- Work remains on **main**; initial clean local HEAD and separately verified GitHub `origin/main` were `b779dec5ee4c1879e427dc07fc6c74751bcf85b3`.
- Task changes are being committed and pushed under standing authorization. A delivery receipt will record the verified art commit/remote state after push; do not infer a push from this pre-delivery note.
- Sites source opening first hit a sandbox DNS failure. The required network escalation was **rejected by the user**. No Sites source push, saved version or deployment happened, and no further attempt was made. Access/audience unchanged.
- [Phone game](https://critz-tycoon.freemarketwildlife.chatgpt.site) therefore still serves its previously successful owner-only version 1: deployment `appgdep_6ab5dd4db9608191a338dfbdc9786320`, saved version `appgprj_6ab5dd1e11ac8191937254280d6ba196~appgver_5aec90aa6f208191ab9a7c3f3ad0546e`, previous hosting source `e64d5ea16be908d90995ea16dffb56f36437ae73`. This review is **not deployed**. A GitHub push does not change the phone build.

## Earlier baseline / resume context

M0.1 audit, M0.2 source measurements and M0.3 production documents are complete. Original gameplay baseline: `191e3a6b7721d8193f47914c6f7afa1d50b70dbc`; previous browser baseline: 14/14 reported checkpoints, no uncaught errors in isolated Chrome contexts. See [audit](AUDIT_M0.md) and [baseline report](verification/M0_BROWSER_BASELINE.json) for their limited scope. Current art work does not repeat or supersede that browser coverage.

The [vision](GAME_VISION.md) remains canon; its older habitat/commission milestone is deferred by the visual-foundation sequencing. Reference source stays pinned to `5eff78649e7170a877b961ef0b3da13b81a16038`; selected environment assemblies narrow U002 without resolving all silhouettes, original artist process or runtime capture unknowns. No reference-game artwork is shipped.

Resume by reading this status, plan, art Bible, reference ledger, decision log and vision; inspect actual Git status/HEAD/remote; stay on main and preserve unrelated edits. Do not treat unapproved/rejected art as accepted because files or a commit exist.
