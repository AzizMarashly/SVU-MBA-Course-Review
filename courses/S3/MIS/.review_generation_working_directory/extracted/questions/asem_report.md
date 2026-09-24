# asem.json — ملخص عاصم (src24, code ASM)

Source: `ملخصات سابقة/_ملخص_عاصم_نظم_المعلومات_الإدارية_MIS.pdf`, 34 pages, text in `src24/text.txt`.
The summary follows the current book chapter by chapter (chapters 1–11; **no chapter 12**) and ends each chapter
with «أسئلة محلولة» = T/F list with (صح)/(خطأ) written after each statement, then «أسئلة خيارات متعددة» with the
correct option **underlined** (no letters, no numbering, dash bullets). There are **no definition/short items**
in the solved-question blocks — only T/F and MCQ.

## Counts — 155 items (all with a worked answer, `marked_by` = "worked-answer")

| ch | page(s) | tf | mcq | matches book | remark |
|---|---|---|---|---|---|
| 1 | 3 | 9 | 6 | 15/15 | = book p39–40 set |
| 2 | 6 | 9 | 6 | 15/15 | = book p84–85 set (MCQ 7–12) |
| 3 | 9 | 8 | 6 | 14/14 | = book p123–124 |
| 4 | 13 | 8 | 6 | — | not in scope (IT infrastructure: client/server, Unix/Linux, Java, XML/HTML, open source) |
| 5 | 16 | 8 | 6 | 14/14 | = book p214–215 |
| 6 | 19 | 8 | 6 | — | not in scope (networks: hub, router, protocol, bandwidth, LAN, DNS, VPN) |
| 7 | 21–22 | 8 | 6 | 14/14 | = book p287–289 (T/F p21, MCQ p22) |
| 8 | 24–25 | 7 | 6 | 13/13 | = book p326–327 (MCQ 1 on p24, MCQ 2–6 on p25) |
| 9 | 28 | 8 | 6 | 14/14 | = book p367–369 |
| 10 | 31 | 8 | 6 | 14/14 | = book p416–417 |
| 11 | 33–34 | 8 | 6 | — | not in scope (systems development: IS plan, BPR, TQM, design, unit testing) |
| **all** | | **89** | **66** | **113** | |

`book_dup` = true on 113 items (all T/F+MCQ of chapters 1, 2, 3, 5, 7, 8, 9, 10); `notes` carries
"book:<page>:<item>". Stems and options are verbatim copies of the book (same order, same wording, same option
order) — I therefore reused the book transcription for those stems. The book's discussion/essay questions are
NOT reproduced by the summary. The summary's items are unnumbered; `item` = null, order = book order.

## Answers vs the book
For all 113 duplicated items the summary's answer is **identical** to the book's printed tick/highlight
(compared item by item on the rendered pages). It adds a short reason on a few T/F items, kept in `notes`
(ch1 T/F 4 «خطأ - تنتج المعلومات», ch4 «خطأ - الموزعة», «خطأ هم SAP و Oracle», «خطأ بالعكس», ch5 «علامة مثلث», «كبير»).

## Doubtful answers (flagged only, not verified)
- ch6 T/F 6 «يمكن أن ترتبط شبكات LAN بشبكات واسعة … باستخدام الإنترنت» — marked (خطأ .؟؟) by the author himself;
  the statement reads as true.
- ch6 T/F 7 «تتصل معظم المنازل … موفر خدمة إنترنت مثل Microsoft Network» — marked (صح).؟؟ by the author.
- ch6 MCQ 3 «جزء الشبكة الذي يعالج حركة المرور الرئيسية» — «العمود الفقري» underlined but followed by
  «(أشك في الجواب؟؟)». Transcribed with the remark moved to `notes`.
- ch6 MCQ 1 has only three options (as printed).
- (Inherited from the book, not the summary's fault:) ch5 T/F 4 answered خطأ, see book_report.md.

## Pages read visually
15 pages rendered to `pages_png/src24_p003…034.png` (dpi 100) and read: 3, 6, 7, 9, 13, 16, 19, 21, 22, 24, 25,
28, 31, 33, 34 (p7 turned out to be chapter-3 prose, no questions). Needed because the MCQ answer is marked only
by underlining, which the text layer drops; the text layer is also badly garbled (the letter «ي» is split off
words everywhere), so the stems of the non-book chapters 4/6/11 were read from the images. Nothing unreadable.

## Curriculum discriminator (§2) — src24/text.txt
Current-book keywords: إدارة المعرفة 14, ذكاء الأعمال 14, سلسلة القيمة 4, Big Data 3, مستودع البيانات 2,
(التجارة الإلكترونية written without ال-prefix in the file, 0 by exact match but the ch7 block is present).
Older-course keywords: Solver 0, جدول محوري 0, نظم دعم القرار الموجهة بالنماذج 0, النظم المفتوحة 0, معايير التصفية 0,
OLAP 2, Pivot 1 (both inside the ch10 BI prose, which the current book also mentions).
→ The summary is unambiguously a summary of the **current** book. `in_book` = true for the 113 book duplicates,
"maybe" for chapters 4, 6, 11 (topics exist in the book's out-of-scope chapters, no audit unit).

## Dependent-copy finding
src24 chapters 1/2/3/5/7/8/9/10 = the book's own review sets, verbatim, with the book's own answers. Any other
source that lists these stems in this order is most likely copied from the book or from this summary, not an
independent recall.
