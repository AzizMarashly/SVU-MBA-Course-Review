# courses/ — source material and generation state

This folder holds **everything a generation run needs to be resumed or extended**: the course
material that was fed to the prompt, the settings the prompt was run with, and the working
directory the run left behind (extracted text, question bank, build scripts, notes, handoff).

Nothing in here is published on the web site. The site only serves the finished review pages in
`/S<semester>/<COURSE>/index.html`. This folder exists so that:

- the owner can continue a run later, on another machine, with no memory of the first run;
- someone else can add a new exam sitting or summary and regenerate the review;
- a reader can check exactly which files a review was built from.

## Layout

```
courses/
  README.md                    <- this file
  DISCLAIMER.md                <- unofficial project, origin of the files, copyright and takedown (ar/en)
  S3/                          <- semester
    IMT/                       <- course code, same as the pages folder /S3/IMT/
      README.md                <- course handoff: state, sources, how to resume, how to publish
      PROJECT_SETTINGS.md      <- the filled-in settings table the review was generated with
      .review_generation_working_directory/               <- working directory of the run (see its own README.md)
      المنهاج الٱكاديمي/        <- textbook, book questions, slides
      اسئلة سابقة/              <- past exams
      ملخصات سابقة/             <- summaries
      ملفات متعلقة بالمادة/     <- related files, some excluded (see the ledger)
```

One folder per course, named with the course code, under its semester. The course folder is a
mirror of the local folder the prompt was run in, so it can be copied back to a machine and the
run resumed without any path changes. Two things are deliberately **not** mirrored:

- the finished deliverables (`<title>_vX.Y.html` and `_bank.json`): the HTML is the published page
  in `/S3/<COURSE>/index.html`, and both are reproducible from the working directory;
- `_old_versions/` (or `archive/` in newer runs): git history already keeps every version.

## Resuming a run

1. Clone the repository and open the course folder (e.g. `courses/S3/IMT/`) in Claude Code.
2. Read the course `README.md` first, then the working directory's own `README.md` or `STATE.md`.
   They say which prompt version was used, what stage was reached, and the exact next step.
3. Take the prompt from `prompt/SVU-MBA-Course-Review-Generator.md`, paste the table from the
   course's `PROJECT_SETTINGS.md` over its PROJECT SETTINGS section, and run it. Section 0d of the
   prompt makes the agent look for `.review_generation_working_directory` and resume.
4. After regenerating, copy the new HTML to the pages folder and bump the version. The course
   `README.md` and `CONTRIBUTING.md` at the repository root give the exact commands.

## Adding a course

Copy the local course folder here as `courses/S<n>/<CODE>/` after the run, add a course
`README.md` following the IMT one, drop the archived versions and the duplicate deliverables,
and publish the HTML to `/S<n>/<CODE>/index.html`. Full steps in `CONTRIBUTING.md`.

## Copyright and origin of the material

Read `DISCLAIMER.md` in this folder (Arabic and English). In short: this repository is
unofficial; the course files were found online and mostly come from the student-run shared drive
"SVU Files"; they belong to the university, the authors and the instructors; they are kept here
only so the reviews can be verified and regenerated; and any rights holder can have a file removed
by opening an issue. Do not redistribute them separately, and do not add material you are not
allowed to share.
