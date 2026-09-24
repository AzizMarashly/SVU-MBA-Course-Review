# Chapter 8 report — تطبيقات نظم المعلومات الإدارية: تطبيقات المؤسسات (pp. 296–333)

## Counts
- Legacy records received: 29 (23 C8, 2 O8, 4 G8). Raw items received: 57 (13 ASM, 16 BOOK, 3 S25, 2 R44, 7 F24 incl. 2 topic, 15 OQ1–OQ3 incl. 3 topic, 1 OQ6-CANDIDATE — not used).
- Canonical records: 27 — exam 9 (two also textbook + other), textbook 14, other 2, generated 2.
- By qtype: mcq 16, tf 7, short 2, essay 3 (Q08-004 and Q08-025 short; Q08-021/022/023 essay).
- Reconstructed: 6 (Q08-003, 005, 006, 007, 008, 009). Q08-001/002 keep the book's MCQ, with the exam recall in `variants`.
- Low-confidence: 3 (Q08-008, Q08-019, Q08-025).
- Generated: 1 kept from legacy (G8-03 → Q08-026), 1 new (Q08-027, unit 8-2-5).

## Legacy mapping
- Kept (block rewritten, page and answer re-checked): C8-06 (Q08-017), C8-07 (Q08-018), C8-08 (Q08-019, now low_conf), C8-09 (Q08-020), C8-14…C8-20 (Q08-010…016), C8-21/22/23 (Q08-021/022/023), C8-03 (Q08-004, stays short: definition + mitigation), O8-01 (Q08-024), G8-03 (Q08-026).
- Kept, source-corrected: C8-01 → Q08-002 (book MCQ 4; S25 «تعريف سلسلة التوريد» and OQ3 70 in `variants`).
- Reworded (short → reconstructed MCQ, distractors = real chapter-8 terms): C8-10 (Q08-007, CLTV; distractors Churn Rate, cross-selling, touch point), C8-12 (Q08-006, direct marketing; distractors = the book's descriptions of SFA, customer service, analytical CRM). C8-02 (Q08-003) flagged reconstructed with the S25 recall in `original`; distractor «سلسلة القيمة الموسّعة» (a chapter-3 term) replaced by «سلاسل التوريد المتزامنة» (p. 309). C8-11 (Q08-005) flagged reconstructed; distractor KMS (chapter 9) replaced by PRM (p. 313). C8-13 (Q08-009) flagged reconstructed; the invented distractors («مركزية فقط / مغلقة المصدر فقط / محلية فقط») replaced by real chapter terms (standalone ERP/SCM/CRM «شيء من الماضي», Push-based, sequential supply chains).
- Merged: C8-04 + C8-05 → Q08-001. F24 «تعريف أنظمة المؤسسة» and book MCQ 1 (integrated modules … = برامج المؤسسات) test the same definition; the book MCQ is kept, F24 plus the OQ2 36 / OQ3 53 ERP-definition items go to `sources`/`variants` (OQ keys not imported).
- Split: none.
- Dropped:
  - O8-02 (Downstream, sources OQ2, OQ3) — no raw item in any source file backs it (`extracted/questions/*.json` searched for السفلي/Downstream: none). The idea stays visible as distractor ب of Q08-003.
  - G8-01 (unit 8-1-2, first step when implementing enterprise software) — unit covered by real book MCQs Q08-017/018.
  - G8-02 (unit 8-1-3, business value of enterprise systems) — covered by book T/F Q08-011 and essay Q08-021.
  - G8-04 (unit 8-4-1, implementation challenges) — covered by book T/F Q08-015/016.

## New questions found in the sources
- Q08-008 — F24 item 29 «تعريف الأنشطة التشغيلية» (no answer text in any copy). Reconstructed as operational CRM (p. 318) with `low_conf`; alternative reading noted (operational management «مراقبة الأنشطة اليومية», p. 28, chapter 1).
- Q08-025 — OQ3 178 (information in the supply chain flows in both directions, p. 302), `low_conf` because its premise (products flow one way) is older-curriculum wording; the book has materials flowing both ways too (returns).

## Corrections to legacy records (id: old → new, evidence)
- Sources (no raw item supports them; the chapter-8 raw file holds R44 only for bullwhip and direct marketing):
  - C8-01: F24 removed (the only F24 supply-chain item is the block-5 topic line «سؤال عن سلسلة التوريد», topic only) → BOOK, ASM, S25 (+ OQ3 70).
  - C8-02: R44 removed → S25, F24.
  - C8-04: R44 removed → F24 (merged into Q08-001).
  - C8-11: R44 removed → F24. The R44 item (block 2 item 35 «التسويق المباشر») is Q08-006; the raw file flags F24 42 as its duplicate, but the recalls ask different things (who identifies cross-selling vs. what direct marketing is), so two records, one source each.
  - O8-01: OQ3, OQ4 removed (no OQ4 item; OQ3 177 asks «what does ERP become — Extended ERP/IOIS», not in the book) → OQ1, OQ2.
- Pages: C8-05 298 → [298, 299]; C8-07 299 → [299, 300]; C8-09 318 → [317, 318] (fig. 8-8 Sales/Service Analytics); C8-15 300 → [300, 301]; C8-16 303 → [302, 303]; C8-17 307 → [306, 307]; C8-18 319 → [319, 320]; C8-19/C8-20 320 → [320, 321]; C8-11 316 → [315, 316]; C8-13 322 → [322, 323]; C8-03 304 → [304, 305]; C8-10 unchanged 319; O8-01 78 (chapter 2) → [313, 322] (p. 78 quoted in `notes`); G8-03 306 → [305, 306]; essays → the section pages.
- Answers: no answer changed. All 7 BOOK T/F ticks (p. 326, checked on the page image) and 6 BOOK MCQ highlights agree with the chapter text; no `book_says` needed. C8-08 (logistics) gets `low_conf`: the chapter never defines logistics in the stem's words; the answer rests on the book's highlight and the p. 307 use of the term.
- Q08-010 keeps the book's wording «… بين المؤسسات»; `notes` say the text speaks of sharing across one enterprise.

## Coverage (14 units)
- Real questions: 8-1-1 (Q08-001, 010), 8-1-2 (017, 018), 8-1-3 (011, 021), 8-2-1 (002, 003, 012, 025), 8-2-2 (004, 022), 8-2-4 (013, 019), 8-3-1 (023), 8-3-2 (005, 006), 8-3-3 (007, 008, 020), 8-3-4 (014), 8-4-1 (015, 016), 8-4-2 (009, 024).
- Generated only: 8-2-3 (Q08-026, legacy), 8-2-5 (Q08-027, new).
- Uncovered: none. Focus units (most exam items): 8-2-1 (S25 ×2, F24), 8-3-2 (F24, R44), 8-3-3 (S25, F24) — all covered by real questions. New generated = 1 (≤ 3); generated 2 < real 25.

## Topic-only items (no record)
- F24 block 5 «سؤال عن سلسلة التوريد» → 8-2-1 (noted on Q08-002).
- F24 block 5 «سؤال عن خدمة العملاء» → 8-3-2 (noted on Q08-023).
- OQ1 123 «نظام تخطيط موارد المشروع (الممتدة)», OQ1 170 «تمتد موارد المشروع لتشمل…» → 8-4-2 (repeats of OQ1 16, on Q08-024).

## OQ items rejected (not in the chapter text): 7 of 12 non-topic OQ items (5 used)
- Collaborative demand forecasting (OQ2 52, OQ3 85: common promotion plan, end-consumer data, buyer/seller views) and OQ3 84 («supply chain is a radical solution…») — the book has no such list.
- OQ3 71 «why companies adopt supply chains — intense global competition», OQ3 100 «enterprise database: >100 users, parallel servers, intranet/extranet», OQ3 175 «IOS began with the supply chain», OQ3 177 «Extended ERP / IOIS» — not in the book.
- Used: OQ1 16 + OQ2 35 (Q08-024), OQ2 36 + OQ3 53 (Q08-001), OQ3 70 (Q08-002), OQ3 178 (Q08-025). OQ6-CANDIDATE (src01 p18, ERP extends to …) not used.

## ASM
- 13 ASM items = the 7 T/F + 6 MCQ of the book set; all 13 agree with the book's marks and the text (**ASM 13/13 agree**). ASM added to `sources` of Q08-001, 002, 010–020 (T/F and MCQ records).

## Symbols
- None used (no tables or calculations in this chapter).

## Pages read visually
- p. 317 (fig. 8-8 CRM capabilities: Sales/Service Analytics), p. 319 (fig. 8-10 analytical CRM), p. 326 (T/F ticks and MCQ 1 highlight confirmed). Saved as `extracted/pages_png/book_p317.png`, `book_p319.png`, `book_p326.png`, `book_p327.png` (p. 327 rendered, not needed after the p. 326 check matched the book helper's marks).
