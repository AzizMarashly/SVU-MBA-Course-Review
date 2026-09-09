# Chapter 14 — إنهاء وإغلاق المشروع — helper report

Input: `extracted/questions/by_chapter/ch14.json` (26 raw items), chapter text `extracted/book/ch_fixed/ch14.txt` (pp. 521–554; body 523–536, review 538–540, cases 541–554).
Output: `render/bank_ch14.py` — imports cleanly (`python -c "import bank_ch14"`).

## Counts
| | |
|---|---|
| raw items received | 26 (BOOK 14 = 10 MCQ + 4 essay; EX15 5; KIFAH 1; S19 1; F24 2; ASEM 3) |
| canonical records | 17 |
| by type | exam 3 · textbook 14 · other 0 · generated 2 (records carry several types: Q14-002 and Q14-003 are exam+textbook) |
| by qtype | mcq 13 · essay 4 |
| reconstructed | 1 (Q14-001) |
| low-confidence | 1 (Q14-001) |
| generated | 2 (Q14-016 → 14-1, Q14-017 → 14-2) |
| topic-only items | 0 |
| unresolved | 0 |

## Deduplication
- **Q14-001** «لمن يُسلَّم المشروع في النهاية» = one record for recalls#16, #34, #76, #95, #158 (EX15, one source), recalls#46 (KIFAH), soufi#145 (S19). Options أ–ج kept verbatim from the EX15 recollection (src03 item 43: الممول/الزبون/المستثمر); option د (مكتب إدارة المشروع) added from the chapter. Other wordings kept in `variants`.
- **Q14-002** F24 item 27 «تعريف الإغلاق المبكر» merged into BOOK mcq-2 (same definition; book stem/options kept, F24 wording in `variants`).
- **Q14-003** F24 item 28 «كل ما يلي من الأنشطة الختامية … ما عدا» merged into BOOK mcq-6 (the F24 note says three options from the book list + one unrelated = answer, which is exactly the book item).
- ASEM others#420/#421/#422 are the book's mcq-7/9/8: added as cross-check source to Q14-008, Q14-010, Q14-009. ASEM agrees with the book highlight in **3/3**.

## Verification notes / disagreements
- No disagreement between a BOOK highlight and the chapter text (all 10 highlights confirmed: closure types p. 526–527; activities list p. 528; team evaluation p. 532; obstacles p. 535; two functions of appraisal p. 534; BOOT p. 530).
- Q14-001: book says delivery/acceptance is by **الزبون** (p. 524 «الموافقة على المشروع وقبوله من قبل الزبون», p. 528 «تسليم المشروع للزبون», p. 529 §14-4-1). KIFAH's own answer (الزبون) agrees. The handwritten EX15 scan (src07 item 10) has option ج «المستهلك/القطاع؟» circled — student recall, unreadable wording → recorded on `other_source`. S19/EX15 variant offers «المستهلك النهائي / الجهة الطارحة» without the book's term → `low_conf`.
- Q14-008 (team evaluation): the book lists the team-level criteria on p. 532 and treats individual performance separately in §14-5-2 (p. 533–534); answer ب confirmed but it rests on that structural distinction rather than an explicit sentence.

## Coverage (subsections = second level of subsections.json)
| sub | name | covered by |
|---|---|---|
| 14-1 | مقدمة | generated Q14-016 (distribution of closure responsibilities, p. 523) |
| 14-2 | أنشطة إنهاء المشروع | generated Q14-017 (PMO performs most closure tasks / final report, p. 524) |
| 14-3 | أنماط إغلاق المشروع | real: Q14-002, 004, 005, 006, 007, 012 |
| 14-4 | أنشطة إغلاق المشروع (wrap-up) | real: Q14-001, 003, 011, 013 |
| 14-5 | تقييم المشروع | real: Q14-008, 010, 014 |
| 14-6 | الدروس والعبر المستخلصة | real: Q14-009, 015 |

Uncovered after generation: none. Generated 2 ≤ real 15; both generated are for non-focus subsections (limit 3 respected). Focus areas by exam count: 14-4 (2 exam records), 14-3 (1).

## Out of scope / skipped
- None (no EMAD, MURAJA or TATI items were assigned to this chapter).

## Pages read
- Text read: 521–540 (chapter body and review questions) plus a skim of 541–554 (English case studies, no questions taken from them).
- Pages rendered visually: none (the extracted text was unambiguous for every verified item).
