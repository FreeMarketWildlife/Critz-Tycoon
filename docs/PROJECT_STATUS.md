# Project status

Updated **2026-09-26 (America/Los_Angeles)**. Current milestone: **M1 visual review**. Active delivery: **M1.E1 gallery — inventory and animation viewer**. Environment revision 2 remains awaiting visual review. M0 remains complete. M1/G1 and M2/G2 are not complete or approved.

## Asset gallery follow-up — 2026-09-26

The user requested a playable link and a sheet of all existing pixel assets, including animation. This authorizes publication of a review gallery beside the existing game, without approving new artwork or modifying gameplay.

- Gallery: `/art-review/`; previous focused review retained at `/art-review/style-proof.html`.
- **216 catalog entries**: 13 revision-2 parts, 41 current prototype appearances/props/buildings/compositions, 162 rejected revision-1 entries. Distinct renderer sizes and story states count as entries; these are not 216 wholly unique production tiles.
- **10 actor appearances**, all four current facing drawings, live walk-parameter/idle previews. NPCs normally remain idle in-game; the gallery exposes the existing renderer parameter. No new walking sprites were authored.
- Three live effects: tank plants/isopods/springtails, opening gecko motion, rescue-marker bob. Environment review PNGs remain static. No approved Emerald-style animation sheets exist yet.
- [Complete PNG contact sheet](../assets/catalogue/all-assets.png), [160 sampled character views](../assets/catalogue/character-frames.png), downloadable in the gallery. Export includes original code-drawn prototype artwork (including its translucent/rounded rendering), explicitly labeled as such.
- **13 gallery checks passed**, including loading, animation changes/pause/step, filtering, PNG export/download, reduced motion, zero uncaught errors and no overflow at 320/390/844/1280 widths. Isolated synthetic storage stayed unchanged. [Report](verification/ART_GALLERY.json). 10/10 domain tests, 14/14 reported game-browser checkpoints, and syntax/build checks pass. [Game report](verification/GALLERY_GAME_REGRESSION.json). The browser reload assertion covers names, money, post count and rescues; its broad success-message wording does not establish full tank/inventory equality. Physical phone Safari remains untested.
- Hosted and GitHub source histories were merged on main at `3ef1c0f2023c125070f95288c3e60de4aba6ee3c`; the Site branch only added the identical hosting manifest. No remote history was overwritten, no branch/worktree created, and the merge changed no tracked file content.
- Current publication is in progress; record the verified deployment below. The earlier permission denial is a historical tool result, not a current restriction after the environment permissions changed and the user asked to view/play.

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
- The earlier art proof changed no game code. The gallery follow-up adds named exports for existing art helpers and includes the gallery/assets in the static build; root game markup, gameplay logic, save keys/schema and GAME_VISION remain unchanged. Review files are served separately and not integrated into gameplay. No real user browser storage was read or modified.
- Physical phone/Safari, Hero/Mom scale, movement, camera and occlusion behavior remain untested in this art proof. No collision, warp, animation or production Tiled pipeline is claimed.

## Approval and exact next action

**Await the user's response to the focused revision-2 proof.** If it still misses the target, revise this small example. Only after the visual direction is accepted should the indoor/outdoor kit and Rootport/route/Liarsville proposals be rebuilt in the revised style. The original broader environment request is unfinished at this visual review boundary.

No M1.1 character lineup or M1.2 Hero/Mom bedroom scale proof is complete. The separate ten shared Hero/rival candidate assignment remains pending. G1 and G2 are explicitly unapproved; no playable-world expansion, M2 movement, save migration or new story content is authorized by this artwork delivery.

## Git and hosting delivery

- Work remains on **main**; initial clean local HEAD and separately verified GitHub `origin/main` were `b779dec5ee4c1879e427dc07fc6c74751bcf85b3`.
- **Artwork/research delivery commit:** `8f57d089cbbff8ede0de37458d7a1fb90ca25690`, pushed to GitHub `origin/main` and verified with `git ls-remote` to match local HEAD. Working tree was clean at that verification. The following documentation-only receipt commit records this evidence; it does not change the reviewed PNG hashes. Final delivery must also verify that receipt HEAD against the remote.
- Sites source opening first hit a sandbox DNS failure. The required network escalation was **rejected by the user**. No Sites source push, saved version or deployment happened, and no further attempt was made. Access/audience unchanged.
- [Phone game](https://critz-tycoon.freemarketwildlife.chatgpt.site) therefore still serves its previously successful owner-only version 1: deployment `appgdep_6ab5dd4db9608191a338dfbdc9786320`, saved version `appgprj_6ab5dd1e11ac8191937254280d6ba196~appgver_5aec90aa6f208191ab9a7c3f3ad0546e`, previous hosting source `e64d5ea16be908d90995ea16dffb56f36437ae73`. This review is **not deployed**. A GitHub push does not change the phone build.

## Earlier baseline / resume context

M0.1 audit, M0.2 source measurements and M0.3 production documents are complete. Original gameplay baseline: `191e3a6b7721d8193f47914c6f7afa1d50b70dbc`; previous browser baseline: 14/14 reported checkpoints, no uncaught errors in isolated Chrome contexts. See [audit](AUDIT_M0.md) and [baseline report](verification/M0_BROWSER_BASELINE.json) for their limited scope. Current art work does not repeat or supersede that browser coverage.

The [vision](GAME_VISION.md) remains canon; its older habitat/commission milestone is deferred by the visual-foundation sequencing. Reference source stays pinned to `5eff78649e7170a877b961ef0b3da13b81a16038`; selected environment assemblies narrow U002 without resolving all silhouettes, original artist process or runtime capture unknowns. No reference-game artwork is shipped.

Resume by reading this status, plan, art Bible, reference ledger, decision log and vision; inspect actual Git status/HEAD/remote; stay on main and preserve unrelated edits. Do not treat unapproved/rejected art as accepted because files or a commit exist.
