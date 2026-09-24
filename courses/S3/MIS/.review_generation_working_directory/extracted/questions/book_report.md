# book.json — the textbook's own end-of-chapter questions (code BOOK, src BOOK)

Source: «Dr Iyad Zoukar - MBA - MIS - The Book.pdf», review section («مراجعة») of each in-scope chapter.
Pages: ch1 39–41, ch2 84–86, ch3 123–125, ch5 214–216, ch7 287–289, ch8 326–328, ch9 367–369, ch10 416–418
(verified against `book/ch_fixed/chNN.txt` page markers and visually).

## Counts — 137 items

| ch | tf | mcq | essay | total |
|---|---|---|---|---|
| 1 | 9 | 6 | 3 | 18 |
| 2 | 9 | 6 | 3 | 18 |
| 3 | 8 | 6 | 3 | 17 |
| 5 | 8 | 6 | 3 | 17 |
| 7 | 8 | 6 | 3 | 17 |
| 8 | 7 | 6 | 3 | 16 |
| 9 | 8 | 6 | 3 | 17 |
| 10 | 8 | 6 | 3 | 17 |
| **all** | **65** | **48** | **24** | **137** |

No `short` items: every set has exactly three blocks — «أسئلة صح / خطأ», «أسئلة خيارات متعددة», «أسئلة \ قضايا للمناقشة» (the last transcribed as `essay`). MCQs always have 4 options (أ ب ت ث).

## Does the book print answers? YES — inline, not as a key after the set
- T/F: the table has صح / خطأ columns and a tick (✓) is printed in one of them for every item. Recorded as
  `marked_answer` = "صح"/"خطأ", `marked_by` = "key".
- MCQ: the correct option is highlighted in yellow in every item. Recorded as `marked_answer` = 0-based index,
  `marked_by` = "highlight" (the letter is repeated in `notes`).
- Essay: no answer; the book prints «مدة الإجابة 15 دقيقة. الدرجات من 100: 15. توجيه للإجابة: الفقرة N-M» — the
  section pointer is kept in `notes` and used for `sub_guess`.
- The page after each set is the chapter's case study («حالة عملية»), no answer key there; grep for
  مفتاح/الإجابات/الأجوبة over `book_fixed.txt` found no separate key anywhere in the book.

## Pages read visually
All 24 review pages were rendered (PyMuPDF, dpi 100) to `pages_png/book_p039..418.png` and read, because the
ticks and highlights exist only visually. The text layer was used for the stems; it is reliable for the words
but scrambles RTL order in mixed lines (e.g. ch2 Q7 option ب is printed «ES – SCM – CRM – KMS», the text layer
gives it reversed) — the visual reading was taken as authoritative in such cases.

## Notes / oddities
- ch2 MCQs are numbered **7–12** as printed (not 1–6); `item` keeps the printed number.
- ch7 p287: the layout is normal (T/F table then MCQ 1) although the text layer interleaves them.
- ch5 T/F 4 («تكمن قوة النموذج العلائقي … حقل مفتاح مشترك») is ticked **خطأ** by the book although it reads like
  the book's own definition — transcribed as printed, flagged here only.
- ch10 T/F 2 («غالباً ما يتخذ المديرون قرارات سيئة») ticked صح — as printed.
- ch7 T/F 3, 4, 5 are about intranets/extranets, treated in the book under 2-6 (ch2), not under any ch7 unit:
  `ch_guess` = 7 (as printed), `sub_guess` = null with a note.
- `sub_guess` for essays follows the printed «توجيه للإجابة» pointer, refined to the third-level unit; ch5 essay 3
  (data hierarchy) is pointed to الفقرة 5-2 by the book but the topic sits in 5-1-1 — set to 5-1-1.
- `in_book` = true for all (they are the book's own items). Discriminator counts are not meaningful for the book
  itself (it is the reference).
