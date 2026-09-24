# Brief for a chapter helper (stages 5–9 for ONE chapter) — MIS review v1.0, prompt v0.10

You build the verified question bank for book chapter **N** of the Arabic MBA course
«نظم المعلومات الإدارية – MIS» (د. إياد زوكار, 507 pages, printed page = PDF page).
Work only inside W = C:\Users\root\SVU-MBA-Course-Review\courses\S3\MIS\.review_generation_working_directory
Set PYTHONUTF8=1 for python. Output: `W\render\bank_chNN.py` (+ a short `W\qa\chNN_report.md`).
Never modify a source file. No personal data (no student names anywhere).

## Inputs
- Chapter text: `W\extracted\book\ch_fixed\chNN.txt` (page markers `=== PAGE n ===`). This is the ONLY authority.
  Lines are broken oddly by the PDF font and a few letters are split («ت لم عد» = «لم تعد»); read around it. If a
  passage is unclear, render the page and read it with the Read tool: in python,
  `import pymupdf; pymupdf.open(BOOK)[n-1].get_pixmap(dpi=100).save(W + "/extracted/pages_png/book_pNNN.png")`
  with BOOK = `C:\Users\root\SVU-MBA-Course-Review\courses\S3\MIS\Dr Iyad Zoukar - MBA - MIS - The Book.pdf`.
- Audit units of the chapter (§9): `W\extracted\book\subsections.json` → "units" → key "N". Use their codes
  ("N-M-K", or "N-M" where the section has no sub-headings) as `sub`.
- **Legacy records** (the verified v0.2 bank, your main input): `W\extracted\legacy\chNN.json`. Each has
  `legacy_id`, `types`, `qtype`, `sources` (already renamed: HD→R44, BKQ→BOOK), `page`, `stem`, `options`,
  `ans` (text), `exp` (the old explanation), `other_source_old`. They were verified against the book on 2026-09-06,
  but you must RE-CHECK every page number and answer against the chapter text now — do not trust blindly, and do
  not discard verified content without a reason you write down.
- **Raw items re-transcribed from every source** for this chapter: `W\extracted\questions\by_chapter\chNN.json`
  (fields per `W\extracted\FORMAT.md`: `code` = source code, `stem`, `options`, `marked_answer`, `marked_by`,
  `qtype`, `in_book`, `sub_guess`, `notes`). Marked answers are CLAIMS to verify, never truth. For `code` BOOK the mark (tick / yellow highlight, `marked_by` key or highlight) is the book's own printed answer: verify it against the chapter text; if the text contradicts it, answer from the text and put the mark on `book_says="علامة الكتاب: …"` (keep it visible, §1). Items with
  `code` in OQ1…OQ5 come from an older curriculum: keep only those whose concept the chapter text actually
  treats; verify from the book, never import their key.
- Data model: `W\render\common.py` (`Q(...)`); finished example: `W\render\EXAMPLE_RECORD.py`.
- Source codes: `W\render\SOURCES.md`. `exam_sources` ⊆ {S25, R44, F24}.

## What to produce — one `Q(...)` per canonical question
1. **Reconcile legacy and raw.** Start from the legacy records. For each, find the raw items that are the same
   question (across sources) and merge: `sources` = every independent code that has it (BOOK, S25, R44, F24, ASM,
   OQ1…OQ5), `exam_sources` = the exam codes among them, other wordings in `variants` (prefixed with the code).
   Raw items with no legacy record become NEW records. Legacy records the sources no longer support (nothing in
   the raw items and nothing in the book) are dropped — list every drop with its id and the reason in the report.
   Two legacy records testing the same idea are merged (say which ids). `legacy_id` = the old id, or
   "C2-03+O2-01" when merged; None for new records. NEVER output two records for the same idea.
2. **Verify every answer from the chapter text** and cite the page(s) you actually read (`pages`, ints within the
   chapter). If the book does not settle a question, say so in `low_conf`. If a source's marked answer (ASM key,
   student recall, older key) contradicts the book, the book wins: `other_source="<code>: <their answer>"`.
   Legacy `other_source_old` values carry over to `other_source` if still true.
3. **Exam items in free form** (a recalled sentence, «تعريف X», a description with the answer in parentheses):
   present as MCQ with the recalled wording as stem, the book's answer as the correct option and 3 distractors that
   are REAL terms from this chapter (never invented), `reconstructed=True`, `original="<the recalled text verbatim>"`.
   Many legacy exam records already did this without the flag: set `reconstructed=True` and put the source's
   recalled text (from the raw item) in `original`. If the source already has options keep them exactly. Never
   convert essay / list / process questions; keep them `qtype="short"` or `"essay"` with the answer as text.
   Book questions and OQ items keep their original format. Items that only name a topic (`qtype: topic`):
   no record; list them in the report as "topic only" with the unit they point to.
4b. **Tables and calculations (§7d)** — any item whose stem carries tabular data or whose answer is a number:
   put the data in `table=T(head, rows)` (the stem keeps only the question sentence), the full working in
   `ans_table=T(...)` when there is one, and the steps in `calc=C(given=[...], steps=[S(what, eq, sub, res)])`;
   `why` then names the rule only. Exact rules and finished examples: `CALC_TABLE_BRIEF.md` in this folder.
4. **Answer block** (§7a/§7b): `why` ≤ 2 sentences (3 for reconstructed) naming the deciding concept, never
   starting with «الإجابة الصحيحة» and never repeating the answer text; `remember` = 2–5 **bold** keywords or a
   short hook; `distractors` only for confusable options, one clause each («ب — ذلك هو **TPS** لا MIS»), omit for
   T/F and short answers unless a near-miss term exists; whole block 40–80 words. The old `exp` is a paragraph:
   condense it into `why`, do not paste it. Bold ONLY in why/remember/distractors, never in stem/options.
   No filler. Arabic (English terms inline as the book writes them).
5. **Low confidence** (`low_conf="<one clause>"`) ONLY when: the book supports the answer with a passing sentence;
   sources disagree and the book does not settle it; the wording is a memory recall that could mean two things;
   or the concept is only marginally in this book. Otherwise `low_conf=None`.
6. **Coverage** (§9): after the real questions, list the units with NO question whose text/options/answer covers
   them. Legacy generated questions (`types` contains "generated") stay if their unit is still uncovered by real
   questions (re-verify page and answer; rewrite the block); drop them if a real question now covers the unit
   (report). For remaining uncovered units write ONE generated MCQ each from the book's wording
   (`types=["generated"]`, `sources=["GEN"]`, `exam_sources=[]`, verified page): all units that are focus areas
   (the units with the most exam questions in your chapter), plus at most 3 NEW ones for other units (DECIDE
   default); never more generated than real questions. Do not generate a question whose idea an existing one tests.
7. **Ids**: `QNN-001`, `QNN-002` … in the order exam → textbook → other → generated. `ch=N`, `sub="<unit code>"`.
8. **Chapter opener** (§11a) at the top of the file: `OPENER = ("<one sentence: what the chapter is about>",
   "**term1**، **term2**، … (3–6 bold terms the exam questions keep returning to)")`, and
   `SUBS = {"<unit code>": "<short Arabic name ≤ 8 words>", …}` for EVERY unit of the chapter.
9. Run `python -c "import bank_chNN"` from `W\render` (the Q() asserts must pass).

## Report (`W\qa\chNN_report.md`, short, in English)
Counts: legacy records received / raw items received / canonical records / by type / reconstructed / low-confidence /
generated (kept from legacy, new). Legacy mapping: kept as is, reworded, merged (ids), split, dropped (ids + reason).
New questions found in the sources (ids, source). Page or answer corrections to legacy records (id: old → new, evidence).
Units covered by real questions / by generated / uncovered (with reason). Topic-only items. OQ items rejected as not in
the book (count + a few examples). ASM disagreements with the book. Pages read visually.
