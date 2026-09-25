# ACM — المحاسبة للمديرين (Accounting for Managers)

Source material and generation state for the ACM review. The published page is `/S2/ACM/index.html` on the site;
this folder is what it was built from.

| | |
|---|---|
| Semester | 2 |
| Published review | **v1.0** (2026-09-25) — https://azizmarashly.github.io/SVU-MBA-Course-Review/S2/ACM/ |
| Prompt used | v0.12, DECIDE mode, no pilot, Arabic interface — settings in `PROJECT_SETTINGS.md` |
| **Scope** | **The F25 sitting only** (exam 2026-09-26), from `Exams/المطلوب بدوره F25 بالامتحان.txt`: chapters 1, 2, 3, 10 in full; chapter 7 in full without journal entries; chapters 8, 9 theory only; 4, 5, 6 excluded. The page says so on its cover. |
| Bank | 209 questions in 7 chapters (1: 23, 2: 47, 3: 17, 7: 38, 8: 27, 9: 11, 10: 46); by type exam 97, textbook 119, other 1, generated 20 (a question can be exam and textbook); 81 audit units, all covered (61 by real questions, 20 by generated); 51 reconstructed, 16 low-confidence; 65 calculation blocks, 13 figures, 34 unsolved book exercises solved |
| Independent sources | 9: the book (review answers marked on its pages, verified against the text), six exam sittings (S23, F23, S24, F24, S25, older/unattributed), the Asem summary (cross-check), students' solutions of the chapter-3 exercises |
| Working directory | `.review_generation_working_directory/` — read its `STATE.md` first |
| Origin of the material | Files circulated in the course's Telegram groups (MBA general group and the semester sub-group); the recalls were folded from the groups' messages, anonymised. Unofficial; see `../../DISCLAIMER.md` for copyright and takedown. |

## What is in this folder

| Path | What it is |
|---|---|
| `PROJECT_SETTINGS.md` | The settings of the v1.0 run in the prompt's table form, the owner's extra instructions, the reorganisation done before the run. |
| `.review_generation_working_directory/STATE.md` | Handoff: stage checklist, decisions, known problems, how to continue. Start here. |
| `…/render/` | PRM's tooling rewritten for prompt v0.12: `bank_chNN.py` (records), `common.py` (record model `Q` + `T`/`C`/`S`/`F`/`M`), `meta_acm.py` (every course specific incl. the F25 scope banner, `SYMBOLS`, the source-files appendix), `build_bank.py`, `render_html.py`, `qa_blocks.py`, `release.py`; briefs `CHAPTER_HELPER_BRIEF.md`, `CALC_TABLE_BRIEF.md`, `EXAMPLE_RECORD.py`, `SOURCES.md`. |
| `…/extracted/` | Book text per page and per chapter (`scripts/pdf_text` extraction), `subsections.json` (81 audit units of the scope), the small PDFs' text, the transcriptions (`questions/`), the stage-3 briefs. Page renders (`pages_png/`) are not in the repository. |
| `…/ledger.json`, `chapter_map.md/json` | Source ledger with MD5 hashes (37 files) and the chapter map. |
| `Course/` | The textbook (447 pages, د. باسل أسعد 2021), two page-copies of its questions and cases (dependent), the 14 lecture decks (no questions), students' scanned solutions of chapters 3–5 exercises. |
| `Exams/` | Exam recollections per sitting (owner's files + `<sitting> - تلغرام.txt` folded from the groups), the written S24 questions, the F24 chart, the F25 scope, study advice, two book-errata images. |
| `Summaries/` | The Asem theory summary (cross-check). |

## How to continue

**Fix an answer or add questions**

1. Edit the chapter file in `.review_generation_working_directory/render/` (every answer cites a book page; never lower a low-confidence flag without book evidence).
2. Bump `.review_generation_working_directory/VERSION` (MINOR) and add a row to `VERSIONS.md`.
3. Build from `render/` with `set PYTHONUTF8=1`: `python release.py` (must print `uncovered: 0` and pass the duplicate checks), `python qa_blocks.py`.
4. From the repository root: `python scripts/publish_page.py S2/ACM`, `python scripts/build_course_index.py`; update `STATE.md` and the version line above.

**Add a new exam sitting**: put the file in `Exams/`, transcribe it into `extracted/questions/` per `extracted/FORMAT.md`, add the source code to
`meta_acm.py` (`SRC_NAMES`, `FILES`, `SRC_ROW`, `EXAM_CODES`) and `ledger.json`, merge its items into existing records by claim, then release as above.

**Widen the scope** (a later sitting that requires chapters 4–6 or the entries of chapter 7): add the units to `extracted/book/subsections.json`,
the chapters to `meta_acm.CHAPTERS`, run chapter helpers for them, and replace the scope banner; the out-of-scope exam items are already
transcribed in `extracted/questions/` with `in_scope: false`.
