# Deliverable versions — مراجعه كامله لماده ال IMT

Scheme: `vMAJOR.MINOR`, see `VERSIONING.md` at the repository root (this file was `CHANGELOG.md` until 2026-09-24).
The current version number lives in `VERSION` and is stamped into the file names
(`…_vX.Y.html`, `…_vX.Y_bank.json`), the HTML cover and footer, and `file_version` in the bank JSON.
`bank/release.py` publishes the current version to the project folder and moves any older copies
into `../_old_versions/`, so the project folder always holds exactly one version.

| Version | Date | Spec (prompt) | Bank |
|---|---|---|---|
| v1.6 | 2026-09-24 | v0.11 | 292 → 304 (F25 added) |
| v1.5 | 2026-09-13 | v0.10 | unchanged |
| v1.4 | 2026-09-09 | v0.9 (bank built and verified under v0.4) | unchanged |
| v1.3 | 2026-09-09 | v0.4 | unchanged |
| v1.2 | 2026-09-09 | v0.4 | unchanged |
| v1.1 | 2026-09-09 | v0.4 | 292 (one summary file removed, six gap fillers added) |
| v1.0 | 2026-09-09 | v0.4 | first complete build |

## v1.6 — 2026-09-24 (F25 added; rendered under prompt v0.11)
- New exam source **F25** (`اسئلة سابقة/دورة F25.txt`, 20 items recalled by two students, no answer key; appendix row #40,
  ledger entry with MD5). All 20 used, every answer checked on the book page:
  - 8 merged into existing records (source F25 added, F25 wording as a variant where it differs): Q01-001, Q03-012,
    Q04-007 (+ page 156), Q05-001, Q05-019, Q07-005, Q10-003, Q11-001. Q03-012 and Q05-019 become exam items.
  - 12 new records: Q04-029, Q05-031, Q05-032, Q07-031, Q07-032, Q07-033, Q09-020, Q09-021, Q10-028, Q11-023,
    Q11-024, Q12-018 — 4 reconstructed (Q04-029, Q05-032, Q07-033, Q09-021), 3 low-confidence (Q05-032 fourth
    option not recalled; Q10-028 and Q11-023 recalled options make two choices correct, the book's «most important» chosen).
  - Bank 292 → 304 (exam 107 → 121); low-confidence 24 → 27; reconstructed 13 → 17; focus areas +7-4, +9-3-1,
    +12-2-2, −12-4; 16 importance scores moved as a result. No existing answer, page (except Q04-007 +156) or flag changed.
- Prompt v0.11 §7d ported from the PRM renderer: `T`/`C`/`S` in `common.py`, `render_table`, `render_calc`, symbol chip
  row + tap-to-open bottom sheet (`SYMBOLS` in `render_html.py`: GDP, GNI), build refuses `|` in stems, §7d lines in
  `qa_blocks.py`. IMT has no calculation items; answer tables added to Q01-023 (table 1-1, p16) and Q04-018 / Q04-029
  (World Bank income classes, figure 4-4, p143; shared `INCOME_T`); their `why` lines now name the rule only. Numbers
  re-read from the page images (table 1-1 shares recomputed: 21.4/14.3/5.1/3.9 of an implied 87.7 trillion).

## v1.5 — 2026-09-13 (rendered under prompt v0.10; bank unchanged)
- §13a (v0.10): the seven prose blocks (how to use, scope, methodology, source files, reference lists,
  contents, file metadata) are collapsible like chapters; intro blocks open, end blocks closed by default,
  state remembered; "طيّ الكل" / "فتح الكل" buttons fold chapters, types and blocks together. The metadata
  summary line keeps version, spec and licence visible. No question, answer or score changed.

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

## v1.3 — 2026-09-09 (prompt v0.4)
- Toolbar: filters (sliders, chapter select, search, fold/theme buttons) collapse behind a «⚙ الفلاتر» button
  on screens up to 760 px wide; the button shows the number of active filters. Remembered per device.
- No change to the question bank.

## v1.2 — 2026-09-09 (prompt v0.4)
- Chapters and question-type sections are collapsible (click the heading, or the two toolbar buttons).
- Importance and repetition filters became sliders (minimum 1–5 and 0–5) instead of fixed buttons.
- Version number added to file names and metadata; release script added.
- No change to the question bank.

## v1.1 — 2026-09-09 (prompt v0.4; was published unversioned)
- One summary file was removed from the inputs at the user's request. Every record that relied on it
  was dropped or re-sourced, and every textual mention of it was removed.
- Coverage audit rerun; six gap-filler records added in `bank/bank_extra.py` so all 109 subsections are covered.
- Bank: 292 questions (exam 107, textbook 142, other 50, generated 15).

## v1.0 — 2026-09-09 (prompt v0.4; was published unversioned)
- First complete build from the v0.4 spec: 11 chapters, Arabic UI, ASK mode.
