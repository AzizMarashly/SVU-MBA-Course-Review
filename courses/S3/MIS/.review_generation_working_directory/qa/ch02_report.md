# Chapter 2 report — أنواع نظم المعلومات (book pp. 48–93)

Output: `render/bank_ch02.py` (imports clean, all `Q()` asserts pass).

## Counts
- Legacy records received: 38 (ch02.json) + 3 taken over from ch07.json (C7-17, C7-18, C7-19) = 41.
- Raw items received: 173 (ASM 18, BOOK 21, S25 3, R44 5, F24 11 incl. 3 topic lines, OQ1–OQ5 110, OQ6-CANDIDATE 5).
- Canonical records: **48** — exam 14, textbook-only 18 (3 of them also "other"), other 12, generated 4.
- By qtype: mcq 27, tf 16, essay 3, short 2.
- Reconstructed exam MCQs: 12. Low-confidence: 4 (Q02-027, Q02-028, Q02-042, Q02-043).
- Generated: 4 = 1 kept from legacy (G2-01 → Q02-045) + 3 new (Q02-046 ERP, Q02-047 SCM, Q02-048 e-government). Real questions: 44.

## Legacy mapping
Kept as is (block rewritten, pages re-verified): C2-01, C2-02, C2-04, C2-05, C2-06, C2-08, C2-09, C2-10, C2-11, C2-12, C2-14, C2-15, C2-16, C2-19, C2-20, C2-21, C2-22, C2-23, C2-25, C2-26, C2-27, C2-28, C2-29, C2-30, O2-01, O2-02, O2-04, O2-05, O2-06, G2-01, C7-17, C7-18, C7-19.

Reworded:
- C2-13 → Q02-009: stem says «تقارير دورية» (the F24 recall says «يومية»; the book says reports on a regular schedule — kept in `original`/notes).
- C2-17 → Q02-013: options now hold the two recalled R44 options (TPS, DSS) plus MIS and ESS; `other_source="R44: ESS"` carried over.
- C2-18 → Q02-014: «تعريف أنظمة الموارد البشرية» reconstructed as MCQ (rule 3) with real chapter-term distractors (ERP, SCM, finance).
- O2-03 → Q02-035: now an ordering question over accounts receivable / budgeting / profit planning (OQ3 asks all three, OQ5 asks accounts receivable).
- O2-05 → Q02-037: options restored to the OQ2 source wording (the legacy had added «فقط»).
- Exam reconstructions flagged: C2-07, C2-08, C2-09, C2-10, C2-11, C2-12, C2-13, C2-14, C2-15, C2-16, C2-17, C2-18 get `reconstructed=True` + `original`.

Merged:
- **C2-07 + C2-24 → Q02-003** (digital dashboard = ESS). Same idea; kept as the S25-recalled MCQ, the book's T/F wording (p.84 item 6) is in `variants`, sources BOOK+S25+ASM.
- OQ items absorbed into book records: OQ1/OQ2/OQ3 "DSS supports structured decisions → خطأ" into C2-23 (Q02-023); OQ3 111/115 + OQ5 151 (functional systems list) into C2-25 (Q02-024); OQ2 88 (functional essay) into C2-29 (Q02-031).

Split: none.

Dropped:
- **G2-02** (generated essay on the enterprise-application challenge, unit 2-5-1): unit 2-5-1 is covered by real questions C2-06 and C2-26.
- No verified legacy content dropped otherwise.

Source-list corrections (codes claimed by legacy but absent from the raw items of that sitting):
- C2-01: R44 removed (no R44 item on CAD/CAM; the R44 KWS item is «نتائجه تصاميم ورسومات» = C2-10). Now BOOK, S25, ASM.
- C2-07: R44 removed (no R44 dashboard item). Now BOOK, S25, ASM (merged with C2-24).
- C2-08: F24 removed (no F24 item «الموجه للإدارة العليا»; the F24 ESS item is aggregate data = C2-09). Now R44 only.
- C2-10: F24 removed (no F24 item on designs/graphics). Now R44 only.
- O2-03: OQ2 removed (OQ2 item 88 lists finance examples but assigns no level); OQ5 added (accounts receivable → operational).
- O2-04: OQ2 removed for the same reason.

## New questions found in the sources
- Q02-039 (OQ1, OQ2): extranet definition, short, unit 2-6-2.
- Q02-040 (OQ1, OQ3, OQ5): e-commerce is part of e-business, T/F, 2-7-2.
- Q02-041 (OQ1, OQ2, OQ4, OQ5): DSS rely on models only → خطأ (book p.62: model-driven vs data-driven DSS), 2-3-5.
- Q02-042 (OQ1, OQ2, OQ3): DSS are interactive → صح, 2-3-5 (low_conf: «لا تحل محل متخذ القرار» not in the book).
- Q02-043 (OQ1, OQ2): CAD definition, short, 2-4-2 (low_conf: «اختبار الأداء» not in the book).
- Q02-044 (OQ3): ESS give summarized, graphical, interactive information → صح, 2-3-6.

## Page / answer corrections to legacy records
All answers confirmed; page numbers corrected where the figure card sits on a later page than the section heading:
- C2-02, C2-14: 53 → 55 (TPS card, Fig. 2-4).
- C2-03: 58 → 60 + 65 (MIS card, Fig. 2-9; Table 2-1 users column).
- C2-10: 57 → 58 (KWS card, Fig. 2-6).
- C2-11: 58 → 60 (the «ملخصات ومقارنات» sentence is on p.60).
- C2-12, C2-17: 59 → 60 (MIS card); C2-17 also cites 51 (budget system example at management level) and 66 (Fig. 2-14 «Annual Budgeting»).
- C2-07/C2-24: 63 → 64 (digital dashboard paragraph).
- C2-09: 63 + 65 (ESS card and Table 2-1).
- C2-15: 55 → 55, 56 (word-processing paragraph is on p.56).
- C2-19: 49 → 49, 50 (sentence opens both 2-1 and 2-2).
- O2-02: 72 → 71, 72 (Table 2-3 on p.72, its explanation on p.71).
- O2-04: 76 → 75, 76.
No legacy answer contradicted the chapter text. BOOK marks (9 ticks, 6 highlights, 3 ch7 ticks) all agree with the text; no `book_says` needed. The ESS «unstructured decisions» mark (C2-04) is supported by the p.63 description (non-routine, «لا يوجد إجراء متفق عليه») rather than by the literal term.

## Coverage (24 units)
- Covered by real questions (20): 2-1, 2-2, 2-3-1, 2-3-2, 2-3-3, 2-3-4, 2-3-5, 2-3-6, 2-3-7, 2-4-1, 2-4-2, 2-4-3, 2-4-4, 2-5-1, 2-5-4, 2-5-5, 2-6-1, 2-6-2, 2-7-1, 2-7-2.
- Covered by generated only (4): 2-3-8 (Q02-045, kept G2-01), 2-5-2 (Q02-046), 2-5-3 (Q02-047), 2-7-3 (Q02-048).
- Uncovered: none.
- Focus units (most exam questions): 2-3-4 (5 exam) and 2-3-6 (4 exam) — both covered by real questions, no generated needed there.
- Note: the p.51–52 text (three system categories) lies under heading 2-3 before 2-3-1; its questions (C2-05, C2-20, C2-28) are filed under 2-2. The p.67 text (2-4 intro) is filed under 2-4-1.

## Topic-only items (no record)
- F24 block 5: «عدة اسئلة من نظم المجموعة الادارية (TPS, KWS…)» → 2-3-1…2-3-7; «سؤال عن الانترنت والانترانت والاكسترانت» → 2-6; «من نظم ربط المؤسسة / تطبيقات المؤسسة» → 2-5-1.
- OQ1 topics: الانترانيت (2-6-1), تحليل الاسعار / تحديد موقع التسهيلات (2-4-1/2-4-2), الاعمال الالكترونية ×3 (2-7-1), التقارير الاستثنائية (not in book), نظم المعلومات الداعمة للإدارة (older taxonomy), «~5 أسئلة عن النظم الوظيفية» ×2 (2-4). Total 10.

## OQ items
- OQ1–OQ5 received: 110. Used/merged: 56. Topic-only: 10. Rejected as not in the current book: 44, e.g. the report-type family (scheduled / exception / demand reports, «التقارير الاستثنائية» — 14 items across OQ1/OQ2/OQ3/OQ4/OQ5), the O'Brien taxonomy «نظم داعمة للعمليات / للإدارة» (OQ2 83/87, OQ3 106–109, OQ4 140/141, OQ1 53/74, OQ3 127), «ليست من نظم المعلومات الإدارية: TPS» (OQ1 62/80), DSS «شبه مهيكلة» definitions (OQ1 66, OQ2 94/95, OQ5 160, OQ3 128/129), EIS→all levels / ESS broader than EIS (OQ2 103, OQ3 136/137), CAM definition (OQ2 86, OQ4 144), McLeod manufacturing model (OQ5 149), machine control = robot (OQ3 119), production scheduling / data analyst level (OQ5 147/148), external data ranking (OQ2 104), weekly reports (OQ5 161).
- OQ6-CANDIDATE: 5 items not used (excluded textbook).

## ASM
18 ASM items (9 T/F + 6 MCQ of the ch2 set, 3 T/F of the ch7 set): all agree with the book's marks and with the text. Disagreements: 0.

## Notes
- The three intranet/extranet T/F items are asked in the book's chapter-7 review set (p.287 items 3–5); chapter 7's body has no intranet passage, so they rest on the chapter-2 text (pp.80–81) plus the book's marks; two carry `low_conf`.
- Pages read visually: 65 (Table 2-1 — text layer garbled) and 66 (Figure 2-14). PNGs in `extracted/pages_png/book_p065.png`, `book_p066.png`.
