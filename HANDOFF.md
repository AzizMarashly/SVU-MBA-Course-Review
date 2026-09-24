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
