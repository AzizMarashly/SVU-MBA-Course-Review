# CLAUDE.md — agent guide for this repository

Read this first. It is the map; the files it points to hold the detail. Do not re-derive any of it
by exploring.

**If `HANDOFF.md` exists at the repository root, read it next: it describes work left in progress
and how to resume it.**

## What this is

Student-made, AI-generated exam review pages for the SVU MBA programme (Syrian Virtual
University), published on GitHub Pages from the repository root:
https://azizmarashly.github.io/SVU-MBA-Course-Review/ . Unofficial. Interface and content are
mostly Arabic (RTL); file and folder names under `courses/` are Arabic too.

Two tiers, never mix them up:

| Tier | Path | Served? | Purpose |
|---|---|---|---|
| Published pages | `S<n>/<CODE>/index.html`, `index.html`, `courses.json` | yes | What students open |
| Sources + generation state | `courses/S<n>/<CODE>/` | no | Course material, settings, and the working directory of the run, so a review can be resumed or regenerated |

Courses today (semester 3): `IMT` (v1.6), `PRM` (v1.4), `MIS` (v1.0, regenerated 2026-09-24 with PRM's tooling;
the v0.2 build is kept in `legacy_v0/`).

## Where to look

| Need | File |
|---|---|
| Human overview, contribution rules, git etiquette | `README.md`, `CONTRIBUTING.md` |
| The generator prompt (v0.11) and its history | `prompt/SVU-MBA-Course-Review-Generator.md`, `prompt/CHANGELOG.md`; every version is a git tag `v0.N` |
| Version scheme (prompt `v0.N` vs course `vMAJOR.MINOR`, when to bump what) | `VERSIONING.md` |
| Ideas waiting for the next prompt version (student feedback, practice) | `prompt/IDEAS.md` — read it when writing a new prompt version |
| State of a course run: stage checklist, decisions, known problems, exact next step | `courses/S3/<CODE>/.review_generation_working_directory/STATE.md` — **always read before touching a course** |
| Folder map and release workflow of a course | `courses/S3/<CODE>/README.md` (IMT also has a working-directory `README.md`) |
| Settings the review was generated with | `courses/S3/<CODE>/PROJECT_SETTINGS.md` |
| Source ledger (what was used, excluded, why) | IMT: `…/notes/ledger.md`; PRM: `…/ledger.json` + `…/render/SOURCES.md` |
| Copyright, takedown, origin of material (ar/en) | `courses/DISCLAIMER.md` |
| Licence | `LICENSE.md` (CC BY-NC-SA 4.0, covers prompt and generated pages) |

## Course layouts differ (IMT was first, PRM is the newer model)

| | IMT | PRM |
|---|---|---|
| Question data + build scripts | `.review_generation_working_directory/bank/` | `.review_generation_working_directory/render/` |
| Per-chapter data | `bank_chNN.py` (+ `bank_extra.py`) | `bank_chNN.py`, record model in `common.py` |
| Course-specific tables (names, source files appendix) | inside `render_html.py` (`FILES`, `SRC_ROW`) | isolated in `meta_prm.py` |
| Version scheme (same for all, see `VERSIONING.md`) | `vX.Y` (`VERSION` = `1.6`), `VERSIONS.md` | `vX.Y` (`VERSION` = `1.4`), `VERSIONS.md` |
| Book text | OCR in `ocr/` | PyMuPDF in `extracted/book/` with lam-alef ligature fix |

MIS (since v1.0) uses PRM's layout: `render/` with `bank_chNN.py`, `common.py`, `meta_mis.py`; the v0.2
build (`bank_a.py` … `bank_e.py`, DOCX/PDF scripts) is kept intact in `legacy_v0/` and is not used.

**For a new course, copy PRM's `render/` tooling and its `CHAPTER_HELPER_BRIEF.md` /
`extracted/FORMAT.md`, not IMT's.** PRM's `meta_prm.py` pattern keeps course specifics out of the
renderer. Tables and calculations (prompt §7d, since v0.11): records carry `table=T(...)`,
`ans_table=T(...)` and `calc=C(given, steps=[S(what, eq, sub, res)])` from `common.py`; the
renderer draws them and adds a symbol chip row with a tap-to-open bottom sheet from the structured
`SYMBOLS` glossary (ar / en / f / note per symbol) in the meta file; the build refuses a
stem containing `|`. Rules and a worked example for helpers: `render/CALC_TABLE_BRIEF.md` (PRM and
MIS). IMT's renderer does not have this yet. The PRM run used one owner session plus helper subagents (transcription per source
group, then one per chapter writing `bank_chNN.py` from the brief); that worked well.

## The release loop (same for every course with a working directory)

```
cd courses/S3/<CODE>/.review_generation_working_directory/<bank|render>
set PYTHONUTF8=1                      # required: Arabic text, Windows console
python release.py                     # must print "uncovered: 0"; bumps nothing itself
python qa_blocks.py                   # must pass
cd <repo root>
python scripts/publish_page.py S3/<CODE>      # out.html -> S3/<CODE>/index.html + analytics snippet
python scripts/build_course_index.py          # regenerates courses.json (exit 1 = changed, normal)
```

Before `release.py`: edit the chapter file, bump `VERSION` (`MAJOR.MINOR` per `VERSIONING.md`), add a `VERSIONS.md` row. After
publishing: update `STATE.md` and the course `README.md` version line.

Facts that bite:

- **`S3/<CODE>/index.html` is `out.html` plus the Cloudflare Web Analytics snippet** (one line
  appended at the end, copied from the home page `index.html`). The release scripts do not add it.
  Never copy `out.html` over the page by hand; use `scripts/publish_page.py`. Diffs between the two
  files that are only that line are expected.
- `courses.json` is generated. Never edit it by hand; a GitHub Action also rebuilds it on push.
- Home page course cards are read from `courses.json` at runtime; static fallback cards in
  `index.html` exist only for the no-JS case.
- Versioned deliverables (`*_vX.Y.html`, `*_bank.json`) inside `courses/` are gitignored; the page
  under `S3/` and `out.html` are the tracked copies. `archive/` and `_old_versions/` are ignored too
  (git history has every version). Page renders `*.png` under `courses/` are ignored.
- Bank files are UTF-8 without BOM; `bank.json` is read with `utf-8-sig`.
- Windows: use `set PYTHONUTF8=1` (cmd) or `$env:PYTHONUTF8=1` (PowerShell) for every Python run.

## Rules that are not negotiable

- Every answer change needs a book page. Never lower a low-confidence flag without book evidence.
- No personal data anywhere (names on answer sheets, phone numbers, Telegram handles), including
  file names.
- IMT: one summary file was removed by the owner during the first run and must never be re-added,
  used, or named.
- MIS: the exam collections from the older curriculum (Dr Suleiman Awad's course: Solver, pivot
  tables, Hong framework) are not in the book; only items whose concept exists in the book were
  kept, re-verified from the book. Do not import their answer keys.
- Do not redistribute course material separately; it is here only to verify and regenerate reviews.
- Source files are immutable once added: never write status or workflow notes into them ("not yet in the bank",
  "waiting for a run", "done"). Their MD5 is recorded in the ledger, so a later edit to remove the note breaks
  the hash. A header describing the file's origin (date, who recalled it, how merged) is fine, written once when
  the file is created. Run status belongs in `STATE.md` §5, the course `README.md` open items, and `HANDOFF.md`.
- Keep the licence/attribution notice and the analytics snippet in every published page.
- Git: several people and AI sessions push to `main`. `git pull --rebase` before committing and
  again before pushing. Focused commits (one course, one fix). Never force-push. Commit only when
  asked.

## Prompt changes

Bump the version in the prompt header, add a `prompt/CHANGELOG.md` entry, tag `v0.N`. Keep rules
generic; course specifics belong in PROJECT SETTINGS. Section numbers (§0d working directory,
§7c low confidence, §7d tables and calculations, §10 importance, §11d source-files appendix, §19 licence) are referenced
throughout the course docs; do not renumber casually.
