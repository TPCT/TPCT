# T-004 — Featured repo cards readable on mobile (S)

## Problem (eyes-on, 375px viewport on github.com/TPCT)
The featured cards sit in a 2-column `<table>`, so on mobile each card renders ~150px wide and its text is unreadable.

## Goal
Cards flow two per row on desktop and become one full-width card per row on mobile.

## Files
- `README.md` — only the "## Featured projects" section.
- `scripts/generate.py`, `scripts/test_generate.py` — repo-card typography only.
- `assets/generated/repo-*.svg` — regenerate from the fixture is NOT what we commit; orchestrator regenerates with the real token. Do not hand-edit generated SVGs.

## Spec
1. Replace the `<table>` in "Featured projects" with a `<p align="center">` containing the six `<a href="https://github.com/TPCT/<repo>"><picture><source media="(prefers-color-scheme: dark)" srcset="./assets/generated/repo-<repo>-dark.svg"><img src="./assets/generated/repo-<repo>-light.svg" width="380" alt="(same alt as now)"></picture></a>` elements, one per line, in the same order. Fixed `width="380"` (no %) so GitHub's `max-width:100%` makes them full-width on narrow screens. Keep everything else in README byte-identical.
2. In the repo-card SVG generator: keep the 500x200 viewBox, but raise readability: title font-size >= 26, description font-size >= 18 with line wrapping recalculated so text never exceeds x=470 and never overlaps the footer row (use at most 3 description lines; ellipsize the last line if needed); footer (language/stars/tag) font-size >= 15. Keep the theme palettes and determinism. Update/add unit tests for the wrapping limit (no line longer than the computed max chars; max 3 lines).

## Acceptance
- `python3 -m unittest discover -s scripts -p 'test_*.py'` passes (PYTHONDONTWRITEBYTECODE=1).
- Fixture run (`python3 scripts/generate.py --fixture scripts/fixtures/sample.json --out .company/runs/gen` or the flag the script uses) → all SVGs pass `xmllint --noout`; render 2 cards with inkscape to PNG under /tmp and confirm no clipping/overlap.
- README: no `<table>` in Featured projects; 6 links, 6 pictures, each img width="380".

## Constraints
No commits/push. Run only affected tests. Do not touch other README sections, the workflow, or hero SVGs.
