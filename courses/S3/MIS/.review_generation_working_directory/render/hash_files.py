# -*- coding: utf-8 -*-
"""Stage 4: MD5 of every file in the course folder (working directory excluded) -> ../extracted/hashes.json.
Usage (from render/): set PYTHONUTF8=1 && python hash_files.py"""
import os, hashlib, json, unicodedata, collections
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE); COURSE = os.path.dirname(WORK)
rows = []
for root, dirs, files in os.walk(COURSE):
    dirs[:] = [d for d in dirs if d != ".review_generation_working_directory"]
    for f in files:
        p = os.path.relpath(os.path.join(root, f), COURSE).replace(os.sep, "/")
        if p.endswith(".md") or "_v" in f and f.endswith(".html"): continue
        full = os.path.join(root, f)
        rows.append(dict(path=unicodedata.normalize("NFC", p), disk_path=p, md5=hashlib.md5(open(full, "rb").read()).hexdigest(), size=os.path.getsize(full)))
rows.sort(key=lambda r: r["path"])
json.dump(rows, open(os.path.join(WORK, "extracted", "hashes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), "files")
c = collections.Counter(r["md5"] for r in rows); print("duplicate hashes:", [k for k, v in c.items() if v > 1])
for r in rows: print(r["md5"][:8], r["size"], r["path"])
