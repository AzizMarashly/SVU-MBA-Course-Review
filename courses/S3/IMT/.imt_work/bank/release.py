# -*- coding: utf-8 -*-
"""Build bank.json + out.html and publish them to the project folder with the version from ../VERSION
in the file names. Older versioned copies are moved to ../../_old_versions/ so only the latest is shared.
Usage (from .imt_work/bank):  python release.py
Bump the version first by editing ../VERSION and adding a line to ../CHANGELOG.md."""
import os, re, shutil, subprocess, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, ".."); PROJ = os.path.join(WORK, "..")
ver = open(os.path.join(WORK, "VERSION"), encoding="utf-8").read().strip()
env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
subprocess.run([sys.executable, os.path.join(HERE, "build_bank.py")], check=True, env=env)
subprocess.run([sys.executable, os.path.join(HERE, "render_html.py")], check=True, env=env)
title = json.load(open(os.path.join(WORK, "bank.json"), encoding="utf-8"))["title"]
html = f"{title}_v{ver}.html"; bank = f"{title}_v{ver}_bank.json"
old_dir = os.path.join(PROJ, "_old_versions"); os.makedirs(old_dir, exist_ok=True)
pat = re.compile(re.escape(title) + r"(_v[\d.]+)?(_bank\.json|\.html)$")
for f in os.listdir(PROJ):
    if pat.match(f) and f not in (html, bank):
        shutil.move(os.path.join(PROJ, f), os.path.join(old_dir, f)); print("archived", f)
shutil.copyfile(os.path.join(WORK, "out.html"), os.path.join(PROJ, html))
shutil.copyfile(os.path.join(WORK, "bank.json"), os.path.join(PROJ, bank))
print("published", html, "and", bank)
