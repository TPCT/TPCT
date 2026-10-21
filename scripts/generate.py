"""Generate deterministic profile SVGs from GitHub or an offline fixture."""

import argparse
from datetime import date, datetime, timezone
import html
import json
import math
import os
from pathlib import Path
import sys
import textwrap
import time
import urllib.error
import urllib.request

LOGIN = "TPCT"
FEATURED = [
    {"name": "JenDock", "tag": "CI/CD · DOCKER", "description": "Self-hosted CI/CD for Docker Compose: Jenkinsfile pipelines, health checks, auto-rollback."},
    {"name": "tpct-mac-theme", "tag": "GNOME · GTK", "description": "macOS-style GNOME desktop: GTK4/GTK3 and Shell theme, global menu and desktop widgets."},
    {"name": "Egyptian-National-ID", "tag": "DJANGO REST", "description": "Django REST API that validates Egyptian national IDs and extracts birth date, gender, region."},
    {"name": "order-payment-api", "tag": "LARAVEL · JWT", "description": "Laravel REST API for users, products, orders and payments, secured with JWT."},
    {"name": "social-media-scheduler", "tag": "LARAVEL", "description": "Laravel app that schedules and auto-publishes posts across social platforms, with analytics."},
    {"name": "ashurbank.iq", "tag": "LARAVEL · FILAMENT", "description": "Bilingual bank website with a Filament CMS: roles and permissions, audit log, Excel import/export.", "language": "PHP"},
]
EXCLUDED_LANGUAGES = {"HTML", "CSS", "SCSS", "Less", "Jupyter Notebook", "Makefile", "Dockerfile", "Procfile", "Batchfile"}
TOP_LANGUAGES = 6
THEMES = {
    "dark": {"bg": "#1E1832", "surface": "#1E1832", "border": "#3A3160", "text": "#F3F0FF", "muted": "#ABA1CC", "cyan": "#8FA0FF", "brand": "#C9B8FF", "crown": "#8A5BFF", "accent_mid": "50%"},
    "light": {"bg": "#FCFBFF", "surface": "#FCFBFF", "border": "#D8D1F0", "text": "#1C1530", "muted": "#5A5275", "cyan": "#3346C4", "brand": "#6E2BFB", "crown": "#5A1FE0", "accent_mid": "55%"},
}
SANS = "Outfit, 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
ROOT = Path(__file__).resolve().parent.parent


def graphql(token: str, query: str, variables: dict | None = None) -> dict:
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables or {}}).encode("utf-8"),
        headers={"Authorization": f"bearer {token}", "User-Agent": "TPCT-profile-generator", "Content-Type": "application/json"},
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
            if payload.get("errors"):
                raise RuntimeError("GitHub GraphQL returned errors")
            return payload["data"]
        except urllib.error.HTTPError as exc:
            if not 500 <= exc.code < 600 or attempt == 2:
                raise RuntimeError(f"GitHub HTTP error {exc.code}") from exc
        except urllib.error.URLError as exc:
            if attempt == 2:
                raise RuntimeError("GitHub request failed after 3 attempts") from exc
        time.sleep(2)
    raise RuntimeError("GitHub request failed")


def fetch(token: str, login: str = LOGIN) -> dict:
    query = """query($login: String!, $after: String) {
      user(login: $login) {
        createdAt
        contributionsCollection { contributionCalendar { totalContributions } }
        repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100, after: $after) {
          totalCount pageInfo { hasNextPage endCursor }
          nodes { stargazerCount languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
            edges { size node { name color } }
          } }
        }
      }
    }"""
    result = {"login": login, "total_stars": 0, "languages": {}, "featured": {}}
    after = None
    while True:
        user = graphql(token, query, {"login": login, "after": after})["user"]
        if user is None:
            raise RuntimeError(f"GitHub user {login} was not found")
        result["created_at"] = user["createdAt"]
        result["contributions_last_year"] = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        repos = user["repositories"]
        result["public_repos"] = repos["totalCount"]
        for repo in repos["nodes"]:
            result["total_stars"] += repo["stargazerCount"]
            for edge in repo["languages"]["edges"]:
                node = edge["node"]
                language = result["languages"].setdefault(node["name"], {"size": 0, "color": node["color"]})
                language["size"] += edge["size"]
        if not repos["pageInfo"]["hasNextPage"]:
            break
        after = repos["pageInfo"]["endCursor"]
    fields = [f'r{i}: repository(owner: {json.dumps(login)}, name: {json.dumps(repo["name"])}) {{ name stargazerCount primaryLanguage {{ name color }} }}' for i, repo in enumerate(FEATURED)]
    featured = graphql(token, "query { " + " ".join(fields) + " }")
    for i, repo in enumerate(FEATURED):
        item = featured[f"r{i}"]
        if item is None:
            raise RuntimeError(f'GitHub repository {login}/{repo["name"]} was not found')
        language = item["primaryLanguage"] or {}
        result["featured"][repo["name"]] = {"stars": item["stargazerCount"], "language": language.get("name"), "language_color": language.get("color")}
    return result


def aggregate_languages(languages: dict[str, dict]) -> list[tuple[str, float, str]]:
    included = sorted(((name, item) for name, item in languages.items() if name not in EXCLUDED_LANGUAGES and item["size"] > 0), key=lambda pair: (-pair[1]["size"], pair[0]))
    total = sum(item["size"] for _, item in included)
    if not total:
        return []
    result = [(name, item["size"] * 100 / total, item["color"]) for name, item in included[:TOP_LANGUAGES]]
    remainder = sum(item["size"] for _, item in included[TOP_LANGUAGES:])
    if remainder:
        result.append(("Other", remainder * 100 / total, None))
    return result


def text_width(text: str, size: float, mono: bool = False) -> float:
    return len(text) * size * (0.62 if mono else 0.56)


def wrap(text: str, size: float, max_width: float, max_lines: int) -> list[str]:
    lines = []
    for word in text.split():
        if text_width(word, size) > max_width:
            raise ValueError(f"Word exceeds width: {word}")
        if lines and text_width(lines[-1] + " " + word, size) <= max_width:
            lines[-1] += " " + word
        else:
            lines.append(word)
        if len(lines) > max_lines:
            raise ValueError("Text exceeds maximum line count")
    return lines


def wrap_card_description(text: str) -> list[str]:
    # Leave 24px at the left and keep descriptions within x=470.
    max_chars = math.floor((470 - 24) / (20 * 0.56))
    lines = textwrap.wrap(text, width=max_chars, break_on_hyphens=False)
    if len(lines) > 3:
        lines = lines[:3]
        lines[-1] = lines[-1][:max_chars - 1].rstrip() + "…"
    return lines


def years_on_github(created_at: str, today: date) -> int:
    return math.floor((today - date.fromisoformat(created_at[:10])).days / 365.25)


def _escape(value) -> str:
    return html.escape(str(value), quote=True)


def _text(x, y, value, size, color, extra="") -> str:
    return f'<text x="{x}" y="{y}" font-family="{_escape(SANS)}" font-size="{size}" fill="{_escape(color)}"{extra}>{_escape(value)}</text>'


def _svg(width, height, title) -> list[str]:
    return ['<?xml version="1.0" encoding="UTF-8"?>', f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">', f'<title>{_escape(title)}</title>']


def _accent(colors: dict, x1: int = 24, x2: int = 56) -> str:
    return f'<defs><linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="{x1}" y1="0" x2="{x2}" y2="0"><stop offset="0%" stop-color="{colors["brand"]}"/><stop offset="{colors["accent_mid"]}" stop-color="{colors["crown"]}"/><stop offset="100%" stop-color="{colors["cyan"]}"/></linearGradient></defs>'


def render_card(repo: dict, data: dict, theme: str) -> str:
    colors = THEMES[theme]
    name, tag = repo["name"], repo["tag"]
    if text_width(name, 28) > 446 or len(tag) > 22:
        raise ValueError(f"Card name or tag exceeds bounds: {name}")
    lines = wrap_card_description(repo["description"])
    item = data["featured"][name]
    parts = _svg(500, 200, f'{name}: {repo["description"]}')
    parts.extend([_accent(colors), f'<rect x="0.5" y="0.5" width="499" height="199" rx="16" fill="{colors["surface"]}" stroke="{colors["border"]}"/>', '<rect x="24" y="24" width="32" height="4" rx="2" fill="url(#accent)"/>', _text(24, 64, name, 28, colors["text"], extra=' font-weight="700"')])
    for i, line in enumerate(lines):
        parts.append(_text(24, 100 + i * 26, line, 20, colors["muted"]))
    language = repo.get("language", item["language"])
    language_color = item["language_color"]
    if "language" in repo:
        language_color = "#4F5D95" if language == "PHP" else data["languages"].get(language, {}).get("color")
    if language:
        parts.append(f'<circle cx="30" cy="176" r="6" fill="{_escape(language_color or colors["muted"])}"/>')
        parts.append(_text(44, 182, language, 17, colors["muted"]))
    if item["stars"] >= 1:
        cx = 44 + text_width(language, 17) + 22 if language else 30
        points = []
        for i in range(10):
            angle = -math.pi / 2 + i * math.pi / 5
            radius = 7 if i % 2 == 0 else 3
            points.append(f"{cx + radius * math.cos(angle):.3f},{176 + radius * math.sin(angle):.3f}")
        parts.append(f'<polygon points="{" ".join(points)}" fill="{colors["muted"]}"/>')
        parts.append(_text(f"{cx + 12:g}", 182, item["stars"], 17, colors["muted"]))
    parts.append(_text(476, 182, tag, 15, colors["cyan"], extra=' text-anchor="end" font-weight="800" letter-spacing="1.5"'))
    return "\n".join(parts + ["</svg>", ""])


def render_stats(data: dict, theme: str, today: date) -> str:
    colors = THEMES[theme]
    parts = _svg(1000, 320, f'GitHub stats for {data["login"]}')
    parts.extend([_accent(colors, 40, 960), f'<rect x="0.5" y="0.5" width="999" height="319" rx="20" fill="{colors["bg"]}" stroke="{colors["border"]}"/>', _text(40, 52, "GITHUB ACTIVITY", 16, colors["cyan"], extra=' font-weight="800" letter-spacing="1.5"')])
    metrics = [(data["contributions_last_year"], "Contributions (12 mo)"), (data["public_repos"], "Public repositories"), (data["total_stars"], "Stars earned"), (years_on_github(data["created_at"], today), "Years on GitHub")]
    for x, (value, label) in zip((40, 270, 500, 730), metrics):
        parts.extend([_text(x, 118, f"{value:,}", 44, colors["text"], extra=' font-weight="800"'), _text(x, 148, label, 17, colors["muted"])])
    parts.extend([f'<line x1="40" y1="176" x2="960" y2="176" stroke="url(#accent)"/>', _text(40, 208, "TOP LANGUAGES · BY CODE SIZE", 14, colors["cyan"], extra=' font-weight="800" letter-spacing="1.5"')])
    languages = aggregate_languages(data["languages"])
    if languages:
        parts.extend(['<defs><clipPath id="languages"><rect x="40" y="222" width="920" height="12" rx="6"/></clipPath></defs>', '<g clip-path="url(#languages)">'])
        x = 40.0
        separators = []
        for name, pct, color in languages:
            width = max(2, 920 * pct / 100)
            parts.append(f'<rect x="{x:.6f}" y="222" width="{width:.6f}" height="12" fill="{_escape(color or colors["muted"])}"/>')
            x += 920 * pct / 100
            separators.append(x)
        for x in separators[:-1]:
            parts.append(f'<line x1="{x:.6f}" y1="222" x2="{x:.6f}" y2="234" stroke="{colors["bg"]}" stroke-width="2"/>')
        parts.append('</g>')
        for i, (name, pct, color) in enumerate(languages):
            x, y = (40, 270, 500, 730)[i % 4], 270 + 28 * (i // 4)
            parts.append(f'<circle cx="{x + 5}" cy="{y - 5}" r="5" fill="{_escape(color or colors["muted"])}"/>')
            parts.append(f'<text x="{x + 18}" y="{y}" font-family="{_escape(SANS)}" font-size="16" fill="{colors["text"]}">{_escape(name)} <tspan fill="{colors["muted"]}">{pct:.1f}%</tspan></text>')
    return "\n".join(parts + ["</svg>", ""])


def write_if_changed(path: Path, content: str) -> bool:
    encoded = content.encode("utf-8")
    if path.exists() and path.read_bytes() == encoded:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as output:
        output.write(content)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("assets/generated"))
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--dump-fixture", type=Path)
    parser.add_argument("--today", type=date.fromisoformat, default=datetime.now(timezone.utc).date())
    args = parser.parse_args(argv)
    if not args.fixture and not os.environ.get("GITHUB_TOKEN"):
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 2
    try:
        data = json.loads(args.fixture.read_text(encoding="utf-8")) if args.fixture else fetch(os.environ["GITHUB_TOKEN"])
        out = ROOT / args.out
        outputs = {}
        for theme in THEMES:
            outputs[out / f"stats-{theme}.svg"] = render_stats(data, theme, args.today)
            for repo in FEATURED:
                outputs[out / f'repo-{repo["name"]}-{theme}.svg'] = render_card(repo, data, theme)
        if args.dump_fixture and not args.fixture:
            outputs[args.dump_fixture] = json.dumps(data, indent=2, sort_keys=True) + "\n"
    except Exception as exc:
        print(f"Generation failed: {exc}", file=sys.stderr)
        return 1
    updated = 0
    try:
        for path, content in outputs.items():
            changed = write_if_changed(path, content)
            updated += changed
            print(f'{"updated" if changed else "unchanged"} {path}')
    except OSError as exc:
        print(f"Writing failed: {exc}", file=sys.stderr)
        return 1
    print(f"Summary: contributions={data['contributions_last_year']}, public repos={data['public_repos']}, stars={data['total_stars']}")
    print(f"{updated} file(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
