# -*- coding: utf-8 -*-
"""MIS: assemble all chapter files into one verified bank (JSON, UTF-8 no BOM), compute focus areas,
importance scores, coverage audit (also written to ../coverage.md) and mechanical checks. Adapted from PRM."""
import importlib, json, os, re, sys, collections, unicodedata, math, itertools
sys.path.insert(0, os.path.dirname(__file__))
import meta_mis as M
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, "..")
CHAPTERS = M.CHAPTERS
SPEC = "v0.11"   # v0.10 run; the tooling carries v0.11 §7d (no MIS record needs a table or calculation)
VERSION = open(os.path.join(WORK, "VERSION"), encoding="utf-8").read().strip()
LEDGER = json.load(open(os.path.join(WORK, "ledger.json"), encoding="utf-8"))
EXAM_CODES = {e["id"] for e in LEDGER["sources"] if e.get("kind") == "exam" and e["decision"].startswith("included")}
assert EXAM_CODES == M.EXAM_CODES, (EXAM_CODES, M.EXAM_CODES)
OTHER_CODES = M.OTHER_CODES
SUBS_ALL = json.load(open(os.path.join(WORK, "extracted", "book", "subsections.json"), encoding="utf-8"))["units"]

def load():
    subs, qs = {}, []
    global CHAPTERS
    present = []
    for n in CHAPTERS:
        try:
            m = importlib.import_module(f"bank_ch{n:02d}")
        except ModuleNotFoundError:
            print("WARNING: bank_ch%02d.py missing — partial build" % n); continue
        subs[n] = {code: getattr(m, "SUBS", {}).get(code) or u["name"] for code, u in SUBS_ALL[str(n)].items()}
        qs += list(m.QS); present.append(n)
        M.OPENERS[n] = tuple(m.OPENER)
    CHAPTERS = present
    try:
        ex = importlib.import_module("bank_extra"); qs += list(ex.QS)
    except ModuleNotFoundError:
        pass
    return subs, qs

# Cross-chapter consolidation (v1.0, prompt idea I-11): true duplicates only — same claim of the book, same expected
# answer, same form. keep <- drop; the kept record is the exam item, in the chapter that owns the book page.
# Log with reasons and pages: ../qa/consolidation_v1.0.md.
MERGES = {
    "Q07-013": "Q01-002",   # business model definition, p. 20 (ch-7 review MCQ 2 = R44 «تعريف نموذج العمل»)
    "Q10-020": "Q05-024",   # data warehouse is not the small store (that is the data mart), T/F, pp. 206–207
    "Q09-011": "Q01-013",   # organizational and management capital definition, pp. 35, 341
    "Q03-020": "Q01-009",   # organizational culture = the basic assumptions accepted by members, p. 29
}

def _join(a, b, sep=" | "):
    return sep.join(x for x in (a, b) if x) or None

def merge_duplicates(qs):
    """Union sources/pages/raw ids/legacy ids, dropped wording becomes a variant, flags and notes kept from both;
    freq is later len(sources), i.e. the size of the source union (never a sum)."""
    byid = {q["id"]: q for q in qs}
    for drop, keep in MERGES.items():
        d, k = byid[drop], byid[keep]
        for c in d["sources"]:
            if c not in k["sources"]: k["sources"].append(c)
        ans = d["options"][d["ans"]] if d["qtype"] == "mcq" else d["ans"]
        k["variants"] = list(k["variants"]) + [f"{'/'.join(c for c in d['sources'] if c != 'ASM')} (كان {drop}): {d['stem']} — {ans}"] + list(d["variants"])
        k["pages"] = sorted(set(k["pages"]) | set(d["pages"]))
        k["raw"] = list(dict.fromkeys(k.get("raw", []) + d.get("raw", [])))
        k["reconstructed"] = k["reconstructed"] or (d["reconstructed"] and k["qtype"] == "mcq")
        for f in ("original", "low_conf", "book_says", "other_source", "notes"):
            k[f] = _join(k[f], d[f])
        if d.get("legacy_id"): k["legacy_id"] = "+".join(x for x in [k.get("legacy_id"), d["legacy_id"]] if x)
    return [q for q in qs if q["id"] not in MERGES]

# Duplicate checks (I-11). Tokens: normalised words without stop words and the article; tf-idf cosine.
DUP_STOP = set("في من على الى عن ان او و ما هو هي هذا هذه التي الذي كل يلي ذلك تلك بين مع لا قد كان تكون يكون يتم عند التاليه التالي ليس هل مثل له لها به بها".split())
def toks(t):
    out = []
    for w in re.sub(r"[^\w\s]", " ", norm(t)).split():
        for p in ("وال", "بال", "كال", "فال", "لل", "ال"):
            if w.startswith(p) and len(w) - len(p) >= 3: w = w[len(p):]; break
        if w not in DUP_STOP and len(w) > 1: out.append(w)
    return out

def vectors(docs):
    df = collections.Counter(t for d in docs for t in set(d)); n = len(docs); out = []
    for d in docs:
        v = {t: (1 + math.log(c)) * math.log((n + 1) / (df[t] + 1)) for t, c in collections.Counter(d).items()}
        z = math.sqrt(sum(x * x for x in v.values())) or 1; out.append({t: x / z for t, x in v.items()})
    return out
cos = lambda a, b: sum(x * b.get(t, 0) for t, x in a.items())

def answer_text(q):
    return q["options"][q["ans"]] if q["qtype"] == "mcq" else str(q["ans"])

# Pairs read by hand in the consolidation pass: same option set and similar stem, different answer on purpose.
DUP_ALLOW = {("Q10-001", "Q10-002")}   # definitions of unstructured vs structured decisions, same three options, p. 379

def check_duplicates(qs):
    """Hard: (1) same normalised option set + stem cosine >= 0.6 + different correct answer; (2) a raw source-item id
    used by two records. Warning: each record's top-3 cross-chapter neighbours above the union threshold
    (stem >= 0.40 or full record >= 0.40 or bold terms >= 0.45)."""
    bold = lambda s: " ".join(re.findall(r"\*\*(.+?)\*\*", s or ""))
    fact = lambda q: q["stem"] if q["qtype"] == "tf" else answer_text(q)[:400]
    Vq = vectors([toks(q["stem"]) for q in qs])
    Vs = vectors([toks(q["stem"]) + (toks(fact(q)) if q["qtype"] != "tf" else []) for q in qs])
    Vf = vectors([toks(q["stem"] + " " + fact(q) + " " + q["why"] + " " + q["remember"]) for q in qs])
    Vb = vectors([toks(bold(q["why"]) + " " + bold(q["remember"])) for q in qs])
    optset = lambda q: frozenset(norm(o) for o in q["options"]) if q["qtype"] == "mcq" else frozenset(("صح", "خطا")) if q["qtype"] == "tf" else None
    errors, near = [], collections.defaultdict(list)
    for i, j in itertools.combinations(range(len(qs)), 2):
        a, b = qs[i], qs[j]
        if optset(a) and optset(a) == optset(b) and cos(Vq[i], Vq[j]) >= 0.6 \
                and norm(answer_text(a)) != norm(answer_text(b)) and (a["id"], b["id"]) not in DUP_ALLOW:
            errors.append(f"same options, similar stem ({cos(Vq[i], Vq[j]):.2f}), different answer: {a['id']} / {b['id']}")
        if a["ch"] != b["ch"]:
            s, f, bd = cos(Vs[i], Vs[j]), cos(Vf[i], Vf[j]), cos(Vb[i], Vb[j])
            if s >= 0.40 or f >= 0.40 or bd >= 0.45:
                for x, y in ((a, b), (b, a)): near[x["id"]].append((max(s, f, bd), y["id"], s, f, bd))
    used = collections.defaultdict(list)
    for q in qs:
        for r in q.get("raw", []): used[r].append(q["id"])
    base = collections.defaultdict(set)
    for r, ids in used.items():
        if len(ids) > 1: errors.append(f"raw item {r} used by {ids}")
        base[r.split("@")[0]].add(r)
    for b0, forms in base.items():
        if len(forms) > 1 and b0 in forms: errors.append(f"raw item {b0} used whole and as sub-questions {sorted(forms)}")
    lacking = [q["id"] for q in qs if not q.get("raw") and "generated" not in q["types"]]
    print(f"duplicate check: {len(near)} records with cross-chapter neighbours above the union threshold (warning, read in the consolidation pass):")
    for k in sorted(near):
        print("  ", k, "->", ", ".join(f"{y} (stem {s:.2f} / full {f:.2f} / bold {bd:.2f})" for _, y, s, f, bd in sorted(near[k], reverse=True)[:3]))
    print(f"raw source-item ids: {len(qs) - len(lacking) - sum('generated' in q['types'] for q in qs)} records declare them, {len(lacking)} real records do not yet")
    assert not errors, "duplicate check failed:" + "".join("\n  " + e for e in errors)

def normalise_types(qs):
    """types derive from sources: exam <=> an exam sitting has it; textbook <=> BOOK; other <=> OQ1..OQ5; ASM is a cross-check only."""
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

OUTSIDE = []
def check_basic(qs, subs):
    ids = [q["id"] for q in qs]
    dup = [i for i, c in collections.Counter(ids).items() if c > 1]
    assert not dup, f"duplicate ids {dup}"
    known = set(M.SRC_NAMES)
    for q in qs:
        assert q["ch"] in CHAPTERS, q["id"]
        assert q["sub"] in subs[q["ch"]], (q["id"], q["sub"])
        assert q["pages"] and all(isinstance(p, int) and 1 <= p <= M.BOOK_PAGES for p in q["pages"]), (q["id"], q["pages"])
        if not all(M.CH_PAGES[q["ch"]][0] <= p <= M.CH_PAGES[q["ch"]][1] for p in q["pages"]):
            OUTSIDE.append((q["id"], q["pages"]))
        assert q["why"] and q["remember"], q["id"]
        assert "**" in q["remember"], (q["id"], "remember needs bold")
        assert set(q["sources"]) <= known, (q["id"], q["sources"])
        assert set(q["exam_sources"]) <= EXAM_CODES, q["id"]
        assert set(q["exam_sources"]) <= set(q["sources"]), q["id"]
        if "generated" in q["types"]:
            assert q["sources"] == ["GEN"] and not q["exam_sources"], q["id"]
        else:
            assert "exam" in q["types"] or "textbook" in q["types"] or "other" in q["types"], q["id"]
            assert ("exam" in q["types"]) == bool(q["exam_sources"]), q["id"]
            assert ("textbook" in q["types"]) == ("BOOK" in q["sources"]), q["id"]
        assert "**" not in q["stem"], q["id"]
        if "|" in q["stem"] or chr(10) in q["stem"]:
            if os.environ.get("PRM_LENIENT"): print("WARNING (lenient):", q["id"], "tabular stem")
            else: raise AssertionError((q["id"], "tabular data belongs in table=T(...), not in the stem (§7d)"))
        if q["options"]:
            assert all("**" not in o for o in q["options"]), q["id"]
        if q["qtype"] == "mcq":
            assert isinstance(q["ans"], int) and 0 <= q["ans"] < len(q["options"]), q["id"]
        if q["qtype"] == "tf":
            assert q["ans"] in ("صح", "خطأ"), q["id"]
        if q["reconstructed"]:
            assert q["original"] and q["qtype"] == "mcq", (q["id"], "reconstructed needs original + mcq")

def focus_areas(qs, subs):
    """per subsection: distinct questions by origin. Rank by exam count then total.
    Focus areas per chapter: units with >= 2 exam sources' questions... (rule as PRM: exam>=2, else top-2 with exam>=1)."""
    tab = {}
    for n, d in subs.items():
        for s, name in d.items():
            tab[(n, s)] = dict(ch=n, sub=s, name=name, exam=0, textbook=0, other=0, generated=0, total=0)
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
    focus = set()
    for n in CHAPTERS:
        ch_rows = [r for r in rows if r["ch"] == n]
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

def norm(t):
    t = unicodedata.normalize("NFKC", t or "")
    t = re.sub(r"[ً-ْـ]", "", t)
    t = t.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"\s+", " ", t).lower()

STOP = {"نظم", "نظام", "المعلومات", "في", "من", "على", "ما", "هي", "هو", "و", "أو", "مع", "الى", "إلى", "كيف", "ال", "التي", "الذي", "لماذا", "أنواع", "أنظمة", "أمثلة", "قيمة", "دور", "إدارة", "المؤسسة", "المؤسسات", "الأعمال", "التجارية", "الرئيسة"}
def coverage(qs, subs):
    """§9: a unit is covered when a question is assigned to it (its text/options/answer test it — the helper's
    assignment); 'mentioned' = the unit's name keywords appear only inside why/remember of questions of other units."""
    res = {}
    for n, d in subs.items():
        rows = []
        chq = [q for q in qs if q["ch"] == n]
        for s, name in d.items():
            mine = [q for q in chq if q["sub"] == s]
            real = [q for q in mine if "generated" not in q["types"]]
            kws = [norm(w) for w in re.split(r"[\s:،؛,()/–-]+", name) if len(w) > 3 and w not in STOP and not w.isascii()]
            mentioned = 0
            if not mine and kws:
                for q in chq:
                    blob = norm((q["why"] or "") + " " + (q["remember"] or "") + " " + (q["distractors"] or ""))
                    if any(k in blob for k in kws): mentioned += 1
            rows.append(dict(sub=s, name=name, covered=bool(mine), covered_by_real=bool(real),
                             covered_by_generated=bool(mine) and not real, real=len(real), generated=len(mine) - len(real), mentioned_only=mentioned))
        res[n] = rows
    return res

def write_coverage_md(cov, focus, rows_focus):
    lines = ["# Coverage audit (§9) and focus areas (§10a) — generated by build_bank.py", ""]
    tot = sum(len(v) for v in cov.values()); direct = sum(1 for n in cov for r in cov[n] if r["covered_by_real"])
    gen = sum(1 for n in cov for r in cov[n] if r["covered_by_generated"]); unc = sum(1 for n in cov for r in cov[n] if not r["covered"])
    ment = sum(1 for n in cov for r in cov[n] if not r["covered"] and r["mentioned_only"])
    lines += [f"Units audited: {tot} (finest TOC level). Directly asked by real questions: {direct}. Covered only by generated questions: {gen}. Not covered: {unc} (of which mentioned only inside explanations: {ment}).", "",
              "| ch | unit | name | real | generated | status | focus |", "|---|---|---|---|---|---|---|"]
    for n in CHAPTERS:
        for r in cov[n]:
            st = "asked" if r["covered_by_real"] else "generated only" if r["covered_by_generated"] else ("mentioned only" if r["mentioned_only"] else "NOT COVERED")
            lines.append(f"| {n} | {r['sub']} | {r['name']} | {r['real']} | {r['generated']} | {st} | {'★' if (n, r['sub']) in focus else ''} |")
    lines += ["", "## Focus areas (exam-question count first, then total)", "", "| ch | unit | name | exam | textbook | other | total |", "|---|---|---|---|---|---|---|"]
    for r in rows_focus:
        if (r["ch"], r["sub"]) in focus:
            lines.append(f"| {r['ch']} | {r['sub']} | {r['name']} | {r['exam']} | {r['textbook']} | {r['other']} | {r['total']} |")
    with open(os.path.join(WORK, "coverage.md"), "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(lines) + "\n")
    return dict(units=tot, direct=direct, generated_only=gen, uncovered=unc, mentioned_only=ment)

def main():
    subs, qs = load()
    qs = merge_duplicates(qs)
    normalise_types(qs)
    check_basic(qs, subs)
    check_duplicates(qs)
    rows, focus = focus_areas(qs, subs)
    for q in qs:
        q["importance"] = score(q, focus)
        q["freq"] = 0 if "generated" in q["types"] else len(q["sources"])
        q["focus"] = (q["ch"], q["sub"]) in focus
        q["subname"] = subs[q["ch"]][q["sub"]]
    cov = coverage(qs, subs)
    stats = write_coverage_md(cov, focus, rows)
    uncovered = [(n, r["sub"], r["name"]) for n in CHAPTERS for r in cov[n] if not r["covered"]]
    total_subs = sum(len(v) for v in subs.values())
    print("questions:", len(qs), "| subsections:", total_subs, "| uncovered:", len(uncovered))
    if OUTSIDE: print("pages cited outside the chapter range (book asks it in this chapter's review set):", OUTSIDE)
    for u in uncovered: print("  UNCOVERED", u)
    print("covered only by generated:", stats["generated_only"], "| mentioned only:", stats["mentioned_only"])
    print("type counts:", collections.Counter(t for q in qs for t in q["types"]))
    print("per chapter:", {n: sum(1 for q in qs if q["ch"] == n) for n in CHAPTERS})
    gen = sum(1 for q in qs if "generated" in q["types"]); real = len(qs) - gen
    print(f"generated {gen} vs real {real} ({gen/len(qs):.1%} of bank)")
    for n in CHAPTERS:
        g = sum(1 for q in qs if q["ch"] == n and "generated" in q["types"]); r = sum(1 for q in qs if q["ch"] == n) - g
        if g > r: print("  WARNING generated>real in ch", n)
    print("importance:", collections.Counter(q["importance"] for q in qs))
    print("low_conf:", sum(1 for q in qs if q["low_conf"]))
    print("reconstructed:", sum(1 for q in qs if q["reconstructed"]))
    print("focus areas:", sorted(focus))
    ledger = LEDGER["sources"]
    chapter_map = json.load(open(os.path.join(WORK, "chapter_map.json"), encoding="utf-8"))
    notice = [f"Generated with the SVU MBA Course Review Generator, prompt {SPEC} · deliverable v{VERSION}",
              "Source and latest version: https://github.com/AzizMarashly/SVU-MBA-Course-Review",
              "Licence of the prompt and of this file: CC BY-NC-SA 4.0 — share freely, credit the source, never sell. Quoted textbook and exam content stays with its owners and is not covered."]
    out = dict(_notice=notice, spec_version=SPEC, file_version=VERSION, title=M.TITLE, generated=M.GENERATED_DATE,
               source_ledger=ledger, chapter_map=chapter_map, course=M.COURSE,
               chapters_in_scope=M.CHAPTERS, chapters={str(c): {"title": M.CH_TITLES[c], "pages": f"{M.CH_PAGES[c][0]}–{M.CH_PAGES[c][1]}"} for c in M.CHAPTERS},
               openers={n: list(v) for n, v in M.OPENERS.items()}, subsections=subs, questions=qs,
               focus_table=rows, focus_areas=sorted([list(f) for f in focus]), coverage=cov, coverage_stats=stats)
    return out

if __name__ == "__main__":
    out = main()
    dst = os.path.join(WORK, "bank.json")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", dst)
