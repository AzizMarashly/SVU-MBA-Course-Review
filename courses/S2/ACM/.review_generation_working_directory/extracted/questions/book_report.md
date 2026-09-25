# Stage 3 — BOOK questions: report

Output: `extracted/questions/book.json`, 98 items, UTF-8 without BOM, LF line endings. Built from the per-page text in
`extracted/book/pNNN.txt`, checked against page renders in `extracted/pages_png/` (gitignored).

## Counts per chapter and type

| Ch | tf | mcq | essay | unsolved exercises (calc) | case items (worked answer) | in scope | out of scope / other |
|---|---|---|---|---|---|---|---|
| 1 | 6 | 5 | 1 | – | 0 | 12 | – |
| 2 | 6 | 5 | 1 | – | 1 | 13 | – |
| 3 | 6 | 5 | – | 1 | 1 | 13 | – |
| 7 | 5 | 5 | – | 3 | 2 | 3 (T/F 5, MCQ 3, MCQ 4) | 11 out + 1 partial (Case 1 (a)) |
| 8 | 5 | 5 | – | – | 4 | 10 (T/F + MCQ) | 4 cases `in_scope: "theory-only chapter"` |
| 9 | 6 | 5 | – | – | – | 5 (T/F 3–4, MCQ 1, 2, 4) | 6 out |
| 10 | 5 | 5 | – | 4 | 6 | 20 | – |
| **Σ** | 39 | 35 | 2 | 8 | 14 | 76 | 22 |

Out-of-scope items and their topics:
- **Ch 7:** T/F 1–4 (adjustments, accrual, accrued revenue, bank reconciliation); MCQ 1 (weighted average, 7-4-2-3); MCQ 2 (lower of cost or market, 7-4-3); MCQ 5 (depreciation entry, 7-5-6); Exercises 1–3 (bad debts 7-2-2, cash shortage 7-3-2, inventory loss 7-4-4); Case 1 (b) (final statements after all adjustments).
- **Ch 7 Case 1 (a):** `in_scope` is a string, "partial". Only the two depreciation amounts are in scope (machines 40,000, computers 70,000; 7-5-4-2).
- **Ch 9:** T/F 1 (9-4-1-3), T/F 2 (9-5-1), T/F 5 (9-5-4-5), T/F 6 (9-5-4-4), MCQ 3 (9-4-1), MCQ 5 (9-5-4).

Unsolved exercises are marked `unsolved: true`. There are 8: ch 3 p. 109 (1), ch 7 pp. 240–241 (3), ch 10 pp. 354–356 (4). The ch 3
exercise is printed as «3) تمرين غير محلول» but was not in the brief's page list.

## Does the book mark its answers? Yes
- **T/F:** every T/F table has a ✓ printed in the صح or خطأ column. These are recorded as `"صح"`/`"خطأ"` with `marked_by: "key"`.
  Seen on pp. 38, 81, 108, 238, 287–288, 322, 353.
- **MCQ:** the correct option is highlighted green. These are recorded as a 0-based index with `marked_by: "highlight"`. Seen on pp. 38–39, 81–82,
  108–109, 238–239, 288, 323, 353–354.
- **Essay and discussion questions** (ch 1, ch 2) and **unsolved exercises:** no answer is printed, so `marked_answer` and `marked_by` are null.
- **Cases:** `marked_answer` holds the printed solution, with `marked_by: "worked-answer"`.
- **A mark that looks doubtful** (recorded as printed, not changed): ch 8 MCQ 4 highlights «كل ما سبق خاطئ», but option أ is
  «الأرباح المحتجزة». Ch 2 T/F 3 («مصادر التمويل … مدينة بطبيعتها») is ticked صح. Both should be checked in stage 4.

## Cases transcribed
- **Ch 1, p. 35 («للاطلاع والمناقشة»):** a reading text about the FASB and the conceptual framework (pp. 35–37). It asks no question, so it has no item.
- **Ch 2, pp. 79–81:** 1 item (journal).
- **Ch 3, pp. 101–107:** 1 item (ledger, trial balance, income account, balance sheet).
- **Ch 7, pp. 229–237:** 2 items. This one case comes after 7-5-6 and covers the whole chapter, not only 7-5.
- **Ch 8, pp. 272–287:** 4 cases, one item each, all `"theory-only chapter"`:
  - Case 1: direct cash-flow statement.
  - Case 2: indirect cash-flow statement.
  - Case 3: multi-step income statement and EPS.
  - Case 4: statement of financial position.
- **Ch 10, pp. 350–352:** 6 items, one per requirement. Item (d) is the chart, described from the image.

## Pages rendered and read
- **Rendered: 47 pages** at 110 dpi: 38, 39, 80–82, 101, 102, 108, 109, 229–240, 272–288, 322, 323, 350–356.
- **Read visually: 37 pages:** 38, 39, 80, 81, 82, 101, 102, 108, 109, 229, 230, 231, 233, 236, 238, 239, 272, 273, 274, 276, 278,
  279, 280, 281, 282, 284, 285, 287, 288, 322, 323, 350, 351, 352, 353, 354, 355.
- **Rendered but not opened: 232, 234, 235, 237, 240, 275, 277, 283, 286, 356.** On these pages the text layer has either plain,
  unspaced amounts or amounts I confirmed by recomputing the totals.

Every spaced or reversed amount in the items was read from an image. Examples: ch 3 exercise; ch 7 MCQ 4; the ch 7 trial balance;
the ch 8 comparative balance sheets; ch 10 exercises 1–3.

## Unreadable or damaged text
Nothing was unreadable. Obvious extraction damage was fixed and noted in `notes`:
- ch 1 T/F 6: «الأرياح» corrected to «الأرباح».
- Formulas split over two lines were reassembled: ch 7 T/F 5.
- Reversed digit groups were read from the images.

Book typos are kept and flagged, not fixed:
- «حقول الملكية» (ch 2 MCQ 1)
- «أو استثنائية» (ch 8 MCQ 1)
- «انتتاج» (ch 9 MCQ 2)
- «عدد الخزائن» for pumps (ch 10 Ex 1)
- The blank in ch 9 MCQ 5, marked here with «...».
- The stray words «مكتبي/مكتبية» in ch 10 Ex 3 were removed.

## Items whose unit is unclear
- **ch 1 T/F 3:** the stem is about "principles", but its wording is the book's definition of the assumptions → 1-4-1 or 1-4-2.
- **ch 1 essay:** users of accounting information → 1-6-1 and 1-6-2 (set to 1-6-2).
- **ch 9 MCQ 4:** conditions for a cost. The text is in the 9-3 introduction (pp. 298–299), which has no audit unit of its own. It is set to 9-2
  because p. 298 falls in 9-2's page range.
- **ch 3 exercise and ch 10 exercises:** these span several units. The main unit is given, and the others are listed in `notes`.
- **ch 8 T/F 4:** discontinued line vs extraordinary items → 8-2-5-3 (p. 255), or 8-2-4 (p. 248).

## Printed case solutions that look wrong (not fixed)
1. **Ch 3 case, p. 102: bank ledger account.**
   - It omits the 4,000,000 equipment credit and prints «رصيد مدين 7,728,000» with totals of 13,810,000.
   - The listed credits add up to 4,582,000, and 4,582,000 + 7,728,000 = 12,310,000 ≠ 13,810,000.
   - The correct balance is 5,228,000 with the equipment entry (the figure the trial balance uses), or 9,228,000 without it.
2. **Ch 8 Case 2, pp. 278–279: the 2019 assets column does not add up.**
   - 152,000 + 50,000 + 44,000 + 80,000 − 34,000 = 292,000, but the total is printed as 342,000 (the equity-and-liabilities side is 342,000).
   - The solution pays 60,000 for land, which needs land of 100,000 in 2019, not the printed 50,000. With 100,000 the column gives 342,000.
   - The solution header also names the wrong company («الأدهم» instead of «الشهباء»).
3. **Ch 10 case, p. 352: mix break-even value.**
   - It is printed as 120,000, which is the fixed cost. The correct figure is 120,000 ÷ 48.57% = 247,058.82.
   - The lines after it do use 247,058.82: × 57.14% = 141,176.47 and × 42.86% = 105,882.35.
4. **Ch 8 Case 3, pp. 282–284: data and solution disagree.**
   - The data give «مصاريف نقل مبيعات 18,000». The solution uses 7,500 and adds «مصروفات نثرية أخرى 10,500», which is not in the data.
   - Totals are unaffected (1,200,000 operating expenses, net 2,400,000, EPS 300). The selling/administrative split changes: 430,500 / 769,500 with the data vs 420,000 / 780,000 printed.
5. **Ch 7 case, pp. 231–237: two treatments that do not match the data.**
   - The 9,000 cash shortage is charged to the cashier by journal entry, but it is also deducted as a loss in the income statement, and the balance sheet shows no receivable from the cashier.
   - The case says the buildings were let (annual contract received from 1/7). The solution instead treats the debit «ايجار المباني» 70,000 as half prepaid (35,000) and leaves «الايجار الدائن» 180,000 wholly in income.
   - All totals add up: trial balance 4,600,000; net profit 684,400; balance sheet 2,816,400.
6. **Ch 2 case, p. 80 (not arithmetic):** shop equipment (تجهيزات المحل, 2,000,000) is journalised as «من ح/ المشتريات», with the narration «شراء بضاعة بشيك».

Checked and consistent: ch 7 MCQ 1 and MCQ 4 keys, ch 8 Cases 1 and 4, ch 10 case alternative 1, and ch 10 MCQ 1–3 keys.
