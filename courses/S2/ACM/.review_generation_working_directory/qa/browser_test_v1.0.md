# Browser test (A.7) — ACM v1.0, 2026-09-25

Chrome (Claude-in-Chrome), page served from a scratch copy of `out.html` over `python -m http.server` on 127.0.0.1:8777 (port 8765 was
taken by another session's server). Desktop: 1394 px viewport. Phone: the window could not be resized (maximised window, `innerWidth`
stayed 1394), so the page was loaded in a same-origin iframe of 390 × 844 px (`innerWidth` 390 inside) — media queries and layout behave
as on a 390 px screen; touch was not tested. `scrollBehavior='auto'` set before screenshots. localStorage cleared at the start.

| Check | Result |
|---|---|
| Answers hidden by default; one click reveals one, label changes, second click hides | 0 open on load; clicking Q01-001 opened only it (open count 1, «إخفاء الإجابة» shown); second click closed it |
| Reading modes (counter vs bank) | exam 97, textbook 119, other 1, generated 20, all 209 — all equal to `bank.json` |
| Importance slider at 5 | 28 shown, all `data-importance=5` (bank: 28) |
| Repetition slider at max | max = 5; 7 shown (bank: 7 with freq 5) |
| Panel closed on phone, open on desktop | desktop first load open; 390 px iframe closed |
| Badge + summary with panel closed and a filter active (390 px) | importance 4+: badge «1», summary «★4+» |
| Essentials | 146 shown, all importance ≥ 3 (bank: 146); every «more» block folded (0 of 147 open); chapter 7 summary «16 من 38 (الأساسيات 16)»; second tap restored 209 and reopened 147/147 |
| Collapse independence | fold chapters → 0 open, an open answer stayed open; fold sections → 0 of 19 open with 7 chapters still open; fold all → 0 chapters/sections/page blocks open, answer untouched; open all restored |
| Page-block defaults | howto and scope open; method, sources, lists, toc, metadata closed; reference lists closed |
| Search inside a collapsed chapter | chapter 9 folded, search «التكاليف الغارقة» → 1 hit (Q09-010), chapter 9 reopened |
| State across reload | mode textbook + importance 3 → 85 after reload; Essentials and a folded chapter 2 survived a reload |
| Reset filters | back to 209, mode all, importance 1 |
| Symbol chip → sheet | FC chip on Q10-001 opened the bottom sheet («FC = التكاليف الثابتة الكلية…»); ✕ closed it |
| Step reveal | Q10-001: 3 collapsed steps; one summary click opened one; «إظهار كل الخطوات» opened all 3 |
| Figures (13) | 390 px: SVG 325 px inside a 351 px card, no horizontal page scroll. The 7 exam charts (Q10-001…007, `hide_labels`) sit under the stem and show only «الخط 1…5», «النقطة أ/ب», axes «ع/س», no names or values; aria-label/caption neutral; the answer block shows «مفتاح الشكل: الخط 1 = الإيرادات الكلية …» right under ✔; the recalled student text (which names the line) moved into the answer block for these 7. The 6 solution figures (Q10-012, 021, 029, 032, 033, 037) now render inside the answer block, because their labels print the answer (e.g. «هامش الأمان = 28,000», «نقطة الإغلاق 26»). Labels enlarged (17 px in a 640-unit viewBox, halo), left margin widened so values like 12,000,000 are not clipped, close point labels staggered on two rows — re-checked on Q10-029 and Q10-012. Highlight visible (filled, larger point). |
| Both themes | light (body rgb 251,250,247) and dark (rgb 17,20,24); figures checked in both |
| Version | title «… — v1.0», cover «الإصدار v1.0», metadata summary «v1.0 · المواصفة v0.12 · CC BY-NC-SA 4.0»; file `مراجعه كامله لماده ال ACM_v1.0.html` |

Not tested: real touch input and a real phone browser; print. Residual cosmetic point: on the hidden-label chart the «الخط 5» label sits
close to line 2's end at 390 px (readable).
