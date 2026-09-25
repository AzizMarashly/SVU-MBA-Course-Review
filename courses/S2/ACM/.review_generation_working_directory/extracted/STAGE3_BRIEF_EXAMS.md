# Stage-3 brief — transcribe every exam recall (ACM review v1.0, prompt v0.12)

Course «المحاسبة للمديرين — Accounting for Managers (ACM)», textbook `Course/كتاب المحاسبة للمديرين.pdf` (د. باسل أسعد, 447 pages,
printed page = PDF page). Work only inside W = `C:\Users\root\SVU-MBA-Course-Review\courses\S2\ACM\.review_generation_working_directory`.
`PYTHONUTF8=1` for python. Never modify a source file. No personal data in the JSON (the files are already anonymised; skip any name you meet).

## The book as the map — and the F25 scope
- Chapter list of the book (12 chapters): 1 المحاسبة وبيئة الأعمال (pp. 12–40) · 2 الدورة المحاسبية: التسجيل، حسابات الميزانية والنتائج، القيد المزدوج (41–83) ·
  3 الترحيل والترصيد وميزان المراجعة والقوائم الختامية (84–110) · 4 العمليات التمويلية والرأسمالية وحركة الأموال: رأس المال، القروض، اقتناء الأصول، الصندوق والمصرف والشيكات (111–133) ·
  5 المشتريات ومصاريفها ومردوداتها والحسم المكتسب، المصروفات، تكلفة البضاعة المباعة والجرد الدوري/الدائم (134–158) ·
  6 الإيرادات: المبيعات ومردوداتها ومسموحاتها، الخصم التجاري وخصم الكمية والخصم النقدي الممنوح، شروط التسليم، البيع بالتقسيط، الإيرادات الأخرى (159–187) ·
  7 التسويات الجردية: المصروفات المدفوعة مقدماً والمستحقة والإيرادات المقبوضة مقدماً ومستحقة القبض، الديون المعدومة والمشكوك فيها، تسوية المصرف وجرد الصندوق، جرد المخزون وطرق تسعيره، الاهتلاك وطرقه (188–241) ·
  8 القوائم المالية الختامية: قائمة الدخل، المركز المالي، التدفقات النقدية (242–289) · 9 أساسيات محاسبة التكاليف: مفاهيم التكلفة، نظام محاسبة التكاليف، نظريات وطرق قياس التكاليف (290–324) ·
  10 تخطيط الإنتاج والأرباح: سلوك التكاليف، هامش المساهمة ومعدله، نقطة التعادل وطرقها، تخطيط الربح، نقطة الإغلاق المؤقت، هامش الأمان، تعدد المنتجات (325–357) · 11 الموازنات (358–388) · 12 التحليل المالي (389–447).
- Units in scope with page ranges: `W\extracted\book\subsections.json` → `units` (codes chapter-first, e.g. `10-2-3-3` = هامش الأمان). Book text per page: `W\extracted\book\pNNN.txt`.
- **Students' labels are not the book's numbering.** «المحاضرة العاشرة» in a message may mean lecture 10 (= book ch. 9) or chapter 10; «الفصل العاشر» / «بحث التعادل» = book ch. 10; «المحاضرة الأخيرة» = ch. 10 (lectures 11–14 were never required). Assign `ch_guess` **by content** through the chapter list above, never by the label; record every label → chapter mapping you used, with evidence, in the report (it feeds the chapter map).
- **F25 scope** (this review's scope): ch 1, 2, 3, 10 in full; ch 7 only depreciation (7-5: asset cost, capital vs revenue expenditure, depreciation concept and methods, depletion/amortisation) **without** depreciation journal entries; ch 8 and 9 theory only (9 up to the definition of the cost accounting system, p. 302); ch 4, 5, 6 out. Set `in_scope`: `true`, `false`, or `"partial: <why>"` (e.g. a depreciation question that asks for the journal entry). Transcribe out-of-scope items too — they are counted in the methodology.

## Sources and codes (one independent source = one exam sitting; files of the same sitting share the code)
| Code | Files in `courses/S2/ACM/Exams/` |
|---|---|
| S23 | `ACM امتحان يوم 1612.txt` (exam 2023-12-16), `S23 - تلغرام.txt` |
| F23 | `مركز خارجي – الكويت، تاريخ الامتحان 20.05.2024..txt`, `F23 - تلغرام.txt` — **but** the long block in the Kuwait file that begins «الفصل العاشر جاب منو 9 أسئلة» and the lines after it were first posted in Oct 2023 as WhatsApp forwards (one dated 17/11/2021): those items belong to **OLD**, not F23. `دورات أقدم - تلغرام.txt` holds the originals with partial-duplicate notes — use it to decide which lines of the Kuwait file are older, and give each such item `code: "OLD"` with `notes` naming both files. |
| S24 | `ACM Exam S24.pdf` (text: `W\extracted\exam_s24\pNNN.txt`; 9 pages, the written exam questions), `S24.txt` (10 practical questions — check whether they duplicate the PDF: `dup_of`), `S24 - تلغرام.txt` |
| F24 | `F24.txt`, `F24_1.jpg` (read it with the Read tool: it is the chart mentioned in F24.txt), `F24 - تلغرام.txt` |
| S25 | `S25 - تلغرام.txt` |
| OLD | `دورات أقدم - تلغرام.txt`, plus the section «أسئلة غير منسوبة لدورة» of `عام - تلغرام.txt`, plus the older lines of the Kuwait file (above) |
| — (no items) | `F25 - تلغرام.txt`, `المطلوب بدوره F25 بالامتحان.txt` (scope only), `طريقة الدراسة.txt` (advice), the other sections of `عام - تلغرام.txt` (scope history, book errata, advice): read them, transcribe nothing, but list in the report the **book errors students reported** (page, what is wrong, message id) and the **exam format per sitting**. |

`src` = the file name (or `"exam_s24.pdf"`), `code` = the sitting code above, `loc` = message id (`#30719`) or PDF page or line, `item` = the item number as written or null.

## Rules
- Format: `W\extracted\FORMAT.md` (`qtype`: mcq | tf | short | essay | calc | topic). Faithful transcription: the recalled wording verbatim in `stem`, options exactly
  as written, `marked_answer` = what the students said the answer was (or the answer the discussion settled on — put the discussion in `notes`, name the disagreement), `marked_by: "student-recall"`.
  Never resolve a disputed answer yourself and never complete a missing option.
- **One raw item per recalled question.** A message listing ten questions gives ten items. A recalled *problem type without numbers* («جاء سؤال عن القسط المتناقص 5 سنين», «مسألة حساب معدل هامش المساهمة») is `qtype: "calc"` with `numberless: true` — it counts later as frequency evidence on the records of that problem type (§5c); a bare topic with no question at all («اجا عن الاستنفاذ») is `qtype: "topic"`.
- The same question re-posted inside one sitting (re-posts, «تجميعة تانية») is transcribed once; later copies go to `dup_of` (index of the first). A question that appears in two sittings is transcribed under each sitting (different code) — the consolidation pass merges them.
- Numbers: keep the digits exactly (Arabic-Indic digits → ASCII is fine); amounts such as `٦ مليون` stay as written plus a normalised value in `notes`.
- Chart questions (نقطة التعادل / نقطة الإغلاق chart with unlabeled lines): one item per sub-question if the recall lists them (e.g. «خط التكاليف الكلية النقدية، خط التكاليف الثابتة، نقطة الإغلاق»), else one item describing the chart, `notes` naming what was asked.
- `ch_guess`, `sub_guess` (unit code) for in-scope items; for out-of-scope items `ch_guess` and a short topic in `sub_guess` (e.g. `"5: مردودات المشتريات"`).

## Output
Group A: `W\extracted\questions\exams_a.json` + `exams_a_report.md` (S23, F23, OLD, the general file). Group B: `W\extracted\questions\exams_b.json` + `exams_b_report.md`
(S24, F24, S25, F25, the advice file). UTF-8 without BOM. Report: items per file and per code (with options / free-form / numberless calc / topic), in-scope vs out, images read, the label → chapter evidence
table, the disputed answers (item index, positions, who says what), the book errors students reported, the exam format and scope per sitting in two short tables, anything unreadable or unplaceable.
