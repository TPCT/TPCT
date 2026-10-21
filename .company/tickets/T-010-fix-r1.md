# T-010 fix r1 — Experience timeline polish (S)

Original ticket: .company/tickets/T-010-experience-impact.md. Impact SVGs are APPROVED as is (do not touch them). Fix only assets/experience-{dark,light}.svg.

Blocking issues found in review (inkscape static render of experience-light):
1. **Order** (newest first by end date): PREVIOUSLY must be: Everything To Gain (2025 – 2026) → Kearney (2024 – 2026) → IPXBit (2025) → dot.jo (2023 – 2025) → Venu Dine (2022 – 2023). Keep each entry's text as is.
2. **Spacing**: "PREVIOUSLY" label is cramped against the Edulixa360 entry above (and "NOW" against the header). Add ≥ 22px gap above each group label and ≥ 10px below it; the timeline line must not run through the group labels (break the line around labels, or offset labels to the right of the line with a clear gap). Grow the viewBox height as needed (≤ 820).
3. **Static line looks broken**: in the static (reduced-motion / no-animation) frame the accent overlay line renders as disconnected segments. The static frame must show one continuous, clean timeline line (per group). Put the dash-draw (stroke-dasharray/dashoffset) ONLY inside the `prefers-reduced-motion: no-preference` block, with the base style being a solid line; ensure `pathLength` maths make the drawn end state a full solid line too.
4. Keep everything else (fonts ≥ the mobile minimums, pulses on current roles, stagger, colours, 640 width).

Acceptance: xmllint OK; inkscape renders both themes (attach paths in report) show order, spacing and a continuous line; headless Chrome screenshot after 3 s shows the fully drawn continuous line and all entries. No commits/push. No other files.
