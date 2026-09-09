# Chapter 8 report — تخطيط الزمن في المشروع (الجزء الثاني), pp. 281–324

## Counts
| | |
|---|---|
| raw items received (`by_chapter/ch08.json`) | 88 (EMAD 37, EX15 18, S19 13, BOOK 5, SOUFI-XCHK 4, F24 3, Y16 2, KIFAH 2, TATI 2, ASEM 2) |
| canonical records | **46** |
| by type (a record may carry several) | exam 26 · textbook 5 · other 21 · generated 0 |
| by qtype | mcq 29 · short 10 · tf 7 |
| reconstructed | 20 |
| low-confidence | 6 (Q08-010, -022, -023, -024, -034, -046) |
| generated | 0 (every subsection is covered by real questions) |

Ids run exam (Q08-001…026) → textbook (027…029) → other (030…046).

## Recalled networks — solved (book rules p.296–301)
- **A–H network** (EX15 photo, Y16 topic, src07 hand drawing): A1, B3(A), C3(A), D2(B), E7(B), F4(D), G4(C,E), H5(F,G).
  ES/EF: A0-1 B1-4 C1-4 D4-6 E4-11 F6-10 G11-15 H15-20 → **duration 20** (student's "20 يوم" confirmed).
  LS/LF: H15-20 G11-15 F11-15 E4-11 D9-11 C8-11 B1-4 A0-1. Slack C7 D5 F5, rest 0. **CP A-B-E-G-H**.
  F +6 days: slack 5 → project +1 day (21), CP becomes A-B-D-F-H. Records Q08-001…005 (duration, ES F/H, LS D, CP, F delay).
- **"Question 7" network** (S19 + TATI screenshot): A6, B7(A), C10(B), F9(B), I11(B), D1(C), G8(C,F), E4(D), H4(G), J6(H,I), K3(E,J).
  Forward pass → duration 44, CP A-B-C-G-H-J-K. R=5 inserted on A→B (critical) → **49**; both sources' "49" confirmed. Record Q08-006.
- **X1–X8 table** (S19) = **M1–M8 table** (TATI, routed to ch09 as recalls#198, same numbers): X1 4(-), X2 2(X1), X3 6(X1,X4), X4 5(-), X5 3(X4), X6 4(X3,X2), X7 5(X6), X8 7(X5).
  ES/EF: X1 0-4 X4 0-5 X2 4-6 X3 5-11 X5 5-8 X6 11-15 X7 15-20 X8 8-15 → **duration 20**.
  LS/LF: X7 15-20 X8 13-20 X6 11-15 X5 10-13 X3 5-11 X2 9-11 X4 0-5 X1 1-5. Slack X1 1, X2 5, X3 0, X4 0, X5 5, X6 0, X7 0, X8 5. **CP X4-X3-X6-X7** (student's solution in TATI agrees).
  LF(X3)=11; slack(X6)=0; slack(X8)=5 (free = total, terminal activity); X2 +6 → X6 (and project) +1 day; X3 +3 → X3 critical → project 23, X6/X7 delayed; ES(M5)=5.
  Records Q08-007…014. TATI added as a source to the sub-questions it shares (LF M3, CP, duration) and Q08-014 (ES M5) is TATI-only. The Gantt / worker-levelling sub-questions of the M-table stay with chapter 9.
- **Three-point**: S19 (60/20/25) → (60+100+20)/6 = 30 (option "30"); EX15 (60/40/50) → 300/6 = 50. Q08-015, -016.

## Subsection coverage
| sub | real questions | generated |
|---|---|---|
| 8-1 CPM | Q08-017, -027, -039 | – |
| 8-2 duration estimation | Q08-015, -016, -020, -023…-026, -029…-038 | – |
| 8-3 forward/backward pass | Q08-001…003, -007, -013, -014, -028 | – |
| 8-4 slack & critical path | Q08-004…006, -008…-012, -018, -040 | – |
| 8-5 replanning / compression | Q08-019, -021, -022, -031, -041…-046 | – |

Uncovered: none. Generated: 0.

## BOOK items and the double printing
The five BOOK MCQs routed here (mcq-3, 7, 8, 9, 10, transcribed from p.272–274) are printed again on **p.313–315** in the chapter-8 review block; the chapter-8 pages were checked visually (highlights identical: 7→ث, 8→ب, 9→ت, 10→ب). All five highlights agree with the chapter text (p.283, 290, 294/296, 304–305). The book's network exercises 2–4 (p.316–317, reprint of p.274–276) are routed to chapter 7 and not duplicated here. The essay item "تكلم عن عملية تخطيط الزمن" (p.315) is also routed to ch07.

## Disagreements between a source's marked answer and the book
None. Cross-checks: ASEM agrees on both book MCQs it reproduces (mcq-9, mcq-10); SOUFI-XCHK agrees on all four it copies (mcq-3, 7, 8, 9); KIFAH's own answer (أطول مسار) agrees; TATI/S19 "49" confirmed; EX15 "20 يوم" confirmed; EMAD keys agree wherever the book covers the item (its slack wording "دون تأخير الأنشطة اللاحقة" differs from the book's "دون تأخير انتهاء المشروع" — noted in `book_says` of Q08-040).

## Low-confidence records
- Q08-010 "fs لـ X8": symbol ambiguous (free slack?); book defines one slack (LS−ES) = 5 either way.
- Q08-022 "بكلف 10000 وخلصناه قبل بأسبوعين": recall could mean crashing (p.307) or project float (p.302); student's "تحطيم" kept, alternative offered as option ب.
- Q08-023 Delphi: the term does not occur anywhere in the book (grep of all chapters); reconstructed from recall, `book_says` set.
- Q08-024 KIFAH "مدة النشاط": only two partial options recalled, no student answer.
- Q08-034 EMAD "الجهد = المدة × الموارد": consistent with p.285 (person-days) but the formula is not written in the book.
- Q08-046 EMAD "flatter slope": book orders crashing by lowest cost/week (p.307, 310) without the slope wording.

## Topic-only / unresolved items (no record)
- recalls#1 (Y16) "أربع خمس أسئلة عن المسار الحرج والبداية والنهاية" → 8-3/8-4 (topic only).
- recalls#3 (Y16) network topic: used as a source for Q08-001…005 because the transcriber matched it to the A–H block; no numbers of its own.
- recalls#12 / #72 (EX15) "7 أسئلة على الشبكة" → covered by Q08-001…005 (listed as variants).
- recalls#14 (EX15) lecture-slide screenshot (business-centre network A5…H35 = book Table 8.2, p.301, 235 days, A-B-F-G-H): not a question.
- recalls#148 (F24) "مسألة عن المسار الحرج عليها 7 أسئلة": no data → 8-4, topic only.
- recalls#184 (TATI) "الجواب 49": answer line of Q08-006.
- others#242 (EMAD) "مثال عملي عن التحطيم — السلايد 53": pointer only → 8-5.
- **Unresolved:** soufi#103 (S19) "المسار الحرج من بين المسارات التالية: 1-2-3-4 / 1-3-4-5 / …" — no network or durations in the file; cannot be solved or verified.

## EMAD items skipped (concept not in this book) — 11
others#196 (ميل للزيادة في التقديرات), #197 (تدريب المقدّرين), #200 (شهر العمل), #201 (إجرائية تخطيط المشروع — ch7 layout), #202 (تقنيات تقدير الموارد: حكم خبير/مماثل/تحليل البدائل), #203 (جدول المهام), #208 (طريقة المعطيات التاريخية as a named method), #210 and #213 (Delphi / extended Delphi — absent from the book), #225 (PERT expansion — the book never spells it out), #226 (PERT summary — only the review question mentions PERT).
Included EMAD items: 25 (merged into 17 records; #195, #199, #211, #228, #229, #231, #236, #239 kept as variants).

## Pages read
- Text (`ch_fixed/ch08.txt`): all of 281–324.
- Visually (PNG): **301** (Table 8.2, CP A-B-F-G-H, 235 days), **314**, **315** (review highlights). Existing renders of p.313 also produced but not needed.
