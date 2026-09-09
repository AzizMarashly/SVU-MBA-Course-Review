# Raw question transcription format (stage 3 helpers)

Each helper writes ONE JSON file `extracted/questions/<group>.json` (UTF-8, no BOM) holding a list of
items, plus a short markdown report `extracted/questions/<group>_report.md`. Transcribe faithfully:
fix only obvious OCR/spacing damage, never invent options or answers. If an option is missing, say so
in `notes`.

Item fields:
- `src`: source id from extracted/index.json (e.g. "src05"); for the book use "BOOK".
- `loc`: where in the source (page number, image name, or paragraph/item number).
- `item`: the item number inside the source as written (string), or null.
- `qtype`: "mcq" | "tf" | "short" | "essay" | "calc" | "topic" (topic = only the topic was recalled, no question).
- `stem`: question text exactly as in the source (Arabic kept as is; English terms kept).
- `options`: list of option strings in source order, or [] if none.
- `marked_answer`: what the SOURCE says/marks as the answer (letter index 0-based, text, "صح"/"خطأ"), or null if the
  source marks nothing. `marked_by`: "key" | "highlight" | "student-recall" | null. Do NOT verify here.
- `ch_guess`: book chapter 1-14 the item most likely belongs to, using extracted/book/toc_raw.txt
  (subsection titles) — or null if unsure. `sub_guess`: subsection code like "8-4-1" or null.
- `dup_of`: if the item is visibly the same question as an item already in your own file, give that item's
  index in your list; also flag `book_dup: true` when the wording matches a book end-of-chapter question.
- `notes`: anything else (data table values, diagram description, "answer highlighted in red", ambiguity).

For calculation items (networks, EVA tables) put ALL the numbers in `notes` or `stem` (e.g. the activity
table as "A:1 | B:3(after A) | ...") so the question can be solved later without the image.
