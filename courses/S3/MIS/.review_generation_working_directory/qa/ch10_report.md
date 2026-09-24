# Chapter 10 report — نظم دعم القرار وذكاء الأعمال (pp. 377–423)

## Counts
- Legacy records received: 36 (23 C10, 4 O10, 9 G10). Raw items received: 134 (17 BOOK, 14 ASM, 4 S25, 5 R44, 12 F24, 79 OQ1–OQ5, 3 OQ6-CANDIDATE).
- Canonical records: 33 — exam 10 (Q10-001…010), textbook 14 (011…024), other 6 (025…030), generated 3 (031…033). By qtype: mcq 14, tf 12, essay 5, short 2.
- Reconstructed: 7 (Q10-001, 002, 003, 005, 006, 007, 008). Low-confidence: 3 (Q10-008, 029, 030).
- Generated: 2 kept from legacy (G10-01, G10-04), 1 new (Q10-033, unit 10-4-3). Generated 3 < real 30.
- No tables or calculations in this chapter; no §7d symbols used.

## Legacy mapping
- Kept (block rewritten, page re-checked): C10-01, 03, 04, 06, 07, 13–18, 20–23, O10-01, O10-02, G10-01, G10-04.
- Reworded / reconstructed: C10-10 (Q10-001), C10-11 (Q10-002) and C10-09 (Q10-005): short «تعريف X» recalls → MCQs whose options are real chapter definitions, `reconstructed=True`, `original` = recall. C10-12 (Q10-003): uses R44's block-3 description as stem, options = the decision types. C10-05 (Q10-008), C10-08 (Q10-006): `reconstructed` flag + `original` added. C10-02 → Q10-004 (book MCQ, S25/F24 «تعريف الدور الإعلامي» recalls as variants).
- Merged: O10-04 → C10-19 (Q10-020, legacy_id "C10-19+O10-04"): both test data mart vs warehouse; OQ1/OQ5 wordings are variants. O10-03 (warehouse definition, OQ only) merged into the F24 exam recall «تعريف مستودع البيانات» (Q10-007).
- Split: none.
- Dropped (generated, unit now covered by real questions): G10-02 (Mintzberg's three categories, 10-2-1: Q10-004, 014), G10-03 (three reasons, 10-2-2: Q10-015), G10-05 (three BI activities, 10-3-5: Q10-009, 010), G10-06 / G10-07 / G10-08 (drill-down, predictive analytics, location analytics, 10-3-6: Q10-021, 030), G10-09 (exception reports, 10-4-1: Q10-016, 024, 027, 029).

## New questions from the sources
- Q10-026 BSC delivered through ESS: OQ1 108/145/46, OQ2 108, OQ3 153, OQ4 11, OQ5 128/129 (p.407, 410, 412).
- Q10-028 warehouse data sources internal + external (T/F): OQ3 104, OQ4 31 (p.207, 393).
- Q10-029 DSS rely on (quantitative) models (T/F): OQ2 92 (p.409; low_conf: the book has no "model-driven DSS" category).
- Q10-030 «نظم دعم القرار المكاني» answered as GIS: OQ2 55 (p.406–407; low_conf: older term and "data-driven" classification not in the book).
- Q10-033 generated GDSS MCQ (p.413–414).

## Corrections to legacy records
- Sources that the re-transcription does not support were removed: C10-01 R44 (no R44 item on the decision stages) → BOOK+ASM; C10-06 R44 → BOOK+ASM; C10-05 BOOK/F24/ASM (the book/ASM item is the "not a function" MCQ = C10-06; F24 item 40 is the warehouse definition) → S25 only; C10-10 F24 (no F24 unstructured item) → S25+R44; C10-11 R44 → F24; O10-01 / O10-02 / O10-03 OQ lists re-derived from the raw items.
- Pages: C10-02 384 → [384, 385] (the informational role is on p.385); C10-14 386 → [386, 387]; C10-01 381 → [381, 382]; C10-15 408 → [408, 410]; C10-19 393 → [206, 207] (data mart is defined in ch. 5); O10-03 206 → [206, 207, 392]; C10-20 205 → [205, 404]; C10-08 396 → [394, 395, 396].
- Q10-003 (C10-12): R44 block 3 recalls «القرارات غير المهيكلة» for a stem describing the book's semi-structured definition (p.379); the R44 key itself lists it under شبه المهيكلة. Answer = شبه المهيكلة, `other_source="R44 (block 3): القرارات غير المهيكلة"`.
- O10-01 (Q10-025): examples now come from the book's Figure 10-11 (p.411, read visually), not from the older answer keys (defect rate, number of suggestions etc. removed).
- No answer changed against a book mark. All 8 T/F ticks and 6 MCQ highlights (pp.416–417) agree with the chapter text; no `book_says` needed.

## Coverage (15 units)
- Real questions: 10-1-2 (Q10-001, 002, 003, 022), 10-1-3 (011), 10-2-1 (004, 014), 10-2-2 (015), 10-3-1 (005, 017, 023), 10-3-2 (012, 018), 10-3-3 (007, 008, 013, 019, 020, 028), 10-3-4 (006), 10-3-5 (009, 010), 10-3-6 (021, 030), 10-4-1 (016, 024, 027, 029), 10-4-2 (025, 026).
- Generated only: 10-1-1 (Q10-031), 10-2-3 (Q10-032), 10-4-3 (Q10-033).
- Uncovered: none. Focus units (most exam questions): 10-1-2 (3), 10-3-3 (2), 10-3-5 (2).
- Note: 10-3-6 is covered by the Big Data T/F (definition printed in ch. 5, p.205; Big Data analytics p.404) and the low-confidence GIS item; drill-down, predictive analytics and operational intelligence have no question now.

## Topic-only items
- R44 «جودة المعلومات» → 10-2-2. F24 block (unknown sitting): «الادوار الادارية اجا منه سؤالين او تلاتة» → 10-2-1; «ذكاء الاعمال سؤالين» → 10-3-1; «مستودعات البيانات سؤال» → 10-3-3; «الانشطة الاساسية في ذكاء الاعمال» → 10-3-5. OQ1 105 / OQ5 «لوحة القيادة التحليلية», OQ1 110/165/176 «تحليل الحساسية» → 10-4-2 / 10-4-1 (no record; sensitivity is in Q10-027).

## OQ items rejected (not in the chapter text): 43 of 79 (31 used as sources/variants of Q10-007, 020, 025–030; 5 topic only)
- Dashboard types strategic/analytical/operational and their colour ratings (OQ1 48, 49, 63, 72; OQ2 93–97; OQ3 155; OQ4 12).
- The nine ESS characteristics and "factors behind ESS" (OQ1 198, 199; OQ2 106, 107; OQ4 10).
- Fact/dimension tables as data marts or warehouses (OQ1 35; OQ2 71, 72; OQ3 113, 114); multidimensional DB and its formation (OQ3 130; OQ2 60 except the warehouse part); warehouse output tools / BI tool lists (OQ2 69, OQ2 src07, OQ5 22).
- Model-base DSS components, dialogue management (OQ1 70; OQ2 84, 85, 90; OQ3 106, 108); spatial DSS "data-driven" (OQ1 56).
- Older framing of sensitivity / what-if (OQ1 58; OQ3 146, 147, 148), decisions under uncertainty (OQ5 14), Islamic bank decision type (OQ5 32), brainstorming (OQ5 33), supply-chain integration and bank profitability analysis (OQ3 110, 116), where data mining is done (OQ3 158), ETL statement (OQ1 155: already covered by Q05-031 in chapter 5).
- OQ6-CANDIDATE (3 items) not used, per instruction.

## ASM
- 14 ASM items = the 8 T/F + 6 MCQ of the book review set; all agree with the book's marks and the text (14/14). No ASM disagreement.

## Cross-chapter notes
- Q10-020 (book T/F 7, data mart smaller than warehouse) tests the same idea as Q05-024 in chapter 5 (a different review set). Both kept as book review items; the owner may merge.
- Q10-007, Q10-020, Q10-021 cite chapter-5 pages (205–207), where the book defines warehouse, data mart and Big Data; `build_bank.py` will print page-range warnings for them.

## Pages read visually
- p.416 (review T/F ticks and MCQ 1, image already in `extracted/pages_png`), p.411 (Figure 10-11, BSC examples). p.411 and p.395 were rendered into `extracted/pages_png/` (gitignored PNGs); everything else was legible in the text layer.
