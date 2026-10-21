# T-010 — Animated Experience timeline + impact numbers (M)

Owner supplied full experience (source, read-only: /home/tpct/TPCT.github.io/.company/private/experience.md — public LinkedIn facts, OK to use as stated).
Same rules as T-007/T-008: brand tokens table in .company/tickets/T-007-shiftcodes-brand.md, CSS animation inside the SVG only, all motion inside
`@media (prefers-reduced-motion: no-preference)` with `animation-fill-mode: backwards` so the static frame is complete; no external refs; font stack
`Outfit, 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif`; each SVG ≤ 30 KB; both themes; transparent outer background is NOT wanted here — use the plate card (rx 20, plate fill + border token, subtle field glow) like the stats card.

## Mobile legibility rule (important)
These SVGs use a **640px-wide viewBox** and are placed in README with `width="640"` (not 100%). Desktop shows them at 640px; on phones GitHub scales them to ~340px (×0.53). So minimum font sizes: body ≥ 20px, labels ≥ 16px, numbers ≥ 44px.

## Files (only these)
assets/impact-dark.svg, assets/impact-light.svg, assets/experience-dark.svg, assets/experience-light.svg (new), README.md.

## 1. Impact numbers — `assets/impact-{dark,light}.svg`, viewBox 640x300
2×2 tiles (each inner plate-raised rect, rx 14). Each tile: big value (accent gradient fill, 800, 46–52px) + label (muted, 18–20px, ≤ 2 lines):
- "9+ yrs" — "shipping production software since 2017"
- "~250" — "freelance projects delivered"
- "3 s → 500 ms" — "Oracle queries on 100M+ rows (Kearney)"   (value can be 40px if needed to fit; must fit tile)
- "$15k → $2k" — "monthly server cost after re-architecture (IPXBit)"
Motion: tiles fade/slide up staggered (120 ms), the arrow "→" in the two before/after values nudges right once (or the "after" value fades in 300 ms after the "before"); a slow sheen sweeps across the card every ~7s. Label "IMPACT" in the secondary colour uppercase small label at top-left (16px, letter-spacing 1.5px) — adjust height if needed (≤ 340).

## 2. Experience timeline — `assets/experience-{dark,light}.svg`, viewBox 640 x (fit, ≤ 760)
Label "EXPERIENCE" at top. Vertical timeline at x≈36: a line (border token) plus an overlay line in the accent gradient that **draws** top→bottom on load (stroke-dashoffset, 1.6s). Each entry: node dot (brand gradient; current roles get a softly pulsing ring, infinite 2.4s), then:
- line 1: Role — bold fg 21px
- line 2: Company · dates — secondary colour 17px
- line 3 (optional): one short impact phrase — muted 17px (≤ 1 line, ellipsize by shortening text yourself; nothing overflows x=616)
Entries, in order (group header "NOW" before the first three, "PREVIOUSLY" before the rest, label style):
NOW
1. CEO — ShiftCodes Digital Technologies · 2026 – now — "Software studio for custom business platforms"
2. Senior Technical Team Lead & Consultant — Monglish International Academy · 2026 – now — "Technical leadership for the academy's platforms"
3. Senior Technical Team Lead & Consultant — Edulixa360 · 2026 – now — "Leading the EdTech platform engineering team"
PREVIOUSLY
4. Senior Software Engineer — Kearney · 2024 – 2026 — "National waste-analytics platform: queries 3 s → 500 ms"
5. CTO — IPXBit Tech Solution · 2025 — "Microservices → modular monolith; servers $15k → $2k"
6. Team Lead, Senior Full-Stack — dot.jo · 2023 – 2025 — "Headless Filament CMS: delivery 1 month → 4 days"
7. CTO — Venu Dine · 2022 – 2023 — "Multi-vendor restaurant APIs, 200k+ daily requests"
8. Senior Software Engineer — Everything To Gain · 2025 – 2026 — "Multi-tenant Laravel/FastAPI/.NET apps"
(Role lines that are too long for one line at 21px: shorten wording sensibly, e.g. "Sr. Technical Team Lead & Consultant"; never wrap.)
Entries fade/slide in staggered (90 ms each) following the line draw.

## 3. README.md
Insert a new section right after the "## About" section (before "## Stack"):
```
## Experience

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/impact-dark.svg">
    <img src="./assets/impact-light.svg" width="640" alt="Impact: 9+ years shipping production software; about 250 freelance projects; Oracle queries from 3 s to 500 ms on 100M+ rows; server cost from $15k to $2k per month.">
  </picture>
</p>
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/experience-dark.svg">
    <img src="./assets/experience-light.svg" width="640" alt="Experience: CEO at ShiftCodes; Senior Technical Team Lead and Consultant at Monglish International Academy and at Edulixa360 (2026 to now). Previously Senior Software Engineer at Kearney, CTO at IPXBit, Team Lead at dot.jo, CTO at Venu Dine, Senior Software Engineer at Everything To Gain.">
  </picture>
</p>

<sub>Full history on <a href="https://tpct.github.io">tpct.github.io</a> and LinkedIn.</sub>
```
Hmm — no LinkedIn URL is known; write the sub line as: `<sub>Full history and case studies on <a href="https://tpct.github.io"><b>tpct.github.io</b></a></sub>` and centre it inside a `<p align="center">`. Nothing else in README changes.

## Acceptance
- xmllint OK on 4 SVGs; only the SVG namespace URL; sizes listed.
- Inkscape static renders to /tmp: all text inside bounds, no overlap, both themes on-brand; check min font sizes by grepping font-size values.
- Headless Chrome (run outside the sandbox if needed) 2 screenshots ~1.2 s apart showing motion; static frame complete with reduced motion.
No commits/push. Don't touch scripts/, .github/ or other assets.
