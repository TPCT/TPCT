"""Offline tests for the profile generator."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import date
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate

FIXTURE = Path(__file__).parent / "fixtures/sample.json"
TODAY = date(2026, 10, 21)


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_wrap(self):
        self.assertEqual(generate.wrap("one two three", 10, 40, 3), ["one two", "three"])
        for line in generate.wrap("one two three four", 10, 40, 4):
            self.assertLessEqual(generate.text_width(line, 10), 40)
        with self.assertRaises(ValueError):
            generate.wrap("one two three", 10, 20, 2)
        with self.assertRaises(ValueError):
            generate.wrap("oversized", 10, 20, 3)

    def test_featured_bounds(self):
        for repo in generate.FEATURED:
            with self.subTest(repo=repo["name"]):
                self.assertLessEqual(len(generate.wrap(repo["description"], 19, 452, 3)), 3)
                self.assertLessEqual(len(repo["tag"]), 22)
                self.assertLessEqual(generate.text_width(repo["name"], 26), 452)

    def test_card_description_wrapping(self):
        max_chars = int((470 - 24) / (20 * 0.56))
        descriptions = [repo["description"] for repo in generate.FEATURED]
        descriptions += ["word " * 100, "W" * 200, "", "one two three"]
        for description in descriptions:
            with self.subTest(description=description):
                lines = generate.wrap_card_description(description)
                self.assertLessEqual(len(lines), 3)
                for line in lines:
                    self.assertLessEqual(len(line), max_chars)
                    self.assertLessEqual(24 + generate.text_width(line, 20), 470)
        self.assertTrue(generate.wrap_card_description("word " * 100)[-1].endswith("…"))
        self.assertEqual(generate.wrap_card_description("one two three"), ["one two three"])

    def test_card_typography(self):
        repo = dict(generate.FEATURED[0], description="word " * 100)
        for theme in generate.THEMES:
            root = ET.fromstring(generate.render_card(repo, self.data, theme))
            texts = root.findall("{http://www.w3.org/2000/svg}text")
            self.assertGreaterEqual(int(texts[0].attrib["font-size"]), 26)
            descriptions = [text for text in texts if 100 <= int(text.attrib["y"]) <= 152]
            self.assertEqual(len(descriptions), 3)
            for text in descriptions:
                self.assertGreaterEqual(int(text.attrib["font-size"]), 18)
                self.assertLess(int(text.attrib["y"]) + 5, 169)
            for text in texts:
                if text.attrib["y"] == "182":
                    self.assertGreaterEqual(int(text.attrib["font-size"]), 15)

    def test_shiftcodes_styling(self):
        palettes = {
            "dark": ("#1E1832", "#3A3160", "#F3F0FF", "#ABA1CC", "#C9B8FF", "#8A5BFF", "#8FA0FF"),
            "light": ("#FCFBFF", "#D8D1F0", "#1C1530", "#5A5275", "#6E2BFB", "#5A1FE0", "#3346C4"),
        }
        ns = {"svg": "http://www.w3.org/2000/svg"}
        for theme, (plate, border, fg, muted, brand, crown, cyan) in palettes.items():
            renders = [generate.render_stats(self.data, theme, TODAY)]
            renders += [generate.render_card(repo, self.data, theme) for repo in generate.FEATURED]
            for svg in renders:
                with self.subTest(theme=theme, title=ET.fromstring(svg).find("svg:title", ns).text):
                    root = ET.fromstring(svg)
                    background = root.find("svg:rect", ns)
                    self.assertEqual(background.attrib["fill"], plate)
                    self.assertEqual(background.attrib["stroke"], border)
                    stops = root.findall(".//svg:linearGradient[@id='accent']/svg:stop", ns)
                    self.assertEqual([stop.attrib["stop-color"] for stop in stops], [brand, crown, cyan])
                    self.assertEqual([stop.attrib["offset"] for stop in stops], ["0%", "50%" if theme == "dark" else "55%", "100%"])
                    self.assertIn('fill="url(#accent)"' if root.attrib["width"] == "500" else 'stroke="url(#accent)"', svg)
                    for text in root.findall("svg:text", ns):
                        self.assertEqual(text.attrib["font-family"], generate.SANS)
                        self.assertNotIn("monospace", text.attrib["font-family"])
                        if text.attrib["fill"] == cyan:
                            self.assertEqual(text.text, text.text.upper())
                            self.assertEqual(text.attrib["font-weight"], "800")
                            self.assertEqual(text.attrib["letter-spacing"], "1.5")
                    self.assertIn(f'fill="{fg}"', svg)
                    self.assertIn(f'fill="{muted}"', svg)

    def test_muted_contrast(self):
        def luminance(color):
            channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
            return sum(c * weight for c, weight in zip(linear, (0.2126, 0.7152, 0.0722)))

        for theme, colors in generate.THEMES.items():
            with self.subTest(theme=theme):
                values = sorted([luminance(colors["muted"]), luminance(colors["surface"])])
                self.assertGreaterEqual((values[1] + 0.05) / (values[0] + 0.05), 4.5)

    def test_languages(self):
        result = generate.aggregate_languages(self.data["languages"])
        self.assertEqual(len(result), 7)
        self.assertEqual([name for name, _, _ in result], ["PHP", "Python", "TypeScript", "JavaScript", "Blade", "C#", "Other"])
        self.assertAlmostEqual(sum(pct for _, pct, _ in result), 100, delta=0.01)
        self.assertEqual(generate.aggregate_languages({}), [])
        self.assertEqual(generate.aggregate_languages({"HTML": {"size": 10, "color": None}}), [])
        tied = {"Z": {"size": 1, "color": None}, "A": {"size": 1, "color": None}}
        self.assertEqual([name for name, _, _ in generate.aggregate_languages(tied)], ["A", "Z"])

    def test_years(self):
        self.assertEqual(generate.years_on_github("2016-05-27T01:13:01Z", TODAY), 10)

    def test_rendering(self):
        for theme in generate.THEMES:
            renders = [(lambda: generate.render_stats(self.data, theme, TODAY), "1000", "320")]
            renders += [(lambda repo=repo: generate.render_card(repo, self.data, theme), "500", "200") for repo in generate.FEATURED]
            for render, width, height in renders:
                svg = render()
                root = ET.fromstring(svg)
                self.assertEqual(root.attrib["width"], width)
                self.assertEqual(root.attrib["height"], height)
                self.assertEqual(root.attrib["viewBox"], f"0 0 {width} {height}")
                self.assertNotIn("http", svg.replace("http://www.w3.org/2000/svg", ""))
                self.assertEqual(svg, render())
                self.assertLessEqual(len(svg.encode("utf-8")), 150_000)
                self.assertTrue(svg.startswith('<?xml version="1.0" encoding="UTF-8"?>'))

    def test_card_animation(self):
        ns = {"svg": "http://www.w3.org/2000/svg"}
        for theme in generate.THEMES:
            for i, repo in enumerate(generate.FEATURED):
                with self.subTest(theme=theme, repo=repo["name"]):
                    root = ET.fromstring(generate.render_card(repo, self.data, theme))
                    border = root.find("svg:rect[@class='card-border']", ns)
                    self.assertEqual(border.attrib["pathLength"], "100")
                    self.assertEqual(border.attrib["stroke-width"], "1.5")
                    self.assertEqual(border.attrib["stroke"], "url(#accent)")
                    self.assertEqual(border.attrib["stroke-dasharray"], "18 82")
                    self.assertEqual(border.attrib["style"], f"animation-delay: -{i}s")
                    css = root.find("svg:style", ns).text
                    self.assertIn("@media (prefers-reduced-motion: no-preference)", css)
                    self.assertIn("animation: card-border 6s linear infinite", css)
                    self.assertIn("stroke-dashoffset: -100", css)
                    self.assertIn(".card-border { opacity: 0; }", css)

    def test_stats_animation(self):
        ns = {"svg": "http://www.w3.org/2000/svg"}
        for theme in generate.THEMES:
            with self.subTest(theme=theme):
                root = ET.fromstring(generate.render_stats(self.data, theme, TODAY))
                css = root.find("svg:style", ns).text
                self.assertIn("@media (prefers-reduced-motion: no-preference)", css)
                self.assertIn("translateY(6px)", css)
                self.assertIn("transform-origin: left; transform-box: fill-box", css)
                self.assertIn("scaleX(0)", css)
                for animation in ("stats-enter", "language-grow", "legend-enter"):
                    self.assertIn(f"animation: {animation} 600ms ease-out backwards", css)
                self.assertIn("animation: stats-shimmer 6s linear infinite", css)
                metrics = root.findall("svg:g[@class='metric']", ns)
                self.assertEqual([g.attrib["style"] for g in metrics],
                                 [f"animation-delay: {i * 120}ms" for i in range(4)])
                for metric in metrics:
                    self.assertEqual(len(metric.findall("svg:text", ns)), 2)
                segments = root.findall(".//svg:rect[@class='language-segment']", ns)
                self.assertEqual(len(segments), len(generate.aggregate_languages(self.data["languages"])))
                self.assertEqual([g.attrib["style"] for g in segments],
                                 [f"animation-delay: {i * 120}ms" for i in range(len(segments))])
                self.assertIsNotNone(root.find("svg:g[@class='legend']", ns))

    def test_stars_and_no_language(self):
        self.assertEqual(generate.render_card(generate.FEATURED[0], self.data, "dark").count("<polygon"), 1)
        self.assertNotIn("<polygon", generate.render_card(generate.FEATURED[1], self.data, "dark"))
        self.data["featured"]["JenDock"]["language"] = None
        svg = generate.render_card(generate.FEATURED[0], self.data, "dark")
        self.assertNotIn("<circle", svg)
        self.assertNotIn(">Python<", svg)

    def test_card_language_override(self):
        repo = generate.FEATURED[5]
        self.assertEqual(repo["name"], "ashurbank.iq")
        for theme in generate.THEMES:
            with self.subTest(theme=theme):
                svg = generate.render_card(repo, self.data, theme)
                self.assertIn(">PHP<", svg)
                self.assertIn('fill="#4F5D95"', svg)
                self.assertNotIn(">JavaScript<", svg)
                self.assertNotIn('fill="#f1e05a"', svg)
                without_override = dict(repo)
                del without_override["language"]
                svg = generate.render_card(without_override, self.data, theme)
                self.assertIn(">JavaScript<", svg)
                self.assertIn('fill="#f1e05a"', svg)

    def test_escaping(self):
        repo = dict(generate.FEATURED[0], description='Use & compare <values> "safely"')
        svg = generate.render_card(repo, self.data, "light")
        ET.fromstring(svg)
        self.assertIn("&amp;", svg)
        self.assertIn("&lt;values&gt;", svg)
        self.assertIn("&quot;safely&quot;", svg)

    @patch("urllib.request.urlopen")
    def test_graphql_errors(self, urlopen):
        urlopen.return_value.__enter__.return_value = io.BytesIO(b'{"errors": [{"message": "failure"}]}')
        with self.assertRaises(RuntimeError):
            generate.graphql("secret", "query {}")

    @patch("generate.time.sleep")
    @patch("urllib.request.urlopen")
    def test_graphql_retry_and_headers(self, urlopen, sleep):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value = io.BytesIO(b'{"data": {"ok": true}}')
        urlopen.side_effect = [urllib.error.URLError("temporary"), response]
        self.assertEqual(generate.graphql("secret", "query {}"), {"ok": True})
        sleep.assert_called_once_with(2)
        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "bearer secret")
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 30)

    @patch("generate.graphql")
    def test_fetch_pagination(self, graphql):
        def page(next_page, stars):
            return {"user": {"createdAt": self.data["created_at"], "contributionsCollection": {"contributionCalendar": {"totalContributions": 8667}, "restrictedContributionsCount": 8278}, "repositories": {"totalCount": 2, "pageInfo": {"hasNextPage": next_page, "endCursor": "cursor"}, "nodes": [{"stargazerCount": stars, "languages": {"edges": [{"size": 100, "node": {"name": "Python", "color": "#3572A5"}}]}}]}}}
        featured = {f"r{i}": {"name": repo["name"], "stargazerCount": 0, "primaryLanguage": None} for i, repo in enumerate(generate.FEATURED)}
        graphql.side_effect = [page(True, 2), page(False, 3), featured]
        data = generate.fetch("secret")
        self.assertEqual(data["total_stars"], 5)
        self.assertEqual(data["languages"]["Python"]["size"], 200)
        self.assertEqual(data["contributions_last_year"], 8667)
        self.assertEqual(graphql.call_args_list[1].args[2]["after"], "cursor")
        self.assertIsNone(data["featured"]["JenDock"]["language"])
        graphql.side_effect = [{"user": None}]
        with self.assertRaisesRegex(RuntimeError, "TPCT"):
            generate.fetch("secret")
        featured["r0"] = None
        graphql.side_effect = [page(False, 0), featured]
        with self.assertRaisesRegex(RuntimeError, "JenDock"):
            generate.fetch("secret")

    def test_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = ["--fixture", str(FIXTURE), "--out", tmp, "--today", "2026-10-21"]
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(generate.main(args), 0)
            self.assertEqual(len(list(Path(tmp).glob("*.svg"))), 14)
            self.assertIn("14 file(s) updated", output.getvalue())
            first_run = {p.name: p.read_bytes() for p in Path(tmp).glob("*.svg")}
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(generate.main(args), 0)
            self.assertIn("0 file(s) updated", output.getvalue())
            self.assertEqual(first_run, {p.name: p.read_bytes() for p in Path(tmp).glob("*.svg")})

    def test_main_failures_write_nothing(self):
        with tempfile.TemporaryDirectory() as tmp, redirect_stderr(io.StringIO()) as error:
            with patch.dict("os.environ", {}, clear=True):
                self.assertEqual(generate.main(["--out", tmp]), 2)
            self.assertIn("GITHUB_TOKEN is not set", error.getvalue())
            with patch.dict("os.environ", {"GITHUB_TOKEN": "secret"}), patch("urllib.request.urlopen") as urlopen:
                urlopen.return_value.__enter__.return_value = io.BytesIO(b'{"errors": ["failure"]}')
                self.assertEqual(generate.main(["--out", tmp]), 1)
            self.assertEqual(list(Path(tmp).iterdir()), [])
            with patch("generate.render_card", side_effect=ValueError("render failed")):
                self.assertEqual(generate.main(["--fixture", str(FIXTURE), "--out", tmp]), 1)
            self.assertEqual(list(Path(tmp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
