# SVU MBA Course Review

Course review pages for the SVU MBA program, hosted on GitHub Pages.

## Layout

| Path | Contents |
|---|---|
| `S<n>/<CODE>/index.html` | The published review pages (GitHub Pages serves the repository root). |
| `index.html` | The home page listing the courses. |
| `prompt/` | The generator prompt, versioned, with its changelog. |
| `courses/S<n>/<CODE>/` | Source material, the filled-in prompt, and the working directory of each run, so a review can be resumed or extended. See `courses/README.md`. Not served on the site. |
| `CONTRIBUTING.md` | How to report mistakes, fix questions, add sources or courses. |

## Adding a course

1. Run the prompt locally on the course material (see below).
2. Copy the course folder to `courses/S<n>/<CODE>/` and write its `README.md` (model: `courses/S3/IMT/README.md`).
3. Put the review page at `S<n>/<CODE>/index.html`.
4. Add a card for it in the root `index.html`.
5. Commit and push; GitHub Pages redeploys automatically.

Details in `CONTRIBUTING.md`.

## The prompt that generates the pages

`prompt/SVU-MBA-Course-Review-Generator.md` is the reusable prompt used to build every review
page here. It reads a folder of course material (textbook, past exams, summaries), verifies
every answer against the book, scores questions by repetition and the teacher's focus areas,
and renders a self-contained interactive HTML review.

**How to use:** put all the course material in one folder, fill in the PROJECT SETTINGS table at
the top of the prompt, then paste the whole file as the prompt to Claude Code opened in that
folder. See the prompt itself for the full process; `prompt/CHANGELOG.md` lists what changed in
each version, and every version is a git tag (`v0.1`, `v0.2`, ...).

## Contributing

Mistakes are expected: the reviews are AI-generated. `CONTRIBUTING.md` explains how to report
or fix one, add a new exam sitting, or add a course. Pull before you push; several people and
sessions work on this repository at once.

## Licence

The prompt is licensed under [CC BY-NC-SA 4.0](LICENSE.md): credit the source, do not sell it,
share improvements under the same licence. `LICENSE.md` also carries a community pledge for the
generated review pages: share them freely with fellow students, keep the attribution notice, and
respect the copyright of the course material they quote.

