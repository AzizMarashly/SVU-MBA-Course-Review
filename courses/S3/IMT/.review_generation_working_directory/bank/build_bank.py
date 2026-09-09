# -*- coding: utf-8 -*-
"""Assemble all chapter files into one verified bank (JSON, UTF-8 no BOM), compute focus areas,
importance scores, coverage audit and mechanical checks."""
import importlib, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
CHAPTERS = [1,2,3,4,5,6,7,9,10,11,12]
SPEC = "v0.9"
VERSION = open(os.path.join(os.path.dirname(__file__), "..", "VERSION"), encoding="utf-8").read().strip()
EXAM_CODES = {"F17","F19","S24","F24"}

def load():
    subs, qs = {}, []
    for n in CHAPTERS:
        m = importlib.import_module(f"bank_ch{n:02d}")
        subs[n] = dict(m.SUBS); qs += list(m.QS)
    ex = importlib.import_module("bank_extra"); qs += list(ex.QS)
    return subs, qs

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
    ledger = [
      dict(id="BOOK", files=["المنهاج الٱكاديمي/MBA-International Marketing and Trading-The Book.pdf","المنهاج الٱكاديمي/أسئلة الكتاب - IMT.pdf (dependent extract of review sections)"], type="primary reference + end-of-chapter questions", decision="included (authority)"),
      dict(id="F17", files=["اسئلة سابقة/دورة f17 تسويق دولي.docx","اسئلة سابقة/IMT_دورة f17 تسويق دولي.docx (identical MD5)","اسئلة سابقة/أسئلة-تسويق-دولي_IMT(1).pdf (same 27 questions + 7 embedded images)"], type="exam recall", decision="included as ONE independent source"),
      dict(id="F19", files=["اسئلة سابقة/دورات  F19.pdf","اسئلة سابقة/أسئلة_دورات_F19_تسويق_دولي_MIS.pdf (identical MD5)"], type="exam recall, handwritten scan (30 q, read visually)", decision="included"),
      dict(id="S24", files=["اسئلة سابقة/دورات.txt (part 2)"], type="exam recall (Telegram export)", decision="included"),
      dict(id="F24", files=["اسئلة سابقة/دورات.txt (part 1)"], type="exam recall with answers (Telegram export)", decision="included"),
      dict(id="EMAD", files=["اسئلة سابقة/ملخصIMT عماد جبور كامل.pdf"], type="Q&A summary S18", decision="included only for items whose concept exists in the current book"),
      dict(id="ASEM", files=["ملخصات سابقة/ملخص_عاصم_التسويق_والتجارة_الدولية_IMT.pdf"], type="summary with solved book review questions", decision="included as cross-check for textbook questions (59/60 T/F agree)"),
      dict(id="EXCLUDED-WAEL", files=["ملخصات سابقة/IMT_F19_وائل منصور.pdf"], type="handwritten summary, 56 scanned pages", decision="no questions; older chapter layout; all pages inspected visually"),
      dict(id="PHOTO", files=["ملفات متعلقة بالمادة/photo_2024-06-05_20-58-43.jpg"], type="handwritten list of recalled exam topics per chapter", decision="topic evidence only"),
      dict(id="EXCLUDED-OLD-ESSAY", files=["اسئلة سابقة/imt exam.docx","imt exam(1).docx","imt-exam.docx","اسئلة.docx","اسئلة(1).docx","اسئلة_IMT.docx","اسئلة_دورات_IMT.pdf"], type="42 essay prompts+answers, older curriculum", decision="excluded: topics not in current book"),
      dict(id="EXCLUDED-OLD-BOOK", files=["ملفات متعلقة بالمادة/الفصل الأول.pdf","الفصل الثاني.pdf","الفصل الثالث.pdf","الفصل الخامس.pdf"], type="chapters of a different textbook", decision="excluded"),
      dict(id="EXCLUDED-PPT", files=["ملفات متعلقة بالمادة/شروط التجارة الدولية.ppt","شروط قيام التجارة والفاه الاقتصادي.ppt"], type="lecture from another course (د. حسين الفحل)", decision="excluded"),
      dict(id="SLIDES", files=["المنهاج الٱكاديمي/Slides/Ch01..Ch14"], type="current course slides", decision="reference only, no questions"),
    ]
    chapter_map = [
      dict(source="Slides Ch01/Ch02", book_chapter=[1,2], evidence="titles"),
      dict(source="Slides Ch03+Ch04", book_chapter=[3], evidence="book merges political+legal"),
      dict(source="Slides Ch05", book_chapter=[4], evidence="Economic environment"),
      dict(source="Slides Ch06", book_chapter=[5], evidence="Information & research"),
      dict(source="Slides Ch07+Ch08", book_chapter=[6], evidence="Entry strategies (one book chapter)"),
      dict(source="Slides Ch09..Ch14", book_chapter=[7,8,9,10,11,12], evidence="titles"),
      dict(source="photo_2024-06-05 topic list", book_chapter="same numbering as book (1-12 without 8)", evidence="ch5 = information systems"),
      dict(source="EMAD/WAEL (S18-era)", book_chapter="older layout; mapped by content", evidence="e.g. Wael ch6 = culture"),
      dict(source="Exam recalls F17/F19/S24/F24", book_chapter="no chapter numbers; assigned by content to book subsection", evidence="content"),
    ]
    notice = [f"Generated with the SVU MBA Course Review Generator, prompt {SPEC} · deliverable v{VERSION}",
              "Source and latest version: https://github.com/AzizMarashly/SVU-MBA-Course-Review",
              "Licence of the prompt and of this file: CC BY-NC-SA 4.0 — share freely, credit the source, never sell. Quoted textbook and exam content stays with its owners and is not covered."]
    out = dict(_notice=notice, spec_version=SPEC, file_version=VERSION, title="مراجعه كامله لماده ال IMT", generated="2026-09-09",
               source_ledger=ledger, chapter_map=chapter_map,
               course="التسويق والتجارة الدولية — INTERNATIONAL MARKETING AND TRADING",
               chapters_in_scope=CHAPTERS, subsections=subs, questions=qs,
               focus_table=rows, focus_areas=sorted([list(f) for f in focus]), coverage=cov)
    return out

if __name__ == "__main__":
    out = main()
    dst = os.path.join(os.path.dirname(__file__), "..", "bank.json")
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("written", dst)
