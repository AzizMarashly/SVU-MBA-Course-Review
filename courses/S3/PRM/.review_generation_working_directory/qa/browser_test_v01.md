# Browser test — v01 (§15 HTML), 2026-09-09, Chrome, served over http://127.0.0.1 (file:// is blocked by the automation tool)

Desktop (1394 px): root dir=rtl; 442 questions; all answers closed on load; 14/14 chapters and 51/51 sections open on load;
the three end-of-file `<details>` lists (source files, most repeated, highest importance) closed; single reveal opens one answer
only and the control label switches show/hide; modes exam 166 / textbook 145 / other 187 / generated 21 — each equals a manual
count of `data-section`; importance ≥5 → 7 (= bank count 7); importance ≥2 hides all generated; repetition slider max 5 → 1
question (Q10-001, freq 5); repetition ≥3 → 21 (= bank); combined exam + ch.8 + ★3+ → 26 (= manual count), badge "3";
Reset returns 442 / imp 1 / freq 0 / all chapters / mode all; collapse-all chapters closes 14 without opening any answer;
search «مونتي كارلو» → 2 hits (Q08-023, Q08-029) with their collapsed chapter and section opened; theme toggle light/dark
(background changes); no literal ** in rendered text; 589 source labels, 0 broken; licence notice present with v0.9 / v01;
14 openers, each 2 lines, each before the first question of its chapter. Reload: mode exam, ★3+, chapter 10 and the folded
chapter 1 all survived (localStorage + URL hash).
Phone (390 px iframe, qa/phone_test.html): panel closed by default with no stored preference; aria-expanded=false;
badge "3" and summary «الامتحانات · ★3+ · الفصل 10» shown next to the counter; Filters button opens (display flex) and
closes it; panel state (open, then closed) survives a reload; smallest touch target 44 px; slider width 219 px (full row);
no horizontal scroll. Filename/cover/metadata all say v01.
Not tested: printing, screen readers, a real phone device.
