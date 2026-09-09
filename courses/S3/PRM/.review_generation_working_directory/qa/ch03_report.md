# Chapter 3 report — إستراتيجية المنظمة واختيار المشاريع (pp. 82–123; text 84–106)

Output: `render/bank_ch03.py` (imports; `build_bank.check_basic` passes for the chapter alone).

## Counts
| item | n |
|---|---|
| raw items received (`by_chapter/ch03.json`) | 66 |
| canonical records | 32 |
| — type exam | 13 (EX15 5, S19 4, KIFAH 3, F24 3 sittings) |
| — type textbook | 10 (6 MCQ + 4 essay; 2 of them also exam/other) |
| — type other (EMAD) | 15 (10 standalone + 5 merged into exam/textbook records) |
| — generated | 1 |
| real records (non-generated) | 31 |
| reconstructed (exam free-form → MCQ) | 5 (Q03-002, 003, 007, 010, 011) |
| low-confidence | 5 (Q03-003, 006, 007, 012, 013) |
| ASEM cross-check | no ASEM items assigned to ch. 3 |

## Calculation items (book method, p. 93–95, figs 3-3 / 3-4 read visually)
- Q03-001 payback 15 y vs 5 y, bank 15% → choose the 5-year project, reject the 15-year one (shorter payback is better; payback ignores time value; the source's own note "interest rate is there to confuse" agrees).
- Q03-002 payback 5 y vs 8 y, 10% → the 5-year project.
- Q03-003 return 11% vs 30%, rate 20% → accept only the 30% project (project must reach the minimum required rate of return; fig 3-3 accepts A/B because 32.1%/27.5% exceed 15%). low_conf: "العائد" interpreted as rate of return.
- Q03-004 NPV −20000 / −50000 at 15% → reject both (negative NPV = reject).

## Coverage (subsections = second level)
- Covered by real questions: 3-2, 3-3, 3-4, 3-5, 3-6, 3-7.
- Covered by generated only: 3-1 (مقدمة) — Q03-032 on the one concrete statement (open, transparent selection process, p. 84).
- Uncovered: none.
- Note: third-level 3-6-2 (non-financial criteria) is touched only inside essay Q03-020; no separate generated question added because 3-6 is already covered (rule 7).

## Disagreements source vs. book
| record | source | source's answer | book |
|---|---|---|---|
| Q03-005 | S19 (student's red circle) | Project analayes | تحليل الجدوى (Feasibility) p.105 |
| Q03-005 | KIFAH | الجدوى الفنية أو التقنية | book does not split feasibility types; answer = تحليل الجدوى |
| Q03-020 | EMAD | financial feasibility = NPV, IRR, payback | book: payback + NPV only (IRR not explained) → `other_source` |
| Q03-022 | EMAD | top mgmt / steering committee / user dept / technical group | book p.105: الإدارة العليا (priorities), فريق الأولويات (evaluation) → `other_source` |
| Q03-007 | KIFAH (student) | حساب العائد | agrees with book (not a listed problem) |
| Q03-001/002 | EX15 highlights | 5-year project | agrees with book |
No BOOK highlight contradicted the chapter text (mcq 1–6 all verified).

## Unresolved / not recorded
- soufi#95 (S19) "/15 تمثل أفضل معدل عائد على الاستثمار: 55%/66%/25%" — stem garbled in the source, numbers unrecoverable.
- recalls#18 / #79 (EX15) "من التالي لا يؤثر على تصنيف المشروع" — other options not recalled; student's choice (مدير المشروع) reported wrong; book p.92 only says classification is broken down by product type, department and function. Not reconstructable.
- recalls#51 (KIFAH) "طريقة لاستخدام المشاريع.. (أنا حطيت تحليل سلسلة القيمة)" — fragmentary stem; value-chain analysis is absent from the book.
- Topic only: soufi#156 (S19) "value chain analysis كانت الجواب" → no matching subsection (concept absent; nearest 3-7-4/3-6-3); soufi#157 (S19) "اجت payback" → 3-6 (covered by Q03-008/001/002).
- EMAD items skipped (concept not in this book, 16): #74 (ranking methods incl. value chain), #80 technical feasibility, #81 operational, #82 schedule feasibility, #84 value chain, #86 generic "decision models", #87 mathematical modelling, #88 five methods, #89–#91 decision tree / criteria profiling, #92 unweighted profiling, #94–#95 Q-sort, #96 Delphi, #102 IRR rule.
- EMAD items used (15): #71 → merged Q03-019; #72 → Q03-022; #75 → merged Q03-018; #76 → Q03-023; #77 → Q03-024; #78 → Q03-025; #79 → merged Q03-020; #83 → merged Q03-006; #85 → Q03-026; #93 → Q03-027; #97 → merged Q03-008; #98 → Q03-028; #99 → Q03-029; #100 → Q03-030; #101 → Q03-031.
- Concept-absent items kept as exam records with `low_conf` + `book_says`: Q03-006 (political feasibility), Q03-013 (criteria profiling / Q-sorting).

## Pages read visually (PNG)
87 (fig 3-1 + four activities), 94 (payback formula, fig 3-3), 95 (NPV formula and symbols), 104 (fig 3-7 selection flow). All other citations from `ch_fixed/ch03.txt` (pp. 84–106 read in full).
