# Chapter 10 report (تخطيط الإنتاج والأرباح، تحليل التعادل), ACM v1.0, prompt v0.12

Output: `render/bank_ch10.py`, with 45 records and 7 METHODS (M1 break-even, M2 shutdown, M3 target profit, M4 margin of safety,
M5 marginal income statement / CMR / ΔCM, M6 sales mix, M7 capacity). `import bank_ch10` passes. `PRM_LENIENT=1 python build_bank.py`
passes with no chapter 10 warning (uncovered: 0). `qa_blocks.py` passes for chapter 10 except one heuristic, listed at the end.
I added 11 symbols to `meta_acm.SYMBOLS` (add only): TVC, TCM, TC, DS, DCM, SPV, VT, SMR, MCMR, CU, BECU.

## Counts
- Raw items received: 99. Canonical records: 45.
- By type: exam 25 (6 of them also textbook), textbook-only 19, generated 1. By form: mcq 25, short 16, tf 4.
- Other counts:

| reconstructed | low_conf | generated | calc | fig | fast | unsolved | tables | answer tables | see-links |
|---|---|---|---|---|---|---|---|---|---|
| 14 | 2 (Q10-012, Q10-018) | 1 (Q10-045) | 24 | 13 | 14 | 10 | 17 | 5 | 1 pair (Q10-010 ↔ Q10-034) |

- Chart questions (all use the book's p. 345 data, P 20, V 12, FC 100000, Dep 20000):
  - Q10-001: shutdown point
  - Q10-002: break-even point
  - Q10-003: total revenue line
  - Q10-004: total cash cost line
  - Q10-005: cash fixed line
  - Q10-006: fixed line
  - Q10-007: vertical axis
- Other figures: Q10-012, Q10-021, Q10-029, Q10-032, Q10-033, Q10-037.
- Unsolved exercises solved (pp. 354–356):
  - Ex 1: Q10-036, Q10-037.
  - Ex 2: Q10-038, Q10-024, Q10-039.
  - Ex 3: Q10-040.
  - Ex 4 (price, quantity, variable cost, fixed cost): Q10-041 to Q10-044.

## Units
- Covered by real questions: every unit except 10-2-3-4. That is 10-1-1, 10-1-2, 10-1-3, 10-1-4, 10-2-1, 10-2-2, 10-2-3-1,
  10-2-3-2, 10-2-3-3 and 10-2-4.
- Covered by a generated question: 10-2-3-4 (capacity usage, Q10-045, from the p. 347 example). F24 #41980 says this unit was deleted
  in that sitting, but the F25 message asks for chapter 10 in full.
- Uncovered: none.

## Out of F25 scope
None. Chapter 10 is fully in scope.

## Number-less credits (§5c)

| Raw item(s) | Record(s) |
|---|---|
| ~a#80 | Q10-001, 004, 005 |
| ~a#62 | Q10-001, 004, 006 |
| ~a#44 | Q10-001 |
| ~a#95, ~a#127, ~a#43, ~b#145 | Q10-002 |
| ~a#14 (S23 «name of line 2», line unknown) | Q10-003 to 006 |
| ~a#64 | Q10-012 |
| ~b#100, ~a#15 (S23 reverse break-even) | Q10-013 |
| ~b#113 | Q10-014 |
| ~b#73, ~b#120 | Q10-020 |
| ~a#65, ~b#38 | Q10-021, Q10-022 |
| ~a#126 | Q10-022 |
| ~a#41, ~a#66, ~a#92, ~b#99, ~b#139 | Q10-023 |
| ~b#76, ~b#77, ~b#123, ~b#153 | Q10-024 |
| ~b#36, ~b#68, ~b#114 | Q10-025 |

The target-profit, CMR and mix recalls have no MCQ record of their type, so their credits sit on the book case or exercise record of
that type. That is why Q10-023, 024 and 025 are exam cards.

## Topic-only items (no record)
- exams_a#81, exams_a#96, exams_a#128: «سؤال عن هامش الأمان».
- exams_a#85: «سؤال عن الربح المخطط».
- exams_a#102: «هي الرسمة يلي اجت حرفيا», an image that is not available.
- exams_b#143: «تركيز ع المساهمة … سؤالين نظري».

## Source answers that disagree with the book
- **exams_b#5 (S24 Q6, sales-mix ratio).** The circulated AI key says «كل ما سبق خاطئ». It uses units: 8000 ÷ 12800 = 62.5%. The book
  computes the ratio from revenue (tables on pp. 349 and 351): 24,000,000 ÷ 48,000,000 = **50%**, which is option ب. Record Q10-014
  carries `other_source`.
- **exams_b#105 (F24).** The recall says «هامش المساهمة = صفر لما تتساوى الإيرادات مع التكاليف». The book (p. 341) says that at
  break-even total CM = fixed costs and profit = 0. Record Q10-018 has low_conf, because what the exam asked is not known.
- **exams_a#131 (OLD, margin of safety).** No answer was given. With the data as recalled (400 units, «18000,000») no option fits.
  Only 28000 fits, and only with 40000 units and FC 18,000,000. Record Q10-012 has low_conf.
- **exams_b#82 (F24).** The recalled answer «خط الايرادات النقدية الكلية» is not a term the book uses. I attached it to the
  total-revenue card Q10-003 with a note that it may mean the total cash cost line.
- **exams_b#80 (F24).** Students disagree on whether the question asked for the fixed line or the fixed cash line. Both lines have a
  card (Q10-006 and Q10-005).
- Everything else agrees with the book:
  - The book's own marks (T/F ticks p. 353, green highlights pp. 353–354) all agree with the text.
  - The student answers on S23 a#2, S24 b#9, b#32 and b#33 also agree.
- Book T/F 1 and T/F 4 are the same claim, one true and one false. I folded them into one card (Q10-026) with an `also` line. As
  separate cards they would fail the build's same-options / different-answer check.

## Book errors confirmed
- **p. 352.** The mix break-even value is printed as 120000 (the fixed costs). The correct value is 120000 ÷ 48.57% = **247,058.82**,
  and the book's own next lines use it (141,176.47 and 105,882.35). Recorded as `book_says` on Q10-025.
- **p. 344.** The shutdown value formula is printed «÷ هامش المساهمة». It should be ÷ the CM ratio, or SP × P; the p. 345 chart shows
  200000. Recorded as `book_says` on Q10-001 and in the M2 fast route.
- **p. 346.** The text gives fixed costs of 100000, but the solution divides 50000 ÷ 8 = 6250. This is the error students reported
  (#19400). Recorded as `book_says` on Q10-011.
- Minor slips, noted but with no effect on any answer:
  - p. 349: 35.65% against 35.64% in the table, and 17825 against 17824.
  - p. 332: the variable cost is printed «1 × 24,000» instead of 120,000.
  - p. 335: the variable cost per unit (20,000) is missing from the text.
  - Ex 1: says «عدد الخزائن» but the product is pumps.
  - Ex 3: stray words «مكتبي/مكتبية».
  - Ex 2: the data are annual but the exercise asks for a statement «عن شهر كانون الثاني».

## Pages
- Read visually (18): 335, 336, 338, 339, 340, 341, 343, 344, 345, 346, 347, 348, 349, 351, 352, 353, 354, 355.
- Rendered but not opened: 330, 342, where the text layer was clean.
- p. 350 case data come from the page-image transcription made in stage 3. Its amounts are consistent with the printed solution.

## Could not verify / for the owner
- **Renderer.** `render_fig` always labels the lines ("الإيرادات الكلية", "التكاليف الثابتة النقدية" …) and the points. On the seven
  unlabelled-chart questions (Q10-001 to Q10-007) the figure therefore shows the answer before the reader chooses. I suggest an option
  such as `F(..., labels=False)`, or numbered labels, for these records.
- The exams' line numbering (for example S24 «line 5», S23 «line 2») was never recalled, so the stems describe each line by its
  position instead.
- `qa_blocks` flags «synonym-looking option pairs» on Q10-003 to 006, 008, 009, 011, 017 and 018. These are distinct book terms that
  share words ("خط التكاليف الكلية" / "…الكلية النقدية"), not synonyms. I left them as they are.
