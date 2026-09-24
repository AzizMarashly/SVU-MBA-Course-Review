# Chapter 1 report — bank_ch01.py (MIS v1.0, prompt v0.10)

## Counts
- Legacy records received: 39 (C1-01…C1-34, O1-01, O1-02, G1-01…G1-03). Raw items received: 80 (15 ASM, 18 BOOK, 16 exam, 31 OQ).
- Canonical records: **34** — exam 14, textbook 18 (2 of them also exam, 1 also exam+other), other 4 (1 new), generated 1.
  By qtype: mcq 21, tf 10, essay 3. Reconstructed: 12. Low-confidence: 2 (Q01-031, Q01-033). Generated: 1 kept from legacy (G1-02), 0 new.
- `python -c "import bank_ch01"` passes.

## Legacy mapping
- Kept as is (stem/options unchanged, block rewritten, sources/pages re-verified): C1-01, C1-02, C1-03, C1-04, C1-05, C1-06, C1-09, C1-10, C1-11, C1-19, C1-20, C1-23…C1-34, O1-01 (options restored to the source's), O1-02, G1-02.
- Reworded (definition "short" → reconstructed MCQ per rule 3): C1-12 → Q01-008, C1-13 → Q01-005 (F24 fill-in wording as stem), C1-16 → Q01-009, C1-18 → Q01-012, C1-21 → Q01-013, C1-22 → Q01-002.
- Merged: **C1-07 + C1-08 → Q01-006** (same idea: definition of information; the F24 item 31 "…بعد تنظيمها" is the only F24 evidence behind both legacy records — it is now `variants` of the book MCQ).
- Split: none.
- Dropped (6):
  - **C1-14** (R44 «تعريف البرمجيات», p.30): no such item exists in the v1.0 re-transcription of R44 (exams.json has no software-definition item in any chapter); sources no longer support it.
  - **C1-15** (R44 «السياسة التنظيمية») and **C1-17** (F24 «تعريف الهيكل التنظيمي»): the raw items were routed by stage 3 to `by_chapter/ch03.json` (raw ids around ch03 lines 737 and 917); left to the chapter-3 helper to avoid a duplicate. Note for the owner: the book's definitions are in chapter 1 (politics p.29, structure p.27) — if the ch03 helper rejects them, they belong here.
  - **G1-01** (generated, unit 1-1-2 IT innovations): unit now covered by the real book essay Q01-028, whose answer lists the five changes.
  - **G1-03** (generated, digital-firm definition, unit 1-1-4): unit covered by real questions Q01-015 (book T/F 1) and Q01-024 (book MCQ 2); the definition is kept inside Q01-015's answer block.
  - (O1-01's OQ2 attribution dropped — no OQ2 raw item carries this question; sources now OQ1, OQ5.)

## New questions found in the sources
- **Q01-033** «ليس من موارد نظام المعلومات» — OQ1 #21, OQ2 #43 (+ OQ2 #14 / OQ3 #67 / OQ4 #37 list the resources). Kept with `low_conf` (book never says «موارد», answer follows from its IS definition and IT components).
- All exam raw items (16) map to legacy records; no new exam question.

## Page / answer corrections to legacy records
- C1-01: 20 → [19, 20] (list of six objectives p.19, definition p.20).
- C1-03: 25 → [24, 25]. C1-26: 25 → [24, 25] («ثلاثة أنشطة تنتج المعلومات» is on p.24).
- C1-05: 22 → [22, 39]; C1-07: 23 → [23, 40]; C1-09/C1-10: 25 → [25, 40]; C1-11: 26 → [26, 27, 40] (review-set page added).
- C1-18: 32 → [32, 33]. C1-20: 36 → [36, 37]. C1-23: 17 → [16, 17, 39].
- **C1-24**: 336 → [11, 35, 39]. The chapter-11 sentence is not in chapter 1; the answer «خطأ» is supported here by p.35 («قيمة الاستثمارات في تكنولوجيا المعلومات تعتمد إلى حد كبير على الاستثمارات التكميلية في الإدارة والتنظيم») and p.11. Note kept in `notes`.
- **C1-29**: 58 → [39, 51, 58]; **C1-30**: 53 → [39, 51, 53]; **C1-31**: 60 → [39, 60]; **C1-06**: 81 → [40, 81]. These four are book review questions of chapter 1 whose answers live in chapter 2 (verified there: p.51 management-level systems serve middle managers incl. non-routine decisions; p.53 TPS = operational level; p.58 MIS serves middle management; p.60 DSS «المشكلات الفريدة والتي تتغير بسرعة… لا تُحدد إجراءات الوصول إلى حل لها بشكل كامل مسبقاً»; p.81 e-business). build_bank.py lists them as "outside the chapter range"; `notes` says so on each.
- C1-04 (S25 WWW): raw item exists in exams.json (S25 item 4) but was tagged ch 6 "out of scope"; the definition is in chapter 1 p.31, S25 recalled it in book order after items 1–3 → kept here, `reconstructed=True`, `original` filled.
- Answers: no legacy answer changed. All 15 BOOK marks (9 T/F, 6 MCQ) verified against the text; none contradicted, so no `book_says`.
- `reconstructed=True` + `original` added to C1-01, C1-02, C1-03, C1-04, C1-19, C1-20 (legacy MCQs built from recalled sentences).

## Coverage (9 units)
- Covered by real questions: 1-1-1 (Q01-028), 1-1-4 (Q01-015, Q01-024), 1-1-5 (Q01-001/002/003/019), 1-2-1 (Q01-004…007, 017, 018, 025, 026, 029, 031, 032), 1-2-2 (Q01-008…011, 020…023, 027, 033), 1-2-3 (Q01-012), 1-2-4 (Q01-013, 014, 016, 030).
- Covered by generated: 1-1-3 (Q01-034, legacy G1-02, re-verified p.16–17).
- Uncovered: **1-1-2** («ما الجديد في نظم المعلومات الإدارية») — treated as covered by the answer of essay Q01-028 (the five changes), hence G1-01 dropped; if the owner prefers a dedicated MCQ, G1-01's question (IT innovations, p.13) is still valid.
- Focus areas (most exam questions): 1-2-1 (5), 1-2-2 (4), 1-1-5 (3) — all covered by real questions; no new generated needed.

## Topic-only items
- None in ch01.json (no `qtype: topic` items).

## OQ items rejected as not in the current book (13 raw items)
- «تعد البيانات قليلة الفائدة للإدارة الوسطى» (OQ1 #10, OQ2 #23) — the book never grades data usefulness by management level.
- «تستخدم لتخفيض درجة عدم التأكد لدى متخذ القرار» (OQ1 #11, OQ2 #24) — not in the book; the two sources also disagree (المعرفة vs المعلومات).
- «يكسب النظام ديناميكية: الرقابة والتغذية العكسية» and its restatements (OQ1 #22, #84, #119, #137; OQ2 #44; OQ3 #11, #68) — the book has feedback (p.25) but no «control» element or «dynamic system» concept.
- «المعلومات مفيدة لأي كان؟ خطأ» (OQ3 #32) — not in the book.
- «(تقرير المبيعات الأسبوعي) يمكن…» (OQ5, incomplete, no answer, chapter-2 concept).
- OQ4 #39 «مدخلات – معالجة – مخرجات» (answer key only, no stem) — concept is in the book (p.24) but there is no question to attach; not added as a source.
- Merged instead of rejected: OQ3 #25 CBIS definition → variant of Q01-005; OQ2 #20 / OQ3 #31 / OQ4 #29 / OQ2 «المعلومات أكثر اختصاراً» → sources/variants of Q01-006; OQ5 #12/#21 T/F → variant of Q01-031.

## ASM
- 15 ASM items (9 T/F + 6 MCQ), all duplicates of the book review set; ASM's worked answers agree with the book mark on **15/15**. ASM added to `sources` of those 15 records. No disagreement.
- Other source disagreements: R44's worked answer for the IS definition says «نظام وسيط بين نظام **المعلومات** ونظام الإدارة» where the book says «نظام **العمليات**» → `other_source` on Q01-005.

## Pages read
- Chapter text read in full from ch01.txt (pp. 10–47); chapter-2 passages read from ch02.txt for pp. 51, 53, 58, 60, 81. No page rendered visually (the text layer was readable everywhere needed).
