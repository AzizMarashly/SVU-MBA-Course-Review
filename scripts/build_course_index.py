# -*- coding: utf-8 -*-
"""Build courses.json at the repository root from the courses' own data, so the home page never
shows hand-typed numbers.

For every published page  S<n>/<CODE>/index.html  the script looks, in this order, for:

1. courses/S<n>/<CODE>/.review_generation_working_directory/bank.json  (the generator's checkpoint)
   -> questions, question types, chapters, independent sources, version, title, date
2. S<n>/<CODE>/course.json  (hand-maintained fallback for a course that has no bank in the repo)

Fields in course.json override anything derived from the bank, so names or notes can be fixed by hand.
Run from anywhere:  python scripts/build_course_index.py     (exit code 1 if courses.json changed,
so CI can decide whether to commit; pass --quiet to suppress the report).
"""
import io, json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = ".review_generation_working_directory"
OUT = os.path.join(ROOT, "courses.json")
SOURCE_EXT = {".pdf", ".docx", ".doc", ".ppt", ".pptx", ".txt", ".jpg", ".jpeg", ".png", ".md", ".xlsx"}


def read_json(path):
    with io.open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def split_course_name(s):
    """'التسويق والتجارة الدولية — INTERNATIONAL MARKETING AND TRADING' -> (ar, en)"""
    if not s:
        return "", ""
    parts = re.split(r"\s+[—–-]{1,2}\s+", s, maxsplit=1)
    if len(parts) == 2:
        a, b = parts
        if re.search(r"[A-Za-z]", a) and not re.search(r"[A-Za-z]", b):
            a, b = b, a
        return a.strip(), smart_title(b.strip()) if b.isupper() else b.strip()
    return (s.strip(), "") if not re.search(r"[A-Za-z]", s) else ("", s.strip())


SMALL = {"and", "of", "the", "in", "for", "on", "to", "a", "an"}


def smart_title(s):
    words = s.lower().split()
    return " ".join(w if (i and w in SMALL) else w.capitalize() for i, w in enumerate(words))


def count_source_files(course_dir):
    n = 0
    for dirpath, dirnames, filenames in os.walk(course_dir):
        dirnames[:] = [d for d in dirnames if d != WORK and not d.startswith("_") and not d.startswith(".")]
        for f in filenames:
            if os.path.splitext(f)[1].lower() in SOURCE_EXT and dirpath != course_dir:
                n += 1
    return n


def from_bank(bank, course_dir):
    qs = bank.get("questions", [])
    types = Counter(t for q in qs for t in (q.get("types") or [q.get("type")]) if t)
    ledger = bank.get("source_ledger", [])
    if isinstance(ledger, dict):
        ledger = list(ledger.values())
    independent = [e for e in ledger if str(e.get("decision", "")).lower().startswith("included")]
    ar, en = split_course_name(bank.get("course", ""))
    return {
        "title": bank.get("title", ""),
        "name_ar": ar,
        "name_en": en,
        "version": str(bank.get("file_version", "")),
        "spec_version": bank.get("spec_version", ""),
        "generated": bank.get("generated", ""),
        "questions": len(qs),
        "questions_by_type": dict(types),
        "chapters": len(bank.get("chapters_in_scope", []) or sorted({q.get("ch") for q in qs})),
        "sources": len(independent),
        "source_ids": [e.get("id") for e in independent],
        "source_files": count_source_files(course_dir),
        "low_confidence": sum(1 for q in qs if q.get("low_conf") or q.get("low_confidence") or q.get("confidence") == "low"),
        "data": "bank",
    }


def main():
    quiet = "--quiet" in sys.argv
    courses = []
    for sem in sorted(d for d in os.listdir(ROOT) if re.fullmatch(r"S\d+", d) and os.path.isdir(os.path.join(ROOT, d))):
        for code in sorted(os.listdir(os.path.join(ROOT, sem))):
            page = os.path.join(ROOT, sem, code, "index.html")
            if not os.path.isfile(page):
                continue
            entry = {"semester": int(sem[1:]), "code": code, "path": f"{sem}/{code}/"}
            course_dir = os.path.join(ROOT, "courses", sem, code)
            bank = os.path.join(course_dir, WORK, "bank.json")
            if os.path.isfile(bank):
                entry.update(from_bank(read_json(bank), course_dir))
                entry["sources_path"] = f"courses/{sem}/{code}/"
            manual = os.path.join(ROOT, sem, code, "course.json")
            if os.path.isfile(manual):
                entry.update(read_json(manual))
                entry.setdefault("data", "manual")
            if "questions" not in entry:
                print(f"warning: {sem}/{code} has neither a bank nor course.json; skipped", file=sys.stderr)
                continue
            entry["download_name"] = entry.get("download_name") or f"{entry.get('title') or code}_v{entry.get('version','')}.html"
            courses.append(entry)

    result = {"generated_by": "scripts/build_course_index.py", "courses": courses}
    new = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    old = io.open(OUT, encoding="utf-8").read() if os.path.isfile(OUT) else None
    changed = new != old
    if changed:
        with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
    if not quiet:
        for c in courses:
            print(f"{c['path']:<10} v{c.get('version','?'):<5} {c['questions']:>4} q  {c['chapters']:>2} ch  "
                  f"{c['sources']:>2} sources  {c.get('source_files','-'):>3} files  ({c['data']})")
        print("courses.json", "updated" if changed else "unchanged")
    sys.exit(1 if changed else 0)


if __name__ == "__main__":
    main()
