# -*- coding: utf-8 -*-
"""ACM: assemble all chapter files into one verified bank (JSON, UTF-8 no BOM), compute focus areas,
importance scores, coverage audit (also written to ../coverage.md) and mechanical checks. Adapted from PRM/MIS for prompt v0.12
(§5a cross-linked cards, §5b build checks, §7e methods/figures, §9 own-content coverage)."""
import importlib, json, os, re, sys, collections, unicodedata, math, itertools
sys.path.insert(0, os.path.dirname(__file__))
import meta_acm as M
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, "..")
CHAPTERS = M.CHAPTERS
SPEC = "v0.12"
VERSION = open(os.path.join(WORK, "VERSION"), encoding="utf-8").read().strip()
LEDGER = json.load(open(os.path.join(WORK, "ledger.json"), encoding="utf-8"))
EXAM_CODES = {e["id"] for e in LEDGER["sources"] if e.get("kind") == "exam" and e["decision"].startswith("included")}
assert EXAM_CODES == M.EXAM_CODES, (EXAM_CODES, M.EXAM_CODES)
OTHER_CODES = M.OTHER_CODES
SUBS_JSON = json.load(open(os.path.join(WORK, "extracted", "book", "subsections.json"), encoding="utf-8"))
SUBS_ALL = SUBS_JSON["units"]
SIM_THRESHOLD = 0.6   # §5b, recorded in STATE.md

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
        M.METHODS[n] = list(getattr(m, "METHODS", []))
    CHAPTERS = present
    return subs, qs

# Cross-chapter consolidation (§5b): true duplicates only — same claim of the book, same expected answer, same form.
# keep <- drop; the kept record is the exam item, in the chapter that owns the book page. Log: ../qa/consolidation_v1.0.md.
MERGES = {}
# Same claim, different form (§5a step 2, not protected): drop -> keep; the dropped record becomes an «also asked as» line.
# Q02-009 (S24 recall «تعريف أساس الاستحقاق», reconstructed MCQ, ch 2 p. 56) -> the book review item Q08-014 (T/F, ch 8 p. 249): same
# claim (revenues and expenses of the period are recognised whatever the date of collection or payment), protected keeper.
FOLDS = {"Q02-009": "Q08-014"}

def _join(a, b, sep=" | "):
    return sep.join(x for x in (a, b) if x) or None

def answer_text(q):
    return q["options"][q["ans"]] if q["qtype"] == "mcq" else str(q["ans"])

def merge_duplicates(qs):
    """Union sources/pages/raw ids, dropped wording becomes a variant (MERGES) or an also-asked-as line (FOLDS); flags and notes kept
    from both; freq is later len(sources) — the size of the source union, never a sum. A merge whose answers disagree is a hard error."""
    byid = {q["id"]: q for q in qs}
    for drop, keep in list(MERGES.items()) + list(FOLDS.items()):
        d, k = byid[drop], byid[keep]
        if drop in MERGES and d["qtype"] == k["qtype"] and d["qtype"] in ("mcq", "tf"):
            assert norm(answer_text(d)) == norm(answer_text(k)) or (d["qtype"] == "mcq" and norm(answer_text(d)) in norm(answer_text(k))), \
                ("merge with disagreeing answers", drop, keep, answer_text(d), answer_text(k))
        for c in d["sources"]:
            if c not in k["sources"]: k["sources"].append(c)
        ans = answer_text(d)
        srcs = "/".join(c for c in d["sources"] if c not in M.XCHK_CODES)
        if drop in MERGES:
            k["variants"] = list(k["variants"]) + [f"{srcs} (كان {drop}): {d['stem']} — {ans}"] + list(d["variants"])
        else:
            form = {"mcq": "اختيار من متعدد", "tf": "صح / خطأ", "short": "سؤال قصير", "essay": "مقالي"}[d["qtype"]]
            k["also"] = list(k["also"]) + [dict(form=form, wording=d["stem"], key=ans, sources=list(d["sources"]))] + list(d["also"])
        if drop in MERGES or d["ch"] == k["ch"]:   # a cross-chapter fold keeps the keeper's pages (its Ref line names the keeper's chapter)
            k["pages"] = sorted(set(k["pages"]) | set(d["pages"]))
        k["raw"] = list(dict.fromkeys(k.get("raw", []) + d.get("raw", [])))
        k["reconstructed"] = k["reconstructed"] or (d["reconstructed"] and k["qtype"] == "mcq")
        for f in ("low_conf", "book_says", "other_source", "notes"):
            k[f] = _join(k[f], d[f])
        if drop in MERGES:   # a fold keeps the recalled wording on its «also asked as» line, not under the keeper's stem
            k["original"] = _join(k["original"], d["original"])
        k.setdefault("aliases", []).append(drop)
    gone = set(MERGES) | set(FOLDS)
    return [q for q in qs if q["id"] not in gone]

# Duplicate checks (§5b). Tokens: normalised words without stop words and the article; tf-idf cosine.
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

# Pairs read by hand in the consolidation pass: same option set and similar stem, different answer on purpose.
DUP_ALLOW = set()

def check_duplicates(qs):
    """Hard: (1) same normalised option set + stem cosine >= SIM_THRESHOLD + different correct answer; (2) a raw source-item id used by
    two records. Warning: each record's top-3 cross-chapter neighbours above the union threshold (written to ../qa/neighbours_v<VERSION>.txt)."""
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
        if optset(a) and optset(a) == optset(b) and cos(Vq[i], Vq[j]) >= SIM_THRESHOLD \
                and norm(answer_text(a)) != norm(answer_text(b)) and (a["id"], b["id"]) not in DUP_ALLOW and (b["id"], a["id"]) not in DUP_ALLOW:
            errors.append(f"same options, similar stem ({cos(Vq[i], Vq[j]):.2f}), different answer: {a['id']} / {b['id']}")
        if a["ch"] != b["ch"]:
            s, f, bd = cos(Vs[i], Vs[j]), cos(Vf[i], Vf[j]), cos(Vb[i], Vb[j])
            if s >= 0.40 or f >= 0.40 or bd >= 0.45:
                for x, y in ((a, b), (b, a)): near[x["id"]].append((max(s, f, bd), y["id"], s, f, bd))
    used = collections.defaultdict(list)
    for q in qs:
        for r in q.get("raw", []):
            if not r.startswith("~"): used[r].append(q["id"])
    base = collections.defaultdict(set)
    for r, ids in used.items():
        if len(ids) > 1: errors.append(f"raw item {r} used by {ids}")
        base[r.split("@")[0]].add(r)
    for b0, forms in base.items():
        if len(forms) > 1 and b0 in forms: errors.append(f"raw item {b0} used whole and as sub-questions {sorted(forms)}")
    lacking = [q["id"] for q in qs if not q.get("raw") and "generated" not in q["types"]]
    lines = [f"# Cross-chapter neighbours (warning list, §5b) — v{VERSION}, stem threshold {SIM_THRESHOLD}", ""]
    for k in sorted(near):
        lines.append(f"{k} -> " + ", ".join(f"{y} (stem {s:.2f} / full {f:.2f} / bold {bd:.2f})" for _, y, s, f, bd in sorted(near[k], reverse=True)[:3]))
    os.makedirs(os.path.join(WORK, "qa"), exist_ok=True)
    with open(os.path.join(WORK, "qa", f"neighbours_v{VERSION}.txt"), "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(lines) + "\n")
    print(f"duplicate check: {len(near)} records with cross-chapter neighbours above the union threshold (warning list in qa/neighbours_v{VERSION}.txt)")
    print(f"raw source-item ids: {len(qs) - len(lacking) - sum('generated' in q['types'] for q in qs)} records declare them, {len(lacking)} real records do not: {lacking[:20]}")
    assert not errors, "duplicate check failed:" + "".join("\n  " + e for e in errors)

def normalise_types(qs):
    """types derive from sources: exam <=> an exam sitting has it; textbook <=> BOOK; other <=> OTHER_CODES; SUM is a cross-check only."""
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

def link_groups(qs):
    """§5a step 2: cross-linked cards (see=[...]) share one frequency and one importance, computed from the union of their sources."""
    byid = {q["id"]: q for q in qs}
    groups = {}
    for q in qs:
        for s in q["see"]:
            assert s in byid, (q["id"], "see -> unknown id", s)
            assert q["id"] in byid[s]["see"], (q["id"], s, "see-link must be symmetric")
        if q["see"]:
            key = tuple(sorted([q["id"]] + q["see"]))
            groups[key] = [byid[i] for i in key]
    for key, grp in groups.items():
        union = []
        for g in grp:
            for c in g["sources"]:
                if c not in union: union.append(c)
        for g in grp:
            g["union_sources"] = union
            g["union_exam"] = [c for c in union if c in EXAM_CODES]
            g["union_textbook"] = any("BOOK" in x["sources"] for x in grp)
            g["union_units"] = [(x["ch"], x["sub"]) for x in grp]
    return groups

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
            assert len(q["options"]) == 4, (q["id"], "reconstructed items have exactly four options (§3b)")
        if q["unsolved"]:
            assert "BOOK" in q["sources"], (q["id"], "unsolved exercises are book records")
        if q["calc"] and q["calc"]["method"]:
            keys = {m["key"] for m in M.METHODS.get(q["ch"], [])}
            assert q["calc"]["method"] in keys, (q["id"], "calc.method not in the chapter METHODS", q["calc"]["method"], keys)
        if q["fig"]:
            f = q["fig"]; be = f["fixed"] / (f["price"] - f["var"])
            assert abs(be - f["be_q"]) < 0.5 + 1e-9, (q["id"], "figure data recompute", be, f["be_q"])
    for n in CHAPTERS:
        keys = [m["key"] for m in M.METHODS.get(n, [])]
        assert len(keys) == len(set(keys)), (n, "duplicate METHODS keys")
        for m in M.METHODS.get(n, []):
            assert m["steps"] and m["page"], (n, m["key"], "method needs steps and a page")

def focus_areas(qs, subs):
    """per unit: distinct claims by origin (cross-linked cards count once). Rank by exam count then total.
    Focus areas per chapter: units with >= 2 exam sources' questions, else top-2 with >= 1."""
    tab = {}
    for n, d in subs.items():
        for s, name in d.items():
            tab[(n, s)] = dict(ch=n, sub=s, name=name, exam=0, textbook=0, other=0, generated=0, total=0)
    seen = set()
    for q in qs:
        k = (q["ch"], q["sub"])
        if "generated" in q["types"]:
            tab[k]["generated"] += 1; continue
        gk = tuple(sorted([q["id"]] + q["see"])) if q["see"] else (q["id"],)
        if gk in seen: continue
        seen.add(gk)
        ex = q.get("union_exam", q["exam_sources"]); tb = q.get("union_textbook", "textbook" in q["types"])
        if ex: tab[k]["exam"] += 1
        if tb: tab[k]["textbook"] += 1
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
    n = len(q.get("union_exam", q["exam_sources"]))
    base = 1 if n == 0 else 2 if n == 1 else 3 if n == 2 else 4
    # cross-linked cards (§5a) share one score: the focus bonus applies when any card of the claim sits in a focus unit
    in_focus = any(u in focus for u in q.get("union_units", [(q["ch"], q["sub"])]))
    bonus = (1 if q.get("union_textbook", "textbook" in q["types"]) else 0) + (1 if in_focus else 0)
    return min(5, base + bonus)

def norm(t):
    t = unicodedata.normalize("NFKC", t or "")
    t = re.sub(r"[ً-ْـ]", "", t)
    t = t.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"\s+", " ", t).lower()

STOP = {"في", "من", "على", "ما", "هي", "هو", "و", "أو", "مع", "الى", "إلى", "كيف", "ال", "التي", "الذي", "لماذا", "أنواع", "مفهوم", "تعريف", "المحاسبة", "المحاسبية", "المالية", "قائمة", "طريقة", "طرق"}
def coverage(qs, subs):
    """§9 step 2 (own content): a unit counts as covered only by a question assigned to it (its expected answer is the unit's own
    term/rule/number — the helper's `sub`) AND whose Ref pages include a page inside the unit's page range. A question assigned to the
    unit whose pages all lie elsewhere counts as 'mentioned' (listed as a warning); 'mentioned only' also counts questions of other units
    whose explanation names the unit's keywords."""
    res = {}; misplaced = []
    for n, d in subs.items():
        rows = []
        chq = [q for q in qs if q["ch"] == n]
        for s, name in d.items():
            rng = SUBS_ALL[str(n)][s]["pages"]
            mine = [q for q in chq if q["sub"] == s]
            inpage = [q for q in mine if any(rng[0] <= p <= rng[1] for p in q["pages"])]
            for q in mine:
                if q not in inpage: misplaced.append((q["id"], s, rng, q["pages"]))
            real = [q for q in inpage if "generated" not in q["types"]]
            kws = [norm(w) for w in re.split(r"[\s:،؛,()/–-]+", name) if len(w) > 3 and w not in STOP and not w.isascii()]
            mentioned = 0
            if not inpage and kws:
                for q in chq:
                    blob = norm((q["why"] or "") + " " + (q["remember"] or "") + " " + (q["distractors"] or ""))
                    if any(k in blob for k in kws): mentioned += 1
            rows.append(dict(sub=s, name=name, covered=bool(inpage), covered_by_real=bool(real),
                             covered_by_generated=bool(inpage) and not real, real=len(real), generated=len(inpage) - len(real),
                             mentioned_only=mentioned + (len(mine) - len(inpage)), pages=rng))
        res[n] = rows
    if misplaced:
        print("WARNING: records assigned to a unit but citing no page inside it (count as 'mentioned', not covered):")
        for m in misplaced: print("   ", m)
    return res, misplaced

def write_coverage_md(cov, focus, rows_focus):
    lines = ["# Coverage audit (§9) and focus areas (§10a) — generated by build_bank.py", "",
             "Scope: the F25 exam scope (see meta_acm.SCOPE_BANNER). A unit is covered only by a question assigned to it whose Ref page lies inside the unit (own content).", ""]
    tot = sum(len(v) for v in cov.values()); direct = sum(1 for n in cov for r in cov[n] if r["covered_by_real"])
    gen = sum(1 for n in cov for r in cov[n] if r["covered_by_generated"]); unc = sum(1 for n in cov for r in cov[n] if not r["covered"])
    ment = sum(1 for n in cov for r in cov[n] if not r["covered"] and r["mentioned_only"])
    lines += [f"Units audited: {tot}. Asked on own content by real questions: {direct}. Covered only by generated questions: {gen}. Not covered: {unc} (of which mentioned only inside explanations: {ment}).", "",
              "| ch | unit | name | pages | real | generated | status | focus |", "|---|---|---|---|---|---|---|---|"]
    for n in CHAPTERS:
        for r in cov[n]:
            st = "asked" if r["covered_by_real"] else "generated only" if r["covered_by_generated"] else ("mentioned only" if r["mentioned_only"] else "NOT COVERED")
            lines.append(f"| {n} | {r['sub']} | {r['name']} | {r['pages'][0]}–{r['pages'][1]} | {r['real']} | {r['generated']} | {st} | {'★' if (n, r['sub']) in focus else ''} |")
    lines += ["", "## Focus areas (exam-question count first, then total; cross-linked cards count once)", "", "| ch | unit | name | exam | textbook | other | total |", "|---|---|---|---|---|---|---|"]
    for r in rows_focus:
        if (r["ch"], r["sub"]) in focus:
            lines.append(f"| {r['ch']} | {r['sub']} | {r['name']} | {r['exam']} | {r['textbook']} | {r['other']} | {r['total']} |")
    with open(os.path.join(WORK, "coverage.md"), "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(lines) + "\n")
    return dict(units=tot, direct=direct, generated_only=gen, uncovered=unc, mentioned_only=ment)

def main():
    subs, qs = load()
    qs = merge_duplicates(qs)
    normalise_types(qs)
    link_groups(qs)
    check_basic(qs, subs)
    check_duplicates(qs)
    rows, focus = focus_areas(qs, subs)
    for q in qs:
        q["importance"] = score(q, focus)
        q["freq"] = 0 if "generated" in q["types"] else len(q.get("union_sources", q["sources"]))
        q["focus"] = (q["ch"], q["sub"]) in focus
        q["subname"] = subs[q["ch"]][q["sub"]]
    cov, misplaced = coverage(qs, subs)
    stats = write_coverage_md(cov, focus, rows)
    uncovered = [(n, r["sub"], r["name"]) for n in CHAPTERS for r in cov[n] if not r["covered"]]
    total_subs = sum(len(v) for v in subs.values())
    print("questions:", len(qs), "| units:", total_subs, "| uncovered:", len(uncovered))
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
    print("§7d/§7e: table", sum(1 for q in qs if q["table"]), "| ans_table", sum(1 for q in qs if q["ans_table"]), "| calc", sum(1 for q in qs if q["calc"]),
          "| fig", sum(1 for q in qs if q["fig"]), "| fast", sum(1 for q in qs if q["fast"]), "| unsolved", sum(1 for q in qs if q["unsolved"]),
          "| essays with model answer", sum(1 for q in qs if q["model_answer"]), "| see-links", sum(1 for q in qs if q["see"]))
    print("focus areas:", sorted(focus))
    ledger = LEDGER["sources"]
    chapter_map = json.load(open(os.path.join(WORK, "chapter_map.json"), encoding="utf-8"))
    notice = [f"Generated with the SVU MBA Course Review Generator, prompt {SPEC} · deliverable v{VERSION}",
              "Source and latest version: https://github.com/AzizMarashly/SVU-MBA-Course-Review",
              "Licence of the prompt and of this file: CC BY-NC-SA 4.0 — share freely, credit the source, never sell. Quoted textbook and exam content stays with its owners and is not covered."]
    out = dict(_notice=notice, spec_version=SPEC, file_version=VERSION, title=M.TITLE, generated=M.GENERATED_DATE,
               source_ledger=ledger, chapter_map=chapter_map, course=M.COURSE, scope=M.SCOPE_BANNER, exam_sitting=M.EXAM_SITTING,
               chapters_in_scope=M.CHAPTERS, chapters={str(c): {"title": M.CH_TITLES[c], "pages": f"{M.CH_PAGES[c][0]}–{M.CH_PAGES[c][1]}", "scope_note": M.CH_SCOPE_NOTE.get(c)} for c in M.CHAPTERS},
               openers={n: list(v) for n, v in M.OPENERS.items()}, methods={n: v for n, v in M.METHODS.items()}, subsections=subs, units_pages={n: {s: SUBS_ALL[str(n)][s]["pages"] for s in subs[n]} for n in subs},
               excluded_units=SUBS_JSON["excluded"], questions=qs, symbols=M.SYMBOLS, similar_stem_threshold=SIM_THRESHOLD,
               focus_table=rows, focus_areas=sorted([list(f) for f in focus]), coverage=cov, coverage_stats=stats, misplaced=misplaced)
    return out

if __name__ == "__main__":
    out = main()
    dst = os.path.join(WORK, "bank.json")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", dst)
