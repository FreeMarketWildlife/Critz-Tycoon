# M1.UI2 — Uninterrupted play area

User request: remove all popup tips and top text; fill the top with the game.

The world fills the available screen above the touch controls, with a right control column on short landscape screens. No brand header, HUD, quest strip, proximity prompt, location banner, reward toast or footer tips remain. Money/place/time are in Start, objectives in Notebook, and help/studio links in Town guide. Story dialogue and character reactions remain. Action and save feedback appears inline only in a menu the player opened, with nonvisual accessible announcements outside menus. Background save errors are retained for the next menu.

The framebuffer expands its field of view with uniform nearest-neighbor scale. Terrain culling, camera bounds and lighting cover its actual dimensions. Dialogue does not resize the view or shift its camera. No asset pixels, movement rules, game save keys or serialized state schema changed.

## Validation

Final clean source `8afa556f8167c7ce23321b43451f835922719381` passes all 115 unit tests and all 88 browser checks: nine screen, 17 contact/dialogue, eight UI, 28 doorway, nine fruit and 17 full chapter walkthrough checks. An earlier run caught the removed HUD callback in Nugget’s reward dialogue; it was removed before this final build. Menu status contrast was also corrected after screenshot inspection. Browser contexts use synthetic saves only. The clean release excludes unrelated pending character work; no actual player storage was accessed.

Physical Safari has not been tested. This is implementation evidence, not user approval of the wider M1/M2 artwork/motion gates. Deployment **`appgdep_6ac76282c0fc8191809f82330019503f` succeeded at 2026-10-08 09:29:49 UTC** for source **`8afa556f8167c7ce23321b43451f835922719381`**, pushed and remote-verified on main. All **1,653 tested build files** match the archive; only the hosting manifest is additional. [Phone game](https://critz-tycoon.freemarketwildlife.chatgpt.site) · [Native receipt](deployment.json) · [Archive proof](archive-check.json). Owner-private access and existing saves are preserved. No physical Safari verification is claimed. This final evidence commit changes documentation only and needs no redundant deployment. Exact next action: user reviews the quieter expanded play screen; implementation and publication are complete.

## Screenshots

[Phone world](phone-world.png) · [Landscape world](landscape-world.png) · [Stable dialogue](phone-dialogue.png) · [Inline save error](inline-save-error.png).
