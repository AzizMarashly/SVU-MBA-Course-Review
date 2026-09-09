# Contributing

Thanks for helping. Everything here is built and maintained by students, for students, and the
reviews are AI-generated, so they contain mistakes. Every fix helps the next person.

There are four ways to contribute, from easiest to most involved.

## 1. Report a mistake

Open an issue: https://github.com/AzizMarashly/SVU-MBA-Course-Review/issues/new

Include: the course, the chapter, the question text (or its position), what is wrong, and the
book page that shows the right answer if you have it. That is enough; someone with the tools
will fix and republish.

## 2. Fix a question yourself

Every review is rendered from a question bank kept in `courses/S<n>/<CODE>/`. The course
`README.md` there says where the data lives and how to rebuild. For IMT, for example:

1. Fork and clone the repository.
2. Edit the chapter file, e.g. `courses/S3/IMT/.review_generation_working_directory/bank/bank_ch05.py`. Keep the record
   structure; the build asserts on it.
3. Bump `VERSION`, add a changelog line, and run the release script (see the course README).
   The build must print `uncovered: 0` and the QA script must pass.
4. Copy the new `out.html` over `S3/<CODE>/index.html`. The home page reads version and counts
   from `courses.json`; run `python scripts/build_course_index.py` to refresh it, or let the
   GitHub Action do it after the push.
   Every published page carries the Cloudflare Web Analytics snippet (the `<script>` from
   `static.cloudflareinsights.com` at the end of the file); keep it when you overwrite the page
   or copy it from the home page `index.html`.
5. Open a pull request. Say what you changed and cite the book page.

If you cannot run Python, you can still open a pull request that edits only the chapter file and
say so; a maintainer will rebuild.

## 3. Add a new source (a new exam sitting, a summary, an answer key)

1. Put the file in the right subfolder of the course, e.g. `courses/S3/IMT/اسئلة سابقة/`.
2. Open that course folder in Claude Code and paste the generator prompt from
   `prompt/SVU-MBA-Course-Review-Generator.md`. Tell it which file is new. The prompt is written
   to resume from the working directory rather than start over.
3. Check the agent updated the source ledger and the source index in the working directory.
4. Release, publish, and open a pull request as in section 2.

Before adding a file: remove personal data (names on answer sheets, phone numbers, Telegram
handles). Do not add material you are not allowed to share.

## 4. Add a whole course

1. Put all the course material in one local folder, fill in the PROJECT SETTINGS table at the
   top of the prompt, and run it in Claude Code from that folder. Expect several hours of agent
   time for a full textbook.
2. When the review is finished, copy the folder to `courses/S<n>/<CODE>/`, without the archived
   versions and the duplicate deliverables, and write a course `README.md` modelled on
   `courses/S3/IMT/README.md`. Save the filled-in PROJECT SETTINGS table as `PROJECT_SETTINGS.md`.
3. Copy the review to `S<n>/<CODE>/index.html` and append the Cloudflare Web Analytics snippet
   found at the end of the home page `index.html`.
4. Nothing to edit on the home page: `courses.json` is rebuilt from the course's `bank.json`
   (run `python scripts/build_course_index.py`, or let the GitHub Action do it). A course
   without a bank in `courses/` needs a hand-written `S<n>/<CODE>/course.json` instead; see
   `S3/MIS/course.json`.
5. Open a pull request.

## Improving the prompt

The prompt in `prompt/` is versioned; every version is a git tag. Propose changes in a pull
request that also adds a `CHANGELOG.md` entry and bumps the version in the prompt header. Keep
changes generic: anything course-specific belongs in PROJECT SETTINGS, not in the rules.

## Rules for everything

- **Cite the book.** A change to an answer needs a page number. "I remember it differently" is
  an issue, not a pull request.
- **Never lower the low-confidence flag** on a question without book evidence.
- **No personal data** anywhere in the repository, including file names and screenshots.
- **Copyright.** Course material is here so reviews can be verified and regenerated. Do not
  redistribute it separately. If you hold rights to something here and want it removed, open an
  issue and it will be taken down. Full notice, in Arabic and English: `courses/DISCLAIMER.md`.
- **Licence.** The prompt and the generated review pages are CC BY-NC-SA 4.0. By contributing
  you agree your changes are under the same licence. For the review pages this means: share them
  free, keep the attribution notice, never sell them (`LICENSE.md`).

## Git workflow

Several people, and several AI sessions, edit this repository at the same time. To avoid
clobbering someone else's work:

```
git pull --rebase          # always, right before you commit
git add <your files>
git commit -m "..."
git pull --rebase          # again, in case something landed meanwhile
git push
```

Keep commits focused (one course, one fix) so they are easy to review and revert. Never force-push
to `main`.
