# Stage-3 brief — transcribe every question from one source group (MIS review v1.0, prompt v0.10)

Course: «نظم المعلومات الإدارية — MIS», textbook «Dr Iyad Zoukar - MBA - MIS - The Book.pdf» (507 pages,
printed page = PDF page). Chapters in scope: 1, 2, 3, 5, 7, 8, 9, 10 (4, 6, 11, 12 are NOT in scope, but
transcribe their items too and set `ch_guess` accordingly — the owner decides what to drop).
Work only inside W = `C:\Users\root\SVU-MBA-Course-Review\courses\S3\MIS\.review_generation_working_directory`.
Set `PYTHONUTF8=1` for every python run. Never modify a source file. No personal data (student names that
appear inside source content are fine to skip; never copy a name into the JSON).

## Output
One JSON file `W\extracted\questions\<group>.json` (UTF-8, no BOM) holding a list of items in the format of
`W\extracted\FORMAT.md`, plus `W\extracted\questions\<group>_report.md` (short). Fields recap:
`src` (source id "srcNN" from `W\extracted\index.json`), `loc`, `item`, `qtype` (mcq | tf | short | essay |
topic), `stem`, `options` ([] if none), `marked_answer` (what the source says, or null), `marked_by`
("key" | "highlight" | "student-recall" | "worked-answer" | null), `ch_guess` (1–12 or null), `sub_guess`
(a unit code from `W\extracted\book\subsections.json` → "units", e.g. "5-1-2", or null), `dup_of`,
`book_dup`, `notes`. Add `code` = the independent-source code given below for your group.
Transcribe faithfully: fix only obvious OCR/spacing damage, never invent options or answers; if the
source gives a definition as the "question" (e.g. «تعريف قاموس البيانات»), use `qtype: "short"` with the
stem as written and put the source's text of the definition (if any) in `marked_answer`.

## The book as the map
`W\extracted\book\subsections.json` lists the 105 audit units with their page numbers; `W\extracted\book\ch_fixed\chNN.txt`
holds the text of each in-scope chapter (page markers `=== PAGE n ===`; lines are broken oddly by the PDF
font; «لا» ligatures were fixed). Use them only to guess chapter/unit. You are NOT verifying answers at this
stage — record what the source says and where.

## Two curricula (§2)
Many files belong to an OLDER MIS course (Dr Suleiman Awad's: Excel Solver, pivot tables, Hong's framework,
"نظم دعم القرار الموجهة بالنماذج", history dates of computers, OLAP dimensions, "النظم المفتوحة/المغلقة",
"معايير التصفية المتقدمة"). Those concepts are not in the current book. Still transcribe every item, but set
`in_book` = true / false / "maybe" for each: true only when the concept is treated in the current book's TOC
units (check the unit list); false when it is a Solver / Excel / history / systems-theory item. Give a keyword
discriminator count for your files in the report (4–6 keywords unique to the current book, 4–6 unique to the
older course, how many hits of each per file).

## Images and scans
Scanned PDFs and photos have no text layer. Render pages with PyMuPDF and read them with the Read tool:
`import pymupdf; d = pymupdf.open(PATH); d[i].get_pixmap(dpi=90).save(OUT)` with OUT under
`W\extracted\pages_png\<srcNN>_pNNN.png` (this folder is gitignored). Count how many pages/images you actually
looked at and say so in the report. If a page is unreadable, say so — never guess its content.

## Report (`<group>_report.md`)
Items transcribed per file; how many with options / free-form / topic-only; images or pages read visually;
dependent-copy findings (is file X the same list as file Y? give item-level evidence); the discriminator
counts; anything unreadable; items you could not place in a chapter.
