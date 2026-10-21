# T-007 — Re-align README with the portfolio's ShiftCodes brand (violet + animated S logo) (M)

Context: the user rejected the berry Prism palette. The portfolio (TPCT/TPCT.github.io @ 5711046, local copy /home/tpct/TPCT.github.io — READ ONLY)
now uses ShiftCodes-logo colours (primary violet #6E2BFB) and the hero shows the animated ShiftCodes "S" mark instead of the prism.
Sources (read only): tokens `src/styles/01-tokens.css`; mark `src/images/brand/shiftcodes-mark.svg` (viewBox 0 0 413 446, 5 paths:
sc-hook-top, sc-hook-bottom, sc-lt, sc-slash, sc-gt — the "S" is two hooks around a `</>`); hero animation `src/styles/40-hero.css` lines ~100–125.

## Tokens (exact, from 01-tokens.css)
| role | dark | light |
|---|---|---|
| canvas / field | #110D1F; field-a #2A1A55, field-b #1B2150, c #160F2A, d #0D0A18 | #EEEBFA; field-a #E4DAFF, b #DCE2FF, c #F3F0FD, d #E7E3F7 |
| plate/surface | #1E1832 | #FCFBFF |
| border | #3A3160 | #D8D1F0 |
| fg / fg2 / muted | #F3F0FF / #CEC6E8 / #ABA1CC | #1C1530 / #4A4266 / #5A5275 |
| brand (text accents) | #B9A2FF | #5B21E6 |
| secondary ("cyan" role, now periwinkle) | #8FA0FF | #3346C4 |
| logo fill gradient a→b→c | #8A5BFF → #6E2BFB → #5A1FE0 | #7B3FFF → #6E2BFB → #5A1FE0 |
| accent / name gradient | #C9B8FF → #8A5BFF (50%) → #8FA0FF | #6E2BFB → #5A1FE0 (55%) → #3346C4 |
| glow | rgb(110 43 251/.45) + rgb(143 160 255/.28) | rgb(110 43 251/.28) + rgb(51 70 196/.18) |

## Changes
1. `assets/hero-dark.svg`, `assets/hero-light.svg` (keep 1000x320, title/desc, same text content and positions, text left of x=560):
   - Replace the prism/beam/spectrum with the ShiftCodes S mark: copy the 5 paths verbatim from shiftcodes-mark.svg into a `<g>` scaled to ~210px tall, centred around x≈790, y≈160; fill with the logo gradient (a→b→c, diagonal). Soft violet glow behind it (two radial glows using the glow tokens). Optional thin orbit ring (stroke = border token, low opacity).
   - Background field and plate with the new tokens; name filled with the accent/name gradient; label line in secondary colour, uppercase sans 700/800 (no monospace); accent rule under the name with the accent gradient.
   - Animation (CSS in <style>, only inside `@media (prefers-reduced-motion: no-preference)`), mirroring the site: entrance — hook-top slides in from (+48,-40) rotate(-8deg), hook-bottom from (-48,+40), `<` from +14px x, `>` from -14px x, `/` from -12px y, staggered (350/470/950/1050/1150 ms), all with opacity 0→1 and `animation-fill-mode: backwards`; then infinite gentle drift (top translate(5px,-4px), bottom translate(-5px,4px), 7s ease-in-out alternate) and a slow cursor-like opacity pulse on `/` (1.6s). Use `transform-box: fill-box; transform-origin: center` where needed. Static (no-motion) rendering must show the full logo.
   - Each hero ≤ 12 KB; no external refs; ids unique within file.
2. `scripts/generate.py` (+ tests): swap both theme palettes for stats + repo cards to the tokens above: plate background with border, card accent bar and stats rule = accent gradient, labels/tags in secondary colour (uppercase sans), titles fg, descriptions muted. Update tests asserting colours. Keep layout/wrapping/determinism and language colours.
3. `README.md` — badges only: Portfolio `6E2BFB`, ShiftCodes `5A1FE0`, Email `1E1832`. Nothing else.

## Acceptance
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'` passes.
- xmllint OK on heroes + fixture output; inkscape renders (to /tmp) of both heroes, one card, stats both themes: logo shape correct (compare with the site's mark), no clipping, muted on plate ≥ 4.5:1.
- grep: no `#F299C4|#A8125A|#C3AEF5|#7FD3E3|#E0569A` left in README/assets/scripts.

## Constraints
No commits/push. Only these files. Do not edit /home/tpct/TPCT.github.io. Workflow untouched.
