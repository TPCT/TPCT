# T-003: Rewrite README.md and remove old assets
Size: S   Depends on: T-001 (hero SVGs), T-002 (generator); the orchestrator must have run the real generation so
`assets/generated/*.svg` exist   Stories: brief must-have 1-8

## Context
`README.md` is the GitHub profile page for https://github.com/TPCT. The current README uses old v5 SVGs and a wall of badges.
New assets: `assets/hero-{dark,light}.svg` (T-001) and `assets/generated/stats-{dark,light}.svg` +
`assets/generated/repo-<Name>-{dark,light}.svg` (T-002). See `.company/architecture.md` (Theming, D3, D4).
Text sections are deliberately plain Markdown/HTML for mobile and accessibility.

## Task
1. Replace `README.md` entirely with the content below. Copy it verbatim. The only allowed changes are fixes for a real
   rendering bug, and you must report any change you make.
2. Delete these files (all unused after step 1): `assets/capabilities.svg`, `assets/impact.svg`, `assets/profile-hero.svg`,
   `assets/v3-hero.svg`, `assets/v3-impact.svg`, `assets/v3-metrics.svg`, `assets/v4-architecture.svg`,
   `assets/v4-command-center.svg`, `assets/v4-proof-board.svg`, `assets/v5-hero.svg`, `assets/v5-process.svg`, `assets/v5-proof.svg`.
   Use plain `rm` (or `git rm`, which stages but does not commit). Do not commit.

### README.md content (verbatim)
````markdown
<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/hero-dark.svg">
  <img src="./assets/hero-light.svg" width="100%" alt="Islam Elsayed: Founder @ ShiftCodes, Systems Architect, Senior Full-Stack Engineer. Alexandria, Egypt.">
</picture>

<br>

**I design and build production systems that businesses run on every day:<br>ERP suites, learning and gaming platforms, and the automation behind them.**

<br>

[![Portfolio](https://img.shields.io/badge/Portfolio-tpct.github.io-7C3AED?style=for-the-badge&logo=githubpages&logoColor=white)](https://tpct.github.io)
[![ShiftCodes](https://img.shields.io/badge/ShiftCodes-shiftcodes.net-4F46E5?style=for-the-badge&logo=googlechrome&logoColor=white)](https://shiftcodes.net)
[![Email](https://img.shields.io/badge/Email-eslamjackie%40outlook.com-12151C?style=for-the-badge&logo=microsoftoutlook&logoColor=white)](mailto:eslamjackie@outlook.com)

<sub>Case studies and full project history live on the portfolio: <a href="https://tpct.github.io"><b>tpct.github.io</b></a></sub>

</div>

## About

- Founder of **[ShiftCodes](https://shiftcodes.net)**, a software studio that builds custom business platforms.
- Systems architect and senior full-stack engineer: Laravel and Python at the core, Docker and Linux on the server.
- I care about modular architecture, clean APIs, role-based access, and delivery pipelines that make shipping safe.

## Stack

| Area | Tools |
|---|---|
| **Languages** | PHP · Python · TypeScript · JavaScript · C# |
| **Backend** | Laravel · Filament · Django / DRF · FastAPI · Node.js · .NET |
| **Frontend** | React · Next.js · Livewire · Tailwind CSS |
| **Data** | PostgreSQL · MySQL / MariaDB · Oracle · Redis · Firestore |
| **Infra & delivery** | Docker · Linux · Nginx · GitHub Actions · CI/CD pipelines |

## Featured projects

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/TPCT/JenDock">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/repo-JenDock-dark.svg">
          <img src="./assets/generated/repo-JenDock-light.svg" width="100%" alt="JenDock: Self-hosted CI/CD for Docker Compose: Jenkinsfile pipelines, health checks, auto-rollback.">
        </picture>
      </a>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/TPCT/tpct-mac-theme">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/repo-tpct-mac-theme-dark.svg">
          <img src="./assets/generated/repo-tpct-mac-theme-light.svg" width="100%" alt="tpct-mac-theme: macOS-style GNOME desktop: GTK4/GTK3 and Shell theme, global menu and desktop widgets.">
        </picture>
      </a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/TPCT/Egyptian-National-ID">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/repo-Egyptian-National-ID-dark.svg">
          <img src="./assets/generated/repo-Egyptian-National-ID-light.svg" width="100%" alt="Egyptian-National-ID: Django REST API that validates Egyptian national IDs and extracts birth date, gender, region.">
        </picture>
      </a>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/TPCT/order-payment-api">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/repo-order-payment-api-dark.svg">
          <img src="./assets/generated/repo-order-payment-api-light.svg" width="100%" alt="order-payment-api: Laravel REST API for users, products, orders and payments, secured with JWT.">
        </picture>
      </a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/TPCT/social-media-scheduler">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/repo-social-media-scheduler-dark.svg">
          <img src="./assets/generated/repo-social-media-scheduler-light.svg" width="100%" alt="social-media-scheduler: Laravel app that schedules and auto-publishes posts across social platforms, with analytics.">
        </picture>
      </a>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/TPCT/palm-resources-01">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/repo-palm-resources-01-dark.svg">
          <img src="./assets/generated/repo-palm-resources-01-light.svg" width="100%" alt="palm-resources-01: Idempotent exercise-session ingest on Firebase Functions and Firestore, in TypeScript.">
        </picture>
      </a>
    </td>
  </tr>
</table>

## Selected private work

Most of my commercial work is private because it runs real client operations. These are the kinds of products I build:

<table>
  <tr>
    <td width="50%" valign="top">
      <b>Business suites</b><br>
      <sub>ERP · HRM · POS · CRM</sub><br>
      Modular platforms for operations, people, sales and customers, with role-based access and reporting.
    </td>
    <td width="50%" valign="top">
      <b>Learning platforms</b><br>
      <sub>LMS</sub><br>
      Course delivery, enrolment and progress tracking for training businesses.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <b>Gaming platform &amp; bots</b><br>
      <sub>Platform · Bots · Automation</sub><br>
      A platform back end, plus the bots and automation that run community and game operations.
    </td>
    <td width="50%" valign="top">
      <b>OCR &amp; document processing</b><br>
      <sub>OCR · Pipelines</sub><br>
      Pipelines that turn scanned documents into structured, searchable data.
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <b>eSIM platform</b><br>
      <sub>Telecom · Provisioning</sub><br>
      Ordering, provisioning and account management for digital SIM products.
    </td>
    <td width="50%" valign="top">
      <b>Monitoring &amp; CI tooling</b><br>
      <sub>DevOps · Observability</sub><br>
      Self-hosted deploy pipelines, health checks and alerting for production services.
    </td>
  </tr>
</table>

## GitHub stats

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/generated/stats-dark.svg">
  <img src="./assets/generated/stats-light.svg" width="100%" alt="GitHub stats for TPCT: contributions in the last 12 months, public repositories, stars and top languages.">
</picture>

<sub>Generated daily from the GitHub API by a workflow in this repository.</sub>

## Contact

Open to architecture work, platform builds and technical partnerships.

**Email** [eslamjackie@outlook.com](mailto:eslamjackie@outlook.com) · **Studio** [shiftcodes.net](https://shiftcodes.net) · **Portfolio** [tpct.github.io](https://tpct.github.io)
````

## Interfaces
Asset paths referenced (all must exist when this ticket runs):
`assets/hero-dark.svg`, `assets/hero-light.svg`, `assets/generated/stats-{dark,light}.svg`,
`assets/generated/repo-{JenDock,tpct-mac-theme,Egyptian-National-ID,order-payment-api,social-media-scheduler,palm-resources-01}-{dark,light}.svg`.

## Constraints
- No emojis. English only. No hostnames, client names, internal URLs or private repo links anywhere in the README.
- Do not edit any SVG, `scripts/`, `.github/`, or `.company/` (other than writing renders into `.company/runs/`).
- No commits and no push.
- Assumptions (decided by Tech Lead/UX): the stack is a plain table, not badges (brief: "not a wall"). There are 3 CTA badges only,
  with Portfolio first and in the strongest color. There are no section dividers, no visitor counter and no snake.

## Acceptance criteria
- [ ] README.md matches the content above.
- [ ] Every local `./assets/...` path in README.md exists on disk.
- [ ] No reference to `v3-`, `v4-`, `v5-`, `profile-hero`, `impact.svg` or `capabilities.svg` remains, and those 12 files are deleted.
- [ ] `assets/` then contains only `hero-dark.svg`, `hero-light.svg` and `generated/`.
- [ ] Every `<picture>` has a dark `<source>` and a light `<img>` with alt text.
- [ ] No emoji characters in README.md.

## Tests / verify locally (run only these)
```bash
cd /home/tpct/TPCT-profile
# 1. every referenced asset exists
grep -oE '\./assets/[^" )]+' README.md | sort -u | while read p; do [ -f "$p" ] && echo "ok $p" || echo "MISSING $p"; done
# 2. no old asset references
grep -nE 'v[345]-|profile-hero|impact\.svg|capabilities\.svg' README.md && echo FAIL || echo "ok no old refs"
ls -R assets
# 3. picture/source/img balance
grep -c '<picture>' README.md; grep -c 'prefers-color-scheme: dark' README.md; grep -c '<img ' README.md   # expect 8 / 8 / 8
# 4. no emoji (non-BMP or common emoji ranges)
python3 -c "import re,sys; t=open('README.md',encoding='utf-8').read(); bad=[c for c in t if ord(c)>0x2600 and c not in '·']; print('emoji/symbols:', bad or 'none')"
```
Optional, if network is available: render with GitHub's Markdown API and check that it renders without errors:
`gh api markdown -f mode=gfm -f context=TPCT/TPCT -f text="$(cat README.md)" > .company/runs/readme.html`

## Out of scope
SVG content (T-001/T-002), GitHub profile bio/blog fields, the portfolio site.

## Addendum (Tech Lead, from T-002 review)
- In `.github/workflows/profile.yml`, add `if: github.ref == 'refs/heads/main'` to the step that commits/pushes generated assets, so a manual run from another branch never pushes to main. No other workflow changes.
- The first real Action run (run 39529331526) failed in "Commit if changed": the commit succeeded (2 files: stats-dark/light), then `git pull --rebase origin main` failed with "cannot pull with rebase: You have unstaged changes." Fix robustly: print `git status --porcelain` (for diagnosis) before committing, then use `git pull --rebase --autostash origin main` before `git push origin HEAD:main`. Also add `PYTHONDONTWRITEBYTECODE: 1` to the job env so tests never leave `__pycache__`. Keep the existing "No changes" early exit.
- Also print one summary line from `scripts/generate.py` (to stdout) with the computed numbers: contributions, public repos, stars (no secrets) — so CI logs show whether the Actions token sees the full contribution calendar.
