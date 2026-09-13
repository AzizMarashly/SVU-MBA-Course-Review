# HANDOFF — work in progress as of 2026-09-14

Written for the next agent. Read `CLAUDE.md` first, then this file. Delete this file (or empty it)
when everything below is committed and the MIS run is finished.

## A0. Uncommitted, ready to commit: prompt v0.11 + PRM v03 (2026-09-14) — MIS paths must stay OUT of this commit

Prompt **v0.11** adds §7d "Tables and calculations" (data as a real table under the stem; answer opens with the
working table, then a «الحساب» block: given values with origin, then المعادلة → التعويض → الناتج per step; an
always-visible «الرموز» chip row; tapping a chip or an underlined symbol opens a bottom sheet with name / English
name / formula / note from the structured `SYMBOLS` glossary — touch-first; §15 QA checks incl. glossary coverage). PRM **v03** is the
re-render: 44 records converted (ch. 3, 7, 8, 9, 10), no answer/page/source changed, all numbers recomputed by the
helpers and matched. Details: PRM `STATE.md` §3, `VERSIONS.md`, `render/CALC_TABLE_BRIEF.md`.

Commit these (owner's call) and then tag `v0.11`:
`prompt/SVU-MBA-Course-Review-Generator.md`, `prompt/CHANGELOG.md`, `CLAUDE.md`, `HANDOFF.md`, `S3/PRM/index.html`,
`courses.json`, `courses/S3/PRM/README.md`, and under `courses/S3/PRM/.review_generation_working_directory/`:
`STATE.md`, `VERSION`, `VERSIONS.md`, `bank.json`, `out.html`, `qa/qa_blocks_v03.txt`, `render/*` (common, build_bank,
render_html, qa_blocks, meta_prm, bank_ch03/07/08/09/10, CHAPTER_HELPER_BRIEF.md, new CALC_TABLE_BRIEF.md).
**Do not add anything under `courses/S3/MIS/`** (its working directory is mid-regeneration; see B/B1). `courses.json`
was rebuilt against the committed MIS bank on purpose, so it is correct as is.

## A. Committed: prompt v0.10 + IMT v1.5 + PRM v02 (commit "Prompt v0.10: collapsible page sections", tag v0.10)

Prompt **v0.10** adds one rule to §13a ("Collapsible page sections"): the seven prose blocks of the
HTML (how to use, scope, methodology, source files, reference lists, contents, file metadata) fold
like chapters; intro blocks open and end blocks closed by default; state remembered per block;
toolbar buttons "طيّ الكل" / "فتح الكل" fold chapters, question sections and blocks together and leave
answers alone; the metadata summary line keeps version, spec and licence visible when folded.
Implemented by a `fold_sections()` post-processing step at the end of `build()` in both renderers,
so the two copies stay identical. IMT v1.5 and PRM v02 are re-renders with no content change,
verified field by field and tested in Chrome.

MIS v0.2 (published) does **not** have the v0.10 sections; it is superseded by the regeneration
below rather than patched.

## B. In progress: MIS regeneration under prompt v0.10 (target v1.0)

**Why:** MIS v0.2 was a re-render of a bank generated on 2026-09-06 before the versioned prompt; it has
no importance score, focus areas, low-confidence flag, three-line answer blocks, subsection mapping,
sliders or collapsible chapters. A regeneration under the current prompt is the only way to align it.

**Where:** `courses/S3/MIS/.review_generation_working_directory/` now has the standard §0d layout
(`STATE.md`, `ledger.json`, `chapter_map.md/json`, `extracted/`, `render/`, `qa/`, `archive/`,
`VERSIONS.md`, `VERSION` = 1.0). The v0.2 build was moved intact to `legacy_v0/` (still buildable
from there: `legacy_v0/bank/release.py`), its extractions to `extracted/legacy_src/` and
`extracted/legacy_txt/`. `render/` is PRM's tooling adapted (`meta_mis.py`, `common.py` with a
`legacy_id` field, `build_bank.py`, `render_html.py` at v0.10, `qa_blocks.py`, `release.py` for the
`vX.Y` scheme, `CHAPTER_HELPER_BRIEF.md`, `SOURCES.md`, `EXAMPLE_RECORD.py`, plus the extraction
scripts `extract_book.py`, `extract_sources.py`, `split_by_chapter.py`, `hash_files.py`).

**Settings:** the table in `courses/S3/MIS/PROJECT_SETTINGS.md` with these overrides: DECIDE mode, no
pilot, spec v0.10, deliverable version 1.0 (`vX.Y` kept for continuity with v0.1/v0.2, a recorded
deviation from §0e), PDF/DOCX never.

**Done (stages 0–4):** layout; book re-extracted with PyMuPDF and the lam-alef fix, page numbers
verified for all 507 pages, 105 audit units from the finest TOC level (`extracted/book/`); chapter
map; ledger with MD5 hashes for all 37 files (`ledger.json`, `extracted/hashes.json`); **all sources
transcribed**: 1170 raw items (exams 157, book 137, Asem 155, OQ1–3 533, OQ4–5 and old-book
candidates 188), 137 pages/images read visually, split into `extracted/questions/by_chapter/chNN.json`
(710 in scope, 460 out of scope in `out_of_scope.json`), with a report per source group.

**Decisions taken (also in STATE.md):** «حل دورات» (block 2 of `دورات.txt`, HD in v0.2) is the answer
key of the 44-question sitting (block 3) → one exam source R44, so v0.2 frequencies that counted both
drop by one. OQ1–OQ5 are older-curriculum collections → type "other", in-book concepts only, keys never
imported. ASM = cross-check only. The book prints its own answers inline (ticks for true/false, yellow
highlights for MCQ) and the Asem summary agrees on all 113 shared items; the helper brief and the
scope/methodology prose must state this (the v0.2 run assumed the book had no keys). Legacy generated
questions are kept where their unit is still uncovered by real questions.

**In progress (stages 5–9):** chapter helpers writing `render/bank_chNN.py` from
`render/CHAPTER_HELPER_BRIEF.md`, using `extracted/legacy/chNN.json` (the 269 v0.2 records) and
`extracted/questions/by_chapter/chNN.json`. Paused on 2026-09-13 at 20:00 to save tokens.

| Chapter | Status | Records |
|---|---|---|
| 1, 2, 3, 5 | **done**: `render/bank_ch01/02/03/05.py` + `qa/ch0N_report.md` | 34, 48, 33, 34 (149 total; 45 reconstructed MCQs, 18 low-confidence) |
| 7, 8, 9, 10 | **not started** (legacy 25 / 29 / 31 / 36 records; raw items 34 / 57 / 83 / 134) | — |

The current `bank.json` and `coverage.md` are **partial (four chapters) and must not be published**.
Extra findings recorded in STATE.md: only Q05-020 answers against the book's own tick (shown via
`book_says`); the annotated older textbook stays excluded (30 candidates kept aside as
OQ6-CANDIDATE, unused); three intranet items moved from chapter 7's review set to chapter 2, so the
chapter-7 helper must drop legacy C7-17/18/19.

**To resume** (a new session, opened at the repository root): read `CLAUDE.md`, this file, then
`courses/S3/MIS/.review_generation_working_directory/STATE.md` and follow its **§5 "To continue"**,
which is the authoritative eight-step sequence. In short:

1. Chapter helpers for 7, 8, 9, 10 (general-purpose subagents, 2–4 at a time; four tripped the
   session limit once), each with the brief, `extracted/book/ch_fixed/chNN.txt`, its legacy and
   transcribed JSON, the chapter-specific notes in STATE.md §5 step 1; each writes
   `render/bank_chNN.py` + `qa/chNN_report.md`.
2. Reinstate G1-01 for unit 1-1-2 (or document 104/105); replace `{asem_agree}` in `qa/summary.json`.
3. From `render/` with `PYTHONUTF8=1`: `python build_bank.py`, `python release.py`,
   `python qa_blocks.py`, `python change_report.py` → `qa/change_report_v0.2_to_v1.0.md`.
4. Browser test at desktop and ~390 px; `qa/browser_test_v1.0.md`; read 20 random answer blocks.
5. Finish `STATE.md`, `VERSIONS.md`, `../README.md`, `../PROJECT_SETTINGS.md`;
   `render/meta_mis.py` `GENERATED_DATE` = release date.
6. Repository root: `python scripts/publish_page.py S3/MIS`, `python scripts/build_course_index.py`.
7. Final report to the owner: §16 completion summary + the v0.2 → v1.0 change report (the owner
   knows v0.2 well and wants exact counts and ids). Then commit (owner's call): the MIS paths plus
   `courses.json` and `S3/MIS/index.html`.

Rules that apply: cite the book page for every answer; never invent options, answers or pages; no
personal data in the review or file names; keep source files unchanged; `out.html` without the
Cloudflare snippet (`publish_page.py` adds it); never import the older-curriculum answer keys.

## B1. MIS tooling already carries prompt v0.11 §7d (2026-09-14)

`courses/S3/MIS/.review_generation_working_directory/render/` was patched together with PRM: `common.py`
(`T`, `C`, `S`, `table` / `ans_table` / `calc` fields), `render_html.py` (tables, calculation block, symbol
legend), `build_bank.py` (refuses `|` in stems unless `PRM_LENIENT=1`), `qa_blocks.py` (§7d lines),
`meta_mis.py` (`SYMBOLS` glossary — currently PRM's list; trim/extend for MIS), `CALC_TABLE_BRIEF.md` and a
§7d paragraph in `CHAPTER_HELPER_BRIEF.md`. Chapter helpers for 7–10 must write calculation items in that form.
The partial MIS `bank.json` / `out.html` were rebuilt during the smoke test (same four chapters; still not
publishable). `courses.json` in the working tree was rebuilt against the committed MIS bank on purpose.

## B2. IMT: new exam source waiting

`courses/S3/IMT/اسئلة سابقة/دورة F25.txt` (20 recalled questions, two students merged) was added on
2026-09-13 without a run. It needs the "add a new exam sitting" procedure in the IMT README: extract,
deduplicate against the bank, verify, add source code F25 + appendix row + ledger entry, release v1.6.
Cheap: one session, no helpers.

## C. Token note

The chapter-helper stage is the expensive part (roughly 150k–300k tokens per chapter). Everything
before it is done and checkpointed; nothing is lost by pausing.
