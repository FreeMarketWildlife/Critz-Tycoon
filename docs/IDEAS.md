# Critz: Tycoon — Ideas notebook

A running home for ideas the user wants remembered. Organize future additions by topic with stable idea IDs; preserve names, specifics, and dialogue intent. Recording an idea does not schedule or implement it. [GAME_VISION.md](GAME_VISION.md) remains the story/design source of truth, and [PROJECT_PLAN.md](PROJECT_PLAN.md) controls implementation order and review gates. Reconcile ideas with those documents when they enter implementation planning.

## IDEA-001 — P2W: Peigh, Teawin, and real-money purchases

**State:** captured for future planning; not implemented or assigned to a milestone.  
**Source:** user brainstorming, 2026-09-27. Character/shop details and the proposed offer below come from the user; dialogue is an editable draft based on their wording.

### Characters and shop

- **Peigh** is literally a walking, anthropomorphic dollar sign.
- **Teawin** is a walking, anthropomorphic teacup and Peigh’s wife. She speaks with a sweet Southern-mama warmth and a Southern accent.
- Together they run **P2W**, a shop in **Liarsville**.
- The shop is conspicuously fancy, luxurious, and super clean.
- Everything sold there costs **real-world money**. In-game currency cannot be spent there.
- Prices are stated directly in real dollars. No intermediary premium currency that obscures how much the player is actually spending.

### Scene 1: after the first ad

After the first advertisement shown to the player, Peigh walks up and introduces the shop as somewhere to go if the player gets tired of ads.

**Peigh — draft dialogue:**

> “UGH, ads are the WORST, but I guess the devs have to keep the lights on. If you ever get sick of them like I do, just swing by my shop in Liarsville, and I’ll see what I can do…”

### Scene 2: visiting P2W

When the player eventually visits the luxury shop, Teawin greets them first. Peigh joins the conversation, starts with his sales pitch, then addresses the ads.

**Teawin — draft greeting:**

> “Oh, hi sugar!”

Her conversation with the player continues in that warm Southern voice; the rest of her exchange is still unwritten.

**Peigh — draft dialogue:**

> “Oh, {playerName}! Welcome in, son! As you can see, we have a wonderful selection of things in stock—many limited-time items that you might not ever see again in your life.
>
> “…Oh, you came here about the ads? Yes, of course. Now, I should let you know: your money there is not worth squat to a man like myself. The only money that works here is cold hard cash. Yes, real-world dollars that can buy you food, shelter, and clothing in the real world—that money is what we take here.
>
> “There’s no weird premium currency where we try tricking your brain into forgetting how much you’re actually spending. No, we just straight up tell you what it is.
>
> “So, if you want to get rid of ads forever, that’d be a one-time transaction of $4.99, and you’ll never see another ad in this game ever again. Do we have a deal?”

`{playerName}` represents the actual player-chosen name, not the literal placeholder “Hero.” “Son” preserves the supplied draft; address variants for the chosen Hero remain to be written.

### Offer and merchandise ideas

| Item/category | Captured intent |
| --- | --- |
| Permanent ad removal | One-time **$4.99 USD** purchase; no more ads in this game, forever. |
| Cosmetics | Real-money shop merchandise; specific items and prices TBD. |
| Special fish | Real-money shop merchandise; species, care requirements, prices, and gameplay effects TBD. |
| Premium quests | Real-money shop content; stories, scope, and prices TBD. |
| Limited-time items | Part of Peigh’s sales pitch; actual stock and availability rules TBD. |
| Other merchandise | Room for later ideas; no additional categories specified yet. |

### Details to resolve later

- When and where the first ad appears, and the later ad cadence/formats.
- When Liarsville and P2W become reachable relative to that first encounter.
- Teawin’s full welcome conversation, player responses, and Peigh’s dialogue on return visits.
- The actual catalog, limited-time availability, and balance/progression effects of special fish and premium quests.
- Purchase platform, confirmation/cancellation flow, and how permanent ad-removal ownership is restored across devices or saves.

These are open questions, not additional user decisions. The current playable slice still has no real advertising or purchases. This entry does not authorize adding them or expanding the playable roster/world.


## IDEA-002 — Emerald-faithful campaign presentation, cutscenes, dialogue, doors, and pixel budget

**State:** captured for future planning; not implemented or assigned to a milestone.  
**Source:** user brainstorming and visual references, 2026-10-01.

### Campaign and cutscene direction

The campaign needs a more deliberate way to author and stage cutscenes. The goal is for **Critz cutscenes to behave like Pokémon Emerald cutscenes**, rather than feeling like a separate cinematic camera system.

Key intentions:

- Cutscene staging should follow Pokémon Emerald’s overworld language: actors remain grounded on the map, move on the tile grid, turn to face one another, pause, emote, walk into and out of scenes, and hand control back to the player cleanly.
- The **camera should not crop important actors out of a scene**. Current cutscenes can place characters outside the visible area, which makes conversations hard to follow.
- Cutscene writing should account for the actual viewport from the start. When several characters participate, positioning and camera behavior should be planned so the player can see the people who matter at each beat.
- Avoid treating cutscenes like modern cinematic pans or close-ups unless there is a very specific reason. The default should feel like an Emerald event script happening naturally in the same world the player is already exploring.
- We should eventually develop a reusable **cutscene/campaign scripting format** that makes it easy to describe actor positions, facing directions, movement, pauses, dialogue, camera behavior, exits, and return of player control.

### Dialogue look and feel

Dialogue should also move much closer to the Pokémon Emerald reference.

The intended direction is:

- Text boxes should feel like part of the same visual system as the overworld rather than a generic browser UI.
- Dialogue pacing, line length, box placement, advance behavior, character naming, and conversational rhythm should be studied against Pokémon Emerald.
- The goal is not merely to use a similar border. The **whole interaction should feel like reading dialogue in Pokémon Emerald**: compact, readable, game-native, and tightly coordinated with character movement and facing.
- Dialogue presentation should be reviewed together with cutscene staging, because the visible playfield, actor placement, and text box all compete for the same screen space.

### Doors and exits

Doors should behave **like Pokémon Emerald doors**.

The desired behavior includes:

- Entering a door should use an Emerald-like door transition/animation rather than feeling like an instant generic scene warp.
- Doorways should visually communicate that they are entrances before the player steps into them.
- Indoor exits should also be visually obvious in the Emerald style.
- **Exits should consistently use a small mat, threshold marker, or glowing/clearly marked exit area**, similar to how Pokémon Emerald communicates where the player leaves an interior.
- The player should not have to guess which tile is the exit.
- Door/exit behavior, animation timing, player movement, facing, and scene transition should eventually be treated as one reusable system rather than being improvised per map.

### Character pixel-budget question

The native character pixel budget is **not settled yet**.

Earlier thought: scaling Emerald’s character budget up by exactly 2× might give Critz more room while preserving the same proportions and pixel-art logic.

Latest thought after reviewing additional user-supplied GIF references:

- It appears entirely possible to make appealing, distinct characters **within the original Pokémon Emerald-sized pixel budget**.
- Therefore, Critz may not need a 2× character pixel budget at all.
- The new reference GIF is important because it shows that recognizable, expressive character art can still be achieved with roughly the original Emerald constraints.
- The preference is now to **seriously test the original Emerald budget before increasing it**.
- A larger budget should only be adopted if Critz characters genuinely cannot achieve the needed readability, identity, animation, and charm at the original scale.
- This should be treated as a visual comparison decision, not assumed from theory: create representative Critz characters at the Emerald-like native budget and compare them against a 2× interpretation at equal display scale.

### Pixel-art principle

The broader goal is not “make everything higher resolution because we can.” The goal is to preserve the visual economy that makes Pokémon Emerald readable and charming.

If the original Emerald-scale budget works, prefer it. Extra pixels should only be introduced when they clearly improve Critz rather than simply making the sprites larger or less disciplined.

### References supplied by the user

The user supplied animated visual references showing:

- an Emerald-style character redraw at a higher pixel budget, useful for evaluating a possible 2× approach; and
- a separate low-resolution character example demonstrating that attractive characters can still be made within an Emerald-like original budget.

These references are design evidence for the future comparison, not shipped Critz artwork and not automatic approval of either budget.

### Questions to resolve when this enters implementation

- Define the exact native sprite/frame dimensions being compared as “Emerald budget” versus “2× budget.”
- Identify several representative Critz characters to test, including at least the Hero and characters with unusual silhouettes.
- Build one short Emerald-style campaign scene that includes multiple actors, movement, facing, dialogue, a door, an interior exit, and return of player control.
- Compare camera visibility, dialogue readability, animation readability, and overall charm at native size.
- Only then lock the production pixel budget and reusable cutscene/door/dialogue rules.

This entry records a target and an experiment to run; it does **not** yet replace the current art bible, implementation plan, or existing approval gates.
