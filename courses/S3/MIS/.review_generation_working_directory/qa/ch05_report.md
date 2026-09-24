# Chapter 5 report — قواعد البيانات (pp. 184–222)

## Counts
- Legacy records received: 35 (27 C5, 2 O5, 6 G5). Raw items received: 96 (14 ASM, 17 BOOK, 5 S25, 3 R44, 8 F24, 47 OQ1–OQ5, 2 OQ6-CANDIDATE).
- Canonical records: 34 — exam 10, textbook 17, other 4, generated 3. By qtype: mcq 16, tf 10, short 5, essay 3.
- Reconstructed: 9 (Q05-002…010). Low-confidence: 5 (Q05-020, 021, 023, 030, 031).
- Generated: 3 kept from legacy (G5-02, G5-03, G5-06), 0 new.

## Legacy mapping
- Kept as is (block rewritten, page re-verified): C5-02, 04, 05, 06, 08, 10, 11–18, 21–23, 25, 26, O5-01, G5-02, G5-03, G5-06.
- Reworded: C5-03 (Q05-001: R44's own three options بت/بايت/ملف kept exactly instead of the legacy 4-option set); C5-07 (Q05-008: distractors replaced by real chapter terms — foreign key, attribute, record); C5-24 (Q05-010: S25 «تعريف نظام Hadoop» reconstructed as MCQ, distractors = data warehouse, in-memory computing, application server); C5-19 (answer reasoning, see corrections); C5-20 (ans normalised to «صح», low_conf).
- Merged: O5-02 → C5-27 (Q05-027, same idea: data hierarchy order; OQ wording kept as variant).
- Split: none.
- Dropped: G5-01 (Project/Select/Join — unit 5-2-1 now covered by 7 real questions); G5-04 (Hadoop — same idea as Q05-010 from S25); G5-05 (in-memory computing — unit 5-3-2 covered by Q05-010/023/024/031).

## New questions from the sources
- Q05-029 DBMS definition — OQ3 items 96 + 131 (p.191).
- Q05-030 Query definition — OQ2 79, OQ3 123 (p.197; low_conf: book has no explicit definition).
- Q05-031 Transform/cleanse before loading into the warehouse — OQ3 61 + 109 (p.207; low_conf: source says «قاعدة البيانات», book says data warehouse).

## Corrections to legacy records
- C5-19 (Q05-020): book tick and ASM both say «خطأ»; text p.195 «يمكن دمج جداول قاعدة البيانات العلائقية بسهولة … شريطة أن يشترك أي جدولين في عنصر بيانات مشترك» and p.194 (Supplier_Number as primary/foreign key) support the statement. Answer kept «صح» against the mark: `book_says="علامة الكتاب: خطأ"`, `other_source="ASM: خطأ"`, low_conf noted so the student knows an exam key may follow the book.
- C5-20 (Q05-021): legacy ans «صح (وفق المرجع الأصلي Laudon)» → «صح»; pages 214 → [193, 214]; low_conf because the chapter never treats hierarchical DBMS.
- C5-22 (Q05-023): pages 207 → [206, 207]; low_conf added (text says "multiple operational systems", not "legacy").
- C5-21 (Q05-022): pages 202 → [200, 202]. C5-14 (Q05-015): 196 → [196, 197]. C5-25: 216 → [187–190]. C5-26: 216 → [199, 200, 202]. C5-27: 216 → [185, 186]. C5-24/Q05-010: 207 → [207, 208].
- Source corrections (raw re-transcription does not support them): C5-01 R44+F24 removed (only R44 item 5 = entity exists; the attribute mention is the answer key's addendum) → BOOK+ASM; C5-03 S25 removed (S25 item 36 is the byte question, C5-04) → R44; C5-09 BOOK+ASM removed (no book question on the data dictionary) → S25+F24; O5-01 OQ1/OQ2/OQ4 removed → OQ3 only; O5-02's OQ2/OQ3/OQ4 have no raw item at all → merged into C5-27 without OQ codes.

## Coverage (9 units)
- Real questions: 5-1-1 (Q05-001…005, 011, 017, 027), 5-1-2 (006, 012, 018, 025), 5-2-1 (007, 008, 013, 014, 016, 019, 020, 021, 028, 029), 5-2-2 (009, 015, 030), 5-2-3 (022, 026), 5-3-2 (010, 023, 024, 031).
- Generated only: 5-2-4 (Q05-032), 5-3-1 (Q05-033), 5-3-3 (Q05-034).
- Uncovered: none. Focus unit = 5-1-1 (6 exam questions).

## Topic-only items
- S25 17 «سؤال عن DBMS» → 5-2-1. R44 «اجى كمان» «اعتماد البرامج ع البيانات» → 5-1-2. Block-5 (unknown sitting) «مشاكل بيئة الملفات التقليدية سؤالين» → 5-1-2; «نظام hadoop سؤال» → 5-3-2. OQ1 130 «قاعدة البيانات الموزعة» → not in the chapter.

## OQ items rejected (not in the chapter text): 40 of 47
- OLAP (13 items: OQ1 20, 69, 94, 120, 149; OQ2 42, 68; OQ3 103, 126bis; OQ5 28, 39, 40; OQ1 95) — the text defers analytics to chapter 6.
- Multidimensional DB / dimensions (OQ1 34; OQ2 67, 70; OQ3 111, 112).
- Data mining (OQ1 50, 51, 196, 196(8); OQ2 115–119, src07; OQ3 156, 157, 160–162; OQ4 7, 8; OQ5 26; OQ5 src04 mcq) — «التنقيب» never appears in chapter 5.
- OQ3 97 (free/near-free DBMS trend) and OQ3 101 («قاعدة بيانات الانترنت», 1000 users) — not the book's framing.
- OQ6-CANDIDATE (2 items) not used, per instruction.

## ASM
- 14 ASM items = the 8 T/F + 6 MCQ of the book set; all 14 agree with the book's marks (14/14). ASM's «خطأ» on T/F 4 goes on `other_source` of Q05-020 because the text is followed there.

## Pages read visually
- None; the text layer was legible for every cited passage (pp. 185–211, 214–216).
