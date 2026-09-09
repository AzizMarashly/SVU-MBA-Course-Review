# .review_generation_working_directory — handover notes for the IMT review generator

> This directory was created under the name `.imt_work` by a prompt v0.4 run and renamed to the
> standard name from prompt v0.5+. Its layout is the one described below, not the §0d layout of the
> current prompt. `STATE.md` next to this file is the §0d handoff (stage checklist, decisions, open
> items); this README is the folder map and workflow. The settings used are in `../PROJECT_SETTINGS.md`.
> Since v1.4 the page is rendered under prompt v0.9 (source-files appendix, source labels, licence notice).

Working files behind the two deliverables in the parent folder:

- `../مراجعه كامله لماده ال IMT_vX.Y.html` — the single-file RTL review (spec v0.4, ASK mode, Arabic UI)
- `../مراجعه كامله لماده ال IMT_vX.Y_bank.json` — the question bank the HTML is rendered from

`X.Y` is the number in `VERSION` (currently 1.4). The project folder holds exactly one version; older
copies are in `../_old_versions/`. History is in `CHANGELOG.md`. Everything here is reproducible:
`bank.json` and `out.html` in this folder are byte-identical to the published files.

## 1. Release a new version (the normal workflow)

1. Edit the data or the renderer.
2. Bump `VERSION` (e.g. `1.3`) and add an entry at the top of `CHANGELOG.md`.
3. Run:

```
cd .review_generation_working_directory/bank
python release.py
```

`release.py` runs `build_bank.py` (asserts, scoring, coverage; must print `uncovered: 0`) and
`render_html.py`, then copies the outputs to the project folder as `…_v1.4.html` / `…_v1.4_bank.json`
and moves the previous version into `../_old_versions/`. Run `python qa_blocks.py` for the mechanical QA
report. Only the standard library is needed. If you run the scripts by hand, set `PYTHONUTF8=1` first.

## 2. Folder map

| Path | What it is |
|---|---|
| `bank/common.py` | `Q(...)` record constructor with field asserts. Data model documented in the docstring. |
| `bank/bank_ch01.py` … `bank_ch07.py` | Per-chapter question data. Plain dict lists (`SUBS`, `QS`), already in final form. |
| `bank/bank_ch09.py` … `bank_ch12.py` | Same, written with `Q(...)` calls. |
| `bank/bank_extra.py` | Late exam items for early chapters + gap-fillers added after the coverage audit. |
| `bank/build_bank.py` | Loads all modules, validates, computes focus areas / importance / freq, writes `bank.json`. |
| `bank/render_html.py` | CSS, JS and HTML generator. All UI strings live here. |
| `bank/qa_blocks.py` | Mechanical checks on the finished bank. |
| `bank/release.py` | Build + publish the versioned files to the project folder, archive older ones. |
| `VERSION`, `CHANGELOG.md` | Current version number and history. |
| `bank.json`, `out.html` | Build outputs (identical to deliverables). |
| `notes/ledger.md` | Source ledger: every input file, MD5 duplicate groups, include/exclude decision, chapter map. |
| `notes/textbook_keys.md` | Book review questions per chapter with answer keys read visually from the book pages. |
| `notes/f19_transcription.md` | Transcription of the handwritten F19 exam scan. |
| `source_index.txt` | Mapping from the ASCII working names (ex00, sum02, slide05 …) to the real input file paths. |
| `txt/*.txt` | Text extractions of every input, named per `source_index.txt`. |
| `ocr/book.txt` | Full OCR of the textbook (423 pages, `=== PAGE n ===` separators). PDF page = printed page. |
| `ocr/book_raw.txt` | Same before Arabic word-order fix. |
| `ocr/ch/chNN.txt` | Book OCR split per chapter. |
| `ocr/bq_raw.txt` | OCR of the "أسئلة الكتاب" PDF. |
| `tools/ocr.ps1` | Windows WinRT OCR (Arabic) for a folder of PNG pages. |
| `tools/bookpages.py` | `python tools/bookpages.py 44 45` prints OCR text of a page range (run from `.review_generation_working_directory`). |
| `tools/grepbook.py` | `python tools/grepbook.py "عبارة"` finds which book pages contain a phrase. |

Not kept (large, regenerable): rendered page PNGs of the book (~640 MB) and exam images (~200 MB),
and the ASCII-named copies of the inputs (the originals are in the parent folder; see `source_index.txt`).

## 3. How the book was read (why OCR)

The book PDF's body font has a broken ToUnicode map, so PyMuPDF text extraction returns garbage.
Pages were rendered to PNG (PyMuPDF, ~150 dpi) and OCR'd with the Windows built-in Arabic OCR
(`tools/ocr.ps1`). WinRT returns Arabic words in reversed order per line; `book.txt` has that fixed.
OCR is good enough for phrase search and page lookup, not for verbatim quoting. Verified anchors:
chapter start pages 1→10, 2→49, 3→90, 4→130, 5→169, 6→198, 7→235, 8→265, 9→297, 10→325, 11→358, 12→391;
review pages ch1 44-45, ch2 85-86, ch3 124-125, ch4 165-166, ch5 191-192, ch6 223-224, ch7 260-261,
ch9 319-320, ch10 352-353, ch11 385-386, ch12 419-420.

## 4. Sources and codes

| Code | Source | Role |
|---|---|---|
| BOOK | المنهاج الأكاديمي / the textbook | textbook questions (review sections) and page evidence for everything |
| F17 | دورة f17 (docx/pdf, identical) | exam sitting, 27 questions |
| F19 | دورات F19 (handwritten scan) | exam sitting, 30 items, see `notes/f19_transcription.md` |
| S24, F24 | دورات.txt (Telegram export) | exam sittings, 32 + 40 items |
| EMAD | ملخص عماد جبور (S18) | "other" source, only items whose concept exists in the current book |
| ASEM | ملخص عاصم | cross-check of textbook answer keys (59/60 T/F agree; disagreement ch5 TF5) |
| GEN | — | generated questions for subsections no source covers |

Excluded (details in `notes/ledger.md`): the old-curriculum essay files group, the four old-textbook
chapter PDFs, the two .ppt from another course, the Wael handwritten summary (no questions),
the photo (topic evidence only), slides (reference only). The user also removed one summary file from
the inputs mid-run and asked that it never be used or mentioned; the bank contains nothing derived from it.

## 5. Scoring rules implemented in `build_bank.py`

- `freq` = number of independent sources of the question (0 for generated).
- `importance` base by exam-source count: 0→1, 1→2, 2→3, 3+→4; +1 if also a book question; +1 if in a
  focus area; capped at 5; generated questions are fixed at 1.
- Focus areas per chapter: subsections with ≥2 exam sources, else the top-2 subsections with ≥1.
- Scope: book chapters 1,2,3,4,5,6,7,9,10,11,12 (chapter 8 skipped by the user).

## 6. Current state of the bank

| Metric | Value |
|---|---|
| Questions | 292 (exam 107, textbook 142, other 50, generated 15; a question may have several types) |
| Reconstructed exam items | 13 |
| Low-confidence items | 24 (flagged in the HTML) |
| Subsection coverage | 109 / 109 |
| Unresolved | F19 Q6/Q7 (Porter, Dunning: topic only), F19 Q23, F17 Q3 (turnkey), F17 Q20 (chapter 8, out of scope) |

## 7. HTML features (all in `render_html.py`)

Native `<details>` answers (work without JS). Toolbar: type chips (all/exam/textbook/other/generated),
importance slider 1–5 and repetition slider 0–5 (minimum thresholds), chapter select, search with
Arabic normalisation, show/hide all answers, fold/unfold all chapters, fold/unfold all type sections,
theme toggle. Every chapter heading and type heading is itself a fold toggle. State is stored in
localStorage (`imt_review_state`) and in the URL hash (`mode=…&imp=…&freq=…&ch=…`). Printing opens all
folds and answers and ignores filters. Each question is rendered once, under the first of its types,
with `data-section` listing all of them.

## 8. Testing notes

Chrome blocks `file://` in the automation tools, so the HTML was tested through
`python -m http.server <port>` from this folder (port 8765 is taken by another app on this machine,
8799 worked). Tested: default hidden answers, mode counts (107/142/50/15), slider counts
(importance ≥4 → 34, ≥5 → 3; repetition ≥2 → 172, ≥3 → 61), fold/unfold (11 chapters, 39 sections),
search, reload persistence, both themes.

## 9. Open item

The spec's last step asks whether the user wants PDF and/or DOCX exports. Not answered yet; nothing produced.
