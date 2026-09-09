# PRM — إدارة المشاريع (Project Management)

Source material and generation state for the PRM review. The published page is
`/S3/PRM/index.html` on the site; this folder is what it was built from.

| | |
|---|---|
| Semester | 3 |
| Published review | v01 (2026-09-09) — https://azizmarashly.github.io/SVU-MBA-Course-Review/S3/PRM/ |
| Prompt used | v0.9, DECIDE mode, no pilot, Arabic interface — settings in `PROJECT_SETTINGS.md` |
| Chapters in scope | 1–14 (the whole book, 554 pages, د. إياد زوكار) |
| Bank | 442 questions: exam 166, textbook 145, other 187, generated 21 (a question may carry several types); 69 low-confidence; 79 reconstructed; 79/79 subsections covered |
| Independent sources | 10: the book (with its highlighted review answers), six exam sittings (c. 2015, the following term, 2016, S19 of 4 Feb 2020, F24, an undated exam pool), the Asem summary (cross-check, 20/20 agree), the Emad S18 question-and-answer summary, a 20-item review set |
| Working directory | `.review_generation_working_directory/` — read its `STATE.md` first (stage checklist, decisions, how to continue) |
| Origin of the material | Student-run shared drive "SVU Files" (PRM folder) plus files circulated in the course groups. Unofficial; see `../../DISCLAIMER.md` for copyright and takedown. |

## What is in this folder

| Path | What it is |
|---|---|
| `PROJECT_SETTINGS.md` | The PROJECT SETTINGS table the review was generated with. Paste it into the current prompt to resume. |
| `.review_generation_working_directory/STATE.md` | Handoff: stage checklist, decisions, known problems, exact next step. Start here. |
| `.review_generation_working_directory/ledger.json`, `chapter_map.md` | Source ledger (hashes, independent-source groups, include/exclude reasons) and the chapter map. |
| `.review_generation_working_directory/render/` | `bank_ch01.py` … `bank_ch14.py` (question data), `common.py` (record model), `build_bank.py` (types, merges, focus areas, importance, coverage), `render_html.py` + `meta_prm.py` (the page and every course-specific table incl. the source-files appendix), `qa_blocks.py`, `release.py`, `SOURCES.md` (what each source code means), `CHAPTER_HELPER_BRIEF.md` (the per-chapter working instructions). |
| `.review_generation_working_directory/bank.json`, `out.html` | Build outputs. `out.html` is byte-identical to `/S3/PRM/index.html` and to the versioned file at this folder's root. |
| `.review_generation_working_directory/extracted/` | Book text (ligature-fixed, per chapter), subsection list, text of every source, the raw question transcriptions per source group with their reports, and the per-chapter splits. Page renders (`pages_png/`) are not in the repository (regenerable). |
| `.review_generation_working_directory/qa/` | Per-chapter reports, mechanical block checks, browser test, `summary.json` (numbers the methodology section reads). |
| `الماده الاكاديميه/` | The textbook, the book-questions PDF (dependent copy), 14 slide decks. |
| `اسئلة سابقة/` | Past-exam recollections (c. 2015 list + its handwritten scan, kifah, 2016, S19 Soufi ×2, F24, the "questions that come in the exam" pool) and one misfiled IMT exam (excluded). |
| `ملخصات سابقة/` | Asem (cross-check), Emad (S18 Q&A), the review set, and five notes/summaries without questions (excluded). |
| `متفرقات/` | A PMP certification guide (excluded). |
| `about.txt` | Two students' notes on the course (exam shape, workload); context only. |

Six duplicate files (byte-identical or converted copies) were deleted before the run; `PROJECT_SETTINGS.md` names them.
Not in the repository: `.review_generation_working_directory/archive/` (git history has every version) and the page renders.

## How to continue

**Fix an answer or add questions**

1. Edit the chapter file in `.review_generation_working_directory/render/` (`bank_ch08.py` for chapter 8, and so on).
2. Bump `.review_generation_working_directory/VERSION` (two digits) and add a row to `VERSIONS.md`.
3. Build and check:
   ```
   cd .review_generation_working_directory/render
   set PYTHONUTF8=1
   python release.py        # must print "uncovered: 0"; moves the previous file to ../archive/
   python qa_blocks.py
   ```
4. Copy `.review_generation_working_directory/out.html` over `/S3/PRM/index.html` at the repository root.
5. Run `python scripts/build_course_index.py` from the repository root so the home page shows the new version and counts, then commit.

**Add a new exam sitting or summary**

1. Put the file in the matching subfolder.
2. Open this folder in Claude Code, paste the latest prompt with the table from `PROJECT_SETTINGS.md`. Tell it the file is new; it resumes from `STATE.md`, transcribes the file per `extracted/FORMAT.md`, assigns a source code in `render/SOURCES.md` and `ledger.json`, merges into the chapter files, and rebuilds.
3. Add a row for the file to `FILES` in `render/meta_prm.py` (the source-files appendix is checked against the folder listing by `qa_blocks.py`).
4. Release and publish as above.

## Open items

- Items from older curricula (maturity levels, OPA/EEF, Delphi, network organisation) are out of scope or low-confidence; see the methodology's out-of-scope list.
- The S19/TATI earned-value table has its column labels swapped between the two sources; the five affected records name both readings.
- PDF / DOCX exports were not requested; none exist.
