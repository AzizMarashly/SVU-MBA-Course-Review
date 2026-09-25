# HANDOFF — open work as of 2026-09-25

Written for the next agent. Read `CLAUDE.md` first, then this file. Delete this file when the list is empty.

Current state: IMT v1.6, PRM v1.4, MIS v1.0, prompt v0.12 (history in git and in each course's `VERSIONS.md` /
`STATE.md`). Prompt v0.12 is the first version with §5a–§5c (duplicate test, consolidation pass, frequency), §7e
(practical chapters) and Appendix A (HTML contract); no course has been rendered under it yet.

## Next course releases (first runs under v0.12)

1. **PRM v1.5** — under §5a step 2, book review items and verbatim exam items keep their own card: undo those of the
   25 folds made in v1.4 (e.g. Q05-017 → Q05-013, Q09-012 → Q09-002) and cross-link them instead (shared frequency
   and importance, own section). Log in `qa/consolidation_v1.5.md`. ~80–120k tokens.
2. **MIS v1.1** — apply `courses/S3/MIS/.review_generation_working_directory/qa/review_v0.2_vs_v1.0.md` (top 5 fixes
   with ids; MIS `STATE.md` §5 step 4), including undoing the merges Q01-013←Q09-011 and Q01-009←Q03-020 and the
   own-content coverage test of §9. ~200–300k tokens.
3. The renderer features v0.12 asks for (§7e Methods block, figures from data, step reveal, Essentials view, full
   model answer for essays — Appendix A) exist in no course yet; adopt them piecemeal, MIS v1.1 / PRM v1.5 first.

## Small

- PRM: F24 item P1 (FF + lead) is its own low-confidence record Q07-013 built on an illustrative example; under §5c it
  could become a credit on Q07-001 instead (owner's call).
- MIS: page shows spec v0.11 (tooling) although the run was planned under v0.10.
- IMT: `release.py` does not validate the VERSION format and archives to `../_old_versions/`; no duplicate build
  checks or consolidation pass yet (PRM/MIS have them) — port with the next IMT release.
- `courses/S2/ACM/` (untracked): course material for a new semester-2 course, added outside these sessions; the
  owner decides whether it belongs in the repository.
- Not tested anywhere: real phone, print, Safari/Firefox, screen readers.

## D. ACM (S2) — new course, started 2026-09-24/25, nothing committed

Sources in `courses/S2/ACM/` (cleaned by the owner's decision: big scanned `ACM تفريغ.pdf` deleted by the owner; exact
duplicate of the book-questions PDF and the re-saved summary export deleted; three files renamed to remove hidden
Unicode marks). Remaining: the book (447 p), `ACM Exam S24.pdf`, two question sets, the summary (p.8 is an image),
`حل مسائل غير محلولة الفصول 3 4 5 ACM.pdf` (7 scanned pages: OCR during transcription, owner's decision), and
`المطلوب بدوره F25 بالامتحان.txt` (F25 scope: ch 1, 2, 3, 10 in full; ch 7 depreciation only, no journal entries;
ch 8, 9 theory only; ch 4, 5, 6 out).

All text PDFs have a text layer with the lam-alef problem (`اإلجابات`, `االت`, `اهتالك`). The owner says PRM's fix
was not accurate.

In flight when this was written (check results before continuing):
- Telegram collection from groups `MBAF22_SEM3` and a second group (link pasted mangled, probably invite
  `+ABg1ed_nMvdkODBk`) into `courses/S2/ACM/telegram/` (one `<SESSION>.txt` per exam sitting, `other.txt`, `files/`,
  `INDEX.md`), read-only via `~/my-os` (`./mos run messaging tg …`) in WSL. Raw, not yet selected or cleaned.
- Arabic PDF extraction evaluation: tool plus README in `scripts/pdf_text/` (methods compared against the pages
  read by eye; the pipeline to use for ACM and later courses). Read its README before extracting the ACM book.

Next: review both outputs; set up `courses/S2/ACM/` the PRM way (README, PROJECT_SETTINGS, working directory with
STATE.md, PRM `render/` tooling).

Telegram result (2026-09-25): both groups read in full (the second link is the real public username
`httpABg1ed_nMvdkODBk`, the MBA general group). The text is done: S23, F23, S24, F24, S25, F25, unknown_session,
other. Only 2 of 88 media files are copied so far. Remaining steps are in `courses/S2/ACM/telegram/INDEX.md`:
copy from the my-os archive once `export-media` finishes, check about 75 photos for names, and fetch the 23.5 MB
lecture transcription, which was over the size cap.

PDF text result (2026-09-25): `scripts/pdf_text/` is the extraction tool from now on. It uses a geometric lam-alef
fix from `rawdict` glyph boxes; measured error was 0–1.3 % on prose and exam pages, against 2–5 % for PRM's regex
fix and 66 % for plain get_text on the S24 exam PDF. Scanned pages: Tesseract works as a draft for printed pages;
handwriting needs vision. Open items are in its README: full-book run and diff; direction of dates and section
numbers; tests for the geometric patterns. PRM's `book_fixed.txt` still has errors (ثالث, خالل, عالقة, مالحظة,
اهتالك …), so grep the PRM bank for quoted book wording with these forms and check it (no need to regenerate).
The evaluation's ground truth is only in this session's scratchpad (`pdf_eval/`) and may be lost.

### ACM v1.0 released (2026-09-25, owner stage) — not committed yet
Released: `/S2/ACM/index.html` (v1.0, prompt v0.12, F25 scope), `courses.json` rebuilt, a semester-2 fallback card in `index.html`.
Bank: 209 questions (exam 97, textbook 119, other 1, generated 20), 81 units covered, 16 low-confidence; consolidation log
`courses/S2/ACM/.review_generation_working_directory/qa/consolidation_v1.0.md`, browser test `qa/browser_test_v1.0.md`. Renderer:
`fig hide_labels` for exam charts (numbered lines, key in the answer), solution figures moved into the answer block.
To commit (one focused commit): `S2/ACM/`, `courses/S2/`, `courses.json`, `index.html`, this file; `scripts/pdf_text/` and the
`.gitignore` / `CLAUDE.md` changes belong to their own commits.
Open for ACM v1.1: fold in the F25 recalls after the sitting (2026-09-26) as source `F25`; move «نص الطالب الأصلي» into the answer block
for every reconstructed record (it can show the recalled answer); test on a real phone; the unresolved items listed on the page
(methodology) and in STATE.md §4. The Telegram / PDF-text notes above are finished for ACM (telegram/ folded and deleted, the book
extracted with `scripts/pdf_text`).
