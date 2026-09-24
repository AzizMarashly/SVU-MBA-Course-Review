# STATE — IMT review (handoff file, §0d)

Written for the next agent. Folder map, release workflow and scoring rules are in `README.md` in this
directory; this file only says where the run stands.

## 1. Settings in force

- Spec version: **v0.11** for rendering (§7d tables + symbol legend since v1.6); the bank was built and verified under v0.4 (2026-09-09) and extended with F25 in v1.6 under the same verification rules.
- Interaction mode: ASK. Pilot chapter: NONE. Interface / question / explanation language: Arabic.
- Chapters in scope: 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12. Primary reference: `MBA-International Marketing and Trading-The Book.pdf`.
- Deliverable version: **v1.6** (`VERSION`); naming `<base>_vX.Y.html`, the repository-wide scheme in `VERSIONING.md` (prompt §0e since v0.12; it overrode the two-digit `_vNN` of §0e up to v0.11).
- PDF / DOCX: ASK AT END — never answered, none produced.
- Last update: 2026-09-24 (v1.6: F25 added, §7d ported).

## 2. Stage checklist (§1–§15 of the prompt)

| Stage | Status | Produced |
|---|---|---|
| 1 Read reference, verify extraction | done (OCR fallback, §1a) | `ocr/book.txt`, `ocr/ch/` |
| 2 Curriculum check, 2a chapter map | done | `notes/ledger.md`, `bank.json → chapter_map` |
| 3 Extract questions | done (F17, F19, S24, F24, F25, book, Emad) | `txt/`, `notes/f19_transcription.md`, `notes/textbook_keys.md` |
| 4 Source ledger with hashes | done | `notes/ledger.md`, `source_index.txt`, `bank.json → source_ledger` |
| 5 Deduplicate | done — 304 canonical questions (F25: 8 merged, 12 new) | `bank/bank_ch*.py`, `bank/bank_extra.py` |
| 6 Conservative editing | done | — |
| 7 Verify + answer blocks, 7c low confidence (27), 7d tables (3 answer tables, no calculations) | done | bank files |
| 8 Cross-check (Asem: 59/60) | done | methodology section |
| 9 Coverage audit + 15 generated | done — 109/109 | `build_bank.py` output |
| 10 Focus areas + importance | done | `bank.json → focus_table` |
| 11 Document structure, 11a–11d | done — 11d appendix added in v1.4 | `bank/render_html.py` (`FILES`, `SRC_ROW`) |
| 12 Bilingual formatting | done | CSS in `render_html.py` |
| 13 HTML deliverable, 13d bank checkpoint | done — v1.6 | `bank.json`, `out.html` → `/S3/IMT/index.html` |
| 14 Privacy note (+ copyright sentence) | done | how-to and methodology |
| 15 QA | done for v1.6 (see §4 below) | `bank/qa_blocks.py` output |

## 3. Decisions not obvious from the files

- Chapter 8 excluded by the owner. One summary file removed by the owner mid-run and never to be used or named.
- Independent sources = BOOK, F17, F19, S24, F24, F25, EMAD, ASEM (8). F25 (v1.6) has no answer key: every F25 answer is from the book page. An F25 item that asks the same idea as an existing record was merged into it (source + frequency, F25 wording and its answer as a variant) even when the option set differs (Q01-001, Q04-007, Q05-019, Q10-003); a new record was made only for a new idea. Where the recalled options make two choices correct (Q10-028, Q11-023) the book's «most important» one is the answer, with a low-confidence line. `دورات.txt` holds two sittings and counts as two.
- Focus areas: subsections with ≥2 exam sources, else the top-2 with ≥1 (deviation from §10a "top of the ranking", stated in the methodology).
- Source labels on questions use the first file of each source group as the row number (`SRC_ROW`); duplicates and dependent copies have their own rows pointing at it.
- Images inspected = 91 distinct (F19 4, Wael 56, photo 1, F17 PDF embedded 7, book review pages 22, book-questions PDF 1); the ledger's "90+" counted crops and zooms separately.
- The layout of this directory predates §0d (`bank/`, `notes/`, `txt/`, `ocr/`); the version history is `VERSIONS.md` (named `CHANGELOG.md` until 2026-09-24); `release.py` archives old copies to `../_old_versions/` (git-ignored) instead of `archive/`.

## 4. Known problems and open questions

- Unresolved: F19 Q6, Q7 (Porter, Dunning), F19 Q23, F17 Q3 (turnkey); F17 Q20 is chapter 8 (out of scope).
- §7d (v1.6): `SYMBOLS` (GDP, GNI) lives in `render_html.py` (IMT keeps course tables there); answer tables on Q01-023 and Q04-018/Q04-029 (`INCOME_T` in `bank_ch04.py`); `build_bank.py` refuses `|` or newlines in stems. Table 1-1 needs horizontal scroll inside its wrapper at 390 px (page itself does not overflow).
- `qa_blocks.py`: 3 blocks over 80 words without an optional line (Q06-016, Q06-035, Q06-038) and 39 "why repeats answer text" hits — all pre-existing, inspected in v1.0/v1.1 and accepted as false positives or essay answers; not re-edited; unchanged in v1.6 (the new F25 records add none). The new §7d line «numeric why without a calc block» lists Q03-009, Q10-009, Q10-020: definitional «=» signs, not arithmetic — accepted.
- v1.4 browser test (Chrome, served over `http://127.0.0.1`, desktop 1394 px and a 390 px iframe): answers hidden by default, single reveal, mode counts 107/142/50/15, importance ≥5 → 3, ≥2 hides all generated, repetition ≥5 → 1, combined filter count matches a manual count, badge and summary, panel closed by default on phone and open on desktop, panel state / filters / mode / chapter state survive reload, reset, collapse/expand chapters without touching answers, search opens a collapsed chapter, all 524 source links resolve to the 39 rows, reference lists and appendix start collapsed, theme toggle. Not tested: printing, screen readers.
- v1.6 browser check (Chrome over `http://127.0.0.1`, 1394 px and a 390 px iframe): 304 questions, 3 answer tables, 20 source links to row #40, 0 broken source links; GNI chip opens the bottom sheet and ✕ closes it; GDP header is an underlined `abbr`; income tables fit at 390 px, table 1-1 (367 px) scrolls inside its wrapper, page width 371 px (no page overflow). Filters/fold/theme not re-tested (unchanged code).
- PDF / DOCX still not requested.

## 4b. F25 (processed in v1.6, 2026-09-24)

`../اسئلة سابقة/دورة F25.txt` → source code F25, appendix row #40, ledger entry with MD5. Merged: Q01-001, Q03-012, Q04-007, Q05-001, Q05-019, Q07-005, Q10-003, Q11-001. New: Q04-029, Q05-031, Q05-032, Q07-031, Q07-032, Q07-033, Q09-020, Q09-021, Q10-028, Q11-023, Q11-024, Q12-018. Details in `VERSIONS.md` and `notes/ledger.md`.

## 5. To continue

Nothing pending. For a fix: edit the chapter file in `bank/`, bump `VERSION` (`MAJOR.MINOR` per `VERSIONING.md`), add a `VERSIONS.md` entry, run
`python release.py` (must print `uncovered: 0`) and `python qa_blocks.py` (with `PYTHONUTF8=1`) from `bank/`,
then `python scripts/publish_page.py S3/IMT` at the repository root, run `python scripts/build_course_index.py` at the repository root (refreshes `courses.json` for the home page), and update this file.
