# Chapter 4 report — دورة حياة المشروع (pp. 124–163)

Output: `render/bank_ch04.py` (imports cleanly, 44 `Q()` records).

## Counts
| item | n |
|---|---|
| raw items received (`by_chapter/ch04.json`) | 95 |
| raw items used in records | 67 |
| raw items excluded (see below) | 28 |
| canonical records | 44 |
| by type: exam / textbook / other / generated | 22 / 14 / 21 / 0 (a record may carry several types) |
| records with an exam sitting in `exam_sources` | 22 |
| reconstructed (free-form recall → MCQ) | 7 |
| low-confidence | 7 (Q04-005, 008, 009, 011, 012, 030, 031) |
| generated | 0 |
| ASEM cross-check | 1 item, 1 agreement (Q04-025, communication KA) |

Records per source: BOOK 14, EMAD 20, S19 7, TATI 7, F24 5, KIFAH 4, EX15 4, Y16 1, ASEM 1, MURAJA 1.

## Coverage (second-level subsections)
| sub | covered by real questions | generated |
|---|---|---|
| 4-1 مقدمة | Q04-028 (definition of the life cycle, p.126) | – |
| 4-2 مراحل دورة الحياة | 26 records | – |
| 4-3 خصائص المراحل | Q04-014, 015, 016 (p.137–138) | – |
| 4-4 PMI / PMBOK | Q04-017 (process groups), Q04-018 (initiating = charter + stakeholders) | – |
| 4-5 المجالات المعرفية | 12 records (all ten KAs touched) | – |

Uncovered: none at the second level, so no generated questions. Note: third-level topic 4-4-1 (PMI facts: founded 1969, PMBOK updated every four years, PMP/CAPM, p.138–139) has no question; 4-4 is covered only through PMBOK items.

## "In which phase does X happen" — one record per X
| X | phase (book) | pages | record |
|---|---|---|---|
| detailing scope / schedule / budget & costs | التخطيط | 127, 129, 131 | Q04-001 (BOOK + S19) |
| executing the plan, leading the team | التنفيذ | 127, 128, 132 | Q04-002 (BOOK + F24) |
| delivery, evaluation, lessons, "إجمالي المشروع" | الإنهاء | 127, 135 | Q04-003 (BOOK + KIFAH) |
| documentation / archiving | الإنهاء | 129, 135 | Q04-004 (S19 + Y16) |
| writing reports | التنفيذ (performance reporting) — low_conf | 132, 133, 150 | Q04-005 |
| risk estimation | التخطيط | 129, 131 | Q04-006 (EX15) |
| contracting with vendors | التعريف (RFP → evaluate → contract, then planning begins) | 131 | Q04-007 (EX15) |
| training the end user | الإنهاء — concept absent from book, low_conf | 127, 135 | Q04-008 (EX15) |
| "not part of planning" → choosing the contractor | التعريف | 127, 131 | Q04-009 (KIFAH) |
| appointing the project manager | Initiation / التعريف | 127, 139 | Q04-010 (S19 + TATI) |
| when planning is done | after approval / end of initiation | 131, 141 | Q04-011 (TATI) |
| most resources consumed / longest | التنفيذ | 127, 128, 132 | Q04-038 (EMAD) |
| developing the project idea | التعريف | 127, 129 | Q04-044 (MURAJA) |

## Disagreements between a source's marked answer and the book
- **TATI p1 item 6** (Q04-011): source highlights two options (ب and د); book supports ب (planning follows approval, p.131) and also re-planning after approved changes (p.141); د uses PMBOK "scope statement" vocabulary absent from the book → `other_source`, low_conf.
- **MURAJA item 13** ("إعداد جدولة المشروع تكون في مرحلة" → التنفيذ): the book puts scheduling in التخطيط (p.127, 129, 131); the item's four-stage model (فكرة/تنفيذ/تسليم/ما بعد التسليم) has no planning option, so it cannot be verified from the book → excluded, noted in Q04-001 `notes`.
- **EMAD 108** (planning-phase contents): the source's answer is a copy of the charter contents (item 107); answered from the book (Q04-036 notes).
- **EMAD 112** lists "تدريب المستخدم النهائي" in closing; the book's closing list (p.135) does not contain it (recorded on Q04-008 `other_source`).
- **SOUFI-XCHK** (not a source): item 13 highlights الإنهاء for the execution-phase stem (the print offers no التنفيذ option); item 62 has no correct option printed (cost KA missing, option repeated). No effect on the bank.
- BOOK highlights: all 10 MCQ highlights agree with the chapter text (mcq-1…10).

## Excluded raw items (28)
- **SOUFI-XCHK copies of book MCQs** (10): src05 items 9, 10, 11, 12, 13, 14, 60, 61, 62, 63 — not a source per SOURCES.md.
- **Topic only** (4): Y16 line 8b "خطوات بتنتمي لأي مرحلة" (→ 4-2); EX15 para 18 and EX15 p4-19 "عدة أسئلة بأي مرحلة بيصير كذا" (→ 4-2); TATI p9 compiler notes (not a question; its phase claims agree with Q04-006). Y16 line 23 ("توثيق المشروع بأي مرحلة") is fully recoverable and was attached as a source to Q04-004.
- **TATI out of scope** (2): p1 item 1 and p5 item 18 — inputs of the scope / scope-plan process (PMBOK inputs vocabulary; the chapter lists no process inputs).
- **Unresolved / could not be verified** (2): S19 item 49 and TATI p8 item 38 — "Develop Preliminary Project Scope Statement is an Integration process" (marked خطأ). The process does not exist in this book (PMBOK-3 vocabulary); in PMBOK 3 it actually belonged to Integration, so the marked answer is also doubtful. Not banked.
- **KIFAH p1 "تحسين العمليات بشكل مستمر"** (1): maturity-model concept (Optimized level), not in the book.
- **EMAD 113–117** (5): maturity levels AD HOC / Repeatable / Well defined / Managed / Optimized — not in the book.
- **EMAD 118–120** (3): PM-system problems, competitive advantage, resistance to change — not in chapter 4 (nor traceable in it).
- **MURAJA 13** (1): see disagreements.

## Notes on verification
- The book's own 4-phase model (p.127) puts monitoring and control inside execution (p.129, 132–133); the PMBOK 5 process groups (p.139–140) are kept distinct in Q04-017.
- KA names differ between p.141 (الجدول الزمني / الموارد / الاتصالات) and the detailed sections p.147–149 (الزمن / الموارد البشرية / التواصل); records use the section wording that the questions use.
- BOOK essays 3–4 (core vs supporting KAs): the book never splits the ten KAs; answered from the chapter with the conventional split and low_conf.
- Pages read visually (PNG render): none — the extracted text was legible for all cited passages.
