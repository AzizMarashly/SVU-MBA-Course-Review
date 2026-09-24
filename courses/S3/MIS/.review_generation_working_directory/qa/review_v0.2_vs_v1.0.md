# Review: MIS v0.2 → v1.0 (opinion, 2026-09-24)

Independent read-only review made after the v1.0 release (one Opus agent, ~65 side-by-side comparisons against the
book text). Kept here for the next MIS pass; **nothing below has been applied yet**. The follow-ups are listed in
`STATE.md` §5.

## Verdict

v1.0 is clearly better for students than v0.2: the «لماذا» block averages 24 words instead of 65, every card has a
«تذكّر» line and a line per wrong option, page citations are right where v0.2 was usually 1–2 pages off, the book's
printed key is used, and no older-curriculum item leaked in. The page is 27% heavier (793 KB vs 624 KB) but has
fewer cards (255 vs 269), so the reading load per card fell.

It lost three things: depth in the 24 book essays (≈144 → ≈97 words), about 12 book review items as cards of their
own (merged into another form), and a few topics that v0.2 asked through generated questions while the coverage
audit still counts their sections as covered.

## Top 5 to fix, in priority order

1. **Topics no longer asked** (small): section 10-3-6 (the six BI analytic functions p.402 incl. drill-down,
   predictive analytics pp.403–405, location analytics p.406), Select / Project / Join (p.195), the six
   organisational factors (p.105). Reinstate G10-06, G10-07, G10-08, G5-01 (and G3-03, see 5). Change coverage
   counting so a section counts as covered only when its own content is asked (today 10-3-6 counts through Q10-021,
   a Big Data T/F defined on p.205, and Q10-030, an older-curriculum GIS item).
2. **Book review items back as their own cards** (medium): exams reuse book review items word for word, so folding
   them loses practice. T/F C2-24, C3-23, C3-24, C3-27, C7-04, C9-13, C9-19; MCQ C3-11, C9-02, O10-04 (Data Mart);
   C1-08 (the F24 «بعد» trap). Undo the two debatable consolidation merges: Q09-011 back to chapter 9 (the book asks
   definition → term there) and Q03-020 back to chapter 3 (different cue, «الافتراضات الأساسية حول المنتجات…»).
3. **Two citations** (small): Q01-016 must cite p.336 (chapter 9, in scope, word for word «مرتبط بأصولها غير
   الملموسة») and say "intangible" in the explanation; Q03-024 cites p.122 (the reference list), use p.106.
4. **Recall-shaped MCQs and flags** (small): give Q03-003 («مفلطحة» is ambiguous), Q01-031 (raw «1و2و3», 5 options)
   and Q05-001 (3 options) four clean options, keeping the recall in `original`. Remove low-confidence flags where the
   book settles the answer: Q03-004 (verbatim p.29), Q03-017, Q03-018 (book marks it), Q08-019, Q10-008 (the
   confusable option is not among the choices), Q02-027. Keep the justified ones (Q05-020, Q05-021, Q08-008, Q03-005,
   Q10-030).
5. **Essay depth** (medium): an expandable "full model answer" for the 24 book essays, rebuilt from v0.2's text and
   re-checked against the book (Q08-021…023, Q10-022…024, Q09-019…021 first). Reinstate G3-03 (six factors) as an
   essay.

Also noted: importance vs focus-area inconsistencies (Q10-004 importance 4 but not a focus unit; Q02-012 in two
sittings but not a focus unit).

## Lesson beyond MIS

Point 2 applies to the duplicate rule (prompt idea I-11) and to PRM v1.4, which folded 25 same-fact records into
"also asked as" lines: **a book review item or a verbatim exam item keeps its own card**, even when another record
tests the same claim. PRM's folds should be re-checked against this.

---

## Detailed comparison tables (from the review)

# MIS v0.2 → v1.0: records compared side by side (scratch, read-only review 2026-09-24)

Full dump of every v1.0 record next to the legacy record(s) it came from: `pairs.txt` (same folder); the 23 dropped legacy records: `dropped.txt`.
Page checks were run on `extracted/book/ch_fixed/*.txt` with `find.py` (same folder).

Verdict key: B = v1.0 better, W = v1.0 worse, = = the same or just different.

| new ← old | ch | what changed | verdict | note |
|---|---|---|---|---|
| Q01-001 ← C1-01 | 1 | option order shuffled, why 45→18 words + remember + distractor | B | shorter; the mnemonic helps |
| Q01-002 ← C1-22+C7-13 | 1 | short answer → reconstructed MCQ; ch-7 book MCQ merged in | = | the book's own MCQ wording is now only in a folded variant |
| Q01-004 ← C1-05 | 1 | R44 item "تعريف إدارة تكنولوجيا المعلومات" now attached here | B | explains why C1-14 was dropped correctly |
| Q01-005 ← C1-13 | 1 | short → MCQ; R44 wording conflict recorded | B | good distractors |
| Q01-006 ← C1-07+C1-08 | 1 | F24 «بعد» trap MCQ folded into a variant | W | the trap question itself is no longer a card (Q01-032 keeps the «قبل» version) |
| Q01-008 ← C1-12 | 1 | short → MCQ | = | |
| Q01-009 ← C1-16+C3-06 (+Q03-020) | 1 | merge; the ch-3 book MCQ «الافتراضات الأساسية حول المنتجات…» is only a variant now | W | a different cue (products: what/how/where/for whom); unmerge or add as a card |
| Q01-012 ← C1-18 | 1 | short → MCQ | = | |
| Q01-013 ← C1-21+C9-06 (+Q09-011) | 1 | merge; the book's ch-9 MCQ direction (definition → term) is lost | W | the kept direction (term → definition) is the less likely exam form |
| Q01-014 ← C1-20 | 1 | pages 36 → 36–37 | B | |
| Q01-016 ← C1-24 | 1 | p. 336 → 11, 35, 39; note calls p. 336 "chapter 11" | **W (error)** | p. 336 is chapter 9 and states it verbatim («مرتبط بأصولها غير الملموسة»); new why no longer says "intangible" |
| Q01-021..023 ← C1-29..31 | 1 | pages now cite the ch-2 text pages | B | |
| Q01-031 ← O1-01 | 1 | clean 4-option MCQ → raw OQ 5-option «1و2و3» + low-confidence flag | W | ambiguous and unnormalised spelling; v0.2 version was cleaner |
| Q01-035 ← G1-01 | 1 | why 71→24 | = | |
| Q02-002 ← C2-02 | 2 | p. 53 → 55, 85 | B | p. 55 carries the TPS card ("Saving") |
| Q02-003 ← C2-07+C2-24 | 2 | book T/F merged into exam MCQ | W | book T/F item no longer practised as T/F |
| Q02-006 ← C2-10 | 2 | p. 57 → 58, 65 | B | KWS card on p. 58 ("Design specs") |
| Q02-007 ← C2-11 | 2 | p. 58 → 60 | B | «الملخصات والمقارنات» is on p. 60 |
| Q02-008 ← C2-12 | 2 | p. 59 → 60, 65 | B | "Simple models" on p. 60 |
| Q02-010 ← C2-14 | 2 | p. 53 → 55, 66 | B | "Order processing" on p. 55 |
| Q02-013 ← C2-17 | 2 | R44 key "ESS" recorded as other_source, MIS kept | = | right answer, book p. 60 "Annual budgeting" |
| Q02-015 ← C2-03 | 2 | p. 58 → 60, 65, 85 | B | "Middle managers" p. 60 |
| Q02-023 ← C2-23 | 2 | OQ variants attached | = | |
| Q02-027..029 ← C7-17..19 | 2 | moved from ch 7 to unit 2-6 | B | correct home |
| Q02-035 ← O2-03 | 2 | 2-item → 3-item ordering MCQ | B | |
| Q03-001 / Q03-016 ← C3-01 | 3 | split into exam definition + book examples | B | |
| Q03-003 ← C3-17 | 3 | clean distractors → student's recalled «مسطحة / أفقية / مفلطحة» (3 options, near-synonyms) + low-confidence | W | «مفلطحة» also means flattened: the item is now ambiguous |
| Q03-004 ← C1-15 | 3 | short → MCQ, moved to ch 3; low-confidence | = | flag is about location, not the answer (p. 29 verbatim) — over-cautious |
| Q03-005 ← C1-17 | 3 | short → MCQ, low-confidence | = | flag justified (no book definition) |
| Q03-006 ← C3-07 | 3 | why 55→34 | = | |
| Q03-008 ← C3-04 | 3 | R44 «التخصيص» naming recorded | B | |
| Q03-010 ← C3-10+C3-11+C3-27 | 3 | three items (essay, F24 MCQ, book T/F) → one short answer | W | the F24 MCQ «استلام المواد… ثم تحويل المدخلات» is gone as a card |
| Q03-017 ← C3-02+C3-23 | 3 | book T/F merged, low-confidence | W | flag over-cautious (book tick + p. 27); T/F lost |
| Q03-018 ← C3-03+C3-24 | 3 | book T/F merged, low-confidence | W | same |
| Q03-019 ← C3-05 | 3 | p. 105 → 124, 338 | B | p. 105 does not mention core competencies; p. 338 does |
| Q03-024 ← C3-28 | 3 | p. 106 → 112, 122 | = | p. 122 is the reference list (Porter 1980); p. 106 was more useful to a student |
| Q05-001 ← C5-03 | 5 | 4 options → recalled 3 (بت / بايت / ملف) | W (small) | weaker practice |
| Q05-006 ← C5-08 | 5 | why 72→26 | = | lost the examples (رقم الطالب / رمز الطالب) |
| Q05-010 ← C5-24 | 5 | short → MCQ with good distractors (warehouse, in-memory, app server) | B | |
| Q05-020 ← C5-19 | 5 | book tick «خطأ» now recorded; answer «صح» kept with low-confidence | B | honest; right call |
| Q05-021 ← C5-20 | 5 | 115-word caveat → 25 words + low-confidence | B | |
| Q05-024 ← C5-23+C10-19+O10-04 | 5 | three records → one T/F | W | O10-04 (definition → «منفذ البيانات») was the only card with Data Mart as the answer |
| Q05-025..027 ← C5-25..27 | 5 | p. 216 (review page) → text pages | B | but the model answer is shorter |
| Q07-001 ← C7-03+C7-04 | 7 | book T/F merged | W | |
| Q07-006 ← C7-08 | 7 | two definitions → one MCQ (Customization), low-confidence | = | Personalization now only a distractor |
| Q07-012 ← C7-14 | 7 | p. 81 → 31, 269 | B | p. 269 has the global-standards text |
| Q07-014 ← C7-10 | 7 | p. 268 → 270 | B | |
| Q07-018..020 ← C7-22..24 | 7 | p. 289 → text pages; essay answer text longer, why shorter | = | |
| Q08-001 ← C8-04+C8-05 | 8 | F24 definition folded into the book MCQ | = | |
| Q08-003 ← C8-02 | 8 | why drops the Nike tier note; distractor line explains Downstream | = | |
| Q08-008 (new, F24) | 8 | «تعريف الأنشطة التشغيلية» guessed as operational CRM | risk | low-confidence is right; the guess could be wrong (p. 28 reading) |
| Q08-015 ← C8-19 | 8 | same «أقل من 5%» figure as the book | = | book p. 321 prints 5% (dropped G8-04 said 50%) |
| Q08-021..023 ← C8-21..23 | 8 | p. 328 → text pages; model answer 130–183 → ~70 words | W for essays | |
| Q09-008 ← C9-01+C9-02+C9-13 | 9 | three book items → one MCQ | W | two book forms lost as cards |
| Q09-014 ← C9-09+C9-19+O9-02 | 9 | book T/F «قواعد البيانات وجداول البيانات…» merged | W | |
| Q09-004/005 ← C9-10 | 9 | split: definition + If-Then-Else | B | |
| Q09-019..021 ← C9-21..23 | 9 | p. 369 → text pages; answers shorter | B pages / W depth | |
| Q09-022 ← O9-01 | 9 | options now raw OQ | = | |
| Q10-001..003 ← C10-10..12 | 10 | short → MCQ with the same option set (structured / unstructured / semi) | B | exactly the discrimination the exam tests |
| Q10-003 | 10 | R44 recalled «غير المهيكلة», record answers «شبه المهيكلة» (R44 key agrees) | = | correct, documented |
| Q10-008 ← C10-05 | 10 | low-confidence added | = | over-cautious: «تحصيل البيانات» is not among the options |
| Q10-022..024 ← C10-21..23 | 10 | p. 418 → text pages | B pages / W depth | Q10-024 why talks about BI users (p. 407), answer is by management level |
| Q10-021 | 10 | only real record for unit 10-3-6 besides Q10-030 | risk | see the coverage note below |

## Concepts that v0.2 asked and v1.0 no longer asks anywhere as a question

| concept | book | v0.2 record | v1.0 trace |
|---|---|---|---|
| six BI analytic functions (production / parameterized reports, dashboards, ad hoc query, **drill-down**, forecasts & scenarios) | p. 402 | G10-06 | none (0 hits for «التنقل لأسفل» / Drill) |
| predictive analytics | pp. 403–405 | G10-07 | none (0 hits for «التنبؤية») |
| location analytics | p. 406 | G10-08 | only Q10-030 (GIS, OQ, low-confidence) |
| Select / Project / Join | p. 195 | G5-01 | none (0 hits) |
| six organisational factors to weigh when planning a new IS | p. 105 | G3-03 | Q03-005 names the structure factor only |
| in-memory computing (RAM, not disk) | p. 209 | G5-05 | distractor text in Q05-010 only |
| Data Mart as the answer | pp. 206–207 | O10-04 | variant text in Q05-024 only |
| Downstream as the answer | p. 303 | O8-02 | distractor of Q08-003, essay Q08-022 |

Unit 10-3-6 counts as "covered by real questions" in coverage.md because of Q10-021 (Big Data T/F, definition on p. 205) and Q10-030 (OQ GIS short answer); neither tests the section's own content.

## Book review items that are no longer cards of their own (merged into another form)

C2-24 (T/F), C3-06 → Q03-020 (MCQ), C3-11 (F24 MCQ), C3-23 (T/F), C3-24 (T/F), C3-27 (T/F), C7-04 (T/F), C9-02 (MCQ), C9-06 → Q09-011 (MCQ), C9-13 (T/F), C9-19 (T/F), O10-04 (MCQ).
The wording survives only in folded «صيغ أخرى» variants; a student practising the book's review set as T/F will not meet them.

## Size

| | v0.2 | v1.0 |
|---|---|---|
| out.html | 624 KB | 793 KB (+27 %) |
| cards | 269 | 255 |
| collapsibles | 270 | 379 |
| visible words (whole page) | 41.7 k | 45.8 k |
| why, mean / max words | 65 / 241 | 24 / 39 (+ remember + distractors = 41 / 64) |
| essay model answer (ans + why), mean words | ~144 | ~97 |
