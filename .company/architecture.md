# Architecture — TPCT profile README redesign (size M)

## Approach
The profile is a static `README.md` plus SVG assets in the repo. Two kinds of SVG:
1. **Hand-made static SVGs** (`assets/hero-{dark,light}.svg`): brand hero, committed once.
2. **Generated SVGs** (`assets/generated/*.svg`): GitHub stats and featured-repo cards, built by
   `scripts/generate.py` (Python 3 stdlib only) from the GitHub GraphQL API. A scheduled GitHub Action
   regenerates them daily and commits only when the output changed.

Everything else (positioning line, CTAs, stack, private work, contact) is **real Markdown text**, not SVG:
it is responsive, accessible, searchable, and readable on mobile, where a 1000px-wide SVG is scaled to about 0.35x.

## Components
| Path | Kind | Owner ticket |
|---|---|---|
| `assets/hero-dark.svg`, `assets/hero-light.svg` | static SVG, viewBox 1000x320 | T-001 |
| `scripts/generate.py` | generator (stdlib: `urllib`, `json`, `html`, `argparse`) | T-002 |
| `scripts/fixtures/sample.json` | offline fixture with the same shape as the API data | T-002 |
| `scripts/test_generate.py` | `unittest` tests | T-002 |
| `.github/workflows/profile.yml` | daily + manual + push(scripts/**, workflow) | T-002 |
| `assets/generated/stats-{dark,light}.svg` | viewBox 1000x300 | T-002 (output) |
| `assets/generated/repo-<Name>-{dark,light}.svg` | viewBox 500x200, 6 repos | T-002 (output) |
| `README.md` | Markdown + `<picture>` | T-003 |

## Theming
Every custom SVG has a dark and a light file. The README switches between them with
`<picture><source media="(prefers-color-scheme: dark)" srcset="dark.svg"><img src="light.svg"></picture>`, and GitHub
follows the viewer's GitHub theme for that query.
Rejected alternative: a single SVG with `@media (prefers-color-scheme)` inside. When the SVG is shown in an `<img>`, it
follows the OS theme, not the GitHub theme, so it can mismatch.

Tokens (shared with the portfolio, from `profile-readme-design-tokens.md`):
- Dark: bg `#0B0D12`, surface `#12151C`, border `#232836`, text `#E6E8EE`, muted `#8B93A7`, cyan `#22D3EE`
- Light: bg `#FFFFFF`, surface `#F6F7FB`, border `#E3E6EF`, text `#0F1222`, muted `#5B6478`, cyan-on-light `#0E7490` (for contrast)
- Accent gradient `#7C3AED` to `#4F46E5`
- Sans: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif`
- Mono: `ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace`

## Data (GraphQL, `user(login: "TPCT")`)
Use `user(login:)`, not `viewer`, because `viewer` does not work with the Actions installation token.
- `createdAt`: gives years on GitHub as `floor((today - createdAt).days / 365.25)`
- `contributionsCollection.contributionCalendar.totalContributions`: contributions in the last 12 months. This
  already includes private (restricted) contributions when the profile setting is on. **Do not add
  `restrictedContributionsCount` again**, because that would double-count. (Measured 2026-10-21: total 8667, restricted 8278.)
- `repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100, after:)`, paginated: totalCount,
  sum of `stargazerCount`, and `languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } }`
- Featured repos: `repository(owner: "TPCT", name: X) { name stargazerCount primaryLanguage { name color } url }`

## Workflow
`on: schedule (daily 03:17 UTC), workflow_dispatch, push to main with paths scripts/** and .github/workflows/profile.yml`.
`permissions: contents: write`. `concurrency: profile-assets`. Token: `secrets.PROFILE_TOKEN || secrets.GITHUB_TOKEN`
(the optional PAT exists in case the installation token cannot see contribution data). Commits use the
`github-actions[bot]` identity only when `git status --porcelain assets/generated` is non-empty.
No loop is possible: generated commits only touch `assets/generated/**`, which is not in the push paths, and pushes made
with GITHUB_TOKEN do not trigger workflows anyway.
Output is deterministic: no timestamps, stable ordering. Re-runs only produce diffs when the data changes.

## Key decisions
- D1: Stats are self-generated. No public stats instances (github-readme-stats and similar), because they are flaky and rate-limited.
- D2: No contribution snake (Platane/snk). It adds an extra branch and moving noise and does not fit the restrained premium
  look. It can be added later.
- D3: Private work and stack are Markdown, not SVG, for mobile readability and accessibility.
- D4: 6 featured repos: JenDock, tpct-mac-theme, Egyptian-National-ID, order-payment-api, social-media-scheduler,
  palm-resources-01. palm-resources-02 is dropped as a near-duplicate of 01, and 6 cards fill a 2x3 grid.
- D5: Repo cards show stars only when the count is 1 or more, so "0 stars" does not weaken the cards. Descriptions are curated in
  the script config, because several repos have no GitHub description.
- D6: Stats metrics: Contributions (last 12 months), Public repositories, Stars earned, Years on GitHub, plus the top 6 languages
  by bytes (excluding markup/config: HTML, CSS, SCSS, Less, Jupyter Notebook, Makefile, Dockerfile, Procfile,
  Batchfile), with the rest grouped as "Other".
- D7: Hero animation is limited to one subtle cyan status-dot pulse, wrapped in `@media (prefers-reduced-motion: no-preference)`.
  Generated SVGs are fully static.

## Risks
- Card text is small on phones (a 2-column table of 500px cards scales to about 0.3x). Mitigation: large card type (name 28px,
  description 19px), alt text = "name: description", and the README remains a 2-column grid by design (GitHub allows no CSS).
- SVG text width depends on the viewer's fonts. Mitigation: width budget at 0.56em per char (sans), at least 40px right padding,
  render check with Chrome headless or Inkscape.
- Installation token may not return contribution data. Mitigation: optional `PROFILE_TOKEN` secret, and the script fails
  loudly (non-zero exit, no files written) instead of writing zeros.

## Test strategy
- `xmllint --noout` on every SVG.
- `python3 -m py_compile scripts/generate.py` and `python3 -m unittest discover -s scripts -p 'test_*.py'`.
- Offline render from fixture: `python3 scripts/generate.py --fixture scripts/fixtures/sample.json --out <dir>`.
- Visual check: Chrome headless screenshots into `.company/runs/renders/` (gitignored).
- At the merge gate, the orchestrator runs a real generation with `GITHUB_TOKEN=$(gh auth token)`, then checks the README on github.com in dark and light themes.
