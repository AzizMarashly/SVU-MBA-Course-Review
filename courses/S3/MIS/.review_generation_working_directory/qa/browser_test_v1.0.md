# Browser test — MIS v1.0 (§15), 2026-09-24

Page: `out.html` (identical to `../مراجعه كامله لماده ال MIS_v1.0.html`), served from the working directory with
`python -m http.server` and opened in Chrome (Claude in Chrome extension). Checks run with DOM scripts plus screenshots.

## Desktop (window 1366 × 900, viewport 1394 px)

| Check | Result |
|---|---|
| Title / cover | «مراجعه كامله لماده ال MIS — v1.0»; cover line shows v1.0, chapters 1, 2, 3, 5, 7, 8, 9, 10, 255 questions, exam 86 / book 131 / other 43 / generated 22 |
| Question cards | 255 rendered, ids Q01-001 … Q10-033 |
| Mode buttons | الكل 255 · الامتحانات 86 · الكتاب 131 · مولَّدة 22 · back to الكل 255 (match `bank.json` type counts) |
| Importance slider | ≥ 4 → 20 cards (18 × 4 + 2 × 5), back to 1 → 255 |
| Show answer | Q01-002 (merged record): answer, why, remember, distractors, reference «الفصل 1 · ص 20، 278», sources R44 + BOOK + ASM, folded «صيغ أخرى في المصادر» with the Q07-013 wording |
| Horizontal overflow | none |
| Metadata footer | «v1.0 · المواصفة v0.11 · CC BY-NC-SA 4.0», date 2026-09-24 |
| §7d symbol sheet | absent (no glossary: `SYMBOLS = {}`, no record has a table or calculation); 0 symbol chip rows |
| Console | no errors or warnings on load |

## Phone width (390 × 844, page loaded in a 390-px iframe because the desktop window could not be narrowed)

| Check | Result |
|---|---|
| Horizontal overflow | none (document scroll width 375 = 390 minus the scrollbar; 0 elements past the right edge) |
| Toolbar | sticky; with «⚙ الفلاتر» open it fills most of the screen, closed it is one line plus the search box (state remembered in `mis_filters_open`) |
| Answer block | Q05-024 (merged): verdict, why, remember, reference «ص 206–207», four sources, variants folded; text wraps, no clipping |
| Fold all / open all | «طيّ الكل» closes chapters, sections and prose blocks (1 `details` left open of 379); «فتح الكل» opens them |
| Search | «Hadoop» → Q05-010, Q10-005, Q10-008, Q10-017, Q10-023 |

## Fixed during the test

- The reference line printed «PDF first–last» for any multi-page record (e.g. «PDF 102–29» for pages 102 and 29, «PDF
  20–278» for the merged Q01-002). `render_html.py` now prints consecutive runs in record order, the same for the book
  and the PDF (printed page = PDF page): «ص 23–27، 30–31، 41 (PDF 23–27، 30–31، 41)».

## Read by eye (20 random answer blocks from `qa_blocks.py`)

Q02-048, Q10-021, Q02-004, Q03-019, Q07-019, Q01-013, Q01-019, Q09-016, Q05-023, Q01-025, Q03-011, Q07-001, Q01-015,
Q10-010, Q05-015, Q02-020, Q01-010, Q01-023, Q03-030, Q03-026: answer consistent with why, remember has the bold key
fact, distractor lines name the concept each wrong option belongs to, low-confidence records (Q03-019, Q05-023) carry
their reason. No problem found.

## Not tested

- A real phone or touch input (only a 390-px iframe in desktop Chrome), print layout, Safari/Firefox, light theme
  toggle beyond load, the frequency slider beyond load.
