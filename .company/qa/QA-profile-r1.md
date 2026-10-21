# QA — github.com/TPCT profile (2026-10-21) — PASS
Eyes-on in the built-in browser against the live profile after commit b29b377 (+ bot refresh adac658):
- Desktop 1440px, dark: hero dark variant, badges, stack table, featured cards 2 per row, private-work table, stats, contact.
- Desktop pane ~800px, dark: cards 1 per row, legible.
- Mobile 375px, light: light variants; cards full width and legible; no horizontal scroll.
- JS check: 11/11 README images loaded (naturalWidth > 0, after a fresh load), contact shows th3professionalcod3r@gmail.com, no eslamjackie.
- An earlier transient "broken images" state was a browser-pane emulation artifact (all light images incl. unchanged hero; standalone decode OK; fine after reload).
- Action "Profile assets": runs 39529653708, 39530081924, 39530411399 green; Summary: contributions=8672, public repos=83, stars=17 (Actions token sees the full calendar).
Known/manual: profile bio still the old "# Hi there… 👋" text — gh token lacks `user` scope, so not changed.
