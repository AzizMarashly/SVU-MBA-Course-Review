# Chapter 6 report — تعريف المشروع (الجزء الثاني), pp. 204–237

## Counts
| item | n |
|---|---|
| raw items received (`by_chapter/ch06.json`) | 60 |
| of which SOUFI-XCHK (cross-check only, not a source) | 6 |
| of which topic-only (no record) | 5 |
| canonical records (real) | 22 |
| generated records | 1 |
| **total records in `bank_ch06.py`** | **23** |
| by type: exam / textbook / other / generated | 7 / 8 / 13 / 1 (a record may carry several types) |
| reconstructed (exam free-form → MCQ) | 1 (Q06-005, F24) |
| low-confidence | 3 (Q06-002, Q06-003, Q06-015) |

Exam sittings represented: EX15, S19, F24, TATI (Y16 only as a topic pointer).

## Shared review block (chapter 5 / chapter 6)
The end-of-chapter MCQs 5–10 and essays 3–4 are printed twice: at the end of chapter 5 (p.189–191) and again at the end of chapter 6 (p.230–232, verified visually on p.231). The task brief said "p.199–200 and p.232–233"; the extracted text and the rendered pages show p.189–191 and p.230–232, so the records cite p.230/231/232 and their `notes` state both print locations. The 8 BOOK items (book#56–61, #64, #65) are all chapter-6 content and are in this bank.

## Subsection coverage
| sub | name | real questions | generated |
|---|---|---|---|
| 6-1 | هيكل تقسيم العمل (WBS, work package, OBS, coding) | Q06-001…005, 007, 008, 009, 012, 014…022 | — |
| 6-2 | هيكل تقسيم العملية PBS | none | Q06-023 |
| 6-3 | مصفوفات المسؤولية | Q06-006, Q06-013 | — |
| 6-4 | خطة التواصل | Q06-010, Q06-011 | — |

Uncovered after generation: none. Only 6-2 needed a generated item (1 generated ≤ 22 real; 6-2 is a non-focus subsection, within the limit of 3). Inside 6-4, F24 recalled a question on "مصادر المعلومات" (6-4-3) but without any wording, so no record was built for it; 6-4 is covered by the two book items.

## Topic-only items (no record)
| raw id | source | text | points to |
|---|---|---|---|
| soufi#139 | S19 | مصفوفة المسؤولية (RAM) | 6-3 (noted in Q06-006) |
| recalls#5 | Y16 | شي خمس أسئلة عن work packages | 6-1 (noted in Q06-001) |
| recalls#119 | F24 | سؤال عن خطة التواصل بالمشروع | 6-4 (noted in Q06-011) |
| recalls#138 | F24 | سؤال عن مصادر المعلومات (ما بتذكر صيغتو) | 6-4-3 (noted in Q06-011) |
| others#162 | EMAD | سلايدات قراءة 23، 24 — الملف 6 | pointer to S18 slides, no question |

## Unresolved / skipped items
- Belong to chapter 5 (scope management), not chapter 6 — passed back: others#149 (مراقبة التغيير في النطاق), others#150 (زحف النطاق — the term appears only in ch05.txt), others#151 (التحقق من نطاق المشروع), others#159 (WBS > 100% → زحف النطاق).
- EMAD items whose claim the book cannot support (skipped, 3): others#152 (تحليل النظم يُستخدم للحصول على WBS — not in the book), others#156 (جميع حزم العمل متقاربة في الحجم والجهد — the book gives only the ≤10 working days rule), others#158 (طرق بناء WBS: قواعد إرشادية / قياس بالمقارنة / لولبية — the book gives the 7 steps and top-down decomposition with bottom-up validation only).
- others#167 (تسمى أيضاً مخطط المسؤولية الخطية): the term "linear responsibility chart" is absent from the book; mentioned in the notes of Q06-006 instead of a record.
- Q06-002 (S19 #17 / TATI #5) is a two-answer MCQ (options أ and ب both highlighted in both sources). The data model accepts one integer answer, so it is kept as `qtype="short"` with the four options quoted verbatim inside the stem and the answer "(أ) و(ب)". Flagged low-confidence.

## Disagreements between a source's marked answer and the book
| record | source(s) | source answer | book answer | handling |
|---|---|---|---|---|
| Q06-003 | S19 (items 16 & 55), TATI p9 #44 | صح (WBS may start in parallel with scope definition) | خطأ — the book presents WBS as the step *after* the scope statement (p.206, 211) and never mentions parallel start | `other_source`, `low_conf` |
| Q06-016 | EMAD #157 | WBS | حزمة العمل — the six what/when/cost/how much/who/how functions are listed under 6-1-6 حزمة العمل (p.216) | `other_source` |
| Q06-015 | EMAD #148 | experts / stakeholder analysis / interviews / historical documents | inputs on p.206 (organisational process assets, scope statement, scope-management plan, approved change requests) + prior-project examples and team effort (p.216) | `other_source`, `low_conf` |

BOOK highlights (p.231) all agree with the chapter text: mcq-5 ث, mcq-6 أ, mcq-7 ب, mcq-8 أ, mcq-9 ت, mcq-10 أ. ASEM confirms mcq-9 (1 agreement, 0 disagreements). SOUFI-XCHK circles agree with all six book answers (not counted as a source).

## Pages read visually (PNG)
207, 208, 215, 216, 224, 231. All other citations come from `ch_fixed/ch06.txt` pages 204–237 read in full.
