# HANDOFF — state as of 2026-09-24

Written for the next agent. Read `CLAUDE.md` first, then this file. Delete this file (or empty it) when section B is
done.

## A. Done on 2026-09-24 (committed and pushed 2026-09-24)

| Course | Release | What |
|---|---|---|
| IMT | v1.6 | F25 exam recall added (8 merged, 12 new, 304 q); prompt v0.11 §7d tables/symbols ported to IMT's renderer; `CHANGELOG.md` renamed `VERSIONS.md` |
| PRM | v1.3 | F25 exam recall added (12 new, 16 merged, 454 q); renumbered from the two-digit scheme (v04 → v1.3) |
| PRM | v1.4 | answer conflict Q04-011/Q07-003 settled (p.177–178, 244) and merged; 10 true duplicates merged or folded; 25 same-fact records folded into "also asked as" lines; 6 shared-table groups on the page; F24 number-less problems credited (I-10); build checks for conflicts / raw ids; 419 q. Log: `qa/consolidation_v1.4.md` |
| MIS | v1.0 | full regeneration under PRM's tooling (chapters 1–10 in scope, 255 q, 105/105 units); 4 cross-chapter duplicates merged; build checks; change report `qa/change_report_v0.2_to_v1.0.md`; v0.2 build kept in `legacy_v0/` |

Repository: `VERSIONING.md` (one `vMAJOR.MINOR` scheme for all courses), `prompt/IDEAS.md` (backlog for the next
prompt, I-1 … I-12), `CLAUDE.md` rule that source files are immutable (no status notes inside them), `.gitignore`
pattern for any MINOR, `courses.json` rebuilt.

Owner decisions of the day (details in the course STATE files and IDEAS.md): problems recalled without numbers
credit the matching table records, for every sitting (I-10); the Asem-type student summaries count toward frequency
(I-12); raw source-item ids are not back-filled in existing banks, only added when a record is touched.

## B. Next: prompt v0.12 from `prompt/IDEAS.md`

The owner wants the ideas moved into the prompt as the next version (after the releases above, so I-11 reflects
what worked). Steps: edit `prompt/SVU-MBA-Course-Review-Generator.md` (bump header to v0.12; §0e rewritten for
`vMAJOR.MINOR` per I-9; §0d immutable sources I-8; §5 duplicate test + consolidation pass I-11 incl. its lessons;
frequency rules I-10, I-12; practical-chapter ideas I-1 … I-7 as the owner chooses), add a `prompt/CHANGELOG.md`
entry, mark adopted entries in IDEAS.md, update course docs that cite changed section numbers. The owner tags
`v0.12`. Ask the owner which of I-1 … I-7 to adopt now — they are larger (renderer work: figures from data, stepwise
reveal, lighter view).

## C. Open, small

- **MIS v1.1: review to apply.** `courses/S3/MIS/.review_generation_working_directory/qa/review_v0.2_vs_v1.0.md`
  (opinion on v0.2 → v1.0; verdict: v1.0 better, but lost topics, book review items folded away, thinner essays).
  Top 5 fixes with ids there and in MIS STATE §5 step 4.
- **PRM v1.5: re-check the 25 folds of v1.4** against the lesson of that review: a book review item or a verbatim
  exam item keeps its own card even when another record tests the same claim. Restore those as cards
  (~80–120k tokens). Also add this exception to I-11 before prompt v0.12.

- PRM: F24 item P1 (FF + lead) still stands as its own low-confidence record Q07-013 built on an illustrative
  example; under I-10 it could become a credit on Q07-001 instead (owner's call).
- MIS: spec shown as v0.11 (tooling) although the run was planned under v0.10.
- IMT: `release.py` does not validate the VERSION format and archives to `../_old_versions/`, unlike PRM/MIS.
- IMT has no duplicate build checks or consolidation pass yet (PRM/MIS have them); port with the next IMT release.
- Not tested anywhere: real phone, print, Safari/Firefox, screen readers.
