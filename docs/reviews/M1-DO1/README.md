# M1.DO1 — Walk through every entrance

The user wants door travel by walking, without selecting an option or pressing A. Automatic entry already existed, but two home-yard thresholds were unreachable: the house door at `(8,3)` fell above the yard’s permitted walking row, and the gate at `(8,11)` was removed by the connected-floor boundary pass. Both are now explicitly authored portals. Only those cells open; adjoining walls, fences and out-of-map positions remain blocked.

All 26 live entrances now declare an entry direction. Completing the entrance step automatically travels; sideways storefront movement does not. Door prompts read “Walk ↑/↓ · destination” instead of presenting an A action. Town-guide instructions use walking throughout. The optional existing A shortcut remains for compatibility; no door requires it. Arrival positions, saves, story restrictions, stairs, names and care/economy behavior remain intact.

## Reference and decisions

Pinned `pret/pokeemerald` revision `5eff78649e7170a877b961ef0b3da13b81a16038`: [field input processing](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/field_control_avatar.c#L145-L180) distinguishes step/held-direction warp handling from A interactions. This is source inspection, not emulator observation. Critz retains its completed-step fade, original art and optional shortcut; exact Emerald door-animation reproduction is not claimed.

## Checks

[101 unit checks](unit-results.txt) pass, including every entrance’s walkable approach, complete step and safe arrival; all directions; exact yard boundary exceptions; and existing story, save, collision and stair checks.

[28 isolated browser scenarios](report.json) cover all 26 entrances with movement only, no A or confirmation. Both previously blocked yard portals use real touch D-pad input; other entrances use keyboard. Each verifies no premature warp, no immediate return, no opened option panel, and preserved money/debt/tank gift. Additional checks cover sideways storefront crossing and runtime/asset errors. Phone screenshots inspected. An initial asynchronous test poll returned before travel; replacing it with explicit state sampling resolved the false bounce report. No physical Safari testing is claimed.

![Walk into the house](yard-home.png)
![Walk through the yard gate](yard-gate.png)

Clean-release and publication evidence will be recorded after verification. Existing unfinished character work is excluded.
