# soufi.json — transcription report (src05 + src06, "محمد صوفي" files)

## Method
- Rendered every page of both PDFs at 120 dpi to `extracted/pages_png/soufi_p01..14.png` and `soufi1_p01..04.png`
  and read all **18 page images** (plus 5 zoomed 220 dpi crops of the network screenshot, the src06 tables and the
  red-pen regions of pp. 11-12) to recover true digits and answer marks. The extracted text was used only as a base
  for the Arabic wording; every number was taken from the images (the PDF font maps ٠→1, ٢→1 etc.).
- Output: `extracted/questions/soufi.json`, **162 items** (src05: 120, src06: 42).

## Totals per page
| src | page | items |
|---|---|---|
| src05 | 1 | 9 (item 9 spills to p2) |
| src05 | 2 | 9 (18 spills to p3) |
| src05 | 3 | 7 (25 spills to p4) |
| src05 | 4 | 12 |
| src05 | 5 | 11 |
| src05 | 6 | 11 (59 spills to p7) |
| src05 | 7 | 8 (67 spills to p8) |
| src05 | 8 | 9 (76 spills to p9) |
| src05 | 9 | 8 (84 spills to p10) |
| src05 | 10 | 8 (92 spills to p11) |
| src05 | 11 | 8 |
| src05 | 12 | 9 (second "108" spills to p13) |
| src05 | 13 | 6 (114 spills to p14) |
| src05 | 14 | 5 (+ empty "120-") |
| src06 | 1 | 6 (items 1, 2, EVA sub-items 3.1-3.4) |
| src06 | 2 | 12 (EVA 3.5, network sub-items 4.1-4.10, three-point item 5) |
| src06 | 3 | 12 (items 6-17) |
| src06 | 4 | 12 (items 18-29) |

qtype split: mcq 100, tf 27, calc 21, short 11, topic 3.

## Answer marks
- src05 pp. 1-6 and items 87-91, 109-119: answers highlighted in **yellow** → `marked_by: "highlight"`.
- src05 items 63-86 and 92-108: answers circled/underlined with **red pen** (handwritten) → also recorded as
  `marked_by: "highlight"`, with "red pen" stated in `notes`. No printed answer key exists (no `"key"`).
- src05 item 18 has two options highlighted (multi-answer, `marked_answer: [0,1]`).
- src05 item 62: nothing marked; handwritten "X تكلفة" — the correct option (إدارة التكلفة) is missing from the print
  and option ث duplicates option أ.
- src06: **no marks at all**; four items carry the student's recalled answer in parentheses/inline
  (items 10 "تحطيم", 12 "دلفي", 24 "value chain analysis", 27 "مدة المشروع غير محددة") → `marked_by: "student-recall"`.
- 119 items marked by highlight/pen, 4 student-recall, 39 unmarked.

## Book review questions vs. exam recollections
- `book_dup: true` on **67 items**. src05 items 1-14, 60-95 and 107-119 are verbatim (or near-verbatim) copies of the
  textbook end-of-chapter MCQs in `extracted/src10/text.txt` (same stems and option sets, chapters 1, 2, 4, 5, 6, 7,
  8, 9, 10, 11, 12). Four src06 items (15, 16, 18 and the src05-dup 14) repeat book questions.
- The remaining ~53 src05 items (15-59 and 96-106) are **not** in the book: PMBOK-flavoured T/F and MCQ items
  ("إجرائية", "البيان التمهيدي للنطاق", "أصول عمليات المنظمة", org-structure scenarios, "/15 ... أفضل معدل عائد",
  critical-path-from-list item 104). These read like past-exam recollections / an older question bank.
- src06 is entirely exam recollection (see header below): 42 items, of which 21 are calculation sub-items.

## Duplicates inside the file (`dup_of`, 10 items)
src05 51→27, 52→21, 54→25, 55→16; src06 14→src05 56, 15→69, 16→71, 17→102, 18→115, 20→91.

## Evidence of the sitting
- src06 page 1 carries an outlined/WordArt header the text extraction dropped:
  **"أسئلة امتحان مقرر ادارة المشاريع اجت بتاريخ 4/2/2020 للفصل S19"** — i.e. the exam of 4 Feb 2020, semester S19.
  The file ends "بالتوفيق جميعا". Both file names carry "S19".
- src05 header: "أسئلة في مقرر ادارة المشاريع + اسئلة دورات PM" — no date or semester inside the file; page footer
  numbers only. Header on every page: "Muhammad Soufi / Project Management / Mohamad_102387".

## Calculation items (all data placed in `notes`)
- src05 #24: embedded screenshot "Question 7" — AON network A6 B7 C10 D1 E4 F9 G8 H4 I11 J6 K3 with the arrows
  listed in notes; activity R (5 days) inserted between A and B; options 49/48/52/53, 49 highlighted.
- src05 #92-95: BCWS=10, ACWP=14, BCWP=12; #94 planned 100 days (options 71/83/120/140, 83 circled);
  #95 budget 1000$ (options 714/857/1167/1400, 1167 circled).
- src06 #1: SS relation, 6 and 12 with lag 4; options 10/12/16/6.
- src06 #3.1-3.5: EVA table (header literally "ACWS"): T1 4000/6000/5000, T2 8000/3000/6000, T3 7000/8000/4000,
  T4 9000/5000/10000, T5 4000/4000/4000 (BCWS / ACWS / BCWP).
- src06 #4.1-4.10: X1(-,4,3) X2(X1,2,4) X3(X1+X4,6,3) X4(-,5,2) X5(X4,3,2) X6(X3+X2,4,3) X7(X6,5,4) X8(X5,7,2)
  (pred, duration, workers); ten sub-questions (LF of X3, float of X6, critical path, "fs" of X8, delay X2 by 6,
  delay X3 by 3, workers after levelling, max workers before levelling, activities shifted, total duration).
- src06 #5: three-point estimate, optimistic 60 / pessimistic 20 / most likely 25 as written; options 30/60/40/32.
- src06 #6: NPV −20000 vs −50000 at 15%.
- src06 #10: cost 10000, finished two weeks early → "(تحطيم)".

## Items not read with full confidence / caveats
- src05 #96: stem is garbled ("/15 تمثل أفضل معدل عائد على الاستثمار") — the numbers of the original question are
  lost; only the marked option (66%) is certain.
- src05 #104: critical path chosen from "1-2-3-4 / 1-3-4-5 / 1-2-5-1 / 1-3-2-2" with no network given in the file.
- src05 #27: stem starts with the truncated word "holders" (Stakeholders).
- src05 #13: highlighted answer is "الإنهاء" although the stem describes execution and no "التنفيذ" option exists —
  transcribed as printed.
- src05 #117: "التجنب" highlighted for the accept-strategy description — transcribed as marked, not verified.
- src05 #62: no answer mark, missing correct option (see above).
- src05 #65, #98, #101, #102, #105: pen marks are underlines/circles on a word or on the option letter rather than
  the whole option; interpreted as marking that option.
- src05 #91: a stray yellow speck also touches the "ث-" label of the last option; ب is the real highlight.
- src06 #4.4: "ماهي fs لا x8" — "fs" assumed to be free slack of X8.
- src06 #5: optimistic (60) larger than pessimistic (20) as written — likely swapped by the student.
- src06 #21-#23, #25: fragments; qtype/chapter are guesses (#23 chapter left null).
- src06 header on p1 is image-like outlined text; read from the render, not from the text layer.
- Item numbering quirks: src05 prints "108" twice (recorded as "108" and "108 (second)"); src05 ends with an empty
  "120-"; src06 prints "5" twice on p2 (EVA sub-item 5 and the three-point item 5).
- Answers were NOT verified against the textbook.
