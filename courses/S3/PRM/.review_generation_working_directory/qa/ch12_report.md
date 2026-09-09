# Chapter 12 report – إدارة المخاطر في المشروع (pp. 440–472)

Output: `render/bank_ch12.py` (imports cleanly, 30 records).

## Counts
| item | n |
|---|---|
| raw items received (`by_chapter/ch12.json`) | 57 |
| canonical records | 30 (27 real + 3 generated) |
| by type: exam / textbook / other / generated | 5 / 14 / 17 / 3 (a record may carry several types) |
| by qtype: mcq / tf / short / essay | 17 / 7 / 3 / 4 |
| reconstructed (free-form exam recalls → MCQ) | 3 (Q12-003, Q12-004, Q12-005) |
| low-confidence | 3 (Q12-004, Q12-005, Q12-027) |
| generated | 3 (Q12-028 priorities 12-4, Q12-029 impact > probability 12-4, Q12-030 risk owner 12-6) |

Raw-item accounting: BOOK 14 (all used), S19 3 (all used), KIFAH 1 (used), F24 3 (2 used, 1 misassigned), EMAD 27 (20 used, 7 skipped), MURAJA 2 (used), ASEM 1 (used as cross-check), SOUFI-XCHK 6 (not a source; cross-check only). Exam sittings present: F24, KIFAH, S19.

## Coverage (subsections)
- Covered by real questions: 12-1 (Q12-018), 12-2 (Q12-001, 014, 019–021), 12-3 (Q12-003–005, 016, 022–024, 027), 12-4 (Q12-006–008, 017), 12-5 (Q12-002, 009–012, 015, 025, 026), 12-6 (Q12-013).
- Generated additionally on ideas no real question tests: 12-4 ×2 (priority order p.451; impact weighs more than probability p.455), 12-6 ×1 (documenting responsibility / risk owner p.462). 12-5 is the focus area (most exam items) and is already densely covered.
- Uncovered: none.
- Note: BOOK mcq-10 (risk register) is filed under 12-6, not the raw `sub_guess` 12-5-3, because the text is on p.461 inside §12-6.

## Disagreements between a source's marked answer and the book
- BOOK mcq-1 (Q12-001): options أ and ث are printed identical; highlight on ث. Correct sequence kept as option أ (ans=0), the duplicate replaced by a real wrong order; explained in `notes`.
- BOOK mcq-7 (Q12-010): no highlighted option in the book (checked on the page image p.465). Answered from the text p.457 = استراتيجية التجنب; noted in `notes`.
- MURAJA #8 "أول مرحلة من مراحل إدارة المخاطر: تخطيط المخاطر": the book's first step is تحديد المخاطر (p.445, fig 12-2); folded into Q12-001 as variant with `other_source`.
- EMAD #359 defines risk as "غير قابل للإدارة"; the book says all projects carry risks that need managing (p.442) → `other_source` on Q12-018.
- S19 #12 recalled answer "دلفي": Delphi does not appear anywhere in the book; Q12-004 answers العصف الذهني (p.445) with `other_source` and `low_conf`.
- SOUFI-XCHK #117 highlights أ (التجنب) for the book's mcq-8; the book highlight and text (p.459) give ث (القبول). Not a source, mention only. The other five SOUFI-XCHK items agree with the book.
- ASEM confirms BOOK mcq-9 (1 of 1 cross-checked in this chapter, agreement 1/1).

## Unresolved / skipped raw items
- F24 item 16 "تعريف التحسين Enhance" (recalls#116): concept belongs to chapter 5 (priority matrix constrain/enhance/accept, ch05.txt); not a chapter-12 item. No record created here; should be picked up by the ch5 helper.
- EMAD items skipped because the book cannot support them: #360 (financial/operational/strategic risk types), #364 (risk-management principles, ISO-style list), #369 (outputs of risk measurement = opportunities), #373 (moving risks red→yellow→green), #379 (buffer), #380 (reserve usually 20%), #384 (wrong priorities stop project start). 7 items.
- No "topic only" items in this chapter.

## Pages read visually (PNG)
443 (fig 12-1), 444 (fig 12-2 process steps), 446 (fig 12-3 RBS), 447 (fig 12-4 risk profile), 454 (fig 12-7), 455 (fig 12-8 matrix + zone text), 465 (review MCQs 4–7, confirming mcq-7 has no highlight). All other cited pages verified from `ch_fixed/ch12.txt`.
