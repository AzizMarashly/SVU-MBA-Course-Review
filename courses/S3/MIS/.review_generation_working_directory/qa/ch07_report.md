# Chapter 7 report — الأعمال الإلكترونية والتجارة الإلكترونية (pp. 263–294)

## Counts
- Legacy records received: 25 (24 C7, 1 O7, 0 G7). Raw items received: 34 (11 ASM, 14 BOOK, 1 S25, 3 R44, 4 F24 incl. 1 topic, 1 OQ2).
- Canonical records: 21 — exam 7 (one also textbook), textbook 13, other 0, generated 1. By qtype: mcq 14, tf 4, essay 3.
- Reconstructed: 7 (Q07-001…007). Low-confidence: 1 (Q07-006).
- Generated: 0 kept from legacy (the v0.2 chapter had none), 1 new (Q07-021, unit 7-1-1).

## Legacy mapping
- Kept (block rewritten, page re-verified): C7-01 (Q07-017), C7-10 (Q07-014), C7-11 (Q07-015), C7-13 (Q07-013), C7-14 (Q07-012), C7-15 (Q07-008), C7-16 (Q07-009), C7-20 (Q07-010), C7-21 (Q07-011), C7-22 (Q07-018), C7-23 (Q07-019), C7-24 (Q07-020).
- Reworded / reconstructed as MCQ (`reconstructed=True`, `original` from the raw item): C7-02 (Q07-002: R44 recalled the term «متاجر التجزئة الالكترونيه» with the features as answer, so the MCQ now asks for the features; distractors = market creator, transaction broker, portal definitions), C7-05 (Q07-004, F24, was short), C7-06 (Q07-003, R44, was short), C7-07 (Q07-005, S25, was short), C7-08 (Q07-006, F24, was short), C7-09 (Q07-007, F24, was short). Distractors are the book's own definitions of neighbouring terms (other revenue models; price transparency / information density / asymmetry; personalization, price discrimination, dynamic pricing; intellectual property, streaming).
- C7-12 (Q07-016): stem restored to the book's own wording («يُعرف عرض الأسعار عبر الإنترنت أيضاً بما يلي»); v0.2 had expanded it with the dynamic-pricing definition, which gave the answer away. C7-01 (Q07-017): options restored to the book's exact four (v0.2 appended «(متجر تجزئة إلكتروني E-Tailer)» to option د).
- Merged: C7-03 + C7-04 → Q07-001 (same idea: Amazon/Walmart = B2C). R44 exam recall is the record; the book T/F 6 (خطأ) is in `variants`; sources R44+BOOK+ASM.
- Split: none.
- Dropped: C7-17, C7-18, C7-19 — moved to chapter 2 (Q02-027/028/029, unit 2-6), per STATE §3. O7-01 («التجارة الإلكترونية جزء من الأعمال الإلكترونية», OQ) — duplicate of Q02-040 in `bank_ch02.py` (same statement, unit 2-7-2, p.81; its OQ raw items are assigned to chapter 2); no raw item in the chapter-7 set.

## New questions from the sources
- None beyond the legacy set. OQ2 item (EDI definition) rejected: «EDI / التبادل الإلكتروني للبيانات» appears nowhere in the book.

## Corrections to legacy records
- Sources: C7-01 R44 removed (no R44 raw item asks Amazon's business model; R44's e-tailer item is C7-02) → BOOK+ASM. C7-03 BOOK+ASM belonged to the T/F (C7-04); now carried by the merged record through the variant.
- Pages: C7-10 268 → 270 (Richness is on p.270). C7-11 269 → [269, 270]. C7-02 279 → [279, 280]. C7-07 271 → [270, 271]. C7-13 20 → [20, 278]. C7-14 81 → [31, 269] (p.81 is extranets; the Internet-as-global-platform / universal-standards passages are p.31 and p.269). C7-15 17 → [17, 31]. C7-22 289 → [265, 266, 267]. C7-23 289 → [272–275]. C7-24 289 → [277, 278].
- Content: C7-22 v0.2 explanation claimed «نحو 80% من مستخدمي فيسبوك يصلون عبر الهواتف» — not in the book text; removed. C7-23 v0.2 defined switching costs as «تكلفة الانتقال من منتج إلى منتج منافس» — the book gives no definition, only that digital markets can lower or raise them (p.273); the answer now says so. C7-18 v0.2 explanation (sales-intranet uses) was not book text — no longer here (record moved to ch2).
- No answer changed. All 11 BOOK marks in the chapter-7 raw set (5 ticks, 6 highlights; the other 3 BOOK items are essays; the 3 intranet ticks are handled in ch2) agree with the chapter text; no `book_says` needed.
- Chapter-1/2 page citations (instruction): Q07-008 (C7-15) p.17, 31; Q07-012 (C7-14) p.31 (+269); Q07-013 (C7-13) p.20 (+278). `build_bank.py` will print these as out-of-chapter warnings, as expected.
- Note: Q07-013 (book MCQ on the business-model definition) tests the same concept as Q01-002 (R44 exam recall, ch1). Kept in chapter 7 per the instruction; different sources and wording.

## Coverage (7 units)
- Real questions: 7-1-2 (Q07-018), 7-1-3 (Q07-005, 006, 008, 011, 012, 014, 015), 7-1-4 (Q07-007, 009, 016, 019), 7-2-1 (Q07-001, 020), 7-2-2 (Q07-002, 010, 013, 017), 7-2-3 (Q07-003, 004).
- Generated only: 7-1-1 (Q07-021, dot-com bubble, pp.264–265).
- Uncovered: none. Focus units: 7-2-3 (R44 + F24 + an F24-file topic line) and 7-1-3 (S25 + F24).
- Unit 7-2-3: the sales, advertising, transaction-fee and affiliate models have no question. They appear only as distractors in Q07-003/004. The topic line suggests one real exam question was on the sales model. No generated question was added because the unit is already covered (DECIDE limits).

## Topic-only items
- F24-file block 5 line 10 «سؤالين عن نماذج ايرادات التجارة الالكترونية (المبيعات واحد منن)» → 7-2-3.

## OQ items rejected (not in the book): 1 of 1
- OQ2 src03 p2 item 9 (EDI definition).

## ASM
- 11 ASM items = the 5 T/F + 6 MCQ of the book set that stay in chapter 7; all agree with the book's marks and the text: **11/11 agree** (the 3 intranet T/F ASM items are counted in the ch2 report).

## Pages read visually
- None; the text layer was legible for every cited passage (pp. 17, 20, 31, 264–285, 287–289).

## Notes for the owner
- T/F answer blocks (Q07-008…011) are 33–37 words, under the 40-word target (like chapter 3's T/F blocks). No distractors, by design.
- No tables, calculations or symbols. Nothing to add to `SYMBOLS`.
