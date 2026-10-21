# T-005 — New contact email + replace palm-resources-01 with ashurbank.iq (S)

User request (mid-run, 2026-10-21): change email to th3professionalcod3r@gmail.com; hide palm-resources-01 (not worth showcasing) and feature a stronger project.
Tech Lead pick: `ashurbank.iq` — public repo, production bilingual corporate website + Filament admin CMS for a bank (Laravel 10/11, Filament v3, Spatie permission/settings/translatable, audit log via owen-it/laravel-auditing, Excel import/export).

## Files
README.md, scripts/generate.py, scripts/fixtures/sample.json, scripts/test_generate.py (only if they reference palm), assets/generated/repo-palm-resources-01-*.svg (delete).

## Spec
1. README: replace every `eslamjackie@outlook.com` with `th3professionalcod3r@gmail.com`. The Email badge becomes
   `[![Email](https://img.shields.io/badge/Email-th3professionalcod3r%40gmail.com-12151C?style=for-the-badge&logo=gmail&logoColor=white)](mailto:th3professionalcod3r@gmail.com)`. Contact footer link likewise.
2. Featured repos config in `scripts/generate.py`: replace the palm-resources-01 entry with
   `{"name": "ashurbank.iq", "tag": "LARAVEL · FILAMENT", "description": "Bilingual bank website with a Filament CMS: roles and permissions, audit log, Excel import/export.", "language": "PHP"}`.
   Add support for an optional `"language"` override key: when present, the card shows that language name and its standard GitHub color (PHP = #4F5D95) instead of the API primaryLanguage (the repo's byte-majority is vendored JS, which misrepresents it). Keep ordering (it's the 6th card).
3. Fixture `scripts/fixtures/sample.json`: replace the palm-resources-01 entry with an ashurbank.iq entry (any plausible fixture data) so fixture runs and tests stay green; add a unit test for the language override.
4. README Featured section: replace the palm card `<a>` with ashurbank.iq (href https://github.com/TPCT/ashurbank.iq, srcset/src ./assets/generated/repo-ashurbank.iq-{dark,light}.svg, width="380", alt "ashurbank.iq: Bilingual bank website with a Filament CMS: roles and permissions, audit log, Excel import/export."). Nothing else in README changes.
5. Delete assets/generated/repo-palm-resources-01-dark.svg and -light.svg. Ensure the tag text "LARAVEL · FILAMENT" fits the card footer without overlapping the language label (right-aligned at x=476).

## Acceptance
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_*.py'` passes.
- `grep -rn "palm-resources\|eslamjackie" README.md scripts/` → no matches.
- Fixture generation to /tmp passes xmllint; render the ashurbank card with inkscape and confirm no overlap.

## Constraints
No commits/push. Affected tests only. Don't touch other sections, workflow or hero.
