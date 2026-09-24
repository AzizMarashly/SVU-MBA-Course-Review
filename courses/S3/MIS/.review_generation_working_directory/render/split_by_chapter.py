# -*- coding: utf-8 -*-
"""Stage 3 -> 5: split every transcribed item by ch_guess into ../extracted/questions/by_chapter/chNN.json
(in-scope chapters; the rest go to out_of_scope.json). Usage (from render/): set PYTHONUTF8=1 && python split_by_chapter.py"""
import os, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); Q = os.path.join(HERE, "..", "extracted", "questions")
OUT = os.path.join(Q, "by_chapter"); os.makedirs(OUT, exist_ok=True)
SCOPE = {1, 2, 3, 5, 7, 8, 9, 10}
by = collections.defaultdict(list); oos = []; n = 0
for f in sorted(glob.glob(os.path.join(Q, "*.json"))):
    grp = os.path.basename(f)[:-5]
    for i, it in enumerate(json.load(open(f, encoding="utf-8"))):
        it = dict(it); it["raw_id"] = f"{grp}#{i}"; n += 1
        ch = it.get("ch_guess")
        if ch in SCOPE: by[ch].append(it)
        else: oos.append(it)
for ch, items in by.items():
    json.dump(items, open(os.path.join(OUT, f"ch{ch:02d}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(oos, open(os.path.join(OUT, "out_of_scope.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("raw items:", n, "| per chapter:", {c: len(v) for c, v in sorted(by.items())}, "| out of scope / unassigned:", len(oos))
print("by code per chapter:", {c: dict(collections.Counter(i.get("code") for i in v)) for c, v in sorted(by.items())})
