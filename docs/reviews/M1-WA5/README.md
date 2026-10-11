# M1.WA5 — Enclosed deep-water review

[Open phone demo](https://critz-tycoon.freemarketwildlife.chatgpt.site/art-review/water.html). Left: shallow/deep still water. Right: shallow/deep moving water. Walk the complete shallow ring; the deeper center is blocked. Visit buttons place the player at each example.

The authoritative [mixed-depth enclosure rule](../../ART_BIBLE.md#m1wa5--enclosed-deep-water-and-submerged-depth-banks) requires a full shallow border including diagonal corners. This replaces the depth stripes that met land in the user screenshots. The standalone puddle remains shallow still water.

Original art uses a stepped cap, recessed rock face and dark toe. The new depth extension has188 tiles (47 masks × freshwater/ocean × still/moving), with Tiled metadata. Existing6,648 tile IDs and3.2-second surface loops remain unchanged. The recessed top face is deeper than the side/bottom rim to show the overhead viewing angle. Entire deep cells are collision-blocked; this bank is not a jumpable ledge.

Reference: user screenshots and pinned [Emerald movement source](https://github.com/pret/pokeemerald/blob/5eff78649e7170a877b961ef0b3da13b81a16038/src/event_object_movement.c). Source distinguishes directional ledge behavior; our deep-water bank is a Critz collision/art decision. No source art is shipped, no new exact Emerald pixel measurement or emulator observation is claimed.

Validation:185 unit tests;41 isolated browser scenarios (11 water,8 clouds,14 clock/sleep,8 deep boundary approaches). Desktop and phone render screenshots inspected. All4 sides of both deep pools reject walking. Synthetic save fixtures verify unchanged money/debt/flags and v1 slot. Physical Safari remains unverified. New visuals await user feedback. Publication receipts accompany this review after deployment.
