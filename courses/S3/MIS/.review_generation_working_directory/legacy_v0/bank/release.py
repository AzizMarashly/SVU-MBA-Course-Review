# -*- coding: utf-8 -*-
"""Build out.html and bank.json in the working directory, and the versioned deliverable in the
course folder (<TITLE>_v<VERSION>.html). Bump ../VERSION and add a line to ../CHANGELOG.md first.

    set PYTHONUTF8=1 && python release.py

Then, at the repository root:  python scripts/publish_page.py S3/MIS  and  python scripts/build_course_index.py
"""
import io, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.dirname(HERE); COURSE = os.path.dirname(WORK)
ver = io.open(os.path.join(WORK, 'VERSION'), encoding='utf-8').read().strip()
env = dict(os.environ, PYTHONUTF8='1')
subprocess.run([sys.executable, 'build_html.py'], cwd=HERE, check=True, env=env)
subprocess.run([sys.executable, 'build_bank.py'], cwd=HERE, check=True, env=env)
from build_docx import TITLE  # noqa: E402
built = os.path.join(HERE, TITLE + '.html')
page = io.open(built, encoding='utf-8', newline='').read().replace('\r\n', '\n')
os.remove(built)
out = os.path.join(WORK, 'out.html')
io.open(out, 'w', encoding='utf-8', newline='\n').write(page)
deliv = os.path.join(COURSE, '%s_v%s.html' % (TITLE, ver))
shutil.copyfile(out, deliv)
print('out.html:', len(page.encode('utf-8')), 'bytes ->', os.path.relpath(deliv, COURSE))
