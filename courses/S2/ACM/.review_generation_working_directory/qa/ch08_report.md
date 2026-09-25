# Chapter 8 helper report (ACM v1.0, prompt v0.12, F25 theory-only)

Output: `render/bank_ch08.py`. `import bank_ch08` passes. `PRM_LENIENT=1 build_bank.py` gives no assertion or warning for ch 8.
`qa_blocks.py` has no ch 8 findings: every block is 40+ words, no why repeats the answer, no calc-why arithmetic, no missing symbols.

## Counts
- Raw items received: 53. Records: **27**.
  - 12 exam
  - 10 textbook (T/F 1–5, MCQ 1–5, each merged with its SUM copy)
  - 5 generated
- By form: 22 MCQ, 5 T/F.
- Reconstructed: 10 (Q08-001…008, 010, 012).
- Low confidence: 1 (Q08-006).
- `book_says`: 1 (Q08-021). `other_source`: 1 (Q08-011).
- Calc blocks: 3 (Q08-005, 006, 007). Tables: 2 (Q08-005, 007).
- None of these: fig, fast, unsolved, METHODS (no two records share a method), see-links (no book item and exam item share a claim).
- Added 12 symbols to `meta_acm.py` SYMBOLS: EBT, TR, Tax, NS, EPS, NIC, DL, NDL, ORG, DIV, RNT, INT.

## Coverage (17 units)
- **Covered by real questions (12):** 8-2-1, 8-2-2, 8-2-3, 8-2-4, 8-2-5-1, 8-2-5-2, 8-2-5-3, 8-3-1, 8-3-2-1, 8-3-3, 8-4-2, 8-4-3.
- **Covered by generated questions (5):**
  - 8-4-1 and 8-4-4: mentioned but not asked (in the Q08-001/008 distractors and the Q08-022 explanation).
  - 8-1, 8-3-2-2, 8-3-4: not covered at all. These are the 3 allowed per chapter, in book order.
- Uncovered: 0. The build lists 8-2-5-3 and 8-3-1 as focus areas.

## Out of F25 scope (no record)
- book#63, book#64: Cases 1 and 2, full direct and indirect cash-flow statements (pp. 272–282).
- book#65: Case 3, full multi-step income statement plus EPS. EPS can only be reached through the full preparation.
- book#66: Case 4, full statement of financial position.
- exams_b#111 (F24, no numbers): gross profit from opening and closing inventory. This needs COGS (the deleted ch 5) and multi-step preparation. The sitting's recall disputes it anyway («ما اجا بضاعة اول واخر المدة»).

## Recalls without numbers, credited to records (§5c)
- OLD EPS type (~exams_a#103, ~#73, ~#97) → **Q08-005**.
- OLD other / non-operating revenues type (~exams_a#104, ~#74, ~#117) → **Q08-007**.
- **Decision for the owner:** no record of either type existed, so I built one each from the book's worked example data: p. 249 (EPS 75) and pp. 252–255 (other revenues 480,000). I followed the ch 10 "chart without numbers uses the book's example" precedent, and the stem and notes say so. If you want the strict "numberless creates no record" rule, drop both records. They carry only `~` raws.
- Topic-only recalls, used only as `~` credits and variants on Q08-010 (uses of the SFP):
  - ~exams_b#83 (F24 «المرونة النقدية»)
  - ~exams_a#110 and ~#111 (OLD «الملاءة المالية وجماعتها سؤالين»)

## Topic-only (no record, no credit)
- exams_a#112 (OLD «سؤال نظري على قائمة المركز المالي»)
- exams_a#113 (OLD «سؤال عن قائمة الدخل»)
- These duplicates were folded into their records as raw ids: exams_b#45 → Q08-011, #141 → Q08-011, #142 → Q08-009, #121 → Q08-012, #144 → Q08-002.

## Where a source's answer disagrees with the book
- **book#61 (MCQ 4, p. 288):** the book highlights «د) كل ما سبق خاطئ». Its own text on p. 261 lists retained earnings under equity, so the answer is أ «الأرباح المحتجزة». Recorded as `book_says`; no low_conf, because p. 261 states it.
- **exams_b#27 (S24):** the student answered «خلال الدورة التشغيلية». The book (p. 261) says within a year or the operating cycle, whichever is longer. Recorded as `other_source` on Q08-011.
- All other book ticks and highlights agree with the text: T/F 1 خطأ, 2 صح, 3 خطأ, 4 خطأ, 5 صح; MCQ 1 ج, 2 د, 3 ب, 5 ج. The SUM T/F keys agree too.

## Book errors confirmed
1. **p. 288, MCQ 4:** wrong highlight (see above).
2. **p. 255:** EPS is printed as 960,000 ÷ 4,000 = **249**. The correct figure is **240**. No record uses it.
3. **p. 257, footnote to the discontinued-operations example:** it prints 200,000 × 20% = 40,000 and 24,000 × (100/80) = 300,000. Neither matches the table on p. 256 (160,000 and 240,000; net 1,600,000; 18,400,000). Noted on Q08-006.
4. **p. 256:** the losses are said to be «متضمنة الضريبة», yet tax is then deducted from them. This is an inconsistent wording.
5. From the stage-3 report, not re-checked here (the cases are out of scope):
   - Case 2: the 2019 land figure and the company name.
   - Case 3: sales freight 18,000 in the data vs 7,500 + 10,500 in the solution.
6. **p. 262, flagged by students (investment classification):** "held for sale" investments are listed under long-term investments, and the purpose wording is garbled («بغرض من الأرباح والفوائد»). No record depends on it, and no generated question uses that paragraph.
7. «أو استثنائية» (MCQ 1) is a book typo. The option is shown as «استثنائية», and the notes say so.

## Low confidence
- **Q08-006 (S24, discontinued-operations net income):** the recall does not say whether the 8,000,000 loss is before tax.
  - The book's method (p. 256) treats it as before tax, which gives 13,600,000.
  - If the loss is after tax, the answer is 12,000,000.
  - The figure itself may really be 800,000, as in the book example.

## Pages
- Rendered and read visually: 250, 255, 256, 257, 287, 288.
- I rendered 250, 255, 256, 257 and 262 (262 was not opened: its text layer is prose). 287 and 288 already existed.
- All other pages were read from the text layer: 244–271, 276–277, 289, plus summary pp. 21–24.

## Could not verify
- The exact data of the S24 discontinued-operations item (Q08-006).
- The missing fourth S24 option for current assets.
