# Brief for a chapter helper (stages 5–9 for ONE chapter)

You build the verified question bank for book chapter **N** of the Arabic MBA course
«إدارة المشاريع – Project Management» (د. إياد زوكار, 554 pages, printed page = PDF page).
Work only inside W = C:\Users\root\SVU-MBA-Course-Review\courses\S3\PRM\.review_generation_working_directory
Set PYTHONUTF8=1 for python. Output: `W\render\bank_chNN.py` (+ a short `W\qa\chNN_report.md`).

## Inputs
- Chapter text: `W\extracted\book\ch_fixed\chNN.txt` (page markers `=== PAGE n ===`). This is the ONLY authority.
  The text was extracted from the PDF; a few lam-alef ligatures may still be reversed («األ» = «الأ», «اال» = «الا»,
  «اإل» = «الإ») and lines are broken oddly. If a passage is unclear, render the page to PNG and read it with the
  Read tool: in python, `pymupdf.open(BOOK_PDF)[n-1].get_pixmap(dpi=110).save(W + "/extracted/pages_png/book_pNNN.png")`
  where BOOK_PDF = `C:\Users\root\SVU-MBA-Course-Review\courses\S3\PRM\الماده الاكاديميه\MBA - Project Management - The Book.pdf`.
- Subsections of the chapter (the audit unit, §9): `W\extracted\book\subsections.json` → key "N". Use the
  second-level codes ("N-M") as `sub`; the third-level topics listed there tell you what each covers.
- Raw questions assigned to this chapter: `W\extracted\questions\by_chapter\chNN.json` — items transcribed
  from the book review section (src BOOK), exam recollections and other sources, each with `src`, `code`
  (independent-source code), `stem`, `options`, `marked_answer`, `notes`. Treat marked answers as claims to
  verify, never as truth.
- Data model: `W\render\common.py` (`Q(...)`); example of finished records: `W\render\EXAMPLE_RECORD.py`.
- Source codes and what they mean: `W\render\SOURCES.md`.

## What to produce — one `Q(...)` per canonical question
1. **Deduplicate** the raw items: the same question from several sources becomes ONE record whose `sources`
   lists every independent source code containing it (a source counts once even if the question repeats inside
   it) and whose `exam_sources` lists the exam sittings among them. Keep the other wordings in `variants`
   (prefix each with the source code). `types` = every kind that applies: "exam" if any exam sitting has it,
   "textbook" if the book review section has it, "other" if a summary/other source has it. A record may carry
   several types.
2. **Verify every answer from the chapter text** and cite the page(s) you actually read (`pages`). Never cite a
   page you did not check. If the book's review question is ambiguous, answer from the chapter text and
   explain. If a source's marked answer contradicts the book, the book wins: put the source's answer on
   `other_source="<code>: <their answer>"`.
3. **Exam items in free form** (a recalled sentence, "تعريف X", "كل مما يلي … ما عدا") → present as MCQ with the
   recalled wording as stem, the book's answer as the correct option and 3 distractors that are REAL terms from
   this chapter (never invented); set `reconstructed=True` and `original="<the recalled text verbatim>"`.
   If the source already has options keep them exactly. Never convert essay / list / process questions;
   keep them as `qtype="short"` or `"essay"` with the answer as text. Items that only name a topic
   (`qtype: topic`) with no recoverable question: do NOT create a record; list them in the report as
   "topic only" with the subsection they point to.
4. **Calculation items** (critical path, EVA, three-point estimate, NPV/payback, resource levelling): solve them
   with the book's method, show the working briefly in `why` (numbers), and cite the book page of the method.
   Put the full data table in the stem so the question is self-contained.
5. **Answer block** (§7): `why` ≤ 2 sentences (3 for reconstructed) naming the deciding concept, never starting
   with «الإجابة الصحيحة»; `remember` = 2–5 **bold** keywords; `distractors` only for confusable options, one
   clause each («ب — ذلك هو **X** لا Y»); whole block 40–80 words. Bold (**…**) ONLY in why/remember/distractors,
   never in stem/options. No filler. Everything in Arabic (English terms allowed inline).
6. **Low confidence** (`low_conf="<one clause>"`) ONLY when: the book supports the answer with a passing
   sentence; sources disagree and the book does not settle it; the wording is a memory recall that could mean
   two things; or the item's concept is absent from this book (then also `book_says`/`other_source` as fits).
   Otherwise leave `low_conf=None`.
7. **Coverage** (§9): after the real questions, list which subsections of the chapter have NO question whose
   text/options/answer covers them. For each uncovered subsection write ONE generated MCQ from the book's
   wording (`types=["generated"]`, `sources=["GEN"]`, `exam_sources=[]`, verified page), preferring subsections
   that are focus areas (most exam questions). Limit: at most 3 generated questions for non-focus subsections
   (DECIDE-mode default), and never more generated than real questions in the chapter. A subsection that is a
   mere «مقدمة» previewing the chapter still gets one generated question on its one concrete statement if
   nothing else covers it. Do not generate a question whose idea an existing question already tests.
8. **Ids**: `QNN-001`, `QNN-002` … in the order exam → textbook → other → generated. `ch=N`, `sub="N-M"`.
9. **Chapter opener** for §11a: put at the top of the file `OPENER = ("<one sentence: what the chapter is about>",
   "**term1**، **term2**، … (3–6 bold terms the questions keep returning to)")`, and `SUBS = {"N-M": "<short Arabic name>", …}`
   for EVERY subsection of the chapter (short names, ≤ 8 words, Arabic).
10. Run `python -c "import bank_chNN"` from `W\render` to make sure the file imports (the Q() asserts pass).

## Report (`W\qa\chNN_report.md`, short)
Counts: raw items received / canonical records / by type / reconstructed / low-confidence / generated;
subsections covered by real questions, by generated, uncovered (with reason); unresolved items (could not be
assigned or verified) with their raw ids; every disagreement between a source's marked answer and the book;
pages you read visually.
