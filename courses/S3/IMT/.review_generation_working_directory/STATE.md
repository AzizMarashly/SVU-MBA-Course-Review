# STATE — IMT review (handoff file, §0d)

Written for the next agent. Folder map, release workflow and scoring rules are in `README.md` in this
directory; this file only says where the run stands.

## 1. Settings in force

- Spec version: **v0.9** for rendering; the bank itself was built and verified under v0.4 (2026-09-09).
- Interaction mode: ASK. Pilot chapter: NONE. Interface / question / explanation language: Arabic.
- Chapters in scope: 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12. Primary reference: `MBA-International Marketing and Trading-The Book.pdf`.
- Deliverable version: **v1.4** (`VERSION`); naming stays `<base>_vX.Y.html` as declared in `../PROJECT_SETTINGS.md`, not the two-digit `_vNN` of §0e.
- PDF / DOCX: ASK AT END — never answered, none produced.
- Last update: 2026-09-09.

## 2. Stage checklist (§1–§15 of the prompt)

| Stage | Status | Produced |
|---|---|---|
| 1 Read reference, verify extraction | done (OCR fallback, §1a) | `ocr/book.txt`, `ocr/ch/` |
| 2 Curriculum check, 2a chapter map | done | `notes/ledger.md`, `bank.json → chapter_map` |
| 3 Extract questions | done (F17, F19, S24, F24, book, Emad) | `txt/`, `notes/f19_transcription.md`, `notes/textbook_keys.md` |
| 4 Source ledger with hashes | done | `notes/ledger.md`, `source_index.txt`, `bank.json → source_ledger` |
| 5 Deduplicate | done — 292 canonical questions | `bank/bank_ch*.py`, `bank/bank_extra.py` |
| 6 Conservative editing | done | — |
| 7 Verify + answer blocks, 7c low confidence (24) | done | bank files |
| 8 Cross-check (Asem: 59/60) | done | methodology section |
| 9 Coverage audit + 15 generated | done — 109/109 | `build_bank.py` output |
| 10 Focus areas + importance | done | `bank.json → focus_table` |
| 11 Document structure, 11a–11d | done — 11d appendix added in v1.4 | `bank/render_html.py` (`FILES`, `SRC_ROW`) |
| 12 Bilingual formatting | done | CSS in `render_html.py` |
| 13 HTML deliverable, 13d bank checkpoint | done — v1.4 | `bank.json`, `out.html` → `/S3/IMT/index.html` |
| 14 Privacy note (+ copyright sentence) | done | how-to and methodology |
| 15 QA | done for v1.4 (see §4 below) | `bank/qa_blocks.py` output |

## 3. Decisions not obvious from the files

- Chapter 8 excluded by the owner. One summary file removed by the owner mid-run and never to be used or named.
- Independent sources = BOOK, F17, F19, S24, F24, EMAD, ASEM (7). `دورات.txt` holds two sittings and counts as two.
- Focus areas: subsections with ≥2 exam sources, else the top-2 with ≥1 (deviation from §10a "top of the ranking", stated in the methodology).
- Source labels on questions use the first file of each source group as the row number (`SRC_ROW`); duplicates and dependent copies have their own rows pointing at it.
- Images inspected = 91 distinct (F19 4, Wael 56, photo 1, F17 PDF embedded 7, book review pages 22, book-questions PDF 1); the ledger's "90+" counted crops and zooms separately.
- The layout of this directory predates §0d (`bank/`, `notes/`, `txt/`, `ocr/`); `CHANGELOG.md` plays the role of `VERSIONS.md`; `release.py` archives old copies to `../_old_versions/` (git-ignored) instead of `archive/`.

## 4. Known problems and open questions

- Unresolved: F19 Q6, Q7 (Porter, Dunning), F19 Q23, F17 Q3 (turnkey); F17 Q20 is chapter 8 (out of scope).
- `qa_blocks.py`: 3 blocks over 80 words without an optional line (Q06-016, Q06-035, Q06-038) and 39 "why repeats answer text" hits — all pre-existing, inspected in v1.0/v1.1 and accepted as false positives or essay answers; not re-edited in v1.4 since the bank was not touched.
- v1.4 browser test (Chrome, served over `http://127.0.0.1`, desktop 1394 px and a 390 px iframe): answers hidden by default, single reveal, mode counts 107/142/50/15, importance ≥5 → 3, ≥2 hides all generated, repetition ≥5 → 1, combined filter count matches a manual count, badge and summary, panel closed by default on phone and open on desktop, panel state / filters / mode / chapter state survive reload, reset, collapse/expand chapters without touching answers, search opens a collapsed chapter, all 524 source links resolve to the 39 rows, reference lists and appendix start collapsed, theme toggle. Not tested: printing, screen readers.
- PDF / DOCX still not requested.

## 5. To continue

Nothing pending. For a fix: edit the chapter file in `bank/`, bump `VERSION`, add a `CHANGELOG.md` line, run
`python build_bank.py && python render_html.py && python qa_blocks.py` (with `PYTHONUTF8=1`) from `bank/`,
copy `out.html` to `/S3/IMT/index.html`, run `python scripts/build_course_index.py` at the repository root (refreshes `courses.json` for the home page), and update this file.
