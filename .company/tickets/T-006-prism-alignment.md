# T-006 — Align README visuals with the portfolio's Prism design language (M)

Context: the portfolio (https://tpct.github.io, sibling repo /home/tpct/TPCT.github.io) is being reskinned to the owner's "Prism" design
language — spec: /home/tpct/TPCT.github.io/.company/ux-prism.md (READ §1–§3 tokens and the hero prism section; do NOT edit that repo).
The profile README currently uses violet/indigo/cyan tokens on near-black. Make the README read as the same brand.

## Tokens to use (from ux-prism.md)
| role | dark | light |
|---|---|---|
| canvas (SVG card background) | #1A1726 with subtle field: radial #302038 (top-left) + #202C43 (right) over #1D192C→#151321 | #FBFAFF plate on field #FCE3EF / #D3E5F3 hints (keep subtle) |
| plate / surface | #2B2638 | #FBFAFF |
| border | #4A4159 | #D9D2E8 |
| fg / fg2 / muted | #F1ECF8 / #CFC6DC / #B7ACC6 | #2B253B / #5D536D / #62586E |
| brand (pink/berry) | #F299C4 | #A8125A |
| crown (violet) | #C3AEF5 | #6945BD |
| cyan text | #7FD3E3 | #146A86 |
| prism spectrum 1–4 | #F299C4 #C3AEF5 #88C8FC #7FD3E3 | #E0569A #8E6BE0 #3E9BE0 #2BB3C9 |
| accent gradient (bars, rules, name) | brand → crown (55%) → cyan | same, light values |
Labels: no monospace any more — small labels are system-sans 700/800 UPPERCASE with letter-spacing ~1.5px, colored cyan-text.
Fonts: SVGs in GitHub <img> cannot load web fonts; use `Outfit, 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif` (display 800 for names) so it upgrades where installed. Keep all text-fit margins.

## Changes
1. `assets/hero-dark.svg`, `assets/hero-light.svg` (1000x320, keep size/accessibility/title/desc and the same text content):
   - Background: rounded plate (rx 20) with the Prism field (two soft radial glows plum + ink-blue, dark; pink + sky, light).
   - Name "Islam Elsayed" filled with the accent gradient (brand→crown→cyan). Label line in Prism label style (cyan, uppercase sans).
   - Replace the stacked-panel decoration on the right with the **prism**: a faceted glass triangle (~170px tall) built from 3 facets
     (linear gradients of prism-1..4 at different angles, semi-transparent, white 1px hairline rim), a thin white beam (dark: rgba(255,255,255,.85); light: rgba(43,37,59,.55)) entering from the left at a slight upward angle, and a spectrum fan leaving to the right (4 bands prism-1..4, opacity ~.6, fading out). Soft glow behind (glow-a pink, glow-b cyan).
   - Motion (subtle, CSS in <style>, only under `@media (prefers-reduced-motion: no-preference)`): beam opacity pulse 4s, spectrum breathe (opacity .45↔.75) 6s. Nothing else moves.
   - Text must stay left of x=560. Validate with xmllint; render with inkscape to /tmp and inspect.
2. `scripts/generate.py` (+ tests if they assert colors/fonts): replace both theme palettes for stats and repo cards with the tokens above; card top accent bar and stats rule use the brand→crown→cyan gradient; tag text and section labels use cyan-text in the uppercase-sans label style (drop the monospace font); card background = plate with border; titles fg 700/800; descriptions muted. Keep layout/wrapping/determinism and the language-color logic. Update the fixture-based tests accordingly.
3. `README.md` — badges only: Portfolio badge color `A8125A`, ShiftCodes `6945BD`, Email `2B2638` (same labels/links/logos). Nothing else changes.

## Acceptance
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'` passes.
- Fixture generation to /tmp → xmllint OK; render one card + stats + both heroes with inkscape to /tmp; visually: no clipping/overlap, Prism colors, readable contrast (muted text on plate ≥ 4.5:1).
- No external references in any SVG (only the SVG namespace URL). Each hero ≤ 10 KB.

## Constraints
No commits/push. Only these files. Do not touch the workflow or other README sections. Do not edit /home/tpct/TPCT.github.io.
