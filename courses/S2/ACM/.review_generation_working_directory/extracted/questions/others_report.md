# Stage-3 others report — summary + solved_345 (ACM, prompt v0.12)

## A. Summary (`ملخص عاصم`, 30 pages)

All 30 pages read in full (text pages `p001.txt`–`p030.txt`/`p007.txt`.. plus image page `p008.png`,
transcribed to `summary/p008.txt`).

### Coverage map (summary heading → book chapter)

The summary is a straight, numbered theory walkthrough of book chapters 1–10, one heading per
chapter, in order — no chapters skipped or reordered:

| Summary section | Pages | Book chapter | F25 status |
|---|---|---|---|
| 1- المحاسبة وبيئة الأعمال | p001–003 | ch1 | in scope (full) |
| 2- الدورة المحاسبية - التسجيل المحاسبي | p004–010 | ch2 | in scope (full) |
| 3- الدورة المحاسبية - الترحيل وترصيد الحسابات وإعداد القوائم المالية | p009–010 | ch3 | in scope (full) |
| 4- المعالجة المحاسبية للعمليات الرأسمالية | p011–012 | ch4 | **out of scope** (F25 excludes ch4) |
| 5- المعالجة المحاسبية للعمليات التشغيلية | p013–015 | ch5 | **out of scope** (F25 excludes ch5) |
| 6- المعالجة المحاسبية للعمليات الإيرادية | p016–017 | ch6 | **out of scope** (F25 excludes ch6) |
| 7- التسويات الجردية | p018–020 | ch7 | in scope **only for 7-5 اهتلاك (depreciation), no entries** — most of ch7 (accruals, doubtful debts, bank/cash reconciliation, inventory count) and even part of the depreciation MCQs (journal entries, sum-of-years-digits detail, inventory pricing) are outside F25 scope |
| 8- القوائم المالية الختامية | p021–024 | ch8 | in scope (full) |
| 9- تكاليف الإنتاج في الشركات الإنتاجية | p025–027 | ch9 | in scope, **theory only** (matches F25) |
| 10- تخطيط الإنتاج والأرباح | p028–030 | ch10 | in scope (full) |

Chapter boundaries between sections were double-checked against the book's own page footers
where the summary happens to reuse a book exercise verbatim (see below) — no drift found.

### Questions/exercises found

The summary is theory only ("هذا الملخص هو نظري المادة فقط وغير كافي لأنه لا يحتوي على الأمثلة
العملية" — its own note 3 on p001) — it contains **no worked numeric exercises**, but every
chapter section ends with two short quiz blocks: "أسئلة محلولة" (solved — True/False with the
answer in parentheses) and "أسئلة خيارات متعددة" (MCQ — options only, **no answer marked** in the
source, except one item on p020 where the author penciled in a hand-worked computation next to an
option). All of these were transcribed to `extracted/questions/summary.json` (104 items, `src`/`code`
= `SUM`): 52 TF items (all `marked_by: "key"`, answer from the source's own صح/خطأ) and 52 MCQ
items (`marked_answer: null` except the one p020 depreciation item, which carries the source's own
worked note as `marked_by: "worked-answer-in-source"`). Two MCQs on p013/p010 and p015/p156-157
reuse book questions almost verbatim (see cross-check note below); their `notes` field carries the
computed answer for a chapter-helper cross-check but `marked_answer` is left null/unmarked since
the summary itself does not mark them — per FORMAT.md, verification was not performed here.

One internal inconsistency flagged in `notes` for chapter-2 review: the TF item on p007 ("الحسابات
التي تتضمن مصادر التمويل هي حسابات مدينة بطبيعتها") is marked "صح" by the summary's own answer key,
but the summary's own parenthetical remark right after it says "(يجب أن يكون الجواب خطأ)" — i.e. the
author flags his own marked answer as likely wrong. Kept as-is (`marked_answer: "صح"`), with the
contradiction spelled out in `notes` for the chapter-2 helper to resolve against the book.

### Parts the instructor deleted / excluded

- General note (p001, "ملاحظة3"): "هناك أجزاء حذفها الدكتور لم ألخصها" — summary explicitly admits
  gaps for deleted material, not itemised beyond the specific cases below.
- p004 (ch2, closing financial statements list): "قائمة التغيير في حقوق الملكية (**حذفها الدكتور**)" —
  statement of changes in equity explicitly dropped by the instructor.
- p019 (ch7): "جرد المخزون السلعي: (**غير مطلوب كله**)" — full inventory-count subsection marked not
  required.
- p020 (ch7 MCQ): one item explicitly prefixed "(**السؤال غير داخل في الفحص**)" — a weighted-average
  inventory pricing question the author flags as outside the exam.
- Consistent with STAGE3_BRIEF_OTHERS.md's own F25 scope line (ch7 only 7-5 depreciation, no
  entries; ch4/5/6 fully out; ch8/9 theory only) — the summary's own chapter-4/5/6 sections and most
  of chapter 7 were transcribed anyway (per the brief's instruction to transcribe what's found), but
  flagged `out of scope` in each item's `notes`.

### 10–20 definitions/lists a student would memorise (term → summary wording → page)

1. **تعريف المحاسبة** (p001): نظام معلومات يجمّع البيانات عن الأحداث الاقتصادية ويحوّلها لمعلومات
   مفيدة لاتخاذ القرار؛ 3 أنشطة: تحديد، تسجيل، تبويب وتلخيص.
2. **الفروض المحاسبية الستة** (p001): الموضوعية والحيادية، القياس الكمي، الوحدة المحاسبية المستقلة،
   الاستمرارية، الدورية، الوحدة النقدية.
3. **المبادئ المحاسبية** (p001): التكلفة التاريخية، مقابلة النفقات بالإيرادات، الثبات، الإفصاح الكامل،
   الأهمية النسبية، الحيطة والحذر.
4. **معادلة الدورة المستندية** (p005): الأصول + المصروفات = المطاليب + الإيرادات.
5. **القيد المزدوج — خطوات التحليل الأربع** (p006): تحديد الأطراف، تحديد طبيعة كل حساب، تحديد أثر
   الزيادة/النقصان، تحديد الطرف مع الحفاظ على الطبيعة أو عكسها.
6. **رصيد الحساب وخطوات الترصيد** (p009): الفرق بين مجموع المدين والدائن؛ الفرق يظهر بالجانب الأقل
   ويسمى "رصيد مرحل".
7. **تكلفة الأصل غير المتداول** (p011): ثمن الشراء + مصاريف النقل والتأمين + الرسوم الجمركية + أجور
   التركيب + كل نفقة أخرى للتشغيل.
8. **شروط الحسم النقدي** (p013): الصيغة (معدل الحسم/عدد أيام الحسم، صافي عدد أيام السداد)، مثال
   (8/5، صافي 30).
9. **معادلة تكلفة البضاعة المباعة** (p014): بضاعة أول المدة + المشتريات + مصاريف المشتريات − مخزون
   آخر المدة.
10. **أنواع التسويات الجردية الأربعة** (p018): مصروفات مدفوعة مقدما، إيرادات مقبوضة مقدما، مصاريف
    مستحقة الدفع، إيرادات مستحقة القبض.
11. **طرق الاهتلاك الثلاث** (p019) — **7-5، بالنطاق**: طريقة النشاط، طريقة القسط الثابت (= (تكلفة
    الأصل − قيمة النفاية) ÷ العمر الإنتاجي)، طريقة القسط المتناقص.
12. **مبادئ قائمة الدخل الثلاثة** (p021): مبدأ الاستحقاق، مبدأ المقابلة، الدورية المحاسبية.
13. **معادلة صافي الدخل قبل الضريبة** (p022): الدخل من العمليات التشغيلية + المكاسب الأخرى − التكاليف
    التمويلية − الخسائر الأخرى.
14. **التبويبات الرئيسية لقائمة المركز المالي** (p022): إجمالي الأصول = إجمالي الالتزامات + حقوق
    الملكية؛ صافي الأصول = إجمالي الأصول − إجمالي الالتزامات.
15. **تبويب قائمة التدفقات النقدية** (p023): أنشطة تشغيلية، استثمارية، تمويلية.
16. **مفاهيم التكلفة الأساسية** (p025–026): تكلفة رأسمالية مقابل جارية؛ مباشرة مقابل غير مباشرة؛
    خاضعة للرقابة مقابل غير خاضعة؛ معيارية؛ فرصة بديلة؛ غارقة؛ تفاضلية؛ إضافية.
17. **هامش المساهمة ومعدله** (p028–029): هامش المساهمة = المبيعات − التكاليف المتغيرة؛ معدل هامش
    المساهمة = هامش المساهمة للوحدة ÷ سعر بيع الوحدة × 100.
18. **نقطة التعادل** (p029): بالكمية = التكاليف الثابتة ÷ هامش المساهمة؛ بالقيمة = التكاليف الثابتة ÷
    معدل هامش المساهمة.
19. **نقطة الإغلاق المؤقت (نقطة التعادل النقدية)** (p029): = التكاليف الثابتة النقدية ÷ هامش المساهمة
    (تستثني الاهتلاكات وسائر التكاليف الثابتة الدفترية).
20. **هامش الأمان** (p029): بالكمية = مبيعات كلية − مبيعات تعادل؛ معدله = (مبيعات فعلية − مبيعات
    تعادل) ÷ مبيعات فعلية.

## B. Solved unsolved-exercises scan (`حل مسائل غير محلولة الفصول 3 4 5`, 7 pages)

All 7 page images read visually and transcribed in full to `solved_345/p001.txt`…`p007.txt`
(handwritten pages p002, p003, p005, p007 transcribed with `[?]` on any digit/word that stayed
ambiguous after cross-checking against the internal arithmetic of each trial balance).

The 7 pages turned out to be **3 separate problems**, each a printed problem statement (page
straight out of the book) plus its handwritten worked solution:

1. **p001 (statement) + p002+p003 (solution)** — word-for-word the book's own end-of-chapter
   exercise on **book p.132** (chapter 4: partnership formation, sahém's admission with an existing
   business's net assets, furniture purchase, cash transfer, bank loan). Confirmed by matching the
   exact figures (10M → 15M capital, 2,000,000 building / 1,000,000 truck / 2,200,000 goods /
   200,000 payable, 420,000+30,000 furniture, 300,000 transfer, 5,000,000 loan) and the resulting
   trial balance total (20,200,000 = 20,200,000). `ch_guess = 4`, **`in_scope = false`** (chapter 4
   is excluded from F25).
2. **p004 (statement, book p.109 footer visible) + p005 (solution)** — the book's chapter-3 exercise
   ("منشأة الوفاء" — opening capital, car purchase on credit, furniture sale, land purchase/sale,
   partial collection). Confirmed against book p.109 text verbatim and the solved trial-balance
   total (70,000 = 70,000). `ch_guess = 3`, **`in_scope = true`** (chapter 3 is in F25 scope).
3. **p006 (statement, book p.157 footer visible) + p007 (solution, headed "الفصل الخامس" in the
   solver's own hand)** — the book's chapter-5 exercise (purchase on credit from supplier يوسف with
   5/15-net-30 terms, salaries, purchase return, rent, partial and final settlement with the
   supplier, cash purchase). Confirmed against book p.157 text verbatim; the solved cash discount
   (12,500 on a 250,000 partial payment, i.e. 5%) checks out against the stated terms. `ch_guess =
   5`, **`in_scope = false`** (chapter 5 is excluded from F25).

Written to `extracted/questions/solved345.json` (3 items, `src`/`code` = `SOL345`, `qtype: "calc"`,
`marked_by: "worked-answer"`), each with the full journal-entry solution in `marked_answer` and a
`notes` field naming the matching book exercise (page, chapter) and any reading uncertainty.

## Pages/images read visually

- Summary: 1 image page (`summary/p008.png`, account-classification table) + 30 text pages read.
- Solved_345: 7 image pages, all handwritten or printed, read and transcribed in full
  (`solved_345/p001.png`…`p007.png`).
- Book cross-reference pages read for verification: p108–110 (ch3), p131–133 (ch4), p156–158 (ch5).

## Anything unreadable

- `solved_345/p002.png`, `p003.png`, `p005.png`, `p007.png` (handwritten): individual digits are
  written in an abbreviated shorthand (e.g. "٦٠،..." for 60,000, "5 M" for 5,000,000). All figures
  were recovered with confidence by cross-checking against (a) the printed problem statement's own
  numbers and (b) each solution's own trial-balance totals (both problems balance exactly), so no
  `[?]` markers were needed in the final `solved345.json` — the couple of genuinely ambiguous
  handwritten account labels in problem 1's trial balance (p003) are flagged in that item's `notes`
  instead of the transcription proper, since the surrounding numbers made the accounts identifiable
  by elimination.
- Summary table image `summary/p008.png`: fully legible printed table, no ambiguity; transcribed to
  `summary/p008.txt`.
- No personal data encountered in either source (solved_345 handwriting has no names of
  reviewers/students, only the fictional exercise characters سمير/فادي/سهيل/سعيد/وجد/يوسف already
  present in the book's own problem text).
