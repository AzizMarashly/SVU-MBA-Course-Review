# Chapter 11 report — البنية التنظيمية للمشاريع (pp. 400–439)

File: `render/bank_ch11.py` (imports cleanly, all `Q()` asserts pass).

## Counts
| item | count |
|---|---|
| raw items received (`by_chapter/ch11.json`) | 66 |
| canonical records | 33 (30 real + 3 generated) |
| by type (a record may carry several) | exam 9, textbook 9, other 16, generated 3 |
| by qtype | mcq 24, essay 4, short 3, tf 2 |
| reconstructed | 6 (Q11-002, 005, 009, 022, 026, 027) |
| low-confidence | 7 (Q11-003, 004, 005, 008, 009, 028, 030) |
| generated | 3 (Q11-031, 032, 033) |

Exam sources present: F24 (2 records), S19 (5), TATI (3, all shared with S19), EX15 (2). No KIFAH or Y16 record survived (see below).

## How the 66 raw items were used
- BOOK 9 items (5 MCQ + 4 essay) → 9 records (Q11-001 merged with F24; Q11-010..017).
- SOUFI-XCHK 8 items (#107–#113) → not a source. #107/#108/#108b/#109 agree with the book highlights. #110–#113 are odd-one-out MCQs on pure-project advantages/disadvantages and matrix characteristics/disadvantages that are NOT in this book's review section (only 5 MCQs, pp. 422–423); they informed the choice of the three generated questions but were not used as sources.
- S19 6 items → 5 records (soufi#25, #31, #55(+src06 #146 dup), #97, #99); soufi#98 out of scope (below).
- TATI 4 items → 3 merged into the S19 records (#10, #19, #45); p1 header is topic-only.
- F24 2 items → Q11-001 (merged with BOOK MCQ 3), Q11-002.
- EX15 3 lines → Q11-008 (recalls#93 + #168 = same sitting, counted once), Q11-009 (recalls#42, garbled).
- KIFAH 1 item → unresolved (below). Y16 1 item → topic only.
- EMAD 25 items → 13 used: 9 own records (Q11-018, 019, 022, 024, 025, 026, 027, 029 + merged into Q11-002, 015, 016, 023); 8 merged as variants (#337→Q11-015; #339, #341, #345, #346, #349, #354, #355→Q11-016; #343/#344→Q11-023; #340→Q11-019; #353→Q11-002); 4 skipped as unsupported by the book (#333 OBS definition, #334 goals of a structure, #336 challenges of organising projects, #350 «شكل الاتصالات شبكية»); 1 topic pointer (#356).
- MURAJA 6 items → 5 records (Q11-020, 021, 023, 028, 030); #15 (others#397, «بيئة عمل أكثر انفتاحاً» as a characteristic) skipped: no supporting sentence in the book.

## Coverage (subsections = audit unit)
| sub | covered by real questions | generated |
|---|---|---|
| 11-1 مقدمة | Q11-014 (book essay 1) | — |
| 11-2 أنواع الهياكل | Q11-010, 015, 016 | — |
| 11-3 الوظيفي | Q11-001, 011, 012, 018, 019, 020, 021 | — |
| 11-4 المشاريعي | Q11-008, 013, 022, 023 | Q11-031 (advantages), Q11-032 (disadvantages) |
| 11-5 المصفوفي | Q11-002, 005, 006, 009, 024, 025, 026, 027, 028 | Q11-033 (reporting channels, 11-5-2) |
| 11-6 اختيار الهيكل | Q11-003, 004, 007, 017, 029, 030 | — |

All six subsections are covered by real questions; uncovered: none. The 3 generated items fill third-level topics (11-4-2, 11-4-3, 11-5-2) that no real question tests and that the SOUFI-XCHK circulating items show are asked in this odd-one-out form. 3 generated ≤ 30 real.

## Topic-only items (no record)
- recalls#2 (Y16): «شي 5 أسئلة عن أنواع المنظمات» → 11-2.
- recalls#175 (TATI header): «5 أسئلة عن أنواع التنظيمات، المصفوفي والشبكي، مسألة إيفا ومسألة مسار حرج» → 11-2 (EVA/CPM belong to other chapters).
- others#354 (EMAD #356): «سلايد مقارنة بعد مساوئ البنية المصفوفية» → 11-5.

## Out of scope (network organisation, not in this book)
- soufi#98 (S19 #99): «مجموعة علماء ينتمون لعدة مؤسسات يعملون لتطوير دواء جديد» (وظيفي/مشاريع/مصفوفي/شبكي; red circle on مشاريع). The crux (several institutions) is the network/virtual organisation; removing it leaves no answerable book question, so no record.
- soufi#55 / soufi#146 / recalls#221 («تدعم المشاريع التي تشترك بها أكثر من مؤسسة») were kept ONLY after rewording to «أكثر من قسم وظيفي» (Q11-005, reconstructed, low_conf, original text preserved). Option «شبكي» replaced by PMO there; in Q11-003, 004, 007 the option «شبكي» is kept because the source options are kept verbatim and the item itself is not about the network type (notes flag it).

## Unresolved
- recalls#62 (KIFAH p3): «يجري العمل في المشاريع في أي مستوى في المنظمة» (student: «داخل وخارج الأقسام»). The chapter has no statement about the organisational level of project work; cannot be verified → no record.

## Disagreements between a source's marked answer and the book
- None where the book settles the matter. Book highlights of all 5 review MCQs agree with the chapter text (pp. 402, 405–406, 410). ASEM has no ch11 items in the raw file.
- Partial support only (kept with `low_conf`/`book_says`): MURAJA #2 «وحدة الهدف وتقليل الصراعات» (book: conflicts resolved more easily, p.417); MURAJA #10 «تحديد المهام الأساسية» criterion (book p.419 gives only nature of work and number/size of projects); EX15 «تحفيز أعلى» → pure project (book never says «تحفيز»); S19 «مجموعة باحثين» → مصفوفي (book silent; could also be read as functional).
- EMAD #357 lists many selection criteria (importance, resources, size, environment, budget); the book (p.419) only names nature of work and project volume — EMAD kept as variant, book answer used (Q11-029).
- SOUFI-XCHK #112 marks the reversed weak/strong statement as «not a characteristic», consistent with the book (p.416); #111 marks «القادة متعددون» as not a disadvantage, consistent with the book's «نادرين» (p.411).

## Pages read visually (PNG)
- p.419 (text garbled in the extraction; selection criteria confirmed), p.420 (Figure 11-4 table: PM authority little/none → limited → low → moderate → high; % full-time staff; PM role part-time/full-time). p.416 rendered but the extracted text was already legible.
