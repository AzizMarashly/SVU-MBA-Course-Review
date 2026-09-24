# Brief: tables and calculation blocks (§7d) — MIS copy of the PRM brief (write new records in this form; the conversion notes apply to legacy records)

Scope: records whose stem carries tabular data or whose answer is a numeric calculation. You **convert the
presentation** of existing, verified records; you do **not** re-verify against sources, change answers, pages,
sources, `low_conf`, `variants` or `notes`. If a recomputation disagrees with the recorded answer, leave the
record as it is and put the discrepancy in your report (with the numbers); the owner decides.

Work only inside W = `C:\Users\root\SVU-MBA-Course-Review\courses\S3\MIS\.review_generation_working_directory\render`.
Set `PYTHONUTF8=1` for every python run. Edit only the chapter file(s) you were assigned.

## Data model (`common.py`)

```python
from common import Q, T, C, S
table=T(head, rows, caption=None, ltr=True)    # data table shown after the stem
ans_table=T(...)                                # table shown at the top of the answer block (full working: ES/EF/LS/LF, SV/CV per activity …)
calc=C(given=[...], steps=[S(what, eq, sub, res, note=None), ...], note=None)
```

- `T`: `head` = column titles (Arabic or symbols), `rows` = equal-length lists. Cells are numbers or short codes;
  `ltr=True` (default) renders cells left-to-right (activity codes, amounts). Use `ltr=False` only for tables whose
  cells are Arabic phrases. No bold inside tables.
- `C.given`: strings `"symbol = value (origin)"` — where every number comes from: «معطيات السؤال», «من الجدول»,
  «من الخطوة 2», «أكبر EF في الجدول» … Arabic allowed, bold allowed for the key value.
- `S`: one step in solving order.
  - `what` (Arabic + symbol): the quantity found, e.g. `"مؤشر الأداء الزمني SPI"`, `"LS(X7)"`.
  - `eq`: the formula in **symbols only** — Latin letters, digits, operators `+ − × ÷ = ≈ min max ( )`. **No Arabic**:
    the cell is rendered left-to-right in monospace. e.g. `"SPI = BCWP ÷ BCWS"`, `"LS = LF − D"`.
  - `sub` (التعويض): the same formula with the numbers put in, symbols only: `"12 ÷ 10"`, `"(60 + 4×25 + 20) ÷ 6 = 180 ÷ 6"`.
  - `res` (الناتج): the result with its unit; Arabic allowed: `"30 يوماً"`, `"11 = الجواب"` on the final step.
  - `note`: optional, Arabic, where a number came from when not obvious: `note="LF(X7) = مدة المشروع = 20"`.
- `C.note`: one optional closing clause (Arabic), e.g. which activity satisfies the condition.

Rendered order in the answer block: ✔ answer → `ans_table` → الحساب (given list, then the step table
المطلوب | المعادلة | التعويض | الناتج) → why → remember → distractors → ref.

## Conversion rules

1. **Stem**: keep only the question sentence(s) plus a short lead-in («بحسب جدول أنشطة المشروع التالي (المدد بالأيام)، …»,
   «الجدول التالي يعطي قيم المتحولات لخمسة أنشطة. …»). All rows/values move into `table=T(...)`. No `|`, no newline,
   no «X1: —، 4، 3؛ …» chains in the stem. The build refuses stems containing `|`.
2. **Shared data**: sibling questions on the same data set share ONE module-level table constant (`NET3_T`, `TBL_A_T` …)
   and ONE shared `ans_table` constant with the full working (e.g. ES/EF/LS/LF/float for every activity; SV/CV/SPI/CPI
   for every activity). Each sibling then needs only the 1–4 steps that answer its own question.
3. **Every numeric question gets a `calc`** — even a one-step one (three-point estimate, payback comparison, TAC ÷ SPI).
   Steps show: the formula, the substitution, the result. Where a number is not in the question or table, say where it
   came from (`given` or `note`).
4. **`why` becomes concept-only**: ≤ 2 sentences naming the deciding rule (e.g. «LF لأي نشاط = أصغر LS بين لواحقه»);
   no arithmetic chains (QA flags a `why` with 2+ «=» signs when a calc exists). `remember` keeps its bold keywords;
   drop numbers from it only if they now merely repeat the calc. `distractors` may keep the short «ج — 40 هو المتوسط
   البسيط…» explanations.
5. **Essay/short answers** (draw the network / Gantt, level the resources): `ans` stays a short prose answer (levels,
   critical path, project duration, conclusion). Path sums go into `calc` steps (one step per path:
   `eq="A-B-E-H-J-K-L"`, `sub="8+2+60+20+10+12+3"`, `res="115 يوماً = المسار الحرج"`). Per-activity times go into
   `ans_table`. For resource levelling, add a resource-per-day table when the answer depends on it
   (`T(["اليوم", 1, 2, …], [["قبل التسوية", 5, 5, 9, …], ["بعد التسوية", …]])`, with day columns).
6. **Recompute every number** (python is fine) before writing it. Book conventions apply (ES of the first activity = 0,
   EF = ES + D, float = LS − ES; three-point = (O + 4M + P) ÷ 6; SV = BCWP − BCWS, CV = BCWP − ACWP,
   SPI = BCWP ÷ BCWS, CPI = BCWP ÷ ACWP). If your recomputation contradicts the recorded `ans`, do not change the
   record — report it.
7. Bold (`**`) only in `given`, `what`, `note`, `why`, `remember`, `distractors` — never in `eq`, `sub`, `res`, tables,
   stem, options.
8. Everything Arabic except symbols; keep the existing tone (see the finished models: `Q08-007`, `Q08-015` in
   `bank_ch08.py`; `Q10-005`, `Q10-022` in `bank_ch10.py`).

## Symbols glossary (`meta_mis.py` → `SYMBOLS`)

Every symbol you use in a table header, a `given` line, a `what` cell or an `eq` cell must exist in `SYMBOLS`
(`qa_blocks.py` lists the ones that do not). Add a missing one with four fields:
`"XYZ": dict(ar="الاسم العربي", en="English name", f="XYZ = A ÷ B", note="…")` — `f` in symbols only (or `""` for a
given value), `note` in Arabic naming every other acronym in words with the acronym in brackets («الكلفة الفعلية
(ACWP)»). Never mix Arabic and English inside one field. Do not use single capital letters as symbols (activity
names A, B, D, E would collide); write the duration as `D` only inside formulas.

## Checks before you report

```
set PYTHONUTF8=1
python -c "import bank_chNN"                                   # Q() asserts (T/C/S shapes) pass
set PRM_LENIENT=1 && python build_bank.py | findstr WARNING     # no WARNING line for YOUR chapter
python qa_blocks.py                                             # read the §7d lines: your ids must not appear in
                                                                #   "stems that still look tabular" / "numeric why without a calc block"
                                                                #   / "calc blocks whose why still carries the arithmetic"
```
Do not run `release.py`, do not edit `VERSION`, `VERSIONS.md`, `STATE.md` or other chapters.

## Report (in your final message, short)

- ids converted, with `table` / `ans_table` / `calc` flags per id
- shared constants you introduced
- any arithmetic discrepancy with the recorded answer (numbers, and the recorded page)
- any record you left unconverted and why
