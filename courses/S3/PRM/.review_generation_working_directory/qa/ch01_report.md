# Chapter 1 report — مقدمة في إدارة المشاريع (الجزء الأول), pp. 11–49

Output: `render/bank_ch01.py` (imports cleanly, 35 records).

## Counts
| item | n |
|---|---|
| raw items received (`by_chapter/ch01.json`) | 110 |
| canonical records | 35 |
| by type: exam / textbook / other / generated | 18 / 7 / 19 / 1 (a record may carry several types) |
| records with exam sittings | 18 (S19 10, EX15 8, TATI 7, F24 3, Y16 1) |
| reconstructed (free-form exam recall → MCQ) | 3 (Q01-005, Q01-016, Q01-017) |
| low-confidence | 7 (Q01-004, 007, 008, 010, 013, 031, 034) |
| generated | 1 (Q01-035, subsection 1-1) |
| raw items merged into records (as primary or variant) | 85 |
| raw items dropped as out of chapter 1 / older curriculum | 18 (all EMAD) |
| topic-only (no record) | 1 |
| SOUFI-XCHK cross-check only (not a source) | 5 |
| ASEM items for this chapter | 0 |

Raw-item accounting: 85 merged + 18 dropped + 1 topic-only + 5 cross-check + 1 redirected to chapter 3 (EX15 `recalls#29` تعريف المحفظة) = 110.

## Coverage of subsections
| sub | name | real questions | generated | status |
|---|---|---|---|---|
| 1-1 | مقدمة | 0 | 1 (Q01-035: PM as a tool for managing change, p.13) | covered by generated only — the intro is a preview; its one concrete statement is used |
| 1-2 | أهمية إدارة المشاريع | 3 (Q01-013, 017, 027) | 0 | covered |
| 1-3 | تعريف المشروع / نظم الإنتاج / البرنامج | 10 | 0 | covered (focus area: EX15, S19, F24, TATI) |
| 1-4 | خصائص المشروع مقابل الأعمال التشغيلية | 17 | 0 | covered (focus area: EX15, S19, TATI, Y16) |
| 1-5 | أبعاد المشروع وأصحاب المصلحة | 4 (Q01-023, 029, 030, 034) | 0 | covered |
Uncovered: none.

## Dedup decisions worth knowing
- Program definition: EX15 «يضم عدداً من المشاريع المترابطة» (kept as stem, options exact) merged with EX15 «مجموعة من الأعمال المتشابهة المنسقة…», EX15/F24 «تعريف البرنامج», S19 «تعريف البرنامج هو مجموعة مشاريع…» and EMAD items 21–26 → Q01-002 (sources EX15, S19, F24, EMAD).
- Project definition: EX15 «تعريف المشروع (سؤالين)» + MURAJA item 3 (options kept exactly) + EMAD items 8–13 → Q01-001.
- «ما الغير صحيح عن نقاط التشابه بين المشروع والعملية» and «من الخصائص المشتركة … ما عدا» are the same EX15 question → Q01-003.
- Constraints: S19 items 21/52, TATI items 3/41 and the S19 src06 recall (المواد/الأشخاص/التجهيزات) → Q01-008; the two T/F constraint items (cost; contract terms) kept as separate records because each was asked in S19 and TATI.
- Book essay-2 (compare project vs operations) + EX15 «الفرق بين التشغيل والمشروع» → one essay record (Q01-018, types exam+textbook). EMAD's three T/F items on the same idea → one T/F record (Q01-026).
- EMAD items 49–51 (المشاريع المحددة / غير المحددة) are merged as variants into the EX15 research-projects item (Q01-004) rather than dropped.

## Disagreements between a source's marked answer and the book
| record | source mark | book | handling |
|---|---|---|---|
| Q01-015 مثال عن الإنتاج بدفعات | EX15 (kifah file) highlights «السيارات»; the scanned sheet of the same sitting circles «الألبسة الجاهزة» | p.22: الألبسة = بدفعات, السيارات = الإنتاج الكمي | answer الألبسة; kifah mark on `other_source` |
| Q01-008 القيود | TATI item 3 highlights two options (التكلفة + نوعية المنتج); TATI item 41 and S19 only التكلفة | p.27: constraints = الزمن والتكلفة والجودة/الأداء, so «نوعية المنتج» is also a constraint | answer التكلفة (source intent), `other_source` + `low_conf` + distractor note |
| Q01-034 أحد أطراف إدارة المشروع | MURAJA: فريق المشروع | p.35 also lists الزبائن among stakeholders | kept فريق المشروع, `low_conf` + distractor note |
| Q01-027 GDP share | EMAD: 20 trillion US / 85 trillion world | p.15: 2.5 trillion ≈ 25% of US GNP | stem restated on the 25% share, EMAD figures in `notes` |
| Q01-013 محدودية المصادر = السبب الرئيسي | S19 + TATI: صح | book never names it the main reason (its reasons: إدارة التغيير, ضغط دورة حياة المنتج …) but does not contradict it | kept صح with `low_conf` |
| Q01-017 أسباب الاهتمام | EMAD's answer list (globalisation, internet, mergers…) is from an older curriculum | p.17–18 list five different reasons | F24's answer (تقليص حجم الشركات) used; EMAD text kept only as a variant |
BOOK highlights (p.40, read visually): all five MCQ highlights agree with the chapter text. SOUFI-XCHK marks on the five copied book MCQs agree with the book highlights.

## Dropped raw items (concept not in chapter 1 of this book)
Older-curriculum stakeholder/sponsor material (book ch.1 has no sponsor, charter, change requests, influencers, or stakeholder-management process): EMAD `others#13` (زبون وممول), `#32` (تأثير سلبي فقط), `#33` (إدارة أزمات/استباقية), `#34` (list incl. الممول والممانعون), `#35` (توقيع الميثاق ← الجهة الممولة), `#36` (مدير المشروع يوجه الممول), `#38` (الزبون شخص فقط), `#39` (يعد ميثاق المشروع ويدير طلبات التغيير ← مدير المشروع), `#41` (المؤثرون — appears in ch.2), `#42` (أولويات أصحاب المصلحة), `#43` (تحديد أصحاب المصلحة في عملية تعريف المشروع).
Portfolio (book covers it in chapter 3, not chapter 1): EMAD `others#27, #28, #29, #30`.
Other: EMAD `others#2` (فوائد إدارة المشاريع — book review MCQ 7, chapter 2 material), `#16` (SMARTE — not in the book; SMART appears only in ch.5/6 for objectives), `#25` (أهداف إدارة البرامج: حل قيود الموارد، محاذاة التوجيه الاستراتيجي — not in the book).
Count: 11 + 4 + 3 = 18 EMAD items dropped. The other 30 EMAD items are merged: 7 as primary stems (Q01-025 … Q01-031) and 23 as variants of records whose answer the book supports (incl. `#1`, `#11`, `#26`, `#49–51`).
TATI: all 8 items have their concept in the book; none dropped.

## Topic-only
- Y16 `recalls#6` «سؤالين عن البحث العلمي» → points to the research-projects item (Q01-004, sub 1-4); Y16 not added to its sources because the item names no question.

## Unresolved / redirected
- EX15 `recalls#29` «تعريف المحفظة»: the portfolio concept is absent from chapter 1 (it is in chapter 3, «محفظة المشاريع»). Not recorded here; the chapter 3 helper should pick it up (exam source EX15). Same for EMAD `others#27–30` if wanted there.
- Q01-004 (مشاريع البحث العلمي: أهداف ورؤية غير واضحة): concept not in the book at all (grep of all 14 chapters finds no «البحث العلمي»); kept as an exam record with `low_conf`, answered from the agreement of all recollections.

## Pages read
Text of every page 11–49 read from `ch_fixed/ch01.txt`. Read visually (PNG): 22, 27, 40.
