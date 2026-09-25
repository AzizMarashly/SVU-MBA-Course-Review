# -*- coding: utf-8 -*-
"""Candidate extraction methods for the evaluation. Each returns the text of ONE page."""
import re, unicodedata, os, subprocess, io
import pymupdf

# ---------------------------------------------------------------- normalisers on plain text
ALEFS = "اأإآ"

def prm_fix(t):
    """The fix used for PRM/MIS (extract_book.py)."""
    return re.sub("ا([أإآا])ل", r"ال\1", t)

def nfkc(t):
    return unicodedata.normalize("NFKC", t)

def naive_fix(t):
    """Plain-text heuristic without geometry: article + reversed ligature (PRM rule), plus a reversed
    pair inside a word where a genuine 'ال' is impossible: alef-with-hamza followed by lam inside a word
    (…أل…, …إل…, …آل… after a letter) is almost always a reversed ligature; 'اال' anywhere is too."""
    t = re.sub("ا([أإآا])ل", r"ال\1", t)                       # اإلجابات -> الإجابات
    t = re.sub(r"(?<=[\u0621-\u064A])([أإآ])ل", r"ل\1", t)      # بأل.. inside a word (rare genuine cases lost)
    return t

# ---------------------------------------------------------------- PyMuPDF plain variants
def mupdf_text(page, sort=False, flags=None):
    if flags is None:
        return page.get_text("text", sort=sort)
    return page.get_text("text", sort=sort, flags=flags)

# ---------------------------------------------------------------- rawdict reconstruction (geometry-aware)
RTL_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")
LTR_RE = re.compile(r"[A-Za-z\u00C0-\u024F]")
DIGIT_RE = re.compile(r"[0-9\u0660-\u0669\u06F0-\u06F9]")
ARABIC_DIGIT = re.compile(r"[\u0660-\u0669\u06F0-\u06F9]")
LIG_REV = {"ال": "لا", "أل": "لأ", "إل": "لإ", "آل": "لآ"}

def _glyph_groups(chars):
    """Group rawdict chars that belong to one glyph. When a font maps the lam-alef ligature glyph to
    the two code points alef+lam (in that wrong order), MuPDF emits the alef with a bbox NESTED inside
    the lam's bbox (SimplifiedArabic: a zero-width box at the glyph's right edge; Times New Roman: a
    narrower box with the same right edge). Two genuine consecutive glyphs never nest, so the nested
    pair identifies the ligature and is rewritten as lam+alef. Returns [text, x0, x1, ox, y0, y1]."""
    groups = []
    for c in chars:
        x0, y0, x1, y1 = c["bbox"]
        ox = c["origin"][0]
        if groups and c["c"] == "ل" and groups[-1][0] in ALEFS:
            p = groups[-1]
            if p[1] >= x0 - 0.15 and p[2] <= x1 + 0.15 and (p[2] - p[1]) < (x1 - x0):
                p[0] = "ل" + p[0]; p[1] = min(p[1], x0); p[2] = max(p[2], x1); p[4] = min(p[4], y0); p[5] = max(p[5], y1)
                continue
        groups.append([c["c"], x0, x1, ox, y0, y1])
    return groups

def _is_rtl(ch): return bool(RTL_RE.match(ch)) and not DIGIT_RE.match(ch)
def _is_ltr(ch): return bool(LTR_RE.match(ch))
def _is_num(ch): return bool(DIGIT_RE.match(ch))

def _logical_order(groups, space_gap=0.2):
    """groups in any order -> logical text. Decide the base direction, sort visually, then reverse the
    embedded runs of the opposite direction."""
    txt_all = "".join(g[0] for g in groups)
    n_rtl = sum(1 for ch in txt_all if _is_rtl(ch)); n_ltr = sum(1 for ch in txt_all if _is_ltr(ch))
    rtl_base = n_rtl > 0   # an Arabic book: any Arabic on the line makes it an RTL line
    # sort by the glyph's right edge for RTL (visual right-to-left), left edge for LTR
    if rtl_base:
        vis = sorted(groups, key=lambda g: -(g[1] + g[2]) / 2)
    else:
        vis = sorted(groups, key=lambda g: (g[1] + g[2]) / 2)
    # embedded runs: in an RTL base, LTR letters and digits (plus neutrals between them) read LTR
    def is_embedded(t):
        if rtl_base:
            return any(_is_ltr(ch) or _is_num(ch) for ch in t)
        return any(_is_rtl(ch) for ch in t)
    def is_neutral(t):
        return not any(_is_ltr(ch) or _is_num(ch) or _is_rtl(ch) for ch in t) and t.strip() != ""
    out = []
    i = 0
    while i < len(vis):
        if is_embedded(vis[i][0]):
            j = i
            last = i
            while j < len(vis):
                if is_embedded(vis[j][0]):
                    last = j; j += 1
                elif is_neutral(vis[j][0]) or vis[j][0] == " ":
                    # keep going only if another embedded glyph follows before a space+RTL
                    k = j
                    while k < len(vis) and (is_neutral(vis[k][0]) or vis[k][0] == " "):
                        k += 1
                    if k < len(vis) and is_embedded(vis[k][0]) and not (rtl_base and vis[j][0] == " " and _is_num(vis[k][0][0]) and any(_is_num(c) for c in vis[last][0]) and False):
                        j = k
                    else:
                        break
                else:
                    break
            run = list(reversed(vis[i:last + 1]))
            # inside an embedded run, digits/letters were already sorted the other way; reversing fixes it
            out.extend(run)
            i = last + 1
        else:
            out.append(vis[i]); i += 1
    # build text; insert a space when two consecutive glyphs are far apart (cell gap) and no space exists
    s = []
    prev = None
    for g in out:
        if prev is not None and prev[0] != " " and g[0] != " ":
            gap = (prev[1] - g[2]) if rtl_base else (g[1] - prev[2])
            h = max(prev[5] - prev[4], 1)
            if gap > 0.6 * h:
                s.append("  ")
            elif gap > space_gap * h:
                s.append(" ")
        s.append(g[0]); prev = g
    return "".join(s)

def mupdf_rtl(page, flags=None, row_merge=True, space_gap=0.2):
    kw = {} if flags is None else {"flags": flags}
    rd = page.get_text("rawdict", **kw)
    lines = []
    for b in rd["blocks"]:
        if b.get("type", 0) != 0:
            continue
        for l in b["lines"]:
            chars = [c for s in l["spans"] for c in s["chars"]]
            if not chars:
                continue
            groups = _glyph_groups(chars)
            # kashida: a "letter" glyph about 1 pt wide inside a word is the tatweel glyph mis-mapped
            h = max(max(g[5] for g in groups) - min(g[4] for g in groups), 1)
            for g in groups:
                if RTL_RE.match(g[0]) and len(g[0]) == 1 and (g[2] - g[1]) < 0.08 * h and g[0] != " ":
                    g[0] = "ـ"
            if not "".join(g[0] for g in groups).strip():
                continue
            x0 = min(g[1] for g in groups); x1 = max(g[2] for g in groups)
            y0 = min(g[4] for g in groups); y1 = max(g[5] for g in groups)
            lines.append([y0, y1, x0, x1, groups])
    if not lines:
        return ""
    lines.sort(key=lambda r: ((r[0] + r[1]) / 2, -r[3]))
    rows = []
    for r in lines:
        if rows and row_merge:
            last = rows[-1]
            ov = min(last[1], r[1]) - max(last[0], r[0])
            if ov > 0.5 * min(last[1] - last[0], r[1] - r[0]):
                last[2].extend(r[4]); last[0] = min(last[0], r[0]); last[1] = max(last[1], r[1])
                continue
        rows.append([r[0], r[1], list(r[4])])
    out = []
    prev_bot = None
    for y0, y1, groups in rows:
        line = _logical_order(groups, space_gap=space_gap)
        line = re.sub(r"[ ]{3,}", "  ", line).strip()
        if prev_bot is not None and y0 - prev_bot > 0.9 * (y1 - y0):
            out.append("")
        out.append(line); prev_bot = y1
    return "\n".join(out) + "\n"

# ---------------------------------------------------------------- final text cleanup (course-neutral)
DIAC = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")
def clean(t, digits_ascii=True, strip_tatweel=True):
    t = nfkc(t)
    t = t.replace("\u200f", "").replace("\u200e", "").replace("\ufeff", "").replace("\u200b", "")
    if strip_tatweel:
        t = t.replace("\u0640", "")
    if digits_ascii:
        t = t.translate({0x660 + i: ord("0") + i for i in range(10)})
        t = t.translate({0x6F0 + i: ord("0") + i for i in range(10)})
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t

# ---------------------------------------------------------------- pdfminer
def pdfminer_text(pdf, pno):
    from pdfminer.high_level import extract_text
    return extract_text(pdf, page_numbers=[pno - 1])

def pdfplumber_text(pdf, pno):
    import pdfplumber
    with pdfplumber.open(pdf) as d:
        return d.pages[pno - 1].extract_text() or ""

# ---------------------------------------------------------------- OCR
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tessdata")

def tesseract_text(png, lang="ara+eng", psm=3):
    base = png + f".tess{psm}"
    subprocess.run([TESS, png, base, "-l", lang, "--tessdata-dir", TESSDATA, "--psm", str(psm)], capture_output=True)
    return open(base + ".txt", encoding="utf-8").read()

def winocr_dir(png_dir, out_dir):
    ps1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "winocr.ps1")
    os.makedirs(out_dir, exist_ok=True)
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1, "-Dir", png_dir, "-OutDir", out_dir],
                       capture_output=True, text=True)
    return r.stdout + r.stderr
