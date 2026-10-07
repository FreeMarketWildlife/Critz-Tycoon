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

### Pixel budget — current preference: exactly 2× Emerald

The current preference is to **lean toward an exactly 2× native pixel budget** rather than staying at the original Emerald resolution.

The proposed relationship is intentionally simple:

| | Pokémon Emerald reference | Proposed Critz target |
| --- | ---: | ---: |
| Native viewport | **240×160 px** | **480×320 px** |
| Visible tile count | **15×10 tiles** | **15×10 tiles** |
| Tile size | **16×16 px** | **32×32 px** |
| Spatial composition | Same 15×10-tile view | Same 15×10-tile view, with 2× pixels per tile |

The reason for doubling the resolution while preserving the same number of visible tiles is to keep the **composition, density, and overworld scale logic** of Pokémon Emerald while giving Critz substantially more room for detail.

For characters, the intended rule is especially important:

- **Every overworld character’s entire body should fit inside one 32×32 tile.**
- Characters should not visually feel two or three tiles tall.
- The world should continue to read on a one-character-per-tile grid, just with a higher-resolution drawing budget inside that tile.
- This is meant to solve some of the current game’s strange scale feeling: characters, structures, terrain, and movement should all feel like they belong to the same coherent tile system.
- The earlier idea of staying at the original Emerald-sized character budget remains useful as evidence that good low-resolution characters are possible, but the current preference is now **2× because it allows more detail without changing the underlying 15×10 composition**.

### Environment depth and transition-tile technique

A major part of making the world feel less flat should be the deliberate use of **boundary/transition tiles that contain two surfaces or elevations at once**.

The desired technique:

- **The core technique:** boundary tiles should visually contain pieces of both neighboring surfaces. For example, one tile might contain rocky ground along its lower portion and the beginning of a lava pool along its upper portion.
- **The illusion of depth:** the boundary tile can be marked impassable in collision. The character’s feet stop at the edge, while the artwork itself blends both surfaces together inside that tile. Visually, this makes the player appear to stand naturally beside a ledge, wall, pool, shoreline, structure, or other elevation change rather than next to a hard square edge.
- **The checkerboard fix:** without transition art, different terrain types can read like flat colored blocks placed next to one another. Baking overlap, lips, borders, shadows, and surface transitions into boundary tiles helps the world feel continuous and spatially layered.
- Collision should remain separate from appearance: a tile may visually contain two surfaces while still being a single blocked or passable gameplay cell according to the map data.
- This should become a consistent environment-art rule for walls, cliffs, water, pools, shorelines, building edges, garden beds, fences, raised terrain, and similar boundaries.

The important visual goal is that Critz should **not look like a checkerboard of isolated 32×32 squares**, even though it is built on a 32×32 placement grid.

### Restricted world palette — proposed direction

The world should also use a deliberately restricted reusable palette instead of freely introducing new colors from asset to asset.

Current proposed palette:

**Row 1 — System, greens / forests, blues / lakes and oceans**

| Role | Hex |
| --- | --- |
| System black | `#000000` |
| Light green | `#C2F3A1` |
| Mid green | `#64CD63` |
| Deep green | `#218739` |
| Dark forest green | `#0E4B1F` |
| Light water blue | `#BCEEFA` |
| Mid water blue | `#46B2E6` |
| Deep water blue | `#1862B5` |
| Dark navy | `#0A2B66` |

**Row 2 — Earth tones & mountains: browns, grays, oranges**

| Role | Hex |
| --- | --- |
| Warm cream | `#FFF4D4` |
| Light tan | `#DEB887` |
| Mid brown | `#9E6A38` |
| Dark brown | `#5E3A1A` |
| Light orange earth | `#DCA060` |
| Deep orange earth | `#A86834` |
| Light gray | `#D2D6DC` |
| Mid gray | `#8A92A6` |
| Dark gray | `#4A5260` |

**Row 3 — Accents & settlements: reds, yellows, purples, shadows**

| Role | Hex |
| --- | --- |
| Bright red | `#FF5252` |
| Deep red | `#B81D24` |
| Bright yellow | `#FFD54F` |
| Deep gold | `#C69500` |
| Light purple | `#D7A6EC` |
| Deep purple | `#803BB0` |
| Purple-black shadow | `#2B1D38` |
| Near-white | `#FDFEFE` |
| Near-black | `#161A1D` |

This palette should be treated as a **strong proposed world palette / starting restriction**, not an excuse to make every asset use every color. Individual sprites and tiles should still use small local subsets and disciplined ramps.

The intended benefit is consistency: forests, lakes, mountains, towns, roofs, paths, shadows, and UI-adjacent world elements should look like they belong to the same game rather than having independently generated palettes.

### Pixel-art principle

The goal is **not** simply to make Pokémon Emerald art twice as large. The goal is to preserve Emerald’s compositional discipline while giving Critz exactly twice the linear pixel resolution to draw with.

That means:

- Same **15×10 visible tile composition**.
- Same grid-based readability and compact overworld feel.
- **32×32 tiles instead of 16×16**.
- Characters contained within a **single 32×32 tile**.
- More pixels available for faces, clothing, silhouettes, materials, foliage, water edges, and animation.
- No smoothing, antialiasing, subpixel placement, or “HD pixel art” shortcuts that undermine the grid.
- More detail should come from better pixel clusters and better drawing, not from making objects arbitrarily larger in tile-space.

### References supplied by the user

The user supplied animated visual references showing both:

- an Emerald-style character redrawn with a larger pixel budget, demonstrating the kind of additional detail a higher-resolution budget can support; and
- a low-resolution character example showing that strong character designs are possible even at an Emerald-like original budget.

The second reference is still useful because it proves that the game does not *need* extra pixels just to make recognizable characters. The current preference for 2× is instead about gaining **more detail while keeping the exact same tile-count composition and compact world scale**.

### Questions to resolve when this enters implementation

- Verify the 480×320 / 32×32 / 15×10 standard in an actual playable scene before making it permanent.
- Build representative Critz characters whose full bodies fit inside a single 32×32 tile.
- Redraw a small environment using the transition-tile technique so walls, water, terrain boundaries, and structures do not read like a checkerboard.
- Test the proposed restricted palette across at least one forest/outdoor scene, one settlement scene, one interior, water, and multiple characters.
- Build one short Emerald-style campaign scene that includes multiple actors, movement, facing, dialogue, a door, an interior exit, and return of player control.
- Review the result at native resolution and at integer display scaling before locking the standard.

This entry records the current design preference and constraints; it does **not** yet replace the current art bible, implementation plan, or existing approval gates.


## IDEA-003 — Creator Easter eggs: real-world critter YouTubers as memorable NPCs and shops

**State:** captured for future planning; not implemented, approved as final content, or assigned to a milestone.  
**Source:** user brainstorming, 2026-10-07, plus linked public creator research. Names and the definitive goldfish exclusivity/shop choice come from the user; additional mechanics, dialogue, and cameo pitches below are proposals.

### Core idea

Fill Critz: Tycoon with discoverable, affectionate Easter eggs referencing successful real-world YouTube creators who care for, breed, study, rescue, or build habitats for animals. These should be **actual in-world shops, specialist NPCs, unusual animal encounters, props, and optional quests**, not just names buried in text. A player who recognizes a creator should have an "I know who that is!" moment; anyone who does not should still see a coherent, useful, charming character in the game. Spread cameos naturally through the world rather than collecting every creator into one location.

### Priority cameo: Luke's Goldies — **Nuggets**

- **Definitive shop sign:** **Nuggets** (NOT "Luke's Nuggets" or "Luke's Nuggies"; those were earlier brainstormed names).
- **Shop owner:** **Luke**, inspired by **Luke Hagopian / Luke's Goldies**, the real-world goldfish keeper and breeder.
- **Hard design rule:** **Nuggets is the ONLY store/location where the player can BUY goldfish in the entire game.** No ordinary pet shop, traveling merchant, online catalog, or other NPC can sell goldfish. Reconcile this exclusive inventory rule with the general pet store and any future catalogs when implemented. Non-purchase ways to obtain goldfish, if any, remain undecided.
- **Core identity:** a specialized goldfish shop, not a general fish retailer. Luke takes his fish seriously; available fancy goldfish variants, proper tank requirements, and their individual personalities can be the shop's main appeal.
- **Character reference supplied in the conversation:** 2026-10-07 uploaded portrait of Luke (IMG_8943.jpeg). Appearance in that supplied image: short dark brown hair; thick eyebrows; full dark brown beard/mustache; friendly expression; red/maroon T-shirt. Use the **uploaded image as the visual reference** when art is commissioned; this chat upload is *not* yet checked in to the repository. The user's identification of the person as Luke Hagopian is treated as the supplied context, not a biometric identification from the portrait.
- **Possible details, not locked:** standout goldfish with names and personalities; a lesson on goldfish care and adequate aquarium sizes; a small side quest about helping a goldfish thrive; special seasonal stock only here.
- **Suggested draft flavor (not approved dialogue):** "Around here, every nugget deserves a good home."

### Priority cameo: SerpaDesign — specialist naturalistic landscaping

- **Real-world inspiration:** **Tanner Serpa / SerpaDesign**, known for planted aquariums, terrariums, vivariums, paludariums, and detailed naturalistic habitats.
- **Proposed in-game role:** a habitat landscaper / aquascaping-and-plant specialist who sells or helps place live plants, moss, substrate, driftwood, rocks, backgrounds, and naturalistic decorative pieces. This preserves the user's preferred **landscaping/plants** direction without locking an exact shop name or inventory.
- **Possible mechanic:** optional enclosure-makeover commissions, teaching players to arrange convincing ecosystems rather than only purchase expensive animals. Potential synergies with tank health, animal enrichment, and player-post aesthetics, pending balance design.
- **Shop name, location, NPC look, stock, and quest are TBD.**

### Two-headed turtle cameo — likely creator identified, not yet confirmed by user

- The user specifically remembers a YouTuber with a **two-headed turtle** and wants an Easter egg in the game, but couldn't recall the creator.
- **Strong candidate:** **Joey Morena (@aqua.terry), AquaTerra Exotic Pets**, whose official site says he cared for a two-headed turtle called **Barf and Belch** and has documented other two-headed animals. This seems especially close to the user's description, **but ask/confirm before locking that identification**.
- Another possible historic match is **Brian Barczyk / The Reptarium**, which also featured a two-headed turtle. Do not imply that the original owner is identified conclusively.
- **Proposed gameplay:** a carefully cared-for, special **non-purchasable** two-headed turtle appears at a sanctuary, exhibition, or specialist's habitat. Learning about it or assisting with an ethical habitat/care quest could unlock a journal entry or decorative reward. Never turn a disability/rare condition into a gimmick, careless breeding target, or routine sellable stock.
- Exact turtle name, NPC, availability, and gameplay impact TBD.

### Additional researched cameo candidates (all optional proposals)

| Real creator / channel | Specialty | Possible Critz cameo, proposed |
| --- | --- | --- |
| **AntsCanada (Mikey Bustos)** | Ant colonies, observation, complex terrarium ecosystems | A dedicated ant-keeper or elaborate ant-farm exhibit; a colony/foraging side quest and interconnected habitat tunnels. |
| **Snake Discovery (Emily and Ed Roberts)** | Reptile education, husbandry, conservation | A reptile education center with handling/care lessons, appropriate husbandry supplies, and safe animal-education missions. |
| **Aquarium Co-Op (Cory McElroy)** | Freshwater fish and aquatic plants, approachable aquarium education | A freshwater mentor, water-testing lessons, aquatic plant and equipment expertise. **Do not stock/sell goldfish**, to preserve Nuggets' unique inventory. |
| **Kamp Kenan (Kenan Harkin)** | Reptiles, tortoises, lizards, conservation | A reptile habitat keeper offering a tortoise-care quest or outdoor reptile exhibit. |
| **Brian Barczyk (legacy tribute)** | Reptiles, The Reptarium, education | A respectful memorial-style reptile exhibit or book/poster tribute rather than assuming a living present-day shopkeeper; permission and depiction to be considered. |

### Design guardrails / open questions

1. Treat creator names, likenesses, slogans, branding, and signature animals as **possible collaborations/tributes**. Check permissions and commercial-use/IP implications before shipping directly recognizable people, brand names, logos, exact likenesses, or real pets. An original, loosely inspired NPC is an alternate route.
2. Do not make real creators sound like they endorsed Critz without approval. Do not assume the creators are participating.
3. **Preserve goldfish exclusivity at Nuggets** even if other fish/plant specialists are added. Ensure goldfish care is accurately represented; goldfish need appropriate space/filtration, not novelty bowls.
4. The user supplied Luke's portrait in this conversation. It needs a separate, approved asset transfer before the repo can use it as a pixel-art character reference; do not claim the image itself has been committed.
5. Prefer optional discovery, easter eggs, specialist shops, and quests that reward curiosity; avoid compulsory cameos blocking the core campaign.
6. Locate each creator cameo and determine prerequisites only after the world/roster review gates. This is an **idea capture only**: no new approved assets, maps, gameplay, or milestone scope.
7. Confirm whether the two-headed turtle reference is **AquaTerra/Barf and Belch**, Brian Barczyk's Reptarium, or someone else; also decide if their iconic animal should be represented by a respectful homage.
8. Later brainstorm more creators by niche (fish, reptiles, amphibians, insects, invertebrates, planted tanks) and give each one a different useful game function rather than repetitive shops.

### Research starting points (checked 2026-10-07)

- Luke Hagopian / Luke's Goldies: https://www.linkedin.com/in/luke-hagopian-7b9b66193 and https://www.youtube.com/channel/UCg0_9roN7QYzFNLjVSD5Z1Q
- Tanner Serpa / SerpaDesign: https://www.serpadesign.com/home and https://www.youtube.com/@SerpaDesign
- AquaTerra Exotic Pets (Joey Morena, Barf and Belch): https://www.aquaterraexoticpets.com/pages/about
- AntsCanada overview: https://journals.sagepub.com/doi/full/10.1177/01622439261442633
- Snake Discovery: https://snakediscovery.com/youtube/
- Aquarium Co-Op / Cory McElroy: https://www.aquariumcoop.com/blogs/meet-the-team/cory-mcelroy
- Kamp Kenan: https://www.youtube.com/watch?v=KoYGHxFF7hI
- Brian Barczyk / Reptarium and two-headed turtle: https://obits.mlive.com/news/brian-barczyk-1969-2024-tiktok-reptile-expert
