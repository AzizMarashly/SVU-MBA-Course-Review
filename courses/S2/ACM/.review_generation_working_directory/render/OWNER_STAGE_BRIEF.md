# Brief for the owner-stage agent (stages 5b, 10–16) — ACM review v1.0, prompt v0.12

You take over from the session owner after the seven chapter helpers have written `bank_ch01/02/03/07/08/09/10.py`. Work only inside
W = `C:\Users\root\SVU-MBA-Course-Review\courses\S2\ACM\.review_generation_working_directory` and the repository root
R = `C:\Users\root\SVU-MBA-Course-Review`. `set PYTHONUTF8=1` for every python run. Read first: `R\CLAUDE.md`, `W\STATE.md`, `W\render\SOURCES.md`,
`W\render\CHAPTER_HELPER_BRIEF.md`, the seven `W\qa\chNN_report.md`, and the prompt sections §5a–§5c, §9, §10, §15, §16, Appendix A in
`R\prompt\SVU-MBA-Course-Review-Generator.md`. Never modify a source file under `R\courses\S2\ACM\` outside the working directory. Do not commit.

## 1. Consolidation pass (§5b)
1. From `W\render`: `python build_bank.py`. Fix any assertion that a helper left (wrong unit code, missing symbol → add it to `meta_acm.SYMBOLS`
   with ar/en/f/note/ex, a `see` link that is not symmetric, a `calc.method` not in the chapter's METHODS). Never change an answer or a page to
   make a check pass — report it instead.
2. Read `W\qa\neighbours_v1.0.txt` and the whole bank once end to end (`python -c` printing one line per record: id, qtype, sub, pages, sources,
   stem[:80], answer[:40]). Apply §5a: same claim + same form across chapters → `MERGES[drop] = keep` in `build_bank.py`; same claim, different
   form → `FOLDS`; a book review item and a verbatim exam item with original options keep both cards and get `see` links in the chapter files
   (edit both records). Keeper: the exam item in the chapter that owns the deciding page. Never merge records whose answers differ; if the book
   settles it, fix the wrong one with the page and put the other reading on `other_source`, else keep both with `low_conf`.
3. Write `W\qa\consolidation_v1.0.md`: every merge, fold, see-link and rejected candidate with the claim and the book page; the threshold used (0.6).
4. Negative-test the three hard checks once each (temporarily introduce a same-options-different-answer pair, a raw id used twice, a merge with
   disagreeing answers; confirm the build fails; revert) and note it in the log.

## 2. qa/summary.json
Fill `W\qa\summary.json`: `images` = total pages/images read visually across all reports (book, others, exams A/B, chapters); `asem` = the §8 sentence
in Arabic («طابق مفتاح ملخص عاصم لأسئلة صح/خطأ إجابات الكتاب في N من M بنداً؛ الاختلافات: …» — compute it from `extracted/questions/summary.json`
marked answers vs the bank's answers of the same book items, by claim); `scope_counts` = one Arabic sentence with the number of exam raw items
outside the F25 scope per chapter (from the exams reports and chapter reports); `out_of_scope` = Arabic lines, one per excluded chapter/topic with
the count of exam items («الفصل 5: 17 سؤالاً عن المشتريات والحسم المكتسب — محذوف في F25»); `unresolved` = Arabic lines for items that could not be
placed or verified (from the chapter reports).

## 3. Release
`python release.py` (must print `uncovered: 0`; if a unit is uncovered, ask the responsible chapter file for one generated question from the
unit's own pages — you may write it yourself from `extracted/book/pNNN.txt`, following the brief), then `python qa_blocks.py`; every list should
be empty or justified; fix what is mechanical (bold in stems, missing claim, ordering), report the rest. Update `FILES_SUMMARY.images` in
`meta_acm.py` to match `qa/summary.json`.

## 4. Browser test (A.7) — desktop and 390 px
Serve `W\out.html` over `python -m http.server 8765` from a copy in your scratchpad (file:// URLs are blocked) and use the Chrome tools
(load them with one ToolSearch: tabs_context_mcp, navigate, computer, javascript_tool, resize_window, find, tabs_close_mcp). Set
`document.documentElement.style.scrollBehavior='auto'` before screenshots. Check: answers hidden by default, one click reveals one; each reading
mode count; importance slider 5 and repetition slider max match the bank (count with JS); panel closed at 390 px and open on desktop; badge and
summary when closed with a filter; Essentials shows exactly importance ≥ 3 and folds the more-blocks; chapters/sections/page blocks fold
independently; search hit inside a collapsed chapter opens it; state survives reload; Reset; a symbol chip opens the sheet; a figure fits
390 px; step reveal and Show-all; reference lists collapsed; both themes; version in title/cover/metadata. Write `W\qa\browser_test_v1.0.md`
with what you tested and what you saw. Close your tab at the end.

## 5. Publish and docs
From R: `python scripts/publish_page.py S2/ACM` then `python scripts/build_course_index.py` (exit 1 = changed, normal). Update the static
fallback course cards in `R\index.html` only if the file has hand-typed values for other courses that show a pattern to follow (read it first;
add an ACM card in the same style if the no-JS fallback lists courses). Update `W\STATE.md` (every stage done, decisions, known problems, "To
continue"), `W\VERSIONS.md`, `R\courses\S2\ACM\README.md` (bank counts, sources, version line), and append a short ACM section to `R\HANDOFF.md`
(what was released, what is open). Do not delete HANDOFF entries of other courses.

## 6. Completion summary (your final message, English, compact)
Per §16 of the prompt: working directory and stage resumed from; deliverable version; chapter map; files / duplicates / independent sources /
images; raw occurrences, unique questions, merges and folds with answer conflicts; reconstructed, out-of-scope, unresolved counts; per-chapter
and per-section counts; procedural chapters with their types, solved exercises, figures, fast routes; coverage N of N and generated count;
focus areas; low-confidence ids; cross-check agreement rate; every count of §15, the average block length; anything you could not test.
