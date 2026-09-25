# PROJECT SETTINGS — ACM review (v1.0 run, 2026-09-25)

This is the PROJECT SETTINGS table filled in at the top of the generator prompt
(`prompt/SVU-MBA-Course-Review-Generator.md`, v0.12) when this review was produced. To resume or extend the run,
paste this table over the PROJECT SETTINGS section of the current prompt and open this folder in Claude Code;
§0d of the prompt makes the agent resume from `.review_generation_working_directory/STATE.md`.

| Setting | Value |
|---|---|
| Review title | `مراجعه كامله لماده ال ACM` |
| Course / subject | `المحاسبة للمديرين — Accounting for Managers (ACM)`, semester 2 |
| Chapters in scope | **The F25 exam scope only** (owner decision 2026-09-25): chapters `1, 2, 3, 10` in full; chapter `7` in full **except everything that is a journal entry** (concepts and calculations of adjustments, doubtful debts, cash and bank reconciliation, inventory count and pricing, depreciation are in; the entry units 7-4-3 and 7-5-6 and the entries inside the other units are out); chapters `8, 9` theory only (9 up to mid page 14 of the chapter = book p. 302, before «مقومات نظام محاسبة التكاليف»). Chapters 4, 5, 6 (and 11, 12) are out. Exam questions about the excluded parts are counted in the methodology and not included. Governing text: the group message quoted below; the paraphrase in `Exams/المطلوب بدوره F25 بالامتحان.txt` (chapter 7 "depreciation only") is superseded by the owner's instruction of 2026-09-25. |
| Primary reference | `Course/كتاب المحاسبة للمديرين.pdf` (447 pages, د. باسل أسعد, Damascus 2021; printed page = PDF page, verified on every page; the review answers are marked on the pages — tick in the صح/خطأ column, green highlight on the MCQ option — and verified against the text) |
| Expected exam format | `MULTIPLE CHOICE` only (students report 30–35 questions, almost every item with a «كل ما سبق صحيح / خاطئ» option; no true/false in recent sittings; about half practical: entries, depreciation, break-even, charts) |
| Question language | `ARABIC` |
| Explanation language | `ARABIC` |
| Interface language | `ARABIC` |
| Interaction mode | `DECIDE` — the owner asked for an unattended run; every default applied is listed in `STATE.md` §3 |
| Pilot chapter | `NONE` |
| Output base name | `مراجعه كامله لماده ال ACM` — files are named `<base>_vMAJOR.MINOR.html` (`VERSIONING.md` at the repository root) |
| Working directory | `.review_generation_working_directory` (inside this folder, §0d layout) |
| PDF / DOCX | `NEVER` (HTML only) |
| Units per chapter | the finest TOC level inside the F25 scope: 81 units (12 / 6 / 5 / 22 / 17 / 8 / 11 for chapters 1 / 2 / 3 / 7 / 8 / 9 / 10) |
| Similar-stem threshold | tf-idf cosine ≥ 0.6 (default) |
| Spec version | `v0.12` |

## The scope message (group2 #51026, 2026-09-21, a student's report of the instructor's statement; pasted by the owner 2026-09-25)

```
الفصول 1 - 2 - 3 - 10 مطلوبين بالكامل
الفصول 4 - 5 - 6 محذوفين بالكامل
الفصل السابع مطلوب كلو ماعدا كلشي قيود
الفصل الثامن مطلوب فقط النظري
الفصل التاسع مطلوب فقط النظري ومو كلو .. مطلوب من بداية الفصل التاسع لعند نص الصفحة 14 .. يعني كلشي من عند مقومات نظام محاسبة التكاليف لآخر هالفصل محذوف
```

## Owner instructions that are not in the prompt

- Use the F25 scope (the message above) as the only scope of this run and state that clearly on the page (cover banner, scope section, chapter openers of partial chapters). Chapter 7: the owner confirmed on 2026-09-25 "align with the message", i.e. the whole chapter without journal entries, not depreciation only.
- The Telegram export in `telegram/` (raw messages of the two course groups) was used only to understand the students' context; every exam recall, answer discussion, scope statement and reported book error it held that was missing from the resources was folded into `Exams/*- تلغرام.txt` files (verbatim, anonymised), then the folder was gitignored and deleted (2026-09-25).
- Run as fast as possible with parallel helpers, without trading accuracy: three transcription helpers (book, others, exams ×2), then one helper per chapter, one owner session for ledger, consolidation, scoring, render and QA.

## Files reorganised before the run (2026-09-25)

The course folder had files at its root and in `Course/`, `Exams/`, `telegram/`. Moved: the two book-question PDFs and the scanned
solutions into `Course/`, the summary into `Summaries/`, `ACM Exam S24.pdf` and the F25 scope file into `Exams/`. Before that the owner
had already removed a 23.5 MB lecture transcription, an exact duplicate of the book-questions PDF and a re-saved summary export, and
renamed three files to strip hidden Unicode marks (see `HANDOFF.md` history in git).
