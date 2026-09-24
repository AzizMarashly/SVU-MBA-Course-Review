# others_b — stage-3 transcription report (codes OQ4, OQ5, OQ6-CANDIDATE)

Output: `others_b.json` — 188 items (130 short, 27 mcq, 16 tf, 15 topic). in_book: true 35 / maybe 41 / false 112.

## Items per file

| code | src | file | items | with options | free-form (short/tf) | topic-only | answered |
|---|---|---|---|---|---|---|---|
| OQ4 | src16 | دورات/اسئلة سابقة/دورات.pdf | 58 (50 key items + 8 from the screenshot page) | 4 | 52 | 2 | 41 |
| OQ4 | src09–src15 | MISS/IMG-*.jpg (7 photos) | 0 separate items — pixel-identical to src16, see below | | | | |
| OQ5 | src21 | دورات/ملاحظات_مقرر_MIS.pdf | 76 (49 numbered notes p1–2 + 27 exam-recall items p3–8) | 13 | 60 | 3 | 59 |
| OQ5 | src04 | دورات/اسئلة MIS_امتحان_2019.docx | 24 | 10 | 4 | 10 | 1 |
| OQ6-CANDIDATE | src01 | دورات/MIS_محدد عليه اسئلة الدورات.pdf | 30 (first 30 question-like sticky notes) | 0 | 30 | 0 | 30 (highlight) |

## Pages / images read visually
- src16: all 24 pages rendered to `pages_png/src16_p001..024.png`; 11 pages read with the Read tool (p1–9, p21, p23). The other 13 were not read because the PDF embeds only 7 distinct images and every page is one of them (checked by xref + md5 of the embedded JPEG streams: p1=p2=p19=p20, p3=p4=p11=p12, p5=p6=p17=p18, p7=p8=p13=p14, p9=p10=p15=p16, p21=p22, p23=p24). Photos are of a laptop screen showing a 2-page Word/PDF answer key at 150 %; items 1–50 all legible; nothing unreadable.
- src09–src15 (7 JPGs): compared pixel-by-pixel (PIL, grayscale) with the 7 embedded images of src16 — max pixel difference 0 for every file. Mapping: src09 WA0053 = key items 31–42 (p1); src10 WA0054 = items 12–26 (p3); src11 WA0000 = items 26–30 (p5); src12 WA0001 = items 42–50 (p7); src13 WA0002 = items 1–11 (p9); src14 WA0009 = phone screenshot of a Word doc (p21); src15 WA0036 = photo of a textbook page (p23). So the 7 photos ARE the PDF (the PDF is just the photos repeated 2–4 times); items were transcribed once under src16 with the JPG id in `notes`.
- src15 / src16 p23 is not part of the key: it is a rotated photo of a printed page of the OLD textbook (section «مفهوم التنقيب في البيانات», definition of DM citing Berry & Linoff 2004) — a textbook page, no questions. Not transcribed.
- src16 p21 (= src14): screenshot of "New-Microsoft-Office-Word-Document-1.docx" on a phone with 8 question-like items (pivot table areas, AutoFilter, Solver convergence, systems supporting middle/upper management, CAM definition, system dynamics = feedback, a truncated forecasting question). Transcribed as 8 OQ4 items with loc p21. Bottom of the screenshot is cut off (last question truncated).
- src23 (MIS_F19_Anan.pdf, 54 pp handwritten summary): rendered p1, 2, 10, 25, 40, 54. p1/p40/p54 = credit/title cards, p2 = note that the summary covers only the theoretical part, p10 and p25 = handwritten summary pages (types of IS by level / decision-support sources). No questions found; contains a student's name on the title card (not copied).
- src01: rendered p1, 2, 3, 19, 43, 84, 118 and read p1, 19, 43, 84, 118. See OQ6 below.

## Dependent-copy findings
- src09–src15 == src16 (pixel-identical; item-level: src13 shows items 1–11 «في الخمسينيات … يعمل بمفهوم لوحة القيادة», src09 shows 31–42 «داخلية و خارجية … نظم معلومات التنفيذيين», etc.). One independent source, code OQ4.
- The src16 key answers items of an exam whose questions are not in this group; items 5, 13, 38, 40, 48 are cross-references («آخر ملف», «قلناها فوق», «الملف الثالث صفحة 3», «الجداول في الملف الثاني», «حكيناها فوق»), and 14 items are «؟؟؟» (2, 4, 15–18, 20, 21, 23–25, 30, 36, 46) — recorded with marked_answer null.
- src21 p3–8 (exam recall, «اجا 50 سؤال») and src04 (exam of 24/1/2019) overlap heavily in topics (open/closed systems, clock, knowledge vs information, intranet/extranet protocols, teleconference = communication-driven DSS, AutoFilter, Solver save model, convergence, advanced EIS) but the wording differs and src04 has extra items (knowledge base, e-business, algorithms models, DSS definitions) — treated as two recollections of the same older-curriculum exam style, both under OQ5 as instructed; no dup_of set between files.
- src21 items 12 and 21 are the same statement (noted).

## Excluded-file checks
- src17 (تعريفات_مادة_نظم_المعلومات_MIS.pdf, 7 pp): a two-column definitions table («تعريف / مثال»: EDI, النظام, النظم المغلقة/المفتوحة, نظام العمل, الأعمال الإلكترونية, سلسلة التوريد, دمج الموارد, التعاون التكميلي, VAN …). Zero question marks, no numbered questions — confirmed: no exam questions. Not transcribed.
- src01 (MIS_محدد عليه اسئلة الدورات.pdf, 130 pp, text layer present but font-damaged): the OLD textbook by **د. سليمان عوض** (header on every page «د. سليمان عوض»; p1 title «مقدمة عن نظم المعلومات في منظمات الأعمال — لمحة تاريخية عن تطور نظم المعلومات»; chapters on IS history, systems theory, functional IS (Mcleod & Schell), data warehouses/OLAP, pivot tables, Solver, model-driven DSS, EIS/balanced scorecard, data mining, inter-organizational systems). Marking = 207 cyan Highlight annotations + 52 sticky-note (Text) annotations; the sticky notes hold the question wording (e.g. p4 «الساعة نظام ؟», p43 «من ادوات المخرجات في مستودع البيانات DW:», p118 «ما الهدف من تحليل المجموعة المتجانسة؟») and the highlight on the same page is the answer. **Recoverable: yes**, via the annotation layer (question from the note, answer from the highlighted passage). Caveat: the PDF text layer is garbled by font encoding (e.g. «الخمسييينات», «ظةم معمومةاتهم»), so highlighted answers were reconstructed from the rendered pages where read (p1, 19, 43, 84, 118) and otherwise summarised from the damaged text — flagged in `notes`. Transcribed the first 30 question-like notes (skipping pure comments such as p33 «في سنوات سابقة الدكتور قايل…», p59 «سؤال بس ما عرفت عن شو», p126 «هذه الفقرة مهمة») as OQ6-CANDIDATE; 22 further notes remain (p86–p129: statistical models, Solver small models, large models, sensitivity analysis, EIS characteristics, balanced scorecard, dashboards, data mining methods, neural nets vs decision trees, complementary cooperation).
- src23: no questions (see above).
- src08 (info.txt): two students' experiences — the course is heavy, attendance carries marks, theory is the hard part, «ملخص عاصم» is enough to pass with a good mark, the exam was easy-to-average; final line «داخل اول 10 ومحذوف 4 و 6» (exam covers chapters 1–10, chapters 4 and 6 removed). No questions.

## Discriminator counts (regex on `extracted/srcNN/text.txt`)
NEW-book keywords: بورتر, سلسلة القيمة, التجارة الإلكترونية, إدارة علاقات العملاء, البيانات الكبيرة, الأنظمة الخبيرة.
OLD-course keywords: Solver, الجدول المحوري, OLAP, التصفية المتقدمة, هونغ, المغلقة, درجة التقارب, الموجه بالنماذج.

| file | NEW hits | OLD hits | verdict |
|---|---|---|---|
| src01 | 1 (سلسلة القيمة 1) | 55 (Solver 23, OLAP 23, الجدول المحوري 7, التصفية المتقدمة 1, درجة التقارب 1) — text layer damaged, real counts higher | OLD |
| src04 | 0 | 5 (Solver, OLAP, التصفية المتقدمة, المغلقة, درجة التقارب) | OLD |
| src16 | 0 (no text layer) | 0 — visually: Solver/pivot/AutoFilter/dashboard/Hong dimensions items | OLD |
| src17 | 0 | 5 (OLAP 2, المغلقة 2, التصفية المتقدمة 1) | OLD |
| src21 | 0 | 11 (OLAP 6, الجدول المحوري 2, درجة التقارب 2, الموجه بالنماذج 1) | OLD |
| src23 | 0 (no text layer) | 0 — visually a summary of the old course (decision-support sources, مصادر دعم القرارات) | OLD |
| src08 | 0 | 0 | n/a |

All files in this group belong to the older curriculum (Dr Suleiman Awad). `in_book` was set per item: true only for concepts with a unit in the current TOC (e-business/intranet/extranet 2-6/2-7, data/information 1-2-1, functional systems 2-4, semi-structured decisions 10-1-2, BI tools/data warehouses & marts 10-3-3/10-3-4, OLAP & data mining 5-3-2, neural nets/decision trees 9-4-4, expert systems/agents 9-4-1/9-4-5, balanced scorecard/ESS 10-4-2, sensitivity/what-if 10-4-1, DBMS/query 5-2-1/5-2-2, ERP 8-1-1); maybe for management-level examples, DSS definitions, MIS report types, work-system vs IS components; false for history dates, systems theory, Excel/Solver/pivot, processing levels, Hong's inter-organizational taxonomy, Awad-specific items.

## Could not place in a chapter
All `in_book: false` items (112) carry ch_guess null by design. Key items with «؟؟؟» or cross-references have no content to place. src16 item 32 («صح») and src21 item 38 (student did not hear the answer) are content-less.
