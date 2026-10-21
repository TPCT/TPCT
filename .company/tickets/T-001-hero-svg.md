# T-001: Hero SVG (dark + light)
Size: S   Depends on: none (can run in parallel with T-002)   Stories: brief must-have 1, 7

## Context
The GitHub profile README (repo TPCT/TPCT, rendered at https://github.com/TPCT) is being redesigned.
See `.company/brief.md` and `.company/architecture.md` (sections "Theming" and "Key decisions").
Today the hero is `assets/v5-hero.svg` (old style, deleted in T-003). This ticket creates the new hero only.
The README (T-003) will show it via `<picture>`: `hero-dark.svg` for GitHub dark theme and `hero-light.svg` for light.
The positioning sentence and CTA buttons are Markdown under the hero (T-003), **not** in this SVG.

## Task
Create exactly two files:
- `assets/hero-dark.svg`
- `assets/hero-light.svg`

They share the same geometry and differ only in colors and glow opacity.

### Canvas
- Root: `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="320" viewBox="0 0 1000 320" role="img" aria-labelledby="title desc">`
- `<title id="title">Islam Elsayed: Founder @ ShiftCodes, Systems Architect, Senior Full-Stack Engineer</title>`
- `<desc id="desc">Profile banner for Islam Elsayed (TPCT), Alexandria, Egypt.</desc>`
- Background: `<rect x="0.5" y="0.5" width="999" height="319" rx="24" fill="BG" stroke="BORDER"/>`

### Palette
| token | dark | light |
|---|---|---|
| BG | #0B0D12 | #FFFFFF |
| SURFACE | #12151C | #F6F7FB |
| BORDER | #232836 | #E3E6EF |
| TEXT | #E6E8EE | #0F1222 |
| MUTED | #8B93A7 | #5B6478 |
| CYAN | #22D3EE | #0E7490 |
| GLOW opacity | 0.22 | 0.12 |

Accent gradient `id="accent"`: linearGradient x1=0 y1=0 x2=1 y2=0, stops `#7C3AED` at 0 and `#4F46E5` at 1.
Glow `id="glow"`: radialGradient with stop `#7C3AED` at 0 (stop-opacity = GLOW) and `#4F46E5` at 1 (stop-opacity 0).

### Fonts (in a `<style>` block, as classes)
- `.sans { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }`
- `.mono { font-family: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace; }`
No `@import`, no `@font-face`, no external URLs of any kind, no `<image>`, no `<script>`, no `<foreignObject>`.

### Left column (all text `text-anchor="start"`, x = 56)
| id | content | y (baseline) | class / size / weight / fill / extra |
|---|---|---|---|
| `t-label` | `TPCT · ALEXANDRIA, EGYPT` | 76 | mono, 16px, 600, CYAN, `letter-spacing="3"` |
| `t-name` | `Islam Elsayed` | 156 | sans, 72px, 800, TEXT, `letter-spacing="-1.5"` |
| accent bar | `<rect x="56" y="180" width="96" height="6" rx="3" fill="url(#accent)"/>` | | |
| `t-role1` | `Founder @ ShiftCodes` | 232 | sans, 30px, 600, TEXT |
| `t-role2` | `Systems Architect · Senior Full-Stack Engineer` | 270 | sans, 24px, 400, MUTED |

The middle dot is U+00B7 (`·`). Write the `@` literally.

### Right decoration (purely geometric, no text), region x 680..960
1. Glow: `<circle cx="830" cy="160" r="230" fill="url(#glow)"/>`, drawn **before** the left text, right after the background.
2. Three stacked "system layer" panels, each `<rect width="220" height="56" rx="12" fill="SURFACE" stroke="url(#accent)" stroke-width="1.5"/>` at
   (x=712, y=64), (x=736, y=132), (x=712, y=200).
3. Inside each panel: three dots `r="4"` fill MUTED at panel-x + 22, 36, 50 (cy = panel-y + 28), and one bar
   `<rect x="panel-x+70" y="panel-y+24" width="96" height="8" rx="4" fill="MUTED" opacity="0.45"/>`.
4. Connectors: dashed vertical lines `stroke="MUTED" stroke-opacity="0.5" stroke-dasharray="3 5" stroke-width="1.5"` from
   (822, 120) to (846, 132) and from (846, 188) to (822, 200).
5. Status dot: `<circle id="pulse" cx="912" cy="92" r="6" fill="CYAN"/>` on the top panel.

### Motion (only this)
```css
@media (prefers-reduced-motion: no-preference) {
  #pulse { animation: pulse 3.2s ease-in-out infinite; }
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
```
Nothing else moves.

## Interfaces
- File paths are fixed (T-003 references them): `assets/hero-dark.svg`, `assets/hero-light.svg`.
- Text element ids are fixed: `t-label`, `t-name`, `t-role1`, `t-role2` (they are used by the bounds check below).

## Constraints
- Hand-written, readable SVG (2-space indent). Each file 6 KB or less. No editor metadata (no inkscape/sodipodi namespaces).
- Do not touch `README.md`, other files in `assets/`, `scripts/`, or `.github/`.
- No commits and no push. The orchestrator commits.
- Assumption (decided by Tech Lead, no user available): the hero shows no avatar/photo, because an external image would be blocked inside SVG
  and an embedded base64 photo bloats the file. The name carries the identity.

## Acceptance criteria
- [ ] Both files exist, are valid XML (`xmllint --noout`), and contain no `http`/`https` string except the SVG namespace URI.
- [ ] Geometry is identical between dark and light (`diff` shows only color/opacity value changes).
- [ ] With the Inkscape bounds check, every `t-*` element has right edge 660 or less (so text never collides with the decoration) and
      all elements are inside 0..1000 x 0..320.
- [ ] Rendered PNGs show: name legible, no clipped text, the decoration on the right, correct theme colors.
- [ ] Animation exists only on `#pulse` and only inside the reduced-motion media query.

## Tests / verify locally (run only these)
```bash
cd /home/tpct/TPCT-profile
xmllint --noout assets/hero-dark.svg assets/hero-light.svg
grep -n 'http' assets/hero-*.svg | grep -v 'http://www.w3.org/2000/svg' && echo "FAIL external ref" || echo "ok no external refs"
# text bounds (id,x,y,w,h); check x+w <= 660 for t-* ids
for f in assets/hero-dark.svg assets/hero-light.svg; do inkscape --query-all "$f" | grep '^t-' | awk -F, '{r=$2+$4; print $1, r, (r<=660?"ok":"FAIL")}'; done
mkdir -p .company/runs/renders
for t in dark light; do google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars --window-size=1000,320 \
  --screenshot=$PWD/.company/runs/renders/hero-$t.png file://$PWD/assets/hero-$t.svg; done
# fallback if chrome fails: inkscape assets/hero-dark.svg --export-type=png --export-filename=.company/runs/renders/hero-dark.png
```
Open or inspect the PNGs and report what you see.

## Out of scope
README changes, deleting old assets (T-003), generated stats/cards (T-002), section dividers (decided: none).
