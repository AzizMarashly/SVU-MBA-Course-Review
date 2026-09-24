# Ideas for the next prompt version

Backlog of improvements not yet in the prompt. When a new prompt version is written, go through this file, move
what is adopted into the prompt (and `CHANGELOG.md`), and delete or mark those entries here. Keep entries
course-neutral: the concept, why it helps, and the constraint it must respect. Course examples go in brackets only
to show where the idea came from.

## From student feedback, 2026-09-15 (practical chapters)

**What students reported.** The review works well for theory and definitions; students passed on it with the book's
practical chapters. It is weaker where a chapter is procedural (problems solved by a sequence of steps): the page
felt heavy, the worked solutions were harder to follow than the lecturer's method, symbols hid the idea that a small
number would have shown, and some problem types need a drawing to be understood. Solved end-of-chapter exercises
that the book leaves unsolved were valued, and students use the worked answers to check a solution they did
themselves.

### I-1. One method per problem type, stated once, followed everywhere
A procedural chapter has a small number of recurring problem types. For each, state the solving method once, as an
ordered list of steps with the output of each step, near the start of the chapter. Every worked answer of that type
follows the same steps in the same order and names the step it is on. Prefer the order the course teaches (lecture,
book) over a shorter or cleverer order; students compare against what they were taught.
*Constraint:* the steps come from the book or course material, with a page; if the book gives no method, say so.

### I-2. Draw what is spatial, from the data
Some problems are spatial or temporal by nature (networks, dependencies, schedules, allocations over time, charts
read against limits). Render them as a figure generated from the same structured data as the question, not typed
by hand, so the figure and the numbers cannot disagree; the build can then also recompute the results and fail on
a mismatch. Highlight what the question asks about (the decisive path, the overloaded period, the point outside the
limits).
*Constraint:* works on phones (scales to ~390 px, readable without zoom); the text answer stays complete for
readers who cannot see the figure.

### I-3. A concrete number before the symbol
When a concept is a relation between quantities (a dependency type, an offset, a ratio, an index), introduce it
with one tiny numeric example ("A ends on day 5, lag 2, so B ends on day 7") before or instead of the symbolic form.
Symbols stay available in the glossary for those who want them. This applies to the symbol sheet of §7d too: each
entry can carry a one-line numeric example.

### I-4. Solve it yourself, then compare (progressive reveal)
For multi-step problems, let the student open the solution one step at a time (step 1 result, then step 2, ...)
instead of the whole answer at once, so they can check where their own work diverged. The full answer stays one tap
away.

### I-5. Decide by rule when the exam allows it
Where the exam format is multiple choice, many "problems" can be answered by a rule or a comparison without the full
calculation (sign of a variance, which of several indices is lowest, which pattern breaks a control rule). For such
items, lead with the rule-based deduction as the fast exam route and fold the full calculation as optional. Only
state a shortcut that follows from the book's definitions, cite the page, and mark it as derived if the book does
not state it in those words. If no reliable shortcut exists for a type, say so rather than inventing one.

### I-6. Solve the book's unsolved exercises
End-of-chapter exercises without a solution in the book are good exam predictors. Solve all of them, labelled as a
generated solution (not the book's), with the method of I-1 and pages for every rule used.

### I-7. A lighter reading path
Theory-heavy pages are long. Offer a way to see less at once: a filter by importance (§10), a mode that hides
optional lines, or an "essentials only" view per chapter. The full content stays; only the default view changes.

## From repository practice

### I-8. Source files are immutable
State in §0d (working directory) that source files are never edited after they are added (no status notes such as
"not yet in the bank"): the ledger records their hash. Status lives in `STATE.md`. (Already a rule in the repository
`CLAUDE.md` since 2026-09-24.)

### I-9. Deliverable versions as `vMAJOR.MINOR` (§0e)
Replace the two-digit `vNN` of §0e with `vMAJOR.MINOR`: MAJOR = bank generation (0 = draft, bump on a full
regeneration), MINOR = every other published release. Already the repository rule in `VERSIONING.md` since
2026-09-24; bring §0e and the output-base-name row in line with it.

### I-10. Problems recalled without their data still count
Exam recalls of practical problems usually keep the problem type and the questions asked but not the numbers. Count
such a recall as frequency evidence on the existing records of the same problem kind (with a note that the sitting's
data were not recalled), never as topic-only and never by inventing a data set. Apply it the same way to every sitting.
(Owner decision, 2026-09-24.)

### I-11. One claim, one record: a defined duplicate test and a whole-bank consolidation pass
Found in the PRM investigation (2026-09-24): chapter helpers working in isolation produced cross-chapter duplicates,
double-counted exam frequency, and one exam item with two contradictory keys; the prompt says "merge variants of the
same question" without defining "same".
- *Duplicate test:* two records are duplicates when they test the same claim of the book (same concept, same expected
  answer), whatever the source, wording, chapter or form. Same form → one record, sources unioned, other wordings as
  variants. Different form (MCQ / true-false / short answer / reverse definition) → one main record with "also asked as"
  lines, unless the exam itself asked both forms. Records that only share a data table are not duplicates; group them
  under the table instead.
- *Consolidation pass:* after all chapter helpers and before importance scoring, one agent reviews the whole bank
  (not per chapter). Every record carries the raw source-item ids it came from and a one-line statement of the claim it
  tests; a raw item is used by one record (or by several with an explicit sub-question index). Merges union the
  source codes (frequency = size of the union, never a sum), stop on differing answers until the book settles them,
  and are logged with the book page.
- *Build checks:* a hard error for the same option set with a similar stem and a different answer, and for a raw id
  used twice; a warning report listing each record's nearest neighbours across chapters as input to the pass (word
  similarity alone cannot decide: paraphrased and reversed pairs share few words).
- *Existing banks* made before this rule get raw ids only when a record is touched; no back-filling run.
- *Lessons from applying it (PRM v1.4, MIS v1.0, 2026-09-24):* kept record = exam item, then more independent
  sources, then the chapter owning the deciding page, then MCQ/true-false over short answer/essay. Same rule with
  different data and a different answer (two NPV problems) is not a duplicate; generated records covering different
  subsections are never merged; the same question asked twice by one source counts once. A raw item that combines
  several sub-questions may feed several records with a `/label` per sub-question. Compare answers as normalised
  option text, not option position (sources reorder options); exempt sub-questions of one shared table; stem
  similarity ≥ 0.6 without the answer text found the one real conflict and nothing else. Word similarity missed
  about 1 in 6 real pairs and flagged look-alikes that were different claims: a review aid, never a decision.
  Number-less credits (I-10) go only to records of the same problem format (table or calculation records).

### I-12. Student summaries count toward frequency
A source that is a student summary of the book (a cross-check copy of the book's own review set) still counts as a
source in the frequency and importance score: its presence shows what students study and what earlier sittings made
worth summarising. State this explicitly so every run counts the same way. (Owner decision, 2026-09-24.)
