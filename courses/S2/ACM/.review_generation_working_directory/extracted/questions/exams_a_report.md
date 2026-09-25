# Stage 3, group A: exam recalls S23, F23, OLD, general file

Output: `exams_a.json`, 132 items (UTF-8, no BOM, LF). Built by a scratch script, and no source file was modified. Every item has
`src, code, loc, item, qtype, stem, options, marked_answer, marked_by, ch_guess, sub_guess, in_scope, dup_of, book_dup, notes`
(+ `numberless` on calc). `dup_of` is null everywhere. No verbatim re-post was transcribed twice; re-posts are named in `notes`.
Similar questions from *different* recallers inside the OLD pool are flagged "possibly the same as item N" and **not** set as `dup_of`,
because OLD mixes several sittings.

## Counts

| File | Code | Items |
|---|---|---|
| `ACM امتحان يوم 1612.txt` | S23 | 14 |
| `F23 - تلغرام.txt` (#18759, posted 2024-05-12 before the F23 exam by a student who sat the 35-question exam) | S23 | 2 |
| `S23 - تلغرام.txt` | — | 0 (discussion of س11 only; #30569 is a re-post of س11) |
| Kuwait file lines 1–17 (posted 2024-06-08) | F23 | 17 |
| `F23 - تلغرام.txt` (#19507–#19519, internal exam 2024-05-22) | F23 | 16 |
| Kuwait file lines 18–117 (= `دورات أقدم` #8370/#8371 of 2023-10-22) | OLD | 49 |
| `دورات أقدم - تلغرام.txt` (#8371 beyond the Kuwait file, #8176, #8240) | OLD | 33 |
| `عام - تلغرام.txt` «أسئلة غير منسوبة لدورة» (#11910) | OLD | 1 |

| Code | total | mcq with options | mcq free-form | calc with numbers | calc numberless | topic | in scope | partial | out |
|---|---|---|---|---|---|---|---|---|---|
| S23 | 16 | 2 | 9 | 0 | 5 | 0 | 13 | 0 | 3 |
| F23 | 33 | 0 | 21 | 0 | 10 | 2 | 30 | 0 | 3 |
| OLD | 83 | 1 (calc #11910) | 38 | 2 | 20 | 23 | 56 | 6 | 21 |
| **all** | **132** | 3 | 68 | 2 | 35 | 25 | 99 | 6 | 27 |

(OLD's "calc with numbers" are the computers depreciation item, #8371 lines 134–135, and #11910. #11910 is also the one OLD item with options.)
The 6 partial items are all ch 8 computations: EPS, other revenue, non-operating revenue. Chapters by count: ch 10 = 33, ch 7 = 25 (15 of them 7-5, the rest adjustments, which are out), ch 2 = 16, ch 8 = 13, ch 9 = 12, ch 3 = 10, ch 6 = 10, ch 5 = 7, ch 1 = 6.

**Code decisions to confirm:** (1) `F23 - تلغرام.txt` #18605 (2024-05-11) is a re-post of OLD #8371, so it was not transcribed as F23. (2) The 2 #18759 items are coded **S23**, based on their date and the "35 questions" remark, though they sit in the F23 file.

## Images
Read: `كتاب - خطأ مبلَّغ 4108.jpg` (book p. 59: financing sources labelled debit and uses credit) and `كتاب - خطأ مبلَّغ 4111.jpg` (book p. 134, 5-1-4: the purchase-returns closing entry).
Referenced but not available: the Kuwait "الصورة مرفقة" chart, F23 #19357, #8371 "هي الرسمة يلي اجت حرفيا", #11911 (follow-up to #11910), S23 #11541, and all the errata photos in the general file.

## Label → chapter evidence

| Label (source) | Book ch | Evidence |
|---|---|---|
| «المحاضرة الأخيرة» (Kuwait l.5) | 10 | chart answers: break-even point, total cash costs, cash fixed costs |
| «الفصل العاشر / البحث العاشر / المحاضرة العاشرة» (Kuwait l.18–26, 67; #8371) | 10 | charts, break-even, shutdown point, margin of safety |
| «مخطط نقطة الاغلاق بالمحاضرة 10» (Kuwait l.96) | 10 (10-2-3-2) | shutdown chart |
| «بحث تحليل التعادل اخر بحث» (Kuwait l.39) | 10 | named |
| «البحث السابع عن قوانين الاهتلاك» (Kuwait l.69) | 7 (7-5) | depreciation |
| «يمكن بالفصل ٨» (#8371 items ٤–٥) | 8 (8-3) | solvency, financial position |
| «من محاضرات ٢ ل محاضرة ٧» debit/credit (Kuwait l.101) | 2–7 | journal entries |
| «من الفصل الاول نظري» (#8371) | 1 | theory |
| «محاضرة محاسبة التكاليف … ورقمها ٩» (F23 #18759/#397) | 9 | cost accounting |
| YouTube «المحاضرة 9» = inventory count, minutes 13–44 deleted (S23 #11769/#11770, #11641 «محاضرة التسويات الجزء التاني») | 7 (inventory part) | **YouTube numbering ≠ book chapter** |
| YouTube lecture «رقمها 11» for cost accounting (F23 #19086) | 9 | again YouTube ≠ book |
| «الجرد المستمر … بالمحاضرة الخامسة» (S23 #11612) | 5 | perpetual inventory |
| «المحاضرة 3 … الخطوات»; «الرابعة … تمويلية رأسمالية وحركة الاموال» (S23 #11808) | 3; 4 | named content |
| «بالمحاضرة الخامسة … ال4 صح وال5 خطأ» (general #11665) | 5 | = book p. 156 T/F 4–5 |
| «بالمحاضرة التاسعة تشابه المحاسبة المالية مع محاسبة التكاليف» (#30535) | 9 | |
| «بالمحاضرة الثالثة» ledger example (#40742) | 3 | posting |
| «القوائم المالية بالمحاضرة 8»; «نظري المحاضرات 1 و 2 و 9» (#11802) | 8; 1, 2, 9 | |

## Disputed / uncertain answers
- **Item 10 (S23 س11, the cash account at year end):** option index 2 «الصندوق دائما مدين بغض النظر» per #30135 and #30570 («افضل اجابة رقم ٣»). #30571 says options 1 and 2 could both be right «حسب العمليات المصرفية». #30572 and #30573 say the problem is the wording. The same question came up again in F23 (item 31) with no answer.
- Item 53 (OLD, debit 1400 / credit 2000): the recalled answer is «مدين ٦٠٠ او العكس», so the recaller is unsure of the direction. It is `book_dup`: book p. 109 MCQ 4 has debit 2000 / credit 1400.
- Item 100 (OLD, computers 1,600,000, salvage 100,000, accumulated depreciation in 2020): the stem says «القسط الثابت وفق ارقام السنين», which is contradictory. The answer given is "last year, so cost − salvage". The useful life was not recalled.
- Hedged answers («على الأغلب», «يمكن»): items 2, 5, 8.
- Answer text given but not linked to its question: #8371 lines 136–138 («تتسجل من ح زبائن الى حساب الصندوق»), noted on item 101.

## Book errors students reported (general file)

| Book page | What is wrong | Msg |
|---|---|---|
| p. 59 (ch 2) | "financing sources = debit accounts, uses of funds = credit accounts", reversed | MBAF22 #4108, confirmed #4109 (image read) |
| p. 81 (ch 2 T/F 3) | «الحسابات التي تتضمن مصادر التمويل هي حسابات مدينة» keyed صح; should be خطأ | #30265 |
| p. 134 (5-1-4) | purchase-returns closing entry printed «من ح/ملخص الدخل إلى ح/مردودات المشتريات», should be the reverse | MBAF22 #4111/#4112 (image read); also #18304–#18317, #40870/#40874; the same error in the student summary #11679/#11707 |
| p. 136 | closing of the cash discount on purchases: is it «من ح/ملخص الدخل إلى ح/حسم نقدي»? (question only) | #40783 |
| p. 156 (ch 5 T/F 4–5) | closing of opening/closing inventory in the income account: key disputed. #19353, #29700/#29705, #30178 and #36374 say the key is wrong; #11684 and #30177 defend it | several |
| p. 262 | investments held for sale listed under long-term investments (non-current), should be current; unclear whether long-term investments are held for profit | #30441, #30464 |
| ch 2–4 journal/ledger tables | debit/credit columns swapped ("مدين يسار ودائن يمين"), and «من» put on the credit side | #17955–#17984, #19016–#19021 |
| various | wrong numbers in examples and end-of-chapter solutions | #17959, #18205, #41586 |
| (no page) | rent 70,000 in a problem: revenue or expense (disputed) | #19267–#19302 |
| (no page, ch 10 example) | fixed costs 50,000 in the solution vs 100,000 in the text; the BE quantity example has "100 الف" | #19400–#19403, #11924/#11927 |
| (no page, ch 10) | BE value must divide by the CM ratio, not the CM | #30139–#30157 |
| (no page) | debit/credit reversed (#29756); closing entry reversed in the perpetual-inventory lecture, which is deleted (#29817) | #29756, #29817 |
| (no page) | amount should be 750,000 per the text, and the debit account should be cash | #40926 |
| (no page) | book answer wrong: the income statement parts link through operating profit | #46366/#46375 |
| (no page) | accumulated depreciation figure in an entry wrong | #47400 |
| lecture 9 | accrual principle listed as shared with cost accounting, but absent from the ch 1 principles list | #30535 |
| student summary pp. 31/36 | errors copied from the book: should be 40,000; fixed costs should be 50,000 | #30575/#30576 |

## Exam format and scope per sitting

| Sitting | Format |
|---|---|
| S23 (2023-12-16) | all MCQ, ~35 questions (#18759); «جميع الإجابات خاطئة» offered on every question (#12002); time too short (#12195); laptop calculator (#11640); hard, and many questions had more than one plausible answer (#12105) |
| F23 external (Kuwait, 2024-05-20) | 30 MCQ; ~10 from ch 10, including one chart with 3 questions; debit/credit cases; depreciation ×2 |
| F23 internal (2024-05-22) | 11 theory questions (#19507); 2 chart questions (BE and shutdown), points and lines numbered only (#19362); long numbers with no thousands separators (#19563) |
| OLD | 2021 forward: 30 questions, ~9–10 from ch 10, charts. External-centres sitting: 25 questions, none from ch 10, all MCQ, one T/F. Another recall: 7–9 theory, 10–15 practical, 4–5 from ch 10 |
| general | 30–35 MCQ (#18468, #28794, #30528, #40555, #47829); calculator not allowed but the laptop one can be used, scrap paper provided (#30094, #30256, #19410); «غير ذلك» option everywhere (#18990) |

| Sitting | Scope reported |
|---|---|
| S23 | first 10 chapters (#9237). Out: perpetual inventory, installment sales, FIFO/LIFO pricing, multi-product BE (#11583/#11585). Theory only: cash-flow statement, cost statements, cost theories |
| F23 | Out: perpetual inventory wherever it appears, installment sales (not the depreciation methods), FIFO/LIFO/weighted average. Theory only: cash-flow statement (#19430), lecture 9 cost accounting (theories yes, problems no, #18914). #18918 asks whether «مقومات محاسبة التكاليف» is deleted (no answer). Ch 10 not yet announced on 2024-05-12 |
| general | "the deleted parts don't change" (#28651) |

## Not transcribed / unplaceable
- The advice sections of the general file were left out as the brief requires. They do contain pattern recalls (#18990: data-heavy question answered «غير ذلك»; #18998: shutdown-chart questions asking for a line name). Those are the same pattern as S23 item 14.
- #18759: «قسم ما كان موجود بالمسجلة … 5 اسئلة» (section not named).
- Kuwait l.4 «أسئلة نظرية عن المحاسبة» (no topic) and l.64 «وواحد تاني غير».
- #8371 item ١٨ is empty, and the list uses the number ١٧ twice.
- #11910: the fixed cost is written «18000,000» and was not normalised.
- The Kuwait file begins with a sender name; it was not copied into the JSON. «فادي» in item 25 is the fictional party in the question, not a student.
