# Chapter 2 helper report: bank_ch02.py (ACM v1.0, prompt v0.12)

## Counts
- Raw items received: 60 (`by_chapter/ch02.json`). 54 were used. 10 more came from `out_of_scope.json` (see below).
- Canonical records: **48** (Q02-001 … Q02-048).
  - By section: 17 exam, 30 textbook, 1 generated. Q02-015/016/017 are book exercises that also carry F24 credits for problems recalled without numbers, so they are typed exam.
  - By form: mcq 20, tf 6, short 21, essay 1.
- Reconstructed: 8 (Q02-004, 008–014).
- Low confidence: 3 (Q02-020, Q02-030, Q02-037).
- Calculation blocks: 9. Answer tables: 7. Data tables: 1. Fast routes: 2. Figures: 0.
- Unsolved book exercises solved: 20, the journal exercises on pp. 71–78 (Q02-015/016/017, 031–047). The p. 79 case keeps the book's own solution. These exercises have no raw ids because stage 3 did not transcribe them, so the build lists them as "real records without raw".
- See-links: 2 symmetric pairs: Q02-001↔Q02-047 (rent collected) and Q02-002↔Q02-016 (purchase returns).
- METHODS: M1 (compound entry with split payment, p. 66), M2 (discount on a sale or purchase, p. 80), M3 (accounting equation, solving for the missing capital, p. 59).
- Symbols added to `meta_acm.py` (added only, nothing renamed): Amt, Paid, Rest, DiscR, Disc, Net.
- Checks: `import bank_ch02` passes. The lenient build shows no assertion for ch 2. qa_blocks is clean for ch 2 except one flag, explained below.

## Coverage
- Units covered by real questions:
  - 2-1-2
  - 2-2-1
  - 2-2-2
  - 2-3-1
  - 2-3-2
- Covered by a generated question: **2-1-1**, with Q02-048 (the documents group, p. 44). The only real item on this unit is T/F 1 (Q02-018), and its fact is on p. 45, which is outside the unit's page range [44]. The build warns about this as "mentioned".
- Uncovered: none.

## Out of F25 scope / not built here
- **exams_a#105 (OLD, «مدخلات النظام المحاسبي»)**: belongs to **ch 1, unit 1-5, p. 21**: inputs are «البيانات الكمية المتعلقة بالأحداث الاقتصادية». No record was built here; the owner should route it to ch 1.

## Topic-only items (no record)
- exams_a#16 (F23): cases on debit/credit.
- exams_a#82 (OLD): «المدين والدائن … من محاضرات ٢ ل ٧».
- exams_a#129 (OLD): «سؤالين تبع من أو إلى».
- exams_a#54 and exams_a#55 (OLD): «سؤالين عن عناصر النظام المحاسبي».

## Items without numbers, credited to existing records (raw id → record)
| Raw id | Record | Added |
|---|---|---|
| exams_b#48 (S24) | Q02-003 | |
| exams_b#156 (S25) | Q02-003 | S25 |
| exams_b#94 (F24) | Q02-004 | F24 |
| exams_b#134 (F24) | Q02-004 | F24 |
| exams_b#90 (F24) | Q02-008 | F24 |
| exams_b#131 (F24) | Q02-008 | F24 |
| exams_a#30 (F23) | Q02-002 | F23 |
| exams_b#93 (F24) | Q02-015 | |
| exams_b#112 (F24) | Q02-016 | |
| exams_b#91 (F24) | Q02-017 | |
| exams_b#132 (F24) | Q02-017 | |

## Items taken from out_of_scope.json (the ch-2 page that teaches the entry)
- exams_b#56 (S24, bank loan) → Q02-004. See the caveat below.
- exams_b#94 and exams_b#134 (F24, loan, no numbers) → Q02-004.
- exams_a#30 (F23, purchase returns) → Q02-002. Taught on p. 80 and p. 74.
- exams_b#151 (S25, cash/bank at year end) → Q02-005. Taught on pp. 60–61.
- summary#54 → Q02-009, as an also-asked-as line. Taught on pp. 55–56.
- summary#42 (loan) → Q02-004, as a variant.
- summary#41 (machine bought on account) → Q02-034. Taught on p. 72 and p. 66.
- summary#60 (discount granted) → Q02-044. Taught on p. 80.
- summary#61 (interest added by the bank) → Q02-046. Taught on pp. 77 and 81.

**Caveat, loan entry (Q02-004):** no ch-2 page shows a loan entry. The answer is derived from two things on ch-2 pages:
- loans are liabilities, which increase on the credit side (p. 50, p. 60);
- borrowing is not revenue (p. 55).

Q02-004 carries this in its notes. The owner decides whether it stays.

## Disagreements between a source's marked answer and the book
| Raw id | Their answer | Book's answer | Page |
|---|---|---|---|
| exams_b#4 (S24, circulated AI key) | أ «مردودات المشتريات مدين» | «كل ما سبق خاطئ» | p. 80: من ح/ الموردين إلى ح/ مرد. المشتريات |
| exams_b#3 (S24) | Key 4800000, disputed by students | 4800000 kept | p. 59: the extended equation puts expenses, and so purchases (p. 69), on the debit side |
| exams_a#10 (S23) | Students split between أ/ب and ج | ج | pp. 60–61: asset balances are always debit |
| book#14 (p. 81 T/F 3) and summary#13 | صح | خطأ | See the book error below |

For exams_b#3, leaving purchases out gives 4320000, which would make the answer «كل ما سبق خاطئ».

## Book errors confirmed (from the page images)
1. **p. 59:** «مصادر التمويل (حسابات مدينة) / أوجه استخدام الأموال (حسابات دائنة)» is reversed. p. 60 makes liabilities, equity and revenues credit, and p. 61 names the liabilities side «منشأ الأموال». This is the cause of the **p. 81 T/F 3** tick on صح, which is wrong.
   - Q02-020 answers خطأ. It carries `book_says`, `sci`, and `low_conf`, because the exam key may follow the book's tick.
2. **p. 80, case entry of the 6th:** «شراء تجهيزات المحل» is booked «من ح/ المشتريات» with the narration «شراء بضاعة بشيك». Equipment is a non-current asset (p. 48, table p. 69).
   - Q02-030 uses ح/ التجهيزات and carries `book_says`, `sci` and `low_conf`.
3. **p. 68 worked example:** machines are printed as 5000, but the text on p. 67 says 50000. The text also has the typo «الإبحار» for «الإيجار». This worked example is not a question, so it is not in the bank.

## Other flags
- **Q02-013:** qa lists it under "synonym-looking option pairs". The options are journal entries that differ only in the account (المصرف vs الصندوق, debit vs credit), so they share words by nature; they are not synonyms.
- **Q02-013 (OLD computer entry):** the recall has no numbers, so it uses the book's p. 68 example data (25000 total, 10000 by cheque). The student recalled that every option used الصندوق, which would be wrong for a payment by cheque. This is noted.
- **Q02-037 (dollar account, p. 73):** the text does not say where the lira came from, hence `low_conf`.
- **Q02-038 (purchase discount, p. 74):** the entry follows the p. 80 pattern. The p. 73 heading names «الحسم المكتسب», and the record says «مستنتج».

## Pages rendered and read visually
- Rendered for this run: 8 pages (59, 60, 64, 66, 68, 69, 70, 73). Opened: 59, 68, 69, 70 and 73. Pages 60, 64 and 66 were rendered but not opened, because their text layer is clean.
- Pages 80 and 81 were opened from the renders made in stage 3.
- The rest of the chapter was read from the text.

## Could not verify
- The F24 recalled options for the rent question were one-sided, and their exact wording is not recorded.
- The S23 loan question's options were not recalled; they were reconstructed.
