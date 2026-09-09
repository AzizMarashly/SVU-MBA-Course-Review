# Changelog — مراجعه كامله لماده ال IMT

The current version number lives in `VERSION` and is stamped into the file names
(`…_vX.Y.html`, `…_vX.Y_bank.json`), the HTML cover and footer, and `file_version` in the bank JSON.
`bank/release.py` publishes the current version to the project folder and moves any older copies
into `../_old_versions/`, so the project folder always holds exactly one version.

## v1.3 — 2026-09-09
- Toolbar: filters (sliders, chapter select, search, fold/theme buttons) collapse behind a «⚙ الفلاتر» button
  on screens up to 760 px wide; the button shows the number of active filters. Remembered per device.
- No change to the question bank.

## v1.2 — 2026-09-09
- Chapters and question-type sections are collapsible (click the heading, or the two toolbar buttons).
- Importance and repetition filters became sliders (minimum 1–5 and 0–5) instead of fixed buttons.
- Version number added to file names and metadata; release script added.
- No change to the question bank.

## v1.1 — 2026-09-09 (was published unversioned)
- One summary file was removed from the inputs at the user's request. Every record that relied on it
  was dropped or re-sourced, and every textual mention of it was removed.
- Coverage audit rerun; six gap-filler records added in `bank/bank_extra.py` so all 109 subsections are covered.
- Bank: 292 questions (exam 107, textbook 142, other 50, generated 15).

## v1.0 — 2026-09-09 (was published unversioned)
- First complete build from the v0.4 spec: 11 chapters, Arabic UI, ASK mode.
