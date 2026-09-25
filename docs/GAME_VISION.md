# Critz: Tycoon — Game Vision

This is the source of truth for future development. **Confirmed direction** describes the creator’s established vision, not a claim that every system is implemented. **Slice decisions** are practical choices for this build. **Proposals** remain open. Never silently rename established characters or places or turn proposals into confirmed canon.

## 1. Confirmed identity and appeal

- Title: **Critz: Tycoon**, part of a planned Critz series. Possible sibling games include **Critz: Battlefront** and **Critz: Tower Defense**.
- Cozy, sandbox-like ecosystem and business simulation with top-down RPG exploration. Aim for the colorful exploratory feeling of Pokémon Emerald / a GBA-era RPG, using original assets and presentation.
- The distinctive reward is watching tiny organisms live in beautiful tanks, understanding their relationships, balancing the ecosystem, and gradually automating appropriate care.
- A small, delightful, functioning world is better than a wide, disconnected collection of unfinished menus.
- Phone touchscreen is the primary platform. Keep a visible comfortable D-pad, A (interact/confirm), B (back/cancel), and Start (pause). Landscape and keyboard play remain usable.

## 2. Confirmed protagonist and rival

- Hero is a **ten-year-old Black child**. Player chooses boy or girl and their own name. “Hero” is only a design-document placeholder.
- Rival is the opposite gender and is also named by the player.
- Rival builds tanks and cares intensely about social posts. Both of the rival’s parents live at home and provide a stable environment, making success easier. Hero faces more obstacles. The rival need not be a villain.

## 3. Confirmed opening story

1. Night: Hero is feeding a gecko in their bedroom.
2. Mom bursts in during a meltdown and breaks the bedroom tanks.
3. She is a loving mother who needs medication. Needing medication does not make her a villain. Write her as a person, with affection, remorse, and support; preserve the story’s emotional stakes.
4. **Every escaped animal survives.** Animals hide around the bedroom, house, yard, and eventually Rootport.
5. **Kaid**, Hero’s friend and neighbor, arrives and asks what happened. Always spell this name Kaid, even if transcription says Kade or Cade.
6. Kaid gives Hero a **25-gallon tank** for their approaching birthday. It is a gift regardless of the loan decision.
7. He offers an **optional $100 loan**. Declining makes the start harder. If accepted, the player chooses whether and when to repay him.
8. The scene ends late at night. Hero wakes in bed the next morning. Exploration and player agency begin.

### Confirmed full-game weekly setback — future implementation

- Mom’s medication costs **$20 per in-game week**, purchased at the **Drug Store**.
- In the envisioned full game, missing that purchase causes Mom to break **every tank Hero currently has at home**.
- The next morning, the animals hide around Rootport for Hero to find. **No escaped real-world animals die in these events.** The setback and search are intended mechanics.
- This mechanic is recorded faithfully but **not active in this first slice**. The pharmacy explicitly explains this. Do not imply a deadline exists while it does not.
- If implemented later, make timing and consequences clear and recovery achievable. Further writing/design review should preserve Mom’s humanity and avoid equating medication needs with villainy. This is a fictional character-specific story, not a general claim about mental illness.

## 4. Confirmed supporting characters

### Kaid

- Around Hero’s age; ten-year-old friend and next-door neighbor.
- Whimsical, young, anthropomorphic pitcher-like appearance, inspired by the energy of the Kool-Aid Man but with an **original actual design**. No copyrighted mascot assets.
- Associated with **Glow n’ Blow**, the glass shop. His involvement must suit his age and the playful world.
- Slice decision: a small teal glass pitcher child, warm amber contents, handle, shorts and shoes. Aunt Ember (new supporting character) does the hot glasswork; Kaid draws shapes, chooses safe corners, decorates cool glass, and helps with safe shop tasks. He does not operate a furnace.

### Professor Nugget

- Herpetologist and mentor.
- Gives Hero a notebook for sketches and journal entries about animals.
- Full-game observation and behavioral study should deepen entries and teach better habitat design.
- Slice: found near the Vet, grants the notebook, offers habitat advice, and pays a small community rescue reward.

## 5. Confirmed geography

**Rootport** is Hero’s hometown. Hero, Kaid, and the rival have neighboring homes.

| Location | Role |
| --- | --- |
| Critz | Pet shop; suitable supplies and eventual appropriate animal sales |
| Vet | Veterinary care |
| Drug Store | Pharmacy; Mom’s medication |
| Bike Shop | Skateboards, bikes, OneWheels, other faster transport |
| Glow n’ Blow | Glass shop and Kaid connection |
| Liarsville | Neighboring town |
| Short forest route | Connects Rootport and Liarsville like an early RPG route |

Later areas may include a forest, cave, snowy mountains, and beach. Much later, snorkeling may let the player observe ocean life. These are future areas, not accessible slice content. Schools were considered and **deliberately left out for now**. Do not silently rename any established place.

## 6. Confirmed tank interaction and ecosystem direction

Approach a bedroom tank and press A. The first-level menu has exactly:

- **Manage**: configure and care for the tank.
- **Stats**: inspect conditions, plants, organism populations, trends, births, deaths, and changes over time.
- **View**: watch animals closely, frame photos or videos, and post to Critter.

Envisioned types: aquariums, terrariums, later paludariums and other forms. Plants, microorganisms, decomposers, and animals influence one another. Reward reasoning and make causes and effects observable. Do not reduce everything to an unexplained health score.

The goal is to make habitats as self-sustaining as realistic, or automate care that remains necessary. A mostly plant-based sealed terrarium has different limits than a habitat containing larger animals. **Do not imply a frog or gecko can simply be sealed away without care.** Ventilation, heat, food, water, species suitability and eventual equipment matter.

The opening gift is **25 gallons**. A **50-gallon tank** was discussed as a possible early larger tank, not the starter gift.

## 7. Confirmed business and Critter direction

- **Critter** is the fictional social platform in this world. Hero posts photos and videos of tanks.
- Implement a transparent, fun approximation of recommendations. Visible factors include animal activity, composition, tank appearance, rarity, and audience interest. Views yield game ad revenue.
- Good work brings clients commissioning tanks. Hero builds and ships commissioned tanks from home.
- Other earnings: town side quests and appropriate pet-store animal sales.
- Spending: supplies, tanks, upgrades, travel, and family needs.
- Personal tanks are experiments and a portfolio. Audience milestones and larger commissions may drive later progression.
- No real accounts, paid APIs, advertisements, or external social services are needed for the slice.

## 8. Slice decisions (implemented, expandable)

These practical implementation choices are not new immutable canon:

- Plain browser ES modules + Canvas 2D world/art + accessible HTML controls and menus. Node only serves, checks, builds and tests.
- Original code-drawn art, camera-follow town, collision, A-triggered doors, transitions, dialogue and quests.
- One active pre-positioned 25-gallon **ventilated terrarium**, called **Little Root**. Opening tank placement is automatic; free placement and multiple tanks are future work.
- Hero starts with $12, 1 moss cutting and 4 litter portions. Kaid’s accepted loan adds $100; both paths receive the tank. No interest or forced repayment.
- Four rescue groups: Pebble the gecko, Button the land snail, 6 isopods, and 12 springtails. Geckos/snails stay in separate safe Vet habitats. Compatible decomposers move to the starter tank.
- Moss, algae, microbial activity, leaf litter, nutrients, waste, moisture, isopods and springtails form the starter model.
- Real-time animation and deterministic discrete habitat hours. One hour per 8 seconds of active play, with explicit Observe and Rest controls. No offline catch-up.
- Nonlethal learning mode: stress slows visible activity and unsuitable conditions stop breeding. The deaths counter stays at zero. Realistic animal death, extinction and disease systems are not implemented.
- Population caps, conservative resource bounds, a 24-hour history, and causal birth/breeding messages. See SYSTEMS.md for exact equations.
- Critter photos store small actual in-game PNG snapshots. Videos have a real six-second capture countdown but are **simulated posts**, not MP4/WebM exports. Pan/zoom influences composition. A transparent fictional game rate generates revenue.
- Five enterable functional shops, both neighboring homes, Professor Nugget notebook/rescue reward, Mom’s prescription delivery, and loan repayment.
- Recoverability: free water, a free pet-store kit, free repeatable yard foraging, safe animals, and a nonexpiring rescue quest.
- Local save version 1 with backup recovery and error notification. No accounts or server state.

## 9. Planned implementation backlog

Confirmed direction awaiting engineering: species-specific care and habitats; multiple tanks/placement; aquarium and later habitat forms; richer ecosystem relationships; appropriate care automation; animal study and sketches; commissions and home shipping; animal sales; richer town quests; a full weekly family-needs loop; forest route and Liarsville.

Proposals needing design/balance decisions: 50-gallon early upgrade details; specific rare species and rarity tiers; audience milestones; progression gates; later biomes, snorkeling and ocean observation; exact transport catalog; sophisticated framing/activity scoring; sandbox difficulty settings. Possible sibling Critz titles are a series vision, not work included in this repository.

No placeholder button should pretend any of these systems exists. Keep the README and this document aligned with actual implementation.

## 10. Next development milestone

Give the existing loop an emotionally meaningful goal: build a suitable gecko habitat and bring Pebble home. Fund it through one small client commission, then extend the tank model to multiple instances. Preserve the deterministic simulation boundaries, schema migration, mobile controls, and narrative facts above.
