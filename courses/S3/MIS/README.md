# MIS — نظم المعلومات الإدارية (Management Information Systems)

Source material and generation state for the MIS review. The published page is
`/S3/MIS/index.html` on the site; this folder is what it was built from.

| | |
|---|---|
| Semester | 3 |
| Published review | v0.2 (2026-09-13): the v0.1 content of 2026-09-06 re-rendered with the licence notice and the source-files appendix — https://azizmarashly.github.io/SVU-MBA-Course-Review/S3/MIS/ |
| Prompt used | none: generated on 2026-09-06 from an ad hoc 15-section brief, before the versioned prompt existed; prompt v0.1 was written from this run. Settings restated in `PROJECT_SETTINGS.md` |
| Latest prompt in repo | v0.9 — this review is **not** in line with it (no importance score, no focus areas, no low-confidence flag, no sliders or collapsible chapters; the answer block is answer + explanation only) |
| Chapters in scope | 1, 2, 3, 5, 7, 8, 9, 10 (4, 6, 11, 12 excluded by the owner) |
| Bank | 269 questions: exam 91, textbook 141, other 23, generated 33 (a question may carry several types); 101/101 book subsections covered; no low-confidence flag in this schema |
| Independent sources | 11 in the bank (BKQ, S25, HD, R44, F24, ASM, OQ1–OQ5); the page's own text says 10 because the Asem summary was added as a cross-check late in the run and the count was not updated |
| Working directory | `.review_generation_working_directory/` — read its `STATE.md` first |
| Origin of the material | Student-run shared drive "SVU Files" (MIS folder) plus files circulated in the course groups. Unofficial; see `../../DISCLAIMER.md` for copyright and takedown. |

## What is in this folder

| Path | What it is |
|---|---|
| `PROJECT_SETTINGS.md` | The settings the review was generated with, restated in the prompt's table form; the owner's extra instructions; the duplicate files removed at import. |
| `.review_generation_working_directory/STATE.md` | Handoff: how the run went, decisions, known problems, how to continue. Start here. |
| `.review_generation_working_directory/bank/` | `bank_a.py` (ch 1–3), `bank_b.py` (5, 7), `bank_c.py` (8–10), `bank_d.py` (section 3: other sources), `bank_e.py` (section 4: generated); `build_html.py` (the page), `build_docx.py` + `pipeline.py` + `build_pdf.py` (DOCX and interactive PDF; need Word), `coverage.py` (101-subsection audit), `qa.py`; `meta_mis.py` (source-files table); `build_bank.py` (exports `bank.json`); `release.py`. |
| `.review_generation_working_directory/bank.json`, `out.html` | Build outputs. The published `/S3/MIS/index.html` is `out.html` plus the Cloudflare analytics line added by `scripts/publish_page.py`. |
| `.review_generation_working_directory/src/` | Text extraction of every question source (`S01`–`S12`; the mapping to file names is in `STATE.md`). |
| `.review_generation_working_directory/txt/` | `book_pages.txt` (all 507 pages, `[pN]` prefixed) and `book_questions.txt` (the end-of-chapter question pages). |
| `Dr Iyad Zoukar - MBA - MIS - The Book.pdf` | The textbook, 507 pages; printed page = PDF page. |
| `دورات/` | Exam recollections: `دورات.txt` (four sittings in one file: S25, «حل دورات», the 44-question sitting, F24), solved-exam scans, the older-curriculum collections, notes, `info.txt` (students' notes on the course). |
| `دورات/اسئلة سابقة/` | A scanned 50-item answer key of the older curriculum (`دورات.pdf`) and its photographs (`MISS/`, 7 unique). |
| `ملخصات سابقة/` | The Asem summary (book questions with worked answers; used), `MIS Q.pdf` (used), a handwritten summary (no questions; unused). |
| `ملفات بوربوينت …/` | The 12 lecture slide decks; checked for questions, none found. |

Not in the repository: the original deliverables `مراجعه كامله لماده ال MIS-v0.1.{html,docx,pdf}`
(the HTML is reproduced byte for byte by the v0.1 state of `release.py`; DOCX and PDF need Word
and were not regenerated), the QA renders, and 8 byte-identical duplicate files (listed in
`PROJECT_SETTINGS.md`). The versioned `…_v0.2.html` at this folder's root is gitignored; the
published page and `out.html` are the tracked copies.

## Two curricula

Most exam collections in the folder belong to an **older MIS course** (Dr Suleiman Awad: Excel
Solver, pivot tables, Hong's framework…) that does not match the current book. Their answer keys
were not used; only items whose concept exists in the current book were kept, re-verified from
the book, and placed in section 3 ("other sources"). The methodology section of the page explains
this to the reader.

## How to continue

**Fix an answer or add questions**

1. Edit the chapter file in `.review_generation_working_directory/bank/` (`bank_a.py` for chapters 1–3, `bank_b.py` for 5 and 7, `bank_c.py` for 8–10; `bank_d.py` and `bank_e.py` for sections 3 and 4).
2. Bump `.review_generation_working_directory/VERSION` and add a line to `CHANGELOG.md` next to it.
3. Build:
   ```
   cd .review_generation_working_directory/bank
   set PYTHONUTF8=1
   python release.py        # out.html + bank.json + the versioned file in this folder
   python coverage.py       # optional: the 101-subsection coverage audit
   ```
   `build_html.py` imports `build_docx.py`, so `python-docx` must be installed; Word is needed only for `pipeline.py`.
4. Publish from the repository root: `python scripts/publish_page.py S3/MIS`, then `python scripts/build_course_index.py`, then commit.

**Add a new exam sitting or summary**

1. Put the file in `دورات/` or `ملخصات سابقة/`.
2. Open this folder in Claude Code, paste the latest prompt with the table from `PROJECT_SETTINGS.md`; tell it the file is new. It resumes from `STATE.md`. New questions go to the matching `bank_*.py` with a new source code in `SRC_AR` (`build_docx.py`) and a row in `meta_mis.py` (`FILES`, `SRC_ROW`).
3. Release and publish as above.

**Bring the review up to prompt v0.9**

Not done. It needs new content for every question (the "remember" and "distractors" lines, the
importance score, the subsection mapping, the low-confidence review), so it is a regeneration
with the current prompt, not a re-render; PRM's `render/` tooling is the template. The v0.2
re-render only added what needs no new content.

## Open items

- The page states 10 independent sources; the bank has 11 (see above).
- DOCX and interactive PDF exist only as the v0.1 originals outside the repository.
