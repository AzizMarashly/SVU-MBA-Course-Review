# -*- coding: utf-8 -*-
"""Stage 1: extract the textbook with PyMuPDF into ../extracted/book/ (same layout as PRM).
The book's font emits the lam-alef ligature reversed («األ» for «الأ», «اال» for «الا», «اإل» for «الإ»,
«اآل» for «الآ»); fixed at character level. Also writes the TOC (pages 2-8) as toc_raw.txt and
the per-chapter files ch_fixed/chNN.txt with "=== PAGE n ===" markers, for the in-scope chapters.
Usage (from render/): set PYTHONUTF8=1 && python extract_book.py
"""
import os, re, json, sys
import pymupdf
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE); COURSE = os.path.dirname(WORK)
BOOK = os.path.join(COURSE, "Dr Iyad Zoukar - MBA - MIS - The Book.pdf")
OUT = os.path.join(WORK, "extracted", "book"); os.makedirs(os.path.join(OUT, "ch_fixed"), exist_ok=True)
CH_PAGES = {1: (10, 47), 2: (48, 93), 3: (94, 131), 4: (132, 183), 5: (184, 222), 6: (223, 262),
            7: (263, 295), 8: (296, 334), 9: (335, 376), 10: (377, 424), 11: (425, 461), 12: (462, 507)}
SCOPE = [1, 2, 3, 5, 7, 8, 9, 10]

def fix(t):
    return re.sub("ا([أإآا])ل", r"ال\1", t)

doc = pymupdf.open(BOOK)
pages = [fix(p.get_text()) for p in doc]
mism = []
for i, t in enumerate(pages, 1):
    m = re.search(r"-\s*(\d+)\s*-", t[:200])
    if not m or int(m.group(1)) != i: mism.append(i)
with open(os.path.join(OUT, "book_fixed.txt"), "w", encoding="utf-8", newline="\n") as f:
    for i, t in enumerate(pages, 1): f.write(f"\n=== PAGE {i} ===\n{t}\n")
with open(os.path.join(OUT, "toc_raw.txt"), "w", encoding="utf-8", newline="\n") as f:
    for i in range(2, 9): f.write(f"\n=== PAGE {i} ===\n{pages[i-1]}\n")
for n in SCOPE:
    a, b = CH_PAGES[n]
    with open(os.path.join(OUT, "ch_fixed", f"ch{n:02d}.txt"), "w", encoding="utf-8", newline="\n") as f:
        for i in range(a, b + 1): f.write(f"\n=== PAGE {i} ===\n{pages[i-1]}\n")
print("pages", len(pages), "| printed-number mismatches (first 200 chars):", len(mism), mism[:20])
print("chapter files:", SCOPE)
