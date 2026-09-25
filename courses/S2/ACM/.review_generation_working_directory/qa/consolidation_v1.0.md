# Consolidation pass (§5b) — ACM v1.0, prompt v0.12

Done by the owner-stage agent on 2026-09-25, after all seven chapter files existed (209 records). Inputs: `qa/neighbours_v1.0.txt`
(14 records with cross-chapter neighbours), the whole bank read once end to end (one line per record: id, form, unit, pages, sources,
stem, answer, claim), the chapter reports' cross-chapter notes, and the owner session's candidate list.
Similar-stem threshold of the hard check: **0.6** (tf-idf cosine on the normalised stem; `build_bank.SIM_THRESHOLD`, also in STATE.md).

## Folds (`FOLDS` in build_bank.py — same claim, different form, the dropped record becomes an «also asked as» line)

| dropped | keeper | claim | book page | why this keeper |
|---|---|---|---|---|
| Q02-009 (S24 recall «تعريف أساس الاستحقاق المحاسبي», reconstructed MCQ, unit 2-2-2) | Q08-014 (book T/F 1 of ch 8, unit 8-2-5-1) | revenues and expenses of the period are recognised whatever the date of collection or payment | p. 249 (keeper); the same rule on p. 56 | the book review item is protected (§5a step 2) and always keeps; S24 and the SUM also-line move to Q08-014, which becomes exam + textbook. A cross-chapter fold keeps the keeper's pages (its Ref line names ch 8), so p. 56 is not added. Answers agree (the MCQ key is the T/F statement). |

No `MERGES` (same claim + same form across chapters): none found.

## See-links added (protected pairs, both keep their cards, shared frequency and importance)

| pair | claim | pages | note |
|---|---|---|---|
| Q03-014 (book MCQ 4 of ch 3: «تشتمل الميزانية على حسابات: كل ما سبق») ↔ Q08-009 (F24, original options: «قائمة المركز المالي تحتوي على: موجودات ومطاليب») | the statement of financial position (balance sheet) holds assets against liabilities and equity | 95, 107 / 258 | same claim, different wording, both protected (book review item; exam item with its recalled options). Neither answer contradicts the other: the book's «المطاليب» include equity (p. 49). |
| Q02-005 (S23 with its recalled options: «حساب الصندوق دائماً مدين») ↔ Q03-015 (book MCQ 5 of ch 3: debit-balance accounts are the assets) | asset accounts carry debit balances | 60–61 / 90, 95 | a reverse definition of one claim (§5a); both protected. |

The build's scoring was changed so linked cards share one score in every case: the focus bonus now applies when any card of the claim sits in a
focus unit (`union_units`), as §10b says ("cross-linked cards of one claim share one score"); before, Q03-014 (focus unit 3-5) and Q08-009
(unit 8-3-1) scored differently. qa_blocks recomputes it the same way.

## Records moved or added by owner decisions (not merges)

- exams_a#105 (OLD, «مدخلات النظام المحاسبي») was in ch 2 unused → raw + variant + OLD source on **Q01-008** (unit 1-5, p. 21).
- exams_b#37 (S24, «سعر الوحدة الواحدة ما بيتغير بتغير حجم الانتاج», options متغيرة / ثابتة / تكلفة تاريخية) was unused in ch 9 → new
  reconstructed, low-confidence record **Q10-046** (unit 10-1-2, pp. 329–330, answer: variable — the per-unit variable cost is constant).
  Not merged with Q09-005 (answer «ثابتة») or Q10-017 (answer: the false statement about fixed totals): different claims and answers.
  Its id is numbered after the generated Q10-045 so that no existing id changes.

## Candidates judged and rejected (kept apart)

| pair | reason | pages |
|---|---|---|
| Q09-005 (fixed = does not change with volume, S24) / Q09-006 (variable, OLD F24) vs Q10-017 (F23, «اختر العبارة الخاطئة في علاقة التكلفة بحجم الإنتاج») and Q10-026 (book T/F on cost behaviour) | Q09-005/006 name a term from a definition (classification, 9-3-2); Q10-017 tests the four behaviour statements (totals vs per unit) and its key is a statement, not a term; Q10-026 is the definition of cost behaviour itself. Different claims and different answer texts; a merge would also fail the disagreeing-answers check. | 300 / 329–330 |
| Q03-011 (T/F: revenues and expenses are matched in the statement of financial position → خطأ) vs Q08-013 (T/F: the income statement mainly helps estimate the future financial position → خطأ) | different claims (where revenues/expenses are matched vs what the income statement predicts); the neighbour score came from bold terms only (0.53) | 95 / 246 |
| Q01-016 vs Q08-019 | «المحاسبة عملية تتضمن: كل ما سبق» vs the operating items of the income statement; shared stem shape only | 15 / 251 |
| Q02-003 vs Q08-017 | capital from the extended accounting equation (calculation) vs net assets = assets − liabilities (T/F definition) | 59 / 260 |
| Q02-024 vs Q08-020 | «ليست من القوائم الختامية: ميزان المراجعة» vs «ليست من مبادئ قائمة الدخل: التحصيل النقدي»; same stem pattern, different facts | 47 / 249 |
| Q02-025 vs Q08-007, Q08-020 | bank commissions are an expense vs the sum of non-operating revenues (480000) vs income-statement principles | 69 / 252–255 / 249 |
| Q02-029 vs Q03-010 | steps of the accounting cycle (essay) vs purpose of the trial balance (T/F) | 45–47 / 91 |
| Q02-046 vs Q08-007 | entry for interest added by the bank vs the sum of other revenues | 77 / 252 |
| Q03-014 vs Q08-017 | contents of the balance sheet (linked to Q08-009 instead) vs net assets | 95 / 260 |
| Q02-021 (non-current assets are for use) vs Q08-011 (current assets: within a year or the operating cycle, whichever is longer) | related definitions, different deciding fact | 48 / 261 |
| Q09-004 (capital cost: benefit over more than one period) vs Q07-014 (a capital expenditure: adding an engine) | definition vs classification of an example | 299–300 / 220 |
| Q01-003 (prudence) vs Q07-023 (lower of cost or market) | the rule applies prudence but asks the balance-sheet presentation | 20 / 214–217 |
| Q01-008 (inputs = data) vs Q01-015 (information are outputs, not inputs) | same chapter, two facts (what the inputs are / what the information is); left as the helper built them | 21–22 |

## Hard checks — negative tests (run once each, in memory on a copy of the loaded bank; nothing written)

1. Same option set + similar stem + different key: a clone of Q03-004 with the key flipped → build fails «same options, similar stem (1.00), different answer: Q03-004 / Q03-099».
2. Raw id used by two records: exams_b#23 added to Q01-003 → build fails «raw item exams_b#23 used by ['Q01-002', 'Q01-003']».
3. Merge with disagreeing answers: `MERGES["Q01-011"] = "Q01-012"` (خطأ vs صح) → build fails «('merge with disagreeing answers', 'Q01-011', 'Q01-012', 'خطأ', 'صح')».

After reverting (nothing had been written), `python release.py` builds clean: 209 records, uncovered 0.
