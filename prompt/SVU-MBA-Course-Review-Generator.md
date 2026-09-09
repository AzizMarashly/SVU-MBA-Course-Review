# PROMPT — Complete Course Review Generator

> Reusable spec for building a consolidated, verified, interactive review file from a folder
> of course material. Fill in **PROJECT SETTINGS**, then paste the whole document as your prompt.
> Everything below the settings block is generic and works for any course.

---

## PROJECT SETTINGS — fill these in

| Setting | Value |
|---|---|
| Review title | `<<< e.g. مراجعه كامله لماده ال MIS >>>` |
| Course / subject | `<<< e.g. نظم المعلومات الإدارية — Management Information Systems >>>` |
| Chapters in scope | `<<< e.g. 1,2,3,5,7,8,9,10 >>>` |
| Primary reference | `<<< exact filename of the textbook >>>` |
| Question language | `<<< ENGLISH / ARABIC / MIXED >>>` |
| Explanation language | `<<< e.g. ARABIC >>>` |
| HTML filename | `<<< title >>>.html` |
| PDF filename | `<<< title >>>.pdf` |
| DOCX filename | `<<< title >>>.docx` |

---

You are in a directory that contains all the material for the course above. Read **all** of it
and understand it first, then index it:

1. The primary reference material or textbook.
2. Previous exam files, question banks, screenshots, scanned documents, and any supplementary
   question sources.
3. Any answer keys available with those sources.
4. Summaries, study guides, lecture slides and course notes.

**Do not merely combine the attached files. You must read, classify, deduplicate, verify,
explain, format, render, and test the final deliverables.**

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

- id, chapter, question type, canonical wording, notable variants
- verified answer, repetition count, list of independent sources
- reference page(s), and any ambiguity worth flagging

**The repetition count must equal the number of independent sources containing the question, not
the number of uploaded files.** A question is counted once per independent source even if it
repeats inside that source. One file may contain several distinct exams — each exam counts as a
separate occurrence only if it is genuinely an independent sitting.

---

## 6. Edit conservatively

Fix OCR damage, broken spacing and obvious typographic corruption. Never invent facts, options,
or wording. If an option is missing from the source, say so — do not complete it.

---

## 7. Verify every answer against the primary reference

For each question provide: the answer, an explanation in the explanation language, why the
correct option is correct, why the plausible distractors are wrong, the corrected version where
the source was wrong, the chapter, the PDF page and the printed page.

**Never cite a page you have not verified.**

---

## 8. Use summaries and answer keys as independent cross-checks

Study summaries often reproduce the book's end-of-chapter questions *with worked answers*. Such a
file is a genuine independent source — register it in the ledger and add it to the source list of
every question it confirms.

Cross-check its key against your verified answers item by item and **report the agreement rate**
(e.g. "64 of 65 matched"). Where it disagrees with the book, the book wins, but **display both
answers at the question** — yours as the answer, the contrary one clearly labelled as coming from
another source, for comparison only.

---

## 9. Audit concept coverage, then fill the gaps

Collecting and deduplicating questions is not enough — the sources together may leave whole ideas
in the book untested.

1. Split every in-scope chapter into its **subsections, using the book's own table of contents**.
   Report the total count.
2. For each subsection, check whether any question's **text, options or answer** actually covers
   it. A mere mention inside an explanation does **not** count as coverage — report those
   separately as "mentioned but never asked".
3. Report three numbers: directly asked / only in explanations / not covered at all.
4. For every uncovered subsection, **write a new question yourself**, from the book's own wording,
   with a page number you have verified.
5. Put these in a **separate, clearly labelled fourth section** so they never blend into the real
   exam questions. Give them a repetition count of zero and a source label meaning "generated".
   State in the document that they exist to close gaps and are **not** predictions of the exam.
6. **Do not repeat an idea.** Verify mechanically that no generated question duplicates an
   existing one, and that no two generated questions cover the same idea. Report the check.
7. Re-run the audit after adding them and report the final coverage as `N of N`.
8. A chapter that needs no generated questions gets none — say so.

Some chapters may be fully covered already; that is a valid and useful result.

---

## 10. Prioritise repeated questions

Order questions so the most frequently repeated appear first within their section. Show
`Frequency: N independent sources` with each question. Add a summary list of the most repeated
questions near the start **with no answers exposed** — use a threshold that keeps the list useful
(if most questions sit at 2 sources, list 3+).

---

## 11. Document structure

Cover → how to use → scope and source summary → most repeated → chapters → methodology →
table of contents → file metadata.

**Keep the start of the file simple. Put all metadata and the table of contents at the end.**
There is no separate answer-key section — every answer lives with its question.

Inside each chapter, order the questions in **four sections**:

1. **Exam questions** (from past papers)
2. **Textbook questions** (the book's own end-of-chapter set)
3. **Questions from other sources** (summaries, study guides, older-curriculum collections whose
   concept exists in the current book and whose answer was re-verified from it)
4. **Generated questions** (§9), with a short note explaining what they are

**Make the type or types of each question explicit** — one question can be both an exam question
and a textbook question. Sections 3 and 4 each carry a one-paragraph explanation of their origin.

Per question, show: number and id, repetition count, question text, options, then the answer,
explanation and reference.

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

Produce **three** files. Each has one job.

### 13a. HTML — the primary interactive file

A single self-contained `.html` file. Each answer is hidden behind a native
`<details>`/`<summary>` control, collapsed by default.

- **No JavaScript is required for the reveal** — it must work with scripting disabled.
- It must work in any browser on phone, tablet and desktop, offline, opened directly from disk.
- No external assets, no CDN, no fonts to download — everything inline.
- JavaScript may add optional extras only: search across questions and answers, chapter filter,
  expand-all / collapse-all, a visible counter, and a light/dark toggle. All must degrade cleanly.
- Provide print styles that reveal every answer when printed.
- Respect the reader's light/dark preference and offer a manual override.

### 13b. PDF — plain reading and printing copy

A flat, non-interactive PDF: each answer simply printed beneath its question.

**Do not attempt an interactive show/hide PDF.** PDF reveal mechanisms rely on AcroForm `/Hide`
actions and a document `/OpenAction`; only Adobe Acrobat honours them. Chrome, Edge, Firefox,
Preview and every phone viewer ignore them and display all answers permanently, which is worse
than not trying. Interactivity belongs in the HTML file.

The PDF must contain no form fields, no `/AcroForm`, no `/OpenAction`, no JavaScript, no widget
annotations, and no wording referring to any reveal mechanism. Include bookmarks for chapters and
sections. Strip all document metadata except the title.

### 13c. DOCX — editable copy

Fully editable, with each answer under a collapsible Word heading so the reader can collapse them.
Every question independent of every other.

**State this limitation in the document:** Microsoft Word does not persist collapsed state inside
a `.docx` — it is a per-session view state, so the file always opens expanded. Tell the reader how
to collapse all headings in one action, and note that collapsing is a desktop-Word feature that may
behave differently in Word for the web, Google Docs or LibreOffice, where answers simply appear
expanded.

---

## 14. Privacy note

State plainly, in the document, that hiding answers is a study aid and not security: the answer
text exists inside the file and is reachable through search, copy, accessibility tools, page source
or file-structure inspection. It must not be relied on for a real exam.

**Prevent any personal data from your device or account being written into any file** — no author,
creator, company, or last-modified-by fields.

---

## 15. Quality assurance — test, don't assume

**Content:** unique ids; every question has an answer, an explanation and a verified page; every
question inside the declared chapter scope; frequency equals the number of distinct sources
(generated questions excepted); no leftover markup artifacts (e.g. literal `**`) in any rendered
output.

**HTML:** open it in a real browser and actually exercise it — confirm answers start hidden, that
clicking reveals only that question, that the control's label changes state, that clicking again
re-hides, that search and filter return correct counts, and that both themes render. Report what
you tested.

**PDF:** verify structurally that no form fields, actions or scripts remain; render pages and
inspect them visually; confirm the answers are present and the layout is correct.

**DOCX:** parse it, confirm the heading structure, render and visually inspect pages.

If a check cannot be run in your environment, say so explicitly rather than implying it passed.
When an automated check reports a failure, **inspect each hit before reporting it** — keyword
audits produce false positives from legitimate content.

---

## 16. Deliverables

The three files, plus a completion summary reporting:

- files supplied, duplicates detected, independent sources counted
- images found and images visually inspected
- raw question occurrences, unique questions after deduplication
- out-of-scope and unresolved questions, with reasons
- per-chapter counts and per-section counts
- book subsections audited and final coverage ratio; generated questions added
- cross-check agreement rate against any summary answer key, and every conflict found
- page counts per format, and anything you could not test

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

---

## 18. Visual style

Keep the focus on the question. Render secondary details — id, question type, repetition count,
source list, page reference — in **gray, small, low-contrast text at the margins**, so the eye
lands on the question first and review is fast. Answers use restrained colour coding: one colour
for the correct answer, another for explanations, red reserved for corrections and conflicting
answers. Generous whitespace, a clear separator between questions, and no decoration that competes
with the content.
