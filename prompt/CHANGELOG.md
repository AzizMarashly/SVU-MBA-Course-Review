# Changelog — SVU MBA Course Review Generator prompt

Each version is a git tag on this repository. Diff any two versions with a compare link such as
https://github.com/AzizMarashly/SVU-MBA-Course-Review/compare/v0.5...v0.6

## v0.12 — 2026-09-24
Applies the backlog `prompt/IDEAS.md` (I-1 … I-12) and the causes found in the MIS v0.2 → v1.0
review (`courses/S3/MIS/.review_generation_working_directory/qa/review_v0.2_vs_v1.0.md`). No
section renumbered; new material sits in new sub-sections (§5a–§5c, §7e) or inside the section
it belongs to. Length 9,967 → 11,771 words, of which the main body is 10,484 and the new
Appendix A (HTML contract) 1,287.

- **Structure — Appendix A (owner decision, 2026-09-25):** the renderer contract of §13a (shared
  control rules, toolbar, filters, Essentials view, collapsing, figures and step reveal) and the
  browser checklist of §15 moved verbatim to "Appendix A — HTML contract" after §19, numbered
  A.1–A.7, so the main text leads with correctness, coverage and exam focus. §13a keeps the base
  requirements plus a summary of what the student sees with pointers to A.1–A.6; §15 keeps a
  one-paragraph HTML check pointing to A.7. No section renumbered; cross-references updated
  (header, §0b, §7e, §11). Course docs cite §13a only historically (IMT `VERSIONS.md`), unchanged.
- **Overridable defaults (owner decision):** the similar-stem threshold (§5b, tf-idf cosine
  ≥ 0.6) and the unit level (§9, roughly 5–15 units per chapter) stay as defaults; two optional
  PROJECT SETTINGS rows override them; the value used is recorded in `STATE.md` (§0d item 1) and,
  for the threshold, in the consolidation log.

- **Priorities (§0a):** explicit order — correctness > faithfulness to source wording > coverage
  > exam focus > brevity > style, plus a short list of the run's non-negotiables. Coverage and
  exam focus were missing, so brevity silently won (thinner essays, lost topics). §0c DECIDE
  default for generated questions now targets the "mentioned but never asked" units (the old
  "uncovered focus areas" set was empty by construction).
- **Duplicates and consolidation (§5, §5a, §5b — I-11 with its lessons and exception):** a defined
  test (same claim of the book = the fact that decides the answer, so a statement and its
  negation carry the same claim): same wording → merge; different wording → a book review item
  or an exam item recorded with its original wording and options is always the card that keeps
  (cross-linked cards share one frequency and one score from the union of ledger source ids,
  but keep their own section, type tags and raw ids), everything else folds as a variant (same
  form) or an "also asked as" line (other form); what is not a duplicate; kept-record fallback
  order; never merge differing answers. Every record carries raw source-item ids and a one-line
  claim. §3b: when the book's review set has the same claim, reconstruct in the book's form. One whole-bank consolidation pass
  after the chapter helpers and before scoring, with a neighbour report as an aid only and a log
  in `qa/`. Three hard build checks (same options + similar stem + different key; raw id used
  twice; disagreeing merge). Helpers get a written brief and never merge across chapters.
- **Frequency (§5c — I-10, I-12):** a problem recalled without its data credits the existing
  records of the same §7e problem type and format, for every sitting (§3 says such a recall is
  not "topic only"); a student summary of the book's review set counts as a source.
- **Coverage (§9):** a unit counts as covered only by a question whose expected answer is the
  unit's own content *and* whose Ref page lies in the unit's page range (the MIS audit counted
  loosely related questions); units are the TOC level giving roughly 5–15 per chapter; a
  previous version's generated question is dropped only when a real question now passes that
  test. **Regeneration change report (§0e):** kept / reworded / merged / split / dropped /
  shortened per record, plus a list of concepts no longer asked that must be empty or
  justified; the previous bank is an input to each chapter helper, which returns a disposition
  per old record. The helper brief (intro) now lists everything a helper must receive.
- **Reconstructed questions (§3b):** minimum quality — four options, one right, distractors from
  the same or a neighbouring unit, no synonym pairs; a recall with fewer or ambiguous options
  gets clean options and keeps the recall in `original`.
- **Essays (§7b):** key points on the answer line plus a collapsed "Full model answer" (about
  100–200 words, pages per point), outside the word target. True/false items need no
  distractors line.
- **Low confidence (§7c):** when *not* to flag (chapter placement, an absent distractor, a
  verbatim or book-marked answer, a source key the book settles); a flag is removed only with
  the settling page.
- **Procedural chapters (§7e — I-1, I-3, I-5, I-6):** defined (two or more records share a
  solving method); a "Methods" block after the opener, closed by default with the type names in
  its summary, one entry per problem type (recognition, ordered steps with outputs, page; the
  course's order); every worked answer follows and names the steps, each Step label linking to
  its entry; a numeric example before the symbol (also per glossary entry, §7d); a "Fast route"
  line for rule-based deductions where the exam is multiple choice, page-cited and labelled
  derived when needed; the book's unsolved exercises solved as textbook records (frequency 1,
  score by §10b) labelled "solution generated". §7d: `Step` column and `Fast route` line added,
  course-specific examples generalised.
- **HTML (§13a — I-2, I-4, I-7):** figures generated from the record's data (inline SVG, phone
  width, highlight, text alternative, about twelve nodes as guidance and horizontal scroll
  beyond, build recomputes and fails on mismatch); step-by-step reveal that keeps the Answer
  line, Fast route, given values and step 1 visible and collapses steps 2..n (Why / Remember /
  Distractors / Ref stay visible), with "Show all steps"; an "Essentials" toggle in the bar
  (importance ≥ 3 only, secondary lines folded, step details closed). §13a rewritten around one
  shared list of control behaviours (persistence, AND, counts, no-script fallback,
  accessibility) instead of repeating them per control — same requirements, shorter.
- **Working directory and versions (§0d, §0e — I-8, I-9):** source files are immutable once
  added; deliverable versions are `vMAJOR.MINOR` (MAJOR = bank generation, MINOR = every other
  published release) per `VERSIONING.md`; `VERSIONS.md` rows record the spec version.
- **§1:** note whether the book prints its own review answers (tick / highlight) — the mark is
  the book's answer, verified against the text. **§3:** raw item ids; "topic only" recalls make no
  record. **§7:** cite the page that states the fact, not a review or reference page, the
  verbatim page first. **§7c:** a flag is also removed by showing its reason is an excluded one.
  **§10a:** cross-linked cards count once.
- **§15 / §16:** checks and summary lines for all of the above (duplicate checks negative-tested,
  coverage sample re-read, figure recomputation, methods cited by steps, Essentials and step
  reveal in the browser test, source hashes unchanged).
- **Room made:** the per-version "Changes in v0.x" history in the header replaced by one v0.12
  paragraph and a link to this file (~400 words); §0c defaults, §0d `STATE.md` contents, §11
  "how to use", §13b/§13c viewer prose, §16 summary list (now refers to the §15 counts) and §17
  tightened without dropping a rule; §13a consolidated as above; the §9/§10 openers shortened.
  Settings row "Spec version" corrected (it still said v0.10). Revised once after an independent
  review (2026-09-25) before tagging.

## v0.11 — 2026-09-14
- §7d (new): questions with tabular data show it as a real table under the stem; numeric answers
  open with the full working table (when there is one) and a "Calculation" block — given values
  with their origin, then one row per step: formula → substitution → result — and the "Why" line
  names the rule only; an always-visible chip row under the table names every symbol the question uses; tapping a
  chip or an underlined symbol opens a bottom sheet (touch-first) with the symbol's name, English
  name, formula and note from a structured course glossary; pointer devices also get a hover card. §15: mechanical checks for flattened stems, numeric answers without a
  calculation block, and arithmetic left in "Why". Tooling: `T()` / `C()` / `S()` in `common.py`,
  `table` / `ans_table` / `calc` record fields, `SYMBOLS` (four fields per symbol) in the course meta file, renderer, and
  `qa_blocks.py` checks including glossary coverage (PRM and MIS render folders).

## v0.10 — 2026-09-13
- §13a: every prose block of the HTML (how to use, scope, methodology, source files, reference
  lists, contents, file metadata) is collapsible like a chapter, intro blocks open and end blocks
  closed by default, state remembered; "Collapse all" / "Expand all" fold chapters, sections and
  blocks together. The metadata summary line keeps version, spec and licence visible when folded.
  §11: the "how to use" text names the new buttons. No content rule changed.

## v0.9 — 2026-09-09
- §19 / `LICENSE.md`: the generated review files are released under the same CC BY-NC-SA 4.0
  licence as the prompt. "Share freely, never sell" becomes a licence condition of every review
  file instead of a community pledge; the notice and the "how to use" text updated. Quoted
  textbook and exam content remains outside the licence.

## v0.8 — 2026-09-09
- §11d: every review file carries a "Source files" appendix listing every supplied file (kind,
  role, source group, pages or items, exclusion reason), and each question's source labels are
  numbers linking to that table. QA checks the appendix against the folder listing.

## v0.7 — 2026-09-09
- Canonical source moved from a GitHub gist to this repository; links and the attribution
  notice updated. No other changes.

## v0.6 — 2026-09-09
- Licence: CC BY-NC-SA 4.0 with a community pledge (`LICENSE.md`).
- §19: every generated file carries an attribution and licence notice; "how to use" carries
  the pledge.

## v0.5 — 2026-09-09
- §0d: working directory with a `STATE.md` handoff so a later agent resumes instead of restarting.
- §0e: version number in every deliverable filename; only the latest stays in the course folder.
- §13a: collapsible chapters and sections; importance and repetition sliders; filter toolbar
  collapses into a one-line bar on phones.

## v0.4 — 2026-09-09
- §0a rule priority, §0b pilot chapter, §0c ASK / DECIDE interaction mode.
- §2a chapter map between source labels and book chapters.
- §10b fixed base for the importance score.
- Interface language setting; spec version in output metadata; UTF-8 without BOM for the bank;
  "how to use" explains the three markers.

## v0.3 — 2026-09-09
- §3b: multiple choice as a direction for exam questions only; book and other sources keep
  their format.
- §10: importance score and focus areas; §7c low-confidence flag.
- §11c reference lists at the end, collapsed. HTML the only mandatory deliverable; PDF / DOCX on
  request. §13d bank checkpoint before rendering. Ask before generating too many gap questions.

## v0.2 — 2026-09-09
- Multiple-choice focus; fixed non-repetitive answer template with bold keywords; two-line
  chapter opener; single-select reading-mode filter in the HTML.

## v0.1 — 2026-09-09
- Initial specification.
