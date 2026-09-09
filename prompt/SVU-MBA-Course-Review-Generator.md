# PROMPT — Complete Course Review Generator (v0.3)

> Reusable spec for building a consolidated, verified, interactive review file from a folder
> of course material. Fill in **PROJECT SETTINGS**, then paste the whole document as your prompt.
> Everything below the settings block is generic and works for any course.

> **Changes in v0.3:** exam questions are presented in multiple-choice form as a direction, not a
> rule — book and other-source questions keep their original format (§3b); an **importance score**
> derived from repetition and the teacher's focus areas orders the questions (§10); low-confidence
> answers are flagged (§7c); the most-repeated list moves to the end, collapsed (§11c); HTML is the
> only mandatory deliverable, PDF/DOCX are offered at the end (§13); the verified bank is saved as a
> checkpoint file before rendering (§13d); the model asks before generating an unusually large
> number of gap-filling questions (§9).
>
> **Carried from v0.2:** fixed, non-repetitive answer template with bold keywords (§7); two-line
> chapter opener (§11a); single-select reading-mode filter in the HTML (§13a).

---

## PROJECT SETTINGS — fill these in

| Setting | Value |
|---|---|
| Review title | `<<< e.g. مراجعه كامله لماده ال MIS >>>` |
| Course / subject | `<<< e.g. نظم المعلومات الإدارية — Management Information Systems >>>` |
| Chapters in scope | `<<< e.g. 1,2,3,5,7,8,9,10 >>>` |
| Primary reference | `<<< exact filename of the textbook >>>` |
| Expected exam format | `<<< e.g. mostly MULTIPLE CHOICE >>>` |
| Question language | `<<< ENGLISH / ARABIC / MIXED >>>` |
| Explanation language | `<<< e.g. ARABIC >>>` |
| HTML filename | `<<< title >>>.html` |
| Bank checkpoint filename | `<<< title >>>_bank.json` |
| PDF / DOCX | `<<< ASK AT END (default) / ALWAYS / NEVER >>>` |

---

You are in a directory that contains all the material for the course above. Read **all** of it
and understand it first, then index it:

1. The primary reference material or textbook.
2. Previous exam files, question banks, screenshots, scanned documents, and any supplementary
   question sources.
3. Any answer keys available with those sources.
4. Summaries, study guides, lecture slides and course notes.

**Do not merely combine the attached files. You must read, classify, deduplicate, verify,
explain, score, format, render, and test the final deliverables.**

You may split the work across helpers (e.g. one per chapter for extraction and verification) if
your environment supports that, but **one agent must own** the source ledger, deduplication,
scoring and the final quality checks, so counts stay consistent across chapters.

---

## 1. Read the reference material first

Read the primary reference completely before touching any question file. Build an internal map of:

- chapter boundaries and section/subsection headings
- definitions, models, frameworks, formulas, tables and worked examples
- printed page numbers vs. PDF page numbers (state whether they match)

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
- Verify suspicions concretely — look for a different instructor's name, a table of contents
  that doesn't match, page citations that point to the wrong content.
- **Exclude out-of-scope sources from the verified bank**, and list every excluded file **by name**
  in the methodology, with the reason.
- Do not discard them blindly: a question from another curriculum may still be usable if its
  concept genuinely exists in the current book — see §9.

---

## 3. Extract all questions from every source

Cover every format present: searchable PDF, scanned PDF, standalone images, screenshots, images
embedded inside Word files, and text held in tables, text boxes, headers and footers.

Cover every question type: multiple choice, true/false, matching, fill-in-the-blank, short
answer, and essay.

**Use OCR where necessary. Visually inspect every scanned page and every image rather than
relying only on text extraction — and state how many images you inspected.** Photographs of
answer sheets contain no extractable text at all; they must be read visually or they will be
silently skipped.

Questions that cannot be confidently assigned to a chapter go to an internal unresolved list,
reported at the end.

### 3b. Exam questions lean towards multiple choice — a direction, not a rule

The real exam is mostly multiple choice, but past-exam files are often **written from memory by
students**: the question appears as a plain sentence or a one-line "what is X?" although it was
asked as a multiple-choice item, and the original options are lost.

- **Exam questions (section 1 of each chapter):** when a question is in free form but was most
  likely a multiple-choice item, present it as one — the recalled wording as the stem, the book's
  answer as the correct option, and distractors that are **real terms from the same chapter**.
  Label it `reconstructed options` in the gray metadata and keep the recalled original text
  beneath it. If the source already has options, keep them exactly as written.
- Because the reconstructed options may differ from what the exam actually shows, the answer
  block for these questions must make **the full idea** clear — the *Why* and *Remember* lines
  should let the reader recognise the right answer among **any** set of options, not only the
  ones shown.
- **Textbook questions and questions from other sources keep their original format.** Do not
  convert them.
- **Generated questions (§9):** prefer multiple choice, but use whatever form tests the idea
  honestly.
- Never convert essay or matching questions, or anything whose answer is a list or a process.
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

- id, chapter, subsection, question type (and `reconstructed` flag where §3b applies),
  canonical wording, notable variants
- verified answer, repetition count, list of independent sources
- reference page(s), confidence (§7c), importance score (§10), any ambiguity worth flagging

**The repetition count must equal the number of independent sources containing the question, not
the number of uploaded files.** A question is counted once per independent source even if it
repeats inside that source. One file may contain several distinct exams — each exam counts as a
separate occurrence only if it is genuinely an independent sitting.

---

## 6. Edit conservatively

Fix OCR damage, broken spacing and obvious typographic corruption. Never invent facts, options,
or wording. If an option is missing from the source, say so — do not complete it. The only
permitted rewriting is the option reconstruction in §3b, and it must be labelled.

---

## 7. Verify every answer, then explain it briefly

For each question, verify the answer against the primary reference, then write the answer block
using the fixed template below. **Never cite a page you have not verified.**

### 7a. Answer block template — fixed order, nothing else

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
```

### 7b. Writing rules for the answer block

- **Say each thing once.** The answer line states the answer; the *Why* line does not repeat it;
  the *Distractors* line does not restate the *Why*. If a line would only repeat another line,
  drop it.
- **Why** is at most two sentences and names the single concept that decides the question. Do not
  summarise the whole topic. Do not open with "The correct answer is…" — the answer line already
  did that. For reconstructed exam questions (§3b) it may run to three sentences so the idea
  survives a different set of options.
- **Remember** holds the words a reader needs to recognise the right option in the exam: the
  defining term, the number, the name of the model, the contrast that separates it from its
  nearest distractor. Keywords are always **bold**.
- **Distractors** covers only the options a student is likely to confuse with the answer. Skip
  options that are obviously wrong. One clause each, e.g. *"B — that is **TPS**, not MIS"*.
- **Bold is for keywords only.** Bold the term, number or name that unlocks the answer — in the
  *Why* line and the *Remember* line. Never bold whole sentences, never bold more than a few words
  per line. Do not use bold anywhere in the question stem or options.
- No filler phrases ("as we know", "it is important to note", "in other words"). Do not repeat
  the question stem inside the explanation.
- Target length for the whole block, excluding the optional lines: **40–80 words**. Go longer only
  when a scientific correction, a conflict, or a reconstructed question genuinely requires it.

### 7c. Flag low-confidence answers only

Most answers need no confidence remark. Add the `⚠ Low confidence` line **only** when one of
these is true:

- the book supports the answer with a single passing sentence rather than a definition or section;
- the sources disagree and the book does not settle it clearly;
- the question wording is ambiguous, or was recalled from memory and could mean two things;
- the answer relies on a scientific correction rather than the book.

State the reason in one clause. Do not add the line to confident answers, and do not add a
"high confidence" label anywhere — silence means confident. Report the count of flagged
questions in the completion summary.

---

## 8. Use summaries and answer keys as independent cross-checks

Study summaries often reproduce the book's end-of-chapter questions *with worked answers*. Such a
file is a genuine independent source — register it in the ledger and add it to the source list of
every question it confirms.

Cross-check its key against your verified answers item by item and **report the agreement rate**
(e.g. "64 of 65 matched"). Where it disagrees with the book, the book wins, but **display both
answers at the question** — yours as the answer, the contrary one on the `Other source:` line
(§7a), for comparison only.

---

## 9. Audit concept coverage, then fill the gaps

Collecting and deduplicating questions is not enough — the sources together may leave whole ideas
in the book untested.

1. Split every in-scope chapter into its **subsections, using the book's own table of contents**.
   Report the total count.
2. For each subsection, check whether any question's **text, options or answer** actually covers
   it. A mere mention inside an explanation does **not** count as coverage — report those
   separately as "mentioned but never asked". Record the subsection on every question — the
   importance score (§10) needs it.
3. Report three numbers: directly asked / only in explanations / not covered at all.
4. For every uncovered subsection, **write a new question yourself**, from the book's own wording,
   with a page number you have verified. Prefer multiple choice with same-chapter distractors.
5. **Before writing them, check the volume.** If the generated questions would exceed the number
   of real questions in a chapter, or exceed roughly a third of the whole bank, **stop and ask
   the user** whether to generate all of them, only the most important subsections, or none.
   Show the per-chapter numbers when asking. There is no fixed cap — the user decides.
6. Put these in a **separate, clearly labelled fourth section** so they never blend into the real
   exam questions. Give them a repetition count of zero and a source label meaning "generated".
   State in the document that they exist to close gaps and are **not** predictions of the exam.
7. **Do not repeat an idea.** Verify mechanically that no generated question duplicates an
   existing one, and that no two generated questions cover the same idea. Report the check.
8. Re-run the audit after adding them and report the final coverage as `N of N`.
9. A chapter that needs no generated questions gets none — say so.

Some chapters may be fully covered already; that is a valid and useful result.

---

## 10. Score importance, then order by it

Repetition alone misses something: the exam papers and the book's own questions together show
**which areas the teacher keeps returning to**. Two questions with the same repetition count are
not equally important if one sits in a subsection with ten other questions and the other stands
alone.

### 10a. Focus areas

For every subsection in scope, count the distinct questions that test it, split by origin (exam /
textbook / other). Rank subsections by exam-question count first, then total. The top of that
ranking is the **focus areas** list. Each chapter's opener (§11a) names its top focus areas; the
methodology holds the full table.

### 10b. Importance score

Give every question an **importance score from 1 to 5**, computed transparently and described in
the methodology. Suggested weights — adjust if the material calls for it, but state what you used:

| Signal | Effect |
|---|---|
| Repeated in N independent exam sources | strongest signal; scales with N |
| Also appears as a textbook end-of-chapter question | +1 |
| Its subsection is a focus area (§10a) | +1 |
| Only appears in summaries / other sources | neutral |
| Generated to fill a gap (§9) | fixed at 1 — never higher |

Render the score as a small gray marker next to the repetition count (e.g. `★★★★☆` or `4/5`),
in the same low-contrast style as the other metadata. **The score is a study aid, not a
prediction** — say so once in the "how to use" section.

### 10c. Ordering

Within every section of every chapter, order questions by **importance score, then repetition
count, then question type** (multiple choice before others). Show `Frequency: N independent
sources` with each question as before.

---

## 11. Document structure

Cover → how to use → scope and source summary → chapters → methodology → most repeated and most
important (collapsed) → table of contents → file metadata.

**Keep the start of the file simple. Put all metadata, the reference lists and the table of
contents at the end.** There is no separate answer-key section — every answer lives with its
question.

### 11a. Chapter opener — two-line context summary

Every chapter starts with a short **"In this chapter"** box, before the first question:

- **Two lines, no more.** Line 1: what the chapter is about, in one sentence. Line 2: the 3–6
  terms, models or numbers the questions below keep returning to, in **bold**, comma-separated —
  drawn from the chapter's focus areas (§10a).
- Written in the explanation language, from the book's own wording, and consistent with the
  questions that follow — it is orientation, not a summary of the whole chapter.
- Visually distinct from questions (a light box), and never collapsed: the reader must see it
  before the first question.

### 11b. Four sections inside each chapter

Inside each chapter, order the questions in **four sections**:

1. **Exam questions** (from past papers — presented in exam-like form, §3b)
2. **Textbook questions** (the book's own end-of-chapter set, original format)
3. **Questions from other sources** (summaries, study guides, older-curriculum collections whose
   concept exists in the current book and whose answer was re-verified from it — original format)
4. **Generated questions** (§9), with a short note explaining what they are

Within each section, order by §10c.

**Make the type or types of each question explicit** — one question can be both an exam question
and a textbook question. Sections 3 and 4 each carry a one-paragraph explanation of their origin.

Per question, show: number and id, repetition count, importance marker, section and type tags,
question text, options, then the answer block (§7a).

### 11c. Reference lists at the end, collapsed

After the methodology, add two lists, each inside its own collapsed `<details>` block, **with no
answers exposed**:

- **Most repeated questions** — threshold chosen to keep the list useful (if most questions sit at
  2 sources, list 3+), at most about 30 items, each linking to the question.
- **Highest importance questions** — score 4 and 5, same format.

They are reference material for the last day before the exam, not the way into the document, so
they stay closed until the reader opens them.

---

## 12. Bilingual formatting

Right-to-left text right-aligned, left-to-right text left-aligned, with correct paragraph
direction on every paragraph — not just visual alignment. No reversed or misplaced punctuation.
Use separate paragraph styles per direction, embed fonts, and never leave a heading orphaned from
the content it introduces.

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
- JavaScript may add optional extras only: search across questions and answers, chapter filter,
  the reading-mode filter below, expand-all / collapse-all, a visible counter, and a light/dark
  toggle. All must degrade cleanly.
- Provide print styles that reveal every answer when printed.
- Respect the reader's light/dark preference and offer a manual override.

#### Reading-mode filter — one question section at a time

The reader must be able to read the whole document **one section type at a time** — for example
all textbook questions across every chapter first, then all exam questions — instead of chapter
by chapter.

- A sticky toolbar at the top holds a **single-select** control (segmented buttons or radio-style
  chips): `All · Exam · Textbook · Other sources · Generated`. Optionally a second axis:
  `All · Importance 4+ · Repeated 2+`.
- Selecting a mode hides every question that does not belong to it, **across all chapters**, and
  hides any chapter that ends up with no visible questions. Chapter headings and the two-line
  chapter summary stay visible for chapters that still have questions.
- A question tagged with two sections (e.g. exam + textbook) appears in both modes.
- The visible counter updates to `N of M questions` for the current mode. The chapter filter and
  the search combine with the mode (logical AND).
- The current mode is remembered across reloads (e.g. `localStorage`) and reflected in the URL
  hash, so a reader can bookmark "textbook only". With scripting disabled the page must still show
  everything.
- Implement by tagging every question element with data attributes (e.g. `data-section`,
  `data-chapter`, `data-importance`, `data-freq`) and toggling a class on the root — no
  per-question DOM rebuilding.
- Printing ignores the mode by default and prints everything; say so near the print
  instructions.

### 13b. PDF — plain reading and printing copy (on request)

A flat, non-interactive PDF: each answer simply printed beneath its question.

**Do not attempt an interactive show/hide PDF.** PDF reveal mechanisms rely on AcroForm `/Hide`
actions and a document `/OpenAction`; only Adobe Acrobat honours them. Chrome, Edge, Firefox,
Preview and every phone viewer ignore them and display all answers permanently, which is worse
than not trying. Interactivity belongs in the HTML file.

The PDF must contain no form fields, no `/AcroForm`, no `/OpenAction`, no JavaScript, no widget
annotations, and no wording referring to any reveal mechanism. Include bookmarks for chapters and
sections. Strip all document metadata except the title.

### 13c. DOCX — editable copy (on request)

Fully editable, with each answer under a collapsible Word heading so the reader can collapse them.
Every question independent of every other.

**State this limitation in the document:** Microsoft Word does not persist collapsed state inside
a `.docx` — it is a per-session view state, so the file always opens expanded. Tell the reader how
to collapse all headings in one action, and note that collapsing is a desktop-Word feature that may
behave differently in Word for the web, Google Docs or LibreOffice, where answers simply appear
expanded.

### 13d. Bank checkpoint — save before rendering

Before producing any output file, save the complete verified bank to the checkpoint filename
from the settings: every canonical question with its fields from §5, the source ledger, the
subsection coverage table and the focus-area ranking. Plain JSON (or Markdown tables if JSON is
impractical), no personal data.

This is the single source of truth for every rendered file. If a later fix is needed, edit the
bank and re-render rather than patching the HTML by hand. Mention the checkpoint file in the
completion summary.

### 13e. Ask before producing PDF and DOCX

When the HTML is finished and tested, **ask the user** whether they also want the PDF and/or the
DOCX, unless the settings table says ALWAYS or NEVER. Produce only what they choose, from the
same bank, and run the format-specific checks in §15 for whatever you produce.

---

## 14. Privacy note

State plainly, in the document, that hiding answers is a study aid and not security: the answer
text exists inside the file and is reachable through search, copy, accessibility tools, page source
or file-structure inspection. It must not be relied on for a real exam.

**Prevent any personal data from your device or account being written into any file** — no author,
creator, company, or last-modified-by fields.

---

## 15. Quality assurance — test, don't assume

**Content:** unique ids; every question has an answer, an explanation, a verified page, a
subsection and an importance score; every question inside the declared chapter scope; frequency
equals the number of distinct sources (generated questions excepted); generated questions never
score above 1; no leftover markup artifacts (e.g. literal `**`) in any rendered output.

**Answer blocks (§7):** every block follows the template order; no block exceeds the word target
without an optional line or a reconstruction justifying it; every *Remember* line contains at
least one bold keyword; no bold inside stems or options; no *Why* line repeats the answer text;
low-confidence lines appear only with a stated reason. Run these as mechanical checks and report
counts, then read a random sample of 20 blocks by eye.

**Reconstructed exam questions (§3b):** each carries the label and the recalled original text;
no distractor is a made-up term; the *Why* line would still identify the answer with different
options.

**Chapter summaries (§11a):** every in-scope chapter has one, it is exactly two lines, and it sits
before the first question.

**Ordering (§10c):** within every section, importance never increases going down the list; ties
are broken by repetition. Verify mechanically.

**HTML:** open it in a real browser and actually exercise it — confirm answers start hidden, that
clicking reveals only that question, that the control's label changes state, that clicking again
re-hides, that search and filter return correct counts, that each reading mode shows only its
questions and the counter matches a manual count for at least one mode, that the mode survives a
reload, that the end-of-file reference lists start collapsed, and that both themes render. Report
what you tested.

**PDF (if produced):** verify structurally that no form fields, actions or scripts remain; render
pages and inspect them visually; confirm the answers are present and the layout is correct.

**DOCX (if produced):** parse it, confirm the heading structure, render and visually inspect pages.

If a check cannot be run in your environment, say so explicitly rather than implying it passed.
When an automated check reports a failure, **inspect each hit before reporting it** — keyword
audits produce false positives from legitimate content.

---

## 16. Deliverables

The HTML file, the bank checkpoint, any requested PDF/DOCX, plus a completion summary reporting:

- files supplied, duplicates detected, independent sources counted
- images found and images visually inspected
- raw question occurrences, unique questions after deduplication
- exam questions reconstructed into multiple choice (§3b)
- out-of-scope and unresolved questions, with reasons
- per-chapter counts and per-section counts
- book subsections audited and final coverage ratio; generated questions added, and whether the
  user was asked about volume (§9)
- focus areas per chapter and the importance-score weights used (§10)
- low-confidence questions flagged, with ids (§7c)
- cross-check agreement rate against any summary answer key, and every conflict found
- answer-block check results (§15) and average block length
- page counts per produced format, and anything you could not test

---

## 17. Working rules

- Do not assume that separate filenames mean separate independent sources.
- Do not use an answer key without checking it against the primary reference.
- **Do not fabricate missing choices, answers, citations, or page numbers.**
- Send brief progress updates as you work.
- Explain technical limitations **before** delivering an inferior substitute, not after.
- **Preserve all attached source files unchanged.**
- Work only on the supplied content unless external research is explicitly necessary for a
  scientific correction — and label it when you do.
- Report honestly: if something failed, say so; if a step was skipped, say that.
- Ask the user only at the two points named above (§9 volume, §13e formats) and when genuinely
  blocked; otherwise decide and state the decision.

---

## 18. Visual style

Keep the focus on the question. Render secondary details — id, question type, repetition count,
importance marker, source list, page reference — in **gray, small, low-contrast text at the
margins**, so the eye lands on the question first and review is fast. Answers use restrained
colour coding: one colour for the correct answer, another for explanations, red reserved for
corrections and conflicting answers, amber only for the low-confidence line. **Bold keywords**
inside the answer block are the only emphasis in the explanation — nothing else competes with
them. The chapter summary box uses a light tint and the same bold keyword style. Generous
whitespace, a clear separator between questions, and no decoration that competes with the content.
