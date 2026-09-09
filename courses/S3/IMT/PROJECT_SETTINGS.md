# PROJECT SETTINGS used for the IMT review

This is the settings block that was filled in at the top of the generator prompt when this
review was produced. To resume or extend the run, take the current prompt from
`prompt/SVU-MBA-Course-Review-Generator.md` at the repository root and paste this table over
its PROJECT SETTINGS section. Settings added by later prompt versions (output base name,
working directory) are listed at the bottom with the values this run effectively used.

| Setting | Value |
| --- | --- |
| Review title | `مراجعه كامله لماده ال IMT` |
| Course / subject | `التسويق والتجارة الدولية — INTERNATIONAL MARKETING AND TRADING` |
| Chapters in scope | `1,2,3,4,5,6,7,9,10,11,12` |
| Primary reference | `MBA-International Marketing and Trading-The Book.pdf` |
| Expected exam format | `MULTIPLE CHOICE` |
| Question language | `ARABIC` |
| Explanation language | `ARABIC` |
| Interface language | `ARABIC` |
| Interaction mode | `ASK` |
| Pilot chapter | `NONE` |
| PDF / DOCX | `ASK AT END` (never answered; none produced) |
| Spec version | `v0.9` — the bank was built with v0.4 and re-rendered with v0.9 (see the working directory `STATE.md`) |

Values for settings that exist in the current prompt but not in v0.4:

| Setting | Value |
| --- | --- |
| Output base name | `مراجعه كامله لماده ال IMT` — files are named `<base>_v<X.Y>.html` and `<base>_v<X.Y>_bank.json` (current: v1.3) |
| Working directory | `.review_generation_working_directory` (inside this folder). Its layout predates prompt v0.5: read its `README.md`, it plays the role of `STATE.md`. |
