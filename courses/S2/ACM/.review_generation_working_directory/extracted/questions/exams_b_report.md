# Stage 3, Group B: exam recalls S24 / F24 / S25 (+ F25 scope, advice file)

Output: `exams_b.json`, 160 raw items (106 unique + 54 `dup_of` re-posts inside the same sitting). Built by a
scratch script from the sources, all fields per `FORMAT.md` plus `code`, `in_scope`, `numberless`. `marked_by` is
`student-recall` wherever an answer is given. For the S24 PDF, the answer comes from the worked solution appended
to the PDF itself (pp. 5-9, also posted as #41646). That solution is unofficial and AI-made (#41746) and is not a key.
Names were removed: the poster in F24.txt, and the customers in F24 stems, now written `[اسم]`. A redaction already
in the source, `[محذوف]` in #30830 item 8, was kept.

## Items per file and code (unique items, then how many have options / free-form / numberless calc / topic)

| File | Code | All | Dups | Options | Free-form | Numberless calc | Topic |
|---|---|---|---|---|---|---|---|
| exam_s24.pdf (pp.1-4 questions, pp.5-9 solution) | S24 | 10 | 0 | 10 | 0 | 0 | 0 |
| S24.txt | S24 | 10 | 10 (all = PDF Q1-Q10, verbatim) | – | – | – | – |
| S24 - تلغرام.txt | S24 | 49 | 16 | 4 | 19 | 7 | 3 |
| F24.txt | F24 | 58 | 21 | 9 | 8 | 11 | 9 |
| F24 - تلغرام.txt | F24 | 18 | 6 | 1 | 1 | 4 | 6 |
| S25 - تلغرام.txt | S25 | 15 | 1 | 1 | 2 | 4 | 7 |
| F25 - تلغرام.txt, المطلوب بدوره F25…, طريقة الدراسة.txt | – | 0 | – | – | – | – | – |

In the table, "free-form" means no options were recalled. That includes MCQs where the student gave only the answer:
the exams are all MCQ, so those items keep `qtype: mcq` with `options: []`.
Unique items per code: S24 43, F24 49, S25 14.
Scope of the unique items: S24 26 in, 7 partial, 10 out · F24 34 in, 8 partial, 7 out · S25 7 in, 5 partial, 2 out.
Many items from ch 4-6 are marked `partial` because the same transaction is a ch2 double-entry exercise on book
pp. 71-80: rent collected 50000 (p.77), bank commission on salary transfer (p.75/80), purchase partly cash / bill /
credit (p.73), return of defective goods to the supplier (p.73/80), sales discount. Depreciation items that ask
for the entry are `partial` (7-5-6 is out). Target costing (p.309, after 9-4) is out.

## Image read
- `F24_1.jpg`: the book's temporary-shutdown chart, **labelled** version. Total revenue is the green line from the origin.
  Total cost is red, starting at 100000; total cash cost is yellow, starting at 80000. Fixed cost is dashed at
  100000 and fixed cash cost dashed at 80000. The shutdown point is at 10000 units / 200000 and breakeven at
  12500 / 250000. Students say the exam version had no labels (F24.txt lines 21-22). Its description is in F11-F13 (idx 79-81).
- Photos referenced in the Telegram files were not downloaded: #30725 (S24 chart, green line), #41702 (S24 Q9 discussion),
  #41830 / #41863 / #41902 (F24 exam questions), #40801 (ch9 deletions). Their content is unknown.

## Label → chapter evidence
| Label (file, msg) | Content it refers to | Book chapter |
|---|---|---|
| «من الفصل الأول / السابع / التامن / التاسع / العاشر» (S24 #30830) | prudence, inputs, relevance / unearned revenue, depreciation / assets, current assets / semi-fixed, target costing, capital cost / breakeven | = book ch 1, 7, 8, 9, 10: student labels = book chapters |
| «أول فقرة بالمحاضرة العاشرة» (S24 #30830 item 15) | breakeven assumptions (p.329) | ch10 |
| «المخطط من المحاضرة ال١٠» (F24 #41857), «مسائل من ١٠» (#41812) | shutdown chart, sales mix | ch10 |
| «قيود من الفصول ٤-٥-٦» (F24.txt l.9) | loan, purchases, discounts, delivery terms | ch 4-6 |
| «المحاضرة ٨ … مخزون سلعي … FIFO, LIFO, WA» (F24 #40481/#40484) | inventory pricing | **book ch7 (7-4)**: lecture 8 ≠ chapter 8 |
| «بالمحاضرة ٩ الصفحة ١٣ نظم التكاليف محذوفة» (S24 #2925); «محاضرة محاسبة التكاليف … ورقمها ٩» (طريقة الدراسة) | cost systems | ch9. Conflicts with the lecture-8 evidence above, unresolved (lecture numbering may split ch7) |
| «الفصل السابع تبع التسويات الجردية» (S24 #30596) | adjustments | ch7 |
| «البيع بالتقسيط بالفصل السادس», «التدفقات … بالفصل التامن», «FIFO … بالفصل السابع», «تحليل التعادل ونسب استغلال الطاقة … بالفصل العاشر», «نظريات … بالفصل التاسع» (#5437, #46518) | as named | ch 6, 8, 7, 10 (10-2-3-4), 9 |
| «الفصل الثامن» deleted / «حذف فصل القوائم المالية» (S25 #47329, #47334, #47850) | financial statements | ch8 |
| F25 #51026: «1-2-3-10 كامل؛ 4-5-6 محذوف؛ السابع ماعدا القيود؛ التامن والتاسع نظري؛ من مقومات نظام محاسبة التكاليف لآخر الفصل محذوف» | «مقومات» = 9-4-1 | book chapters |
| «العملي متركز في المحاضرة 10» (F25 #51121); «القيود بالفصول 2-3، الاهتلاك بالفصل 7» (#51122) | practical | ch10, ch2-3, ch7 |

## Disputed / uncertain answers (item index in exams_b.json)
| Idx | Item | Positions |
|---|---|---|
| 3 | S24 Q4 capital | Solution: 4800000, with purchases summed as a debit balance. #41676, #41686, #41689: purchases should not be added (unless they are ending inventory). No consensus (#41740). |
| 4 | S24 Q5 purchase returns | Solution: "Dr purchase returns 500000". #41656, #41657, #41677, #41713: the entry is Dr suppliers / Cr purchase returns, so the answer is «كل ما سبق خاطئ». #41680: purchase returns is the credit side. #41683: it is debit only in the closing entry. |
| 8 | S24 Q9 inventory shortage | Solution: «كل ما سبق صحيح». #41700: only «أمين المستودع مدين 10000» is right. #41701: the closing entry is the reverse. #41706-#41708: income should be Dr 20000, but the options say Cr 20000 / Dr 30000. #41711: Dr storekeeper 10000. |
| 5 | S24 Q6 sales-mix ratio | Solution gives «كل ما سبق خاطئ», computed from units only (62.5%). Nobody objected, but this is AI-made. |
| 32 | S24 price-fall effect | «ارتفاع نقطة التعادل» is only the poster's own choice. |
| 24 | S24 unearned revenue | Answer «جميعها خاطئة لانها التزامات متداولة» although the options include «التزامات قصيرة الأجل». The recall is probably inexact. |
| 67 | S24 relevance | #30830: «قيمة تنبؤية». #41717: «قيمة تنبؤية او تأكدية او كلاهما». |
| 80 | F24 chart, 2nd line | «خط التكاليف الثابتة» (l.25, #41893) vs «التكلفة النقدية الثابتة» (l.56, #41857). #41801 (Riyadh center) recalls a chart answer «خط الايرادات النقدية الكلية» (idx 82). |
| 89 | F24 transport cost | l.28: delivery at the customer's stores, customer paid 100000. l.32: delivery at the company's stores. l.132 and #41927: no transport in the seller's entry. |
| 111 | F24 gross-profit question | #41809 says it came. l.134 and #41946 say no opening/closing inventory or gross profit came. |
| 86 | F24 declining-balance computers | The student's reasoning gives 5000000 accumulated at the end of 2020. Other options are not recalled. |

## Book errors students reported (in my files)
- F25 #50994 (2026-09-18) says there are errors in the book's journal entries («فيه اخطاء بالكتاب بالقيود المحاسبية»),
  but gives no page. No other erratum is in the Group B files; the reported-error images and the errata sections are in
  `عام - تلغرام.txt` (Group A).
- Not an erratum, but related: S24 #30787 says closing entries and the income summary appear without being explained, as do
  adjustments in the final statements.

## Exam format per sitting
| Sitting (date) | Format as reported |
|---|---|
| S24 (2024-11-13) | 30 MCQ (#30758, #41631) with 5 options A-E, often «كل ما سبق صحيح / خاطئ» (#30753). About half are calculations, mostly breakeven (#30758). About a third are indirect theory (#30787). Theory is nearly verbatim from the book (#30793). ~10 easy / 10 medium / 10 hard (#30798). Theory is about half (#41652). 10 practical entry questions are recalled (PDF), plus ~4 chart-naming questions from ch10 (#41647). ~5 ch10 practical questions (#30830). |
| F24 (2025-08-05, Riyadh + internal) | Mostly entries and theory (#41798). More theory than any earlier sitting, easier, time adequate (#41934, #41900). ~5 entry questions (#41857). 3 questions on the unlabeled shutdown chart, the third sitting in a row with it (#41862). The first 2 questions came from ch1 end-of-chapter questions (#41875). Scratch paper was given (#41839) and could not be taken out (#41958). One of the S24 recall set came again (#41796). |
| S25 (2026-04-08) | A good share of theory, taken from the chapter questions (#48038). The doctor repeated theory from earlier sittings, changing one word (#48040). Practical followed the S24 PDF pattern (#48042, #48043). Most options include «كل ما سبق صحيح أو خاطئ» (#48047). Called hard with no easy questions (#48044); few questions, so high failure risk (#48024). |
| undated (طريقة الدراسة.txt) | 35 questions. Numbers have no thousands separators. Time is barely enough. A chart question gives all the data but asks only the name of line 2. |
| F25 (2026-09-26) | Not held at export time; no recall. |

## Scope per sitting (as reported by students)
| Sitting | Scope |
|---|---|
| S24 | First 10 chapters (#27098, #29613). Deleted: perpetual inventory, inventory valuation methods, cash-flow practical (theory in), cost statements practical (theory in), instalment sales (#29930), budgets (#29978), «مسائل التاسع» (#30597). Depreciation and adjustments are in (#30319). |
| F24 | Doctor's list relayed in #5437 (first 10 chapters). Deleted: perpetual inventory; instalment sales (ch6); cash flow theory only (ch8); cost statements and cost theories theory only (ch9); FIFO/LIFO/WA (ch7); only «تحليل التعادل ونسب استغلال الطاقة» in ch10; cost-measurement theories «إطلاع» (ch9). Multi-product breakeven was disputed (#41775 deleted vs #41776, #41980 required). |
| S25 | Same list (#46518). Also: periodic inventory in (#47226); ch9 theory only, with «الأركان الرئيسة / مقومات محاسبة التكاليف» deleted; «الفصل الثامن» listed as deleted (#47334, #47850 «التامن محذوف»); ch 11-12 out (#47982); multi-product breakeven not deleted (#47999). |
| F25 | #51026: ch 1, 2, 3, 10 full; 4, 5, 6 out; «السابع مطلوب كلو ماعدا كلشي قيود»; 8 theory; 9 theory up to «مقومات نظام محاسبة التكاليف». Then #51108-#51115: depreciation is required, only entries are out. `المطلوب بدوره F25…` rewords this as «الفصل 7: الاهتلاك فقط، بدون القيود». **Discrepancy:** the original message says all of ch7 except entries; the file (and this review's scope) says depreciation only. #51101 doubts that 4-6 are out. |

## Unreadable / unplaceable
- The photos listed above were not downloaded.
- F24 #41865 «دفتر الميزانية اتوقع سؤال» (idx 116): topic unclear.
- S25 «مسألتين من التسعير» (idx 148-149): the kind of pricing is unclear.
- S25 year-end cash/bank entry (idx 151): chapter unclear.
- S25 indirect-cost recall (idx 146): the question/option split is ambiguous.
- S24 #41717 was posted 2025-08-04 as "previous semester" questions, so it is kept under S24 as the file does. Several of its
  items (loan, COGS, trade credit) are not in the PDF.
- F24.txt line 151 is one run-on line holding four questions. Its S24 texts were pasted by the student as "same / similar
  came" (idx 87, 100, 101); F24 options were reportedly one-sided (a single account and amount).
- The F24 sale-discount stem (idx 97) keeps its inconsistent terms and dates as written: «(10/5. 30)», sale 1/11, paid 11/9.
