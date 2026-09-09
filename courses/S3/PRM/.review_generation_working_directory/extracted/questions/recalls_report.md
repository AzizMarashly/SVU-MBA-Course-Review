# recalls.json — transcription report (src01, src02, src03, src04, src07, src08)

227 items. Indices below are 0-based positions in `recalls.json`.

| src | file | items | notes |
|---|---|---|---|
| src01 | 2016 pm اسئلة دورات.docx | 11 (idx 0-10) | Telegram-style topics of a 2016 sitting; Lag/Lead study note; one recalled MCQ. img1.png = emoji, ignored. |
| src02 | PM-112هام.docx | 35 (idx 11-45) | Recollection list + 3 readable images + forum question. |
| src03 | Pm-112- Q_A by kifah (2).pdf | 55 (idx 46-100) | p1-3 = kifah's own answers ("أنا حطيت"); p4-5 = verbatim copy of the src02 list with highlights; p5 embeds the two src02 photos. |
| src04 | أسئلة PRM فصل F24 مركز خارجي.txt | 48 (idx 101-148) | 43 numbered + 5 practical (P1-P5). |
| src07 | اسئلة-مشروعات.pdf | 26 (idx 149-174) | Handwritten scan: items 1-19, 21-26 (no item 20), network, EVA table. |
| src08 | الأسئلة التي تأتي في فحص ال PM (2).pdf | 52 (idx 175-226) | Typed set, 49 items with yellow highlights + header topics + closing notes; 5 images. |

Counts: mcq 77, short 70, topic 27, calc 27, tf 26. `dup_of` set on 58 items (within-file and cross-source verbatim copies; the earliest index wins). 16 items carry a `CURRICULUM CHECK` note.

## Visual inspection
Inspected visually: 20 page/image renders + 1 WMF render + 7 zoom crops.
- src02: img2.jpeg (EVA table, values confirmed as given), img3.png (lecture slide screenshot, taskbar shows **2015/07/29 03:48**, video title `MBA_PM112_C4_F14...`), img4.jpeg (network "باستخدام الشكل، ما هي مدة المشروع؟", A1→B3,C3; B→D2,E7; C→G4; D→F4; E→G4; F→H5; G→H5 — confirmed). img1.wmf rendered with Pillow: 72x18 px empty form-field frame (Facebook "Top of Form" placeholder), nothing to transcribe.
- src03: kifah_p01..p05 (5 pages). Green highlight = the student's chosen answer, red = the student's remark. p5 embeds the same two photos as src02 img4/img2.
- src07: scan_p01..p03 (3 handwritten pages), fully read; circled letters transcribed as `marked_by: student-recall`.
- src08: tati_p01..p09 (9 pages) + zoom crops of p02 (LMS "Question 7" screenshot), p03 (EVA notebook table), p04 (EVA solution table), p06 (resource table), p07 (Gantt/AON solution photo). Highlights transcribed as `marked_by: highlight`. Text extraction had mis-ordered the image pages; loc uses the page where the image actually sits.

## Data blocks (all numbers are in the JSON notes)
- Network N1 (src02 idx 11, src03 idx 99, src07 idx 169-173, topic in src01 idx 3 and src02 idx 12 / src03 idx 72): A:1 | B:3(A) | C:3(A) | D:2(B) | E:7(B) | F:4(D) | G:4(C,E) | H:5(F,G). Sub-questions recalled: project duration (src02 says "20 يوم"), ES of F and H, LS of D, critical path, effect of F delayed 6 days.
- EVA table E1 (src02 idx 13, src03 idx 100, src07 idx 174): Task BCWS/ACWP/BCWP = 1: 9500/10000/9500 | 2: 15000/13000/11000 | 3: 13000/13000/13000 | 4: 8000/8000/9000 | 5: 10000/10000/9000. Sub-questions: biggest schedule variance, biggest cost variance, on time and budget, later/costlier/cheaper.
- EVA table E2 (src08 idx 189): BCWP/ACWP/BCWS = 4000/6000/5000 | 8000/3000/6000 | 7000/8000/4000 | 9000/5000/10000 | 4000/4000/4000, with the student's SV/SPI/CV/CPI solution.
- Network N2 (src08 idx 183, LMS screenshot "Question 7"): A6→B7; B→C10,F9,I11; C→D1,G8; D→E4; F→G; G→H4; H→J6; I→J; J→K3; E→K. Add R=5 between A and B; options 49/48/52/53; compiler says 49.
- Resource-levelling problem R1 (src08 idx 198): 8 activities M1..M8 with predecessors, durations, workers; 7 sub-questions; student solution CP M4-M3-M6-M7, duration 20.
- SS lag item (src02 idx 21, src03 idx 66/98, src07 idx 161): SS, 6 and 12 days, lag 4 → options 16/12/4. **Conflicting student answers**: src03 highlights 12, src07 circles 16 (with a sketch giving 16).
- Payback items: 5 vs 8 years @10% (src02 idx 25 / src03 idx 70); 15 vs 5 years @15% (src03 idx 97 / src07 idx 160, both mark "choose the second, reject the first"; margin note says the rate is a distractor).
- PERT: optimistic 60, pessimistic 40, most likely 50 (src02 idx 33, values as written).

## Recurring items across files (same sitting evidence)
| item | src02 | src03 | src07 | others |
|---|---|---|---|---|
| Network N1 + "إذا F تأخر 6 أيام" | 11, 12 | 72, 99 | 169-173 | src01 topic 3 (generic) |
| EVA table E1 (5 tasks) | 13 | 73, 100 | 174 | src01 topic 4 (generic) |
| SS 6/12 lag 4 | 21, 43 | 66, 98 | 161 | — |
| لمن يسلم المشروع | 16, 34 | 46, 76, 95 | 158 | — |
| Continuously improve Process → Optimized | 17 | 78 (+52, 57 related) | — | — |
| لا ينتمي لتقدير زمن المشروع (Critical Path) | 15 | 74 | — | — |
| لا يؤثر على تصنيف المشروع (مدير المشروع wrong) | 18 | 79 | — | — |
| Political feasibility | 19 | 80 | — | — |
| مشروع/برنامج/محفظة (group of works) | 20 | 65 | 155 (يضم عدد من المشاريع) | src04 item 3 (تعريف البرنامج) |
| مشاريع البحث العلمي: أهداف غير محددة | 23 | 68, 94 | 157 | src01 topic 6 |
| Delphi | 24 | 69 | — | — |
| Payback 5 vs 8 @10% | 25 | 70 | — | — |
| Payback 15 vs 5 @15% | — | 97 | 160 | — |
| مثال الإنتاج بدفعات | (mass production 27) | 82 | 152 | src04 item 29 (الإنتاج الكمي) |
| خصائص المشروع ما عدا (مدة غير محددة) | — | 81 | 151 | src01 idx 10 (خصائص المشاريع MCQ) |
| مرحلة تقدير المخاطر | — | 83 | 153 | src08 closing notes 226 |
| عوامل نجاح المشاريع ما عدا العولمة | — | 86 | 156 | — |
| Gantt / critical path meaning / work package / smallest WBS element | 30, 37 | 87-90 | 162-165 | src08 idx 226 (closing notes) |
| تسوية الموارد / المشاريع المقيدة بالموارد | 44 | 91, 92 | 166, 167 | src04 P4 (idx 147, F24) |
| Matrix vs functional vs project org (motivation) | — | 93 | 168 | src08 header, items 10/19/45 |
| feasibility study covering technical capability | — | 49, 96 | 159 | — |
| PLC vs project life cycle | 41 | 63, 77 | 149 | src08 item 35 |

## Best grouping into sittings
1. **Sitting A — c. 2015 (spring/summer 2015 term, likely S15 or F14 resit).** src02, src03 p4-5, and src07 describe the same paper: identical N1 network photo, identical E1 table, the SS-lag item, "F delayed 6 days", "لمن يسلم المشروع", "Continuously improve → Optimized", Political feasibility, payback pairs, the 26 handwritten items of src07 match src03 items 29-46 one-to-one (same order). Evidence for date: the src02 screenshot's Windows clock reads 2015/07/29 and the lecture video is labelled F14; src03 p4 heading says "أسئلة من دورة الفصل الماضي" (copied later, so kifah's own p1-3 is the following term). src02's Facebook links (fbid ~310251…) are consistent with 2015. **Nothing in these three files carries an explicit semester label.**
2. **Sitting B — the term after A (kifah's own exam, src03 p1-3).** Different items ("خيار لا يعتبر من التخطيط", Mitigating Risk, "إدارة المشاريع هي", optimized/managed, scope management, payback definition, "داخل وخارج الأقسام"), with overlaps to A on the delivery question (idx 46 vs 16) and the maturity-level vocabulary (52, 57 vs 17). Treat as a separate sitting that reused part of the A pool.
3. **Sitting C — 2016 (src01).** Explicitly "2016" in the file name; topic-level only (EVA 4-5 q, CP 4-5 q, 5 org-type q, network 6-7 q, EVA table 6-7 q, work packages 5 q, research projects 2 q, phases). Consistent with the A pool structure (network + EVA table blocks) but no item-level identity; only the "خصائص المشاريع" MCQ (idx 10) is item-level, and it resembles src03 81 / src07 151.
4. **Sitting D — F24, external centre (src04).** Explicit label in the file name. Vocabulary matches the current book closely (chapters 1-14 in order: 1-2-1 downsizing, 3-5 classifications, 4-5 PMBOK areas, 6-1 WBS checks, 7-7-2 milestone chart, 11-5-1 strong matrix, 13-2 team stages, 14-3-2 premature closure, 12-2 risk order). Practical part: FF + lead, 4-activity EVA, SPI, resource levelling (7 q), critical path (7 q) — same *shape* as A but different data (4 activities, FF instead of SS). Independent sitting.
5. **Sitting E — undated typed set (src08).** Different style (many T/F, PMBOK-3rd-edition process vocabulary, "شبكي" org type, LMS "Question 7" screenshot with Arabic-Indic digits, its own EVA table E2 and resource problem R1 "اجت بالفحص الماضي"). Overlaps with A only at the level of topics (5 org-type questions, one EVA and one CP problem — same as src01's description) and the closing notes. Probably the oldest material (course version taught with PMBOK process groups); treat as a separate, curriculum-suspect pool.

## Items to curriculum-check (vocabulary from a different syllabus)
src08: idx 176 (مدخلات إجرائية إدارة النطاق), 177 (sponsor signs charter), 179 (الموازنة من أعلى إلى أسفل), 191 (إجراءات الإطلاق ضمن إدارة التكامل), 193 (مخرجات إجرائية خطة إدارة النطاق), 194, 197 (مجموعات إجراءات إدارة المشاريع), 214 (Develop Preliminary Project Scope Statement), 220 (إجرائية WBS بالتوازي مع تعريف النطاق), 222 (Organizational Process Assets), 223 (Enterprise Environmental Factors), 225 (تعريف فعاليات المشروع من WBS); also 175/186/194/221 use the org type "شبكي" (network organisation) which the book's ch11 does not list.
src02/src03: idx 17, 78 ("Continuously improve Process → Optimized"), 52 ("تحسين العمليات بشكل مستمر → التنفيذ والرقابة"), 57 ("في أي مرحلة يجري تكامل المشروع: optimized / managed") — CMMI-style maturity levels, absent from the book TOC. Also idx 45 / 226 (Task vs Activity as "smallest planning element") uses a planning vocabulary not in the TOC.
src04 item 4 (idx 104, "نهج الحس السليم") and item 15 (idx 115, "المشاريع المقادة بالتغيير") could not be placed on a TOC title; ch_guess is tentative.

## Caveats
- Nothing was verified against the book; `marked_answer` reproduces only what the source marks (highlight, circle, or the student's remark). Student remarks are kept in `marked_answer`/`notes`, not in stems.
- src03 p1 item 4 (idx 49): three green lines — unclear whether lines 2-3 are options or an explanation.
- src07 item 10 (idx 158) option c is hard to read ("المستهلك/القطاع"?).
- src08 idx 198 resource table: worker column alignment inferred from the Gantt labels; last value overwritten (2/3). CPI "1,6" for row 2 is as written (8000/3000 = 2.67).
- src08 idx 222 highlights "صح" on a statement that misdefines OPA; treat the highlight as the compiler's opinion only.
- `ch_guess`/`sub_guess` were assigned from toc_raw.txt titles; items about "في أي مرحلة" were put under ch4 (4-2-x) even when the topic itself belongs elsewhere (e.g. risk estimation → also 12-4).
