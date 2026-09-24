# Chapter 9 report — تطبيقات نظم المعلومات الإدارية: إدارة المعرفة (pp. 335–375)

## Counts
- Legacy records received: 31 (23 C9, 4 O9, 4 G9). Raw items received: 83 (14 ASM, 17 BOOK, 4 S25, 2 R44 incl. 1 topic, 5 F24 incl. 1 topic, 41 OQ1–OQ5; 0 OQ6-CANDIDATE).
- Canonical records: 28 — exam 7 (one also other), textbook 14 (one also other), other 3, generated 4.
- By qtype: mcq 16, tf 8, short 1, essay 3.
- Reconstructed: 7 (Q09-001…007).
- Low-confidence: 1 (Q09-022).
- Generated: 2 kept from legacy (G9-03 → Q09-025, converted short → mcq; G9-04 → Q09-026), 2 new (Q09-027 unit 9-2-2, Q09-028 unit 9-2-3).

## Legacy mapping
- Kept as is (block rewritten, page and answer re-checked): C9-06, C9-07, C9-08, C9-14, C9-15, C9-16, C9-17, C9-18, C9-20, C9-21, C9-22, C9-23, O9-01, O9-03, G9-04.
- Reworded (short → reconstructed MCQ with real chapter terms as distractors): C9-03 (Q09-001, wisdom: distractors = the book's definitions of data / information / knowledge, p. 337); C9-04 (Q09-002, organizational learning: distractors = KM, organizational capital, COPs); C9-11 (Q09-007, intelligent agent); C9-12 (Q09-006, fuzzy logic). C9-05 (Q09-003): options kept, flagged `reconstructed` with the S25 recall in `original`. G9-03 (Q09-025): generated short → MCQ.
- Split: C9-10 → Q09-004 (S25 29 «تعريف الانظمة الخبيرة») + Q09-005 (F24 44 «تعمل من خلال قواعد if then else»). Two different recalls (definition vs rule form), each now its own reconstructed MCQ.
- Merged: C9-01 + C9-02 + C9-13 → Q09-008 (tacit knowledge: book MCQ 2 kept, MCQ 1 and T/F 1 in `variants`); C9-09 + C9-19 + O9-02 → Q09-014 (knowledge discovery = data mining: book MCQ 6 kept, T/F 7 and the OQ data-mining definition items in `variants`).
- Dropped: O9-04 (CAD definition) — the same OQ items (OQ1 9, OQ2 28) are already recorded in chapter 2 as Q02-043; CAD in chapter 9 is covered by the book essay Q09-021. G9-01 (knowledge-worker roles, 9-3-1) — unit now covered by the real T/F Q09-017 (the roles are in its `remember`). G9-02 (KWS requirements, 9-3-2) — unit covered by the real T/F Q09-018.

## New questions found in the sources
- Q09-024 «مجال الشبكات العصبية محدد بمجالات معينة» — OQ3 166 (T/F; book p. 361 settles it: خطأ).
- Q09-007 gains OQ3 29 (automated purchase order → agent) as a variant/source; Q09-014 gains OQ1 196, OQ2 115, OQ3 156/160, OQ5 26 (filed under chapter 5 by the split and rejected there as "not in chapter 5"; the concept is defined in chapter 9, p. 355). Keys not imported.

## Corrections to legacy records (id: old → new, evidence)
- Source corrections (no raw item supports them; `exams.json` and `src20/text.txt` searched — R44's only chapter-9 items are «تعريف الحكمة» and the topic «تطبيق الحكمة»):
  - C9-01: R44 removed → BOOK, ASM (now textbook only, Q09-008).
  - C9-09: R44 removed → BOOK, ASM (+ OQ via O9-02 merge).
  - C9-10: R44 removed → S25 (Q09-004) and F24 (Q09-005).
  - C9-11: R44 removed → S25, F24 (+ OQ3).
  - O9-01: OQ2, OQ4 removed (OQ2 58 asks about knowledge-driven DSS, not the same question; no OQ4 item) → OQ1, OQ5.
  - O9-02: OQ4 removed (no OQ4 data-mining item) → OQ1, OQ2, OQ3, OQ5.
  - O9-03: OQ5 added (OQ5 48 T/F in `variants`).
- Q09-005 (from C9-10): `other_source` added — the F24 key's example «أنظمة التشخيص في الطب أو دعم العملاء» is the book's example of case-based reasoning (p. 358), not of expert systems.
- Pages: C9-09/C9-19 355 → [345, 355] (knowledge discovery named on both pages; unit set to 9-1-3); C9-10 356 → [356] and [356, 358] (If-Then-Else on p. 358); C9-11 363 → [363, 364]; C9-07 343 → [343, 344]; C9-08 344 → [344, 345]; C9-18 350 → [350, 351]; O9-01 356 → [356, 364] (the "embedded knowledge base" wording is on p. 364); O9-03 360 → [360, 361, 362]; G9-03 356 → [356, 357, 358]; C9-21 369 (review page) → [336–341]; C9-22 → [346–349]; C9-23 → [352–354].
- Answers: no answer changed. All 8 BOOK T/F ticks and 6 BOOK MCQ highlights agree with the chapter text; no `book_says` needed.

## Coverage (15 units)
- Real questions: 9-1-1 (Q09-001, 002, 008, 009, 019), 9-1-2 (003, 010, 011, 012), 9-1-3 (013, 014), 9-2-1 (015, 016, 020), 9-3-1 (017), 9-3-2 (018), 9-3-3 (021), 9-4-1 (004, 005, 022), 9-4-3 (006), 9-4-4 (023, 024 — "other" only), 9-4-5 (007).
- Generated only: 9-2-2 (Q09-027, new), 9-2-3 (Q09-028, new), 9-4-2 (Q09-025, legacy), 9-4-6 (Q09-026, legacy).
- Uncovered: none. Focus units (most exam questions): 9-1-1 (R44 + S25/F24), 9-4-1 (S25, F24), 9-4-5 (S25 + F24), all covered by real questions. New generated = 2 (≤ 3), generated 4 < real 24.

## Topic-only items (no record)
- R44 block 3 «تطبيق الحكمة» → 9-1-1 (noted on Q09-001).
- Block 5 (unknown sitting) «خطوات سلسلة القيمة لادارة المعرفة اجا سؤالين منها» → 9-1-2 (noted on Q09-003).
- OQ1 118 «مين في قاعدة معرفة؟» → merged idea Q09-022. OQ4 (src16 p21) «اي من الاساليب يمكن استخدامها في التنبؤ» (options cut off) → rejected with the decision-tree family below.

## OQ items rejected (not in the chapter text): 30 of 41 (11 used)
- "Knowledge is more concise than information and lasts longer" family (10: OQ1 12, 90; OQ2 21, 25; OQ3 33, 35; OQ4 47; OQ5 15, and the two «المعرفة هي» MCQs of OQ5) — the book never compares conciseness/useful life.
- «المعلومات المكثفة» (OQ2 22), «يصبح الانسان خبيراً عندما» (OQ3 34), «زيادة مبيعات التمر في رمضان 50%: بيانات/معلومات/معرفة» (OQ5 16; the book's hierarchy does not settle this example).
- Knowledge-driven DSS (OQ1 30, OQ2 57, 58, OQ3 91) and «نظام دعم القرار يدعم الوكيل الذكي» (OQ3 78) — older DSS taxonomy.
- Decision trees / classification-prediction methods (OQ1 52, 128; OQ2 121; OQ3 163; OQ5 47; OQ4 src16 p21 topic) — decision trees are not in the book.
- Neural-network specifics of the older text (OQ1 129, 168; OQ3 164, 165, 167; OQ5 46): relative importance of variables, training weights, unconstrained nonlinear optimisation, "high flexibility", linear/non-linear variables.
- OQ items used: OQ1 89/118/153/189 + OQ5 src04 (Q09-022); OQ1 197, OQ2 120, OQ4 9, OQ5 48 (Q09-023); OQ3 166 (Q09-024); OQ3 29 (Q09-007). OQ1 153/189 and OQ1 118 are the same question as OQ1 89 (dup_of).

## ASM
- 14 ASM items = the 8 T/F + 6 MCQ of the book set; all 14 agree with the book's marks and the text (**ASM 14/14 agree**). ASM added to `sources` of Q09-008 (3 items), 009, 010, 011, 012, 013, 014 (2 items), 015, 016, 017, 018.

## Symbols
- None used (no tables or calculations in this chapter).

## Pages read visually
- None; the text layer was legible for every cited passage (pp. 336–365). Book marks taken from the book helper's visual reading (`book.json`), consistent with ASM and the text.
