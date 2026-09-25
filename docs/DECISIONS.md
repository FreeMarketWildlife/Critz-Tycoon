# Decision log

Only user approvals promote visual/feel proposals into approved standards. Technical choices below are labeled separately.

| ID / date | Decision | Authority / state |
| --- | --- | --- |
| D001 / 2026-09-24 | Work directly on `main`; do not create development branches/worktrees. | User instruction, approved. Existing feature branch is historical and retained. |
| D002 / 2026-09-24 | Execute M0 only now; progress through M1 visual and M2 playable feel review gates before broader integration. | User's supplied production brief, approved scope. |
| D003 / 2026-09-24 | Target 240×160 exploration, 8×8 base tiles, 16×16 metatiles, native raster then nearest-neighbor scaling, external virtual controller, original Critz identity. | User-approved technical direction; artwork itself remains unapproved. |
| D004 / 2026-09-24 | Preserve GAME_VISION as canon and existing working systems/saves. Its older habitat/commission “next milestone” is deferred by this visual-foundation plan. | User-approved scope and precedence; GAME_VISION left unchanged. |
| D005 / 2026-09-24 | Locate playable foundation in existing PR #1 and fast-forward local `main` from `9f14c4f` to `191e3a6` for audit. | Routine local integration within user instruction to build on existing implementation. No new branch, remote push, PR closure or deployment. |
| D006 / 2026-09-24 | Research at pret/pokeemerald `5eff78649e7170a877b961ef0b3da13b81a16038`; mark source inspection and PNG measurement separately from emulator observation. | M0 research method, verified provenance; no execution capture claimed. |
| D007 / 2026-09-24 | Propose Tiled orthogonal JSON + PNG sheets and stable metadata; fixed GBA-period exploration simulation; proposed proportions/palettes in art bible. | Technical production proposals, subject to proof in M1–M3. Not user art/feel approval. |

No G1/G2 approvals exist. When received, append date, user decision, exact files/revision or artifact hashes, accepted deviations, and any remaining conditions. Do not rewrite an unresolved proposal as a past approval.

- Follow-up user authorization: “push EVERYTHING then give me the link.” Commit and push the playable foundation and all pending M0 project files directly to GitHub `main`; retain the existing successful phone-play deployment. This does not authorize starting M1 or imply visual approval.
