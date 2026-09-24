# PROJECT SETTINGS — MIS review

Settings of the **v1.0 regeneration** (2026-09-13 … 2026-09-24), in the prompt's PROJECT SETTINGS form. The first
bank (v0.1, 2026-09-06, republished as v0.2) was generated before the versioned prompt from an ad hoc 15-section brief;
its settings differed only in the interaction mode (ASK), the spec (pre-v0.1) and the DOCX/PDF outputs.

| Setting | Value |
|---|---|
| Review title | `مراجعه كامله لماده ال MIS` |
| Course / subject | `نظم المعلومات الإدارية — Management Information Systems` |
| Chapters in scope | `1,2,3,5,7,8,9,10` (4, 6, 11, 12 excluded by the owner) |
| Primary reference | `Dr Iyad Zoukar - MBA - MIS - The Book.pdf` (507 pages; printed page = PDF page; end-of-chapter answers marked inline: tick for true/false, yellow highlight for MCQ) |
| Expected exam format | mostly MULTIPLE CHOICE, with true/false |
| Question language | `MIXED` (Arabic with English terms) |
| Explanation language | `ARABIC` |
| Interface language | `ARABIC` |
| Interaction mode | `DECIDE` (no stops for the owner; defaults recorded in `STATE.md` §3) |
| Pilot chapter | `NONE` |
| Output base name | `مراجعه كامله لماده ال MIS` → `…_v1.0.html`; older files move to `.review_generation_working_directory/archive/` |
| Version scheme | `vMAJOR.MINOR` per `VERSIONING.md` (MAJOR 1 = first full generation under the versioned prompt) |
| Working directory | `.review_generation_working_directory` (§0d layout; the v0.2 build in `legacy_v0/`) |
| PDF / DOCX | `NEVER` (HTML only) |
| Spec version | run under `v0.10`; tooling and page at `v0.11` (§7d; no MIS record has a table or calculation) |
| Sources | 10 independent: BOOK, S25, R44 («حل دورات» is R44's key, one source), F24, ASM (cross-check only, never a type), OQ1–OQ5 (older curriculum: in-book concepts only, keys never imported) |
| Duplicate rule | prompt idea I-11: one record per claim; true duplicates across chapters merged in one consolidation pass (`qa/consolidation_v1.0.md`), checked by the build |

## Owner instructions that are not in the prompt

- Show the book's own answer when a question comes from the book, even when it was corrected;
  keep the corrected wrong answer visible for reference (rendered as the red "different answer in
  another source" line).
- Order inside each chapter: exam questions, then book questions, then questions from other
  files, then generated questions; a question can carry several types.
- Keep the start of the file simple; metadata and the table of contents at the end; no personal
  data from the device or account.
- Meta information (repetition, type) in grey, so the question text stays in focus.

## Duplicate files removed when the folder was imported (2026-09-13)

Byte-identical copies, verified by MD5; the kept file is named first.

| Kept | Removed |
|---|---|
| `دورات/_⁨حل أسئلة MIS⁩.docx` | `دورات/اسئلة سابقة/حل أسئلة MIS.docx`, `دورات/اسئلة سابقة/حل أسئلة MIS(1).docx` |
| `ملخصات سابقة/MIS Q.pdf` | `ملخصات سابقة/MIS Q(1).pdf` |
| `دورات/اسئلة سابقة/MISS/IMG-20150829-WA0053.jpg` | `…/IMG-20150830-WA0007.jpg` |
| `دورات/اسئلة سابقة/MISS/IMG-20150829-WA0054.jpg` | `…/IMG-20150830-WA0003.jpg` |
| `دورات/اسئلة سابقة/MISS/IMG-20150830-WA0000.jpg` | `…/IMG-20150830-WA0006.jpg` |
| `دورات/اسئلة سابقة/MISS/IMG-20150830-WA0001.jpg` | `…/IMG-20150830-WA0004.jpg` |
| `دورات/اسئلة سابقة/MISS/IMG-20150830-WA0002.jpg` | `…/IMG-20150830-WA0005.jpg` |

The v0.1 run saw all 45 files; the v1.0 run hashed the 37 files left after the removal (`ledger.json`).
