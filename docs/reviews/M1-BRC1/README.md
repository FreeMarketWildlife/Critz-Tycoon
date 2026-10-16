# M1.BRC1 — body-region correction editor

Implementation and local verification are complete. Public editor publication is in progress under direct user authorization; hosted route: https://critz-tycoon.freemarketwildlife.chatgpt.site/sprite-editor/?mode=body-regions.

The mode reuses the sprite editor shell and supports pixel labels, stroke undo/redo, isolated autosave, source-bound correction import/export, clipboard fallback, layer visibility/opacity and integer zoom. Initial composition is dummy 100%, reference 40%, labels 60%, in that render order. Artwork, source pixels and game saves are unchanged.

Evidence: 32 focused writer tests; 24 independent Chromium/WebKit browser scenarios; ordinary-editor and workspace browser regressions (10 each); targeted desktop 1024/1366 and WebKit portrait 320/390/430 checks. The 430 viewport is 430×932. Both source layers match the seed RGBA exactly in isolation. Default blend checks cover 743 opaque sites, with maximum rounding difference 0.56 RGB units. Clipboard denial and selectable fallback are tested in isolated contexts. Browser emulation does not establish physical-phone behavior.

Reports are in `independent-review/`. Private browser screenshots remain ignored under `local-review/`. The user directly approved publishing the updated editor, supplied Brendan reference and current dummy on the existing public Critz Tycoon site on October 15, 2026; this supersedes the earlier local-only publication hold. The approved preload is copied byte-for-byte to `sprite-editor/assets/body-regions-seed.json`.

Git base: `eafb945d0e5f4c8f77681cdc4a57bbc4c84b33c4`. Only BRC1 source, tests, approved seed and scoped documentation are included. The deployment will overlay this editor onto the current live version 60 source `bc9f9a54694d67671b60a12fddf05f6b7150699c`, preserving that game's runtime, assets and saves. Creator and gameplay artwork remain paused. Publication receipt follows after deployment verification.
