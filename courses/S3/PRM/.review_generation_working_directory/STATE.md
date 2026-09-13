# STATE — PRM review (handoff file, §0d)

## 1. Settings in force
- Spec v0.11 (v0.9 at generation; re-rendered under v0.10 and v0.11), interaction mode DECIDE, pilot NONE, Arabic interface/questions/explanations, chapters 1–14 (settings table: `../PROJECT_SETTINGS.md`).
- Primary reference: `الماده الاكاديميه/MBA - Project Management - The Book.pdf` (554 pages, printed page = PDF page, 0 mismatches).
- Deliverable version: **v03** (`VERSION`), 2026-09-14 (v01 2026-09-09, v02 2026-09-13). PDF/DOCX: not produced (DECIDE default).

## 2. Stage checklist
| Stage | Status | Produced |
|---|---|---|
| 1 Read reference, verify extraction | done — PyMuPDF text; lam-alef ligature reversed by the font and fixed at character level | `extracted/book/book_fixed.txt`, `extracted/book/ch_fixed/`, `extracted/book/subsections.json` (79 level-2 subsections) |
| 2 Curriculum check, 2a chapter map | done — discriminator in `extracted/questions/others_report.md` | `chapter_map.md`, `chapter_map.json` |
| 3 Extract questions | done — 1003 raw items (book 187, soufi 162, recalls 227, others 427), 123 images/pages read visually | `extracted/questions/*.json`, `*_report.md`, `by_chapter/` |
| 4 Source ledger with hashes | done — 10 independent sources (BOOK, EX15, KIFAH, Y16, S19, F24, TATI, ASEM, EMAD, MURAJA); 6 duplicate files deleted before the run | `ledger.json`, `render/SOURCES.md`, `render/meta_prm.py` (FILES, 35 rows) |
| 5 Deduplicate | done — 442 canonical (4 cross-chapter merges in `build_bank.py` MERGES) | `render/bank_ch01..14.py` |
| 6 Conservative editing | done | — |
| 7 Verify + answer blocks, 7c low confidence | done — 69 low-confidence, 79 reconstructed | bank files, `qa/chNN_report.md` |
| 8 Cross-check | done — ASEM 20/20 agree with the book highlights; SOUFI-XCHK not a source | `qa/summary.json` |
| 9 Coverage audit + generated | done — 79/79 covered; 68 by real questions, 11 by 21 generated (DECIDE default applied, no volume question asked) | `bank.json → coverage` |
| 10 Focus areas + importance | done — rule: subsections with ≥2 exam sources else top-2 with ≥1 | `bank.json → focus_table` |
| 11 Document structure, 11a–11d | done | `render/render_html.py`, `render/meta_prm.py` |
| 12 Bilingual formatting | done (RTL root, ltr spans for codes/paths) | CSS in `render_html.py` |
| 13 HTML deliverable, 13d bank checkpoint | done — v03 | `bank.json`, `out.html`, `../مراجعه كامله لماده ال PRM_v01.html`, `/S3/PRM/index.html` |
| 14 Privacy note | done (how-to + methodology) | — |
| 15 QA | done — `qa/qa_blocks_v01.txt`, `qa/browser_test_v01.md`; 20-block random sample read by eye; v03: `qa/qa_blocks_v03.txt` (§7d lists empty), Q08-007/Q10-005/Q10-022/Q09-020 checked in Chrome at desktop and 390 px | `qa/` |

## 3. Decisions not obvious from the files
- Audit unit = level-2 TOC headings (79); level-3 headings are topics inside them (stated in the methodology).
- Types derived from sources in `build_bank.py` (`normalise_types`): exam ⇔ exam sitting, textbook ⇔ BOOK, other ⇔ EMAD/MURAJA; ASEM adds to `sources` only.
- Exam sittings: EX15 (= PM-112هام.docx + scan + kifah p4–5, c. 2015), KIFAH (kifah p1–3, the following term), Y16, S19 (= Soufi_1 + non-book items of the Soufi bank), F24, TATI (undated pool, older vocabulary, concept-in-book items only).
- The book's chapter 2/6/8 reviews reprint chapters 1/5/7; each question is one record, placed in the chapter its content belongs to.
- Maturity-model, OPA/EEF, Delphi and network-organisation items: not in the book → out-of-scope list or low-confidence records with `book_says`.
- IMT renderer reused; `render_html.py` overrides `CHAPTERS` from the bank and reads `qa/summary.json` for methodology numbers.

- v03 (2026-09-14, prompt v0.11 §7d): the 44 table/calculation records (Q03-002; Q07-001/021/022/023; Q08-001…016; Q09-003…007/020/021; Q10-005…014/020…023/026/027) carry `table` / `ans_table` / `calc` (`T()`, `C()`, `S()` in `common.py`); shared constants per data set (`NET1/2/3`, `NET3M`, `TBL_X`, `TBL_A/B` with `_Q`, `_T`, `_ANS`, `_RES`); `why` is concept-only. An always-visible «الرموز» chip row under each such question comes from the structured `SYMBOLS` glossary in `meta_prm.py` (four fields: ar, en, f, note); tapping a chip or any underlined symbol in a table / calc cell opens a bottom sheet (touch-first, glossary embedded as JSON + `SYM_JS`); pointer devices also get a hover card. Presentation only: no answer, page, source or low-confidence flag changed; every number was recomputed by the converting helper and matched. Rules for helpers: `render/CALC_TABLE_BRIEF.md`. The build refuses a stem containing `|`; `PRM_LENIENT=1` downgrades that to a warning during partial edits.
- Q09-020/021 (levelling essays): the single `ans_table` slot holds the per-day resource histogram (the answer's deliverable); per-activity times sit in `calc.given`.

## 4. Known problems and open questions
- 23 answer blocks exceed 80 words without an optional line (essays/calculations/lists) — accepted under §0a, listed in `qa/qa_blocks_v01.txt`.
- "Why repeats answer" check: 30 hits inspected, all name the term legitimately; one opener («الجواب هو») fixed.
- The recalled S19/TATI EVA table has swapped column labels between sources; five records carry `low_conf` with the alternative answers.
- Not tested: printing, screen readers, real phone device. PDF/DOCX not produced.

## 5. To continue
Nothing pending. Possible follow-ups: extend the same §7d form to IMT (its renderer lacks it); review the 22 blocks over 80 words listed in `qa/qa_blocks_v03.txt` (accepted under §0a). For a fix: edit `render/bank_chNN.py`, bump `VERSION` (two digits), add a row to `VERSIONS.md`, run from `render/`:
`set PYTHONUTF8=1 && python release.py && python qa_blocks.py` (previous deliverable moves to `archive/`), then at the repository root
`python scripts/publish_page.py S3/PRM` (adds the analytics snippet) and `python scripts/build_course_index.py`, update this file.
