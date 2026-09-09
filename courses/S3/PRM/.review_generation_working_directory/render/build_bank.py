# -*- coding: utf-8 -*-
"""PRM: assemble all chapter files into one verified bank (JSON, UTF-8 no BOM), compute focus areas,
importance scores, coverage audit and mechanical checks."""
import importlib, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import meta_prm as M
CHAPTERS = M.CHAPTERS
SPEC = "v0.9"
VERSION = open(os.path.join(os.path.dirname(__file__), "..", "VERSION"), encoding="utf-8").read().strip()
LEDGER = json.load(open(os.path.join(os.path.dirname(__file__), "..", "ledger.json"), encoding="utf-8"))
EXAM_CODES = {e["id"] for e in LEDGER["sources"] if e.get("kind") == "exam" and e["decision"].startswith("included")}

def load():
    subs, qs = {}, []
    global CHAPTERS
    present = []
    for n in CHAPTERS:
        try:
            m = importlib.import_module(f"bank_ch{n:02d}")
        except ModuleNotFoundError:
            print("WARNING: bank_ch%02d.py missing — partial build" % n); continue
        subs[n] = dict(m.SUBS); qs += list(m.QS); present.append(n)
        M.OPENERS[n] = tuple(m.OPENER)
    CHAPTERS = present
    try:
        ex = importlib.import_module("bank_extra"); qs += list(ex.QS)
    except ModuleNotFoundError:
        pass
    return subs, qs

OTHER_CODES = {"EMAD", "MURAJA"}

# Cross-chapter duplicates found by the stem scan (stage 5, owner decision): the same exam item was routed to two
# chapters by different helpers. keep <- drop: sources are merged, the dropped id disappears from the bank.
MERGES = {"Q04-013": "Q07-006", "Q07-005": "Q04-012", "Q03-012": "Q05-005", "Q07-007": "Q06-007"}

def merge_duplicates(qs):
    byid = {q["id"]: q for q in qs}
    for drop, keep in MERGES.items():
        d, k = byid[drop], byid[keep]
        for c in d["sources"]:
            if c not in k["sources"]: k["sources"].append(c)
        k["variants"] = list(k["variants"]) + [f"{'/'.join(d['sources'])} (كان {drop}): {d['stem'][:120]}"] + list(d["variants"])
        k["pages"] = sorted(set(k["pages"]) | set(d["pages"]))
        if d["low_conf"] and not k["low_conf"]: k["low_conf"] = d["low_conf"]
    return [q for q in qs if q["id"] not in MERGES]

def normalise_types(qs):
    """types are derived from the sources so every chapter file follows the same rule:
    exam <=> an exam sitting has it; textbook <=> BOOK; other <=> EMAD/MURAJA; ASEM is a cross-check only."""
    for q in qs:
        if "generated" in q["types"]:
            continue
        q["exam_sources"] = [c for c in q["sources"] if c in EXAM_CODES]
        t = []
        if q["exam_sources"]: t.append("exam")
        if "BOOK" in q["sources"]: t.append("textbook")
        if set(q["sources"]) & OTHER_CODES: t.append("other")
        assert t, (q["id"], "no usable source", q["sources"])
        q["types"] = t

def check_basic(qs, subs):
    ids = [q["id"] for q in qs]
    dup = [i for i,c in collections.Counter(ids).items() if c>1]
    assert not dup, f"duplicate ids {dup}"
    for q in qs:
        assert q["ch"] in CHAPTERS, q["id"]
        assert q["sub"] in subs[q["ch"]], (q["id"], q["sub"])
        assert q["pages"], q["id"]
        assert q["why"] and q["remember"], q["id"]
        assert "**" in q["remember"], (q["id"], "remember needs bold")
        
        assert set(q["exam_sources"]) <= EXAM_CODES, q["id"]
        assert set(q["exam_sources"]) <= set(q["sources"]), q["id"]
        if "generated" in q["types"]:
            assert q["sources"] == ["GEN"] and not q["exam_sources"], q["id"]
        else:
            assert "exam" in q["types"] or "textbook" in q["types"] or "other" in q["types"], q["id"]
            assert ("exam" in q["types"]) == bool(q["exam_sources"]), q["id"]
            assert ("textbook" in q["types"]) == ("BOOK" in q["sources"]), q["id"]
        # no bold in stem/options
        assert "**" not in q["stem"], q["id"]
        if q["options"]:
            assert all("**" not in o for o in q["options"]), q["id"]
        if q["qtype"] == "mcq":
            assert isinstance(q["ans"], int) and 0 <= q["ans"] < len(q["options"]), q["id"]
        if q["qtype"] == "tf":
            assert q["ans"] in ("صح","خطأ"), q["id"]

def focus_areas(qs, subs):
    """per subsection: distinct questions by origin. Rank by exam count then total."""
    tab = {}
    for n, d in subs.items():
        for s, name in d.items():
            tab[(n,s)] = dict(ch=n, sub=s, name=name, exam=0, textbook=0, other=0, generated=0, total=0)
    for q in qs:
        k = (q["ch"], q["sub"])
        if "generated" in q["types"]:
            tab[k]["generated"] += 1
        else:
            if "exam" in q["types"]: tab[k]["exam"] += 1
            if "textbook" in q["types"]: tab[k]["textbook"] += 1
            if "other" in q["types"]: tab[k]["other"] += 1
            tab[k]["total"] += 1
    rows = sorted(tab.values(), key=lambda r: (-r["exam"], -r["total"]))
    # focus areas: per chapter, subsections with exam>=2, or the top-2 by (exam,total) if they have exam>=1
    focus = set()
    for n in CHAPTERS:
        ch_rows = [r for r in rows if r["ch"]==n]
        top = [r for r in ch_rows if r["exam"] >= 2]
        if len(top) < 2:
            top = [r for r in ch_rows if r["exam"] >= 1][:2]
        for r in top: focus.add((r["ch"], r["sub"]))
    return rows, focus

def score(q, focus):
    if "generated" in q["types"]:
        return 1
    n = len(q["exam_sources"])
    base = 1 if n == 0 else 2 if n == 1 else 3 if n == 2 else 4
    bonus = (1 if "textbook" in q["types"] else 0) + (1 if (q["ch"], q["sub"]) in focus else 0)
    return min(5, base + bonus)

def coverage(qs, subs):
    covered, mentioned = collections.defaultdict(set), collections.defaultdict(set)
    for q in qs:
        covered[q["ch"]].add(q["sub"])
    # "mentioned in explanations": subsection name tokens appearing in why/remember of other questions
    res = {}
    for n, d in subs.items():
        rows = []
        for s, name in d.items():
            direct = s in covered[n]
            direct_real = any(q["ch"]==n and q["sub"]==s and "generated" not in q["types"] for q in qs)
            rows.append(dict(sub=s, name=name, covered=direct, covered_by_real=direct_real,
                             covered_by_generated=(direct and not direct_real)))
        res[n] = rows
    return res

def main():
    subs, qs = load()
    qs = merge_duplicates(qs)
    normalise_types(qs)
    check_basic(qs, subs)
    rows, focus = focus_areas(qs, subs)
    for q in qs:
        q["importance"] = score(q, focus)
        q["freq"] = 0 if "generated" in q["types"] else len(q["sources"])
        q["focus"] = (q["ch"], q["sub"]) in focus
        q["subname"] = subs[q["ch"]][q["sub"]]
    cov = coverage(qs, subs)
    uncovered = [(n, r["sub"], r["name"]) for n in CHAPTERS for r in cov[n] if not r["covered"]]
    total_subs = sum(len(v) for v in subs.values())
    print("questions:", len(qs), "| subsections:", total_subs, "| uncovered:", len(uncovered))
    for u in uncovered: print("  UNCOVERED", u)
    byg = sum(1 for n in CHAPTERS for r in cov[n] if r["covered_by_generated"])
    print("covered only by generated:", byg)
    print("type counts:", collections.Counter(t for q in qs for t in q["types"]))
    print("per chapter:", {n: sum(1 for q in qs if q["ch"]==n) for n in CHAPTERS})
    gen = sum(1 for q in qs if "generated" in q["types"]); real = len(qs)-gen
    print(f"generated {gen} vs real {real} ({gen/len(qs):.1%} of bank)")
    for n in CHAPTERS:
        g = sum(1 for q in qs if q["ch"]==n and "generated" in q["types"]); r = sum(1 for q in qs if q["ch"]==n)-g
        if g > r: print("  WARNING generated>real in ch", n)
    print("importance:", collections.Counter(q["importance"] for q in qs))
    print("low_conf:", sum(1 for q in qs if q["low_conf"]))
    print("reconstructed:", sum(1 for q in qs if q["reconstructed"]))
    print("focus areas:", sorted(focus))
    ledger = LEDGER["sources"]
    chapter_map = json.load(open(os.path.join(os.path.dirname(__file__), "..", "chapter_map.json"), encoding="utf-8"))
    notice = [f"Generated with the SVU MBA Course Review Generator, prompt {SPEC} · deliverable v{VERSION}",
              "Source and latest version: https://github.com/AzizMarashly/SVU-MBA-Course-Review",
              "Licence of the prompt and of this file: CC BY-NC-SA 4.0 — share freely, credit the source, never sell. Quoted textbook and exam content stays with its owners and is not covered."]
    out = dict(_notice=notice, spec_version=SPEC, file_version=VERSION, title=M.TITLE, generated=M.GENERATED_DATE,
               source_ledger=ledger, chapter_map=chapter_map,
               course=M.COURSE,
               chapters_in_scope=M.CHAPTERS, openers={n: list(v) for n, v in M.OPENERS.items()}, subsections=subs, questions=qs,
               focus_table=rows, focus_areas=sorted([list(f) for f in focus]), coverage=cov)
    return out

if __name__ == "__main__":
    out = main()
    dst = os.path.join(os.path.dirname(__file__), "..", "bank.json")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", dst)
