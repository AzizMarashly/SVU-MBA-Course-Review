# Chapter 5 report — تعريف المشروع، الجزء الأول (pp. 164–203)

Output: `render/bank_ch05.py` (imports clean, 35 records).

## Counts
| item | count |
|---|---|
| raw items received (`by_chapter/ch05.json`) | 51 (6 BOOK, 4 SOUFI-XCHK cross-check only, 10 S19, 1 KIFAH, 3 F24, 9 TATI, 18 EMAD) |
| canonical records | 35 (33 real + 2 generated) |
| by type | exam 15 · textbook 6 · other 15 (3 records carry two types: Q05-005, Q05-011, Q05-012 exam+other) · generated 2 |
| by qtype | mcq 13 · tf 10 · short 9 · essay 3 |
| reconstructed | 4 (Q05-004, Q05-012, Q05-014, Q05-015) |
| low-confidence | 7 (Q05-002, 006, 007, 008, 009, 014, 025) |
| generated | 2 (Q05-034 → 5-1, Q05-035 → 5-3) |

## Coverage (§9)
- Covered by real questions: 5-2 (10), 5-4 (15), 5-5 (6), 5-6 (2).
- Covered by generated only: 5-1 (مقدمة — its one concrete statement: unclear/unrealistic/unagreed/unwritten definition → trouble before start, p.166), 5-3 (problem/opportunity definition procedures, p.176).
- Uncovered: none.

## Merges (dedup)
- Q05-001 = soufi#14 (S19 15) + recalls#187 (TATI 11, negative form) + recalls#199 (TATI 23).
- Q05-002 = soufi#19 + recalls#177; Q05-003 = soufi#22 + recalls#182; Q05-009 = soufi#30 + recalls#193; Q05-010 = soufi#44 + recalls#210; Q05-013 = soufi#46 + recalls#212.
- Q05-011 = soufi#34 + recalls#200 + others#144 (EMAD boundaries).
- Q05-005 = recalls#209 (TATI) + others#140 (EMAD "المشكلة التي يحلها المشروع → مبررات").
- Q05-012 = recalls#110 (F24 "تعريف متطلبات المشروع") + others#142.
- Q05-027 = others#134 + others#143; Q05-029 = others#136 + others#137.

## Unresolved / skipped
- others#138 (EMAD 140: "حجم وثيقة بيان المشروع يتعلق بـ…") — concept not in the book; skipped (EMAD rule).
- others#135 (EMAD 137, scope-management definition) — the defining sentence is in chapter 4 (p.146, §4-5-2), not chapter 5; kept as Q05-028 under 5-4 with p.146 cited and a note, because the item was routed here and no other helper receives it.
- Topic-only items: none in this chapter's file.
- Exam items on PMBOK vocabulary absent from the book, kept with `low_conf` + `book_says`: Q05-006 (OPA), Q05-007 (EEF), Q05-008 (inputs of scope planning), Q05-009 (output of "خطة إدارة النطاق").
- recalls#115 (F24 "المشاريع المقادة بالتغيير") had `sub_guess` 5-3; the book puts the project types under 5-5 (p.182) → filed under 5-5.

## Disagreements between a source's marked answer and the book / this review
| record | source says | this review | basis |
|---|---|---|---|
| Q05-006 | S19 (student highlight): صح | خطأ | book has no definition of OPA (only listed p.284); PMBOK definition contradicts the statement → `low_conf`, `other_source` |
| Q05-007 | S19 (student highlight): خطأ | صح | same: PMBOK definition of EEF matches the statement → `low_conf`, `other_source` |
| Q05-008 | S19 (student highlight): بنية تقسيم العمل | خطة إدارة المشروع | book: scope statement is the output of scope definition (p.177) and the WBS is built afterwards (p.166); WBS cannot be an input → `low_conf`, `book_says`, `other_source` |
| Q05-023 | EMAD: مدير المشروع | مدير المشروع أو الجهة الراعية (المدير غالباً) | p.167 — partial agreement, recorded on `other_source` |
- BOOK highlights (mcq 1–4, p.189) all verified correct against pp.177–187. SOUFI-XCHK marks (soufi#63–66) agree with the book on all four; not added as a source.
- ASEM: no ch-5 items in the routed file (0 cross-checks).
- TATI highlights (items 2, 7, 17, 24, 33, 34, 36) all agree with the book; TATI 11/23 carried no highlight.

## Pages
- Text read: 164–191 in full (ch05.txt), plus the four case studies pp.192–203 (English, no questions taken); p.146 (ch04.txt) for the scope-management definition; p.284 (ch08.txt) for the only mention of EEF/OPA.
- Read visually (PNG): 167 (contract features), 169 (figure 5-1 charter elements), 186 (figure 5-4, constrain/enhance/accept), 187 (figure 5-5 priority matrix: Performance = Constrain, Time = Enhance, Cost = Accept).
