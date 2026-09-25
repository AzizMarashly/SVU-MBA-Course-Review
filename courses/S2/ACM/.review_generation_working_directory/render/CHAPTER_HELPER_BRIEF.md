# Brief for a chapter helper (stages 5–9 for ONE chapter) — ACM review v1.0, prompt v0.12

You build the verified question bank for book chapter **N** of the Arabic MBA course «المحاسبة للمديرين — Accounting for
Managers» (د. باسل أسعد, 2021, 447 pages, printed page = PDF page). Work only inside
W = `C:\Users\root\SVU-MBA-Course-Review\courses\S2\ACM\.review_generation_working_directory`. Set `PYTHONUTF8=1` for python.
Output: `W\render\bank_chNN.py` (+ a short `W\qa\chNN_report.md`). Everything in Arabic (English terms inline are fine).

## Scope of this run — F25 only
The review covers what the students report as required for the F25 sitting (2026-09-26): chapters 1, 2, 3, 10 in full; **chapter 7 in full
except everything that is a journal entry** (concepts and calculations of adjustments, doubtful debts, cash and bank reconciliation, inventory
count and pricing, depreciation are in; the entry units 7-4-3 and 7-5-6 and the entries inside other units are out); chapters 8 and 9 theory
only (9 up to the definition of the cost accounting system, p. 302). `W\extracted\book\subsections.json` lists the units of your chapter
(`units` → your chapter number) and the `excluded` parts. **Every record's `sub` must be one of your chapter's units.** A raw item whose content
is outside the scope (cost-accounting theories in chapter 9, a full statement preparation in chapter 8) makes no record: list it in the report
under «out of F25 scope» with its raw id. **Chapter 7 helper:** the transcriptions were made under an older reading of the scope
("depreciation only"), so ignore their `in_scope` flag and apply this rule instead — keep an item if the concept or the amount is the point
(the adjustment amount, the allowance, the shortage split, the cash-count difference, which items are added to the bank balance, the depreciation
charge or accumulated depreciation) even when the source wraps it as an entry — present it as the amount/concept and say so in `notes`; drop it
only when the question is solely which account is debited or credited. Older sittings had removed FIFO/LIFO/weighted average and the perpetual
inventory; the F25 message does not, so they stay in as theory plus one worked example each.

## Inputs
- Chapter text: `W\extracted\book\ch\chNN.txt` (page markers `=== PAGE n ===`). This is the ONLY authority for answers and pages.
  The extraction is clean on prose, but **thousands groups come out reversed and spaced** (`000  ،  500  ،1` on the page = 1,500,000) and
  **fractions and multi-column tables are garbled**. For any formula, worked example or table, render the page and read the image:
  `python -c "import pymupdf;d=pymupdf.open(r'C:\Users\root\SVU-MBA-Course-Review\courses\S2\ACM\Course\كتاب المحاسبة للمديرين.pdf');d[N-1].get_pixmap(dpi=110).save(r'W\extracted\pages_png\book_pNNN.png')"`
  then the Read tool. Count the pages you looked at.
- Units of the chapter (audit unit, §9) with page ranges: `W\extracted\book\subsections.json`. Use the unit codes as `sub` (chapter-first,
  e.g. `10-2-3-3`).
- Raw questions assigned to this chapter: `W\extracted\questions\by_chapter\chNN.json` — items transcribed from the book review section
  and cases (code BOOK), exam recollections (codes S23 F23 S24 F24 S25 OLD), the summary (SUM), the student solutions (SOL345); each with
  `src`, `code`, `raw_id`, `stem`, `options`, `marked_answer`, `marked_by`, `in_scope`, `numberless`, `unsolved`, `notes`. Treat marked answers as
  claims to verify, never as truth. Student-recalled answers and the AI-written S24 key (see the exams reports) are often wrong.
- Data model: `W\render\common.py` (`Q`, `T`, `C`, `S`, `F`, `M`); finished examples: `W\render\EXAMPLE_RECORD.py`; rules for tables and
  calculations: `W\render\CALC_TABLE_BRIEF.md`; source codes: `W\render\SOURCES.md`; symbols glossary: `SYMBOLS` in `W\render\meta_acm.py`.
- Cross-check material: the summary text `W\extracted\summary\pNNN.txt` (definitions), the exams reports `W\extracted\questions\exams_*_report.md`
  (disputed answers, book errors students reported, exam format).

## What to produce — one `Q(...)` per canonical question
1. **Claim line.** Every record carries `claim="…"`: one line naming the book fact whose knowledge decides the answer, phrased so that a
   true/false item and its negation, or a definition and its reverse, carry the same claim (the fact, not the letter).
2. **Deduplicate by claim (§5a).** Same claim, same wording → ONE record: `sources` lists every independent source code containing it
   (a source counts once even if the question repeats inside it), other wordings in `variants` (prefix each with the source code), `raw` lists
   every raw id it was built from (`raw_id` values; `id@1`, `id@2` when one raw item feeds several records; a leading `~` for a number-less
   credit). **Protected cards:** a book review item and an exam item recorded with its original wording and options each keep their own card;
   link them with `see=["Q10-007"]` on both (symmetric) — they then share frequency and importance (the build unions their sources). Every
   other repeat of the claim (a paraphrased recall, a reconstructed item, a summary rewording) is folded into the kept card: same form → a
   variant; different form (MCQ vs true/false vs short) → an `also=[("صح / خطأ", "wording", "key", ["S24"])]` line. Never merge two
   records whose answers differ; report the conflict.
3. **Frequency evidence without numbers (§5c).** A raw item with `numberless: true` («جاء سؤال عن القسط المتناقص») creates no record: add
   its sitting code to `sources`/`exam_sources` of every existing record of the same problem type **and the same format** in this chapter,
   add `~raw_id` to their `raw`, and a variant «S25: نُقل نوع المسألة دون بياناتها». Topic-only items make no record; list them in the report.
4. **Verify every answer from the chapter text** and cite the page(s) you actually read (`pages`), the page that states the fact first.
   If a source's marked answer contradicts the book, the book wins: `other_source="S24 (حل الطلاب): …"`. If the book's own printed solution
   or statement is wrong (students reported errors, e.g. p. 59 sources/uses of funds, p. 134 closing entry; check them), answer from the
   correct rule and put the book's text on `book_says`, with `sci` only if it is a matter of accounting science, and `low_conf` per §7c.
5. **Exam items in free form** («تعريف X», «جاء سؤال عن Y والجواب Z») → present as MCQ: recalled wording as stem, the book's answer as the
   correct option, three distractors that are REAL terms of the same or an adjacent unit (never invented, no synonym pairs), **exactly four
   options**; `reconstructed=True`, `original="<recalled text verbatim>"`. When the book's review set has an item on the same claim,
   reconstruct in the book's form (its stem direction and option set) and say so in `notes`. If the source already has options, keep them
   exactly (also «كل ما سبق صحيح/خاطئ»). Never convert essay / list / process questions (`qtype="short"` or `"essay"`).
6. **Essays and lists (§7b):** `ans` = the key points (≤ 40 words); `model_answer` = the full model answer from the book's own content, 100–200
   words, bold keywords, the page of each point inline «(ص 25)». Required for every `qtype="essay"`.
7. **Calculations (§7d, §7e).** Any item whose stem carries data or whose answer is a number: `table=T(...)` for tabular data (the stem keeps
   the question sentence only; no `|` in stems), `calc=C(given=[...], steps=[S(what, eq, sub, res)], method="M1")` with every number's
   origin, `ans_table=T(...)` for a full working shared by sibling questions. Symbols in `eq`/`sub` are Latin only and must exist in `SYMBOLS`
   (add missing ones to `meta_acm.py` with ar/en/f/note/ex — coordinate: add only, never rename). Recompute every number in python.
   - **Methods block (§7e):** if two or more records of the chapter share a solving method, define at the top of the file
     `METHODS = [M("M1", "نقطة التعادل بالكمية والقيمة", "المعطى: سعر البيع والتكلفة المتغيرة للوحدة والتكاليف الثابتة؛ المطلوب: كمية أو قيمة التعادل",
     [("هامش المساهمة للوحدة CM = P − V", "CM"), ("نقطة التعادل بالكمية BEQ = FC ÷ CM", "BEQ"), …], 338, fast="…")]` — one entry per problem
     type, steps in the order the book teaches (cite the page), and every calc of that type uses `method="M1"` and the same step order.
   - **Fast route:** `fast="…"` only where a rule of the book decides the item without the full calculation (which line is the fixed-cost line,
     the sign of a change, accumulated depreciation after the last year = cost − salvage), with the page; add «(مستنتج)» if the book does not
     state it in those words. Never invent a shortcut.
   - **Figures:** chapter 10 break-even / shutdown chart questions get `fig=F("cvp", price=…, var=…, fixed=…, be_q=…, cash_fixed=…, sales_q=…,
     highlight="be"|"shutdown"|"safety"|"lines", alt="…")` from the record's own data (the build recomputes be_q and fails on a mismatch).
     A chart recalled without numbers uses the book's example data (p. 339–345) and says so in `notes` and in the stem lead-in.
   - **Unsolved book exercises:** solve each with the chapter's method as a textbook record with `unsolved=True` (`sources=["BOOK"]`),
     full calc block, a page for every rule used.
8. **Answer block (§7):** `why` ≤ 2 sentences (3 for reconstructed) naming the deciding concept, never starting with «الإجابة الصحيحة»
   and not repeating the answer text; `remember` = 2–5 **bold** keywords; `distractors` only for confusable options («ب — ذلك هو **X** لا Y»);
   whole block 40–80 words (calc blocks, model answers and tables do not count). Bold ONLY in why/remember/distractors/model_answer/given/what.
9. **Low confidence** (`low_conf="<one clause with the page that would settle it>"`) ONLY when: the book supports the answer with a passing
   sentence or the concept is absent; sources disagree and the book does not settle it; the recalled wording could mean two things; the answer
   relies on a scientific correction. Never for unit placement, for a feared distractor, or when the book states the answer.
10. **Coverage (§9):** after the real questions, list the units with NO real question whose expected answer is the unit's own content and
    whose page lies inside the unit's page range. Write ONE generated MCQ per uncovered unit from the book's wording (`types=["generated"]`,
    `sources=["GEN"]`, verified page inside the unit), at most 3 for units that are not focus areas; never more generated than real questions
    in the chapter; never an idea an existing question already tests.
11. **Ids:** `QNN-001`, `QNN-002` … in the order exam → textbook → other → generated. `ch=N`, `sub="<unit code>"`.
12. **Chapter opener:** `OPENER = ("<one sentence: what the chapter is about>", "**term1**، **term2**، … (3–6 bold terms)")` and
    `SUBS = {"<unit code>": "<short Arabic name ≤ 8 words>", …}` for EVERY unit of the chapter.
13. Run `python -c "import bank_chNN"` from `W\render` (the Q() asserts pass), then `set PRM_LENIENT=1 && python build_bank.py`
    and make sure no assertion names your chapter (other chapters may be missing — that is fine).

## Report (`W\qa\chNN_report.md`, short)
Counts: raw items received / canonical records / by type / reconstructed / low-confidence / generated / calc / fig / fast / unsolved / see-links;
units covered by real questions, by generated, uncovered (with reason); items out of F25 scope (raw ids, one line each); number-less credits
applied (raw id → record ids); topic-only items; every disagreement between a source's marked answer and the book (raw id, their answer, the
book's answer, page); every book error you confirmed; pages rendered and read visually; anything you could not verify.
