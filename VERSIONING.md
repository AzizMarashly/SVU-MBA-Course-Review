# Versioning

Two independent version series exist in this repository. They are never compared with each other.

| Series | Form | Where | Example |
|---|---|---|---|
| Generator prompt | `v0.N` | prompt header, `prompt/CHANGELOG.md`, git tag `v0.N` | `v0.11` |
| Course review (deliverable) | `vMAJOR.MINOR` | per course, see below | `v1.6` |

## Course review versions: `vMAJOR.MINOR`

The same scheme applies to every course. Numbers are per course and are **not** synchronised across courses:
IMT v1.6 and PRM v1.3 can exist at the same time. What is aligned is the meaning of each part.

- **MAJOR** is the generation of the question bank.
  - `0`: a draft or early bank, made before a full run under the versioned prompt (for example, MIS v0.1 and v0.2).
  - `1`: the first full generation under the versioned prompt.
  - Increment MAJOR only when the bank is **regenerated** from the sources (a new full run), not when it is
    edited. Reset MINOR to `0`.
- **MINOR** counts every other published release in that generation: a new source (exam sitting, summary), an answer or
  page fix, new or merged records, a re-render for a newer prompt, a style change.
- **Every regenerated deliverable gets a new number** (prompt §0e: never overwrite a file in place). A partial or test
  build that is not published does not consume a number.

## Where the version lives

| Place | Content |
|---|---|
| `courses/S<n>/<CODE>/.review_generation_working_directory/VERSION` | `MAJOR.MINOR` without `v`, for example `1.3` |
| `bank.json` → `file_version` | the same string, read by `scripts/build_course_index.py` into `courses.json` |
| Deliverable file name in the course folder | `<base>_vMAJOR.MINOR.html`; older files move to `archive/` |
| Inside the page | cover, browser title, and end-of-file metadata, next to the prompt (spec) version |
| `VERSIONS.md` in the working directory | one row per version: number, date, formats, what changed, bank checkpoint **and spec version** |

Every course uses `VERSIONS.md` for this history; the name `CHANGELOG.md` inside a course working directory is retired.

## Release checklist (version part)

1. Choose the bump: MINOR for an edit, MAJOR only for a full regeneration.
2. Edit `VERSION`, add the `VERSIONS.md` row, then run the release loop in `CLAUDE.md`.
3. Update the version line in `STATE.md` and in the course `README.md`.

## History of the alignment (2026-09-24)

Before this date PRM used the two-digit form from prompt §0e (`v01`, `v02`, `v03`), while IMT and MIS used `vX.Y`.
The two-digit form was retired. PRM's history maps as follows (old files in `archive/` keep their old names):

| Old | New |
|---|---|
| PRM v01 | v1.0 |
| PRM v02 | v1.1 |
| PRM v03 | v1.2 |
| PRM v04 (F25 source) | v1.3 |

IMT (v1.0 … v1.6) and MIS (v0.1, v0.2, then v1.0 for the regeneration) already followed the scheme and keep their numbers.
Prompt §0e described two-digit numbers until v0.11; since prompt v0.12 (2026-09-24, idea I-9) §0e states this scheme
and the two agree.
