# BOOK end-of-chapter review questions — transcription report

Source: `MBA - Project Management - The Book.pdf` (554 pages, printed page = PDF page), text split per chapter in
`extracted/book/ch/chNN.txt`. Output: `extracted/questions/book.json` — 187 items, `src="BOOK"`, `loc` = book page.

## Answer marking (important)

The book prints **no answer key** with the questions, BUT every MCQ in every chapter has **one option
highlighted in yellow** in the PDF (a filled rectangle behind the option line). These highlights were detected
programmatically (yellow-pixel bands per review page, mapped to the text spans) and spot-checked visually on
pages 108, 109, 357, 393, 422, 464, 465, 505. They are recorded as `marked_answer` (0-based index) with
`marked_by = "highlight"`. Exactly one MCQ has no highlight: chapter 12 mcq-7 (`marked_answer = null`).
Answers were NOT verified.

Pages 346, 347, 459, 496, 497, 535 were checked: the words "الحلول"/"إجابات" there are ordinary body text
(manual/mathematical *solutions* to resource problems, brainstorming solutions, lessons learned, answers in a case
study) — none of them is an answer key.

## Per chapter

| ch | review pages | MCQ | essay/calc | notes |
|----|--------------|-----|------------|-------|
| 1 | 40–42 | 10 | 4 | MCQ 6–10 and essays 3–4 cover chapter-2 material (triangle trade-off, benefits/challenges, history, PM role). |
| 2 | 73–75 | 10 | 4 | **Verbatim reprint of the chapter 1 review** (same questions, same highlights). Items carry `dup_of` -> chapter 1 item. |
| 3 | 108–109 | 6 | 4 | Only 6 MCQ (confirmed visually on p.108–109). |
| 4 | 156–158 | 10 | 4 | — |
| 5 | 189–191 | 10 | 4 | MCQ 5–10 and essays 3–4 cover chapter-6 material (WBS, OBS, RAM, communication plan). |
| 6 | 230–232 | 10 | 4 | **Verbatim reprint of the chapter 5 review**. `dup_of` -> chapter 5 item. |
| 7 | 272–276 | 10 | 1 essay + 3 calc | MCQ 3, 7–10 cover chapter-8 material (CPM, forward pass, compression, estimation). Essays 2–4 are network/Gantt exercises with activity tables (transcribed into `notes`). |
| 8 | 313–317 | 10 | 1 essay + 3 calc | **Verbatim reprint of the chapter 7 review**. `dup_of` -> chapter 7 item. |
| 9 | 355–358 | 10 | 2 essay + 2 calc | Essay numbering on p.358 is 3, (empty "4-"), 5 — items recorded as essay-3 and essay-5. Tables in `notes`. |
| 10 | 391–394 | 10 | 2 essay + 2 calc | mcq-7/8 share a stem (schedule vs cost conclusions); mcq-9/10 are numeric EVM items. Essay 4 is a 5-part EVM exercise (X1..X10 table + cost data) fully transcribed in stem/notes. |
| 11 | 422–423 | 5 | 4 | Only 5 MCQ (confirmed visually on p.422; p.423 has MCQ 4–5 then the essays). |
| 12 | 464–466 | 10 | 4 | mcq-1: options أ and ث are printed identical (ث highlighted). **mcq-7 has no highlighted answer.** |
| 13 | 505–508 | 10 | 4 | — |
| 14 | 538–540 | 10 | 4 | — |

Totals: 131 MCQ, 56 essay/calc (46 essay + 10 calc) = 187 items.
Unique (non-reprint) content: 101 MCQ, 42 essay/calc.

## Pages read visually (PNG in `extracted/pages_png/book_pNNN.png`)

108, 109 (ch3 — scrambled stem of mcq-1, MCQ count), 275, 276, 277 (ch7 exercise tables, incl. the lag table),
357, 358 (ch9 — option order of mcq-9, exercise tables, odd "4-" numbering), 393, 394 (ch10 — EVM tables and
X1..X10 network table), 422 (ch11 mcq-1/2 options), 464, 465 (ch12 — identical options of mcq-1; missing highlight
of mcq-7), 505 (ch13 mcq-1 sequences). Chapter 8's tables (p.316–317) were not re-rendered: the extracted text is
identical to chapter 7's tables.

## Text-repair notes

* The PDF text layer stores every lam-alef ligature reversed (e.g. `األعمال` for `الأعمال`, `ال` for `لا`,
  `ثالث` for `ثلاث`); these were repaired throughout. Words were also re-joined where the extraction split them
  (`شك|الً`, `وم|ا`, `الأ نشطة`).
* Book typos were kept as printed and flagged in `notes` (e.g. `الزبزن`, `ومدرايريهم`, `الزني`, `قتوات`, `المروع`,
  `التفديرية`, `Finsish`, `Botom-Up`, `INTELIGENT`, `Rigester`, `علية`).
* `src10/text.txt` (earlier print of the same review pages) was used only to confirm `شكلاً` in ch1 mcq-2.
* Case studies (English, "حالة عملية رقم N") after each review section were ignored as instructed.

## Odd things

1. Three chapter pairs (1/2, 5/6, 7/8) reprint the identical review block; the second copy is marked with `dup_of`.
2. Chapter 3 has 6 MCQ and chapter 11 has 5 MCQ; all others have 10.
3. Chapter 9 essay list skips number 4 (empty label) and goes 3 -> 5.
4. Chapter 12 mcq-1 has two identical options (أ = ث); chapter 12 mcq-7 has no highlighted answer.
5. Chapter 3 mcq-5 and chapter 7 mcq-3 have stems that already contain the answer wording (printed that way).
6. `sub_guess` points to the subsection that actually covers the item, which for the "reprint" pairs and for
   several chapter 1/5/7 items lies in the following chapter; `ch_guess` is always the chapter the item is printed in.

## Per-chapter counts (MCQ / essay+calc)

ch01 10/4 · ch02 10/4 · ch03 6/4 · ch04 10/4 · ch05 10/4 · ch06 10/4 · ch07 10/4 · ch08 10/4 · ch09 10/4 ·
ch10 10/4 · ch11 5/4 · ch12 10/4 · ch13 10/4 · ch14 10/4 — total 187
