# MIS — نظم المعلومات الإدارية (Management Information Systems)

Source material and generation state for the MIS review. The published page is
`/S3/MIS/index.html` on the site; this folder is what it was built from.

| | |
|---|---|
| Semester | 3 |
| Published review | **v1.0** (2026-09-24): full regeneration of the bank under the versioned prompt — https://azizmarashly.github.io/SVU-MBA-Course-Review/S3/MIS/ |
| Prompt used | v0.10 run, tooling and page at **v0.11** (§7d tables and calculations: no MIS record needs them); settings in `PROJECT_SETTINGS.md` |
| Version scheme | `vMAJOR.MINOR` (`VERSIONING.md` at the repository root); history in `.review_generation_working_directory/VERSIONS.md` (v0.1, v0.2 = the draft bank of 2026-09-06; v1.0 = the regeneration) |
| Chapters in scope | 1, 2, 3, 5, 7, 8, 9, 10 (4, 6, 11, 12 excluded by the owner) |
| Bank | 255 questions: exam 86, textbook 131, other 43, generated 22 (a question may carry several types); 72 reconstructed exam MCQs, 26 low-confidence; 105/105 audit units covered (83 by real questions, 22 only by generated ones) |
| Independent sources | 10: BOOK, S25, R44 (the 44-question sitting with its «حل دورات» key), F24, ASM (cross-check of the book set), OQ1–OQ5 (older curriculum, in-book concepts only) |
| Working directory | `.review_generation_working_directory/` — read its `STATE.md` first |
| Origin of the material | Student-run shared drive "SVU Files" (MIS folder) plus files circulated in the course groups. Unofficial; see `../../DISCLAIMER.md` for copyright and takedown. |

## What is in this folder

| Path | What it is |
|---|---|
| `PROJECT_SETTINGS.md` | The settings of the v1.0 run in the prompt's table form, the owner's extra instructions, the duplicate files removed at import. |
| `.review_generation_working_directory/STATE.md` | Handoff: stage checklist, decisions, known problems, how to continue. Start here. |
| `…/render/` | PRM's tooling adapted: `bank_ch01.py` … `bank_ch10.py` (the records), `common.py` (record model `Q`, plus `T`/`C`/`S` for §7d), `meta_mis.py` (every course specific: titles, pages, source codes, prose, source-files appendix, `SYMBOLS` — empty), `build_bank.py` (types, importance, focus areas, coverage, consolidation `MERGES`, duplicate checks), `render_html.py`, `release.py`, `qa_blocks.py`, `change_report.py`; helper briefs `CHAPTER_HELPER_BRIEF.md`, `CALC_TABLE_BRIEF.md`; extraction scripts. |
| `…/extracted/` | Book text (PyMuPDF with the lam-alef fix, `book/`, 105 audit units in `subsections.json`), source texts, 1170 transcribed raw items (`questions/`, split per chapter in `questions/by_chapter/`), the v0.2 records (`legacy/`). |
| `…/ledger.json`, `chapter_map.md/json` | Source ledger with MD5 hashes (37 files), chapter map. |
| `…/qa/` | Chapter reports, `summary.json`, `consolidation_v1.0.md`, `change_report_v0.2_to_v1.0.md`, `browser_test_v1.0.md`. |
| `…/bank.json`, `out.html`, `coverage.md` | Build outputs. The published `/S3/MIS/index.html` is `out.html` plus the Cloudflare analytics line added by `scripts/publish_page.py`. |
| `…/legacy_v0/` | The v0.1/v0.2 build (bank_a…e.py and scripts), still buildable from `legacy_v0/bank/release.py`. |
| `Dr Iyad Zoukar - MBA - MIS - The Book.pdf` | The textbook, 507 pages; printed page = PDF page. Its end-of-chapter review answers are marked in the page (tick / yellow highlight) and are used as the book's key. |
| `دورات/` | Exam recollections (`دورات.txt`: S25, «حل دورات» = key of R44, R44, F24), solved-exam scans, the older-curriculum collections, notes. |
| `ملخصات سابقة/` | The Asem summary (book questions with worked answers), `MIS Q.pdf`, a handwritten summary. |
| `ملفات بوربوينت …/` | The 12 lecture slide decks; checked for questions, none found. |

The versioned `…_v1.0.html` at this folder's root and `archive/` are gitignored; the published page and `out.html` are
the tracked copies.

## Two curricula

Most exam collections in the folder belong to an **older MIS course** (Dr Suleiman Awad: Excel Solver, pivot tables,
Hong's framework…) that does not match the current book. Their answer keys were not used; only items whose concept
exists in the current book were kept, re-verified from the book, and typed "other sources". The methodology section of
the page explains this to the reader.

## How to continue

**Fix an answer or add questions**

1. Edit `render/bank_chNN.py` (every answer cites a book page; never lower a low-confidence flag without book evidence).
2. Bump `VERSION` (MINOR) and add a row to `VERSIONS.md`.
3. Build from `render/` with `set PYTHONUTF8=1`: `python release.py` (must print `uncovered: 0` and pass the duplicate
   checks), `python qa_blocks.py`.
4. From the repository root: `python scripts/publish_page.py S3/MIS`, `python scripts/build_course_index.py`; update
   `STATE.md` and the version line above.

**Add a new exam sitting or summary**: put the file in `دورات/` or `ملخصات سابقة/`, transcribe it into
`extracted/questions/`, add the source code to `meta_mis.py` (`SRC_NAMES`, `FILES`, `SRC_ROW`) and `ledger.json`,
merge its items into existing records by claim (frequency = number of sources), then release as above.

## Open items

- Records do not yet carry raw source-item ids (`raw=[...]`); the build check for a raw id used twice is in place and
  lists the 233 real records without them.
- 3 answer blocks over 80 words and 22 T/F blocks under 40 words (accepted, see `STATE.md` §4).
