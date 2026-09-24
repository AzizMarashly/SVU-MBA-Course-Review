# STATE — MIS review (handoff file, §0d)

**Run finished 2026-09-24: v1.0 released and published to `/S3/MIS/index.html` (not committed; `courses.json` not rebuilt — the owner session runs `scripts/build_course_index.py` for all courses).**
Read this whole file before touching the course; section 5 says what to do next.

## 1. Settings in force
- Spec: run under **v0.10**, tooling and page at **v0.11** (§7d tables/calculations; no MIS record needs one, `SYMBOLS` is empty), interaction mode **DECIDE**, pilot NONE, Arabic interface/explanations, questions MIXED (Arabic with English terms), chapters 1, 2, 3, 5, 7, 8, 9, 10 (settings table: `../PROJECT_SETTINGS.md`). PDF/DOCX: NEVER.
- Primary reference: `Dr Iyad Zoukar - MBA - MIS - The Book.pdf` (507 pages, printed page = PDF page, 0 mismatches).
- Deliverable version: **v1.0** (`VERSION` = `1.0`), scheme `vMAJOR.MINOR` of `VERSIONING.md` (MAJOR 1 = first full generation). Output file: `../مراجعه كامله لماده ال MIS_v1.0.html`; the v0.2 file was moved to `archive/` by `release.py`.
- Last update: 2026-09-24, release of v1.0.

## 2. Stage checklist
| Stage | Status | Produced |
|---|---|---|
| 0 Working directory | done — the v0.2 run lives in `legacy_v0/` (bank_a..e.py, build scripts, bank.json, out.html, STATE/CHANGELOG/VERSION; still buildable from `legacy_v0/bank/`), old extractions in `extracted/legacy_src/`, `extracted/legacy_txt/`; PRM `render/` tooling copied and adapted: `meta_mis.py` (all course specifics), `common.py` (+ `legacy_id`), `build_bank.py` (units from `extracted/book/subsections.json`, coverage.md writer, page-range warning), `render_html.py` (prose from meta_mis, localStorage prefix `mis`), `qa_blocks.py`, `release.py` (vX.Y) | this layout |
| 1 Read reference, verify extraction | done — `render/extract_book.py` (PyMuPDF, lam-alef fix, page numbers verified for all 507 pages) | `extracted/book/book_fixed.txt`, `ch_fixed/chNN.txt` (in-scope chapters), `toc_raw.txt`, `subsections.json` + `subsections.md` (105 audit units) |
| 2 Curriculum check, 2a chapter map | done — discriminator counts in `extracted/questions/*_report.md` (all OQ files older curriculum; دورات.txt, book, Asem current) | `chapter_map.md`, `chapter_map.json` |
| 3 Extract questions | done — `render/extract_sources.py` → `extracted/srcNN/text.txt` + `extracted/index.json`; 4 helpers → 1170 raw items (exams 157, book 137, Asem 155, OQ1–3 533, OQ4–5 + old-book candidates 188); 137 pages/images read visually; `render/split_by_chapter.py` → 710 in scope, 460 out of scope/unassigned | `extracted/questions/{exams,book,asem,others_a,others_b}.json` + `*_report.md`, `by_chapter/chNN.json`, `out_of_scope.json`, `extracted/STAGE3_BRIEF.md` |
| 4 Source ledger with hashes | done — `render/hash_files.py` → 37 files, no duplicate hashes; 10 independent sources (BOOK, S25, R44, F24, ASM, OQ1–OQ5) | `extracted/hashes.json`, `ledger.json`, `render/SOURCES.md`, `render/meta_mis.py` (FILES 37 rows, SRC_ROW, FILES_SUMMARY) |
| 5–9 per chapter | done — ch 1 (35 records incl. the reinstated G1-01 = Q01-035), 2 (48), 3 (32), 5 (34), 7 (20), 8 (27), 9 (27), 10 (32) after consolidation | `render/bank_ch01…10.py`; `qa/chNN_report.md` |
| 9b Consolidation (I-11) | done — whole-bank pass after the helpers: 4 true duplicates merged (`MERGES` in `build_bank.py`), same-fact-other-form pairs listed; build checks added (`check_duplicates`) | `qa/consolidation_v1.0.md` |
| 10 Focus areas + importance | done — 24 focus units; importance 1: 44, 2: 94, 3: 97, 4: 18, 5: 2 | `bank.json`, `coverage.md` (105/105 covered: 83 by real questions, 22 by generated only) |
| 11–13 Render, bank checkpoint | done — `release.py`: `out.html` 773 KB, `../مراجعه كامله لماده ال MIS_v1.0.html`; bank checkpoint `bank.json` (file_version 1.0, spec v0.11) | `out.html`, `bank.json` |
| 14 Privacy note | in the renderer (how-to + methodology) | — |
| 15 QA | done — `qa_blocks.py` clean except accepted length hits (§4); `change_report.py`; browser test desktop + 390 px; 20 random blocks read | `qa/change_report_v0.2_to_v1.0.md`, `qa/browser_test_v1.0.md` |
| 16 Docs / publish | done — `../README.md`, `../PROJECT_SETTINGS.md`, `VERSIONS.md`; `scripts/publish_page.py S3/MIS` run; not committed | `/S3/MIS/index.html` |

## 3. Decisions not obvious from the files
- Audit unit = the finest TOC level (N-M-K; N-M where a section has no sub-headings): 105 units. PRM used N-M, but here N-M gives only 30 units for 8 chapters; the finest level reconciles with the 101 hand-picked subsections of v0.2. Stated in the methodology text.
- «حل دورات» (block 2 of `دورات.txt`, code HD in v0.2) is the answer key of the 44-question sitting (block 3): same items, same order → ONE exam source **R44**. `حل دورتين Mis.pdf` pp. 1–3 copy block 2 and pp. 3–11 copy the F24 list (dependent copy of both). Frequencies of questions that had HD+R44 drop by one; legacy sources were renamed HD→R44, BKQ→BOOK in `extracted/legacy/chNN.json`.
- The untitled topic list at the end of `دورات.txt` (block 5) is kept as topic evidence under F24; no records.
- **The book prints its review answers inline** (tick in the صح/خطأ column, yellow highlight on the correct MCQ option; not in the text layer, read from page images by the book helper) — v0.2 assumed no key. The mark is the book's answer, verified against the chapter text; a contradiction goes on `book_says` (so far only Q05-020, C5-19: book tick «خطأ», text supports «صح»). Asem's 113 in-scope worked answers equal the book's marks (0 disagreements in ch 1/2/3/5: 15+18+14+14 compared).
- OQ1–OQ5 (older curriculum, د. سليمان عوض) → type "other", in-book concepts only, keys never imported (CLAUDE.md rule). The older textbook with annotated exam questions (`MIS_محدد عليه اسئلة الدورات.pdf`, src01) stays excluded: its 52 question notes are answered by the old book's own text; 30 candidates are in `extracted/questions/others_b.json` (code OQ6-CANDIDATE), unused. The 7 MISS photos are pixel-identical to the 7 images embedded in `اسئلة سابقة/دورات.pdf`.
- Three book T/F items on intranets asked in the chapter-7 review set are recorded in chapter 2 (unit 2-6, legacy C7-17/18/19 taken over by `bank_ch02.py`); the chapter-7 helper must DROP them and report "moved to ch2". Other chapter-7 review items (business model, e-business infrastructure) stay in chapter 7 under its units.
- Book review questions may cite pages outside their chapter (e.g. ch-1 review questions answered in ch-2 text): `build_bank.py` prints them as a warning, does not fail.
- Exam items about chapters 4, 6, 11 (about 31) are out of scope → `qa/summary.json → unresolved` (already written in Arabic).
- Legacy generated questions are kept when their unit is still uncovered by real questions; new generation follows the DECIDE default (focus-area units + ≤3 new per chapter). Chapter 1 helper dropped G1-01 (unit 1-1-2) judging an essay answer covers it, but `build_bank.py` counts coverage by the `sub` field, so **1-1-2 shows as uncovered** — fix at the end: reinstate G1-01 as a generated MCQ in `bank_ch01.py` (unit 1-1-2, p. 13–15, legacy record in `extracted/legacy/ch01.json`), or accept 104/105 and say so.
- Types derive from sources in `build_bank.py`; ASM is never a type. `exam_sources` ⊆ {S25, R44, F24}.
- DECIDE defaults applied: no pilot; generated-question volume per §0c; HTML only.
- `qa/summary.json` holds `images` (137), `asem` (filled 2026-09-24: 113 of 113 ASM answers equal the book marks — ch 1/2/3/5/7/8/9/10: 15/18/14/14/11/13/14/14; Q05-020 is the one item where the chapter text overrides both) and `unresolved` (Arabic list) — the renderer reads it.

- **Consolidation (2026-09-24, prompt idea I-11, owner decision):** after the eight helpers, one pass over the whole bank; only true duplicates (same claim, same answer, same form) merged, keeping the exam item in the chapter that owns the page: Q07-013 → Q01-002 (business model, p. 20), Q10-020 → Q05-024 (data warehouse is not the small store, pp. 206–207), Q09-011 → Q01-013 (organizational and management capital, pp. 35, 341), Q03-020 → Q01-009 (organizational culture, p. 29). A reconstructed exam MCQ built from a recall «تعريف X» counts as the same form as a book definition MCQ asked the other way (the recall fixes no direction). Merges live in `build_bank.py` `MERGES` (sources, pages, legacy and raw ids unioned, the dropped wording as a variant, flags from both, freq = size of the source union). No answer conflict found. Same-fact-other-form pairs stay separate (list in `qa/consolidation_v1.0.md`).
- Build checks (`check_duplicates` in `build_bank.py`): hard failure for the same option set + stem cosine ≥ 0.6 + different answer (Q10-001 / Q10-002, structured vs unstructured definitions, allow-listed in `DUP_ALLOW`), and for a raw source-item id used by two records (`raw=[...]` in `common.Q`, `id@n` for sub-questions); warning list of cross-chapter neighbours above the union threshold.
- G1-01 reinstated as generated MCQ Q01-035 (unit 1-1-2, p. 13) so the audit counts 105/105.
- Q03-004 / Q03-005 carry `legacy_id` C1-15 / C1-17 (the same R44/F24 items, moved from chapter 1 to chapter 3 by the chapter-1 helper), so the change report shows them as reworded, not new.
- Spec recorded as v0.11: the renderer and checks are v0.11; v0.11 only added §7d, which no MIS record needs. `SYMBOLS` is empty and the page ships no symbol sheet.
- The reference line prints consecutive page runs in record order («ص 23–27، 30–31، 41»), the PDF numbers equal to the printed ones (fixed during the browser test; before it printed «PDF first–last»).

## 4. Known problems and open questions
- No record declares raw source-item ids yet (`raw`); the check is in place and prints "233 real records do not yet". Filling them needs a pass over `extracted/questions/by_chapter/*.json` per record.
- `freq` counts every source code in the union, ASM included, although ASM is a cross-check copy of the book set (so a BOOK+ASM item shows «2 مصادر مستقلة»). Inherited from the PRM tooling. **Owner decision 2026-09-24: keep counting it** (a popular student summary is itself a signal of what students study); same in PRM and IMT.
- Accepted `qa_blocks.py` hits: 3 blocks over 80 words (Q03-030 89, Q05-033 87, Q07-021 81); 22 T/F blocks under 40 words (no distractors by design); 22 "why repeats the answer text" hits (heuristic, read, acceptable).
- Out-of-chapter page warnings (expected: book review items answered on another chapter's pages, plus merged records): Q01-002, Q01-009, Q01-013, Q01-021…024, Q03-004, 005, 017, 018, 019, 022, Q07-008, Q07-012, Q10-007, Q10-021, Q10-028.
- Not tested: a real phone/touch device, print layout, Safari/Firefox (`qa/browser_test_v1.0.md`).

## 5. To continue
The v1.0 run is complete. Next steps (owner):
1. Repository root: `python scripts/build_course_index.py` (together with the other courses), then commit the MIS paths (`courses/S3/MIS/`, `S3/MIS/index.html`) and `courses.json`.
2. `raw=[...]` ids: owner decision 2026-09-24 — not filled now; fill them only for records touched later (future runs get them from the start, prompt idea I-11).
3. New sources or fixes: MINOR releases (v1.1 …) with the loop in `../README.md`.
4. **Next MIS pass (v1.1): apply the review** `qa/review_v0.2_vs_v1.0.md` (2026-09-24, not applied yet) — its top 5: reinstate the lost topics (10-3-6, Select/Project/Join, six organisational factors) and make coverage require a section's own content; restore book review items as their own cards and undo the merges Q01-013←Q09-011, Q01-009←Q03-020; fix citations Q01-016, Q03-024; clean recall-shaped MCQs Q03-003, Q01-031, Q05-001 and drop six unneeded low-confidence flags; expandable full model answers for the 24 essays. Estimated one Opus agent, ~200–300k tokens.
