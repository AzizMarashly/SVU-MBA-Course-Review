# Stage-3 brief — transcribe the BOOK's own questions (ACM review v1.0, prompt v0.12)

Course: «المحاسبة للمديرين — Accounting for Managers (ACM)», textbook `Course/كتاب المحاسبة للمديرين.pdf`
(د. باسل أسعد, 447 pages, printed page = PDF page, verified on every page). This run covers the **F25 exam scope only**:
chapters 1, 2, 3, 10 in full; chapter 7 only section 7-5 (depreciation) without 7-5-6 (depreciation entries);
chapters 8 and 9 theory only (9 up to the intro of 9-4, p. 302). Chapters 4, 5, 6, 11, 12 are out.
Work only inside W = `C:\Users\root\SVU-MBA-Course-Review\courses\S2\ACM\.review_generation_working_directory`.
Set `PYTHONUTF8=1` for every python run. Never modify a source file. No personal data.

## Inputs
- Book text per page: `W\extracted\book\pNNN.txt` (and per chapter `W\extracted\book\ch\chNN.txt`, page markers `=== PAGE n ===`).
  Extraction is good on prose (~1 % error) but: (a) **thousands groups come out reversed and spaced**: `000  ،  500  ،1`
  on the page is 1,500,000 — read amounts carefully, and when in doubt render the page; (b) **formulas with fractions and
  multi-line tables are garbled** — render the page and read it with the Read tool:
  `python -c "import pymupdf;d=pymupdf.open(r'C:\Users\root\SVU-MBA-Course-Review\courses\S2\ACM\Course\كتاب المحاسبة للمديرين.pdf');d[N-1].get_pixmap(dpi=110).save(r'W\extracted\pages_png\book_pNNN.png')"`
  (create the folder; it is gitignored). Count the pages you rendered and looked at.
- Audit units with page ranges: `W\extracted\book\subsections.json` → `units` (chapter → code → name, pages). Codes are chapter-first
  (`1-4-1` = chapter 1, section 4, paragraph 1). The file also lists `excluded` parts and the `review_pages` of each chapter.
- Format of the output items: `W\extracted\FORMAT.md`.

## What to transcribe (all of it, faithfully — fix only obvious extraction damage, never invent an option or an answer)
1. **Every end-of-chapter review item** («أسئلة وتمارين») of the in-scope chapters: ch1 pp. 38–40, ch2 pp. 81–83, ch3 pp. 108–110,
   ch7 pp. 238–241, ch8 pp. 287–289, ch9 pp. 322–324, ch10 pp. 353–357. Types: true/false tables (`tf`), multiple choice (`mcq`,
   options in source order), essay/short questions (`essay` / `short`), exercises with data (`calc`, put every number in `stem`/`notes`),
   including **unsolved exercises** («تمارين غير محلولة», pp. 240–241 and 354–356) — mark them `unsolved: true`.
   For chapter 7 and 9 also transcribe the items that fall outside the F25 scope (e.g. inventory pricing, bank reconciliation, cost
   theories) but set `in_scope: false` with the unit or topic name; in-scope items get `in_scope: true`.
2. **The practical cases** («حالة عملية») inside the in-scope chapters and their solutions as printed: pp. 35 (ch1), 79 (ch2), 101 (ch3),
   229–236 (ch7 depreciation — check which pages belong to 7-5), 272–286 (ch8), 350–352 (ch10). One item per question asked in the case
   (`qtype: "calc"` or `"short"`), with the case data in `notes` and the book's printed solution in `marked_answer`, `marked_by: "worked-answer"`.
   Chapter 8 cases are full-statement preparation: transcribe them, set `in_scope: "theory-only chapter"`.
3. **Does the book mark its answers?** Render at least one true/false page and one MCQ page per chapter (e.g. pp. 38, 39, 81, 82, 108, 238, 287,
   322, 353) and look for ticks, highlights or a printed key. If the book gives no key, `marked_answer` is null and `marked_by` null for
   every review item; say so in the report. If it does mark answers, record the mark exactly and `marked_by: "highlight"` / `"key"`.
4. For every item fill `ch_guess` (book chapter) and `sub_guess` (unit code from subsections.json; for out-of-scope items the section code
   such as `7-4-2` or `9-5-1`). `src: "BOOK"`, `code: "BOOK"`, `loc: "p. N"`, `item` = the printed number (e.g. "T/F 3", "MCQ 5", "Q 2", "Case 1 (a)").

## Output
`W\extracted\questions\book.json` (UTF-8, no BOM, a JSON list of items) and `W\extracted\questions\book_report.md`:
counts per chapter and type (in scope / out of scope), whether the book marks answers (with the page you looked at), pages rendered
and read visually, anything unreadable, items whose chapter or unit is unclear, and every place where the printed solution of a
case looks arithmetically wrong (give the numbers — do not fix it).
