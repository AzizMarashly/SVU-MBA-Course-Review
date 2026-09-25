# Stage-3 brief — the summary and the scanned solutions (ACM review v1.0, prompt v0.12)

Course «المحاسبة للمديرين — ACM», textbook `Course/كتاب المحاسبة للمديرين.pdf` (447 pages, printed page = PDF page).
F25 scope: chapters 1, 2, 3, 10 in full; chapter 7 only 7-5 depreciation (no entries); chapters 8, 9 theory only; 4, 5, 6 out.
Work only inside W = `C:\Users\root\SVU-MBA-Course-Review\courses\S2\ACM\.review_generation_working_directory`. `PYTHONUTF8=1`.
Never modify a source file. No personal data (the summary names its author on p. 1 — that is a public author credit, keep it out of the JSON anyway).

## A. The summary `Summaries/ملخص المحاسبة للمديرين ACM.pdf` (30 pages; text in `W\extracted\summary\pNNN.txt`, p. 8 is an image: `W\extracted\summary\p008.png`)
1. Read it all. It is a theory summary («ملخص عاصم»). Report: which book chapters/sections it covers (map its headings to the book's
   chapter numbers), whether it contains any questions or worked exercises (if yes, transcribe them into `W\extracted\questions\summary.json`
   per `W\extracted\FORMAT.md` with `src: "SUM"`, `code: "SUM"`), and which parts it says the instructor deleted («أجزاء حذفها الدكتور»).
2. Transcribe the image page 8 (Read tool on the PNG) into `W\extracted\summary\p008.txt` — tables one row per line, ` | ` between cells.
3. List 10–20 definitions or lists in the summary that a student would memorise (term → summary wording, with the summary page), so the
   chapter helpers can use them as cross-checks against the book. Put them in the report.

## B. The scanned solutions `Course/حل مسائل غير محلولة الفصول 3 4 5 ACM.pdf` (7 pages, no text layer; PNGs `W\extracted\solved_345\pNNN.png`)
Read every page image with the Read tool and transcribe it fully into `W\extracted\solved_345\pNNN.txt` (handwritten or printed; tables one row per
line with ` | `; numbers exactly as shown; `[?]` after any uncertain token). Then write `W\extracted\questions\solved345.json`: one item per
solved problem, `src: "SOL345"`, `code: "SOL345"`, `qtype: "calc"`, `stem` = the problem as far as the sheet states it, `marked_answer` = the
solution as written, `marked_by: "worked-answer"`, `ch_guess` (3, 4 or 5), `notes` = which book exercise it seems to solve (compare with the
unsolved exercises at the end of book chapters 3, 4, 5: pp. 108–110, 131–133, 156–158 in `W\extracted\book\pNNN.txt`). Chapter 3 is in
scope; chapters 4 and 5 are not, transcribe them anyway and mark `in_scope: false`.

## Report `W\extracted\questions\others_report.md`
Coverage map of the summary, question count found (may be zero), the definitions list, the solved-345 items with the book exercise they
match, pages/images read visually (count), anything unreadable.
