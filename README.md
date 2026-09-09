# SVU MBA Course Review

Course review pages for the SVU MBA program, hosted on GitHub Pages.

## Adding a course

1. Create a folder under the semester folder, named after the course code (e.g. `S3/IMT/`).
2. Put the review page in it as `index.html`.
3. Add a link to it in the root `index.html`.
4. Commit and push; GitHub Pages redeploys automatically.

## The prompt that generates the pages

`prompt/SVU-MBA-Course-Review-Generator.md` is the reusable prompt used to build every review
page here. It reads a folder of course material (textbook, past exams, summaries), verifies
every answer against the book, scores questions by repetition and the teacher's focus areas,
and renders a self-contained interactive HTML review.

**How to use:** put all the course material in one folder, fill in the PROJECT SETTINGS table at
the top of the prompt, then paste the whole file as the prompt to Claude Code opened in that
folder. See the prompt itself for the full process; `prompt/CHANGELOG.md` lists what changed in
each version, and every version is a git tag (`v0.1`, `v0.2`, ...).

## Licence

The prompt is licensed under [CC BY-NC-SA 4.0](LICENSE.md): credit the source, do not sell it,
share improvements under the same licence. `LICENSE.md` also carries a community pledge for the
generated review pages: share them freely with fellow students, keep the attribution notice, and
respect the copyright of the course material they quote.

