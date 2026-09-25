# Critz: Tycoon workflow

- Work directly on `main`. Do not create development branches or worktrees. Inspect existing branches/PRs when locating prior work; do not delete them or publish/close them as a side effect.
- Before changing the game, read `docs/PROJECT_STATUS.md`, `docs/PROJECT_PLAN.md`, `docs/ART_BIBLE.md`, and the relevant parts of `docs/REFERENCE_MEASUREMENTS.md`. Check actual Git status and state the active task ID and deliverable.
- `docs/GAME_VISION.md` remains the story/design source of truth. The visual-foundation plan controls current sequencing; the vision's older “next milestone” is deferred, not cancelled or implemented.
- Work on one implementation task at a time, within the currently authorized milestone. Research/checks may run in parallel. Use planned, in progress, awaiting review, blocked, and complete states honestly.
- M0 is documentation/audit only. M1 visual approval and M2 movement/feel approval must come from the user. Never self-approve artwork, silently cross a review gate, or expand the roster/world before its gate.
- Distinguish reference-verified facts, proposed Critz decisions, and unresolved measurements. Pin reference revisions. Source inspection is not emulator/frame-capture observation.
- Preserve player names, Black child Hero, child Kaid/rival, adult Mom/Professor Nugget, compassionate story, surviving animals, 25-gallon gift, optional $100 loan, Rootport names, Manage/Stats/View, ecosystem causes, Critter earnings, and existing progress.
- Preserve save keys and v1 data until a tested migration exists. Never test against a user's real browser storage. Use isolated browser contexts and synthetic fixtures.
- Keep appearance separate from collision, interaction, warp, and gameplay data. Ship original reusable PNG assets with stable IDs and metadata; do not ship reference-game sprites.
- Run checks relevant to the change. Record actual results, limitations, approval evidence, branch/verified commit, and exact next action in status before ending. Provide a preview or exact launch instructions. Code/art being written is not completion.
- Routine authorized edits/tests need no additional permission. Review gates require a concrete visual/playable deliverable and the user's response.
