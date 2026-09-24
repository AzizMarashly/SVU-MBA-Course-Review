# Cross-chapter consolidation pass — MIS v1.0 (2026-09-24)

Rule: prompt idea I-11 (`prompt/IDEAS_ADOPTED_v0.12.md`; prompt §5a–§5b since v0.12). Two records are duplicates when they test the same claim of the book
(same concept, same expected answer). Only **same-form** duplicates were merged (owner decision for v1.0); pairs that
test the same fact in another form (MCQ vs true/false, reverse definition, essay) stay separate and are listed below.

## Method

1. Full eight-chapter build before consolidation: 258 records from the chapter helpers (259 with Q01-035, the reinstated G1-01, added before the merges).
2. Candidate list (scripts adapted from the PRM investigation): tf-idf cosine on stem + answer, on the full record
   (stem, answer, why, remember) and on the bold terms of why/remember; union rule stem ≥ 0.40 or full ≥ 0.40 or
   bold ≥ 0.45, plus the top-3 cross-chapter neighbours of every record, plus every pair sharing a book page (within a
   unit or across chapters). 826 candidate pairs; the 310 with a shared page or a score ≥ 0.30 were read pair by pair,
   and the whole bank (one line per record: id, form, unit, pages, sources, stem, answer) was read once end to end to
   catch reversed and paraphrased pairs that share few words.
3. Each candidate judged by reading both records and, for the merged ones, the book page.

## Merged (class a: same claim, same answer, same form) — 4 pairs, 259 → 255 records

| kept | dropped | claim | book page | why this record is kept |
|---|---|---|---|---|
| Q01-002 (R44, reconstructed MCQ) | Q07-013 (BOOK/ASM, ch-7 review MCQ 2) | business model = how a firm produces and sells a product or service to create wealth | p. 20 (ch-7 review item on p. 288, pages 20, 278 kept) | exam item; p. 20 is in chapter 1. The exam recall is «تعريف نموذج العمل», so the direction of the reconstructed MCQ is not an exam form; both are definition MCQs. |
| Q05-024 (BOOK/ASM, ch-5 review T/F) | Q10-020 (BOOK/ASM/OQ1/OQ5, ch-10 review T/F) | the data warehouse is not the small store; the data mart is the small subset for one group | pp. 206–207 | neither is an exam item; pp. 206–207 are in chapter 5. Q10-020's OQ1/OQ5 variants move with it. |
| Q01-013 (R44, reconstructed MCQ) | Q09-011 (BOOK/ASM, ch-9 review MCQ) | organizational and management capital = the complementary investments in processes, culture and behaviour needed to get value from IS investments | p. 35 (also p. 341) | exam item; p. 35 is in chapter 1. The R44 recall quotes the ch-9 review wording almost verbatim. |
| Q01-009 (F24, reconstructed MCQ) | Q03-020 (BOOK/ASM, ch-3 review MCQ) | organizational culture = the basic assumptions (values, ways of doing things) accepted by most members | p. 29 (ch-3 review item on p. 124) | exam item; the definition is on p. 29 in chapter 1 (chapter 3 has no own text for it). |

How the merge is applied: `render/build_bank.py` → `MERGES` (keep ← drop). Sources, pages, legacy ids and raw ids are
unioned; the dropped wording and answer become a variant «SRC (كان Qxx-yyy): …»; `reconstructed`, `original`,
`low_conf`, `book_says`, `other_source` and `notes` are kept from both (none of the four dropped records carried one);
`freq` = number of sources in the union. Results: Q01-002 R44/BOOK/ASM, Q05-024 BOOK/ASM/OQ1/OQ5, Q01-013 R44/BOOK/ASM,
Q01-009 F24/BOOK/ASM. Units left by the dropped records stay covered (7-2-2, 10-3-3, 9-1-2, 3-2-2).

## Answer conflicts

None. The four merged pairs have the same answer. No other pair with the same claim and a different answer was
found. One near-conflict is already documented: Q10-008 (S25 recall: «وظيفته الحصول على البيانات – تنظيفها –
تنظيمها وربطها – كتالوج البيانات» → data warehouse, p. 392) and Q10-010 (BOOK: the same steps named as the BI activity
«تحصيل البيانات», p. 401) — different option sets and different questions; Q10-008 keeps its low-confidence flag,
which names p. 401.

## Same fact, other form — left as they are

| records | forms | fact | page |
|---|---|---|---|
| Q01-023 / Q02-023 | T/F «صح» / T/F «خطأ» (negated statement) | DSS serve unique, rapidly changing, non-routine decisions | p. 60 |
| Q01-021 / Q02-015 | T/F / MCQ | MIS (and DSS) serve middle management | pp. 58, 60 |
| Q02-009 / Q02-022 | MCQ (F24) / T/F (BOOK) | MIS give middle managers reports on current performance | p. 58 |
| Q05-011 / Q05-017 | MCQ / T/F (both in the ch-5 review set) | a characteristic of an entity is an attribute | p. 186 |
| Q05-012 / Q05-018 | MCQ / T/F (both in the ch-5 review set) | in the traditional file environment a data change requires changing every program | p. 189 |
| Q08-001 / Q08-010 | MCQ / T/F | enterprise software lets data be used across functions and processes | pp. 298–299 |
| Q10-008 / Q10-013 | MCQ «which system» / MCQ «which is not a function» | the four functions of the data warehouse | p. 392 |
| Q02-003 / Q02-044 | MCQ / T/F (OQ3) | ESS show summarised graphical information (digital dashboard) | pp. 63–64 |
| Q10-021 / Q05-033 | T/F / generated short answer | big data: huge volume, high velocity, wide variety | p. 205 |
| Q02-046 / Q08-001 | generated MCQ / MCQ | enterprise systems integrate the functions in one software system (ch. 2 wording: one data repository; ch. 8: integrated modules) | pp. 78, 298–299 |
| Q02-013 / Q02-035 | MCQ / ordering MCQ (OQ) | budgeting is a management-level (MIS) application | pp. 66, 73 |
| Q01-024 / Q02-037 / Q02-040 | MCQ / MCQ «all of these» / T/F | e-business covers all digital business activities; e-commerce is part of it | pp. 40, 81 |
| book essays vs single items | essay / MCQ, T/F | the 24 book essays (Q01-028…030, Q02-030…032, Q03-026…028, Q05-025…027, Q07-018…020, Q08-021…023, Q09-019…021, Q10-022…024) contain facts that single items also test | — |

Pairs flagged by the word scores and judged **not** the same claim: Q01-015 / Q07-008, Q01-027 / Q10-013,
Q02-004 / Q10-016, Q02-016 / Q10-001, Q02-024 / Q08-001, Q02-041 / Q10-029, Q05-024 / Q10-007, Q01-012 / Q09-010
(information value chain vs knowledge-management value chain), Q10-001 / Q10-002 (unstructured vs structured decision
definitions; allow-listed in the build check).

## Build checks added (`render/build_bank.py` → `check_duplicates`)

- Hard: same normalised option set, stem cosine ≥ 0.6, different correct answer → build fails. One hit on the full
  bank, Q10-001 / Q10-002, read and allow-listed (`DUP_ALLOW`).
- Hard: one raw source-item id used by two records (`raw=[...]` field in `common.Q`, sub-question form `id@n`).
  Tested with a synthetic duplicate (fails) and with `@1`/`@2` (passes). No MIS record declares raw ids yet: 233 real
  records lack the field (the chapter helpers recorded source items in `variants` / `original` text only).
- Warning: each record's top-3 cross-chapter neighbours above the union threshold (21 records on the final bank),
  all read in this pass.
