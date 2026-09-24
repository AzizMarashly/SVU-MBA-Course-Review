# others_a — stage-3 transcription report (codes OQ1, OQ2, OQ3)

Output: `extracted/questions/others_a.json` — 533 items (UTF-8, no BOM, `ensure_ascii=False, indent=1`).
Extra field `in_book` (true / false / "maybe") on every item, `code` = OQ1 / OQ2 / OQ3. `book_dup` is false
everywhere (no end-of-chapter question lists were compared at this stage). `dup_of` indexes point inside this file.
All five files belong to the OLDER curriculum (Dr Suleiman Awad: systems theory, McLeod functional models,
Power's DSS taxonomy, Excel filters / pivot tables / Solver, Hong's IOIS framework, history dates).

## Items per file

| src | file | items | with options | free-form (short/essay/tf) | topic-only | marked answer | in_book true / maybe / false |
|---|---|---|---|---|---|---|---|
| src05 | اسئلة_دورات_مجمعة_MIS.pdf (23 pp) | 193 (numbers 1–201 + 1 lecture-note block) | 39 | 115 | 39 | 134 | 31 / 59 / 103 |
| src06 | تجميعة اسئلة دورات_MIS_2.pdf (6 pp) | 0 separate — fully contained in src05 #107–201 (see below) | – | – | – | – | – |
| src03 | أسئلة_من_مقرر_نظم_المعلومات_الإدارية_MIS.pdf (16 pp) | 134 (numbered 1–134) | 43 | 89 | 2 | 133 | 20 / 51 / 63 |
| src07 | حل أسئلة MIS.docx | 12 items that exist only in src07 (the rest of src07 is attached to src03 items as notes) | 0 | 12 | 0 | 11 | 2 / 3 / 7 |
| src22 | ملخصات سابقة/MIS Q.pdf (24 pp) | 194 (numbered 1–190; 70, 71, 89, 99, 126 each used twice) | 0 | 191 | 3 | 190 | 35 / 58 / 101 |

`marked_by`: src05 = "student-recall" (128) / "worked-answer" (10, the Q&A block copied from src07) / null (55);
src03 = "highlight" (133) — **src03 marks its answers in green text** (some stems yellow = «مهم»); the text
layer loses colour so every content page (p2–p16) was read visually; src07 = "key"; src22 = "key" (a student's
self-study Q&A, each item answered in the file).

## Pages read visually (PyMuPDF, dpi 90, in `extracted/pages_png/`)
- src05: 10 of 23 pages (p1, 2, 3, 7, 10, 11, 12, 13, 14, 15) — text layer is complete but line-broken with
  ligature damage (تعتت = تعتبر, الخبتر ة = الخبيرة, «??» in item 40 is literally in the source). Transcribed
  from text, fixed OCR damage only, verified against the images.
- src03: 15 of 16 pages (p2–p16; p1 is the table of contents) — needed for the green/yellow marking.
- src22: 1 page (p10) to confirm layout — clean text layer, plain Q&A, no colour marking (only a name watermark).
- src06: 0 pages (clean text layer, compared textually with src05).
- Nothing was unreadable. All 4 PDFs rendered (23 + 6 + 16 + 24 = 69 PNGs).

## Dependent-copy findings
1. **src06 ⊂ src05 (verbatim).** src05 pages 16–22 (items 107–201) are src06 in full, in the same order:
   - src06 p1 recall list #1–30 (numbering skips 27) = src05 #107–135 (29 items; e.g. src06 #1 «اي لوحة قيادة
     فيها معلومات اكتر؟ التحليلية» = src05 #107; src06 #30 «الحلال بيعطي، تعظيم، تصغير…» = src05 #135).
   - src06 p2–3 bullet notes with page refs (ص2, ص28, ص4 … ص122) = src05 #136–169 (src05 merges the last two
     bullets on دمج الموارد / تعاون التكميلي into #169).
   - src06 p3–4 «منقول من زميلة» list = src05 #170–192 (numbering jumps 178→188 in both).
   - src06 p4–6 numbered Q&A 1, 2, 3, 7, 8, 9, 10, 13, 14, 19 = src05 #193–201 (src05 folds Q7+Q8 into #196);
     the answer to Q19 (تحليل الحساسية) is cut off at the same word in both files.
   Each of these items is transcribed once with `src: "src05"` and `notes: "also src06 …"` giving the src06
   location. src05 additionally has its own items #1–106 (a different recall set with inline answers) and a
   final lecture-review note (p22–23) that src06 lacks.
2. **src06 p4–6 Q&A = the opening of src07.** The Q&A block (لمحة تاريخية … تحليل الحساسية) is word-for-word the
   first part of the solutions docx (src07, items 1–19). So src06 is itself a compilation from src07 plus recall
   lists.
3. **src07 vs src03.** src07 is a student's answer file whose numbering does NOT follow src03 (src07 «3. متى بدأ
   العمل بمستودع البيانات» = src03 #6; src07 «22.» = src03 #97–99). Answers were matched by content and attached in
   `notes` as «src07: …». Since src03 already carries green answers, `marked_answer` = src03's green text
   (`marked_by: "highlight"`); src07 is quoted in notes, and content that exists only in src07 was transcribed as 12
   separate items with `src: "src07"`. Mismatches found:
   - src03 #26 TPS definition says «لتوفير معلومات مفصلة»; src07 says «ملخصة».
   - src03 #99 «KNITRO Solver»; src07 «KNITRI SOLVER»; src07 merges #98 and #99.
   - src03 #67 dimensions: src07 adds «بعد الترويج»; src03 #91 model base: src07 adds small/large quantitative models.
   - src03 #10 «الإنسان هو نظام يتكون من أنظمة فرعية» (صحيح) vs src07 «الأنسان هو نظام عمل».
   - src03 #83 green answer «تفاعلية فورية» (traditional reporting system gives interactive reports?) — src07 #26
     says traditional = non-interactive, advanced = interactive; source wording is loose (noted).
   - src03 #133 repeats the stem of #131 («يساعد في رفع الكفاءة التشغيلية») but answers «دمج الموارد» (source slip).
4. Cross-file overlap (not dependency): src03's MCQ items 12–16, 24, 32–35, 39, 41–48, 53–59, 70–73, 77, 84–89, 96,
   121 are the same questions as src05 #1–106 (src05 is the recall of the exam that src03 was written for). Two
   answer disagreements: src05 #11 «المعرفة» vs src03 #24 «المعلومات»; src05 #27 «الجواب 2 و 3» vs src03 #53 «1 و3».
   src22 #105/#106 (internal vs external DW sources) and #184/#185 (horizontal vs vertical linkage) have their
   answers swapped relative to src03 and to src22's own later items — flagged in notes.

## Discriminator keyword counts (text layer, whitespace collapsed; ligature-damaged files may undercount)

| file | الأصول التكميلية | بورتر | سلسلة القيمة | الشركة الرقمية | الضبابي | البيانات الكبيرة | NEW total | Solver | حلال | (الجدول) المحوري | Hong | التصفية التلقائية | الساعة | الموجهة بالنماذج | OLD total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| src03 | 0 | 0 | 1* | 0 | 0 | 0 | 1* | 4 | 9 | 0 | 1 | 3 | 1 | 4 | 22 |
| src05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 5 | 0 | 0 | 7 | 5 | 6 | 25 |
| src06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 0 | 0 | 3 | 3 | 5 | 15 |
| src07 | 0 | 0 | 1* | 0 | 0 | 0 | 1* | 3 | 8 | 0 | 0 | 0 | 0 | 5 | 16 |
| src22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 1 | 0 | 0 | 0 | 1 | 6 |

\* the single «سلسلة القيمة» hit in src03/src07 is «دعم سلسلة القيمة والتوريد» inside Hong's framework, not Porter's
value chain. Every file is unambiguously the older course (0 genuine current-book keywords vs 6–25 older-course hits).

## in_book policy used
- true: concept treated in a current-book unit (e-business/e-commerce 2-7, intranet/extranet 2-6, TPS/DSS/ESS
  definitions 2-3, functional systems by management level 2-4, ERP 8-1, supply chain 8-2, DBMS/query 5-2, data
  warehouse/mart 10-3-3, sensitivity/what-if 10-4-1, balanced scorecard/dashboards 10-4-2, data mining 5-3-2,
  neural networks 9-4-4, intelligent agents 9-4-5).
- "maybe": same topic but older-course framing (data/information/knowledge 1-2-1, "dynamic system" feedback,
  Power's data-/knowledge-driven DSS, OLAP dimensions, report types of MIS, dashboard types, EIS features).
- false: history dates, systems theory (open/closed, clock, org chart, work system), McLeod manufacturing/marketing
  subsystems, functional intelligence/research systems, IRS, Excel filter/pivot/Solver/trendline/chart keys, decision
  criteria (Hurwicz, expected value, game theory, Markov), Hong's IOIS framework, database size classes, DM software.

## Items not placed in a chapter
All `in_book: false` items (267) have `ch_guess: null` by design. Every true/maybe item carries a chapter and unit.
Nothing else was left unplaced. No personal data copied (compiler names on src06 p6 and src22 p1 skipped).
