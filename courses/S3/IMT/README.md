# IMT — التسويق والتجارة الدولية (International Marketing and Trading)

Source material and generation state for the IMT review. The published page is
`/S3/IMT/index.html` on the site; this folder is what it was built from.

| | |
|---|---|
| Semester | 3 |
| Published review | v1.4 (2026-09-09) — https://azizmarashly.github.io/SVU-MBA-Course-Review/S3/IMT/ |
| Prompt used | bank built with v0.4, page rendered with v0.9; ASK mode, Arabic interface — settings in `PROJECT_SETTINGS.md` |
| Latest prompt in repo | v0.9 — this review is in line with it (source-files appendix, per-question source labels, licence notice, `STATE.md`) |
| Chapters in scope | 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12 (chapter 8 skipped by the owner) |
| Bank | 292 questions: exam 107, textbook 142, other 50, generated 15; 24 low-confidence; 109/109 subsections covered |
| Working directory | `.review_generation_working_directory/` — read its `STATE.md` (where the run stands) and `README.md` (folder map, workflow) |
| Origin of the material | Student-run shared drive "SVU Files" (IMT folder) plus files circulated in the course groups. Unofficial; see `../../DISCLAIMER.md` for copyright and takedown. |

## What is in this folder

| Path | What it is |
|---|---|
| `PROJECT_SETTINGS.md` | The PROJECT SETTINGS table the review was generated with, plus values for settings added in later prompt versions. Paste it into the current prompt to resume. |
| `.review_generation_working_directory/README.md` | Handoff notes: folder map, release workflow, scoring rules, current state, open items. Start here. |
| `.review_generation_working_directory/bank/` | Question data per chapter (`bank_ch01.py` … `bank_ch12.py`, `bank_extra.py`), `build_bank.py`, `render_html.py`, `release.py`, `qa_blocks.py`. |
| `.review_generation_working_directory/bank.json`, `.review_generation_working_directory/out.html` | Build outputs. `out.html` is byte-identical to the published `/S3/IMT/index.html`. |
| `.review_generation_working_directory/notes/ledger.md` | Source ledger: every input, duplicate groups, include/exclude decisions, chapter map. |
| `.review_generation_working_directory/notes/textbook_keys.md` | Book review questions per chapter with answer keys read from the book. |
| `.review_generation_working_directory/notes/f19_transcription.md` | Transcription of the handwritten F19 exam scan. |
| `.review_generation_working_directory/txt/`, `.review_generation_working_directory/ocr/` | Text extraction of every input and full OCR of the textbook (page-separated). |
| `.review_generation_working_directory/source_index.txt` | Maps the short working names (`ex00`, `sum02`, …) to the real file names below. |
| `المنهاج الٱكاديمي/` | The textbook (423 pages), the book-questions PDF, and the 14 slide decks. |
| `اسئلة سابقة/` | Past exams: F17, F19 (scan), S24 and F24 (Telegram export), plus older-curriculum essay files (excluded, see ledger). |
| `ملخصات سابقة/` | Two summaries: one used as an answer-key cross-check, one inspected and excluded (no questions). |
| `ملفات متعلقة بالمادة/` | Related files: a photo of recalled exam topics (used), chapters of an older textbook and two slide decks from another course (excluded). |

Not in the repository: `_old_versions/` (git history has every version) and the two versioned
deliverables at the folder root (`…_v1.4.html`, `…_v1.4_bank.json`), which are identical to
`.review_generation_working_directory/out.html`, `.review_generation_working_directory/bank.json` and the published page. `release.py` recreates them.

## Exam sittings and sources

F17 (27 questions), F19 (30, handwritten), S24 (32), F24 (40); textbook review questions per
chapter; the Emad summary (S18, only items whose concept exists in the current book); the Asem
summary as cross-check. Full detail and the reasons for every exclusion: `.review_generation_working_directory/notes/ledger.md`.

## How to continue

**Fix an answer or add questions**

1. Edit the chapter file in `.review_generation_working_directory/bank/` (`bank_ch05.py` for chapter 5, and so on).
2. Bump `.review_generation_working_directory/VERSION` and add a line at the top of `.review_generation_working_directory/CHANGELOG.md`.
3. Build and check:
   ```
   cd .review_generation_working_directory/bank
   set PYTHONUTF8=1
   python release.py        # must print "uncovered: 0"
   python qa_blocks.py
   ```
4. Publish the page: copy `.review_generation_working_directory/out.html` over `/S3/IMT/index.html` at the repository root.
5. Run `python scripts/build_course_index.py` from the repository root (or let the GitHub Action do it after the push) so the home page shows the new version and counts, then commit.

**Add a new exam sitting or summary**

1. Put the file in the matching subfolder (`اسئلة سابقة/` or `ملخصات سابقة/`).
2. Open this folder in Claude Code, paste the latest prompt with the table from
   `PROJECT_SETTINGS.md` in its settings section. Tell it the file is new; it will extract, deduplicate against the bank,
   verify against the book OCR, rescore, and rebuild.
3. Add the file to `.review_generation_working_directory/source_index.txt` and `.review_generation_working_directory/notes/ledger.md` if the agent did not.
4. Release and publish as above.

**Bring the review up to a newer prompt**

Done for v0.9 in review v1.4 (source-files appendix and per-question source labels, §11d; licence
notice, §19; `STATE.md`, §0d). For a later prompt version, compare its changelog against
`.review_generation_working_directory/STATE.md`, edit `render_html.py`, and release as above; the bank
data normally does not need to change.

## Open items

- F19 Q6, Q7 (Porter, Dunning), F19 Q23, F17 Q3 (turnkey): topic known, question text not
  reconstructed with confidence.
- F17 Q20 is about chapter 8, which is out of scope.
- PDF / DOCX exports were never requested; none exist.

## Not to be used

The owner removed one summary file from the inputs during the first run and asked that it never
be used or referenced. It is not in this folder and nothing in the bank is derived from it. Do
not re-add it.
