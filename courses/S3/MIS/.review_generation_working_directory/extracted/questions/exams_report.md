# exams group — stage-3 report (src20 دورات.txt, src19 حل دورتين Mis.pdf, src18 حل دورة mis 38-60 scan)

Output: `exams.json` — 157 items, all with `src: "src20"` (src19 and src18 are folded into `notes` /
`marked_answer` of the src20 items; they add no independent question).

## Totals

| block (src20 دورات.txt) | code | items | mcq | short | topic | answered |
|---|---|---|---|---|---|---|
| 1 «اسئلة mis يلي قدرت تذكرتا … S25» (38 numbered) | S25 | 37 | 1 | 35 | 1 | 25 student-recall |
| 2 «حل دورات لمادة mis» (answer key, 37 entries: ١…٣٥ with ١٢ and ٣٢ each used twice) + 3 «اسئلة MIS اجت 44» recall | R44 | 43 (37 key + 6 recall-only topics) | 4 | 32 | 7 | 35 worked-answer |
| 4 «أسئلة MIS فصل F24 مركز خارجي» (60 numbered) | F24 | 60 | 0 | 60 | 0 | 57 (13 student-recall, 21 worked-answer from src19, 23 key from src18) |
| 5 after the last «-----» (17 topic lines) | F24 (notes: unknown sitting) | 17 | 0 | 0 | 17 | 0 |
| **total** | | **157** | 5 | 127 | 25 | 117 |

Per code: S25 37, R44 43, F24 77 (60 + 17 topic lines). `in_book`: true for all but R44-13 «نشر ممنهج» (maybe).
S25 item 8 is not a question («في لسى كم سؤال عن الفصل الثاني بس ما تذكرتن») — skipped, hence 37 not 38.

## Block 2 ↔ block 3 (same 44-question sitting)

Block 2 is the answer key of the sitting recalled in block 3: the first 24 block-3 lines follow the key's
order exactly — l.110 المحول = key 1; l.111 (ادارة تكنولوجيا + مرافق التكنولوجيا) = key 2+3; l.112 اصغر وحدة = 4;
l.113 كيان = 5; l.114 الايراد المجاني = 6; l.115 Save/TPS = 7; l.116 امازون = 8; l.117 اجرائيات العمل = 9;
l.118 السياسة التنظيمية = 10; l.119 منصة = 11; l.120 الموازنة السنوية = 12a; l.121 TCP/IP = 12b; l.122 النشر
الممنهج = 13; l.123 نظرية تكلفة المعاملات = 14; l.124 رأس المال التنظيمي = 15; l.125 النطاق الترددي = 16;
l.126 نظام المعلومات = 17; l.127 الحكمة = 18; l.128 ذكاء الاعمال = 19; l.129 منهجية تطبيق النظم = 20; l.130 ESS = 21;
l.131 كرة الثلج = 22; l.132 البرمجة = 23; l.133 القرارات غير المهيكلة = 24. The «اجى كمان» list (pasted twice,
counted once) maps to key 27, 26, 17, 28, 29, 30, 31, 32a, 32b, 4/5, —, 1, —, 16, 34, 33, 22, 35, 18, —, 25, —, 23, 20, —,
19, — in that order. Block 3 supplies options for key items 1, 4, 12a, 20 (set as `mcq`) and the scenario of 20.
Six block-3 lines have no key entry and were added as `topic` (اعتماد البرامج ع البيانات، طبقة واجهة الشبكة، تطبيق
الحكمة، جودة المعلومات، هندسة البرمجيات باستخدام الحاسوب، خدمات البنية التحتية) → 37 + 6 = 43 ≈ the 44 recalled.
Oddities kept in `notes`: key 11 marks «*Mis*» under a stem whose block-3 answer is «منصة التحويل/التسليم»;
key 12a marks ESS for the annual budget; key 20 has options but no marked answer (block 3 hints الدراسة النموذجية);
key 29 has ESS in the stem and MIS as the answer.

## src19 = dependent copy (no items transcribed from it)

src19 pages 1–3 reproduce block 2 word for word (same numbering incl. the duplicated ١٢/٣٢, same typos «TPC/IP»,
«محللول» fixed to «محللو»), plus three insertions taken from block 3: item 13 gets the parenthetical «ما كتير ذاكرة…»,
item 14 spells out «(تكلفة المعاملات)», item 20 gets the options «تدريجي/موازي/نموذج/مباشر». Pages 3–11 then
reproduce block 4 (F24 items 1–60, header «أسئلة MIS فصل F24» without «مركز خارجي») and paste the book definition
under 42 of them (2–16, 19, 21–28, 32, 34, 40–42, 44, 46, 48–51, 53–54, 56–60; item 30 marked «مكرر»). So src19 is
a merged copy of blocks 2+3+4 with worked answers, not a separate sitting. Every R44 item carries «src19 p.1-3» in
`notes`; every F24 item names its src19 page and whether a definition is pasted; F24 items 1–37 without a student
answer take the src19 definition as `marked_answer` with `marked_by: "worked-answer"`.

## src18 scan (F24 items 38–60)

All 50 pages rendered at dpi 70 and read (50/50). Order is reversed (60 → 38); each item is a phone-screenshot
card of the block-4 line followed by a photo/screenshot of the book passage with the answer term highlighted.
Page map: 60 p1-2 · 59 p3-4 · 58 p5-6 (card again p8) · 57 p7, p9, p11 (p10 is the adjacent Virtualization text) ·
55 p12-13 · 56 p14-15 · 54 p16-17 · 53 p18-19 · 52 p20 (card only) · 51 p21-22 · 50 p23-25 · 49 p26-28 · 48 p29-30 ·
47 p31-32 · 46 p33-35 · 45 p36 (card only) · 44 p37-38 · 43 p39-40 · 42 p41-42 · 41 p43-44 · 39 p45-46 · 40 p47-48 ·
38 p49-50. Items 45 and 52 have no book excerpt (their `marked_answer` is the card's parenthesis). No page was
unreadable; the phone screenshots (p26, p31, p39) are small but legible.

## S25 ↔ F24 overlaps (same question in two sittings, S25 item → F24 item)

2→43 التميز التشغيلي · 7→10 CRM · 10→17 المنتجات والخدمات البديلة · 13→1 قانون ميتكالف · 14→8 IaaS ·
16→33 تكرار البيانات وعدم الاتساق · 18→24 قاموس البيانات · 24→45 الجزء العلوي من سلسلة التوريد · 27→49 التعلم
التنظيمي · 30→60 الوكيل الذكي · 31→56 نشر النتائج · 33→54 الأدوار الإعلامية · 37→9 الدردشة (13 clear pairs);
looser: 29→44 الأنظمة الخبيرة, 34→32 تحصيل البيانات, 32→12/30 (unstructured vs structured decisions).
S25 ↔ R44: 6→28 KWS, 32→24. R44 ↔ F24: 17→39 نظام المعلومات, 11→36 منصة التسليم, 35→42 التسويق المباشر,
19→46 ذكاء الأعمال, 9/27→27 إجراءات العمل, 2→19 تكنولوجيا المعلومات. All recorded as `dup_of` (later item → earlier index).

## Curriculum discriminator (§2)

Current-book keywords (ذكاء الأعمال, سلسلة التوريد, Hadoop, القوى التنافسية, التميز التشغيلي, الوكيل الذكي):
src20 = 11/5/2/3/2/1, src19 = 8/3/2/3/1/2. Older-course keywords (Solver, pivot/المحورية, Hong, الموجهة بالنماذج,
OLAP, النظم المفتوحة/المغلقة): 0 hits in both. src18 is image-only but every excerpt is a page of the current
book (SVU header, Laudon 2020 source lines). All three files belong to the current curriculum.

## Placement

One item without a chapter: R44-13 «نشر ممنهج/مبرمج» (term not in the TOC). Out-of-scope chapters used:
ch 4 (Metcalfe, IaaS, open source, web services, XML, infrastructure eras/services — 12 items), ch 6 (switch,
router, WAN, TCP/IP layers, bandwidth, chat, newsgroups, VoIP, ISP, digital signals, SDN, the Web — 16 items),
ch 11 (programming, conversion strategies, CASE — 3 items). Answers were not verified against the book.
