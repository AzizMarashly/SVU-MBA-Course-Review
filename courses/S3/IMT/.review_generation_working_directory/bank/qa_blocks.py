# -*- coding: utf-8 -*-
"""Mechanical answer-block checks (§15) over bank.json."""
import json, re, os, sys, random, collections
b = json.load(open(os.path.join(os.path.dirname(__file__), "..", "bank.json"), encoding="utf-8"))
qs = b["questions"]
def words(s): return len(re.findall(r"\S+", re.sub(r"\*\*", "", s or "")))
def block_words(q):
    ans = q["ans"] if isinstance(q["ans"], str) else q["options"][q["ans"]]
    core = words(ans) + words(q["why"]) + words(q["remember"]) + words(q["distractors"]) + 6
    return core
lens = [block_words(q) for q in qs]
over = [(q["id"], block_words(q)) for q in qs if block_words(q) > 80 and not (q["reconstructed"] or q["book_says"] or q["other_source"] or q["sci"] or q["qtype"]=="essay")]
under = [(q["id"], block_words(q)) for q in qs if block_words(q) < 40]
print("avg block words (core lines):", round(sum(lens)/len(lens),1), "| min", min(lens), "| max", max(lens))
print("blocks > 80 words without justification (optional line/reconstruction/essay):", len(over))
for o in over[:40]: print("  ", o)
print("blocks < 40 words:", len(under), under[:15])
# why must not repeat answer text verbatim; must not start with 'الإجابة الصحيحة'
bad_why = [q["id"] for q in qs if q["why"].startswith("الإجابة الصحيحة") or q["why"].startswith("الجواب")]
print("why starting with 'الإجابة الصحيحة':", bad_why)
rep = []
for q in qs:
    if q["qtype"]=="mcq":
        a = q["options"][q["ans"]]
        if len(a) > 12 and a in q["why"]: rep.append(q["id"])
print("why repeating full answer text:", rep)
print("remember without bold:", [q["id"] for q in qs if "**" not in q["remember"]])
print("bold in stem/options:", [q["id"] for q in qs if "**" in q["stem"] or (q["options"] and any("**" in o for o in q["options"]))])
print("low_conf without reason:", [q["id"] for q in qs if q["low_conf"] is not None and len(q["low_conf"]) < 10])
print("reconstructed without original:", [q["id"] for q in qs if q["reconstructed"] and not q["original"]])
print("generated importance >1:", [q["id"] for q in qs if "generated" in q["types"] and q["importance"]>1])
print("importance >5:", [q["id"] for q in qs if q["importance"]>5])
# recompute importance independently
foc = set(tuple(x) for x in b["focus_areas"])
def sc(q):
    if "generated" in q["types"]: return 1
    n=len(q["exam_sources"]); base=1 if n==0 else 2 if n==1 else 3 if n==2 else 4
    return min(5, base + (1 if "textbook" in q["types"] else 0) + (1 if (q["ch"],q["sub"]) in foc else 0))
print("importance mismatches:", [q["id"] for q in qs if sc(q)!=q["importance"]])
print("freq mismatches:", [q["id"] for q in qs if q["freq"] != (0 if "generated" in q["types"] else len(q["sources"]))])
print("leftover literal ** count in stems:", sum(q["stem"].count("**") for q in qs))
random.seed(7); sample = random.sample(qs, 20)
print("RANDOM SAMPLE IDS:", [q["id"] for q in sample])
