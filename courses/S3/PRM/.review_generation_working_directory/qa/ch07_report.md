# Chapter 7 report — تخطيط الزمن في المشروع (الجزء الأول), pp. 238–280

## Counts
| item | n |
|---|---|
| raw items received (`by_chapter/ch07.json`) | 79 (EMAD 37, BOOK 9, EX15 9, S19 8, F24 6, SOUFI-XCHK 3, TATI 2, MURAJA 2, ASEM 2, Y16 1) |
| of which SOUFI-XCHK (cross-check only, not a source) | 3 |
| of which topic-only (no record) | 3 |
| canonical records (real) | 38 |
| generated records | 3 |
| **total records in `bank_ch07.py`** | **41** |
| by type: exam / textbook / other / generated | 14 / 9 / 19 / 3 (a record may carry several types) |
| reconstructed (exam free-form → MCQ/short) | 5 (Q07-009, 010, 011, 012, 013 — all F24) |
| low-confidence | 5 (Q07-003, 005, 006, 012, 013) |

Exam sittings represented: EX15, S19, F24, TATI (Y16 only as a topic pointer).

## Dedup map (raw → record)
| record | raw ids merged |
|---|---|
| Q07-001 SS + Lag (16 days) | recalls#21, #43 (topic dup), #66, #98, #161 (EX15); soufi#120 (S19) |
| Q07-002 what Gantt shows | recalls#37, #87, #162 (EX15); soufi#151 (S19) |
| Q07-004 planning is iterative | soufi#32 (S19); recalls#196 (TATI) |
| Q07-010 milestone chart "except" | recalls#121 (F24); others#232, #233 (EMAD, as variants) |
| Q07-012 AOA vs AON | recalls#143 (F24); others#219, #220, #221, #222 (EMAD, as variants) |
| Q07-015 / Q07-016 book MCQ 1 / 2 | book#80 / book#81 + others#407 / #408 (ASEM confirms both, 2/2 agreement) |
| Q07-029 dependency relationship + four types | others#182, #184 |
| Q07-030 mandatory vs discretionary dependencies | others#183, #186, #188 |
| Q07-034 Lead accelerates the successor | others#191, #193 |

Book MCQs 3, 7, 8, 9, 10 (p.272–274) are not in `ch07.json` (they were assigned to chapter 8: book#82, #86–#89) and are therefore not in this bank.

## The SS + Lag item (Q07-001) — 12 vs 16
Definitions used, p.266 (SS: «يُمكن أن يبدأ النشاط B حالما يبدأ النشاط A … كما يمكن أن يكون هناك فارق أو تأخير زمني Lag في هذا النوع من العلاقات»; figure 7-19 links the START of A to the START of B) and p.267 (Lag = «مدة التأخير الزمني بين نشاطين»). With SS + Lag 4 the successor's START is 4 days after the predecessor's START: A = days 0–6, B = days 4–16, total = 16. "12" only results from ignoring the lag (both start together); "10" is the FS reading (6 + 4 = start of B). The book gives no numeric SS example, but its definitions leave one reading only, so the record is NOT flagged low-confidence; the intra-EX15 conflict (src03 highlights 12, src07 circles 16 with a sketch) is recorded on `other_source` and in `notes`.

## Calculation exercises (kept as essay, answer in words)
| record | data | result |
|---|---|---|
| Q07-021 book essay 2 (p.274–275) | 12 activities A…L | 115 days, critical path A-B-E-H-J-K-L (other paths 58 and 105) |
| Q07-022 book essay 3 (p.275) | 10 activities A…J | 155 days, critical path A-C-E-G-J |
| Q07-023 book essay 4 (p.276, lags) | 8 activities with FS lags + SF C→D 20, SS D→E 5, FF G→F 10 | 70 days, critical chain A-C-(lag 10)-G-(FF lag 10)-F-H; E has 25 days float. The book gives definitions only, no worked solution; 70 holds whether F is stretched or split to satisfy the FF constraint (stated in `notes`). |

## Subsection coverage
| sub | name | real questions | generated |
|---|---|---|---|
| 7-1 | مقدمة | none | Q07-039 (time planning inseparable from time control, p.240) |
| 7-2 | مفهوم التخطيط وعمليته | Q07-003, 004, 005, 006, 015, 020, 024, 025 | — |
| 7-3 | بيان العمل SOW | none (only mentioned inside the sequence MCQ) | Q07-040 (SOW definition, p.243) |
| 7-4 | هيكل تقسيم العمل WBS | Q07-007, 009, 014, 027 | — |
| 7-5 | تقييم منطق المشروع PLE | Q07-016 (+ Q07-008 leans on it) | — |
| 7-6 | الجدول الزمني الأولي DMS | Q07-026 (scheduling stages); critical path used by Q07-021/022 | Q07-041 (float / critical activities, p.252–253) |
| 7-7 | مخطط غانت ونقاط العلام | Q07-002, 010, 022, 028 | — |
| 7-8 | المخطط الشبكي وعلاقات التبعية | Q07-001, 008, 011, 012, 013, 017, 018, 019, 021, 023, 029–038 | — |

Uncovered after generation: none. 3 generated ≤ 38 real; 7-1, 7-3 are non-focus (limit 3 respected); 7-6 had only an "other" question, so one generated MCQ on the float/critical-activity definition was added (book MCQ 7 on the critical path lives in chapter 8's bank, so no duplication of its idea).

## Topic-only items (no record)
| raw id | source | text | points to |
|---|---|---|---|
| recalls#8 | Y16 | Lag / Lead explanation with examples (study note by the group, not a recalled question) | 7-8-3 (covered by Q07-011, 019, 031, 034) |
| recalls#43 | EX15 | نشاطين ستارت تو ستارت بينهم لاك | 7-8-3 (dup of Q07-001) |
| recalls#131 | F24 | سؤال من فقرة تقييم منطق المشروع (ما عم اتذكرو بالضبط) | 7-5 (covered by Q07-016) |

## Unresolved / skipped items
- recalls#45 (EX15): forum question «شو هوي أصغر عنصر في التخطيط؟ Task أم Activity» — marked in the source as not confirmed to have appeared; the book's WBS levels (p.245–246) end at «حزمة العمل» / «مكوّن حزمة العمل» and never oppose Task to Activity, so no record.
- recalls#144 (F24, FF + Lead calculation): numbers not recalled; kept as a reconstructed method question (Q07-013, short, low-confidence) rather than dropped, because the relation type is clear.
- EMAD items skipped (concept absent from this book or unsupported): others#170 (resource planning harder than time planning), #171 (when the schedule is set), #172 (what planning requires: safety, environment…), #175 (duration cannot be estimated easily), #176 (task states), #177 (measuring activities = progress), #178 (every activity has predecessor/successor except first/last), #179 (interrupting activities), #180 (tasks not entered in the schedule), #189 (external dependency: permit six weeks), #192 (no risk from lead), #218 (arrows may cross), #223 (hammock activities). 13 skipped of 37; 24 used (19 records / variants).
- MURAJA others#393 («فوائد التخطيط: تحسين تركيز المنظمة ومرونتها») skipped: the "benefits of planning" list is not in the book.

## Disagreements between a source's marked answer and the book
| record | source | source's answer | book |
|---|---|---|---|
| Q07-001 | EX15 (src03 highlight) | 12 يوم | 16 (p.266–267 definitions); the same sitting's src07 circles 16 |
| Q07-026 | EMAD | steps: WBS → define activities → sequence | book's scheduling stages p.254 (durations → start/end → critical path → replanning → resources → DMS → PMS); EMAD list kept on `other_source` |
| Q07-027 | EMAD | WBS components: project / sub-project / phase / activity-task | book's six levels p.245–246 (program → work-package component) |
| Q07-028 | EMAD | milestones must be "SMARTE" | acronym not in the book (p.257 definition kept) |
| Q07-030 | EMAD | three dependency types incl. "external" | book has mandatory and discretionary only (p.268) |
| Q07-031 | EMAD | Lag = delay of the successor's start | book: delay between two activities in general, applicable to all four relations (p.265–267) — refinement, not a contradiction |

No BOOK highlight contradicts the chapter text (MCQ 1, 2, 4, 5, 6 all verified). ASEM agrees with the book on both of its chapter-7 items (2/2). SOUFI-XCHK (soufi#74–76) agrees with the book on MCQ 4, 5, 6.

## Pages read visually (PNG)
266 (figure 7-19, SS relation; confirms the arrow runs from the start of A to the start of B) and 276 (table of exercise 4 — matches the transcription in the raw notes). All other citations come from the extracted text of pp.239–276 read in full; p.141 (chapter 4) was read in the extracted text for Q07-005.
