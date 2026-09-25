# STATE — ACM review (handoff file, §0d)

Read this whole file before touching the course; section 5 says what to do next.

## 1. Settings in force
- Spec **v0.12**, interaction mode **DECIDE**, pilot NONE, Arabic interface / questions / explanations. Settings table: `../PROJECT_SETTINGS.md`.
- **Scope = the F25 sitting only** (exam 2026-09-26; owner decision 2026-09-25 from `../Exams/المطلوب بدوره F25 بالامتحان.txt`): chapters 1, 2, 3, 10 in full; chapter 7 in full without journal entries (owner confirmed the original group message on 2026-09-25; the scope file's «الاهتلاك فقط» is a superseded paraphrase); chapters 8, 9 theory only (9 up to p. 302). Chapters 4, 5, 6 out. Stated on the page cover (`meta_acm.SCOPE_BANNER`), in the scope section and in the openers of chapters 7, 8, 9.
- Primary reference: `../Course/كتاب المحاسبة للمديرين.pdf` (447 pages, printed page = PDF page, 0 mismatches; the review answers are marked on the pages: a tick in the صح/خطأ column, a green highlight on the MCQ option).
- Audit unit (§9): the finest TOC level inside the scope — 81 units (`extracted/book/subsections.json`, with page ranges and the excluded parts). Similar-stem threshold (§5b): 0.6.
- Deliverable version: **v1.0** (`VERSION`), scheme `vMAJOR.MINOR` (`VERSIONING.md` at the repository root). PDF/DOCX: NEVER.
- Last update: 2026-09-25 — **v1.0 released and published** (`/S2/ACM/index.html`); all stages done.

## 2. Stage checklist
| Stage | Status | Produced |
|---|---|---|
| 0 Working directory | done — PRM/MIS `render/` tooling copied and rewritten for v0.12: `common.py` (claim, model_answer, fast, see, fig, unsolved, also, C.method, F, M), `meta_acm.py` (scope, titles, codes, SYMBOLS with examples, FILES 37 rows), `build_bank.py` (see-groups, own-content coverage, fig recompute, METHODS checks, neighbours file), `render_html.py` (scope banner, Methods block, step reveal, model answers, fast route, cross-links, Essentials, cvp SVG), `qa_blocks.py`, `release.py`, `hash_files.py`, `split_by_chapter.py`; briefs `CHAPTER_HELPER_BRIEF.md`, `CALC_TABLE_BRIEF.md`, `EXAMPLE_RECORD.py`, `SOURCES.md` | this layout |
| 1 Read reference, verify extraction | done — `scripts/pdf_text/extract_pdf.py` (geometric lam-alef fix; 12 pages flagged = title/table pages), page numbers verified for all 447 pages, chapter boundaries from title pages (12/41/84/111/134/159/188/242/290/325/358/389) | `extracted/book/pNNN.txt`, `book.txt`, `ch/chNN.txt` (all 12), `subsections.json` |
| 2 Curriculum check, 2a chapter map | done — one curriculum (د. باسل أسعد 2021); the two question PDFs are page copies of the book (text match page by page); lecture decks 7–8 → ch 7, 10–11 → ch 9, 12 → ch 10 | `chapter_map.md/.json` |
| 3 Extract questions | done — book (`book.json`), others (`summary.json` 104 items, `solved345.json`), exams A and B (`exams_a.json`, `exams_b.json`) with their reports; split by `render/split_by_chapter.py` into `by_chapter/` | `extracted/questions/*.json` + `*_report.md`, `by_chapter/` |
| 4 Source ledger with hashes | done — 37 files, no duplicate hashes; 9 independent sources: BOOK, S23, F23, S24, F24, S25, OLD (older/unattributed sittings = one), SUM (cross-check), SOL345 (other); context: SCOPE, ABOUT, SLIDES | `extracted/hashes.json`, `ledger.json`, `render/SOURCES.md`, `render/meta_acm.py` FILES |
| 5–9 per chapter | done — seven helpers (opus) with `render/CHAPTER_HELPER_BRIEF.md`; 209 records as delivered; owner decisions applied afterwards (see §3) | `render/bank_chNN.py`, `qa/chNN_report.md` |
| 5b Consolidation | done — 1 fold (Q02-009 → Q08-014), 2 new see-links (Q03-014↔Q08-009, Q02-005↔Q03-015), 13 candidates rejected, three hard checks negative-tested | `qa/consolidation_v1.0.md`, `qa/neighbours_v1.0.txt` |
| 10 Focus areas + importance | done (build_bank.py; linked cards now share the focus bonus) — 24 focus units | `coverage.md`, `bank.json` |
| 11–13 Render, bank checkpoint | done — `release.py`: 209 questions, 81 units, uncovered 0 | `bank.json`, `out.html`, `../مراجعه كامله لماده ال ACM_v1.0.html` |
| 14 Privacy note | done (in the renderer) | |
| 15 QA | done — `qa_blocks.py` clean except the justified lists below; 20-block sample read; browser test desktop + 390 px (iframe) | `qa/qa_blocks_v1.0.txt`, `qa/browser_test_v1.0.md`, `qa/summary.json` |
| 16 Docs / publish | done — `scripts/publish_page.py S2/ACM`, `scripts/build_course_index.py`, home-page fallback card, `../README.md`, `HANDOFF.md` | `/S2/ACM/index.html`, `courses.json` |

## 3. Decisions not obvious from the files
- Telegram export (`../telegram/`, raw messages of the two course groups, made by an earlier session): used for context; every recall, answer discussion, scope statement and reported book error missing from the resources was folded into `../Exams/<sitting> - تلغرام.txt` (verbatim, anonymised) and `../Exams/عام - تلغرام.txt`, the two errata images copied to `../Exams/`; the folder was gitignored and deleted (2026-09-25). It reappeared once a minute later (another session's export still writing) and was deleted again.
- Folder reorganised before hashing: `Course/` (book, its two question copies, lecture decks, the scanned solutions), `Exams/` (all sittings, scope, advice, errata), `Summaries/` (Asem).
- OLD = one exam source for sittings before S23 (WhatsApp forwards, one dated 2021-11-17) and unattributed recalls; the block «الفصل العاشر جاب منو 9 أسئلة…» of the Kuwait F23 file belongs to OLD (first posted Oct 2023).
- The S24 answer key circulated in the group (#41646) is AI-written and disputed by students: never used as a key (students' corrections for Q5, Q9 are in the exams report; the book decides).
- The book marks its review answers (tick / green highlight); each mark is the book's answer verified against the text, contradictions on `book_says` (Q08-021, Q02-020, Q01-001). ملخص عاصم reproduces the book's T/F items with a key → agreement rate reported in the methodology (§8), SUM never a type.
- Number-less recalls («جاء سؤال عن القسط المتناقص») are credits on the existing records of the same problem type and format (§5c, `~raw_id`).
- Book errors students reported (p. 59 sources/uses of funds; p. 134 closing entry — chapter 5, out of scope; disputed T/F keys on inventory; numeric slips 50,000 vs 100,000) are to be checked by the chapter helpers: book text on `book_says`, answer from the correct rule.
- DECIDE defaults: no pilot; generated questions per §0c (one per unit mentioned but never asked, up to three per chapter for units not covered at all; chapter 7 has 7, all kept by the owner; 20 generated in all, never more than the real ones in a chapter); HTML only.
- Owner decisions applied at the owner stage (2026-09-25): (1) the seven exam chart records Q10-001…007 carry `fig=F(..., hide_labels=True)`: the figure shows «الخط 1…5», «النقطة أ/ب», axes «ع/س», no names or values, a neutral alt text; the answer block prints «مفتاح الشكل: …» under ✔, and their recalled text moved behind the answer (it names the line). Line order: 1 revenue, 2 total cost, 3 fixed, 4 cash fixed, 5 total cash cost; أ shutdown, ب break-even. Solution figures (Q10-012, 021, 029, 032, 033, 037) render inside the answer block because their labels print the answer. (2) The book marks its review answers (tick / green highlight); fixed in meta_acm, ledger.json, SOURCES.md, PROJECT_SETTINGS.md, README. (3) Q01-001 kept (mark + book_says + low_conf); exams_a#105 → Q01-008; exams_b#37 → new Q10-046 (S24, low_conf); Q02-004 kept with a low_conf clause; Q08-005/007 and the chart records lead with «البيانات من مثال الكتاب…» and carry each sitting as a variant «نُقل نوع المسألة دون بياناتها»; ch 7 keeps its 7 generated, Q07-023, Q07-012; the F23 activity-method credit stays unapplied (listed as unresolved); Q10-026 keeps book T/F 1 + 4 as one card.
- qa_blocks «synonym-looking option pairs» on Q02-013, Q10-003…006, 008, 009, 011, 017, 018: journal-entry options, chart-line names and formula/definition options that share words by nature; each read once, kept.
- §8: the Asem T/F key agrees with the bank on 34 of 35 book items (disagreement: p. 81 T/F 3, Q02-020, where the summary follows the book's tick and the bank corrects it from pp. 60–61).

## 4. Known problems and open questions
- The other session's Telegram media export may re-create `../telegram/` (gitignored); delete it if it reappears.
- The extraction's thousands groups are reversed and spaced in the text layer; amounts were read from page images. Formula lines with fractions are garbled in the text layer.
- Generic renderer issue (not changed): on reconstructed records whose recalled text contains the recalled answer, «نص الطالب الأصلي» under the stem shows it before the reveal (fixed only for the 7 hidden-label charts). Candidate for v1.1: move the original line into the answer block for every record.
- Q10-046 is numbered after the generated Q10-045 (ids of existing records were not renumbered).
- Not tested: real touch input on a phone (the 390 px test used an iframe), print.
- 16 low-confidence records: Q01-001, Q01-005, Q01-007, Q02-004, Q02-020, Q02-030, Q02-037, Q07-004, Q07-008, Q07-010, Q07-016, Q08-006, Q09-003, Q10-012, Q10-018, Q10-046.

## 5. To continue
v1.0 is published. For a correction: edit `render/bank_chNN.py` (book page for every answer change), bump `VERSION` to 1.1, add a `VERSIONS.md` row, `cd render && set PYTHONUTF8=1 && python release.py && python qa_blocks.py`, then at the repository root `python scripts/publish_page.py S2/ACM` and `python scripts/build_course_index.py`; update this file, `../README.md` and `HANDOFF.md`. Open candidates for v1.1 are in §4 and in `HANDOFF.md`. After the F25 sitting (2026-09-26), fold its recalls in as a new source `F25` (see `../README.md`, "Add a new exam sitting").
