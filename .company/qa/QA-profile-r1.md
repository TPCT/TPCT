# QA — github.com/TPCT profile (2026-10-21) — PASS
Eyes-on in the built-in browser against the live profile after commit b29b377 (+ bot refresh adac658):
- Desktop 1440px, dark: hero dark variant, badges, stack table, featured cards 2 per row, private-work table, stats, contact.
- Desktop pane ~800px, dark: cards 1 per row, legible.
- Mobile 375px, light: light variants; cards full width and legible; no horizontal scroll.
- JS check: 11/11 README images loaded (naturalWidth > 0, after a fresh load), contact shows th3professionalcod3r@gmail.com, no eslamjackie.
- An earlier transient "broken images" state was a browser-pane emulation artifact (all light images incl. unchanged hero; standalone decode OK; fine after reload).
- Action "Profile assets": runs 39529653708, 39530081924, 39530411399 green; Summary: contributions=8672, public repos=83, stars=17 (Actions token sees the full calendar).
Known/manual: profile bio still the old "# Hi there… 👋" text — gh token lacks `user` scope, so not changed.

## r2 (after T-006 Prism alignment, commit 5167c28) — PASS
- Live github.com/TPCT, 1440px dark: Prism hero (gradient name, glass prism + spectrum), new badge colors; 11/11 images loaded (naturalWidth>0).
- Profile bio now: "Founder @shiftcodes · Systems Architect · Senior Full-Stack Engineer (Laravel · Python · Docker). Portfolio: tpct.github.io".
- Action run 39535598683 green.

## r3 (after T-007 ShiftCodes brand, commit a7afc8d) — PASS
- Live github.com/TPCT 1440px dark: violet hero with ShiftCodes S mark, violet badges; 11/11 images loaded.
- 375px light: light hero/S mark, 11/11 images loaded, scrollWidth 375 (no horizontal scroll).
- Action run 39539711108 green (contributions=8753).

## r4 (after T-008/T-009 motion, commit c6e7d36) — PASS
- Local preview (python http.server + browser pane): typing line cycles phrases with caret; marquee scrolls; hero S mark animates in, complete afterwards; Codex Chrome check confirmed card/stats motion.
- Live github.com/TPCT 1440px dark: 14/14 README images loaded (hero, typing, badges, marquee, 6 cards, stats, snake); violet snake renders.
- 375px light: 14/14 loaded, scrollWidth 375.
- Workflows: Snake 39540372991 green (output/snake-{dark,light}.svg 84,116 B each, < 150 KB); Profile assets 39540372967 green.
