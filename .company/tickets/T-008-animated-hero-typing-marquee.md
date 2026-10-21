# T-008 — More motion: hero sweep/glow, typing role line, tech-stack marquee (M)

Owner feedback: wants more animation and eye-catching visuals. GitHub limits: SVG in <img> — CSS/SMIL inside the SVG only, no JS, no external refs/fonts.
Brand tokens: see T-007 ticket table (.company/tickets/T-007-shiftcodes-brand.md) — use exactly those. Keep motion subtle, everything inside
`@media (prefers-reduced-motion: no-preference)` (SMIL can't be media-gated: prefer CSS animations; if SMIL is used, the static first frame must look complete). Every SVG ≤ 150 KB (aim ≤ 20 KB). Both themes for every asset.

## Files (only these)
assets/hero-dark.svg, assets/hero-light.svg (edit), assets/typing-dark.svg, assets/typing-light.svg (new),
assets/stack-dark.svg, assets/stack-light.svg (new), README.md.

## 1. Hero (keep existing layout, text, S mark paths and entrance/drift animations from T-007)
- Gradient sweep across the S mark: a diagonal light band (white → transparent, ~30% opacity dark / ~45% light) clipped to the S-mark shape (clipPath reusing the same 5 paths via <use> or duplicate), sweeping every ~6s (after the entrance, start at 2.2s).
- Glow behind the mark gently breathes (opacity/scale 0.85↔1, 5s alternate).
- Accent rule under the name: a shimmer moving along it (gradient position animation, 4s).
- Static render (no motion) must look identical to T-007's.

## 2. Typing role line — `assets/typing-{dark,light}.svg`, 1000x64
Centered monospace-free sans text (Outfit/'Plus Jakarta Sans'/system stack, 26px, weight 600, fg colour) cycling through 4 phrases with a typewriter
effect and blinking caret (brand colour):
"Founder @ ShiftCodes" · "Systems Architect" · "Laravel · Python · Docker" · "I build ERP, LMS and gaming platforms".
Technique: each phrase is its own <text> with a clipPath/mask rect whose width animates with `steps(n)` (n = char count), phrase visible only during its slot (total cycle ~16s, 4s per phrase: type 1.6s, hold 1.4s, erase 0.6s, gap 0.4s); caret follows the reveal edge (animate translateX with same steps), blinks while holding.
Text width: compute per phrase with a char-width estimate (0.56em) and centre each; ensure the longest phrase fits in 940px.
Static/no-motion: show the first phrase fully, no caret blink. Transparent background (no card) so it sits on GitHub's page; colours per theme.

## 3. Tech-stack marquee — `assets/stack-{dark,light}.svg`, 1000x72
Two rows? No — one row of pill chips (rx 18, plate fill + border token, label fg 15px weight 600, a small 8px dot in brand/secondary gradient before each label) for:
PHP, Laravel, Filament, Livewire, Python, Django, FastAPI, TypeScript, React, Next.js, Node.js, Tailwind CSS, PostgreSQL, MySQL, Redis, Docker, Nginx, Linux, GitHub Actions.
Content duplicated once and translated left continuously (linear, ~40s per loop, seamless: translate by exactly one set's width). Left/right edges fade (mask with linear gradient alpha). Transparent background. Static: first chips visible, no motion.

## 4. README.md
- Directly under the hero `<picture>` add the typing `<picture>` (dark/light, width="100%", alt "Founder @ ShiftCodes · Systems Architect · Laravel · Python · Docker · I build ERP, LMS and gaming platforms").
- In "## Stack": keep the table, and put the marquee `<picture>` (width="100%", alt "Tech stack: …list…") directly above it.
- Add a new section after "## GitHub stats" stats picture + its <sub> note:
```
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/TPCT/TPCT/output/snake-dark.svg">
  <img src="https://raw.githubusercontent.com/TPCT/TPCT/output/snake-light.svg" width="100%" alt="Contribution graph being eaten by a snake, in ShiftCodes violet.">
</picture>
```
(The `output` branch is produced by T-009's workflow.) Nothing else changes.

## Acceptance
- xmllint OK on all 6 SVGs; no `http` except SVG namespace; sizes listed in report.
- Inkscape renders (static frame) of each to /tmp look complete and on-brand; for typing, also check the longest phrase fits (render with the clip removed).
- Open each SVG in headless Chrome/Chromium if available and take 2 screenshots ~1.5 s apart to confirm motion; if Chrome can't run, say so.
No commits/push. Don't touch scripts/ or .github/.
