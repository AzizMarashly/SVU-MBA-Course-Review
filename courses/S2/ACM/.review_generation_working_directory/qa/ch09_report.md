# Chapter 9 helper report (ACM v1.0, prompt v0.12, F25 scope: theory up to p. 302)

Output: `render/bank_ch09.py`. `import bank_ch09` passes, and `PRM_LENIENT=1 build_bank.py` shows no assertion for ch 9.

## Counts
- Raw items received: 52. Canonical records: 11 (10 real, 1 generated).
- By qtype: 9 MCQ, 2 T/F. By type: 10 exam (5 of them also textbook), 0 textbook-only, 1 generated.
- Reconstructed: 5 (Q09-001, 003, 005, 006, 007). Low confidence: 1 (Q09-003). ans_table: 1 (Q09-001, the p. 295 comparison table).
- calc 0 / fig 0 / fast 0 / unsolved 0 / see-links 0 / METHODS none (theory only). All blocks are 49–69 words.

## Units
- Covered by real questions: 9-1 (Q09-001), 9-2 (Q09-002, 003), 9-3-1 (004), 9-3-2 (005, 006, 007), 9-3-3 (008), 9-3-4 (009), 9-3-5 (010).
- Covered by generated only: 9-4 (Q09-011, definition of the cost accounting system, p. 302).
- Uncovered: none.
- Placement: the two conditions of a cost (and "planned cost") sit in the 9-3 introduction (pp. 298–299), which has no audit unit of its own. They are put in 9-2, because p. 298 is inside its range. The SUBS name of 9-2 now says «…ومفهوم التكلفة».
- Standard and actual costs (9-3-4) are on p. 302, outside the unit's range [301]. They are tested only as distractors and in Q09-003.

## Folding (§5a)
- Book review items are the kept cards. Exam recalls without options were reconstructed in the book's form and became variants: Q09-002 (MCQ 4), Q09-004 (MCQ 1), Q09-008 (MCQ 2). On the T/F cards they became `also` lines: Q09-009 (T/F 3) and Q09-010 (T/F 4).
- Exam-only claims got their own reconstructed four-option MCQs: fin vs cost accounting, planned cost, fixed, variable, semi-fixed.
- SUM items summary#85, 86, 89, 90, 92 add SUM to the book cards.

## Out of F25 scope (no record)
- book#67 (T/F 1, unit guide 9-4-1-3); book#68 (T/F 2, total-cost method 9-5-1); book#71 (T/F 5, value chain); book#72 (T/F 6, product life cycle); book#75 (MCQ 3, pillars 9-4-1); book#77 (MCQ 5, strategic approaches).
- summary#83, 84, 87, 88, 91, 93: the SUM copies of those same items.
- exams_b#29 (S24, target costing); exams_b#147, exams_b#159 (S25, target costing/pricing).

## Number-less / topic credits
- ~exams_b#35 (S24 «سؤال عن التكاليف الغارقة») → Q09-010.
- Topic lines from sittings already on a record were added as plain raw ids:
  - exams_b#46 → Q09-004
  - exams_b#69 and #118 → Q09-002
  - exams_b#51@1 / @2 → Q09-007 / Q09-005
  - exams_b#72 → Q09-006
  - exams_a#108 and #109 → Q09-008 / Q09-010

## Not used (needs the owner's decision)
- exams_b#37 (S24): «انو سعر الوحدة الواحدة ما بيتغير بتغير حجم الانتاج», options متغيرة / ثابتة / تكلفة تاريخية, no answer.
- As worded it is about per-unit behaviour. The answer would be "variable" (constant variable cost per unit, ch 10 p. 328–330). If it means total cost, the answer is "fixed", which is Q09-005. Chapter 9 says nothing about per-unit behaviour.
- I did not merge it into Q09-005, because the answers may differ. Suggest a ch 10 (10-1-2) record, or drop it.

## Disagreements between a source and the book
- F24 exams_b#70: the students' answer is «عندما يحقق شرط الانتفاع». The book requires both conditions, use and benefit (pp. 298–299). This is a partial answer, not a contradiction, and is recorded on `other_source` of Q09-002.
- Every book mark checked (T/F 3 خطأ, T/F 4 خطأ, MCQ 1 ب, MCQ 2 د, MCQ 4 ج) agrees with the text.
- The S23 answer (acquisition → use) and the F24 controllable answer agree with the book.

## Book errors confirmed (typos only, no science error)
- p. 300: fixed costs are labelled «Nun-current Costs».
- p. 302: «Sank Costs».
- p. 301 and p. 323: «انتتاج».
- All three are noted in the record notes. Nothing needs `book_says`.

## Cross-chapter
- Fixed/variable definitions (Q09-005, 006) overlap ch 10 unit 10-1-2 (pp. 329–330). Check for consolidation when ch 10 is in.
- The financial vs cost accounting table may overlap ch 1 (1-8, branches of accounting). No neighbours were flagged against ch 1.

## Pages
- Rendered and read visually: 295 (comparison table), 322 (T/F ticks), 323 (MCQ highlights).
- Read from text: 294–302 (and 303 to confirm the scope cut-off).
- Nothing left unverified, except the exact wording and options of the recalls, which the sources do not preserve.
