# -*- coding: utf-8 -*-
"""PRM: assemble all chapter files into one verified bank (JSON, UTF-8 no BOM), compute focus areas,
importance scores, coverage audit and mechanical checks."""
import importlib, json, os, re, sys, collections, itertools, math
sys.path.insert(0, os.path.dirname(__file__))
import meta_prm as M
from common import T
CHAPTERS = M.CHAPTERS
SPEC = "v0.11"
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

# ---- Consolidation (IDEAS I-11; v1.4 whole-bank pass, log in ../qa/consolidation_v1.4.md) ----
# Every entry: drop -> (keep, the one claim both records test). Kept record = the exam item, in the chapter that owns
# the book page. Sources, pages and raw ids are unioned (frequency = size of the source union, never a sum); the
# dropped id becomes an alias so old #anchors still resolve.
# MERGES (class a): same claim, same form -> the dropped wording becomes a variant of the kept record.
MERGES = {
    # stage 5 (v1.0): the same exam item routed to two chapters by different helpers
    "Q04-013": ("Q07-006", "the project plan contains subsidiary plans (TF, TATI)"),
    "Q07-005": ("Q04-012", "the project management plan defines execution, monitoring, control and closure (TF, S19)"),
    "Q03-012": ("Q05-005", "market need, business need, legal requirement are reasons to start a project (S19)"),
    "Q07-007": ("Q06-007", "decomposition has criteria for the level of detail of the WBS (TF, S19)"),
    # v1.4
    "Q04-011": ("Q07-003", "planning starts once the project scope statement is ready (p.178); key settled from the book"),
    "Q09-006": ("Q08-009", "critical path X4-X3-X6-X7 of the X1..X8 table (TATI sub-question also counted in Q08-009/Q08-013)"),
    "Q09-007": ("Q08-007", "LF(X3) = 11 of the X1..X8 table (TATI sub-question; its ES(X5) part is Q08-014)"),
    "Q02-008": ("Q14-001", "the final output is handed over to the customer (S19)"),
    "Q04-035": ("Q05-024", "contents of the project charter (EMAD, two wordings)"),
    "Q12-005": ("Q04-006", "risks are identified and estimated in the planning phase"),
    "Q08-018": ("Q08-017", "the critical path is the longest path, which fixes the shortest completion time"),
    "Q03-002": ("Q03-001", "payback: the shorter period wins, the interest rate plays no part (one EX15 item recalled with two data sets)"),
}
# FOLDS (class a with another form, and class b): same claim, other form -> one main record with an "also asked as" line
FOLDS = {
    "Q08-044": ("Q08-021", "shortening the duration at least extra cost = crashing"),
    "Q06-014": ("Q06-004", "the document / process that breaks the work into detailed tasks = WBS"),
    "Q02-010": ("Q02-001", "the three linked project variables are time, cost and performance/quality"),
    "Q02-021": ("Q02-001", "the three linked project variables are time, cost and performance/quality (scope)"),
    "Q03-028": ("Q03-001", "payback ignores the interest rate / time value of money"),
    "Q03-029": ("Q03-001", "payback: the shorter period is better"),
    "Q03-031": ("Q03-004", "negative NPV -> reject"),
    "Q03-030": ("Q03-017", "NPV = discounted net cash flows minus the initial investment"),
    "Q03-026": ("Q03-027", "weighted scoring model: weight x score per criterion, then sum"),
    "Q04-034": ("Q04-024", "definition phase: need, vision, goals, team, scope, charter"),
    "Q04-044": ("Q04-024", "definition phase: developing the project idea"),
    "Q04-036": ("Q04-001", "planning phase: scope detail, activities, schedule, budget, risks -> baseline plan"),
    "Q04-037": ("Q04-002", "execution phase: carry out the plan, lead the team, monitor and control"),
    "Q04-040": ("Q04-003", "closing phase: handover, evaluation, lessons learned"),
    "Q04-015": ("Q04-014", "a product life cycle can contain one or more projects"),
    "Q05-028": ("Q04-019", "scope management = all the work required and only the work required"),
    "Q05-022": ("Q05-001", "the charter authorises the project manager to use organisational resources"),
    "Q05-017": ("Q05-013", "objectives must be realistic: achievable with the available resources and skills"),
    "Q06-016": ("Q06-001", "the work package is the lowest WBS element (what / when / cost / who)"),
    "Q07-034": ("Q07-011", "a lead lets the successor start before the predecessor ends"),
    "Q07-031": ("Q07-019", "lag = a time delay between two activities (lead = negative lag)"),
    "Q08-034": ("Q08-025", "effort = person-days or person-hours needed for an activity"),
    "Q08-042": ("Q08-041", "fast tracking = doing activities in parallel / overlapped (no extra resources, more risk)"),
    "Q09-012": ("Q09-002", "resource levelling = cutting the peaks of resource demand"),
    "Q10-031": ("Q10-001", "earned value = budgeted cost of the work performed (BCWP)"),
    "Q11-019": ("Q11-020", "in the functional structure the project sits inside one functional department"),
    "Q11-025": ("Q11-005", "matrix structure: resources assigned temporarily from the functional departments"),
}
# Sub-questions without a data table of their own that share one data set (grouped on the page like the table families)
GROUPS_EXTRA = [(["Q10-020", "Q10-021", "Q10-022", "Q10-023"],
                 T(["BCWS", "ACWP", "BCWP"], [[10, 14, 12]], caption="القيم المشتركة لأسئلة الكتاب الأربعة (منتصف المشروع)"))]

def ans_text(q):
    return q["options"][q["ans"]] if q["qtype"] == "mcq" else str(q["ans"])

def answers_agree(d, k):
    """True/False where the records are comparable (same option set, or two TF on the same claim); None otherwise,
    and then the claim logged in MERGES/FOLDS is the evidence."""
    if d["qtype"] == k["qtype"] == "mcq" and optset(d) == optset(k):
        return norm(ans_text(d)) == norm(ans_text(k))
    if d["qtype"] == k["qtype"] == "tf" and cos1(d["stem"], k["stem"]) >= 0.6:
        return d["ans"] == k["ans"]
    return None

def absorb(k, d):
    for c in d["sources"]:
        if c not in k["sources"]: k["sources"].append(c)
    k["pages"] = sorted(set(k["pages"]) | set(d["pages"]))
    k["raw"] += [r for r in d["raw"] if r not in k["raw"]]
    k["aliases"] += [d["id"]] + d["aliases"]
    k["also"] += d["also"]
    k.setdefault("merged_subs", []).extend([[d["ch"], d["sub"]]] + d.get("merged_subs", []))
    for f in ("other_source", "book_says"):
        if d[f] and d[f] not in (k[f] or ""): k[f] = (k[f] + "؛ " if k[f] else "") + d[f]
    if d["low_conf"] and not k["low_conf"]: k["low_conf"] = d["low_conf"]

def merge_duplicates(qs):
    byid = {q["id"]: q for q in qs}
    for drop, (keep, claim) in list(MERGES.items()) + list(FOLDS.items()):
        d, k = byid[drop], byid[keep]
        assert claim and answers_agree(d, k) is not False, (drop, keep, "answers differ: settle from the book first", ans_text(d), ans_text(k))
        if drop in MERGES:
            opts = (" — " + " / ".join(d["options"]) + " — المفتاح: " + ans_text(d)) if d["options"] else ""
            recon = " (خيارات معاد بناؤها)" if d["reconstructed"] else ""
            orig = f" — نص الطالب: {d['original']}" if d["original"] else ""
            k["variants"] = list(k["variants"]) + [f"{'/'.join(d['sources'])} (كان {drop}){recon}: {d['stem']}{opts}{orig}"] + list(d["variants"])
        else:
            k["also"].append(dict(id=drop, qtype=d["qtype"], stem=d["stem"], options=d["options"], ans=ans_text(d),
                                  sources=list(d["sources"]), original=d["original"], reconstructed=d["reconstructed"],
                                  low_conf=d["low_conf"], other_source=d["other_source"], book_says=d["book_says"],
                                  variants=list(d["variants"]), pages=d["pages"], claim=claim))
            d = dict(d, other_source=None, book_says=None, low_conf=None)  # shown on the "also asked as" line instead
        absorb(k, d)
    gone = set(MERGES) | set(FOLDS)
    for q in qs:
        assert q["id"] in gone or not (set(q["see"]) & gone), (q["id"], "see= points to a merged id")
    out = [q for q in qs if q["id"] not in gone]
    see = {q["id"]: set(q["see"]) for q in out}
    for q in out:
        for s in q["see"]:
            assert q["id"] in see.get(s, ()), (q["id"], "see= must be mutual", s)
    return out

# ---- Similarity for the I-11 build checks: tokens and tf-idf cosine ----
STOP = set("""في من على الى إلى عن ان أن إن او أو و ما هو هي هذا هذه التي الذي الذين كل مما يلي ذلك تلك بين مع لا لم قد كان
تكون يكون يتم عند عندما التالية التالي التاليه جميع كلما بعد قبل حيث عملية أي اي ماعدا عدا ليس ليست هل مثل له لها به بها فيه فيها
منها منه the of and a an to in is are for on by with or as be which what from that this""".split())
def norm(s):
    s = re.sub(r"[ً-ْـ]", "", str(s)).lower()
    s = re.sub("[إأآٱ]", "ا", s).replace("ة", "ه").replace("ى", "ي").replace("ؤ", "و").replace("ئ", "ي")
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()
def toks(s):
    out = []
    for t in norm(s).split():
        if t in STOP or len(t) < 2: continue
        for p in ("وال", "بال", "كال", "فال", "لل", "ال"):
            if t.startswith(p) and len(t) - len(p) >= 3: t = t[len(p):]; break
        if t.startswith("و") and len(t) > 4: t = t[1:]
        for suf in ("ات", "ون", "ين", "ها", "ه", "ي"):
            if t.endswith(suf) and len(t) - len(suf) >= 3: t = t[:-len(suf)]; break
        out.append(t)
    return out
def optset(q): return frozenset(norm(o) for o in q["options"] or [])
def vectors(docs, background=()):
    df = collections.Counter(t for d in list(docs) + list(background) for t in set(d)); n = len(docs) + len(background)
    def v(d):
        c = collections.Counter(d); x = {t: (1 + math.log(k)) * math.log((n + 1) / (df[t] + 1)) for t, k in c.items()}
        nn = math.sqrt(sum(y * y for y in x.values())) or 1
        return {t: y / nn for t, y in x.items()}
    return [v(d) for d in docs]
def cos(a, b): return sum(x * b.get(t, 0) for t, x in a.items())
DOCS = []  # idf background (all stems), filled by main()
def cos1(s1, s2): return cos(*vectors([toks(s1), toks(s2)], DOCS))

def check_conflicts(qs):
    """Hard error (I-11): same option set, stem similarity >= 0.6, different keyed answer. Sub-questions of one data table are exempt."""
    V = vectors([toks(q["stem"]) for q in qs]); bad = []
    for i, j in itertools.combinations(range(len(qs)), 2):
        a, b = qs[i], qs[j]
        if a["qtype"] != "mcq" or b["qtype"] != "mcq" or optset(a) != optset(b): continue
        if a["table"] and a["table"] == b["table"]: continue
        if cos(V[i], V[j]) >= 0.6 and norm(ans_text(a)) != norm(ans_text(b)): bad.append((a["id"], b["id"], round(cos(V[i], V[j]), 2)))
    assert not bad, ("same options, similar stem, different answer (settle from the book, then merge):", bad)

def check_raw(qs):
    """Hard error (I-11): a raw source item used by two records ('~' = I-10 credit, may be shared). Returns the coverage."""
    use = collections.defaultdict(list)
    for q in qs:
        for r in q["raw"]:
            if not r.startswith("~"): use[r].append(q["id"])
    twice = {r: ids for r, ids in use.items() if len(ids) > 1}
    assert not twice, ("raw source item used by two records:", twice)
    real = [q for q in qs if "generated" not in q["types"]]
    return sum(1 for q in real if q["raw"]), len(real)

def neighbours(qs, path):
    """Warning report (I-11): each record's nearest cross-chapter records; union rule stem >= 0.40 or full >= 0.40 or bold >= 0.45."""
    fact = lambda q: q["stem"] if q["qtype"] == "tf" else ans_text(q)[:400]
    bold = lambda s: " ".join(re.findall(r"\*\*(.+?)\*\*", s or ""))
    Vs = vectors([toks(q["stem"]) + (toks(fact(q)) if q["qtype"] != "tf" else []) for q in qs])
    Vf = vectors([toks(" ".join([q["stem"], fact(q), q["why"], q["remember"]])) for q in qs])
    Vb = vectors([toks(bold(q["why"]) + " " + bold(q["remember"])) for q in qs])
    near = collections.defaultdict(list)
    for i, j in itertools.combinations(range(len(qs)), 2):
        a, b = qs[i], qs[j]
        if a["ch"] == b["ch"] or (a["table"] and b["table"]): continue
        s, f, bb = cos(Vs[i], Vs[j]), cos(Vf[i], Vf[j]), cos(Vb[i], Vb[j])
        if s >= 0.40 or f >= 0.40 or bb >= 0.45:
            near[a["id"]].append((max(s, f, bb), b["id"], s, f, bb)); near[b["id"]].append((max(s, f, bb), a["id"], s, f, bb))
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Cross-chapter neighbours (I-11 warning report, not an error): id -> up to 3 nearest (stem full bold)\n")
        for q in qs:
            if near[q["id"]]:
                fh.write(q["id"] + " -> " + "; ".join(f"{o} ({s:.2f} {f:.2f} {b:.2f})" for _, o, s, f, b in sorted(near[q["id"]], reverse=True)[:3]) + "\n")
    return sum(1 for v in near.values() if v), sum(len(v) for v in near.values()) // 2

def first_section(q): return next(s for s in ("exam", "textbook", "other", "generated") if s in q["types"])

def table_groups(qs):
    """Records of one chapter and section that share one data table (or a GROUPS_EXTRA data set) are shown under it once."""
    fam = collections.defaultdict(list)
    for q in qs:
        if q["table"]: fam[(q["ch"], json.dumps(q["table"], ensure_ascii=False))].append(q["id"])
    byid = {q["id"]: q for q in qs}
    found = [(ids, byid[ids[0]]["table"]) for ids in fam.values() if len(ids) > 1] + GROUPS_EXTRA
    groups = {}
    for ids, t in found:
        ids = sorted(ids); gid = "tbl-" + ids[0]
        assert len({(byid[i]["ch"], first_section(byid[i])) for i in ids}) == 1, (gid, "group members must share chapter and section")
        for i in ids: byid[i]["group"] = gid
        groups[gid] = dict(ids=ids, table=t, own=all(byid[i]["table"] == t for i in ids))
    return groups

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
        if "|" in q["stem"] or chr(10) in q["stem"]:
            if os.environ.get("PRM_LENIENT"): print("WARNING (lenient):", q["id"], "tabular stem")
            else: raise AssertionError((q["id"], "tabular data belongs in table=T(...), not in the stem (§7d)"))
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
    DOCS[:] = [toks(q["stem"]) for q in qs]
    check_conflicts(qs)                       # before merging: a merge must never hide two keys
    n_in = len(qs)
    qs = merge_duplicates(qs)
    normalise_types(qs)
    check_basic(qs, subs)
    raw_n, real_n = check_raw(qs)
    groups = table_groups(qs)
    nb_recs, nb_pairs = neighbours(qs, os.path.join(os.path.dirname(__file__), "..", "qa", f"neighbours_v{VERSION}.txt"))
    rows, focus = focus_areas(qs, subs)
    for q in qs:
        q["importance"] = score(q, focus)
        q["freq"] = 0 if "generated" in q["types"] else len(q["sources"])
        q["focus"] = (q["ch"], q["sub"]) in focus
        q["subname"] = subs[q["ch"]][q["sub"]]
    print(f"consolidation: {n_in} records in the chapter files -> {len(qs)} (merged {len(MERGES)}, folded {len(FOLDS)});",
          f"also-asked-as on {sum(1 for q in qs if q['also'])} records; cross-links {sum(len(q['see']) for q in qs) // 2}; table groups {len(groups)}")
    print(f"raw ids: {raw_n}/{real_n} real records carry them | cross-chapter neighbours: {nb_recs} records, {nb_pairs} pairs (qa/neighbours_v{VERSION}.txt)")
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
               focus_table=rows, focus_areas=sorted([list(f) for f in focus]), coverage=cov, groups=groups)
    return out

if __name__ == "__main__":
    out = main()
    dst = os.path.join(os.path.dirname(__file__), "..", "bank.json")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", dst)
