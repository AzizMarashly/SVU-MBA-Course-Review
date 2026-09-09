# -*- coding: utf-8 -*-
"""Build bank.json + out.html and publish the HTML to the course folder as <title>_vNN.html (§0e).
The previous version is moved to ../archive/. Usage (from render/): python release.py
Bump ../VERSION (two digits) and add a row to ../VERSIONS.md first."""
import os, re, shutil, subprocess, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, ".."); PROJ = os.path.join(WORK, "..")
ver = open(os.path.join(WORK, "VERSION"), encoding="utf-8").read().strip()
assert re.fullmatch(r"\d\d", ver), "VERSION must be two digits (e.g. 01)"
env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
subprocess.run([sys.executable, os.path.join(HERE, "build_bank.py")], check=True, env=env)
subprocess.run([sys.executable, os.path.join(HERE, "render_html.py")], check=True, env=env)
title = json.load(open(os.path.join(WORK, "bank.json"), encoding="utf-8"))["title"]
html = f"{title}_v{ver}.html"
arch = os.path.join(WORK, "archive"); os.makedirs(arch, exist_ok=True)
pat = re.compile(re.escape(title) + r"_v\d\d\.(html|pdf|docx)$")
for f in os.listdir(PROJ):
    if pat.match(f) and f != html:
        shutil.move(os.path.join(PROJ, f), os.path.join(arch, f)); print("archived", f)
shutil.copyfile(os.path.join(WORK, "out.html"), os.path.join(PROJ, html))
print("published", html)
