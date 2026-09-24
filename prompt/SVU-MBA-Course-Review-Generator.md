# PROMPT — Complete Course Review Generator (v0.12)

> Reusable spec for building a consolidated, verified, interactive review file from a folder
> of course material. Fill in **PROJECT SETTINGS**, then paste the whole document as your prompt.
> Everything below the settings block is generic and works for any course.
>
> **Version control:** this prompt lives in the GitHub repository
> https://github.com/AzizMarashly/SVU-MBA-Course-Review — every version is a tagged release.
> Latest: https://github.com/AzizMarashly/SVU-MBA-Course-Review/blob/main/prompt/SVU-MBA-Course-Review-Generator.md
> History of every version: https://github.com/AzizMarashly/SVU-MBA-Course-Review/blob/main/prompt/CHANGELOG.md
> and the repository tags (`v0.1`, `v0.2`, ...). Generated review pages for each course are
> published from the same repository.
>
> **Licence:** CC BY-NC-SA 4.0 — attribution, non-commercial, share-alike — for the prompt **and
> for every review file generated with it**. Full text in `LICENSE.md` at the repository root;
> what it means for the output in §19.

> **Changes in v0.12:** a defined duplicate test, a whole-bank consolidation pass and one
> frequency rule (§5a–§5c); coverage counted by a unit's own content, and a change report on
> regeneration (§9, §0e); minimum quality for reconstructed questions (§3b), essay answers with
> an expandable full model answer (§7b), and clearer low-confidence rules (§7c); procedural
> chapters: one method per problem type, a number before the symbol, a rule-based fast route,
> the book's unsolved exercises solved (§7e); figures drawn from the question's data, step-by-step
> reveal and an "Essentials" view in the HTML (§13a, Appendix A); deliverable versions as `vMAJOR.MINOR`
> and immutable source files (§0d, §0e); an explicit priority order (§0a). Earlier versions:
> see the changelog.

---

## PROJECT SETTINGS — fill these in

| Setting | Value |
|---|---|
| Review title | `<<< e.g. مراجعة كاملة لمادة … >>>` |
| Course / subject | `<<< course name in both languages >>>` |
| Chapters in scope | `<<< e.g. 1,2,3,5,7,8,9,10 >>>` |
| Primary reference | `<<< exact filename of the textbook >>>` |
| Expected exam format | `<<< e.g. mostly MULTIPLE CHOICE >>>` |
| Question language | `<<< ENGLISH / ARABIC / MIXED >>>` |
| Explanation language | `<<< e.g. ARABIC >>>` |
| Interface language | `<<< e.g. ARABIC — toolbar, headings, answer-block labels (§7a) >>>` |
| Interaction mode | `<<< ASK (default) / DECIDE — see §0c >>>` |
| Pilot chapter | `<<< chapter number, or NONE — see §0b >>>` |
| Output base name | `<<< title >>>` — files are named `<base>_vMAJOR.MINOR.<ext>`, see §0e |
| Working directory | `.review_generation_working_directory` (inside the course folder, §0d) |
| PDF / DOCX | `<<< ASK AT END (default) / ALWAYS / NEVER >>>` |
| Units per chapter (optional) | `<<< default: the TOC level giving roughly 5–15 units per chapter — §9 >>>` |
| Similar-stem threshold (optional) | `<<< default: tf-idf cosine ≥ 0.6 on the normalised stem — §5b >>>` |
| Spec version | `v0.12` — write this into the output metadata (§16) |

---

## 0. Ground rules that govern everything below

### 0a. Priority when rules conflict

Instructions in this document will sometimes pull in different directions. Resolve conflicts in
this order, highest first:

1. **Correctness against the primary reference** — every answer, page and method; never traded
   for anything below.
2. **Faithfulness to the source wording** of questions and options (§6).
3. **Coverage** — every in-scope unit of the book asked on its own content (§9), and no content
   lost between versions (§0e).
4. **Exam focus** — the form, order and emphasis the exam uses (§3b, §7e, §10).
5. **Brevity and non-repetition** of answer blocks (§7).
6. **Visual style and formatting** (§12, §18).

When a lower rule would force you to break a higher one, break the lower one and say so in the
methodology.

**Non-negotiables of every run:** every answer cites a verified page that states the fact (§7);
every in-scope unit is asked on its own content (§9); one claim, one record — and a book review
item or a verbatim exam item always keeps its own card (§5a); essay answers keep a full model
answer (§7b); a low-confidence flag only for the reasons of §7c; no source file is ever modified
(§0d); nothing is invented — no option, page, method or data set (§17).

### 0b. Pilot chapter — approve the style before the full run

If the settings name a pilot chapter, do the following before touching the other chapters:

1. Run §1–§10 for the pilot chapter only, then render a complete HTML file for it with every
   feature of §13a and Appendix A in place. Save it in `pilot/` inside the working directory (§0d, §0e).
2. Stop and ask the user to review the style: answer-block length, keyword bolding, how
   reconstructed exam questions read, the importance markers, the chapter opener.
3. Apply their corrections to the pilot, and record them as additional rules in the methodology
   so every later chapter follows them.
4. Only then continue with the remaining chapters.

In DECIDE mode (§0c) the pilot is still built and saved, but the run continues without waiting.

### 0c. Interaction mode — ASK or DECIDE

The document names a small number of points where you stop and ask the user: the pilot review
(§0b), generated-question volume (§9), and optional formats (§13e). Elsewhere you decide and
state the decision.

- **ASK** (default): stop at each of those points and wait.
- **DECIDE**: never stop. Use these defaults, and list every default you applied in the
  completion summary: pilot built and saved, run continues; generated questions for every unit
  reported as "mentioned but never asked" (§9 step 2), plus at most three per chapter for units
  not covered at all, chosen in the order of the book; HTML only, unless the settings say ALWAYS.

You may still stop in DECIDE mode when genuinely blocked — corrupted extraction with no visual
fallback, a missing primary reference, an unreadable scope — but not for preferences.

### 0d. Working directory — everything intermediate lives there, and a later agent can resume

**First action of every run:** look for the working directory named in the settings, inside the
course folder.

- **If it exists**, read its `STATE.md` before anything else, then continue from the last
  completed stage. Do not re-extract, re-verify or re-score anything the state file marks as done
  unless the source files have changed (compare the hashes in the ledger). Say in your first
  progress update which stage you resumed from.
- **If it does not exist**, create it and start from stage 1.

Nothing intermediate is ever written to the course folder itself — only the final deliverables
go there (§0e). **Source files are immutable once added:** never edit, annotate or rename a
supplied file (no status notes such as "not yet in the bank"); the ledger records its hash, and
status lives in `STATE.md`. The working directory holds, in fixed subfolders:

| Path | Contents |
|---|---|
| `STATE.md` | The handoff file — see below |
| `ledger.json` | Source ledger (§4): every file, its hash, group, type, include/exclude reason |
| `chapter_map.md` | The chapter map (§2a) with evidence |
| `extracted/<source-id>/` | Raw extracted text per source, OCR output, notes on what was read visually |
| `bank.json` | The verified bank checkpoint (§13d) — the single source of truth |
| `coverage.md` | Unit audit, focus areas, generated-question decisions (§9, §10) |
| `pilot/` | The pilot chapter file and the user's style corrections (§0b) |
| `qa/` | Every QA check's output (§15), the consolidation log (§5b), the change report (§0e) |
| `render/` | Scripts or templates used to turn `bank.json` into the deliverables |
| `archive/` | Superseded deliverable versions (§0e) |
| `VERSIONS.md` | Version log of deliverables (§0e) |

**`STATE.md` is written for the next agent, not for the user.** Update it at the end of every
stage and before any stop for user input. It contains, in this order: (1) spec version,
interaction mode, settings in force including the unit level (§9) and the similar-stem threshold
(§5b) actually used, date of the last update; (2) a stage checklist — stages 1
to 15 of this document — each `done`, `in progress` (with what remains) or `not started`, with
the files it produced; (3) decisions not obvious from the files: chapter-map judgements, excluded
sources, pilot corrections, importance deviations, DECIDE-mode defaults; (4) known problems and
open questions — unresolved questions, low-confidence ids, anything that could not be tested; (5) **"To continue":** the exact next step in one or two sentences, so an agent
with no memory of this run can pick it up. Keep it factual and short; if you cannot finish a
stage, record exactly where you stopped.

### 0e. Deliverable versioning — the latest file is always the one in the course folder

Every deliverable filename carries a version `vMAJOR.MINOR`: `<base>_v1.0.html`,
`<base>_v1.1.html`, with the same number across formats produced from the same bank.

- **MAJOR** is the generation of the question bank: `0` for a draft made before a full run under
  this prompt, `1` for the first full generation. Bump MAJOR only when the bank is
  **regenerated** from the sources (a new full run), and reset MINOR to `0`.
- **MINOR** counts every other release placed in the course folder in that generation: a new
  source, an answer or page fix, merged records, a re-render for a newer prompt, a style change.
  Never overwrite a deliverable in place; a partial or test build that stays in the working
  directory consumes no number.
- **Only the latest version stays in the course folder.** When a new version is produced, move
  the previous one into `archive/` in the working directory.
- The version also appears **inside** the file: on the cover, in the browser title, and in the
  end-of-file metadata next to the spec version (§16).
- `VERSIONS.md` records, per version: number, date, spec version, formats produced, what changed
  since the previous version (one to three lines), and the bank checkpoint it was rendered from.
- The pilot file (§0b) is named `<base>_pilot_ch<N>_v1.0.html` and kept in `pilot/`.
- **A regeneration (MAJOR bump) produces a change report** in `qa/`: for every record of the
  previous bank, whether it was kept, reworded, merged (into which record), split, dropped or
  shortened (answer text under half its previous length), with the reason; and a list of
  **concepts the previous version asked that no question asks any more**. That list must be
  empty or every entry justified — a regeneration may not lose content silently (§0a priority
  3). The previous bank is an input to the run: each chapter helper receives its chapter's
  previous records and returns a disposition for each.

---

You are in a directory that contains all the material for the course above. Read **all** of it
and understand it first, then index it: the primary reference; previous exam files, question
banks, screenshots, scanned documents; answer keys; summaries, study guides, slides and notes.

**Do not merely combine the attached files. You must read, classify, deduplicate, verify,
explain, score, format, render, and test the final deliverables.**

You may split the work across helpers (e.g. one per chapter for stages 5–9) if your environment
supports that. Give each helper a written brief that carries: the rules of §3b, §5–§7 and §9;
the chapter map (§2a); the ledger's source ids (§4); the unit list of its chapter (§9) and the
duty to record the unit on every record; the pilot corrections (§0b); the chapter's previous
records on a regeneration (§0e); and the duty to list every record whose deciding page lies in
another chapter, as input to §5b. **One agent must own** the source ledger, the consolidation
pass (§5b), scoring and the final quality checks, so counts stay consistent across chapters.
Chapter helpers never merge across chapters; the consolidation pass does.

---

## 1. Read the reference material first

Read the primary reference completely before touching any question file. Build an internal map of:

- chapter boundaries and section/subsection headings
- definitions, models, frameworks, formulas, tables, worked examples, solving methods (§7e)
- printed page numbers vs. PDF page numbers (state whether they match)
- the book's own review set and whether the book prints its answers (a tick, a highlight, a key
  page) — the book's mark is the book's answer, verified against the chapter text

The primary reference is the authority. **Do not blindly trust answer keys found in exam files
or summaries.** Where the material conflicts with established science, present both: *"Answer
according to the provided material"* and *"Scientific correction"*.

**Always show the book's answer when the question comes from the book — even when it has been
corrected. Keep the wrong answer that was corrected visible for reference.**

### 1a. Verify your text-extraction toolchain before trusting it

Before extracting anything, prove the extractor actually reproduces the document's language.
Some PDF fonts carry no Unicode mapping and will silently yield empty text, mojibake, or
Latin-only output while appearing to succeed. Extract one known page and compare it against
the rendered image. If extraction is broken for a file, say so and fall back to visual reading —
never silently work from corrupted text.

---

## 2. Check whether the folder mixes more than one curriculum

Folders shared between students often contain material from an **older or different version of
the course** whose topics do not exist in the current textbook.

- Build a discriminator: pick 4–6 topic keywords unique to the current book and 4–6 unique to
  the suspected other course, normalise the text, and classify every file.
- Verify suspicions concretely — a different instructor's name, a table of contents that doesn't
  match, page citations that point to the wrong content.
- **Exclude out-of-scope sources from the verified bank**, and list every excluded file **by name**
  in the methodology, with the reason.
- Do not discard them blindly: a question from another curriculum may still be usable if its
  concept genuinely exists in the current book — re-verify it from the book and never import its
  answer key (§11b).

### 2a. Map the sources' chapter names to the book's

Exam files, summaries and slides often number things differently from the book — "Lecture 3"
may be the book's chapter 5, "Week 4" may span two chapters. Build a **chapter map** once, from
evidence (headings, topics, page citations), before assigning any question to a chapter. Record
it as a table in the methodology: source label → book chapter(s) → evidence. Every question is
assigned through this map, never by guessing per question. Where a label cannot be mapped
confidently, say so and put its questions on the unresolved list (§3).

---

## 3. Extract all questions from every source

Cover every format present: searchable PDF, scanned PDF, standalone images, screenshots, images
embedded inside Word files, and text held in tables, text boxes, headers and footers.

Cover every question type: multiple choice, true/false, matching, fill-in-the-blank, short
answer, essay, and the book's end-of-chapter exercises, solved or not (§7e).

**Use OCR where necessary. Visually inspect every scanned page and every image rather than
relying only on text extraction — and state how many images you inspected.** Photographs of
answer sheets contain no extractable text at all; they must be read visually or they will be
silently skipped.

Give every raw item an id (`<file>#<index>`) — records cite these ids (§5b). Questions that
cannot be confidently assigned to a chapter go to an internal unresolved list, reported at the
end. A recalled item that names only a topic with no recoverable question makes no record; list
it as "topic only" with its unit. A recall that names a problem type of §7e and what was asked,
without its numbers, is not topic-only — see §5c.

### 3b. Exam questions lean towards multiple choice — a direction, not a rule

The real exam is mostly multiple choice, but past-exam files are often **written from memory by
students**: the question appears as a plain sentence or a one-line "what is X?" although it was
asked as a multiple-choice item, and the original options are lost.

- **Exam questions (section 1 of each chapter):** when a question is in free form but was most
  likely a multiple-choice item, present it as one — the recalled wording as the stem, the book's
  answer as the correct option, and distractors that are real terms of the same unit or an
  adjacent unit of the same chapter. Label it `reconstructed options` in the gray metadata and
  keep the recalled text verbatim as `original` beneath it. If the source already has options,
  keep them exactly.
- When the book's own review set has an item on the same claim, reconstruct in the book's form —
  its stem direction and its option set — since that is the form the exam most likely reused;
  say so in the metadata.
- **Minimum quality of a reconstructed item:** exactly four options; exactly one right by the
  book; no invented term; no two options that are synonyms or near-synonyms in the question
  language. When the recall itself lists options that break this (three options, ambiguous
  synonyms, "1 and 2 and 3" numbering), the card gets clean options and the recalled list stays
  in `original` with a note — the recall is evidence, not the card.
- Because the reconstructed options may differ from what the exam actually shows, the *Why* and
  *Remember* lines must let the reader recognise the right answer among **any** set of options.
- **Textbook questions and questions from other sources keep their original format.** Never
  convert essay or matching questions, or anything whose answer is a list or a process.
- **Generated questions (§9):** prefer multiple choice, but use whatever form tests the idea
  honestly.
- Use judgement. A question that reads naturally as it is needs no change. The aim is that the
  exam section *feels* like the exam, not that every item is forced into four options.
- Report in the completion summary how many exam questions were reconstructed.

---

## 4. Identify duplicate source files before counting frequency

Compute a hash (e.g. MD5) of every file **before** counting anything. The same document is often
present several times under different names, in different folders, or converted to another
format. Also detect *dependent* copies — a question file and its separate answer-key file, or a
PDF and photographs of the same pages — and treat each such group as **one** source.

Maintain a source ledger recording, for each independent source: an id, its files, its type, and
why it was included or excluded.

---

## 5. Deduplicate into canonical questions

Merge variants of the same question into one canonical record holding:

- id, chapter, unit (§9), question type (and `reconstructed` flag where §3b applies),
  canonical wording, notable variants, the raw source-item ids it was built from (§3), and a
  **one-line statement of the claim it tests** — the book fact whose knowledge decides the
  answer, stated so that a true/false item and its negation, or a definition and its reverse,
  carry the **same** claim (the expected answer is the fact, not the letter or the true/false
  value)
- verified answer, repetition count, list of independent sources, exam sittings among them
- reference page(s), confidence (§7c), importance score (§10), any ambiguity worth flagging
- for problem-type questions (§7d, §7e): the structured data (table, network, cash flows)
  the figure and the checks are computed from

A raw source item feeds one record. A raw item that combines several sub-questions may feed
several records, each citing it with a sub-question label.

### 5a. The duplicate test — one claim, one record

Two records are **duplicates when they test the same claim of the book**: same concept and same
expected answer, whatever the source, wording, chapter or form. Apply, in this order:

1. **Same claim, same wording** — stems and options match after normalisation (spacing,
   punctuation, diacritics, option order) apart from OCR and recall noise, and no term is
   replaced by another term → one record: sources unioned, the other copies kept as variants
   with their source code, both type tags carried.
2. **Same claim, different wording.** A **book review item** (the book's own end-of-chapter
   question) and an **exam item recorded with its original wording and, if any, its original
   options — not reconstructed (§3b)** — each keep their own card: exams reuse them word for
   word, and a student practising the book's set must meet them in their form. Such cards are
   cross-linked ("same claim as #…") and share one frequency and one importance score, computed
   from the union of their ledger source ids; each card keeps its own section (§11b), type tags
   and raw item ids, and its metadata line shows the union with a link to the other card; §10a
   and the reference lists (§11c) count the claim once. Every other record —
   a paraphrased recall, a reconstructed item (§3b), a summary rewording, a generated item — is
   folded into the card that keeps: with the **same form** (both MCQ, both true/false …) as a
   variant; with a **different form** (MCQ / true-false / short answer / reverse definition) as
   an **"also asked as"** line (form, wording, key, sources). A recalled "define X" and a
   definition MCQ asked the other way round are the same form (the recall fixes no direction).
3. **Not duplicates:** the same rule applied to different data with a different expected answer;
   two generated items covering different units; records that only share a data table — group
   those under the table instead (§7d). If one sitting asked both forms itself, keep both and
   cross-link them.

**Kept record.** A card that step 2 protects (book review item, verbatim exam item) is always the
keeper; when neither or both records are protected, keep: the exam item; then the record with
more independent sources; then the chapter that owns the deciding book page; then MCQ /
true-false over short answer or essay. The dropped id stays as an alias (its anchor still
resolves). **Never merge two records
whose answers differ** until the book settles the answer with a page; log the decision.

### 5b. Consolidation pass — whole bank, after the chapters, before scoring

Chapter helpers working in isolation produce cross-chapter duplicates, double-counted frequency
and contradictory keys. After all chapters are built and before importance scoring, one agent
reviews the **whole bank** with the test of §5a, helped by a neighbour report (each record's
nearest cross-chapter neighbours by stem, answer and bold-term similarity). Word similarity is a
review aid, never a decision: it misses paraphrased and reversed pairs and flags look-alikes that
are different claims, so also read the bank once end to end (one line per record: id, form,
unit, pages, sources, stem, answer). Every merge, fold and rejected candidate is logged in `qa/`
with the claim and the book page.

**Build checks**, run on every build: a hard error for the same option set (compared as
normalised text, not position) with a similar stem (tf-idf cosine ≥ 0.6 on the normalised stem
unless the settings override it; record the value used in `STATE.md` and the consolidation log)
and a different key; a hard error for
a raw item id used by two records (sub-question labels and number-less credits excepted); a hard
error for a merge whose answers disagree; and the neighbour report as a warning.

### 5c. Frequency — what counts as a source occurrence

**The repetition count equals the number of independent sources containing the claim, never a
sum over merged records and never the number of files.** A question is counted once per
independent source even if it repeats inside that source; one file may hold several exams, each
counting separately only if it is genuinely an independent sitting. In addition:

- **A problem recalled without its data** ("a critical-path problem with seven questions") counts
  as exam evidence on the existing records of the same problem type of the chapter's Methods
  block (§7e) **and the same format** (table or calculation records), each with a note that the
  sitting's data were not recalled.
  Never count it as topic-only, and never invent a data set. Apply this the same way to every
  sitting.
- **A student summary that reproduces the book's review set** is an independent source in the
  frequency and importance score (§8): its presence shows what students study. State the rule
  in the methodology so every run counts alike.

---

## 6. Edit conservatively

Fix OCR damage, broken spacing and obvious typographic corruption. Never invent facts, options,
or wording. If an option is missing from the source, say so — do not complete it. The only
permitted rewriting is the option reconstruction in §3b, and it must be labelled.

---

## 7. Verify every answer, then explain it briefly

For each question, verify the answer against the primary reference, then write the answer block
using the fixed template below. **Never cite a page you have not verified.** Cite the page that
states the fact, not a review page or a reference list; when several pages support the answer,
cite first the one where the answer's wording appears verbatim. An answer or page is changed
later only with a book page that settles it.

### 7a. Answer block template — fixed order, nothing else

The labels shown below are rendered in the **interface language** from the settings; the text
after each label is in the explanation language. Keep the labels short and identical on every
question.

```
✔ Answer: <option letter> — <option text>          (or the answer itself for non-MCQ)
Why: <one or two sentences, in the explanation language>
Remember: <2–5 bold keywords, or a short memory hook>
Distractors: <one short clause per wrong option, only where it is plausibly confusing>
Ref: ch. N · p. <printed> (PDF <n>)
```

Optional lines, only when they apply:

```
Book says: <the book's / source's original answer, when corrected>        ← red
Other source: <contrary answer from a summary or key, labelled by source>  ← red
Scientific correction: <when the material conflicts with established science>
⚠ Low confidence: <one clause saying why — see §7c>                        ← amber
Also asked as: <form · wording · key · sources>, one line per folded form (§5a)
```

### 7b. Writing rules for the answer block

- **Say each thing once.** The answer line states the answer; the *Why* line does not repeat it;
  the *Distractors* line does not restate the *Why*. If a line would only repeat another line,
  drop it. True/false items usually need no *Distractors* line.
- **Why** is at most two sentences and names the single concept that decides the question. Do not
  summarise the whole topic. Do not open with "The correct answer is…". For reconstructed exam
  questions (§3b) it may run to three sentences so the idea survives a different set of options.
- **Remember** holds the words a reader needs to recognise the right option in the exam: the
  defining term, the number, the name of the model, the contrast that separates it from its
  nearest distractor. Keywords are always **bold**.
- **Distractors** covers only the options a student is likely to confuse with the answer. One
  clause each, e.g. *"B — that is **X**, not Y"*.
- **Bold is for keywords only** — the term, number or name that unlocks the answer, in the *Why*
  and *Remember* lines. Never bold whole sentences or more than a few words per line; no bold in
  stems or options.
- No filler phrases ("as we know", "in other words"). Do not repeat the stem in the explanation.
- **Essay, list and process questions keep their depth.** The answer line gives the key points
  (the list heads, at most about 40 words); beneath it a collapsed **"Full model answer"** holds
  the book's own content for those points — typically 100–200 words, keywords bold, with the
  page of each point — so the block stays scannable and the student who must write the essay
  still has the whole answer. The full model answer, like the working of §7d, is outside the
  word target.
- Target length for the whole block, excluding the optional lines: **40–80 words**. Go longer only
  when a scientific correction, a conflict, or a reconstructed question genuinely requires it.

### 7c. Flag low-confidence answers only

Most answers need no confidence remark. Add the `⚠ Low confidence` line **only** when one of
these is true:

- the book supports the answer with a single passing sentence rather than a definition or section,
  or the item's concept is absent from the book (then also `Book says` / `Other source` as fits);
- the sources disagree and the book does not settle it;
- the question wording is ambiguous, or was recalled from memory and could mean two things, so
  that the answer would change with the reading;
- the answer relies on a scientific correction rather than the book.

**Do not flag** because the item's chapter or unit placement is uncertain; because a distractor
you fear is not among the options; because the answer is stated verbatim or marked by the book's
own key; or because a source's key differs when the book settles it (use `Other source`). State
the reason in one clause, with the page that would settle it if one exists. Never add a
"high confidence" label — silence means confident. A flag is removed only by citing the book page
that settles it, or by showing that its reason is one excluded above, with the page that states
the answer. Report the count of flagged questions in the completion summary.

### 7d. Tables and calculations — show the data as a table and the working as steps

Applies to every question whose stem carries tabular data (items with durations and
predecessors, per-task figures, cash flows …) and to every question whose answer is a number or
a set of numbers.

**Data table.** The stem keeps only the question sentence and a short lead-in. The values go into
a real table under the stem: a header row, one row per item, numbers and codes left-to-right
inside cells, no bold. Never flatten a table into a sentence of values. Sibling questions on the
same data set share one table, repeated under each of them so every question stays
self-contained, and are grouped on the page.

**Answer block order for these questions:**

```
✔ Answer: …
Fast route: <rule-based deduction, when §7e allows one>
<Working table>      the full working when there is one — every item's intermediate values —
                     shared by sibling questions
Calculation:
  • given values, one per line, each with its origin: "X = 12 (given)", "duration = 20 =
    largest value in the table", "the only successor of A is D (predecessor column)"
  | Step | Required | Formula | Substitution | Result |     one row per step, in solving order
  optional one-clause closing note (which item satisfies the condition)
Why: the rule that decides the question, in words — no arithmetic here
Remember / Distractors / Ref as in §7a
```

Rules:

- **Formula and substitution cells hold symbols and numbers only** (Latin letters, digits,
  `+ − × ÷ = ≈ min max`); they render left-to-right in a monospace face. Words in the
  explanation language go in the *Required* cell, the given lines and the notes.
- **Every number has an origin.** A value that is not in the question or its table is introduced
  in a given line or a step note saying where it came from.
- **One step per quantity**, in the order a student would solve it, labelled with the step of the
  chapter's method (§7e) when one exists. A one-line calculation is still a calculation block
  with one step.
- **Essay-type calculation questions** (draw the network, level the resources) keep a short prose
  answer (result, path, duration, conclusion); path sums become steps, per-item values a working
  table, and an allocation over time shows a per-period table before and after.
- **Symbols legend.** The course keeps one glossary of symbols; each entry has separate fields —
  name in the explanation language, English name, formula in symbols only, a one-sentence note in
  the explanation language that spells out every other acronym it mentions (acronym in
  brackets), and **a one-line numeric example** ("BCWP 12, BCWS 10 → SPI 1.2"). Never mix the
  two languages in one field; each field renders on its own line with its own direction. Under
  every question table an always-visible row of chips names the symbols that question uses;
  tapping a chip, or any underlined symbol in a table or calculation cell, opens a bottom sheet
  with the fields, a close button and the question's other symbols (the primary path — most
  readers are on phones); on pointer devices hovering shows the same card inline.
- On a phone the step table stacks into one card per step; wide data tables scroll horizontally
  inside the question card.
- The word target of §7b does not count the working table, the calculation block or the legend.

### 7e. Procedural chapters — one method per problem type, a number before the symbol

A chapter is procedural when two or more of its records share a solving method (a calculation
block of §7d with the same steps). Students find such chapters heavier than theory: worked
answers that each take their own route are hard to follow, and symbols hide what a small number
would show. For every procedural chapter:

- **Problem types and methods.** Identify the chapter's recurring problem types (usually three
  to six). Directly after the opener (§11a), a collapsible **"Methods"** block, closed by default
  with the type names in its summary line, gives one entry per type: its name, how to recognise
  it (what the stem gives and asks), the solving steps as an ordered list with the output of
  each step, and the book page of the method. Prefer the order the course teaches (book, then
  lecture material) over a shorter or cleverer order — students compare against what they were
  taught. If the book gives no method for a type, say so and cite the nearest page; never
  present your own order as the book's.
- **Every worked answer of a type follows the same steps in the same order** and names the step
  it is on (the *Step* column of the calculation block, §7d); every *Step* label links to its
  Methods entry. A reader who knows the Methods block can predict the shape of every answer.
- **A concrete number before the symbol.** Where a concept is a relation between quantities (a
  dependency type, an offset, a ratio, an index), the Methods entry and the glossary (§7d)
  introduce it with one tiny numeric example ("A ends on day 5, lag 2, so B starts on day 7")
  before the symbolic form. Symbols stay in the glossary for those who want them.
- **Fast route — decide by rule when the exam allows it.** Where the expected exam format is
  multiple choice, many problems are answered by a rule or a comparison without the full
  calculation (the sign of a variance, which of several indices is lowest, which pattern breaks
  a rule). For such items the answer block carries a **Fast route** line — the deduction in one
  or two sentences with the page of the definition it follows from, labelled *derived* when the
  book does not state it in those words — and the full calculation below it stays as the check.
  Only state a shortcut that follows from the book's definitions; if none exists for a type, say
  nothing rather than inventing one.
- **The book's unsolved exercises.** End-of-chapter exercises that the book leaves unsolved are
  strong exam predictors. Solve every one of them with the chapter's method, with a page for
  every rule used, as records in the textbook section (§11b) labelled **"solution generated —
  not the book's"**. They are textbook records, not generated questions of §9: frequency 1
  (the book), score by §10b.
- **Spatial problems carry their figure.** Problems that are spatial or temporal by nature
  (networks, dependencies, schedules, allocations over time, values read against limits) get a
  figure in the HTML drawn from the record's structured data (§5), never typed by hand, with
  what the question asks about highlighted (the decisive path, the overloaded period, the point
  outside the limits). The build recomputes the answer from the same data and fails on a
  mismatch. Presentation rules in Appendix A.6.

---

## 8. Use summaries and answer keys as independent cross-checks

Study summaries often reproduce the book's end-of-chapter questions *with worked answers*. Such a
file is a genuine independent source — register it in the ledger, add it to the source list of
every question it confirms, and count it (§5c).

Cross-check its key against your verified answers item by item and **report the agreement rate**
(e.g. "64 of 65 matched"). Where it disagrees with the book, the book wins, but **display both
answers at the question** — yours as the answer, the contrary one on the `Other source:` line
(§7a), for comparison only.

---

## 9. Audit concept coverage, then fill the gaps

The sources together may leave whole ideas in the book untested.

1. Split every in-scope chapter into **units, using the book's own table of contents** at the
   level that yields roughly 5 to 15 units per chapter unless the settings override it (record
   the level chosen in `STATE.md`). Report the total count.
2. For each unit, check whether any question **asks the unit's own content**: a unit counts as
   covered only by a question whose expected answer is a term, rule, list, number or
   distinction that the unit itself defines, and whose *Ref* page lies inside the unit's page
   range. A question that touches the topic, whose concept is defined in another unit, or that
   mentions the unit only inside an explanation does **not** count — report those separately as
   "mentioned but never asked". Record the unit on every question — the importance score (§10)
   needs it.
3. Report three numbers: asked on own content / only mentioned / not covered at all.
4. For every uncovered unit, **write a new question yourself**, from the book's own wording,
   with a page number you have verified. Prefer multiple choice with same-chapter distractors. A
   unit that is a mere introduction still gets one question on its one concrete statement.
5. **Before writing them, check the volume.** If the generated questions would exceed the number
   of real questions in a chapter, or exceed roughly a third of the whole bank, **stop and ask
   the user** whether to generate all of them, only the most important units, or none. Show the
   per-chapter numbers when asking. In DECIDE mode apply the §0c default instead.
6. Put these in a **separate, clearly labelled fourth section** so they never blend into the real
   exam questions. Give them a repetition count of zero and a source label meaning "generated".
   State in the document that they exist to close gaps and are **not** predictions of the exam.
7. **Do not repeat an idea.** Verify mechanically that no generated question duplicates an
   existing one (§5a), and that no two generated questions cover the same idea. Report the check.
8. Re-run the audit after adding them and report the final coverage as `N of N`.
9. A chapter that needs no generated questions gets none — say so. When regenerating, a
   generated question of the previous version is dropped only if a real question now asks the
   same content by the test in step 2; otherwise it stays (§0e change report).

Some chapters may be fully covered already; that is a valid and useful result.

---

## 10. Score importance, then order by it

The exam papers and the book's own questions together show **which areas the teacher keeps
returning to**; two questions with the same repetition count are not equally important if one
sits in a unit with ten other questions and the other stands alone.

### 10a. Focus areas

For every unit in scope, count the distinct claims that test it (cross-linked cards of §5a count
once), split by origin (exam / textbook / other). Rank units by exam-question count first, then total. The top of that ranking
is the **focus areas** list. Each chapter's opener (§11a) names its top focus areas; the
methodology holds the full table.

### 10b. Importance score

Give every question an **importance score from 1 to 5**, computed from the fixed base below so
that scores mean the same thing across courses and runs. Describe the computation in the
methodology; if the material forces a deviation, state exactly what changed and why.

**Base score, from the number of independent exam sources containing the question (§5c):**

| Exam sources | Base |
|---|---|
| 0 (textbook or other sources only) | 1 |
| 1 | 2 |
| 2 | 3 |
| 3 or more | 4 |

**Bonuses, added to the base, total capped at 5:**

| Signal | Effect |
|---|---|
| Also appears as a textbook end-of-chapter question | +1 |
| Its unit is a focus area (§10a) | +1 |
| Generated to fill a gap (§9) | fixed at 1 — no base, no bonuses |

So a question asked in one exam and also in the book scores 3; asked in two exams inside a
focus area scores 4; asked in three exams, in the book, in a focus area scores 5. Cross-linked
cards of one claim (§5a) share one score.

Render the score as a small gray marker next to the repetition count (e.g. `★★★★☆` or `4/5`),
in the same low-contrast style as the other metadata. **The score is a study aid, not a
prediction** — say so once in the "how to use" section (§11).

### 10c. Ordering

Within every section of every chapter, order questions by **importance score, then repetition
count, then question type** (multiple choice before others). Show `Frequency: N independent
sources` with each question.

---

## 11. Document structure

Cover → how to use → scope and source summary → chapters → methodology → source files (§11d) →
most repeated and most important (collapsed) → table of contents → file metadata (including the
spec version, §16).

**Keep the start of the file simple. Put all metadata, the reference lists and the table of
contents at the end.** There is no separate answer-key section — every answer lives with its
question.

The **"how to use"** section is short, in the interface language, and explains the markers the
reader will meet on every question, each in one or two sentences: **Frequency** (how many
independent sources asked it); **Importance** (★ 1–5, what it is built from, and that it is a
study aid, not a prediction); **⚠ Low confidence** (appears only where the answer rests on thin
evidence, §7c; its absence means the answer was verified normally). It also names the reading
modes, the sliders, the Essentials view (importance 3 and above, details folded), the chapter
collapse controls and the "Collapse all" / "Expand all" buttons (§13a, Appendix A), notes that the
importance slider at 2 or more hides generated questions, and suggests a reading order: exam
questions first, then textbook, then the rest.

### 11a. Chapter opener — two-line context summary

Every chapter starts with a short **"In this chapter"** box, before the first question:

- **Two lines, no more.** Line 1: what the chapter is about, in one sentence. Line 2: the 3–6
  terms, models or numbers the questions below keep returning to, in **bold**, comma-separated —
  drawn from the chapter's focus areas (§10a).
- Written in the explanation language, from the book's own wording, and consistent with the
  questions that follow — it is orientation, not a summary of the whole chapter.
- Visually distinct from questions (a light box), and never collapsed: the reader must see it
  before the first question. In a procedural chapter the Methods block (§7e) follows it.

### 11b. Four sections inside each chapter

Inside each chapter, order the questions in **four sections**:

1. **Exam questions** (from past papers — presented in exam-like form, §3b)
2. **Textbook questions** (the book's own end-of-chapter set and exercises, original format;
   unsolved exercises carry the "solution generated" label of §7e)
3. **Questions from other sources** (summaries, study guides, older-curriculum collections whose
   concept exists in the current book and whose answer was re-verified from it — original format)
4. **Generated questions** (§9), with a short note explaining what they are

Within each section, order by §10c. **Make the type or types of each question explicit** — one
question can be both an exam question and a textbook question. Sections 3 and 4 each carry a
one-paragraph explanation of their origin.

Per question, show: number and id, repetition count, importance marker, section and type tags,
question text, options (and data table, §7d), then the answer block (§7a).

### 11c. Reference lists at the end, collapsed

After the methodology, add two lists, each inside its own collapsed `<details>` block, **with no
answers exposed**:

- **Most repeated questions** — threshold chosen to keep the list useful (if most questions sit at
  2 sources, list 3+), at most about 30 items, each linking to the question.
- **Highest importance questions** — score 4 and 5, same format.

They are reference material for the last day before the exam, not the way into the document, so
they stay closed until the reader opens them.

### 11d. Source files — the reader must be able to see what the review was built from

The review file names **every file it was built from**, so a reader can judge its coverage, find
the original material, and notice when a source is missing or outdated.

**Appendix "Source files"**, placed after the methodology and before the reference lists, inside
its own collapsed `<details>` block, holding one table with a row per supplied file:

| Column | Content |
|---|---|
| # | Running number, also used as the short label on questions (below) |
| File name | Exactly as supplied, with its relative folder if the material was in subfolders |
| Kind | Textbook · past exam · answer key · summary · slides · screenshot / photo · other |
| Role | How it was used: primary reference · exam source · cross-check · excluded |
| Source group | The independent-source id from the ledger (§4); duplicates and dependent copies share one id |
| Pages / items | Pages read, or number of images inspected, or number of questions extracted |
| Note | Reason for exclusion (§2), duplicate-of, extraction problems (§1a), curriculum mismatch |

Rules:

- **List every file, including excluded ones and duplicates** — an excluded file with its
  reason, a duplicate pointing to the file it duplicates. Nothing supplied is silently omitted.
- The primary reference gets the first row, with its edition or year if the file shows it, and
  whether printed and PDF page numbers match (§1).
- File names as plain text, not links (the material is not published with the review); the name
  and its folder inside the course folder only, never a full local path.
- No personal data: keep a student's or instructor's name from a file name only if it is needed
  to identify the file; otherwise describe the file ("photos of the 2024 answer sheet, 6 images").
- A one-line summary above the table: total files, independent sources, excluded files, images
  inspected — the same numbers as the completion summary (§16).

**Short source labels on each question:** the gray metadata line lists the sources as **the `#`
numbers of this table** (`Sources: #3, #7, #12`), each linking to its row; generated questions
show `Source: generated (§9)`. The appendix is in the interface language with the file names
untouched; in the PDF and DOCX it is a plain table at the same position.

---

## 12. Bilingual formatting

Right-to-left text right-aligned, left-to-right text left-aligned, with correct paragraph
direction on every paragraph — not just visual alignment. No reversed or misplaced punctuation.
Use separate paragraph styles per direction, embed fonts, and never leave a heading orphaned from
the content it introduces.

Everything that is not question or explanation text — the toolbar, section headings, the
"In this chapter" label, the answer-block labels (§7a), the "how to use" text, the methodology
headings, button captions and the counter — is written in the **interface language** from the
settings, and the page direction (`dir` on the root element) follows it. Question text keeps its
own direction per paragraph regardless.

Beware: in a bidirectional paragraph, justification is *logical*, not physical. Verify the
rendered output rather than trusting the markup.

---

## 13. Deliverable formats

The **HTML file is the deliverable**. The PDF and DOCX are optional copies produced only on
request — see §13e.

### 13a. HTML — the primary interactive file

A single self-contained `.html` file. Each answer is hidden behind a native
`<details>`/`<summary>` control, collapsed by default.

- **No JavaScript is required for the reveal** — it must work with scripting disabled.
- It must work in any browser on phone, tablet and desktop, offline, opened directly from disk.
- No external assets, no CDN, no fonts to download — everything inline.
- JavaScript may add optional extras only — the toolbar, filters and views below, a visible
  counter, a light/dark toggle. All must degrade cleanly: without scripting everything is shown,
  every collapsible keeps its default state and the native control still works.
- Print styles open every chapter, section, page block, answer and step, and ignore the filters;
  say so near the print instructions.
- Respect the reader's light/dark preference and offer a manual override.

**What the student sees (details: Appendix A):** a sticky toolbar with a one-line bar and a
collapsible filter panel (A.2); filters — reading mode, importance and repetition sliders,
chapter, search — that combine as AND, keep their state per device and never hide a matching
question inside a collapsed parent (A.1, A.3); an **Essentials** view showing importance 3 and
above with secondary lines folded (A.4); chapters, sections, answers and page blocks that collapse
independently, with questions visible on open (A.5); figures drawn from the question's data and a
step-by-step reveal that keeps the answer line visible (A.6). Priorities: the reveal and the default
view work without scripting; phone width first; every control accessible; nothing a filter hides is
lost.

### 13b. PDF — plain reading and printing copy (on request)

A flat, non-interactive PDF: each answer printed beneath its question, every step and full model
answer open, figures included. **Do not attempt an interactive show/hide PDF** — only Adobe
Acrobat honours the reveal mechanisms; every other viewer shows all answers anyway. No form
fields, `/AcroForm`, `/OpenAction`, JavaScript or widget annotations, and no wording about a
reveal mechanism. Bookmarks for chapters and sections; all document metadata stripped except the
title.

### 13c. DOCX — editable copy (on request)

Fully editable, each answer under a collapsible Word heading, every question independent of every
other. State in the document that Word does not persist collapsed state in a `.docx` (the file
opens expanded), how to collapse all headings in one action, and that other editors may not
collapse at all.

### 13d. Bank checkpoint — save before rendering

Before producing any output file, save the complete verified bank as `bank.json` in the working
directory (§0d): every canonical question with its fields from §5, the source ledger, the unit
coverage table, the chapter map (§2a), the focus-area ranking and the symbol glossary (§7d).
Plain JSON, encoded **UTF-8 without a byte-order mark**, no personal data. Include the spec
version and the deliverable version it will be rendered into (§0e) at the top of the file.

This is the single source of truth for every rendered file. If a later fix is needed, edit the
bank, bump the deliverable version and re-render from `render/` rather than patching the HTML by
hand. Mention the checkpoint file in the completion summary.

### 13e. Ask before producing PDF and DOCX

When the HTML is finished and tested, **ask the user** whether they also want the PDF and/or the
DOCX, unless the settings table says ALWAYS or NEVER, or the interaction mode is DECIDE (§0c,
default HTML only). Produce only what they choose, from the same bank, and run the
format-specific checks in §15 for whatever you produce.

---

## 14. Privacy note

State plainly, in the document, that hiding answers is a study aid and not security: the answer
text exists inside the file and is reachable through search, copy, accessibility tools, page source
or file-structure inspection. It must not be relied on for a real exam.

**Prevent any personal data from your device or account being written into any file** — no author,
creator, company, or last-modified-by fields.

---

## 15. Quality assurance — test, don't assume

**Content:** unique ids; every question has an answer, an explanation, a verified page, a unit,
a claim line, raw source ids and an importance score; every question inside the declared chapter
scope; frequency equals the number of distinct sources (generated questions excepted); generated
questions never score above 1; no leftover markup artifacts (e.g. literal `**`) in any output.

**Duplicates (§5a–§5b):** the three hard build checks pass (same options + similar stem +
different key; raw id used twice; disagreeing merge) — negative-test each once by introducing a
violation; the neighbour report was read and every pair judged in the consolidation log; every
book review item and every exam item with original options is still its own card, unless merged
under §5a step 1 (same wording), in which case the merged card carries both type tags.

**Answer blocks (§7):** every block follows the template order; no block exceeds the word target
(counted without the working table, calculation block, legend and full model answer) without an
optional line, a reconstruction or an essay justifying it; every *Remember* line
contains at least one bold keyword; no bold inside stems or options; no *Why* line repeats the
answer text; low-confidence lines appear only with a stated reason, and none for a reason §7c
excludes; every essay or list question has a full model answer with pages. Run these as
mechanical checks and report counts, then read a random sample of 20 blocks by eye.

**Reconstructed exam questions (§3b):** each carries the label and the recalled original text;
exactly four options, exactly one right, no made-up term, no synonym pair; the *Why* line would
still identify the answer with different options.

**Tables, calculations and procedural chapters (§7d, §7e):** no stem contains a flattened table
(a run of separator-delimited numeric groups, or `|` characters); every numeric answer has a
calculation block; no *Why* line carries an arithmetic chain when a calculation block exists;
formula and substitution cells contain no bold and no explanation-language words; every symbol
used is in the glossary and every glossary entry has a numeric example; every procedural chapter
has a Methods block whose types are cited by the steps of every worked answer of that type;
every figure's result recomputed from its data equals the record's answer; every fast route
cites a page; every unsolved book exercise has a labelled solution. Report the counts of records
with a data table, a working table, a calculation block, a figure and a fast route.

**Coverage (§9):** every unit is asked on its own content by the test in step 2 (a sample of 20
"covered" units re-read by eye); after a regeneration, the change report exists and its list of
concepts no longer asked is empty or justified.

**Chapter openers (§11a):** every in-scope chapter has one, exactly two lines, before the first
question.

**Source files (§11d):** the appendix has exactly one row per file found in the course folder
(compare against a directory listing, ignoring the working directory); every question's source
labels resolve to rows in it; the summary numbers above the table equal those in the completion
summary.

**Importance (§10b):** recompute every score from the bank with the fixed base and bonuses and
confirm it matches what is rendered; no generated question scores above 1; no score exceeds 5;
cross-linked cards share one score.

**Interface language (§12):** no toolbar caption, heading or answer-block label is in a language
other than the interface language; the root `dir` matches it.

**Metadata (§16):** every produced file carries the spec version; the bank has no byte-order mark.

**Ordering (§10c):** within every section, importance never increases going down the list; ties
are broken by repetition. Verify mechanically.

**HTML:** exercise the file in a real browser at desktop width and at a phone width (about
390 px): reveal, every filter and view, collapsing, symbol sheet, figures, step reveal, state
across reloads, both themes, version numbers — the full checklist is Appendix A.7. Report what
you tested.

**Working directory (§0d):** `STATE.md` exists, every stage is marked, the "To continue" line is
accurate; no intermediate file was written to the course folder; no source file was modified
(hashes unchanged).

**Versioning (§0e):** exactly one file per produced format in the course folder, all with the
same version; earlier versions in `archive/`; `VERSIONS.md` has an entry for the current version.

**PDF (if produced):** verify structurally that no form fields, actions or scripts remain; render
pages and inspect them visually; confirm the answers are present and the layout is correct.
**DOCX (if produced):** parse it, confirm the heading structure,
render and visually inspect pages.

If a check cannot be run in your environment, say so explicitly rather than implying it passed.
When an automated check reports a failure, **inspect each hit before reporting it** — keyword
audits produce false positives from legitimate content.

---

## 16. Deliverables

In the course folder: the versioned HTML file and any requested PDF/DOCX (§0e). In the working
directory: the bank checkpoint, `STATE.md`, `VERSIONS.md`, the consolidation log, the change
report (on regeneration), the pilot file if one was built, and the archive of earlier versions
(§0d). Plus a completion summary.

**Every output file carries both versions** in its end-of-file metadata block — the spec version
from the settings (e.g. `Generated from prompt v0.12`) and the deliverable version from its
filename (e.g. `Review file v1.3`) — in the HTML footer, the PDF's last page, the DOCX's last
section and the bank's header.

The completion summary reports:

- the working-directory path and the stage resumed from (§0d); the deliverable version and what
  changed (§0e), with the change report's counts on a regeneration; the interaction mode and
  every DECIDE default applied (§0c); the pilot corrections (§0b)
- the chapter map (§2a) with unmapped labels; files, duplicates, independent sources, images
  inspected, and confirmation that the appendix (§11d) lists every file
- raw occurrences, unique questions, merges and folds with any answer conflict and how the book
  settled it (§5b); reconstructed (§3b), out-of-scope and unresolved questions with reasons
- per-chapter and per-section counts; procedural chapters with their types, solved exercises,
  figures and fast routes (§7e); coverage ratio and generated questions, and whether the user
  was asked about volume (§9); focus areas and score weights (§10); low-confidence ids (§7c);
  cross-check agreement rate and conflicts (§8)
- every count of §15, the average block length, page counts per format, and anything you could
  not test

---

## 17. Working rules

- Do not assume that separate filenames mean separate independent sources.
- Do not use an answer key without checking it against the primary reference.
- **Do not fabricate missing choices, answers, citations, page numbers, methods or data sets.**
- Send brief progress updates as you work.
- Explain technical limitations **before** delivering an inferior substitute, not after.
- **Preserve all attached source files unchanged** (§0d). Write intermediate files only inside the
  working directory; never leave temporary files in the course folder.
- Update `STATE.md` before every stop and at every stage boundary.
- Work only on the supplied content unless external research is explicitly necessary for a
  scientific correction — and label it when you do.
- Report honestly: if something failed, say so; if a step was skipped, say that.
- Ask the user only at the points named in §0c and when genuinely blocked; otherwise decide and
  state the decision.
- When two rules collide, follow the priority order in §0a and note it in the methodology.

---

## 18. Visual style

Keep the focus on the question. Render secondary details — id, question type, repetition count,
importance marker, source list, page reference — in **gray, small, low-contrast text at the
margins**, so the eye lands on the question first and review is fast. Answers use restrained
colour coding: one colour for the correct answer, another for explanations, red reserved for
corrections and conflicting answers, amber only for the low-confidence line. **Bold keywords**
inside the answer block are the only emphasis in the explanation — nothing else competes with
them. The chapter summary box and the Methods block use a light tint and the same bold keyword
style. Figures use the same restrained palette with one highlight colour. Generous whitespace, a
clear separator between questions, and no decoration that competes with the content.

---

## 19. Licence and attribution in the generated files

This prompt is licensed under **Creative Commons BY-NC-SA 4.0**, and **every review file generated
with it is released under the same licence**: attribution, non-commercial, share-alike. The full
text lives in `LICENSE.md` at the root of the repository. The generated files must carry that
forward.

- **Licence notice in every deliverable.** The end-of-file metadata block (§16) contains a fixed
  notice, in the interface language, with this content:

  ```
  Generated with the SVU MBA Course Review Generator, prompt v<spec> · deliverable v<MAJOR.MINOR>
  Source and latest version: https://github.com/AzizMarashly/SVU-MBA-Course-Review
  Licence of the prompt and of this file: CC BY-NC-SA 4.0 — share freely, credit the source,
  never sell. Quoted textbook and exam content stays with its owners and is not covered.
  ```

  The same lines go into the PDF's last page and the DOCX's last section when those are
  produced, and as a comment at the top of `bank.json`.
- **Licence terms in "how to use".** Add three short sentences at the end of the "how to use"
  section (§11), marked as the licence conditions of this file: share it freely with other
  students of the course, at no charge; keep the notice at the end so they can find the source;
  selling it, or putting it behind a paywall or subscription, is not allowed.
- **The licence covers the review's own contribution only.** Do not attach any licence statement
  to the quoted textbook or exam content; say in the notice, and in one sentence in the privacy
  note (§14), that the quoted material stays with its owners and the reader must respect its
  copyright.
- **Do not remove or reword the notice** when re-rendering, and check in §15 that every produced
  file contains it and that the version numbers in it match the filename.

---

## Appendix A — HTML contract

The renderer contract for the HTML deliverable of §13a, placed after the content rules so that
correctness, coverage and exam focus come first. Every rule here is binding; §13a summarises
what the student sees and §15 points to the test list in A.7.

### A.1 Rules shared by every control

The choice is remembered across reloads per device
(e.g. `localStorage`); filters combine as a logical AND; the counter shows `N of M questions`
and the per-chapter and per-section counts update as filters change; a chapter or section left
empty is hidden; a filter or search never leaves a matching question hidden inside a collapsed
parent — open every ancestor of a visible match; a single **Reset filters** control returns
everything to its default; every control is a real `<button>` / `<input>` with an accessible
name, keyboard-operable, and touch targets are at least 44 px high. Implement by tagging every
question element with data attributes (`data-section`, `data-chapter`, `data-importance`,
`data-freq`) and toggling classes on the root — no per-question DOM rebuilding.

### A.2 Toolbar — filters must not eat the screen on a phone

The sticky toolbar has **two parts**: a one-line **bar** always visible, and a **filter panel**
beneath it. The bar holds only the counter, a **Filters** toggle button (`aria-expanded`,
`aria-controls`), the **Essentials** toggle (below) and the search box (which may move into the
panel on very narrow screens). The panel holds everything else: reading mode, chapter filter,
the two sliders, expand / collapse answers, expand / collapse chapters, theme, Reset filters. On
phones the panel starts closed, on wide screens open. When the panel is closed and any filter is
active, the Filters button shows a **badge** with the number of active filters and a short
summary next to the counter (`Exam · ★3+ · Ch. 5`). Opening the panel must not push the content
the reader is looking at off the screen.

### A.3 Filters

- **Reading mode** — a single-select control: `All · Exam · Textbook · Other sources ·
  Generated`. Selecting a mode hides every question that does not belong to it across all
  chapters; a question with two sections appears in both modes; chapter headings and openers
  stay for chapters that still have questions. The mode is reflected in the URL hash so a reader
  can bookmark "textbook only".
- **Importance ≥ N** — range 1 to 5, default 1, current value shown as stars. Generated
  questions are pinned at 1, so the slider at 2 or more removes them (say so in "how to use").
- **Repeated in ≥ N sources** — range 0 to the highest count in the bank, default 0.
- **Chapter filter** and **search** across questions and answers.
- Sliders are native `<input type="range">`, full width on narrow screens; their values join the
  mode in the URL hash so a link can carry "exam questions, importance 4+".

### A.4 Essentials view — a lighter reading path

Theory-heavy pages are long. The **Essentials** toggle in the bar shows less at once without
removing anything: it hides questions below importance 3, and inside the remaining answer
blocks it folds the *Distractors* line, the "also asked as" lines, the full model answer and the
working table behind one "more" control per block; the step `<details>` (A.6) simply stay
closed. A second tap restores the full view. It combines with the other filters and counts as
an active filter for the badge. Per chapter, the summary line shows the essentials count next
to the full count.

### A.5 Collapsing — three levels, plus the page blocks

Chapters, the four sections inside them (§11b) and answers collapse independently with the
same native `<details>`/`<summary>` mechanism. Default on open: chapters open, sections open,
answers closed — the reader sees questions immediately, not a list of headings. The chapter
summary line shows number, title and visible question count, the section summary line its name
and count; the opener (§11a) and the Methods block (§7e) sit inside the chapter directly under
it. The toolbar offers **Collapse all chapters** / **Expand all chapters** independently of the
answer pair, so a reader can keep every chapter open with every answer closed.

Every block that is not a chapter (how to use, scope and sources, methodology, source files,
reference lists, table of contents, file metadata) collapses the same way with the same look, so
a reader who folds everything is left with a short list of headings. The heading is the
`<summary>`; the file-metadata summary line also shows the review version, the spec version and
the licence name, so the §19 notice stays visible when folded. Default: the introductory blocks
open, every block after the last chapter closed. **Collapse all** / **Expand all** fold or open
chapters, sections and these blocks together and leave answers untouched. A link to a folded
block or anything inside it (table of contents, `#src-n` references, a *Step* label's link to
the Methods block, URL hash) opens it before scrolling, and scrolls below the sticky toolbar.

### A.6 Figures and step-by-step reveal (§7e)

- **Figures** are inline SVG generated by the build from the record's structured data, so figure
  and numbers cannot disagree. They scale to a phone width (about 390 px) and stay readable
  without zoom (labels at least 12 px; about twelve nodes or bars per figure as guidance — beyond
  that the figure scrolls horizontally inside the card, like a wide table (§7d), rather than
  shrinking); the highlighted element (path, period, point) is distinguishable by shape or
  weight as well as colour; both themes render it; the text answer stays complete for a reader
  who cannot see the figure, and the figure carries a short text alternative.
- **Step-by-step reveal.** For a multi-step calculation the answer block opens with the
  `✔ Answer` line, the *Fast route*, the given values and the *first* step; steps 2..n are each
  their own collapsed native `<details>`, in order, so a student who solved the problem alone
  can check where their work diverged, and the working table opens with the last step. *Why*,
  *Remember*, *Distractors* and *Ref* stay visible below the steps. A **Show all steps** control
  opens the whole working in one tap; print opens everything. Sibling questions of one table
  share the figure once, repeated under each question like the table.

### A.7 Browser test (§15)

Open the file in a real browser at desktop width and at a phone width (about 390 px) and
actually exercise it: answers start hidden, one click reveals one answer, its control's label
changes state, a second click re-hides it; each reading mode shows only its questions, search
and each filter return correct counts, and the counter matches a manual count for at least one
mode; the importance slider at 5 and the repetition slider at its maximum show exactly the
questions the bank says; the panel starts closed on the phone width and open on desktop; with
the panel closed and a filter active, the badge and summary show; Essentials shows exactly the
questions scored 3 or more, folds what A.4 says and restores on a second tap; chapters,
sections and page blocks open and
collapse per their defaults and independently, and the collapse-all pairs do not touch answer
state; a search hit inside a collapsed chapter opens it; mode, sliders, panel, Essentials and
chapter state survive a reload; Reset filters returns everything to default; a symbol chip opens
the sheet and closes; a figure fits the phone width with its highlight visible; step reveal
opens one step at a time and Show all opens the rest; the reference lists start collapsed; both
themes render; the version number in the filename matches the cover and the metadata. Report
what you tested.
