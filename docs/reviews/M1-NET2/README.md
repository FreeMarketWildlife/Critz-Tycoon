# M1.NET2 — Net Meadow tile comparison

[Tile-based test](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/net-grid.html) · [Original free-movement version](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/net.html)

The user liked the existing meadow's vibe and explicitly requested preserving that version while testing everything on tiles like the real game. This is a separate comparison, awaiting user art/feel judgment. It reuses all existing net, Hero and critter art without alteration. The original HTML, model, renderer, styles and pose inspector remain byte-exact to their delivered revision; [preservation hashes](original-preserved.json).

## What changed

- Terrain is a 20×14 array of 32px grass/path cells, including cell-registered flowers and connected path turns.
- Player and critters use the actual unchanged `src/movement.js` controller: integer committed cell coordinates, adjacent cardinal destinations, 16-tick walk steps, rest tap-to-turn, and completion of a committed step after release. Rendering uses the game's doubled-pixel foot registration `(32x+16,32y+32)`.
- The simulation uses the game's fixed `280896/16777216` second tick and motion clock. Carry speed matches normal game walking. Ready mode gates the same controller at one advance per three ticks: approximately804ms per tile versus268ms carrying. This slower cadence is a proposed Critz catching-test choice; it is not measured Animal Crossing timing. Cadence changes apply at step boundaries.
- Critters wander to adjacent cells and reserve both current and in-flight destination cells. Player and critter steps cannot overlap those reservations. Beetles react to actual fast movement; ready steps stay quiet. Critter pace and startle remain prototype decisions.
- The net targets exactly the adjacent cell in the locked facing direction. Catching reads the critter's occupied tile at the strike, rather than a free-space radius. A crossing critter changes occupied tile at the halfway point. Diagonal and two-away tiles do not count. A swing released mid-step waits for the committed step to finish, then locks the settled tile/facing.
- Existing carry, hold/release, READY toggle, temporary bag, release/reset and touch controls remain. Bag offers the tile/target overlay and close/wide views. The intro and bag link back to the original version.

All terrain is walkable ground; flowers and turf remain decorative. Play bounds and moving-actor reservations are explicit. There are no new static colliders or overhead props, and no collision is inferred from painted alpha. B-contact art direction remains unchanged. Save data, economy, the accepted adventure and unrelated character studies are untouched.

## Checks

Nine focused model tests cover four-direction16-tick movement, rest turns, step completion after release, slower ready cadence, adjacent-tile catches/misses, queued swings, actor reservations, creature cell travel, beetle response and original-version byte preservation. A further observer/input-only simulation catches all six moving critters in10 swings over4119 ticks, without teleporting or mutating critters; [report](catching-model-report.json). This is model evidence, not browser play.

Six actual-input browser scenarios cover movement/turning/ready, catching the actual starting snail, a queued mid-step swing, pause/resume of an in-flight step, two-finger touch, all four viewports, the grid overlay and the original comparison link. Synthetic adventure save/backup markers remain exact and zero storage writes occur. [Browser report](browser-report.json). Screens at320×568,390×844,844×390 and1280×900 have ≥44px controls. Physical iPhone Safari and human feel approval remain untested.

Source and deployment receipts follow in PROJECT_STATUS. Publish only this comparison over the previous live source: keep unrelated/private character-study changes out of the deployment. Next action: user compares tile carry, creep, turn, swing and critter positioning with the preserved free-movement version before selecting a direction or integrating it into the adventure.
