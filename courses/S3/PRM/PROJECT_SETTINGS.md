# PROJECT SETTINGS used for the PRM review

This is the settings block filled in at the top of the generator prompt
(`prompt/SVU-MBA-Course-Review-Generator.md`, v0.9) when this review was produced. To resume or
extend the run, paste this table over the PROJECT SETTINGS section of the current prompt and open
this folder in Claude Code; §0d of the prompt makes the agent resume from
`.review_generation_working_directory/STATE.md`.

| Setting | Value |
| --- | --- |
| Review title | `مراجعه كامله لماده ال PRM` |
| Course / subject | `إدارة المشاريع — PROJECT MANAGEMENT` |
| Chapters in scope | `1,2,3,4,5,6,7,8,9,10,11,12,13,14` (the whole book; the 14 slide decks cover the same 14 chapters) |
| Primary reference | `MBA - Project Management - The Book.pdf` (الماده الاكاديميه/, 554 pages, د. إياد زوكار; printed page = PDF page) |
| Expected exam format | `mostly MULTIPLE CHOICE` — student reports (about.txt) say roughly 10 calculation items (critical path, EVA) and the rest theory |
| Question language | `ARABIC` |
| Explanation language | `ARABIC` |
| Interface language | `ARABIC` |
| Interaction mode | `DECIDE` — the owner asked for an unattended run; every default applied is listed in `STATE.md` and the completion summary |
| Pilot chapter | `NONE` |
| Output base name | `مراجعه كامله لماده ال PRM` — files are named `<base>_vNN.html` (§0e) |
| Working directory | `.review_generation_working_directory` (inside this folder, §0d layout) |
| PDF / DOCX | `ASK AT END` — in DECIDE mode this means HTML only unless asked later |
| Spec version | `v0.9` |

Notes on the folder before the run: six byte-identical or converted duplicate files were removed
on 2026-09-09 before extraction (three copies of the lecture summary `ملخص ادارة مشاريع.pdf`, three
copies of `PM-112هام.docx` plus its PDF conversion, and a re-saved copy of
`2016 pm اسئلة دورات.docx`). `about.txt` holds two students' experience notes and is not a
question source.
