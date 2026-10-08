# M1.UI2 — Uninterrupted play area

User request: remove all popup tips and top text; fill the top with the game.

The world fills the available screen above the touch controls, with a right control column on short landscape screens. No brand header, HUD, quest strip, proximity prompt, location banner, reward toast or footer tips remain. Money/place/time are in Start, objectives in Notebook, and help/studio links in Town guide. Story dialogue and character reactions remain. Action and save feedback appears inline only in a menu the player opened, with nonvisual accessible announcements outside menus. Background save errors are retained for the next menu.

The framebuffer expands its field of view with uniform nearest-neighbor scale. Terrain culling, camera bounds and lighting cover its actual dimensions. Dialogue does not resize the view or shift its camera. No asset pixels, movement rules, game save keys or serialized state schema changed.

## Validation

Working-tree checks: 115 tracked unit tests; nine new screen checks, 17 contact/dialogue checks, eight menu/dialogue/NPC checks. Browser contexts are isolated with synthetic saves. Screenshots inspected at phone and landscape sizes. The unrelated untracked appearance test is excluded because its pending 24×32 atlas work is not part of this deliverable. Clean-release regression checks and publication receipt will follow.

Physical Safari has not been tested. This is implementation evidence, not user approval of the wider M1/M2 artwork/motion gates. Exact next action: complete clean-release checks, publish the identical build, then user reviews the quieter expanded play screen.
