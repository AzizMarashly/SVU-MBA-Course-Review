# Chapter 3 helper report — ACM v1.0 (prompt v0.12)

Output: `render/bank_ch03.py`. `import bank_ch03` passes, `PRM_LENIENT=1 build_bank.py` has no assertion or warning for chapter 3, and
`qa_blocks.py` lists no Q03 id. Six symbols were added to `meta_acm.py` SYMBOLS (nothing renamed): Dr, Cr, Bal, TDB, TCB, Cap.

## Counts
- Raw items received: 36. Canonical records: 17.
- By type: exam 6 (5 of them also textbook), textbook-only 10, other 1 (Q03-017, textbook + SOL345), generated 0.
- By form: mcq 10, tf 6, short 1.
- Reconstructed: 1 (Q03-006). Low-confidence: 0.
- Calc: 6 (Q03-001, 002, 003, 005, 016, 017). Tables: 5 records. ans_table: 2. Fast routes: 2 (Q03-002, Q03-005). Figures: 0.
- Unsolved book exercises solved: 1 (Q03-017). See-links: 0. Also-lines: 1 (Q03-004 ← S24).
- METHODS: M1 balance an account (p. 90), M2 trial balance and the unknown balance (p. 91), M3 income account and balance sheet from the
  trial balance (p. 95).

## Coverage
- Every unit has a real question: 3-1 (Q03-012), 3-2 (Q03-007, 008), 3-3 (Q03-003, 004, 009, 015, 016), 3-4 (Q03-002, 010, 013, 017),
  3-5 (Q03-001, 005, 006, 011, 014).
- No generated questions were needed. Nothing is uncovered.

## Out of F25 scope
None. Chapter 3 is in scope in full. The sales-returns part of exams_a#51 belongs to chapter 6, which is out; this is noted on Q03-001.

## Number-less credits (§5c)
| raw id | record | what was asked |
|---|---|---|
| ~exams_a#22 (F23) | Q03-002 | capital as the unknown |
| ~exams_a#40 (F23) | Q03-002 | bank balance as the balancing figure |
| ~exams_a#23 (F23) | Q03-001 | net income |
| ~exams_a#45 (F23) | Q03-001 | net profit |
| ~exams_a#60 (OLD) | Q03-001 | net profit before tax |
| ~exams_a#51 (OLD) | Q03-001 | income statement |
| ~exams_a#116 (OLD) | Q03-001 | total expenses from the trial balance |
| ~exams_a#130 (OLD) | Q03-005 | one balance-sheet item |

- The F23 case (purchases, sales, salaries, advertising) looks like the book's case on pp. 101–107. So the case was split into four MCQ records
  (Q03-001, 002, 005, 016: raw ids book#37@1–@4), and the credits sit on them.
- Capital as the unknown has no record of its own, because no recall kept any numbers. It is covered by M2 and by the fast route on Q03-002
  (unknown balance = the difference between the two sides, p. 91). A worked example from the case data is in the notes: 15,710,000 − 7,710,000 = 8,000,000.

## Folded or merged items
- **SUM:** summary#22–32 duplicate the book's T/F 1–6 and MCQ 1–5 word for word. "SUM" was added to the sources of those 11 cards.
- **exams_a#53 (OLD):** a recall of MCQ 4 with the sides reversed, which the recaller was unsure of. It became a variant on Q03-003. If the
  reversed version is the right one, the answer would be credit 600 (noted on the card).
- **exams_b#55 (S24, "define balancing"):** folded into Q03-004 (T/F 3) as an MCQ also-line.
- **exams_a#75 (OLD, which credit accounts close to income):** reconstructed as Q03-006 with its own claim (sorting the credit balances). It is
  close to Q03-011. The duplicate check pairs Q03-011 with Q08-013 on bold keywords only (0.53); the owner should look at that pair.

## Marked answers vs the book
- All 11 book marks agree with the chapter text: the T/F ticks on p. 108 and the green MCQ highlights on pp. 108–109, all checked on the page images.
- The SUM keys agree with the book.
- SOL345 (the student solution of the p. 109 exercise) agrees with my own solution in every entry and balance: trial balance 70,000 = 70,000.
- No source disagrees with the book.

## Book errors confirmed
- **p. 102, bank ledger account in the case (confirmed on the image).**
  - The 4,000,000 equipment credit ("شراء تجهيزات بشيك") is missing, and the balance is printed as "رصيد مدين 7,728,000" with totals of 13,810,000.
  - The listed credits add up to 4,582,000, so 4,582,000 + 7,728,000 = 12,310,000 ≠ 13,810,000.
  - The correct balance is 13,810,000 − 8,582,000 = 5,228,000. This is the figure the book's own trial balance (p. 106) and balance sheet (p. 107) use.
  - Recorded on Q03-016 as `book_says`, not `sci`, because it is an arithmetic slip. 7,728,000 is used as a distractor.
- **p. 102, capital account:** the total is printed as 800,000 on the debit side instead of 8,000,000. This is a typo with no effect on any record.
- Everything else was recomputed in Python and matches the book: trial balance 15,710,000; income account 6,110,000 with net profit 228,000;
  balance sheet 9,828,000.

## Pages
- Rendered this run: 87, 90, 91, 95, 99, 103, 104, 106, 107, 110.
- Read visually: 101, 102, 106, 107, 108, 109. 101, 102, 108 and 109 were already rendered at stage 3.
- The other rendered pages have clean digits in the text layer, or amounts confirmed by recomputing the totals.

## Could not verify / assumptions
- **Q03-017:** the exercise does not give the cost of the furniture and land that were sold. The solution assumes they were sold at book value
  (no gain or loss), as the student solution does. This is stated in the notes.
