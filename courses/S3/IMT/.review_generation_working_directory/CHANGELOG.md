# Changelog — مراجعه كامله لماده ال IMT

The current version number lives in `VERSION` and is stamped into the file names
(`…_vX.Y.html`, `…_vX.Y_bank.json`), the HTML cover and footer, and `file_version` in the bank JSON.
`bank/release.py` publishes the current version to the project folder and moves any older copies
into `../_old_versions/`, so the project folder always holds exactly one version.

## v1.4 — 2026-09-09 (rendered under prompt v0.9; bank unchanged)
- §19 (v0.9): the review file itself is under CC BY-NC-SA 4.0 — the "how to use" text states the
  licence conditions (share free, keep the notice, never sell) and the footer notice says the licence
  covers the review's own content, not the quoted textbook and exam text.
- §11d: "ملفات المصدر" appendix (collapsed table, one row per file in the course folder: 39 rows, kind,
  role, source group, pages/items, exclusion or duplicate note) and per-question source labels that link
  to those rows (`#3`, `#8` …). `qa_blocks.py` checks the appendix against the folder listing (NFC-normalised).
- §19: attribution and licence notice in the footer (prompt version, deliverable version, repository link,
  CC BY-NC-SA 4.0); licence terms at the end of "how to use"; `_notice` at the top of `bank.json`.
- §14: one sentence on the textbook's and exams' copyright in the privacy note.
- §13a: toolbar restructured into a one-line bar (counter, ⚙ الفلاتر button with badge, search) and a panel
  (reading mode, sliders, chapter, answer/chapter/section buttons, theme, new "إعادة ضبط التصفية" button).
  The panel overlays the content on phones, starts closed there, and the badge counts the reading mode too;
  with the panel closed a short summary of active filters shows next to the counter. Chapter and section
  headings show live visible counts; a filter or search opens any chapter/section that contains a match;
  per-chapter open/closed state is remembered; "collapse all" and "expand all" are separate buttons for
  chapters and for sections; sliders and JS-only controls are hidden without scripting; the badge hides at 0.
- §0e/§16: version in the browser title; footer says "Review file v1.4" and "Generated from prompt v0.9";
  methodology states that the bank was built and verified under v0.4 and re-rendered under v0.9.
- `STATE.md` added (§0d handoff format); `PROJECT_SETTINGS.md` spec-version row updated.

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
