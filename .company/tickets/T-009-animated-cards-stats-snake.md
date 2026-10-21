# T-009 — Animated repo-card borders, animated stats, contribution snake (M)

Owner wants more motion. Same rules as T-008 (CSS inside SVG, reduced-motion gated, static frame complete, ≤150 KB each, both themes, T-007 tokens).

## Files (only these)
scripts/generate.py, scripts/test_generate.py, scripts/fixtures/* (if needed), .github/workflows/snake.yml (new). Do NOT touch README.md, assets/*.svg (hand-made) or .github/workflows/profile.yml.

## 1. Repo cards (generator)
- Animated gradient border: keep the static 1px border token, and overlay a second rounded-rect stroke (1.5px) painted with the accent gradient where a bright segment travels around the card: use `stroke-dasharray` (segment ≈ 18% of perimeter, gap rest) + `stroke-dashoffset` CSS animation (linear, 6s infinite); `pathLength="100"` to make the maths simple. Offset each card's animation-delay deterministically from its index (e.g. -1s * index) so they don't move in lockstep.
- Subtle hover-free lift: none (no JS/hover in img). Keep text layout as is.
## 2. Stats (generator)
- Numbers + labels fade/slide in (translateY 6px → 0, opacity 0→1) staggered 120 ms each; language bar segments grow from 0 to their width (scaleX with transform-origin left, `transform-box: fill-box`), staggered; legend fades in. Use `animation-fill-mode: backwards` so the static frame is complete. Runs once (no loop) except a slow shimmer across the accent rule (6s infinite).
- Everything inside `@media (prefers-reduced-motion: no-preference)`.
## 3. Tests
Update/add unit tests: card SVG contains the animated border element with pathLength 100 and deterministic delays; stats SVG contains reduced-motion media block; output still deterministic (two runs identical); xmllint-valid via fixture run.
## 4. Contribution snake workflow — `.github/workflows/snake.yml`
```
name: Snake
on:
  schedule: [{cron: "17 4 * * *"}]
  workflow_dispatch:
  push:
    branches: [main]
    paths: [".github/workflows/snake.yml"]
permissions:
  contents: write
concurrency: {group: snake, cancel-in-progress: true}
jobs:
  snake:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/snake-light.svg?color_snake=#6E2BFB&color_dots=#EAE5FA,#D9C9FF,#B9A2FF,#8A5BFF,#5A1FE0
            dist/snake-dark.svg?color_snake=#B9A2FF&color_dots=#1E1832,#3B1E86,#5A1FE0,#8A5BFF,#C9B8FF
      - uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
          keep_history: false
          jekyll: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
Validate YAML parses. (Orchestrator triggers it after push and checks the size of the outputs.)

## Acceptance
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'` passes; fixture generation to /tmp → xmllint OK; inkscape static renders of one card + stats (both themes) look unchanged vs T-007; headless Chrome 2 screenshots ~1.5 s apart (if available) show motion.
No commits/push.
