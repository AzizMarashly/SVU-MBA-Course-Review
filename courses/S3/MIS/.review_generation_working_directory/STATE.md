# STATE — MIS review (handoff file, §0d)

Written on 2026-09-13 when the run was imported into the repository. The run itself happened on
2026-09-06 in a Claude Code session opened on the course folder, before the versioned prompt
existed; this working directory was reconstructed from that session's scratchpad. Folder map and
release workflow: `../README.md`.

## 1. Settings in force

- No spec version (ad hoc brief, restated in `../PROJECT_SETTINGS.md`). Interaction mode ASK.
  Interface, questions and explanations in Arabic; chapters 1, 2, 3, 5, 7, 8, 9, 10.
- Primary reference: `Dr Iyad Zoukar - MBA - MIS - The Book.pdf`, 507 pages, printed page = PDF page.
- Deliverable version: **v0.2** (`VERSION`), naming `<base>_vX.Y.html`. The v0.1 originals
  (HTML, DOCX, interactive PDF, plain PDF) were named `<base>-v0.1.*` and stay outside the repository.

## 2. Stage checklist (mapped onto the prompt's stages after the fact)

| Stage | Status | Produced |
|---|---|---|
| 1 Read reference | done — PyMuPDF text, reflowed per page | `txt/book_pages.txt`, `txt/book_questions.txt` |
| 2 Curriculum check | done — two curricula found; older-course sources excluded or used for in-book concepts only | methodology text in `bank/build_docx.py` / `build_html.py` |
| 3 Extract questions | done — 12 text sources + 3 scanned PDFs and 7 photos read visually | `src/S01..S12*.txt` (see §3 below for the mapping) |
| 4 Source ledger | done informally — hashes checked, 8 duplicates found (2 removed by the run's own count of 6 + 2 the import found again); ledger written as `LEDGER` in `bank/build_bank.py` | `bank.json → source_ledger` |
| 5 Deduplicate | done — 269 canonical | `bank/bank_a..e.py` |
| 6 Conservative editing | done | — |
| 7 Verify + answer blocks | done — answer + explanation + page; book answers kept visible when corrected (`book_answer`) | bank files |
| 7c Low confidence | **not in this schema** | — |
| 8 Cross-check | done — Asem summary added late as `ASM` (raised book-question frequencies) | `bank_d.register_assem_summary()` |
| 9 Coverage audit + generated | done — 101/101 subsections; 33 generated | `bank/coverage.py`, `bank_e.py` |
| 10 Importance / focus areas | **not done** (pre-v0.3 run) | — |
| 11 Structure | done — 4 sections per chapter (exam, book, other, generated); most-repeated list; methodology; metadata | `bank/build_html.py` |
| 11d Source-files appendix | done in v0.2 | `bank/meta_mis.py` |
| 12 Bilingual formatting | done | CSS in `build_html.py` |
| 13 HTML deliverable | done — v0.2 | `out.html` → `/S3/MIS/index.html` |
| 13d Bank checkpoint | done at import — exported from the Python records | `bank.json` (via `build_bank.py`) |
| 14 Privacy note | done | intro + footer |
| 15 QA | v0.1: `bank/qa.py` (DOCX/PDF checks), visual checks; v0.2: v0.1 reproduced byte for byte before the additions, then diffed | — |
| 19 Licence notice | done in v0.2 | intro pledge + footer notice |

## 3. Decisions not obvious from the files

- Source codes (`SRC_AR` in `build_docx.py`): BKQ = book end-of-chapter questions; S25, HD
  («حل دورات»), R44 (44-question sitting) and F24 (60 questions) are the four blocks of
  `دورات/دورات.txt`; ASM = Asem summary; OQ1–OQ5 = older-curriculum collections used for
  in-book concepts only; GEN = generated (freq 0). Row numbers for the appendix: `meta_mis.py`.
- `src/` mapping: S01 أسئلة الكتاب (mojibake, book text used instead) · S02 اسئلة_دورات_مجمعة (OQ1) ·
  S03 أسئلة_من_مقرر (OQ2) · S04 تجميعة اسئلة دورات_2 (dependent copy of S02) · S05 حل دورتين
  (dependent copy of the HD block) · S06 MIS Q (OQ3) · S07 محدد عليه (older-course book, excluded) ·
  S08 تعريفات (definitions, unused) · S09 ملاحظات (OQ5) · S10 ملخص عاصم (ASM) · S11 امتحان 2019 (OQ5) ·
  S12 حل أسئلة docx (OQ2). Scans read visually: دورات.pdf + MISS photos (OQ4), حل دورة 38-60
  (answers 38–60 of F24), MIS_F19_Anan (handwritten summary, unused).
- Frequency = number of independent sources; a block repeated inside `دورات.txt` counts once.
- Types are Arabic in the records (`دورة`, `كتاب`, `أخرى`, `مولّد`); `build_bank.py` maps them to
  the repository vocabulary (exam, textbook, other, generated).
- The page says "10 independent sources" (written before ASM was added); the bank ledger has 11.
  Left as is in v0.2 because v0.2 changes no content; fix the text in the next content release.
- Chapter 7 needed no generated question.

## 4. Known problems

- No low-confidence flag, importance score or focus areas (pre-v0.3 schema).
- The "10 sources" wording above.
- DOCX / PDF pipeline (`pipeline.py`, `build_pdf.py`) needs Microsoft Word via COM and was not
  re-run at import; `tags.json`, `caps.json`, `geo.json` are its v0.1 intermediates.
- `build_html.py` imports `build_docx.py` for the shared constants, so `python-docx` must be
  installed even for the HTML build.

## 5. To continue

Nothing pending. For a fix: edit `bank/bank_*.py`, bump `VERSION`, add a `CHANGELOG.md` line,
run from `bank/`: `set PYTHONUTF8=1 && python release.py`, then at the repository root
`python scripts/publish_page.py S3/MIS` and `python scripts/build_course_index.py`, update this file.
For a full upgrade to prompt v0.9, regenerate with the current prompt (PRM tooling as template);
the bank records here are the verified input.
