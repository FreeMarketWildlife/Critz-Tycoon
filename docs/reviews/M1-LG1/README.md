# M1.LG1 — Luke’s Greenhouse

**Playable review; art and movement acceptance await the user.** [Open the phone review](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/greenhouse.html) · [Main adventure](https://critz-tycoon.freemarketwildlife.chatgpt.site).

The user’s 2026-10-08 request commissions Luke, a greenhouse of goldfish, eight planted black tubs and an upfront $100 silhouette-scoop interaction. It supersedes IDEA-003’s older “Nuggets” name. This is one focused implementation task within the visual review milestone. Other creator cameos remain planned; no broader roster, world, art or movement gate is self-approved.

## Try it

Start with a separate $300 review wallet. Walk north through the door. Luke approaches immediately and offers one goldfish for $100. Decline, or arrive with less than $100, and he says **“GET OUT!”** before ushering the player back outside without charging.

After paying, he says **“Ok, go ahead and pick a tub”**. Walk to one of eight tubs and press A. Confirm **“Are you sure you want that one?”**, then watch the concealed fish. Tap where a silhouette is going; the net takes 380ms to land. It catches the nearest fish inside its 25px catch radius at landing time. Colors are concealed, while individually authored head/body/tail shapes can reward familiarity. A miss is free to retry. There is no outcome reroll after the scoop: the revealed fish is the one actually caught.

One charge buys one fish. Enjoy the face reveal, press A, then explore and view any tub freely. Walk out; the next entrance starts admission again. Leaving before catching refunds the unused scoop. Reloading resumes the existing paid/caught visit. These refund/retry choices resolve unspecified edge cases and remain provisional game-balance choices.

Use arrows/WASD and Z/Enter/Space for A; X/Escape for B; P for the menu. In the scoop view, arrows move the reticle and A drops the net. Touch controls are at least44 CSS pixels. The menu contains the wallet, collection, help, Calm setting and a review-only reset. Calm removes the dramatic reveal motion; fish still swim because timing is the mechanic. This is earned fictional game money only.

## Art and references

[Art measurements, observed references and limitations](art-notes.md) · [Native contact sheet](../../../assets/review/luke-greenhouse/contact-native.png) · [Clean3× sheet](../../../assets/review/luke-greenhouse/contact-3x.png) · [Luke grid](art-luke-grid.png) · [Fish grids](art-fish-grid.png) · [Luke walk](art-luke-walk.gif) · [Fish loops](art-fish-loop.gif).

Luke has brown hair, a full beard, bright blue eyes and a maroon shirt. The current approved Hero remains unchanged. Native artwork includes four-direction Luke poses, sixteen distinct fancy-goldfish designs, front/side/top/swim views, sixteen distinct silhouette masks, separately authored small world fish, four planted black tubs, wall aquariums, a modular glass greenhouse and a separately drawn top-down tub.

The sixteen names/patterns are original Critz individuals across ranchu and oranda varieties, not sixteen biological species or a reproduction of Luke’s live inventory. [Luke’s official shop](https://lukesgoldies.com/) and [care-guide image](https://lukesgoldies.com/cdn/shop/files/Screen_Shot_2022-08-29_at_10.42.53_PM.png?v=1661830987&width=1920) informed fish forms; [his official channel](https://www.youtube.com/@lukesgoldies) supplied the face context. [His breeding guide](https://lukesgoldies.com/blogs/news/how-to-breed-and-raise-goldfish) discusses fancy varieties. No downloaded photographs or reference-game pixels ship. The cameo’s dialogue, ejection and transaction rules are fictional user-directed game behavior, not real-world claims or endorsement.

## Save and integration boundary

Only `critz.lukes-greenhouse.review.v1` is read/written. The existing adventure, v1 save/backup, names, money/debt, 25-gallon gift, animal survival, care, Critter earnings and story remain untouched. The only existing UI change is a link in the art library. Goldfish purchases occur only through Luke; existing adventure shops have no goldfish sales.

The review collection persists individual IDs, design, personality seed and the paid visit. Its fish do not yet transfer into adventure aquariums. Production world placement, appropriate aquarium care/stocking and collection migration require a subsequent scoped integration after user feedback. Repeated designs can recur across visits; each catch has a distinct saved individual ID. This review does not claim infinite unique artwork.

## Verification and release

- [Independent native art validation](art-validation.json): decode every PNG and compare each RGBA pixel to editable indexed source; dimensions, hashes, binary alpha, anatomical masks, blue eyes, idle/stride contacts,16 unique silhouette masks and exact3× display.
- Eight domain checks in `tests/greenhouse.test.mjs`: payment, immutability, insufficient funds, deterministic stock, capture identity/idempotence, refunds/re-entry, reachability and malformed saves.
- [Browser report](browser-report.json): actual keyboard/touch entry, approach, ejection, exact/insufficient payments, all eight tubs, missed/landed scoops, keyboard-only aiming/catching, reveal/collection reload, unused refund, re-entry, safe quota-failure recovery, corrupt-save retention and320/390/844 layouts. All tests use isolated synthetic storage, including unchanged adventure/backup sentinels.
- Phone/landscape, native and enlarged screenshots inspected. Physical Safari and reference emulator timing are unverified. The net timing, fish motion and room layout are original Critz choices, not claimed Emerald measurements.

Clean source passes135 unit tests, all14 greenhouse browser checks and all17 existing-adventure browser scenarios. Final exact source, remote SHA and successful deployment receipt are recorded in [project status](../../PROJECT_STATUS.md). Do not infer publication from a Git push alone. **Exact next action:** the user plays this review and gives feedback on Luke’s likeness, the planted greenhouse, fish faces/silhouettes and scoop timing before accepted-world integration.
