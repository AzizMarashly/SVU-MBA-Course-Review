# Chapter 1 helper report (ACM v1.0, prompt v0.12)

**Counts.** 41 raw items received. 23 canonical records: 16 mcq (11 real + 5 generated), 6 tf, 0 short, 1 essay. By section:
10 exam (4 of them book cards credited by exam recalls), 8 textbook-only, 5 generated. 6 reconstructed, 3 low-confidence, 0 calc/table/fig/fast/unsolved,
0 see-links, 1 model answer. No METHODS block (theory-only chapter).
`python -c "import bank_ch01"` passes; `PRM_LENIENT=1 python build_bank.py` has no ch 1 assertion (uncovered: 0); `qa_blocks.py` clean for ch 1.

**Coverage (12 units).** Real questions cover 1-2, 1-3, 1-4-1, 1-4-2, 1-5, 1-6-2, 1-7-1. Generated (one each): 1-1 (Q01-019), 1-6-1 (Q01-020;
the essay Q01-018 spans 1-6-1 too but its `sub` is 1-6-2), 1-7-2 (Q01-021), 1-8 (Q01-022), 1-9 (Q01-023). Uncovered: none. 5 generated vs 18 real.

**Dedup.** The 11 SUM items (summary#0–10) are verbatim copies of the book review set: folded as SUM into each book card.
S24 exams_b#23 (same stem, answer قيمة تنبؤية) → variant on the book card Q01-002; S24 exams_b#67 (short form, «تنبؤية أو تأكيدية أو كلاهما») → `also` line there.
No protected verbatim exam item exists in ch 1, so no see-links.

**Number-less / topic-only credits applied** (`~raw` + variant, sitting added to sources/exam_sources):
- ~exams_b#103 (F24), ~exams_b#154 (S25) «فرض الوحدة المحاسبية المستقلة» → Q01-001 (book MCQ 4)
- ~exams_a#48 (F23) «واحد عن التكلفة التاريخية» → Q01-004 (book MCQ 3)
- ~exams_b#20, ~exams_b#21, ~exams_b#47 (S24, two prudence questions, MCQ + T/F, no text) → Q01-003 (book T/F 6); the MCQ form as an `also` line.

**Reconstructed from free-form recalls:** exams_a#4 S23 (Q01-005, not an assumption), exams_a#46 F23 (Q01-006, periodicity), exams_a#47 F23
(Q01-007, materiality), exams_b#22 S24 (Q01-008, inputs), exams_b#84 + exams_b#125 F24 (Q01-009, outputs), exams_a#107 OLD (Q01-010, relevance definition).

**Topic-only, no record:** exams_a#98 (OLD, «two ch 1 theory questions»), exams_b#107 (F24, «مبادئ المحاسبة»), exams_b#117 (F24, «first two questions
from the ch 1 end-of-chapter set», which ones unknown; supports the book cards in general).

**Out of F25 scope:** none (all of ch 1 is in scope).

**Marked answers vs the book.** All 11 book marks (T/F ticks p. 38, MCQ highlights pp. 38–39, checked on the page images) agree with the text except:
- book#9 (MCQ 4, Q01-001): the book highlights د «كل ما سبق», but pp. 17–18 define independence from the **owners** and from **other economic units** only;
  employees are never mentioned. No option matches the text exactly (ب + ج together). Kept the book mark as the answer (the only option containing both),
  text/mark discrepancy on `book_says`, `low_conf` set. Owner may prefer a different treatment.
- Student recalls: exams_b#22 (inputs = data) and exams_b#23 (قيمة تنبؤية) agree with the book. exams_b#67's longer answer is also correct (p. 25).

**Book errors confirmed:** p. 38 T/F 6 prints «بالأرياح» (typo for بالأرباح; same typo on p. 20). Book T/F 3 reuses the definition of the assumptions (p. 17)
under the word «المبادئ» on purpose (answer خطأ) — not an error. No student-reported errata concern ch 1.

**Low confidence (3):** Q01-001 (mark vs text, above); Q01-005 (S23 recaller unsure whether the stem had «ليس»); Q01-007 («تعريف الأهمية النسبية»
may mean the principle, p. 20, rather than the characteristic, p. 26).

**Pages rendered and read visually:** 22 (figure 1-2: inputs/processing/outputs), 38, 39 (answer marks). All other pages read from the clean text layer
(prose only, no tables or numbers in this chapter).

**Could not verify:** the content of the two OLD and F24 topic-only questions; which book items F24 used.
