# Chapter 2 report — مقدمة في إدارة المشاريع، الجزء الثاني (pp. 50–81)

Output: `render/bank_ch02.py` (imports cleanly, Q() asserts pass).

## Counts
| item | n |
|---|---|
| raw items received (`by_chapter/ch02.json`) | 57 |
| canonical records | 25 |
| by type — exam / textbook / other / generated | 13 / 7 / 11 / 0 (a record may carry several types) |
| by qtype — mcq / tf / short / essay | 17 / 2 / 4 / 2 |
| reconstructed (free-form exam recall → MCQ) | 5 (Q02-002, 003, 010, 012, 013) |
| low-confidence | 4 (Q02-004, 006, 012, 025) |
| generated | 0 |

Ordering of ids: exam Q02-001…013 → textbook Q02-014…019 → other Q02-020…025.

Exam-sitting coverage: F24 3 items, S19 6, TATI 4 (all shared with S19), EX15 2, KIFAH 2, Y16 0.

## Deduplication (raw → record)
- Q02-001 ← book#5 (BOOK mcq-6) + recalls#101 (F24 item 1, only the answer recalled). soufi#4 (SOUFI-XCHK) agrees, not a source.
- Q02-002 ← recalls#105 (F24). Q02-003 ← recalls#104 (F24).
- Q02-004 ← soufi#24, soufi#53 (S19, same sitting counted once) + recalls#185, recalls#219 (TATI).
- Q02-005 ← soufi#26, soufi#50 (S19) + recalls#188, recalls#216 (TATI).
- Q02-006 ← soufi#41 (S19) + recalls#207 (TATI, no highlight).
- Q02-007 ← soufi#42 (S19) + recalls#208 (TATI). Q02-008 ← soufi#101, soufi#149 (S19). Q02-009 ← soufi#104 (S19).
- Q02-010 ← recalls#38 (EX15 statement). Q02-011 ← recalls#86 + recalls#156 (EX15, two copies of the same list).
- Q02-012 ← recalls#54 (KIFAH) + others#46 (EMAD essay, older-curriculum answer on `other_source`).
- Q02-013 ← recalls#55 (KIFAH) + others#52, others#54 (EMAD, as variants).
- Q02-014 ← book#6 + others#403 (ASEM). Q02-015 ← book#7. Q02-016 ← book#8 + others#404 (ASEM). Q02-017 ← book#9 (soufi#7 agrees).
- Q02-018 ← book#12 (essay-3). Q02-019 ← book#13 (essay-4) + others#56 (EMAD variant).
- Q02-020 ← others#53. Q02-021 ← others#61 + others#63 (variant). Q02-022 ← others#62. Q02-023 ← others#47. Q02-024 ← others#69. Q02-025 ← others#67.

BOOK items routed here (mcq-6,7,8,9,10, essay-3,4) are printed twice in the book — chapter-1 review (p.40–42) and, verbatim, chapter-2 review (p.73–75); each record's `notes` says so and the `pages` cite the chapter-2 body pages where the content lives.

## Coverage (second-level subsections)
| sub | name | covered by real questions | generated |
|---|---|---|---|
| 2-1 | نجاح وفشل المشروع | Q02-003, 011, 012 | — |
| 2-2 | مدير المشروع | Q02-002, 006, 017, 022 | — |
| 2-3 | ما هي إدارة المشاريع؟ | Q02-013, 020 | — |
| 2-4 | أهداف إدارة المشاريع (مفاضلة المثلث، المهارات، البرمجيات، الفوائد، التحديات) | Q02-001, 004, 009, 010, 014, 015, 018, 019, 021 | — |
| 2-5 | أصحاب المصلحة | Q02-005, 007, 008 | — |
| 2-6 | تاريخ إدارة المشاريع | Q02-016, 023, 024, 025 | — |

Uncovered: none at the audit level, so no generated questions were written. Third-level gaps worth knowing: 2-4-3 برمجيات إدارة المشاريع (p.63) and the sponsor's duties in 2-5-2 (p.66–67) have no question of their own (the sponsor appears only as a distractor in Q02-002/008/024).

## Disagreements between a source's marked answer and the book
- others#69 (EMAD): "معهد إدارة المشاريع → الثمانينات". Book p.70: PMI and APM were founded in the late 1960s; the 1980s are the PC era (p.71). Book wins → Q02-024 ans "أواخر الستينيات", `other_source` records EMAD's answer.
- others#67 (EMAD): Gantt chart "1917, WWI". Book p.69 says only "بدايات القرن العشرين" — not a contradiction, noted on `other_source` of Q02-025 and flagged low-confidence.
- others#46 (EMAD): approaches that improve success = socio-technical / knowledge-management / project-management approaches. Not in this book; the book's answer is نهج الحس السليم (p.54–55). Kept on `other_source` of Q02-012.
- No disagreement between the BOOK highlight and the chapter text for any of the 5 book MCQs. ASEM agrees with the book on both items it reproduces here (2/2). SOUFI-XCHK agrees on its three copies (soufi#4, #6, #7); soufi#6 carries an extra fifth option not in the book.

## Low-confidence items and why
- Q02-004: "الوقت هو العامل الأقل مرونة" — S19 and TATI agree, but the phrase is absent from the book (grep of all 14 chapters); p.60 only calls time and money "موارد حرجة ونادرة" (`book_says`).
- Q02-006: PM traits — the book does not list them; p.56 rules out only option ج (wide technical knowledge). Options ب/د (analytical / systems approach) come from the older curriculum (EMAD's "المنظور المنظومي"), not in this book.
- Q02-012: KIFAH recall is vague and the student did not know the answer; the book's five-part common-sense approach is the only supported answer.
- Q02-025: Gantt dating rests on one passing sentence (p.69).

## Unresolved / skipped raw items
Topic only (no recoverable question), per brief not recorded:
- others#44 (EMAD) "مليون سبب لفشل المشاريع — السلايد 5" → sub 2-1 (p.52–54 lists failure causes and the ten danger signs).
- others#45 (EMAD) "مليون سبب لنجاح المشاريع" → sub 2-1.

EMAD items skipped because the concept is not in this book (older curriculum), 8 items:
- others#55 (better to train an engineer in management than a manager in engineering), #57 (project cannot work isolated from the organisational environment — belongs to the organisation-structure chapter, not supported by ch.2 text), #58 / #59 / #60 (المنظور المنظومي، أبعاد نظام الإدارة), #64 / #65 / #66 (constrain / enhance / accept exercise), #68 (IBM first commercial user of PM).

Wording issues handled: book#5 option "الزبزن" → written "الزبون" with the typo noted; book#7 "ومدرايريهم" → "ومديريهم" noted; recalls#55 (KIFAH) options were English and the third truncated ("soci....") — kept the two legible ones and completed with chapter terms; recalls#86 has only three recalled options, kept as-is.

## Pages read
Text (ch02.txt): 50–81 in full. Rendered and read visually: 53 (figure 2-1 success criteria — content is an image, not in the text), 56 (project-manager paragraph used by Q02-002/006/017/022), 60 (triangle and diamond wording), 66 (stakeholder definition and sponsor). Whole-book grep for «مرونة», «منظومي», «النظامي», «تحليلي», «1917», «IBM» to test the EMAD/S19 claims above.
