# M1.NET3 — Normal movement, A-button net, visible escapes

[Updated Net Meadow](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/net-grid.html) · [Preserved original free-movement meadow](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/net.html)

The user found NET2 less fun and rejected the movement slowdown. This revision keeps the existing tile movement/controller at its ordinary speed and changes only net handling and critter reactions. It is a review test, awaiting user feel/art feedback; the accepted adventure and saves are untouched.

## Controls and proposed timing

- Tap on-screen **A**: swing from carry with a longer windup.
- Hold **A**: lift and ready the net. It never auto-swings while held.
- Release after readying: the quick downward swing.
- Keyboard action equivalents: Space, Z or Enter. Arrows/WASD still move. There is no READY toggle and no ready movement slowdown.
- The original game controller still completes16-tick steps and tap-turns exactly as before. A swing requested during an existing committed step waits for that boundary; this rule is unchanged from NET2.

Current **proposed Critz test values**: ready after240ms, tap strike at340ms/700ms total, readied strike at140ms/480ms total; all quantized to the existing game tick. These values and fear radii are not measured Animal Crossing specifications. Adjacent-tile aim remains unchanged. Raised ready tool layers reuse exact original net pixel registrations under new asset names, leaving NET1 art and behavior intact.

## Fright and escape

Close footsteps/bumping build fear. Holding the readied net reduces the disturbance without changing player speed. Missed swings can immediately startle nearby critters. A brief visible flinch gives a small recovery window; then beetles spread their wings and fly up out of the scene, while snails/isopods scuttle toward the nearest grass clump and disappear behind rustling blades. In-flight escape actors release collision reservations and cannot be captured once the escape begins. Escaped critters leave for this visit; BAG → Reset meadow restores all six safely.

Grass patches are walkable decorations planted only on grass tiles, with separate back/front foliage layers sorted by ground contact. No new static collider or blocker is inferred from art alpha. Flight is an integer-pixel visual departure; the regular player and creature walking controller is unchanged. Escapes are nonlethal, session-only and never mutate inventory, money or adventure saves.

## Validation

- 13 focused tests cover unchanged movement traces with/without a held net,16-tick steps, tap/hold timing, no auto-repeat/cancel swing, adjacent catches, committed-step swing queuing, reservations, actual fear/escape outcomes, reset and original preservation.
- 47 saved native checks verify hard alpha, dimensions, exact PNG hashes, untouched original beetle and exact prepared tool sources. Original Hero/net/creature images remain unchanged. [Native report](native-checks.json), [flight/grass sheet](native-assets-4x.png).
- 9 actual-input browser scenarios cover keyboard and two-finger touch, tap versus prepared timing, cancellation, movement/step buffering, a real snail catch, naturally triggered beetle flight and crawler hiding, four layouts, bag/reset and the working original link. Synthetic save/backup markers remain exact, with zero storage writes. [Browser report](browser-report.json), [flight](beetle-flight.png), [scuttle](crawler-scuttle.png), [hiding](crawler-hiding.png), [held net on phone](phone-ready-walking.png).
- An input-only model observer catches all six in six swings over637 ticks at normal movement speed using the real press/hold/release functions, without teleporting or altering critters. [Model report](catching-model-report.json). This is model evidence, not browser play.

Screens and state checks establish the prototype's behavior, not final art/feel approval. Physical iPhone Safari remains untested. Source, full-suite and scoped publication receipts follow in PROJECT_STATUS. The original free version stays unchanged; private character studies remain outside publication.

Next: user tests the A-button rhythm and actual escape reactions before any broader catching or adventure integration.

## Publication receipt

Version **60** deployed successfully to the [existing phone URL](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/net-grid.html). Public JS/model/stylesheet/wing/grass bytes were checked against the tested build after rollout; all nine actual-input browser scenarios then passed on the hosted page without sign-in. [Hosted report](hosted-browser-report.json), [asset proof](hosted-asset-proof.json), [actual flight](hosted-beetle-flight.png), [grass hiding](hosted-crawler-hiding.png).

Root main passed344 unit tests; the scoped public source passed335, existing/new syntax checks, production build and full delivery validation (4617 exact files,1276 equal JSON documents plus generated contact data). Original meadow passed all seven regression scenarios on the same production build, with original source/render/style/viewer hashes exact. [Production report](production-browser-report.json), [original regression](original-regression-report.json), [source/deployment proof](publication.json). Physical iPhone Safari remains untested. A swing still plants the player for its action as before; holding readies the net without changing ordinary movement.

Implementation `b59e81fde308aa94bf64360c797b46630d74c913` was pushed to origin/main and remote-verified. Sites source `bc9f9a54694d67671b60a12fddf05f6b7150699c` adds only NET3 over prior live source `4ecb721b4d9e5152913c93701bd2382990a94dc9`; deployment `appgdep_6ad15d9c0c208191b2b1aecd48bf9fc5` succeeded. Accepted adventure src/root entry/style/playable assets have zero diff. Private character work and unrelated checkout edits remain excluded. This final evidence/status update is documentation only; no redundant deployment is needed.

Next action remains the user's art/feel review of tap/hold/release and natural flight/hiding, before adventure adoption or broader catching work.
