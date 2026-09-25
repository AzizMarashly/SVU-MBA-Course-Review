# Chapter 7 helper report (ACM v1.0, prompt v0.12)

Scope used: the whole chapter except journal entries, as the brief's chapter-7 rule says. The transcriptions' `in_scope` flags were ignored.
The book's review marks (ticks on T/F, green highlight on MCQ) were treated as the book's answer, then checked against the text. All 9 marked
items agree with the text.

## Counts
- Raw items received: 83. Used in records: 69 (as a direct raw id or as a `~` credit). Not used: 14 (listed below).
- Canonical records: 38.
  - By type: exam 16 (3 of them also textbook), textbook only 15, generated 7.
  - By qtype: mcq 23, short 9, tf 5, essay 1.
- Reconstructed: 7 (Q07-004, 005, 009, 010, 012, 013, 014).
- Low confidence: 4 (Q07-004, 008, 010, 016).
- Other features: calc 23, table 5 (CASE_T and INV_T), ans_table 5 (CASE_ANS), fig 0, fast 4 (Q07-001, 002, 004, 005).
- Unsolved exercises solved: 3 (Q07-016, 030, 031).
- See-links: 2 pairs (Q07-006 ↔ Q07-030, Q07-007 ↔ Q07-031).
- METHODS: M1–M14 (straight line, sum of years' digits, double-declining, activity, asset cost, doubtful-debt allowance, bank reconciliation,
  cash shortage, inventory shortage, weighted average, FIFO, LIFO, deferral/accrual adjustments, depletion). No record uses M3 (double-declining)
  or M7 (bank reconciliation, which appears only in the essay's model answer). Both are defined because the owner asked for them.
- Added 29 symbols to `meta_acm.SYMBOLS` (added only, nothing renamed): DV HY HT AR BD PR PDD OPD NAR CB CA SH INV NSH ASH DMG EI UC TC CUR DEF MON
  REC ACC PP RC UD QE QX. `NS` already meant number of shares, so NSH and ASH are used for the shortages.

## Coverage (22 units, 0 uncovered)
- Covered by real questions (15 units): 7-1, 7-1-1, 7-1-2, 7-1-4, 7-2-2, 7-3-1-1, 7-3-1-2, 7-3-2, 7-4-2-3, 7-4-4, 7-5-1, 7-5-2, 7-5-3,
  7-5-4-2, 7-5-4-3.
- Covered by generated questions only (7 units): 7-1-3, 7-2-1, 7-4-1, 7-4-2-1 (FIFO), 7-4-2-2 (LIFO), 7-5-4-1 (activity), 7-5-5 (depletion).
  Each uses the book's own example data. Seven generated records is more than the brief's "at most 3" if that cap applies per chapter; the
  owner should decide. Without them these 7 units would stay uncovered.
- The generated question I first wrote for 7-1-1 was removed, because Q07-027 already covers that unit.

## Out of F25 scope (no record)
Each of these asks only which account is debited or credited:
- book#47 / summary#72: depreciation entry (accumulated depreciation credit).
- exams_b#6, exams_b#16, exams_b#50 (S24 Q7): the entry for paying the insurance.
- exams_b#25 (S24): the entry for the depreciation provision.
- exams_a#39 (F23): «قيود ايراد مستحق مقبوض مقدما», entries only and ambiguous.
- exams_a#88 (OLD): bad-debt entries.
- exams_a#120 (OLD): the customers entry on bankruptcy.
- exams_a#56 (OLD): the "name of the entry in month 11" of an insurance contract. The recall is too vague to reconstruct and asks only for an entry.

## Topic-only items (no record)
- exams_a#59 (OLD): «قوانين الاهتلاك كذا سؤال».
- exams_a#72 (OLD): adjustments of revenues and expenses.
- exams_a#89 (OLD): «سؤال عن المصاريف المدفوعة مقدما».
- These three were also credited as `~` on the matching records: exams_a#32 (F23) and exams_a#86 (OLD), theory on الاستنفاذ, on Q07-013;
  exams_a#87 (OLD), sum-of-years' digits, on Q07-005.

## Number-less credits applied
- exams_a#7 (S23), exams_b#65 (S24) → Q07-001.
- exams_a#6 (S23), exams_a#20 (F23), exams_b#43 / #63 (S24), exams_b#127 / #128 (F24), exams_b#158 (S25) → Q07-002.
- exams_a#21 (F23), exams_a#118 (OLD), exams_b#128 (F24) → Q07-003.
- exams_a#63, exams_a#87, exams_a#119 (OLD) → Q07-005.
- exams_b#66 (S24), exams_a#76 (OLD) → Q07-006.
- exams_a#122 (OLD) → Q07-007.
- exams_b#98 / #138 (F24), exams_a#115 (OLD) → Q07-015 and Q07-016.
- Not applied: exams_a#42 (F23, activity method). No real record of that type exists, and a generated record (Q07-037) cannot carry an exam
  credit. The owner may prefer to turn Q07-037 into a reconstructed F23 record that uses the book's example data (the approach used for charts).

## Source answer vs the book
- exams_b#8 (S24 Q9): the AI-written key says «كل ما سبق صحيح». The book's answer is «ح/ أمين المستودع مدين 10000»: option أ makes income a
  credit, but the book debits the income summary with the normal shortage (pp. 216–217).
- exams_a#8 (S23): the student recalled "added to the bank account in the books". In the book's memo these cheques are deducted from the book
  balance (pp. 202, 205). The record is low-confidence because the recalled «ستضاف إلى» fits a two-sided reconciliation, which gives the same effect.
- exams_b#24 (S24): the student answered «جميعها خاطئة لأنها التزامات متداولة». The book's answer is «التزامات قصيرة الأجل» (p. 194).
  The recall is inexact, so the record is low-confidence.
- All other marked answers agree with the book: S24 Q1, Q2, Q8; F24 5,000,000 and 300,000; the OLD 1,500,000; the book's 5 T/F and 4 kept MCQs.

## Book errors confirmed
1. Chapter case, cash shortage (pp. 232, 235, 236): the 9,000 is charged to the cashier by entry, but it is also deducted as a loss, and no
   receivable from the cashier appears. By the book's own rule (p. 208), net profit would be 693,400 and the balance-sheet total 2,825,400.
   Put on Q07-029 as `book_says`.
2. Chapter case, rent: the data say the buildings were let, but the solution treats «ايجار المباني» as prepaid. No record was made for it.
3. p. 217: the book writes «750000 − 20000 − 10000 (بضاعة تالفة) = 715000». The damaged goods cost 15,000, which gives 715,000. With the
   printed 10,000 the result would be 720,000. This is noted only here.
4. p. 227: the depletion is printed as «50000 × 15 = 75000000»; the correct figure is 750,000. Put on Q07-038 as `book_says`, and the printed
   figure is used as a distractor.
5. p. 212: the FIFO table prints 3 stray rows after 18 June (60 × 228, 44 × 218, 36 × 240). The correct balance is 14,776. Put on Q07-035.
6. p. 226: the double-declining example says "machine of one million, 10 years, no salvage", but its table uses 1,500,000 and 5 years
   (rate 40%). The book also applies the doubled rate to the remaining depreciable value, not the textbook-standard book value. M3 follows
   the book's table.

## Judgement calls for the owner
- Book MCQ 2 (lower of cost or market, Q07-023): its rule sits in 7-4-3, the excluded entries unit. It was kept as a concept item (balance-sheet
  presentation) and placed in 7-4-4, whose example applies the rule (p. 217).
- Q07-012 (where depreciation appears): the rule is on p. 228, inside the excluded unit 7-5-6. It is kept because it asks where the expense is
  shown, not the entry.
- Q07-016 (Exercise 1): the book has no example of topping up an existing allowance. The 37,500 charge (40,000 − 2,500) is my inference and
  carries low confidence. The total charged to income, 287,500, is the same under either treatment.
- S24 Q1, Q2, Q8, Q9 are wrapped as entries but kept with their options exactly as written: the point of each is the amount (asset cost, annual
  charge, cash shortage, shortage split). Each record's `notes` says this.
- Q07-004 and Q07-005 make the same claim (accumulated depreciation after the last year = cost − salvage) but have different data and
  answers, so they are not merged.

## Pages rendered and read visually (12)
205, 210, 211, 212, 213, 217, 224, 225, 226, 227, 238, 239. Pages 229–237 were already read by the transcriber and their amounts were used as
transcribed; the arithmetic was rechecked in python. Every number in the records was recomputed.

## Could not verify
- The original options of exams_a#8 (S23), exams_a#68 / #114 (OLD) and exams_b#88 (F24) were not recalled; they were rebuilt from the book.
- F24 exams_b#86: which declining-balance style was meant (low confidence).
- The useful life in exams_a#100 (OLD): 5 years was taken from the book's example on p. 225.

Checks: `python -c "import bank_ch07"` passes. `PRM_LENIENT=1 python build_bank.py` shows no assertion or warning for chapter 7 and
"uncovered: 0". `qa_blocks.py` lists no Q07 id.
