# -*- coding: utf-8 -*-
"""Publish a course's build output to its GitHub Pages folder.

    python scripts/publish_page.py S3/PRM        (from anywhere)

Copies  courses/S<n>/<CODE>/.review_generation_working_directory/out.html
to      S<n>/<CODE>/index.html
and appends the Cloudflare Web Analytics snippet (taken from the home page index.html, so
there is one place to change the token). The published page is therefore out.html + snippet,
never byte-identical to out.html. Then run scripts/build_course_index.py.
Exit code 1 if the page was unchanged, 2 on error.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = ".review_generation_working_directory"
SNIPPET_RE = re.compile(r"<!-- Cloudflare Web Analytics -->.*?<!-- End Cloudflare Web Analytics -->", re.S)


def snippet():
    home = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    m = SNIPPET_RE.search(home)
    if not m:
        sys.exit("home page index.html has no Cloudflare snippet")
    return m.group(0)


def main(argv):
    if len(argv) != 2 or not re.fullmatch(r"S\d+/[A-Z0-9]+/?", argv[1]):
        sys.exit(__doc__)
    rel = argv[1].strip("/")
    src = os.path.join(ROOT, "courses", rel, WORK, "out.html")
    dst = os.path.join(ROOT, rel, "index.html")
    if not os.path.isfile(src):
        print("no build output:", src); return 2
    page = io.open(src, encoding="utf-8").read()
    if SNIPPET_RE.search(page) is None:
        line = snippet() + "\n"
        i = page.rfind("</body>")
        if i >= 0:   # inside <body>, right before the closing tags
            page = page[:i] + line + page[i:]
        else:        # page without closing tags: append
            page = page.rstrip("\n") + "\n" + line
    old = io.open(dst, encoding="utf-8").read() if os.path.isfile(dst) else None
    if old == page:
        print("unchanged:", os.path.relpath(dst, ROOT)); return 1
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)
    print("published:", os.path.relpath(dst, ROOT), f"({len(page.encode('utf-8'))} bytes)")
    print("now run: python scripts/build_course_index.py")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
