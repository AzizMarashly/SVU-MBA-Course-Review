# -*- coding: utf-8 -*-
"""Mechanical answer-block checks (§15) over bank.json — ACM, prompt v0.12."""
import json, re, os, sys, random, collections, unicodedata
b = json.load(open(os.path.join(os.path.dirname(__file__), "..", "bank.json"), encoding="utf-8"))
qs = b["questions"]
def words(s): return len(re.findall(r"\S+", re.sub(r"\*\*", "", s or "")))
def block_words(q):
    ans = q["ans"] if isinstance(q["ans"], str) else q["options"][q["ans"]]
    return words(ans) + words(q["why"]) + words(q["remember"]) + words(q["distractors"]) + 6
lens = [block_words(q) for q in qs]
over = [(q["id"], block_words(q)) for q in qs if block_words(q) > 80 and not (q["reconstructed"] or q["book_says"] or q["other_source"] or q["sci"] or q["qtype"]=="essay" or q.get("calc"))]
under = [(q["id"], block_words(q)) for q in qs if block_words(q) < 40]
print("avg block words (core lines):", round(sum(lens)/len(lens),1), "| min", min(lens), "| max", max(lens))
print("blocks > 80 words without justification (optional line/reconstruction/essay/calc):", len(over))
for o in over[:40]: print("  ", o)
print("blocks < 40 words:", len(under), under[:15])
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
print("reconstructed without original / not 4 options:", [q["id"] for q in qs if q["reconstructed"] and (not q["original"] or len(q["options"]) != 4)])
print("reconstructed with synonym-looking option pairs (shared 3+ words):", [q["id"] for q in qs if q["reconstructed"] and any(len(set(a.split()) & set(b_.split())) >= 3 for i, a in enumerate(q["options"]) for b_ in q["options"][i+1:])])
print("essays without model answer:", [q["id"] for q in qs if q["qtype"] == "essay" and not q.get("model_answer")])
print("model answers without a page reference (ص N):", [q["id"] for q in qs if q.get("model_answer") and not re.search(r"ص\s*\d+", q["model_answer"])])
print("fast routes without a page:", [q["id"] for q in qs if q.get("fast") and not re.search(r"ص\s*\d+", q["fast"])])
print("records without a claim:", [q["id"] for q in qs if not q.get("claim")])
print("generated importance >1:", [q["id"] for q in qs if "generated" in q["types"] and q["importance"]>1])
print("importance >5:", [q["id"] for q in qs if q["importance"]>5])
foc = set(tuple(x) for x in b["focus_areas"])
def sc(q):
    if "generated" in q["types"]: return 1
    n=len(q.get("union_exam", q["exam_sources"])); base=1 if n==0 else 2 if n==1 else 3 if n==2 else 4
    inf = any(tuple(u) in foc for u in q.get("union_units", [(q["ch"], q["sub"])]))
    return min(5, base + (1 if q.get("union_textbook", "textbook" in q["types"]) else 0) + (1 if inf else 0))
print("importance mismatches:", [q["id"] for q in qs if sc(q)!=q["importance"]])
print("freq mismatches:", [q["id"] for q in qs if q["freq"] != (0 if "generated" in q["types"] else len(q.get("union_sources", q["sources"])))])
byid = {q["id"]: q for q in qs}
print("see-links with different score:", [q["id"] for q in qs for s in q.get("see", []) if byid[s]["importance"] != q["importance"] or byid[s]["freq"] != q["freq"]])
# ordering (§10c) inside every section of every chapter
bad_order = []
for ch in sorted({q["ch"] for q in qs}):
    for sec in ("exam", "textbook", "other", "generated"):
        seq = sorted([q for q in qs if q["ch"] == ch and sec in q["types"]], key=lambda q: (-q["importance"], -q["freq"], 0 if q["qtype"]=="mcq" else 1, q["id"]))
        for a, b_ in zip(seq, seq[1:]):
            if (a["importance"], a["freq"]) < (b_["importance"], b_["freq"]): bad_order.append((ch, sec, a["id"], b_["id"]))
print("ordering violations:", bad_order)
# §7d / §7e
tab = [q["id"] for q in qs if q.get("table")]; calc = [q["id"] for q in qs if q.get("calc")]
print("records with a data table:", len(tab), "| with a calculation block:", len(calc), "| with an answer table:", sum(1 for q in qs if q.get("ans_table")),
      "| with a figure:", sum(1 for q in qs if q.get("fig")), "| with a fast route:", sum(1 for q in qs if q.get("fast")), "| unsolved exercises solved:", sum(1 for q in qs if q.get("unsolved")))
print("stems that still look tabular (no table field, 3+ ';'-separated groups, 8+ digits):",
      [q["id"] for q in qs if not q.get("table") and len(re.findall(r"[؛;]\s*\S+[:،|]", q["stem"])) >= 3 and len(re.findall(r"\d", q["stem"])) >= 8])
print("numeric answers without a calc block:", [q["id"] for q in qs if not q.get("calc") and q["qtype"] == "mcq" and re.fullmatch(r"[\d.,\s]+(ل\.س|وحدة|%)?", q["options"][q["ans"]] or "") and "generated" not in q["types"]])
print("numeric why without a calc block (3+ '=' signs):", [q["id"] for q in qs if not q.get("calc") and q["why"].count("=") >= 3])
print("calc blocks whose why still carries the arithmetic (2+ '=' signs):", [q["id"] for q in qs if q.get("calc") and q["why"].count("=") >= 2])
print("calc cells with Arabic letters in eq/sub:", [q["id"] for q in qs if q.get("calc") and any(re.search(r"[؀-ۿ]", st["eq"] + st["sub"]) for st in q["calc"]["steps"])])
meth = b.get("methods", {})
print("procedural chapters (Methods block):", {k: [m["key"] for m in v] for k, v in meth.items() if v})
print("calc blocks without a method in a procedural chapter:", [q["id"] for q in qs if q.get("calc") and meth.get(str(q["ch"])) and not q["calc"].get("method")])
import importlib
sys.path.insert(0, os.path.dirname(__file__))
_meta = importlib.import_module("meta_acm")
_missing = set()
for q in qs:
    _texts = []
    for t in (q.get("table"), q.get("ans_table")):
        if t: _texts.append(" ".join(map(str, t["head"])))
    if q.get("calc"): _texts += q["calc"]["given"] + [st["eq"] + " " + st["what"] for st in q["calc"]["steps"]]
    for tok in re.findall(r"(?<![A-Za-z])([A-Z][A-Za-z]{1,4})(?![A-Za-z])", " ".join(_texts)):
        if tok not in _meta.SYMBOLS and not re.fullmatch(r"[A-Z]\d*|X\d+|M\d+", tok): _missing.add(tok)
print("symbols used in tables/calc but missing from SYMBOLS:", sorted(_missing))
print("glossary entries without a numeric example:", [k for k, v in _meta.SYMBOLS.items() if not v.get("ex")])
print("leftover literal ** count in stems:", sum(q["stem"].count("**") for q in qs))
random.seed(7); sample = random.sample(qs, min(20, len(qs)))
print("RANDOM SAMPLE IDS:", [q["id"] for q in sample])
# §11d / §15: the "Source files" appendix must list exactly the files in the course folder
import render_html
PROJ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
disk = set()
for root, dirs, files in os.walk(PROJ):
    dirs[:] = [d for d in dirs if d not in (".review_generation_working_directory", "_old_versions", "archive")]
    for f in files:
        if f.endswith(".md") or re.match(r".*_v\d+\.\d+(\.html|\.pdf|\.docx)$", f): continue
        disk.add(unicodedata.normalize("NFC", os.path.relpath(os.path.join(root, f), PROJ).replace("\\", "/")))
listed = set(unicodedata.normalize("NFC", row[1]) for row in render_html.FILES)
print("source appendix rows:", len(listed), "| files on disk:", len(disk))
print("  on disk but not in appendix:", sorted(disk - listed))
print("  in appendix but not on disk:", sorted(listed - disk))
print("  question source labels without a row:", sorted({s for q in qs for s in q["sources"] if s != "GEN" and s not in render_html.SRC_ROW}))
print("  appendix summary files == rows:", render_html.FILES_SUMMARY["files"] == len(render_html.FILES))
