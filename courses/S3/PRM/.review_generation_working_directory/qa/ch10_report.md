# Chapter 10 – مراقبة وضبط المشروع (pp. 366–399) – helper report

## Counts
- Raw items received: **111** (BOOK 14, EMAD 65, S19 16 = src05 9 + src06 7, F24 5, EX15 6 = src02 2 + src03 2 + src07 1 + …, Y16 2, TATI 2, ASEM 2). Of the src05 items, 8 are SOUFI-XCHK (crosscheck-only, not a source).
- Canonical records: **35** → exam 14, textbook 14, other 14 (a record may carry several types), generated 1.
- By qtype: mcq 27, tf 4, essay 3, short 1.
- Reconstructed: **12** (Q10-002, 003, 005–014).
- Low-confidence: **13** (Q10-002, 004, 007, 008, 009, 010–014, 022, 023, 027).
- Generated: **1** (Q10-035, sub 10-1).
- EMAD: 65 items → **28 used** (merged into 12 records: Q10-001, 002, 003, 022, 023, 025, 028–034), **37 skipped** because the book does not support them: 268–278 (cost-management definitions, cost types, reserves, time-planning stages), 280–299 except 279 (resource-planning / cost-estimation / budget-determination inputs–outputs, accuracy ranges, ±25/75 %), 301, 302 (50/50, 20/80, 0/100 rules), 304 (VAC etc.), 305 (topic pointer to S18 slide), 326 (VAC), 327 (TCPI).
- ASEM: 2 items, both agree with the book (S-Curve; BCWP).
- SOUFI-XCHK: 8 book copies (items 88–95), all agree with the book's highlight.

## EVA tables (solved with SV = BCWP − BCWS, CV = BCWP − ACWP, SPI = BCWP/BCWS, CPI = BCWP/ACWP, pp. 383–386)
- **EX15 table** (9,500/10,000/9,500 …): T1 SV 0 / CV −500; T2 SV −4,000 / CV −2,000; T3 0/0; T4 +1,000/+1,000; T5 −1,000/−1,000 → on plan = 3, under budget = 4, largest cost overrun = 2, most behind = 2, ahead = 4 (Q10-005 … 009).
- **S19/TATI table** (4000/6000/5000 …): the two sources give the same numbers but swap the BCWS/BCWP labels. Adopted TATI's labelling (it carries a worked solution consistent with it): T1 SV −1,000 SPI 0.8 CV −2,000; T2 +2,000 / +5,000; T3 +3,000 / −1,000; T4 −1,000 SPI 0.9 / +4,000; T5 0/0 → on plan = 5, most behind = 1, most over budget = 1, fastest = 3, ahead & under = 2 (Q10-010 … 014). All five carry `low_conf` stating that S19's column order would give 5/3/3/1/4 instead.
- Book review Q9/Q10 (p.393): SPI 1.2 → 100/1.2 ≈ 83 days; CPI 0.857 → 1000/0.857 ≈ 1167 $. The text defines TAC/BAC (p.382) but never writes TAC/SPI or BAC/CPI, so both records are `low_conf`.
- Book calc 3 (p.393): BCWS 5500, BCWP 3750, ACWP 4500 → SPI 0.68, CPI 0.83 (behind and over budget).
- Book calc 4 (pp.393–394): duration 22 days, CP X1–X2–X4–X5–X9, BAC 89,500, BCWS(day 10) 41,500, BCWP 47,435; ACWP ≈ 48,743 under a stated assumption (`low_conf`).

## Coverage
- Covered by real questions: 10-2 (Q10-028), 10-3 (Q10-004, 015, 016), 10-4 (Q10-017, 018, 024, 029, 034), 10-5 (25 records).
- Covered by generated: 10-1 (Q10-035 – "the most neglected area of PM is control").
- Uncovered: none.

## Topic-only / unresolved (no record created)
- Y16 recalls#0 «أربع خمس أسئلة عن EVA» → 10-5.
- Y16 recalls#4 «جدول EVA … مين سابق الخطة ومين متأخر …» (no values) → 10-5; mentioned in the notes of the EX15 table records.
- EX15 recalls#39 «منحرف زمنياً» (fragment) → 10-5.
- F24 P2 «جدول فيه 4 أنشطة … المتقدم زمنياً والأعلى صرفاً» (values not recalled) → 10-5.
- F24 P3 «سؤال لازم نحسب فيه SPI» (no data) → 10-5 (noted on Q10-022).
- F24 item 41 «شرح قرارات المتابعة.. (والجواب قرارات المتابعة)» – question not recoverable → 10-5-4 (جداول مساعدة باتخاذ القرار).
- EMAD 305 (pointer to S18 slide) → out of scope.

## Disagreements source vs book
- **S19 item 22 / TATI item 4** (top-down budgeting tf): S19 highlight = خطأ; the concept is absent from this book, the statement is the standard definition, so the record answers صح with `other_source="S19: خطأ"` and `low_conf` (Q10-004).
- **S19 vs TATI** column labelling of the 4000/6000/5000 table (see above) – the book cannot settle it; TATI adopted, flagged.
- No disagreement between the BOOK highlights and the chapter text; ASEM and SOUFI-XCHK agree with all book answers they copy.

## Pages read visually (PNG)
371 (tables 10-1/10-2), 376 (direct interviews paragraph, garbled in text), 382 (fig. 10-3, TAC/BAC), 385 (fig. 10-4/10-5), 388 (table 10-3 decision table), 393 (review Q9–Q10 highlights and the EVM exercise table).
