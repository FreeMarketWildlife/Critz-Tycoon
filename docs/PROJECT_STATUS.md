# Project status

Updated **2026-09-24 (America/Los_Angeles)**. Current milestone: **M0 — Audit and production plan, complete**. Active implementation task: **none**. Last completed task: **M0.3**. Next planned task: **M1.1**, after the user authorizes M1. This session was explicitly limited to M0.

## Approval state

- Approved by user: main-only workflow; original Emerald-generation visual target;240×160 / 8×8 / 16×16 native standard; preservation requirements; staged M0–M7 progression.
- M0 documents delivered. No art/feel approvals have been requested or assumed. **G1 and G2 are not approved.**
- No approved example images, final palette, lineup, bedroom art or movement harness exists. ART_BIBLE proposals remain proposals. Completing this audit does not start M1.

## Completed and verified

| Task | State | Evidence |
| --- | --- | --- |
| M0.1 — existing implementation audit | Complete | Located playable PR/branch, read vision/systems/QA/source/tests, recorded discrepancies and save/gameplay contracts in [AUDIT_M0.md](AUDIT_M0.md); reran baseline. |
| M0.2 — reference measurements | Complete for M0 evidence scope | Pinned Emerald source; measured 7 representative sprite sheets/all 9 poses; reference pixel/tile/palette, movement/cadence/camera ledger, confidence and unresolved register. [Reference measurements](REFERENCE_MEASUREMENTS.md), [raw bounds](reference-data/emerald-sprite-bounds.json), [reproduction script](reference-data/measure-sprites.py). No emulator capture claimed. |
| M0.3 — production/resume documents | Complete | [Plan](PROJECT_PLAN.md), [art bible](ART_BIBLE.md), this status, [decision log](DECISIONS.md), root [AGENTS.md](../AGENTS.md), README sequencing/main update. No gameplay implementation. |

Baseline verification: **10/10 domain/world tests**, **14/14 reported browser checkpoints**, four JS syntax checks and static build pass. Browser uncaught errors: 0. Chrome 153.0.8010.54 with Playwright 1.62.1 in an isolated context; viewport sizes 320×568, 390×844, 844×390, 1280×900. [Raw browser report](verification/M0_BROWSER_BASELINE.json). Unit tests exercise both loan choices; browser walkthrough exercises girl Hero/accepted loan only. Browser reload asserts name/money/post count/rescues, not a full tank/inventory equality check. Physical iPhone/Safari and true multi-touch are untested. See audit for the complete gap list.

Documentation validation: local Markdown file links resolve; sprite measurement script reproduces the checked-in JSON against the pinned external checkout; whitespace checks pass; runtime/test/build source files and GAME_VISION remain identical to the playable commit. Reference PNGs were inspected/measured externally and are not shipped in this repository.

## Repository state and source of truth

- Working repository: `/Users/tanoshi/Documents/ChatGPT/Critz-Tycoon`.
- Remote: `https://github.com/FreeMarketWildlife/Critz-Tycoon.git`.
- Current local branch: **main**; no new branch/worktree created.
- Last verified gameplay baseline (before documentation commits): **`191e3a6b7721d8193f47914c6f7afa1d50b70dbc`** (existing playable foundation).
- Remote main at initial M0 inspection: **`9f14c4fbc4fc1e8ca4ca59c171488896c36f9dcc`**, initial README. The playable foundation was fast-forwarded from the already-existing `feature/playable-foundation` history.
- [PR #1](https://github.com/FreeMarketWildlife/Critz-Tycoon/pull/1) was open at the original inspection. The user subsequently authorized committing and pushing all pending project work directly to GitHub `main`. This delivery includes the existing playable commits, M0 documents, reference evidence, workflow instructions and phone link. Use `git log -1` and compare `HEAD` with `origin/main` for the delivery SHA; the gameplay baseline above does not include the documentation commits. No gameplay code was changed for this delivery.
- `docs/GAME_VISION.md` unchanged; blob `a92234f4c79dc202cd8d9e8e5be372cde31270d7`. Its habitat/commission next-feature suggestion is deferred by current visual-foundation sequencing. Canon and implemented/future distinctions remain authoritative.

## Open issues and pending decisions

Reference unknowns U001–U008 are tracked in [REFERENCE_MEASUREMENTS.md](REFERENCE_MEASUREMENTS.md): semantic head/eye annotation, exact reference environmental assemblies, displayed animation phase boundaries, door/fade duration, camera capture/script exceptions, phone scale/readability, palette/Kaid silhouette approval, run permissions/skateboard/catch-up policies. These do not block delivering an honest M0 ledger; do not call them reference-exact when building the proofs.

Preservation risks to address at M2–M4: fractional-foot v1 positions; strict schema 1 without migration; generic unchecked fallback spawn; collision coupled to artwork bounds; old diagonal/path-helper assumptions; missing optional-field/reload assertions; fixed-clock changes accidentally altering habitat or payment time. Keep the primary/backup keys, scene/entity IDs, all story flags, saved PNG post images, balances and simulation intact. No save migration was needed or performed in M0.

## Exact next action and M1 review deliverable

Latest user direction: prepare a self-contained prompt for a separate ChatGPT Astra / Ultra chat to create an illustrated art bible and **ten shared Hero/rival candidates: five boys and five girls, one identical south-facing idle pose each, on one still comparison sheet**. The player-selected gender is Hero and the opposite gender is rival; this is not twenty separate-role designs. [Copy-ready prompt](ART_BIBLE_NEW_CHAT_PROMPT.md). This session supplies the prompt and standing delivery instructions, not new artwork. External output must return for review before being treated as approved or integrated. The earlier broader M1 lineup below remains follow-up context, not the immediate ten-option assignment.

**Wait for instruction to begin M1, then start only M1.1.** Produce seven original characters: boy Hero, girl Hero, boy rival, girl rival, Kaid, Mom and Professor Nugget, using the proposed shared 16×32 frame and measured visible-size range. Show front and side poses together, including both Kaid side views, with baseline/frame guides on a separate overlay. Hero must read as a ten-year-old Black child; children/adults differ in silhouette without doubled canvases; Kaid is a small original pitcher child.

After M1.1, M1.2 adds **one 240×160 bedroom composition** using reusable draft tiles: bed, desk, chair, shelf, window, stairs/door, plant/rug and 25-gallon tank, with Hero and Mom together for scale. Deliver native 1× and exact 4× nearest-neighbor PNG views (bedroom enlargement 960×640), draft tiles/sprite sheets, editable sources, palette/metadata and a ground/occlusion guide. G1 asks the user to approve or revise proportions, silhouettes, colors, perspective and room scale. No roster/world expansion or M2 movement begins before that approval.

## Resume in a fresh session

1. Read this status, PROJECT_PLAN, ART_BIBLE, relevant REFERENCE_MEASUREMENTS, DECISIONS and GAME_VISION; inspect AGENTS.
2. Run `git status --short --branch`, `git branch --show-current`, `git log -5 --oneline`, and check remotes/PR state if needed. Stay on main; protect all existing local edits. Do not repeat the already-completed foundation fast-forward blindly.
3. Confirm the user's current milestone authorization. State task ID/deliverable before edits. If user has not authorized M1, do not create art or change runtime.
4. Use recorded reference revisions and hashes; do not replace verified facts with generic “retro” defaults. Resolve or label uncertainties at the relevant gate.
5. At completion run relevant checks, update task/approval state, record exact next action and verified commit/artifact revision, and deliver native/enlarged or playable review evidence as appropriate.

## Launch and reproduce baseline

From this prepared working copy with Node 20+ and npm on PATH:

```sh
cd /Users/tanoshi/Documents/ChatGPT/Critz-Tycoon
npm run dev
```

Open [local game](http://localhost:5173). M0 does not change its appearance. This machine currently exposes bundled Node but not npm; this exact command works without installation:

```sh
cd /Users/tanoshi/Documents/ChatGPT/Critz-Tycoon
/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node scripts/serve.mjs
```

Baseline commands actually used (package-script equivalents):

```sh
export PATH=/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin:$PATH
node --check src/main.js && node --check src/state.js && node --check src/world.js && node --check src/art.js
node --test tests/*.test.mjs
node scripts/build.mjs
export CODEX_PRIMARY_RUNTIME_NODE_MODULES=/Users/tanoshi/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules
export CHROMIUM_EXECUTABLE='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
node tests/browser.mjs
git diff --check
```

The browser runner starts/stops its own server at 127.0.0.1:5177 and uses isolated storage. Ordinary launch uses localhost:5173; changing browser origin/port changes which save slot is visible. No preview server is promised to remain running after M0. The main-branch delivery includes the source needed for a fresh GitHub clone.

## Phone-testing link — hosting verification follow-up

The user requested a phone-playable link and authorized publishing as needed. Sites reports an existing successful version 1 deployment at [Play Critz: Tycoon](https://critz-tycoon.freemarketwildlife.chatgpt.site). Access remains owner-only; sign in with the owner's account if prompted. No new deployment was necessary and no access policy was changed.

Verified hosting source commit: `e64d5ea16be908d90995ea16dffb56f36437ae73` (separate from the local GitHub baseline; source equality has not been checked). Saved version: `appgprj_6ab5dd1e11ac8191937254280d6ba196~appgver_5aec90aa6f208191ab9a7c3f3ad0546e`. Deployment: `appgdep_6ab5dd4db9608191a338dfbdc9786320`, native status `succeeded`, no failure message. Earlier notes that this audit did not deploy remain true, but must not be read as saying no hosted version exists. This is the existing playable prototype, not M1 artwork. M1 authorization/approval state is unchanged.

Standing delivery policy now recorded in AGENTS: commit and push completed requested changes to `origin/main` after relevant checks, without another confirmation; separately publish and verify changes affecting the playable build through the existing Sites project. Documentation-only updates are pushed without implying a new game deployment. This prompt/workflow update changes no game code or artwork; the phone build remains unchanged. Resume by checking actual HEAD/remote state rather than treating the earlier baseline SHA as the latest documentation commit.
