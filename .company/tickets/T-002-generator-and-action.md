# T-002: Stats + repo-card SVG generator and daily GitHub Action
Size: M   Depends on: none (can run in parallel with T-001)   Stories: brief must-have 3, 5, 7

## Context
The profile README (repo TPCT/TPCT) needs reliable GitHub stats and pinned-style cards for the featured repos, in dark and light
variants. We do not use public stats services (they are flaky). Instead, a Python stdlib script reads the GitHub GraphQL API and writes
static SVGs into `assets/generated/`, and a scheduled Action refreshes them. Read `.company/architecture.md` first
(sections "Data", "Workflow", "Key decisions" D4-D7, "Theming").
The repo has no scripts or workflows yet. README wiring is T-003, so do not touch README.md.

## Task
Create these files:
1. `scripts/generate.py`: the generator (Python 3.10+, **stdlib only**).
2. `scripts/fixtures/sample.json`: offline fixture in the normalized data shape (see Interfaces).
3. `scripts/test_generate.py`: `unittest` tests.
4. `.github/workflows/profile.yml`: exact content given below.

Do **not** commit generated SVGs from fixture data into `assets/generated/`. When verifying, render into `.company/runs/gen/`.
The orchestrator will run the real generation into `assets/generated/` with a real token.

### Config (top of generate.py, module-level constants)
```python
LOGIN = "TPCT"
FEATURED = [  # order = README order
    {"name": "JenDock", "tag": "CI/CD · DOCKER",
     "description": "Self-hosted CI/CD for Docker Compose: Jenkinsfile pipelines, health checks, auto-rollback."},
    {"name": "tpct-mac-theme", "tag": "GNOME · GTK",
     "description": "macOS-style GNOME desktop: GTK4/GTK3 and Shell theme, global menu and desktop widgets."},
    {"name": "Egyptian-National-ID", "tag": "DJANGO REST",
     "description": "Django REST API that validates Egyptian national IDs and extracts birth date, gender, region."},
    {"name": "order-payment-api", "tag": "LARAVEL · JWT",
     "description": "Laravel REST API for users, products, orders and payments, secured with JWT."},
    {"name": "social-media-scheduler", "tag": "LARAVEL",
     "description": "Laravel app that schedules and auto-publishes posts across social platforms, with analytics."},
    {"name": "palm-resources-01", "tag": "FIREBASE",
     "description": "Idempotent exercise-session ingest on Firebase Functions and Firestore, in TypeScript."},
]
EXCLUDED_LANGUAGES = {"HTML", "CSS", "SCSS", "Less", "Jupyter Notebook", "Makefile", "Dockerfile", "Procfile", "Batchfile"}
TOP_LANGUAGES = 6
THEMES = {
    "dark":  {"bg": "#0B0D12", "surface": "#12151C", "border": "#232836", "text": "#E6E8EE", "muted": "#8B93A7", "cyan": "#22D3EE"},
    "light": {"bg": "#FFFFFF", "surface": "#F6F7FB", "border": "#E3E6EF", "text": "#0F1222", "muted": "#5B6478", "cyan": "#0E7490"},
}
ACCENT = ("#7C3AED", "#4F46E5")
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
```
The `·` is U+00B7. Write the file as UTF-8 and write SVGs with `encoding="utf-8"`. Also add an
`<?xml version="1.0" encoding="UTF-8"?>` prolog to each SVG.

### CLI
```
python3 scripts/generate.py [--out DIR] [--fixture PATH] [--dump-fixture PATH] [--today YYYY-MM-DD]
```
- `--out`: default `assets/generated`, resolved relative to the repo root (the parent of `scripts/`), not the cwd.
- `--fixture`: load normalized data from JSON and make no network calls. Without it, read the token from env `GITHUB_TOKEN`
  (exit code 2 with message `GITHUB_TOKEN is not set` if missing).
- `--dump-fixture`: after fetching, also write the normalized data as pretty JSON (indent 2, sorted keys) to PATH.
- `--today`: date override for the "years" metric. Default `datetime.now(timezone.utc).date()`.
- Print one line per file: `updated <path>` or `unchanged <path>`, then `N file(s) updated`. Exit 0.
- On any API or render error: print to stderr, exit 1, and **write no files**. Render everything into memory first, then write.

### Functions (exact names; tests import them)
```python
def graphql(token: str, query: str, variables: dict | None = None) -> dict
    # POST https://api.github.com/graphql, headers: Authorization: bearer <token>, User-Agent: TPCT-profile-generator,
    # Content-Type: application/json. timeout=30. Up to 3 attempts on urllib.error.URLError / HTTP 5xx (sleep 2s between).
    # Raise RuntimeError on HTTP 4xx, or if the JSON has a non-empty "errors" key. Return payload["data"].
def fetch(token: str, login: str = LOGIN) -> dict          # returns normalized data (shape below)
def aggregate_languages(languages: dict[str, dict]) -> list[tuple[str, float, str]]
    # input {name: {"size": int, "color": str|None}}; drop EXCLUDED_LANGUAGES; sort by size desc then name;
    # keep TOP_LANGUAGES; if the remainder > 0, append ("Other", pct, None). pct is a percentage of the included total (sum = 100).
    # Return [(name, pct, color)]. Empty input returns [].
def text_width(text: str, size: float, mono: bool = False) -> float   # len(text) * size * (0.62 if mono else 0.56)
def wrap(text: str, size: float, max_width: float, max_lines: int) -> list[str]
    # greedy word wrap using text_width; raise ValueError if a word alone is too wide or more than max_lines are needed
def years_on_github(created_at: str, today: date) -> int   # floor((today - created_date).days / 365.25)
def render_card(repo: dict, data: dict, theme: str) -> str   # repo = one FEATURED entry
def render_stats(data: dict, theme: str, today: date) -> str
def write_if_changed(path: Path, content: str) -> bool
def main(argv: list[str] | None = None) -> int
```
Escape every dynamic string with `html.escape(s, quote=True)`.

### GraphQL
Query 1 (paginate with `after` until `hasNextPage` is false):
```graphql
query($login: String!, $after: String) {
  user(login: $login) {
    createdAt
    contributionsCollection { contributionCalendar { totalContributions } }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100, after: $after) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }
    }
  }
}
```
Query 2 (one request, aliases `r0..r5` built from FEATURED):
`r0: repository(owner: "TPCT", name: "JenDock") { name stargazerCount primaryLanguage { name color } }` and so on.
If `user` is null or any featured repository is null, raise RuntimeError naming it.
`contributions_last_year` = `contributionCalendar.totalContributions` **only**. Do not add restrictedContributionsCount, because it
is already included (see architecture "Data").

## Interfaces
### Normalized data (also the fixture format)
```json
{
  "login": "TPCT",
  "created_at": "2016-05-27T01:13:01Z",
  "contributions_last_year": 8667,
  "public_repos": 83,
  "total_stars": 17,
  "languages": {"PHP": {"size": 9100000, "color": "#4F5D95"}, "Python": {"size": 4200000, "color": "#3572A5"}},
  "featured": {"JenDock": {"stars": 1, "language": "Python", "language_color": "#3572A5"}}
}
```
`featured` has one key per FEATURED name. `language` and `language_color` may be null. If `language` is null, omit the dot and language text entirely. The fixture must contain all 6 featured repos and at least 9 languages, including `HTML` and `CSS`, so exclusion and "Other"
are exercised. Use realistic values: PHP, Python, TypeScript, JavaScript, Blade, C#, Shell, Vue, HTML, CSS with GitHub colors
(Blade `#f7523f`, C# `#178600`, Shell `#89e051`, Vue `#41b883`, TypeScript `#3178c6`, JavaScript `#f1e05a`, HTML `#e34c26`, CSS `#663399`).
Featured stars: JenDock 1, all others 0. Languages: JenDock Python, tpct-mac-theme JavaScript, Egyptian-National-ID Python,
order-payment-api PHP, social-media-scheduler PHP, palm-resources-01 TypeScript.

### Output files (in `--out`)
`stats-dark.svg`, `stats-light.svg`, and `repo-<name>-dark.svg` / `repo-<name>-light.svg` for each FEATURED name (exact case,
e.g. `repo-JenDock-dark.svg`). That is 14 files in total.

### Repo card spec: `width="500" height="200" viewBox="0 0 500 200"`, role="img", `<title>` = `<name>: <description>`
Colors are from THEMES[theme]. Define `linearGradient id="accent"` (ACCENT[0] to ACCENT[1], horizontal).
- Background `<rect x="0.5" y="0.5" width="499" height="199" rx="16" fill=surface stroke=border/>`
- Accent tick `<rect x="24" y="24" width="32" height="4" rx="2" fill="url(#accent)"/>`
- Name: x=24, y=64, sans 26px weight 700, fill text.
- Description: `wrap(description, 19, 452, 3)`. Lines at x=24, baselines y=100, 126, 152. sans 19px, fill muted.
- Footer baseline y=182:
  - if language: `<circle cx="30" cy="176" r="6" fill=language_color or muted/>`, then the language text at x=44, sans 17px, muted.
  - if stars >= 1: a 5-point star polygon (outer r=7, inner r=3, point up, fill muted), centered at
    x = (44 + text_width(language,17) + 22 if language else 30), cy=176. Then the star count text at star_cx + 12, y=182, sans 17px, muted.
    If stars == 0, draw no star and no count.
  - tag: x=476, y=182, `text-anchor="end"`, mono 15px weight 600, letter-spacing 1, fill cyan.
- Validation: raise ValueError if the name is wider than 452 at 26px, or if the tag is longer than 22 chars.

### Stats spec: `width="1000" height="320" viewBox="0 0 1000 320"`, role="img", `<title>GitHub stats for TPCT</title>`
- Background `<rect x="0.5" y="0.5" width="999" height="319" rx="20" fill=bg stroke=border/>`
- Label `GITHUB ACTIVITY` at x=40, y=52, mono 16px weight 600, letter-spacing 3, fill cyan.
- 4 metrics. Column x = 40, 270, 500, 730. Value baseline y=118, sans 44px weight 800, fill text, formatted `f"{n:,}"`. Label
  baseline y=148, sans 17px, fill muted. Order and labels:
  `contributions_last_year` "Contributions (12 mo)", `public_repos` "Public repositories", `total_stars` "Stars earned",
  years_on_github "Years on GitHub".
- Divider `<line x1="40" y1="176" x2="960" y2="176" stroke=border/>`
- Label `TOP LANGUAGES · BY CODE SIZE` at x=40, y=208, mono 14px weight 600, letter-spacing 2, fill muted.
- Bar: clipPath `<rect x="40" y="222" width="920" height="12" rx="6"/>`. Segments are consecutive rects, width = 920*pct/100
  (minimum 2), inside the clip, fill = color (`Other` or null color uses muted).
  Add a 2px gap: draw a bg-colored separator line between segments, or reduce each width by 2. Either way the total is 920.
- Legend: up to 7 entries in 4 columns (x = 40, 270, 500, 730), rows at baseline y=270 and y=298. Each entry is a circle r=5 at
  (col+5, baseline-5) filled with the color, then text at col+18: `<name> <pct:.1f>%`, sans 16px. Name is fill text, pct is fill muted (use `<tspan>`).
- If aggregate_languages returns [], omit the bar and legend.

### Workflow: `.github/workflows/profile.yml` (exact)
```yaml
name: Profile assets

on:
  schedule:
    - cron: "17 3 * * *"
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - "scripts/**"
      - ".github/workflows/profile.yml"

permissions:
  contents: write

concurrency:
  group: profile-assets
  cancel-in-progress: false

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4

      - name: Test generator
        run: python3 -m unittest discover -s scripts -p 'test_*.py'

      - name: Generate SVGs
        env:
          GITHUB_TOKEN: ${{ secrets.PROFILE_TOKEN || secrets.GITHUB_TOKEN }}
        run: python3 scripts/generate.py --out assets/generated

      - name: Commit if changed
        run: |
          if [ -z "$(git status --porcelain assets/generated)" ]; then
            echo "No changes"
            exit 0
          fi
          git config user.name "github-actions[bot]"
          git config user.email "41898333+github-actions[bot]@users.noreply.github.com"
          git add assets/generated
          git commit -m "chore: refresh generated profile assets"
          git pull --rebase origin main
          git push origin HEAD:main
```

## Constraints
- Stdlib only (no pip installs, no requirements.txt). Python 3.10+ syntax is fine.
- Output must be deterministic: no timestamps or random ids, a fixed attribute order, and `\n` line endings. Two runs on the same data
  produce byte-identical files.
- No external references in SVGs (no fonts, images, `href` to http, or scripts). No animations in generated SVGs.
- Never print the token. The token is only in the Authorization header.
- Do not touch README.md, `assets/` (except reading), or `.company/` (except writing renders into `.company/runs/`).
- No commits and no push.
- Assumptions (decided by the Tech Lead): 6 featured repos as listed (palm-resources-02 dropped as near-duplicate). Stars are hidden when 0.
  No contribution snake. Optional `PROFILE_TOKEN` secret is a fallback if GITHUB_TOKEN cannot read contribution data.

## Acceptance criteria
- [ ] `python3 -m py_compile scripts/generate.py scripts/test_generate.py` passes.
- [ ] All tests pass (command below).
- [ ] `python3 scripts/generate.py --fixture scripts/fixtures/sample.json --out .company/runs/gen --today 2026-10-21` writes 14 files.
      A second identical run prints `0 file(s) updated`.
- [ ] Every generated SVG passes `xmllint --noout`, and its only `http` string is the SVG namespace.
- [ ] Without `--fixture` and without `GITHUB_TOKEN`, the script exits 2 with the message. A GraphQL `errors` payload makes it exit 1 and write no files.
- [ ] Rendered PNGs (dark + light) of stats and of 2 cards (JenDock and Egyptian-National-ID) show no clipped or overlapping text.
- [ ] Workflow YAML parses: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/profile.yml`
      (PyYAML is installed system-wide, but the script itself must still be stdlib-only).

## Tests
`scripts/test_generate.py` (unittest, imports `generate` after inserting the `scripts/` dir into `sys.path`) must cover:
1. `wrap`: splits on words; respects max width; raises ValueError for too many lines and for a single over-wide word.
2. Every FEATURED description fits `wrap(desc, 19, 452, 3)`, every tag is 22 chars or less, and every name fits 452px at 26px.
3. `aggregate_languages`: excludes HTML/CSS; top 6 + "Other"; pct sums to 100 (within 0.01); empty input returns [].
4. `years_on_github("2016-05-27T01:13:01Z", date(2026, 10, 21)) == 10`.
5. Rendering from the fixture: each SVG parses with `xml.etree.ElementTree`, has width/height/viewBox, and contains no `http` other than the namespace.
   Rendering twice is identical.
6. Card with stars 0 contains no `<polygon`. Card with stars 1 contains one.
7. Escaping: a description containing `&` and `<` produces valid XML.
8. `graphql` raises RuntimeError on an `{"errors": [...]}` response (mock `urllib.request.urlopen`).
9. `main([... --fixture ..., --out tmpdir])` writes 14 files and returns 0. A second run updates 0 files.

Run only:
```bash
cd /home/tpct/TPCT-profile
python3 -m py_compile scripts/generate.py scripts/test_generate.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
python3 scripts/generate.py --fixture scripts/fixtures/sample.json --out .company/runs/gen --today 2026-10-21
xmllint --noout .company/runs/gen/*.svg
mkdir -p .company/runs/renders
for t in dark light; do
  google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars --window-size=1000,320 \
    --screenshot=$PWD/.company/runs/renders/stats-$t.png file://$PWD/.company/runs/gen/stats-$t.svg
  for r in JenDock Egyptian-National-ID; do
    google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars --window-size=500,200 \
      --screenshot=$PWD/.company/runs/renders/repo-$r-$t.png file://$PWD/.company/runs/gen/repo-$r-$t.svg
  done
done
# fallback: inkscape <svg> --export-type=png --export-filename=<png>
```
Network-dependent real run (orchestrator only, not Codex): `GITHUB_TOKEN=$(gh auth token) python3 scripts/generate.py`.

## Out of scope
README.md (T-003), hero (T-001), contribution snake, repo topics/descriptions on GitHub itself.
