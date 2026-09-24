# Consolidation log — PRM v1.4 (2026-09-24, IDEAS I-10 / I-11)

Whole-bank pass over v1.3 (454 records), after the owner-approved read-only investigation on v1.2 (judged groups and
all flagged pairs: union rule stem ≥ 0.40 or full ≥ 0.40 or bold ≥ 0.45). The 12 F25 records of v1.3 were re-checked
with the same rule: 16 flagged pairs involve them, all judged class c (related, different claim or different data), none merged.
The mechanism lives in `render/build_bank.py` (`MERGES`, `FOLDS`, `GROUPS_EXTRA`); chapter files keep every record,
the build drops the merged ones and turns their ids into aliases (old `#Qxx-yyy` anchors resolve on the page).

Result: 454 → **419** questions (8 new merges + 27 folds; the 4 stage-5 merges of v1.0 are unchanged).

## Answer conflict (settled first)
Q04-011 (TATI, keyed ب «انتهاء مرحلة إطلاق المشروع») and Q07-003 (S19, keyed د «عند الانتهاء من إعداد وثيقة بيان نطاق
المشروع»): same stem and options. Book p.178: «قبل أن يتمكن مدير المشروع من بدء عملية التخطيط، فإنه يحتاج إلى تعريف فهم مشترك…»,
i.e. the project scope statement (p.177: «ينتج عن تعريف نطاق المشروع وثيقة تُدعى بيان نطاق المشروع … من أجل تخطيط المشروع»);
p.244: precise scope definition precedes the schedule and budget. Both raw sources mark د (soufi#16 highlight; recalls#181 highlights
ب and د). Outcome: key **د**, one record Q07-003 (Q04-011 = alias). Low confidence **kept**: p.131 also makes detailed planning the
phase that follows project approval (supports ب) and p.141 says changes require more planning (supports أ). The v1.3 low-conf
reason on Q04-011 («بيان النطاق» not in the book) was wrong and is gone.

## Merges and folds
| Dropped id (form, sources) | Kept id (form) | Class | Claim / reason | Pages of the kept record |
|---|---|---|---|---|
| Q04-011 (MCQ, TATI) | Q07-003 (MCQ) | a (merge → variant) | planning starts once the project scope statement is ready (p.178); key settled from the book | 131, 141, 177, 178, 241, 243, 244 |
| Q09-006 (MCQ, TATI) | Q08-009 (MCQ) | a (merge → variant) | critical path X4-X3-X6-X7 of the X1..X8 table (TATI sub-question also counted in Q08-009/Q08-013) | 298, 300, 301, 344 |
| Q09-007 (MCQ, TATI) | Q08-007 (MCQ) | a (merge → variant) | LF(X3) = 11 of the X1..X8 table (TATI sub-question; its ES(X5) part is Q08-014) | 297, 300, 344 |
| Q02-008 (MCQ, S19) | Q14-001 (MCQ) | a (merge → variant) | the final output is handed over to the customer (S19) | 67, 524, 528, 529, 530 |
| Q04-035 (short, EMAD) | Q05-024 (essay) | a (merge → variant) | contents of the project charter (EMAD, two wordings) | 129, 130, 169, 170, 171, 172, 173, 174, 175 |
| Q12-005 (MCQ, S19) | Q04-006 (MCQ) | a (merge → variant) | risks are identified and estimated in the planning phase | 129, 131, 445, 449 |
| Q08-018 (MCQ, S19) | Q08-017 (MCQ) | a (merge → variant) | the critical path is the longest path, which fixes the shortest completion time | 283, 298, 301, 314 |
| Q03-002 (MCQ, EX15) | Q03-001 (MCQ) | a (merge → variant) | payback: the shorter period wins, the interest rate plays no part (one EX15 item recalled with two data sets) | 93, 94 |
| Q08-044 (short, EMAD) | Q08-021 (MCQ) | a (other form → also asked as) | shortening the duration at least extra cost = crashing | 304, 307, 308 |
| Q06-014 (short, EMAD) | Q06-004 (MCQ) | a (other form → also asked as) | the document / process that breaks the work into detailed tasks = WBS | 206, 211, 212 |
| Q02-010 (MCQ, EX15) | Q02-001 (MCQ) | b (fold → also asked as) | the three linked project variables are time, cost and performance/quality | 56, 59, 60 |
| Q02-021 (short, EMAD) | Q02-001 (MCQ) | b (fold → also asked as) | the three linked project variables are time, cost and performance/quality (scope) | 56, 59, 60 |
| Q03-028 (TF, EMAD) | Q03-001 (MCQ) | b (fold → also asked as) | payback ignores the interest rate / time value of money | 93, 94 |
| Q03-029 (TF, EMAD) | Q03-001 (MCQ) | b (fold → also asked as) | payback: the shorter period is better | 93, 94 |
| Q03-031 (TF, EMAD) | Q03-004 (MCQ) | b (fold → also asked as) | negative NPV -> reject | 94, 95 |
| Q03-030 (TF, EMAD) | Q03-017 (MCQ) | b (fold → also asked as) | NPV = discounted net cash flows minus the initial investment | 94, 95 |
| Q03-026 (short, EMAD) | Q03-027 (TF) | b (fold → also asked as) | weighted scoring model: weight x score per criterion, then sum | 98, 99, 100 |
| Q04-034 (short, EMAD) | Q04-024 (MCQ) | b (fold → also asked as) | definition phase: need, vision, goals, team, scope, charter | 127, 129, 130, 131 |
| Q04-044 (MCQ, MURAJA) | Q04-024 (MCQ) | b (fold → also asked as) | definition phase: developing the project idea | 127, 129, 130, 131 |
| Q04-036 (short, EMAD) | Q04-001 (MCQ) | b (fold → also asked as) | planning phase: scope detail, activities, schedule, budget, risks -> baseline plan | 127, 129, 131, 132 |
| Q04-037 (short, EMAD) | Q04-002 (MCQ) | b (fold → also asked as) | execution phase: carry out the plan, lead the team, monitor and control | 127, 128, 132, 133, 135 |
| Q04-040 (short, EMAD) | Q04-003 (MCQ) | b (fold → also asked as) | closing phase: handover, evaluation, lessons learned | 127, 128, 135, 136 |
| Q04-015 (short, EX15/KIFAH) | Q04-014 (TF) | b (fold → also asked as) | a product life cycle can contain one or more projects | 126, 138 |
| Q05-028 (TF, EMAD) | Q04-019 (MCQ) | b (fold → also asked as) | scope management = all the work required and only the work required | 141, 146, 178 |
| Q05-022 (short, EMAD) | Q05-001 (MCQ) | b (fold → also asked as) | the charter authorises the project manager to use organisational resources | 166, 168, 169 |
| Q05-017 (MCQ, BOOK) | Q05-013 (TF) | b (fold → also asked as) | objectives must be realistic: achievable with the available resources and skills | 183, 184 |
| Q06-016 (short, EMAD) | Q06-001 (MCQ) | b (fold → also asked as) | the work package is the lowest WBS element (what / when / cost / who) | 208, 210, 211, 215, 216, 231 |
| Q07-034 (TF, EMAD) | Q07-011 (MCQ) | b (fold → also asked as) | a lead lets the successor start before the predecessor ends | 267 |
| Q07-031 (short, EMAD) | Q07-019 (MCQ) | b (fold → also asked as) | lag = a time delay between two activities (lead = negative lag) | 265, 267 |
| Q08-034 (TF, EMAD) | Q08-025 (MCQ) | b (fold → also asked as) | effort = person-days or person-hours needed for an activity | 285 |
| Q08-042 (short, EMAD) | Q08-041 (TF) | b (fold → also asked as) | fast tracking = doing activities in parallel / overlapped (no extra resources, more risk) | 304, 305, 306, 307 |
| Q09-012 (MCQ, BOOK/EMAD) | Q09-002 (MCQ) | b (fold → also asked as) | resource levelling = cutting the peaks of resource demand | 341, 343, 346 |
| Q10-031 (TF, EMAD) | Q10-001 (MCQ) | b (fold → also asked as) | earned value = budgeted cost of the work performed (BCWP) | 381, 392, 393 |
| Q11-019 (short, EMAD) | Q11-020 (MCQ) | b (fold → also asked as) | in the functional structure the project sits inside one functional department | 403, 404 |
| Q11-025 (short, EMAD) | Q11-005 (MCQ) | b (fold → also asked as) | matrix structure: resources assigned temporarily from the functional departments | 403, 407, 411, 412, 415 |

## Cross-linked (both forms asked in the same sitting, both kept)
| Ids | Claim | Sitting |
|---|---|---|
| Q01-008 (MCQ) ↔ Q01-009 (TF) | cost is a constraint on the project (p.27) | S19 and TATI each asked both forms |

## Rejected candidates (kept as separate records)
| Ids | Why not merged |
|---|---|
| Q12-021 / Q12-025 | different claims: risk management is proactive (p.445) vs the response plan is prepared before the risk occurs (p.457) |
| Q14-016 / Q14-017 | two generated items covering different subsections (14-1 distribution of closure duties, 14-2 who carries out most closure tasks); merging would uncover a subsection |
| Q03-035 (F25) / Q03-004 (S19) | same rule (negative NPV → reject) but different data and a different expected answer (accept A, reject B vs reject both) |
| other F25 pairs (Q02-026/Q02-003, Q12-032/Q12-012, Q11-034/Q11-002, Q09-033/Q09-018, Q12-031/Q12-013/Q12-024, Q03-033/Q03-021, Q01-036/Q01-029, Q04-045/Q01-001, Q02-024) | different claims of the same topic (class c) |

## Table groups (class c, page only; no record changed except Q08-014)
| Group | Members | Shared data |
|---|---|---|
| tbl-Q08-001 | Q08-001…Q08-005 | EX15/Y16 AON network |
| tbl-Q08-007 | Q08-007…Q08-014 (8) | X1…X8 table; Q08-014 moved from TATI's M1…M8 names to X names (same data, M5 = X5; TATI wording kept in `original`/variants) so it joins the group |
| tbl-Q09-003 | Q09-003…Q09-005 | X1…X8 table (levelling) |
| tbl-Q10-005 | Q10-005…Q10-009 | EX15 EVA table |
| tbl-Q10-010 | Q10-010…Q10-014 | S19/TATI EVA table |
| tbl-Q10-020 | Q10-020…Q10-023 | BOOK values BCWS 10 / ACWP 14 / BCWP 12 (`GROUPS_EXTRA`; stems unchanged) |

## F24 credits (I-10, same handling as F25 items 31/32 in v1.3)
| F24 item (raw) | Credited to | Variant |
|---|---|---|
| P5 «مسألة عن المسار الحرج عليها 7 أسئلة» (recalls#148) | Q08-007, Q08-008, Q08-009, Q08-013, Q08-014 | `F24_CPM` (bank_ch08) |
| P4 «مسألة عن Resource leveling عليها 7 أسئلة» (recalls#147) | Q09-003, Q09-004, Q09-005 | `F24_LEV` (bank_ch09) |
| P2 4-activity EVA table, «المتقدم زمنياً والأعلى صرفاً» (recalls#145) | Q10-012, Q10-013, Q10-014 | `F24_EVA` (bank_ch10) |
| P3 «سؤال لازم نحسب فيه SPI» (recalls#146) | Q10-013 | `F24_SPI` (bank_ch10) |
| P1 FF + lead, total time (recalls#144) | already its own record Q07-013 (v1.0, F24, low-conf method question); not changed | — |
Only table-format records were credited: crediting P3 also to the book questions Q10-020/Q10-022 would have moved them into the
exam section and split their group, and they are not table-format records. No data were invented; each variant says F24's numbers
were not recalled. Raw ids of credits carry a leading `~` (a credit may sit on several records).

## Build checks added (build_bank.py)
- Hard: same normalised option set + stem cosine ≥ 0.6 + different key (runs before merging). On v1.3 it finds exactly Q04-011/Q07-003; after the fix, none.
- Hard: `merge_duplicates` asserts the answers agree where comparable (same option set, or two TF on the same claim) and requires a logged claim for every entry.
- Hard: a raw source-item id used by two records (`~` credits exempt; `<id>/<label>` = sub-question). Coverage: 44 of 399 real records carry `raw` (filled where touched in v1.4).
- Warning report: `qa/neighbours_v1.4.txt` (cross-chapter neighbours, union rule): 22 records, 14 pairs, all judged class c above or earlier.
- All three hard checks were negative-tested (reintroducing the conflicting key, a disagreeing merge, and a duplicated raw id each stop the build).
