# M1.CT2 — Contact comparison with actual tile movement

[Play the contact lab on phone](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/contact-lab/).

The user likes CT1 but explicitly requires tile-based movement for a valid comparison. Every option now imports the actual adventure controller, `src/movement.js`. The former free/fine approach and method selector are removed. Old `movement=fine` URLs still use tile walking. No new controller or reference timing is invented.

Hold arrows/WASD or the touch controls to walk. A short press completes one tile; from rest, changing direction first turns in place. Committed steps finish after release or direction changes, preserving the main game's behavior. The same controller supplies walking stride/idle poses and blocked-wall animation. A fresh collision requests the existing optional haptic once; holding into the wall does not repeat the request. Copy choice records `tile-based` and the actual controller.

A–D continue to compare the same house, indoor wall and cliff on four ground surfaces. The solid cells, roof occlusion, collision/grid/cutaway views and source artwork are unchanged. Every structural transition cell is fully blocked, even its ground-colored part. At frontal contact Hero's anchor is y256; the idle foot edge is y254:

| Option | Structure / ground in the 32px transition cell | Idle front-foot gap |
| --- | --- | --- |
| A | 8 / 24px | 54px |
| B | 16 / 16px | 46px |
| C | 24 / 8px | 38px |
| D | 28 / 4px | 34px |

This is the spacing to judge with tile movement. The 22×8 foot rectangle is an inspection overlay; traversal checks explicit destination cells through the real controller. The fixed clock uses the shared bounded accumulator, and background/blur input clears without abandoning a committed step. The demo has no running unlock, ledge traversal or door warp, matching its limited collision-study purpose. Adventure saves, editor drafts, accepted maps and native art remain untouched. User praise approves the test direction, not a particular material split or the broader M1/M2 gates.

[Canonical terminology and art rules](../../ART_BIBLE.md#transition-tile-contact-study--m1ct1-user-correction). [Pinned reference measurements and original study history](../M1-CT1/README.md). CT1's fine-approach instructions and measurements are historical and superseded by this correction.

Validation uses isolated synthetic browser contexts. Unit checks compare the lab with independent direct calls to the actual controller over3,000 ticks, verify turns, committed release, full-cell collision, all four approaches,30,000 stress ticks, haptic deduplication and copy metadata. Browser coverage exercises all12 fixture/option combinations, brief committed steps, all sides, roof/foot inspection, clipboard, synthetic-save preservation, blur recovery and phone portrait/landscape. Physical Safari and physical vibration remain unverified; unsupported API status stays explicit.

Publication and final results are recorded in project status and adjacent reports. The next action is to test A–D with tile walking and paste Copy choice for chat.

Final clean checks: **175 unit tests and15 contact browser scenarios**, syntax checks and891 tested runtime hashes. Phone and all three B contact fixtures were inspected. An obsolete fine-mode assertion in the browser harness was corrected before final results. [Browser report](browser-check.json) · [Verification](verification.json) · [Preserved work](preservation.json).
