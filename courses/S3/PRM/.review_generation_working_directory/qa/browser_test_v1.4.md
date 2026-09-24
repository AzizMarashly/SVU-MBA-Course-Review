# Browser test — PRM v1.4 (2026-09-24)

Chrome (Claude in Chrome), `out.html` served from the working directory on a local HTTP server. Desktop window 1280 px wide;
phone width through `qa/phone_test.html` (iframe 390 × 800 px; the window itself could not be resized below ~1390 px).

| Check | Desktop | 390 px | Result |
|---|---|---|---|
| Old id of a merged record opens its kept record (`#Q09-006` → Q08-009, `#Q04-011` → Q07-003 in a folded chapter, `#Q02-021` → Q02-001, `#Q08-044` → Q08-021 after "fold all chapters") | yes | yes | pass — chapter opened, record lands just below the sticky toolbar (first run landed under the toolbar: fixed with one instant scroll offset by the toolbar height) |
| «سُئل أيضاً بصيغة أخرى» block inside the answer (Q02-001: MCQ from EX15 with options and key + short answer from EMAD) | yes | yes | pass — RTL, one card per folded form, key in green, student's text muted; no horizontal scroll (scrollWidth 375 ≤ 390) |
| «يضم أيضاً المعرّف السابق» in the sources line | yes | yes | pass |
| Cross-link Q01-008 → Q01-009 (chip link inside the answer) | yes | — | pass — tap scrolls to Q01-009 below the toolbar |
| Table groups: shared table drawn once, sub-questions under it, per-question «↑ الجدول المشترك» link | yes (tbl-Q08-007) | yes (tbl-Q10-010) | pass — `#tbl-…` hash kept (first run: the filter state overwrote it; fixed); id range wrapped badly on the phone, fixed (two ltr spans) |
| Filters with groups: importance 5+ → 23 records, empty groups hidden, partly-empty groups keep their table; mode «الكتاب» → only tbl-Q10-020 visible (4); reset | yes | — | pass |
| Search finds folded wording (e.g. text only in a folded record) | yes | — | pass |
| Fold all / open all / show all answers (419) / hide answers | — | yes | pass |
| Symbol chip → bottom sheet (CPI on Q10-012 inside a group), nav chips for the question's 7 symbols | — | yes | pass |
| Console errors | none | none | pass |

Not tested: light theme after the change, printing, a real phone, screen readers, iOS Safari.
