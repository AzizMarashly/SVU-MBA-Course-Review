# scripts/pdf_text — Arabic PDF text extraction (prototype, 2026-09-25)

Status: **evaluation done, tool is a working prototype; not yet run on a whole book.** Owner asked
for a wrap-up after ~2 h; what is below is measured, what is listed under "untested" is not.

## What was wrong with the PRM/MIS fix

`extract_book.py` used `re.sub("ا([أإآا])ل", r"ال\1", t)` on the plain `get_text()` output. The real
fault is in the PDFs: the fonts (SimplifiedArabic in ACM, Times New Roman in PRM) map the
**lam-alef ligature glyph to the two code points alef+lam in the wrong order**, so every `لا/لأ/لإ/لآ`
comes out as `ال/أل/إل/آل`. A plain-text regex cannot tell that reversed pair from the genuine
definite article `ال` (`طالب` vs `طلاب` are both words), so the PRM rule only repairs the case
"article + ligature" (`اإلجابات → الإجابات`) and leaves every other occurrence: `مالحظة`
(ملاحظة), `اهتالك` (اهتلاك), `خالل` (خلال), `ثالث` (ثلاث), `عالقة` (علاقة), `البد` (لابد),
`أولن` (ولأن), `االستهالكية` (الاستهلاكية). Measured on the PRM book (p.22 prose): PRM fix
2.0 % CER, geometric method 0.0 %; on ACM p.21: 4.3 % vs 0.3 %. Word recall 73 % → 100 %.
**PRM's `book_fixed.txt` therefore still contains those broken words** (grep `ثالث|خالل|عالقة|البد`
in it); the bank answers were written by helpers reading that text plus page images, so the risk
is in quoted book wording, not in facts. Worth a grep-and-check pass, not a regeneration.

The geometric signature that fixes it: in `page.get_text("rawdict")` the alef of a ligature has a
bbox **nested inside** the following lam's bbox (zero-width box at the glyph's right edge in
SimplifiedArabic; a narrower box with the same right edge in Times). Genuine consecutive glyphs never
nest. `normalize_ar._glyph_groups` rewrites such pairs as `ل`+alef. The same file also fixes:
kashida rendered as a run of 1-pt-wide `ف` glyphs (`حصففففر` → `حصر`), Word's split text runs
(`القرار،ات`, `من ج / هة`) by re-sorting all glyphs of a row by x, mixed-direction lines (English
headings, numbers, option letters `A.`…`E.`) by reversing embedded LTR runs, and table rows (cells
on one line, two spaces between cells).

## Measured accuracy (CER on hand-transcribed passages, 11 pages; lower is better)

| method | ACM p21 prose | p129 journal | p322 T/F table | exam S24 p1 | case p128 | PRM p22 | PRM p2 TOC | scanned print | handwriting | image table (summary p8) |
|---|---|---|---|---|---|---|---|---|---|---|
| PyMuPDF `get_text()` | 6.3 | 11.8 | 6.6 | **65.7** | 5.7 | 5.1 | 6.5 | – | – | – |
| + PRM regex fix | 4.3 | 11.8 | 5.2 | 65.0 | 5.0 | 2.0 | 1.9 | – | – | – |
| `get_text(sort=True)` | 65.9 | 41.7 | 58.7 | 65.8 | 69.4 | 68.4 | 60.0 | – | – | – |
| pdfminer.six / pdfplumber | 76–78 | 58 | 77 | 72 | 77 | 77 | 71–74 | – | – | – |
| **geometric (this tool)** | **0.3** | 6.3* | **2.8** | **1.3** | **1.0** | **0.0** | **0.6** | – | – | – |
| Tesseract 5.4 ara+eng psm3 (300 dpi) | 8.3 | 29.5 | 5.3 | 13.6 | 6.4 | 9.8 | 1.3 | 21.3 (80 % words) | 59 | 41 |
| Windows OCR ar-SA | unusable on watermarked SVU pages (garbage), not scored | | | | | | | | | |
| vision transcription (Claude reading the PNG) | used as the reference; on text pages it agreed with the geometric output to 0–3 % | | | | | | | | 100 % of a handwritten trial balance read correctly | table read fully |

\* p129: the remaining 6 % is the date `١٢/١٠` coming out as `10/12` (a number run reversed) and
Arabic-Indic digits normalised to ASCII; amounts and account names were all correct. Section
numbers typed as separate glyphs (`٥-١` on the page = "1-5" logical) come out in visual order.

The exam PDF (Word export with per-word text runs) is the big win: plain PyMuPDF gives word-reversed
lines (66 % CER), the geometric method 1.3 %.

## Chosen pipeline

1. Text-layer pages: `normalize_ar.mupdf_rtl(page)` → `normalize_ar.clean()` (NFKC, ASCII digits,
   tatweel and bidi marks removed). No OCR.
2. Detector (`extract_pdf.py`): a page with < 80 Arabic letters and at least one image is flagged
   `needs_ocr` / `needs_vision`; a `quality` score also drops with leftover suspect patterns.
3. Flagged pages: a vision helper reads `pNNN.png` (200 dpi). Tesseract is a fallback only for
   clean printed scans (80 % word recall on the CamScanner page, useless on handwriting and on the
   watermarked table page). Windows OCR is not usable on SVU pages.

Command for a new book:

```
set PYTHONUTF8=1
python scripts/pdf_text/extract_pdf.py "courses/S2/ACM/كتاب المحاسبة للمديرين.pdf" courses/S2/ACM/.review_generation_working_directory/extracted/book
```
Outputs `pNNN.txt`, `book.txt` with `=== PAGE n ===` markers (PRM FORMAT.md style), `pages.json`,
and a PNG for every flagged page.

Vision-helper brief for flagged pages: open `pNNN.png`; transcribe every line in reading order,
tables as one row per line with ` | ` between cells, numbers exactly as shown (keep Arabic-Indic
digits), handwriting with `[?]` after any uncertain token; do not translate, do not fix the author's
spelling; write to `pNNN.txt`, add `"method": "vision"` to the page's entry in `pages.json`.

## Dependencies

`pip install pymupdf rapidfuzz` (rapidfuzz only for the evaluation). Tesseract: `winget install
UB-Mannheim.TesseractOCR`, then put `ara.traineddata` from tessdata_best in a folder and pass
`--tessdata-dir` (Program Files is not writable); tested only via the scratch evaluation, not
wired into `extract_pdf.py`. EasyOCR/PaddleOCR were not tried (time).

## Untested / next steps

- Run `extract_pdf.py` on the whole ACM book and the PRM book and diff against `book_fixed.txt`
  (expect the words listed above to change; check nothing else regresses).
- Number runs: decide whether dates/section numbers typed as separate glyphs should stay visual.
- Long-dash TOC leaders join the Latin title and page number into one LTR run (`13-----INTRODUCTION`).
- `normalize_ar.py` is the evaluation module copied as-is (it still contains the pdfminer/Tesseract/
  Windows-OCR helpers used for the comparison); split into a clean module + tests for every pattern
  (`test_normalize_ar.py` covers only the plain-text functions so far).
- Evaluation scripts, renders, ground truth and all method outputs are in the session scratchpad
  `scratchpad/pdf_eval/` (ground_truth.py, eval.py, methods.py, out/scores.json).
