# Chapter 9 report — تخطيط الموارد في المشروع (pp. 325–365)

## Counts
- Raw items received: **60** (BOOK 14, EMAD 23, SOUFI-XCHK 7, EX15 5, S19 4, F24 3, TATI 2, ASEM 2).
- Canonical records: **32** — by type: exam 8, textbook 14, other 15, generated 1 (a record may carry several types).
- qtype: mcq 17, tf 6, short 4, essay 5 (incl. the two book calculation problems and one EMAD list).
- Reconstructed: **6** (Q09-002..007). Low-confidence: **2** (Q09-008, Q09-023). Generated: **1** (Q09-032).

## Coverage
- Covered by real questions: 9-1, 9-2, 9-3, 9-4, 9-5, 9-6 (all six).
- Covered only by generated: none. 9-2 was covered only by a low-confidence tf (Q09-008), so one generated MCQ on the definition of تقدير موارد النشاط was added (Q09-032).
- Uncovered: none.
- Focus (most exam items): 9-6 (levelling problem + EX15 goal item), then 9-4 (peak workers before levelling).

## Calculation problems (book method p.343–352)
- **S19 X1–X8 = TATI M1–M8 (same data)**: ES/EF: X1 0–4, X4 0–5, X2 4–6, X3 5–11, X5 5–8, X8 8–15, X6 11–15, X7 15–20. Duration **20**, critical path **X4–X3–X6–X7**; floats X1 = 1, X2 = X5 = X8 = 5. Load per day (early start): 5,5,5,5,6,**9**,5,5,5,5,5,5,5,5,5,4,4,4,4,4 → max **9** before levelling. Time-constrained levelling: shift X5 (and its successor X8) within their 5-day float → peak **7** (day 6: X2 4 + X3 3); 7 is the minimum (X2 must overlap critical X3), exhaustive check confirms. Student's solution (TATI p7: CP M4-M3-M6-M7, 20 days, "بإزاحة M5 و M8", LF(M3)=11, ES(M5)=5) agrees with the book method. Student's daily-total row (5,5,6,9,…) is a mis-transcription of 5,5,5,5,6,9,… — peak 9 is the same.
- **BOOK essay-3 (time constraint)**: duration 24, CP A–C–F–G, floats B 8, D 9, E 12, H 8; early-start peak 5 (days 1–8), 81 worker-days. Shifting E by 10, D by 9, H by 8 gives peak **4** (16 equivalent shift sets reach 4; 3 is impossible since 81/24 > 3).
- **BOOK essay-5 (resource constraint, 3 workers)**: unconstrained 11 days, CP A–C–E–F, peak 4 on days 3–5. Day-by-day with priority rules (least float → least duration → least resources → ID): A 1–2; day 3 C (float 0) before B; day 7 B (float 0 after delay) before E; day 10 D (fewer resources) + E together; F 12–14 → **14 days** (delay 3). 14 is optimal because B and C (2 workers each) cannot overlap.

## Disagreements source vs book
- EX15 recall "فائدة تسوية الموارد — تخفيف الزمن" contradicts p.341 (levelling usually lengthens the project) → book answer used, student's on `other_source` (Q09-002).
- EMAD 265: priority rules under "time constraints" with "الأكبر موارد" on ties; book p.348 gives them for resource-constrained levelling with "أقل كمية من الموارد" → `other_source` on Q09-016.
- S19 tf "بسبب تعقد الفعالية قد لا يكون بالإمكان تحديد الموارد" marked صح, TATI marks خطأ; the sentence is not in the book. Answered خطأ from the book's framing of activity resource estimation (p.331–332), `low_conf` (Q09-008).
- BOOK highlights (10 MCQs): all confirmed by the chapter text. ASEM (2 items) and SOUFI-XCHK (7 items) agree with the book on every item.

## Unresolved / not used
- Topic only: EX15 recalls#91/#166 "المشاريع المقيدة بالموارد" → 9-6; EX15 recalls#92/#167 "هدف تسوية الموارد" (merged as variant into Q09-002); F24 recalls#135 "سؤال عن المشاريع المقيدة بالزمن" → 9-6; EMAD others#264 "الأمثلة من المحاضرة 10 السلايد 31" → 9-6.
- F24 recalls#147 "مسألة عن Resource leveling عليها 7 أسئلة" (القسم العملي 4): no data recalled. TATI's problem carries exactly 7 sub-questions, so it is plausibly the same problem, but this cannot be verified; F24 was NOT added to the sources of Q09-003..007.
- EMAD skipped (concept absent or stated differently in the book): others#243 (resources = scarce + constraints), #244 (storable / non-storable), #245 (4M classification; book lists six types p.330), #246 (network becomes schedule when resources assigned), #248 (allocation at/below/above capacity), #256 (improve schedule by adding resources before levelling), #259 (priority matrix to decide time- vs resource-constrained). 7 items.
- EMAD near-duplicates merged: #250 + #252 (contract at the peak) → Q09-024; #257 + #258 → Q09-028; #253 → variant of Q09-012; #262 → variant of Q09-002; #263 → variant of Q09-016.

## Pages read
- Text: 325–365 (whole chapter file). Visually (PNG): 350 (day-3 allocation figure and float update rule), 358 (both problem tables) — plus 349, 351 rendered for context.
