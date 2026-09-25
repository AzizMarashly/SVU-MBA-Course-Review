# -*- coding: utf-8 -*-
"""Render bank.json -> single self-contained RTL HTML review file (ACM review, spec v0.12). Adapted from PRM/MIS; course specifics in
meta_acm.py. v0.12 additions: scope banner, Methods block (§7e), step-by-step reveal and figures (A.6), full model answers (§7b),
fast route, cross-linked cards and «also asked as» lines (§5a), Essentials view (A.4)."""
import json, os, re, html, collections
HERE = os.path.dirname(__file__)
B = json.load(open(os.path.join(HERE, "..", "bank.json"), encoding="utf-8"))
QS = B["questions"]; SUBS = {int(k): v for k, v in B["subsections"].items()}
CHAPTERS = sorted(int(k) for k in B["subsections"])
OPENERS_BANK = {int(k): tuple(v) for k, v in B.get("openers", {}).items()}
METHODS_BANK = {int(k): v for k, v in B.get("methods", {}).items()}
FOCUS = set(tuple(x) for x in B["focus_areas"])
TITLE = B["title"]; SPEC = B["spec_version"]; VER = B["file_version"]
LETTERS = ["أ", "ب", "ج", "د", "هـ", "و"]
from meta_acm import *  # noqa: course tables
CHAPTERS = sorted(int(k) for k in B["subsections"])  # override meta: chapters present in the bank
TODAY = GENERATED_DATE
try:
    QA = json.load(open(os.path.join(HERE, "..", "qa", "summary.json"), encoding="utf-8"))
except FileNotFoundError:
    QA = {}
BYID = {q["id"]: q for q in QS}
ALIAS = {a: q["id"] for q in QS for a in q.get("aliases", [])}

def esc(s): return html.escape(str(s) if s is not None else "", quote=True)
def md(s):
    s = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
def stars(n): return "★"*n + "☆"*(5-n)
def fmt(x):
    if isinstance(x, float) and x.is_integer(): x = int(x)
    return f"{x:,}" if isinstance(x, int) and abs(x) >= 1000 else str(x)

def render_table(t, cls):
    """Data table of a question (§7d): header row; numeric/code cells left-to-right, Arabic cells right-to-left."""
    if not t: return ""
    cell = (lambda c: f'<td class="ltr">{esc(c)}</td>') if t["ltr"] else (lambda c: f'<td>{esc(c)}</td>')
    cap = f'<caption>{esc(t["caption"])}</caption>' if t["caption"] else ""
    head = "".join(f'<th>{abbr(esc(h))}</th>' for h in t["head"])
    body = "".join("<tr>" + "".join(cell(c) for c in r) + "</tr>" for r in t["rows"])
    return f'<div class="tw"><table class="{cls}">{cap}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

_SYM_RE = re.compile(r"(?<![A-Za-z])([A-Z][A-Za-z]{0,4})(?![A-Za-z])")
def symbols_used(q):
    texts = []
    for t in (q.get("table"), q.get("ans_table")):
        if t: texts.append(" ".join(str(h) for h in t["head"]))
    c = q.get("calc")
    if c:
        texts += c["given"] + [st["what"] + " " + st["eq"] for st in c["steps"]]
    if q.get("fast"): texts.append(q["fast"])
    seen, out = set(), []
    for tok in _SYM_RE.findall(" ".join(texts)):
        if tok in SYMBOLS and tok not in seen:
            seen.add(tok); out.append(tok)
    return out

def sym_lines(k):
    d = SYMBOLS[k]
    return [d["ar"] + " (" + d["en"] + ")"] + ([d["f"]] if d["f"] else []) + [d["note"], "مثال: " + d["ex"]]

def abbr(text):
    if not SYMBOLS: return text
    def w(m):
        k = m.group(1)
        if k not in SYMBOLS: return m.group(0)
        return f'<abbr data-k="{k}" title="{esc(chr(10).join(sym_lines(k)))}">{k}</abbr>'
    return _SYM_RE.sub(w, text)

def render_symbols(q, cls):
    syms = symbols_used(q)
    if not syms: return ""
    chips = []
    for k in syms:
        d = SYMBOLS[k]
        f = f'<span class="p-f ltr">{esc(d["f"])}</span>' if d["f"] else ""
        chips.append(f'<span class="chip" data-k="{esc(k)}" role="button" tabindex="0"><b class="ltr">{esc(k)}</b> {esc(d["ar"])}'
                     f'<span class="pop"><span class="p-ar"><b class="ltr">{esc(k)}</b> = {esc(d["ar"])}</span>'
                     f'<span class="p-en ltr">{esc(d["en"])}</span>{f}<span class="p-n">{esc(d["note"])}</span><span class="p-x">مثال: {esc(d["ex"])}</span></span></span>')
    return f'<div class="{cls}"><span class="slbl">الرموز:</span> {"".join(chips)} <span class="shint">اضغط على أي رمز للشرح الكامل</span></div>'

SYM_JS = r"""(function(){
var sheet=document.getElementById('symsheet');if(!sheet)return;
var body=sheet.querySelector('.sh-body'),nav=sheet.querySelector('.sh-nav');
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function show(k,q){var d=window.SYMS[k];if(!d)return;
 body.innerHTML='<span class="p-ar"><b class="ltr">'+esc(k)+'</b> = '+esc(d.ar)+'</span><span class="p-en ltr">'+esc(d.en)+'</span>'+(d.f?'<span class="p-f">'+esc(d.f)+'</span>':'')+'<span class="p-n">'+esc(d.note)+'</span><span class="p-x">مثال: '+esc(d.ex)+'</span>';
 nav.innerHTML='';var chips=q?q.querySelectorAll('.syms .chip'):[];
 if(chips.length>1){nav.innerHTML='<span class="slbl">رموز هذا السؤال:</span> ';chips.forEach(function(c){var kk=c.getAttribute('data-k');var b=document.createElement('span');b.className='chip'+(kk===k?' open':'');b.setAttribute('data-k',kk);b.textContent=kk;nav.appendChild(b);});}
 sheet.hidden=false;}
function close(){sheet.hidden=true;}
document.addEventListener('click',function(e){
 var t=e.target.closest('.syms .chip, abbr[data-k], #symsheet .sh-nav .chip');
 if(t){e.preventDefault();var q=t.closest('.q')||sheet._q;sheet._q=q;show(t.getAttribute('data-k'),q);return;}
 if(e.target.closest('.sh-x')||(e.target===sheet))close();});
document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
})();"""

def method_link(ch, key):
    for m in METHODS_BANK.get(ch, []):
        if m["key"] == key:
            return f'<a class="mlink" href="#m{ch}-{esc(key)}">{esc(key)} · {esc(m["name"])}</a>'
    return esc(key)

def render_calc(c, ch, qid):
    """Calculation block (§7d) with step-by-step reveal (A.6): given values and the first step visible, steps 2..n each a collapsed
    <details>, a «Show all steps» control (JS), and the last step opening the working table."""
    if not c: return ""
    out = ['<div class="calc"><p class="a-calc"><span class="lbl">الحساب:</span>' + (f' <span class="meta">الطريقة: {method_link(ch, c["method"])}</span>' if c["method"] else "") + '</p>']
    if c["given"]:
        out.append('<ul class="given">' + "".join(f'<li>{abbr(md(g))}</li>' for g in c["given"]) + "</ul>")
    def row(i, st):
        note = f'<div class="cnote">{md(st["note"])}</div>' if st["note"] else ""
        return (f'<table class="ctbl"><thead><tr><th>المطلوب</th><th>المعادلة</th><th>التعويض</th><th>الناتج</th></tr></thead><tbody>'
                f'<tr><td class="cwhat" data-l="المطلوب">{i}. {abbr(md(st["what"]))}</td>'
                f'<td class="ltr ceq" data-l="المعادلة"><span>{abbr(esc(st["eq"]))}</span></td>'
                f'<td class="ltr csub" data-l="التعويض"><span>{esc(st["sub"])}</span></td>'
                f'<td class="cres" data-l="الناتج"><b>{esc(st["res"])}</b>{note}</td></tr></tbody></table>')
    steps = c["steps"]
    out.append('<div class="tw steps">' + row(1, steps[0]) + "</div>")
    if len(steps) > 1:
        out.append(f'<button type="button" class="chip jsonly showsteps" data-for="{esc(qid)}">إظهار كل الخطوات ({len(steps)})</button>')
        for i, st in enumerate(steps[1:], 2):
            out.append(f'<details class="step"><summary>الخطوة {i}: {abbr(md(st["what"]))}</summary><div class="tw">{row(i, st)}</div></details>')
    if c["note"]: out.append(f'<p class="cfinal">{md(c["note"])}</p>')
    out.append("</div>")
    return "".join(out)

FIG_POINTS = ["أ", "ب"]
def fig_parts(f):
    """Numbered names used when a figure hides its labels (hide_labels=True): lines in drawing order, points left to right."""
    lines = [("الإيرادات الكلية", None), ("التكاليف الكلية", None), ("التكاليف الثابتة", f["fixed"])]
    if f.get("cash_fixed"):
        lines += [("التكاليف الثابتة النقدية", f["cash_fixed"]), ("التكاليف الكلية النقدية", None)]
    pts = []
    if f.get("cash_fixed"): pts.append(("نقطة الإغلاق المؤقت", f["cash_fixed"] / (f["price"] - f["var"])))
    pts.append(("نقطة التعادل", f["fixed"] / (f["price"] - f["var"])))
    return lines, pts

def fig_key(q):
    """Answer-block key of a figure drawn with hide_labels (A.6: the text answer stays complete for a reader who cannot see the figure)."""
    f = q.get("fig")
    if not f or not f.get("hide_labels"): return ""
    lines, pts = fig_parts(f)
    ls = "، ".join(f"الخط {i} = {n}" + (f" ({fmt(v)} ل.س)" if v else "") for i, (n, v) in enumerate(lines, 1))
    ps = "، ".join(f"النقطة {FIG_POINTS[i]} = {n} ({fmt(round(v))} وحدة)" for i, (n, v) in enumerate(pts))
    return (f'<p class="a-key"><span class="lbl">مفتاح الشكل:</span> {ls}؛ {ps}؛ المحور ع = المبالغ (الإيرادات والتكاليف، ل.س)، '
            f'المحور س = حجم النشاط (الكمية).</p>')

def render_fig(q):
    """Inline SVG drawn from the record's data (A.6). kind cvp: revenue, total cost, fixed cost lines, break-even point; optional cash
    lines and shutdown point; optional margin-of-safety band. LTR coordinate space; labels >= 12 px; scales to the card width.
    hide_labels=True (chart questions that ask the reader to name a line or point): numbered markers only («الخط 1», «النقطة أ»), no
    names and no values, a neutral text alternative; the names go to the answer block (fig_key)."""
    f = q.get("fig")
    if not f: return ""
    P, V, FC = f["price"], f["var"], f["fixed"]; beq = FC / (P - V)
    cfc = f.get("cash_fixed"); sq = f.get("sales_q")
    hide = bool(f.get("hide_labels"))
    qmax = f.get("qmax") or max(beq * 2, (sq or 0) * 1.15)
    ymax = max(P * qmax, FC + V * qmax) * 1.08
    W, H, L, Bm, T, R = 640, 380, 104, 62, 18, 20
    sx = lambda x: L + (x / qmax) * (W - L - R)
    sy = lambda y: H - Bm - (y / ymax) * (H - Bm - T)
    hl = f.get("highlight", "be")
    lines, pts = fig_parts(f)
    if hide:
        alt = (f"مخطط تعادل بـ{len(lines)} خطوط مرقمة ونقطتين (أ، ب) بلا مسميات ولا قيم، كما في الامتحان؛ مفتاح الشكل في الإجابة."
               if len(pts) > 1 else f"مخطط تعادل بـ{len(lines)} خطوط مرقمة ونقطة (أ) بلا مسميات ولا قيم؛ مفتاح الشكل في الإجابة.")
        title = alt
    else:
        alt = f.get("alt") or "مخطط التعادل: خط الإيرادات وخط التكاليف الكلية وخط التكاليف الثابتة ونقطة التعادل"
        title = f.get("alt") or "مخطط التعادل"
    parts = [f'<svg class="fig" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(alt)}" xmlns="http://www.w3.org/2000/svg">']
    parts.append(f'<title>{esc(title)}</title>')
    if sq and hl == "safety":
        parts.append(f'<rect x="{sx(min(beq, sq)):.1f}" y="{T}" width="{abs(sx(sq) - sx(beq)):.1f}" height="{H - Bm - T}" class="f-band"/>')
    parts.append(f'<line x1="{L}" y1="{sy(0):.1f}" x2="{W - R}" y2="{sy(0):.1f}" class="f-axis"/><line x1="{L}" y1="{T}" x2="{L}" y2="{sy(0):.1f}" class="f-axis"/>')
    if hide:
        parts.append(f'<text x="{L + 4}" y="{H - 8}" class="f-lbl">س</text><text x="{L - 6}" y="{T + 4}" class="f-lbl" text-anchor="end">ع</text>')
    else:
        parts.append(f'<text x="{W - R}" y="{H - 6}" class="f-lbl" text-anchor="end">الكمية (وحدة)</text><text x="{L - 6}" y="{T + 4}" class="f-lbl" text-anchor="start">ل.س</text>')
    lname = lambda i, txt: f"الخط {i}" if hide else txt
    # revenue, total cost, fixed
    parts.append(f'<line x1="{sx(0):.1f}" y1="{sy(0):.1f}" x2="{sx(qmax):.1f}" y2="{sy(P * qmax):.1f}" class="f-rev"/>')
    parts.append(f'<line x1="{sx(0):.1f}" y1="{sy(FC):.1f}" x2="{sx(qmax):.1f}" y2="{sy(FC + V * qmax):.1f}" class="f-tc"/>')
    parts.append(f'<line x1="{sx(0):.1f}" y1="{sy(FC):.1f}" x2="{sx(qmax):.1f}" y2="{sy(FC):.1f}" class="f-fc"/>')
    parts.append(f'<text x="{sx(qmax) - 4:.1f}" y="{sy(P * qmax) + 14:.1f}" class="f-lbl f-rev-t" text-anchor="end">{lname(1, "الإيرادات الكلية")}</text>')
    parts.append(f'<text x="{sx(qmax) - 4:.1f}" y="{sy(FC + V * qmax) - 6:.1f}" class="f-lbl f-tc-t" text-anchor="end">{lname(2, "التكاليف الكلية")}</text>')
    parts.append(f'<text x="{sx(qmax) - 4:.1f}" y="{sy(FC) - 6:.1f}" class="f-lbl f-fc-t" text-anchor="end">{lname(3, "التكاليف الثابتة = " + fmt(FC))}</text>')
    if cfc:
        sp = cfc / (P - V)
        parts.append(f'<line x1="{sx(0):.1f}" y1="{sy(cfc):.1f}" x2="{sx(qmax):.1f}" y2="{sy(cfc):.1f}" class="f-cfc"/>')
        parts.append(f'<line x1="{sx(0):.1f}" y1="{sy(cfc):.1f}" x2="{sx(qmax):.1f}" y2="{sy(cfc + V * qmax):.1f}" class="f-ctc"/>')
        parts.append(f'<text x="{sx(qmax) - 4:.1f}" y="{sy(cfc) + 16:.1f}" class="f-lbl f-cfc-t" text-anchor="end">{lname(4, "التكاليف الثابتة النقدية = " + fmt(cfc))}</text>')
        parts.append(f'<text x="{sx(qmax) - 4:.1f}" y="{sy(cfc + V * qmax) + 16:.1f}" class="f-lbl f-ctc-t" text-anchor="end">{lname(5, "التكاليف الكلية النقدية")}</text>')
        big = 8 if hl == "shutdown" else 5
        parts.append(f'<line x1="{sx(sp):.1f}" y1="{sy(P * sp):.1f}" x2="{sx(sp):.1f}" y2="{sy(0):.1f}" class="f-drop"/><circle cx="{sx(sp):.1f}" cy="{sy(P * sp):.1f}" r="{big}" class="f-pt f-sp{" f-hl" if hl == "shutdown" else ""}"/>')
        if hide:
            parts.append(f'<text x="{sx(sp) - 12:.1f}" y="{sy(P * sp) - 10:.1f}" class="f-lbl f-ptn" text-anchor="middle">{FIG_POINTS[0]}</text>')
        else:
            dy = 38 if abs(sx(sp) - sx(beq)) < 150 else 18   # second row when the two points are close
            parts.append(f'<text x="{sx(sp):.1f}" y="{sy(0) + dy:.1f}" class="f-lbl" text-anchor="middle">نقطة الإغلاق {fmt(round(sp))}</text>')
    big = 8 if hl in ("be", "lines") else 5
    if hide and hl == "lines": big = 5
    parts.append(f'<line x1="{sx(beq):.1f}" y1="{sy(P * beq):.1f}" x2="{sx(beq):.1f}" y2="{sy(0):.1f}" class="f-drop"/><line x1="{L}" y1="{sy(P * beq):.1f}" x2="{sx(beq):.1f}" y2="{sy(P * beq):.1f}" class="f-drop"/>')
    parts.append(f'<circle cx="{sx(beq):.1f}" cy="{sy(P * beq):.1f}" r="{big}" class="f-pt f-be{" f-hl" if hl == "be" else ""}"/>')
    if hide:
        parts.append(f'<text x="{sx(beq) - 12:.1f}" y="{sy(P * beq) - 10:.1f}" class="f-lbl f-ptn" text-anchor="middle">{FIG_POINTS[len(pts) - 1]}</text>')
    else:
        parts.append(f'<text x="{sx(beq):.1f}" y="{sy(0) + 18:.1f}" class="f-lbl f-be-t" text-anchor="middle">نقطة التعادل {fmt(round(beq))}</text>')
        parts.append(f'<text x="{L - 6}" y="{sy(P * beq) + 4:.1f}" class="f-lbl" text-anchor="end">{fmt(round(P * beq))}</text>')
    if sq:
        parts.append(f'<line x1="{sx(sq):.1f}" y1="{sy(P * sq):.1f}" x2="{sx(sq):.1f}" y2="{sy(0):.1f}" class="f-drop"/><text x="{sx(sq):.1f}" y="{sy(0) + 38:.1f}" class="f-lbl" text-anchor="middle">المبيعات {fmt(sq)}</text>')
        if hl == "safety":
            parts.append(f'<text x="{(sx(sq) + sx(beq)) / 2:.1f}" y="{T + 16}" class="f-lbl f-hl-t" text-anchor="middle">هامش الأمان = {fmt(round(abs(sq - beq)))}</text>')
    parts.append("</svg>")
    cap = alt if hide else (f.get("alt") or "مخطط التعادل مرسوم من بيانات السؤال")
    return f'<figure class="figw">{"".join(parts)}<figcaption class="meta">{esc(cap)}</figcaption></figure>'

def render_q(q, num, sec):
    # A figure that is part of the question (a chart with numbered, unnamed lines) goes under the stem; a figure that draws the
    # solution (break-even, shutdown, margin of safety values) goes into the answer block, after the calculation.
    stem_fig = bool(q.get("fig") and q["fig"].get("hide_labels"))
    types = q["types"]
    tags = " ".join(f'<span class="tag t-{t}">{SEC_NAMES[t] if t!="generated" else "مولَّد"}</span>' for t in types)
    data_sec = " ".join(types)
    if "generated" in types:
        srcs = 'المصدر: مولَّد لسد فجوة (البند 9 من المواصفة)'
    else:
        srcs = "المصادر: " + "، ".join(f'{esc(SRC_NAMES.get(s, s))} <a class="srcref" href="#src-{SRC_ROW[s]}" title="ملف المصدر رقم {SRC_ROW[s]} في ملحق ملفات المصدر">#{SRC_ROW[s]}</a>' for s in q["sources"])
        if q.get("see"):
            srcs += ' · <span class="seelink">الادعاء نفسه: ' + "، ".join(f'<a href="#{esc(s)}">{esc(s)}</a>' for s in q["see"]) + ' (التكرار والأهمية مشتركان: مصادر الاتحاد ' + "، ".join(esc(SRC_NAMES.get(c, c)) for c in q.get("union_sources", [])) + ')</span>'
    qt = {"mcq":"اختيار من متعدد","tf":"صح / خطأ","short":"سؤال قصير","essay":"مقالي"}[q["qtype"]]
    recon = ' <span class="tag recon">خيارات معاد بناؤها</span>' if q["reconstructed"] else ""
    lowc = ' <span class="tag lowc">⚠</span>' if q["low_conf"] else ""
    uns = ' <span class="tag uns">حل مولَّد — ليس حلّ الكتاب</span>' if q.get("unsolved") else ""
    meta1 = f'<div class="meta"><span class="qid">{esc(q["id"])}</span> · <span>{qt}</span> · {tags}{recon}{uns}{lowc}</div>'
    freq_txt = "مولَّد — التكرار: 0" if "generated" in types else f'التكرار: {q["freq"]} {"مصدر مستقل" if q["freq"]==1 else "مصادر مستقلة"}'
    meta2 = f'<div class="meta"><span>{freq_txt}</span> · <span class="imp" title="الأهمية {q["importance"]}/5">{stars(q["importance"])} <small>{q["importance"]}/5</small></span> · <span>الفقرة {esc(q["sub"])}: {esc(q["subname"])}</span></div>'
    stem = f'<p class="stem"><span class="num">{num}.</span> {esc(q["stem"])}</p>' + render_table(q.get("table"), "qtbl") + (render_fig(q) if stem_fig else "")
    if q.get("table") or q.get("calc") or q.get("ans_table") or q.get("fig"):
        stem += render_symbols(q, "syms")
    opts = ""
    if q["qtype"] == "mcq":
        opts = '<ol class="opts">' + "".join(f'<li><span class="let">{LETTERS[i]})</span> {esc(o)}</li>' for i, o in enumerate(q["options"])) + "</ol>"
    elif q["qtype"] == "tf":
        opts = '<p class="opts tf">( صح / خطأ )</p>'
    orig = f'<p class="orig">نص الطالب الأصلي: {esc(q["original"])}</p>' if q["original"] else ""
    ans_line = f'{LETTERS[q["ans"]]} — {esc(q["options"][q["ans"]])}' if q["qtype"] == "mcq" else esc(q["ans"])
    lines = [f'<p class="a-ans"><span class="lbl">✔ الإجابة:</span> {ans_line}</p>' + fig_key(q)]
    if q.get("fig") and q["fig"].get("hide_labels") and orig:   # the recalled text names the line: keep it behind the answer
        lines.append(orig); orig = ""
    if q.get("fast"):
        lines.append(f'<p class="a-fast"><span class="lbl">الطريق السريع:</span> {abbr(md(q["fast"]))}</p>')
    at = render_table(q.get("ans_table"), "qtbl atbl")
    if at and q.get("calc") and len(q["calc"]["steps"]) > 1:
        at = f'<details class="more atw"><summary class="jsonly">جدول الحل الكامل</summary>{at}</details>'
    elif at:
        at = f'<details class="more" open><summary class="jsonly">جدول الحل</summary>{at}</details>'
    lines.append(render_calc(q.get("calc"), q["ch"], q["id"]) + at + ("" if stem_fig else render_fig(q)))
    if q.get("model_answer"):
        lines.append(f'<details class="model more"><summary>الإجابة النموذجية الكاملة</summary><div class="mbody">{md(q["model_answer"])}</div></details>')
    lines.append(f'<p class="a-why"><span class="lbl">لماذا:</span> {md(q["why"])}</p>')
    lines.append(f'<p class="a-rem"><span class="lbl">تذكّر:</span> {md(q["remember"])}</p>')
    if q["distractors"]:
        lines.append(f'<details class="more dis" open><summary class="jsonly">المشتتات</summary><p class="a-dis"><span class="lbl">المشتتات:</span> {md(q["distractors"])}</p></details>')
    runs = []
    for p in q["pages"]:
        if runs and p == runs[-1][1] + 1: runs[-1][1] = p
        else: runs.append([p, p])
    pgs = "، ".join(str(a) if a == b else f"{a}–{b}" for a, b in runs)
    lines.append(f'<p class="a-ref"><span class="lbl">المرجع:</span> الفصل {q["ch"]} · ص {pgs} (PDF {pgs})</p>')
    if q["book_says"]:
        lines.append(f'<p class="a-red"><span class="lbl">يقول الكتاب:</span> {md(q["book_says"])}</p>')
    if q["other_source"]:
        lines.append(f'<p class="a-red"><span class="lbl">مصدر آخر:</span> {md(q["other_source"])}</p>')
    if q["sci"]:
        lines.append(f'<p class="a-sci"><span class="lbl">تصحيح علمي:</span> {md(q["sci"])}</p>')
    if q["low_conf"]:
        lines.append(f'<p class="a-amber"><span class="lbl">⚠ ثقة منخفضة:</span> {esc(q["low_conf"])}</p>')
    if q.get("also"):
        also = "".join(f'<li>{esc(a["form"])} · {esc(a["wording"])} · الإجابة: {esc(a["key"])} · {"، ".join(esc(SRC_NAMES.get(c, c)) for c in a["sources"])}</li>' for a in q["also"])
        lines.append(f'<details class="more also" open><summary class="jsonly">سُئل أيضاً بصيغة أخرى</summary><div class="a-also"><span class="lbl">سُئل أيضاً بصيغة أخرى:</span><ul>{also}</ul></div></details>')
    vars_html = ""
    if q["variants"]:
        vars_html = '<details class="vars"><summary>صيغ أخرى في المصادر</summary><ul>' + "".join(f"<li>{esc(v)}</li>" for v in q["variants"]) + "</ul></details>"
    srcline = f'<p class="meta src">{srcs}</p>'
    anchors = "".join(f'<span id="{esc(a)}"></span>' for a in q.get("aliases", []))
    return (f'<article class="q" id="{esc(q["id"])}" data-section="{data_sec}" data-chapter="{q["ch"]}" '
            f'data-importance="{q["importance"]}" data-freq="{q["freq"]}" data-sec="{sec}">{anchors}'
            f'{meta1}{stem}{opts}{orig}{meta2}'
            f'<details class="ans"><summary><span class="show">إظهار الإجابة</span><span class="hide">إخفاء الإجابة</span></summary>'
            f'<div class="ablock">{"".join(lines)}{srcline}{vars_html}</div></details></article>')

def order_key(q):
    return (-q["importance"], -q["freq"], 0 if q["qtype"]=="mcq" else 1, q["id"])

def render_methods(n):
    ms = METHODS_BANK.get(n) or []
    if not ms: return ""
    names = " · ".join(f'{esc(m["key"])} {esc(m["name"])}' for m in ms)
    ents = []
    for m in ms:
        steps = "".join(f'<li>{md(s[0])}<span class="meta"> ← {md(s[1])}</span></li>' for s in m["steps"])
        fast = f'<p class="m-fast"><span class="lbl">الطريق السريع:</span> {md(m["fast"])}</p>' if m.get("fast") else ""
        ents.append(f'<div class="mentry" id="m{n}-{esc(m["key"])}"><h4><span class="mkey ltr">{esc(m["key"])}</span> {esc(m["name"])} <small class="meta">ص {esc(m["page"])}</small></h4>'
                    f'<p class="m-rec"><span class="lbl">كيف تعرفها:</span> {md(m["recognise"])}</p><ol class="m-steps">{steps}</ol>{fast}</div>')
    return (f'<details class="methods"><summary><span class="olbl">طرق الحل في هذا الفصل ({len(ms)}):</span> {names} <span class="tog meta"><span class="hide">طيّ ▲</span><span class="show">فتح ▼</span></span></summary>'
            f'<p class="meta">لكل نوع مسألة طريقة واحدة بخطوات ثابتة كما يعلّمها الكتاب؛ كل حل في هذا الفصل يتبع خطوات طريقته بالترتيب نفسه ويسمّيها.</p>{"".join(ents)}</details>')

def render_chapter(n):
    qs = [q for q in QS if q["ch"]==n]
    about, terms = OPENERS_BANK.get(n) or OPENERS[n]
    ess = sum(1 for q in qs if q["importance"] >= 3)
    note = f'<p class="scopenote">{esc(CH_SCOPE_NOTE[n])}</p>' if n in CH_SCOPE_NOTE else ""
    parts = [f'<section class="chapter" id="ch{n}" data-chapter="{n}"><details class="chd" open><summary><h2>الفصل {n}: {esc(CH_TITLES[n])} <small class="meta">الكتاب ص {CH_PAGES[n][0]}–{CH_PAGES[n][1]} · <span class="cnt" data-total="{len(qs)}" data-ess="{ess}">{len(qs)} سؤالاً</span></small><span class="tog meta"><span class="hide">طيّ ▲</span><span class="show">فتح ▼</span></span></h2></summary>',
             f'<div class="opener"><div class="olbl">في هذا الفصل</div><p>{esc(about)}</p><p>{md(terms)}</p>{note}</div>', render_methods(n)]
    num = 0; done = set()
    for sec in ["exam","textbook","other","generated"]:
        sq = sorted([q for q in qs if sec in q["types"] and q["id"] not in done], key=order_key)
        done.update(q["id"] for q in sq)
        if not sq:
            if sec == "generated":
                parts.append(f'<div class="secnote meta">هذا الفصل لم يحتج إلى أسئلة مولَّدة: جميع فقراته المطلوبة مغطاة بأسئلة حقيقية.</div>')
            continue
        parts.append(f'<details class="secd" data-sec="{sec}" open><summary><h3 class="sech s-{sec}" data-sec="{sec}">{SEC_NAMES[sec]} <small class="meta cnt" data-total="{len(sq)}">({len(sq)})</small><span class="tog meta"><span class="hide">طيّ ▲</span><span class="show">فتح ▼</span></span></h3></summary>')
        if sec in ("other","generated"): parts.append(f'<p class="secintro">{esc(SEC_INTRO[sec])}</p>')
        for q in sq:
            num += 1
            parts.append(render_q(q, num, sec))
        parts.append('</details>')
    parts.append("</details></section>")
    return "\n".join(parts)

def counts():
    c = collections.Counter()
    for q in QS:
        for t in q["types"]: c[t] += 1
    return c

def methodology():
    c = counts()
    recon = sum(1 for q in QS if q["reconstructed"]); lowc = [q["id"] for q in QS if q["low_conf"]]
    gen = sum(1 for q in QS if "generated" in q["types"])
    total_subs = sum(len(v) for v in SUBS.values())
    cs = B.get("coverage_stats", {}); real_cov = cs.get("direct", 0); gen_cov = cs.get("generated_only", 0); unc = cs.get("uncovered", 0); ment = cs.get("mentioned_only", 0)
    focus_rows = [r for r in B["focus_table"] if (r["ch"], r["sub"]) in FOCUS]
    ft = "".join(f'<tr><td>{r["ch"]}</td><td>{esc(r["sub"])}</td><td>{esc(r["name"])}</td><td>{r["exam"]}</td><td>{r["textbook"]}</td><td>{r["other"]}</td><td>{r["total"]}</td></tr>' for r in sorted(focus_rows, key=lambda r:(r["ch"], -r["exam"], -r["total"])))
    led = "".join(f'<tr><td class="ltr">{esc(e["id"])}</td><td>{esc("؛ ".join(e["files"]))}</td><td>{esc(e["type"])}</td><td>{esc(e["decision"])}</td></tr>' for e in B["source_ledger"])
    ledger = f'<table class="tbl"><thead><tr><th>المعرّف</th><th>الملفات</th><th>النوع</th><th>القرار</th></tr></thead><tbody>{led}</tbody></table>'
    cm = "".join(f'<tr><td>{esc(r["source"])}</td><td>{esc(str(r["book_chapter"]))}</td><td>{esc(r["evidence"])}</td></tr>' for r in B["chapter_map"])
    chmap = f'<table class="tbl"><thead><tr><th>تسمية المصدر</th><th>فصل الكتاب</th><th>الدليل</th></tr></thead><tbody>{cm}</tbody></table>'
    unres = "".join(f"<li>{esc(u)}</li>" for u in QA.get("unresolved", []))
    oos = "".join(f"<li>{esc(u)}</li>" for u in QA.get("out_of_scope", []))
    excl = "".join(f"<li><b>{esc(k)}</b>: {esc(v)}</li>" for k, v in B.get("excluded_units", {}).items())
    meth_n = sum(len(v) for v in METHODS_BANK.values()); proc = [n for n, v in METHODS_BANK.items() if v]
    n_tab = sum(1 for q in QS if q.get("table")); n_calc = sum(1 for q in QS if q.get("calc")); n_fig = sum(1 for q in QS if q.get("fig")); n_fast = sum(1 for q in QS if q.get("fast")); n_uns = sum(1 for q in QS if q.get("unsolved")); n_at = sum(1 for q in QS if q.get("ans_table"))
    gen_by_ch = "، ".join(f"الفصل {n}: {sum(1 for q in QS if q['ch'] == n and 'generated' in q['types'])}" for n in CHAPTERS)
    n_see = sum(1 for q in QS if q.get("see")); n_also = sum(1 for q in QS if q.get("also")); n_model = sum(1 for q in QS if q.get("model_answer"))
    return f"""
<section id="method"><h2>المنهجية</h2>
<h3>نطاق دورة F25</h3>
<p>{esc(SCOPE_BANNER)}</p>
<ul>{excl}</ul>
<p>{esc(QA.get("scope_counts", ""))}</p>
<h3>قراءة المرجع وتحقق أداة الاستخراج</h3>
<p>{METHOD_EXTRACTION.format(pages=BOOK_PAGES, images=QA.get("images", "—"))}</p>
<h3>منهاج واحد في المجلد</h3>
<p>{METHOD_CURRICULA}</p>
<h3>سجل المصادر</h3>{ledger}
<h3>خريطة الفصول</h3>{chmap}
<h3>التكرار والتحقق والدمج</h3>
<p>{METHOD_DUP}</p>
<p>عتبة تشابه نص السؤال في فحص البناء: جيب التمام {B.get("similar_stem_threshold", 0.6)} على النص المطبَّع. سجلات مرتبطة بادعاء واحد: <b>{n_see}</b>؛ سطور «سُئل أيضاً بصيغة أخرى»: <b>{n_also}</b>. سجل الدمج في qa/consolidation_v{esc(VER)}.md في المستودع.</p>
<p><b>التحقق المتقاطع مع ملخص عاصم:</b> {esc(QA.get("asem", "ملخص نظري بلا أسئلة؛ استُخدم للتحقق من التعاريف."))}</p>
<h3>إعادة بناء أسئلة الامتحانات</h3>
<p>الأسئلة التي نقلها الطلاب بصيغة حرة («تعريف X»، «جاء سؤال عن Y مع الجواب») وكان واضحاً أنها اختيار من متعدد أُعيد بناؤها بأربعة خيارات من مصطلحات الفصل نفسه، مع وسم «خيارات معاد بناؤها» وإبقاء نص الطالب الأصلي أسفل السؤال؛ حين يكون للكتاب سؤال مراجعة عن الادعاء نفسه أُعيد البناء بصيغة الكتاب. عدد الأسئلة المعاد بناؤها: <b>{recon}</b>. أسئلة الكتاب والمصادر الأخرى بقيت بصيغتها الأصلية.</p>
<h3>الفصول الإجرائية: طرق الحل والأشكال والطريق السريع</h3>
<p>الفصول التي تتكرر فيها مسائل بطريقة حل واحدة ({"، ".join(str(n) for n in proc)}) تبدأ بكتلة «طرق الحل» ({meth_n} طريقة) تسمّي كل نوع مسألة وخطواته بصفحة الكتاب، وكل حل يتبع خطوات طريقته ويسمّي الطريقة. السجلات ذات جدول بيانات: <b>{n_tab}</b>؛ ذات جدول حل كامل: <b>{n_at}</b>؛ ذات كتلة حساب: <b>{n_calc}</b>؛ ذات شكل مرسوم من بيانات السؤال (يعيد البناء حساب نقطة التعادل من البيانات ويفشل عند الاختلاف): <b>{n_fig}</b>؛ ذات «طريق سريع» بقاعدة من الكتاب: <b>{n_fast}</b>؛ تمارين الكتاب غير المحلولة التي حُلّت هنا: <b>{n_uns}</b>؛ أسئلة مقالية بإجابة نموذجية كاملة: <b>{n_model}</b>.</p>
<h3>تدقيق التغطية والأسئلة المولَّدة</h3>
<p>قُسّمت الفصول المطلوبة إلى <b>{total_subs}</b> فقرة وفق فهرس الكتاب (أدقّ مستوى في الفهرس داخل نطاق F25). تُعدّ الفقرة مغطاة فقط بسؤال جوابه المتوقع مصطلح أو قاعدة أو رقم تعرّفه الفقرة نفسها وصفحة مرجعه داخل الفقرة. <b>{real_cov}</b> فقرة سألتها أسئلة حقيقية على محتواها، و<b>{gen_cov}</b> فقرة كُتب لها أسئلة من نص الكتاب (القسم الرابع في كل فصل: <b>{gen}</b> سؤالاً مولَّداً)، و<b>{unc}</b> فقرة بقيت بلا سؤال ({ment} منها مذكورة داخل الشروح فقط). التغطية النهائية: <b>{total_subs - unc} من {total_subs}</b>. وضع التشغيل DECIDE فطُبّقت قاعدته دون سؤال المستخدم عن الحجم (المولَّد لم يتجاوز الحقيقي في أي فصل ولا ثلث البنك: {gen} من {len(QS)}): سؤال مولَّد لكل فقرة ذُكرت في الشروح ولم تُسأل على محتواها، وحتى ثلاثة في كل فصل للفقرات التي لم يذكرها أي سؤال؛ عدد المولَّد في كل فصل: {gen_by_ch}. الفصل 7 أخذ سبعة لأن سبعاً من فقراته (منها FIFO وLIFO وأسلوب النشاط والاستنزاف) لم يسألها أي مصدر. تحقق آلي من أن كل مولَّد يغطي فقرة لا سؤال حقيقي فيها ولا يكرر مولَّداً آخر.</p>
<h3>مجالات التركيز ودرجة الأهمية</h3>
<p>لكل فقرة عُدّت الادعاءات المميزة بحسب الأصل (امتحان / كتاب / أخرى؛ البطاقتان المرتبطتان تُعدّان مرة) ورُتّبت الفقرات بعدد أسئلة الامتحان ثم المجموع. <b>مجال التركيز</b> في كل فصل = الفقرات التي سألتها دورتان أو أكثر، وإن قلّت عن اثنتين أُخذت أعلى فقرتين سألتهما دورة واحدة على الأقل. الدرجة (1–5): الأساس من عدد الدورات المستقلة التي ورد فيها السؤال (0 ← 1، 1 ← 2، 2 ← 3، 3 فأكثر ← 4)، زائد 1 إن كان السؤال أيضاً من أسئلة الكتاب، زائد 1 إن كانت فقرته مجال تركيز، والحد الأقصى 5؛ المولَّد يثبت على 1. الدرجة معونة للدراسة لا توقّع للامتحان.</p>
<table class="tbl"><thead><tr><th>الفصل</th><th>الفقرة</th><th>الاسم</th><th>امتحان</th><th>كتاب</th><th>أخرى</th><th>المجموع</th></tr></thead><tbody>{ft}</tbody></table>
<h3>الثقة المنخفضة</h3>
<p>أُضيف سطر «⚠ ثقة منخفضة» إلى <b>{len(lowc)}</b> سؤالاً فقط: حيث نُقل السؤال من الذاكرة بصيغة قد تعني أمرين، أو اختلفت المصادر ولم يحسمها الكتاب، أو استند الجواب إلى جملة عابرة أو غاب مفهومه عن الكتاب. غياب السطر يعني تحققاً عادياً.</p>
<h3>أسئلة الدورات خارج نطاق F25 وأسئلة لم يمكن حسمها</h3>
<ul>{oos}{unres}</ul>
<h3>ترتيب الأولويات عند التعارض</h3>
<p>اتُّبع الترتيب: دقة المرجع ← أمانة الصياغة ← التغطية ← تركيز الامتحان ← الإيجاز ← الشكل. تجاوز بعض كتل الإجابة حدَّ 80 كلمة كان مقصوداً في الأسئلة المقالية والحسابية وحيث لزم سطر «يقول الكتاب» أو «مصدر آخر» أو إعادة بناء الخيارات، وفق البند 0أ من المواصفة.</p>
<h3>الخصوصية وحقوق المادة</h3>
<p>إخفاء الإجابات معونة للمذاكرة وليس حمايةً: نص الإجابات موجود داخل الملف ويمكن الوصول إليه بالبحث أو النسخ أو أدوات الوصول أو عرض المصدر، فلا يُعتمد عليه في امتحان حقيقي. لا يحوي الملف أي بيانات شخصية عن المؤلف أو الجهاز. نصوص الكتاب وأسئلة الامتحانات المقتبسة هنا تبقى ملكاً لمؤلفيها والجامعة، وعلى القارئ احترام حقوقها عند مشاركة الملف.</p>
<h3>إصدار المواصفة ووضع التشغيل</h3>
<p>{METHOD_VERSION.format(spec=esc(SPEC))}</p>
</section>"""

def sources_appendix():
    s = FILES_SUMMARY
    rows = "".join(f'<tr id="src-{n}"><td>{n}</td><td class="fn">{esc(path)}</td><td>{esc(kind)}</td><td>{esc(role)}</td><td class="ltr">{esc(grp)}</td><td>{esc(pages)}</td><td>{esc(note)}</td></tr>' for n, path, kind, role, grp, pages, note in FILES)
    return f"""<section id="sources"><h2>ملفات المصدر</h2>
<p>كل ملف وُجد في مجلد المادة مذكور هنا، بما فيها المستبعد والمكرر، ليعرف القارئ ممّ بُنيت المراجعة وما ينقصها. رقم كل ملف هو الرقم الذي يظهر عند كل سؤال في سطر «المصادر». أسماء الملفات كما وُردت؛ المادة نفسها غير منشورة مع المراجعة.</p>
<p class="meta">{s["files"]} ملفاً · {s["sources"]} مصادر مستقلة استُخدمت للأسئلة · {s["excluded"]} ملفاً مستبعداً · {s["duplicates"]} نسخ مكررة أو تابعة · {s["images"]} صورة/صفحة فُحصت بصرياً.</p>
<details class="reflist"><summary>جدول الملفات ({s["files"]})</summary>
<table class="tbl files"><thead><tr><th>#</th><th>اسم الملف</th><th>النوع</th><th>الدور</th><th>مجموعة المصدر</th><th>الصفحات / البنود</th><th>ملاحظة</th></tr></thead><tbody>{rows}</tbody></table>
</details></section>"""

def ref_lists():
    freqs = collections.Counter(q["freq"] for q in QS if "generated" not in q["types"])
    thr = 3 if sum(v for k,v in freqs.items() if k>=3) >= 8 else 2
    rep = sorted([q for q in QS if q["freq"] >= thr], key=lambda q:(-q["freq"], -q["importance"]))[:30]
    imp = sorted([q for q in QS if q["importance"] >= 4], key=lambda q:(-q["importance"], -q["freq"]))[:30]
    def li(q): return f'<li><a href="#{esc(q["id"])}">{esc(q["stem"])}</a> <span class="meta">— الفصل {q["ch"]} · التكرار {q["freq"]} · {stars(q["importance"])}</span></li>'
    return f"""<section id="lists"><h2>قوائم مرجعية لليوم الأخير</h2>
<details class="reflist"><summary>الأسئلة الأكثر تكراراً ({thr}+ مصادر مستقلة) — {len(rep)} سؤالاً</summary><ol>{"".join(li(q) for q in rep)}</ol></details>
<details class="reflist"><summary>الأسئلة الأعلى أهمية (4 و5) — {len(imp)} سؤالاً</summary><ol>{"".join(li(q) for q in imp)}</ol></details>
</section>"""

def toc():
    items = "".join(f'<li><a href="#ch{n}">الفصل {n}: {esc(CH_TITLES[n])}</a> <span class="meta">({sum(1 for q in QS if q["ch"]==n)})</span></li>' for n in CHAPTERS)
    return f'<section id="toc"><h2>فهرس المحتويات</h2><ol>{items}</ol><ul><li><a href="#howto">كيف تستخدم هذا الملف</a></li><li><a href="#scope">النطاق والمصادر</a></li><li><a href="#method">المنهجية</a></li><li><a href="#sources">ملفات المصدر</a></li><li><a href="#lists">القوائم المرجعية</a></li><li><a href="#metadata">بيانات الملف</a></li></ul></section>'

CSS = """
:root{--bg:#fbfaf7;--fg:#1f2328;--muted:#6b7280;--line:#e5e2da;--card:#ffffff;--ans:#166534;--ansbg:#f0fdf4;--why:#1e3a8a;--red:#b91c1c;--amber:#b45309;--tint:#eef2ff;--accent:#2563eb;--chip:#f3f4f6;--chipon:#1f2328;--chipontext:#fff;--band:rgba(37,99,235,.10);--warn:#fff7e6;--warnline:#f0c36d}
:root[data-theme="dark"]{--bg:#111418;--fg:#e6e6e6;--muted:#9aa0a6;--line:#2a2f36;--card:#181c22;--ans:#4ade80;--ansbg:#0f2419;--why:#93c5fd;--red:#f87171;--amber:#fbbf24;--tint:#1a2033;--accent:#60a5fa;--chip:#232a33;--chipon:#e6e6e6;--chipontext:#111;--band:rgba(96,165,250,.18);--warn:#2a2416;--warnline:#8a6d1f}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#111418;--fg:#e6e6e6;--muted:#9aa0a6;--line:#2a2f36;--card:#181c22;--ans:#4ade80;--ansbg:#0f2419;--why:#93c5fd;--red:#f87171;--amber:#fbbf24;--tint:#1a2033;--accent:#60a5fa;--chip:#232a33;--chipon:#e6e6e6;--chipontext:#111;--band:rgba(96,165,250,.18);--warn:#2a2416;--warnline:#8a6d1f}}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:120px}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Segoe UI","Noto Naskh Arabic","Tahoma","Arial",sans-serif;font-size:17px;line-height:1.75;direction:rtl;text-align:right}
main{max-width:960px;margin:0 auto;padding:16px 20px 80px}
h1,h2,h3{line-height:1.3}
h2{margin-top:56px;border-bottom:2px solid var(--line);padding-bottom:6px}
h3.sech{margin-top:36px;color:var(--fg)}
details.chd > summary,details.secd > summary{cursor:pointer;list-style:none}
details.chd > summary::-webkit-details-marker,details.secd > summary::-webkit-details-marker{display:none}
details.chd > summary h2,details.secd > summary h3{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.tog{margin-inline-start:auto;font-size:.75em;font-weight:normal;white-space:nowrap}
details.chd > summary .tog .hide,details.secd > summary .tog .hide,details.methods > summary .tog .hide{display:none}
details.chd[open] > summary .tog .hide,details.secd[open] > summary .tog .hide,details.methods[open] > summary .tog .hide{display:inline}
details.chd[open] > summary .tog .show,details.secd[open] > summary .tog .show,details.methods[open] > summary .tog .show{display:none}
details.chd:not([open]) > summary h2{margin-bottom:0}
p{margin:.4em 0}
a{color:var(--accent)}
.meta{color:var(--muted);font-size:.82em}
.cover{padding:40px 0 12px}
.cover h1{font-size:2em;margin:0 0 8px}
.cover .sub{color:var(--muted);font-size:1.05em}
.scopebox{background:var(--warn);border:1px solid var(--warnline);border-radius:12px;padding:12px 16px;margin:14px 0 6px;font-size:.98em}
.scopebox .olbl{font-weight:700;margin-bottom:2px}
.scopenote{margin-top:6px;padding-top:6px;border-top:1px dashed var(--warnline);color:var(--amber);font-size:.92em}
.toolbar{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0}
.toolbar .bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.toolbar .grp{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.chip{border:1px solid var(--line);background:var(--chip);color:var(--fg);border-radius:999px;padding:3px 12px;cursor:pointer;font:inherit;font-size:.85em;min-height:32px}
.chip.on{background:var(--chipon);color:var(--chipontext);border-color:var(--chipon)}
.toolbar select,.toolbar input{font:inherit;font-size:.85em;padding:4px 8px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg)}
.toolbar input{min-width:180px}
.bar #search{margin-inline-start:auto;flex:1 1 160px;max-width:320px}
.counter{font-size:.85em;color:var(--muted);white-space:nowrap}
.fsum{font-size:.8em;color:var(--muted)}
.fsum:empty{display:none}
.filters{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
.toolbar.fclosed .filters{display:none}
html:not(.js) .ftog,html:not(.js) .sliders,html:not(.js) .jsonly{display:none}
.fbadge{display:inline-block;background:var(--chipon);color:var(--chipontext);border-radius:999px;padding:0 6px;font-size:.8em;margin-inline-start:4px}
.fbadge[hidden]{display:none}
.chip.ftog.on .fbadge{background:var(--chipontext);color:var(--chipon)}
@media (max-width:760px){
 .filters{position:absolute;right:0;left:0;top:100%;margin:0;background:var(--bg);border-bottom:1px solid var(--line);box-shadow:0 8px 16px rgba(0,0,0,.12);padding:10px 12px;max-height:calc(100vh - 60px);overflow:auto}
 .filters .chip,.filters select,.filters .sl,.bar .chip{min-height:44px}
 .filters .sl{flex-basis:100%}
 .filters .sl input[type=range]{flex:1;width:auto}
 .filters select{flex-basis:100%}
 .bar #search{flex-basis:100%;max-width:none;margin:0}
}
.sl{display:inline-flex;align-items:center;gap:6px;font-size:.85em;border:1px solid var(--line);border-radius:999px;padding:2px 10px;background:var(--chip)}
.sl.on{border-color:var(--chipon)}
.sl span{min-width:2.2em;text-align:center;color:var(--muted)}
.sl.on span{color:var(--fg);font-weight:bold}
.sl input[type=range]{width:90px;padding:0;border:0;background:transparent;accent-color:var(--chipon);direction:ltr}
.opener{background:var(--tint);border-radius:12px;padding:12px 16px;margin:14px 0 14px}
.opener .olbl,.methods .olbl{font-size:.8em;color:var(--muted);margin-bottom:2px}
.opener p{margin:.2em 0}
details.methods{background:var(--tint);border-radius:12px;padding:10px 16px;margin:0 0 22px}
details.methods > summary{cursor:pointer;list-style:none;display:flex;flex-wrap:wrap;gap:6px;align-items:baseline}
details.methods > summary::-webkit-details-marker{display:none}
.mentry{border-top:1px dashed var(--line);padding:8px 0 4px}
.mentry h4{margin:.2em 0}
.mkey{display:inline-block;background:var(--chipon);color:var(--chipontext);border-radius:6px;padding:0 8px;font-size:.85em;margin-inline-end:4px}
.m-steps{margin:.2em 0;padding-inline-start:1.4em}
.m-steps li{margin:2px 0}
.m-rec,.m-fast{margin:.2em 0}
.m-fast .lbl,.m-rec .lbl,.a-fast .lbl{color:var(--why)}
.mlink{text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:0 6px}
.secintro{color:var(--muted);font-size:.9em;border-inline-start:3px solid var(--line);padding-inline-start:10px}
.q{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin:18px 0}
.q .stem{font-size:1.06em;margin:.3em 0 .4em}
.q .num{color:var(--muted);font-size:.85em;margin-inline-end:4px}
.opts{margin:.2em 0 .4em;padding-inline-start:0;list-style:none}
.opts li{padding:2px 0}
.opts .let{color:var(--muted);display:inline-block;min-width:1.6em}
.opts.tf{color:var(--muted)}
.orig{color:var(--muted);font-size:.85em;background:var(--chip);border-radius:8px;padding:4px 10px}
.tag{display:inline-block;border-radius:6px;padding:0 6px;font-size:.78em;background:var(--chip);color:var(--muted);border:1px solid var(--line)}
.tag.recon,.tag.lowc,.tag.uns{color:var(--amber);border-color:var(--amber)}
.imp{letter-spacing:1px}
details.ans{margin-top:8px}
details.ans > summary{cursor:pointer;list-style:none;display:inline-block;border:1px solid var(--line);border-radius:8px;padding:3px 12px;font-size:.9em;color:var(--fg);background:var(--chip);min-height:32px}
details.ans > summary::-webkit-details-marker{display:none}
details.ans > summary .hide{display:none}
details.ans[open] > summary .hide{display:inline}
details.ans[open] > summary .show{display:none}
.ablock{margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}
.ablock p{margin:.35em 0}
.lbl{font-weight:600;margin-inline-end:4px}
.a-ans{color:var(--ans);background:var(--ansbg);border-radius:8px;padding:4px 10px}
.a-fast{border-inline-start:3px solid var(--why);padding-inline-start:8px}
.a-why,.a-rem,.a-dis,.a-also{color:var(--fg)}
.a-why .lbl,.a-rem .lbl,.a-dis .lbl,.a-also .lbl{color:var(--why)}
.a-also ul{margin:.1em 0;padding-inline-start:1.4em;font-size:.92em}
.a-ref{color:var(--muted);font-size:.9em}
.a-red{color:var(--red)}
.a-amber{color:var(--amber)}
.a-sci{color:var(--red)}
.src{margin-top:6px}
.seelink a{text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:0 4px}
details.vars{font-size:.85em;color:var(--muted);margin-top:6px}
details.vars summary,details.model summary,details.step summary{cursor:pointer}
details.model{margin:.4em 0;border:1px solid var(--line);border-radius:8px;padding:4px 10px}
details.model summary{font-weight:600;color:var(--why)}
.mbody{padding:4px 0;font-size:.97em}
details.more > summary{cursor:pointer;color:var(--muted);font-size:.85em}
html:not(.ess) details.more > summary{display:none}
html:not(.ess) details.more:not(.model) > summary{display:none}
details.model > summary{display:list-item!important;color:var(--why);font-size:1em}
details.step{margin:4px 0;border:1px dashed var(--line);border-radius:8px;padding:2px 10px}
details.step > summary{font-size:.92em;color:var(--why)}
.showsteps{margin:4px 0}
.tw{overflow-x:auto;margin:8px 0}
.qtbl,.ctbl{border-collapse:collapse;font-size:.92em}
.qtbl th,.qtbl td,.ctbl th,.ctbl td{border:1px solid var(--line);padding:3px 10px;text-align:center;vertical-align:top;white-space:nowrap}
.qtbl th,.ctbl th{background:var(--chip);font-weight:600}
.qtbl caption{caption-side:top;text-align:start;color:var(--muted);font-size:.9em;padding:2px 0}
.qtbl.atbl{font-size:.88em}
.syms{font-size:.85em;margin:4px 0 8px;display:flex;flex-wrap:wrap;gap:4px 6px;align-items:center;line-height:1.5}
.syms .slbl{color:var(--why);font-weight:600}
.syms .chip{display:inline-block;position:relative;border:1px solid var(--line);background:var(--chip);border-radius:999px;padding:1px 10px;cursor:help;color:var(--fg);min-height:0}
.syms .chip:hover,.syms .chip:focus{border-color:var(--why);outline:none}
.syms .pop{display:none;position:absolute;top:calc(100% + 4px);inset-inline-start:0;z-index:20;width:max-content;min-width:16em;max-width:min(26em,85vw);background:var(--card);color:var(--fg);border:1px solid var(--why);border-radius:10px;padding:8px 12px;box-shadow:0 6px 18px rgba(0,0,0,.25);font-size:1em;line-height:1.6;white-space:normal;text-align:start;cursor:auto}
@media (hover:hover){.syms .chip:hover .pop{display:block}}
#symsheet{position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.45);display:flex;align-items:flex-end;justify-content:center}
#symsheet[hidden]{display:none}
#symsheet .sh-box{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:16px 16px 0 0;width:100%;max-width:34em;padding:12px 16px calc(16px + env(safe-area-inset-bottom));box-shadow:0 -6px 24px rgba(0,0,0,.3);line-height:1.7;max-height:70vh;overflow:auto}
#symsheet .sh-x{float:left;border:1px solid var(--line);background:var(--chip);color:var(--fg);border-radius:999px;width:2.4em;height:2.4em;font-size:1em;cursor:pointer}
#symsheet .sh-body > span,.syms .pop > span{display:block}
#symsheet .p-ar,.syms .pop .p-ar{font-weight:600;font-size:1.05em}
#symsheet .p-en,.syms .pop .p-en{color:var(--muted);font-size:.92em}
#symsheet .p-f,.syms .pop .p-f{font-family:Consolas,"Courier New",monospace;background:var(--chip);border-radius:6px;padding:2px 10px;margin:4px 0;display:inline-block;direction:ltr;unicode-bidi:isolate}
#symsheet .p-n,.syms .pop .p-n{margin-top:4px}
#symsheet .p-x,.syms .pop .p-x{color:var(--muted);font-size:.9em}
#symsheet .sh-nav{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px 6px;font-size:.85em}
#symsheet .sh-nav .chip{cursor:pointer;display:inline-block;border:1px solid var(--line);background:var(--chip);border-radius:999px;padding:1px 10px;direction:ltr}
#symsheet .sh-nav .chip.open{border-color:var(--why);color:var(--why);font-weight:600}
#symsheet .sh-nav .slbl{color:var(--why);font-weight:600}
@media (min-width:601px){#symsheet .sh-box{border-radius:16px;margin-bottom:6vh}}
.syms .chip b{color:var(--why);margin-inline-end:4px}
.syms .shint{color:var(--muted);flex-basis:100%;font-size:.9em}
abbr[title]{text-decoration:underline dotted;text-underline-offset:3px;cursor:help;color:inherit}
.calc{margin:.4em 0}
.a-calc{margin:.2em 0}
.a-calc .lbl{color:var(--why)}
.given{margin:.1em 0 .3em;padding-inline-start:1.4em;font-size:.95em}
.given li{margin:1px 0}
.ctbl td{white-space:normal}
.ctbl td.cwhat{text-align:start}
.ctbl td.ceq,.ctbl td.csub{white-space:nowrap}
.ctbl td.ceq span,.ctbl td.csub span{font-family:Consolas,"Courier New",monospace;font-size:.95em}
.ctbl td.cres{color:var(--ans);white-space:nowrap}
.ctbl .cnote{font-size:.85em;color:var(--muted);font-weight:normal;white-space:normal}
.cfinal{margin:.2em 0;font-size:.95em}
.figw{margin:8px 0;max-width:640px}
.figw svg{width:100%;height:auto;display:block;background:var(--card);border:1px solid var(--line);border-radius:10px}
.figw figcaption{margin-top:2px}
.f-axis{stroke:var(--fg);stroke-width:1.5}
.f-lbl{font-size:17px;fill:var(--fg);font-family:inherit;direction:ltr;unicode-bidi:isolate;paint-order:stroke;stroke:var(--card);stroke-width:4px;stroke-linejoin:round}
.f-rev{stroke:var(--ans);stroke-width:2.5}
.f-tc{stroke:var(--red);stroke-width:2.5}
.f-fc{stroke:var(--muted);stroke-width:2;stroke-dasharray:6 4}
.f-cfc{stroke:var(--amber);stroke-width:2;stroke-dasharray:3 4}
.f-ctc{stroke:var(--amber);stroke-width:2;stroke-dasharray:8 4}
.f-rev-t{fill:var(--ans)}.f-tc-t{fill:var(--red)}.f-fc-t{fill:var(--muted)}.f-cfc-t,.f-ctc-t{fill:var(--amber)}
.f-drop{stroke:var(--muted);stroke-width:1;stroke-dasharray:3 3}
.f-pt{fill:var(--card);stroke:var(--fg);stroke-width:2}
.f-pt.f-hl{fill:var(--accent);stroke:var(--accent)}
.f-band{fill:var(--band)}
.f-hl-t{fill:var(--accent);font-weight:700}
.f-ptn{font-weight:700;font-size:22px}
.a-key{font-size:.92em;border-inline-start:3px solid var(--ans);padding-inline-start:8px}
.a-key .lbl{color:var(--ans)}
.tbl{border-collapse:collapse;width:100%;font-size:.88em;margin:10px 0;display:block;overflow-x:auto}
.tbl th,.tbl td{border:1px solid var(--line);padding:4px 8px;text-align:right;vertical-align:top}
.tbl th{background:var(--chip)}
.tbl.files .fn{direction:ltr;text-align:left;unicode-bidi:plaintext;word-break:break-all;font-size:.92em}
.tbl.files td:target,tr:target td{background:var(--ansbg)}
.srcref{text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:0 4px;direction:ltr;unicode-bidi:isolate}
.notice{margin-top:10px;padding:8px 12px;border:1px dashed var(--line);border-radius:8px}
.notice p{margin:.2em 0}
.pledge{border-inline-start:3px solid var(--line);padding-inline-start:10px;color:var(--muted);font-size:.92em}
details.pgd > summary{cursor:pointer;list-style:none}
details.pgd > summary::-webkit-details-marker{display:none}
details.pgd > summary h2{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
details.pgd:not([open]) > summary h2{margin-bottom:0;border-bottom-color:transparent}
details.pgd > summary .tog .hide{display:none}
details.pgd[open] > summary .tog .hide{display:inline}
details.pgd[open] > summary .tog .show{display:none}
footer details.pgd > summary h2{margin-top:0}
details.reflist{margin:10px 0}
details.reflist summary{cursor:pointer;font-weight:600}
.hidden{display:none!important}
.chapter.hidden{display:none!important}
html.ess .q .ablock details.more:not([open]) > *:not(summary){display:none}
footer{margin-top:60px;color:var(--muted);font-size:.85em;border-top:1px solid var(--line);padding-top:12px}
[dir="ltr"],.ltr{direction:ltr;text-align:left;unicode-bidi:isolate}
@media (max-width:600px){.ctbl thead{display:none}.ctbl,.ctbl tbody,.ctbl tr,.ctbl td{display:block;width:100%;box-sizing:border-box}.ctbl tr{border:1px solid var(--line);border-radius:8px;margin:6px 0;padding:4px 8px}.ctbl td{border:0;padding:2px 0;text-align:start;white-space:normal!important}.ctbl td.ltr{direction:rtl;text-align:start}.ctbl td::before{content:attr(data-l) ": ";color:var(--muted);font-size:.85em}.ctbl td.ceq span,.ctbl td.csub span{direction:ltr;unicode-bidi:isolate}body{font-size:16px}main{padding:10px 12px 60px}.q{padding:12px}.toolbar input{min-width:120px}}
@media print{.toolbar,.noprint{display:none!important}.tbl.files{display:table}details{display:block}details > summary{display:none}details.model > summary,details.step > summary,details.methods > summary{display:block!important}details > *:not(summary){display:block!important}.tog{display:none}.q{break-inside:avoid;border-color:#bbb}.hidden{display:block!important}body{background:#fff;color:#000}a{color:#000;text-decoration:none}}
"""

JS = """
(function(){var KEY="__KEY__";var FMAX=parseInt(document.getElementById("freq").max)||5;
var root=document.documentElement;
var modeBtns=document.querySelectorAll('[data-mode]'),impSl=document.getElementById('imp'),freqSl=document.getElementById('freq'),impV=document.getElementById('impv'),freqV=document.getElementById('freqv');
var chSel=document.getElementById('chsel'),search=document.getElementById('search'),counter=document.getElementById('counter'),essBtn=document.getElementById('ess');
var state={mode:'all',imp:1,freq:0,ch:'all',q:'',ess:false};
function clampI(v,lo,hi){v=parseInt(v);return isNaN(v)?lo:Math.min(hi,Math.max(lo,v));}
try{var saved=JSON.parse(localStorage.getItem(KEY+'_review_state')||'{}');if(saved.mode)state.mode=saved.mode;if(saved.imp!=null)state.imp=clampI(saved.imp,1,5);if(saved.freq!=null)state.freq=clampI(saved.freq,0,FMAX);if(saved.ch)state.ch=saved.ch;if(saved.ess)state.ess=true;}catch(e){}
var h=location.hash.replace('#','');if(/^mode=/.test(h)){h.split('&').forEach(function(kv){var p=kv.split('=');if(p[0]==='mode')state.mode=p[1];if(p[0]==='imp')state.imp=clampI(p[1],1,5);if(p[0]==='freq')state.freq=clampI(p[1],0,FMAX);if(p[0]==='ch')state.ch=p[1];if(p[0]==='ess')state.ess=p[1]==='1';});}
function norm(s){return (s||'').toLowerCase().replace(/[\\u064B-\\u0652\\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي');}
var MODE_NAMES={all:'الكل',exam:'الامتحانات',textbook:'الكتاب',other:'مصادر أخرى',generated:'مولَّدة'};
function cntText(el,vis){var tot=parseInt(el.getAttribute('data-total'));var paren=el.textContent.charAt(0)==='(';
 var s=vis===tot?tot+' سؤالاً':vis+' من '+tot;if(!paren&&el.getAttribute('data-ess'))s+=' (الأساسيات '+el.getAttribute('data-ess')+')';el.textContent=paren?'('+(vis===tot?tot:vis+'/'+tot)+')':s;}
function apply(reveal){
 var qs=document.querySelectorAll('article.q'),shown=0,total=qs.length,nq=norm(state.q);
 root.classList.toggle('ess',state.ess);
 var minImp=Math.max(state.imp,state.ess?3:1);
 qs.forEach(function(a){
  var ok=true;
  if(state.mode!=='all'&&a.getAttribute('data-section').split(' ').indexOf(state.mode)<0)ok=false;
  if(parseInt(a.getAttribute('data-importance'))<minImp)ok=false;
  if(parseInt(a.getAttribute('data-freq'))<state.freq)ok=false;
  if(state.ch!=='all'&&a.getAttribute('data-chapter')!==state.ch)ok=false;
  if(nq&&norm(a.textContent).indexOf(nq)<0)ok=false;
  a.classList.toggle('hidden',!ok);if(ok)shown++;
 });
 document.querySelectorAll('article.q details.more').forEach(function(d){if(!d._touched)d.open=!state.ess;});
 document.querySelectorAll('section.chapter').forEach(function(s){var n=s.querySelectorAll('article.q:not(.hidden)').length;s.classList.toggle('hidden',n===0);
  var c=s.querySelector('details.chd > summary .cnt');if(c)cntText(c,n);
  if(reveal&&n>0){s.querySelector('details.chd').open=true;}
  s.querySelectorAll('details.secd').forEach(function(d){var m=d.querySelectorAll('article.q:not(.hidden)').length;d.classList.toggle('hidden',m===0);
   var sc=d.querySelector('summary .cnt');if(sc)cntText(sc,m);if(reveal&&m>0)d.open=true;});
 });
 counter.textContent=shown+' من '+total+' سؤالاً';
 var parts=[];if(state.mode!=='all')parts.push(MODE_NAMES[state.mode]);if(state.ess)parts.push('الأساسيات');if(state.imp>1)parts.push('★'+state.imp+'+');if(state.freq>0)parts.push('تكرار '+state.freq+'+');if(state.ch!=='all')parts.push('الفصل '+state.ch);if(state.q)parts.push('بحث: «'+state.q+'»');
 var nf=parts.length;fbadge.textContent=nf;fbadge.hidden=nf===0;ftog.classList.toggle('on',nf>0);
 fsum.textContent=(nf>0&&tb.classList.contains('fclosed'))?parts.join(' · '):'';
 modeBtns.forEach(function(b){b.classList.toggle('on',b.getAttribute('data-mode')===state.mode);});
 essBtn.classList.toggle('on',state.ess);essBtn.setAttribute('aria-pressed',state.ess?'true':'false');
 impSl.value=state.imp;freqSl.value=state.freq;
 impV.textContent=state.imp<=1?'الكل':state.imp+'+';freqV.textContent=state.freq<=0?'الكل':state.freq+'+';
 impSl.parentElement.classList.toggle('on',state.imp>1);freqSl.parentElement.classList.toggle('on',state.freq>0);
 chSel.value=state.ch;if(search.value!==state.q)search.value=state.q;
 try{localStorage.setItem(KEY+'_review_state',JSON.stringify({mode:state.mode,imp:state.imp,freq:state.freq,ch:state.ch,ess:state.ess}));}catch(e){}
 var frag='mode='+state.mode+'&imp='+state.imp+'&freq='+state.freq+'&ch='+state.ch+'&ess='+(state.ess?1:0);
 if(location.hash.replace('#','')!==frag&&!/^(Q\\d\\d-\\d\\d\\d|m\\d+-M\\d+|src-\\d+|ch\\d+)$/.test(location.hash.replace('#',''))){history.replaceState(null,'','#'+frag);}
}
var tb=document.querySelector('.toolbar'),ftog=document.getElementById('ftog'),fbadge=document.getElementById('fbadge'),fsum=document.getElementById('fsum');
modeBtns.forEach(function(b){b.addEventListener('click',function(){state.mode=b.getAttribute('data-mode');apply(true);});});
essBtn.addEventListener('click',function(){state.ess=!state.ess;document.querySelectorAll('article.q details.more').forEach(function(d){d._touched=false;});apply(true);});
document.querySelectorAll('article.q details.more').forEach(function(d){d.addEventListener('toggle',function(){if(root.classList.contains('ess'))d._touched=true;});});
impSl.addEventListener('input',function(){state.imp=clampI(impSl.value,1,5);apply(true);});
freqSl.addEventListener('input',function(){state.freq=clampI(freqSl.value,0,FMAX);apply(true);});
chSel.addEventListener('change',function(){state.ch=chSel.value;apply(true);});
var t;search.addEventListener('input',function(){clearTimeout(t);t=setTimeout(function(){state.q=search.value;apply(!!state.q);},150);});
document.getElementById('reset').addEventListener('click',function(){state={mode:'all',imp:1,freq:0,ch:'all',q:'',ess:false};search.value='';apply(false);});
document.getElementById('expand').addEventListener('click',function(){document.querySelectorAll('article.q:not(.hidden) details.ans').forEach(function(d){d.open=true;});});
document.getElementById('collapse').addEventListener('click',function(){document.querySelectorAll('details.ans').forEach(function(d){d.open=false;});});
document.addEventListener('click',function(e){var b=e.target.closest('.showsteps');if(!b)return;var q=b.closest('.ablock');q.querySelectorAll('details.step,details.atw').forEach(function(d){d.open=true;});b.hidden=true;});
function setFilters(open){tb.classList.toggle('fclosed',!open);ftog.setAttribute('aria-expanded',open?'true':'false');try{localStorage.setItem(KEY+'_filters_open',open?'1':'0');}catch(e){}}
(function(){var v=null;try{v=localStorage.getItem(KEY+'_filters_open');}catch(e){}if(v===null)v=window.matchMedia('(max-width:760px)').matches?'0':'1';setFilters(v==='1');})();
ftog.addEventListener('click',function(){setFilters(tb.classList.contains('fclosed'));apply(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&window.matchMedia('(max-width:760px)').matches&&!tb.classList.contains('fclosed')){setFilters(false);apply(false);}});
var chOpen={};try{chOpen=JSON.parse(localStorage.getItem(KEY+'_ch_open')||'{}');}catch(e){}
function saveCh(){try{localStorage.setItem(KEY+'_ch_open',JSON.stringify(chOpen));}catch(e){}}
document.querySelectorAll('section.chapter').forEach(function(s){var id=s.id,d=s.querySelector('details.chd');if(chOpen[id]===false)d.open=false;
 d.addEventListener('toggle',function(){chOpen[id]=d.open;saveCh();});});
function setAll(sel,open){document.querySelectorAll(sel).forEach(function(d){d.open=open;});}
document.getElementById('foldch').addEventListener('click',function(){setAll('details.chd',false);});
document.getElementById('opench').addEventListener('click',function(){setAll('details.chd',true);});
document.getElementById('foldsec').addEventListener('click',function(){setAll('details.secd',false);});
document.getElementById('opensec').addEventListener('click',function(){setAll('details.secd',true);});
var pgOpen={};try{pgOpen=JSON.parse(localStorage.getItem(KEY+'_pg_open')||'{}');}catch(e){}
document.querySelectorAll('details.pgd').forEach(function(d){var id=d.getAttribute('data-pg');if(pgOpen[id]===true)d.open=true;if(pgOpen[id]===false)d.open=false;
 d.addEventListener('toggle',function(){pgOpen[id]=d.open;try{localStorage.setItem(KEY+'_pg_open',JSON.stringify(pgOpen));}catch(e){}});});
document.getElementById('foldall').addEventListener('click',function(){setAll('details.chd,details.secd,details.pgd',false);});
document.getElementById('openall').addEventListener('click',function(){setAll('details.chd,details.secd,details.pgd',true);});
function openTo(id){var el=document.getElementById(id);if(!el)return;var p=el;while(p){if(p.tagName==='DETAILS'&&!p.classList.contains('ans'))p.open=true;p=p.parentElement;}el.scrollIntoView();}
window.addEventListener('hashchange',function(){openTo(location.hash.slice(1));});
if(/^(Q\\d\\d-\\d\\d\\d|m\\d+-M\\d+|src-\\d+|ch\\d+)$/.test(h))setTimeout(function(){openTo(h);},50);
var theme=document.getElementById('theme');
function setTheme(v){if(v)root.setAttribute('data-theme',v);else root.removeAttribute('data-theme');try{localStorage.setItem(KEY+'_theme',v||'');}catch(e){}theme.textContent=v==='dark'?'☀ فاتح':v==='light'?'🌙 داكن':'◐ المظهر';}
try{setTheme(localStorage.getItem(KEY+'_theme')||'');}catch(e){}
theme.addEventListener('click',function(){var cur=root.getAttribute('data-theme');var dark=cur?cur==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;setTheme(dark?'light':'dark');});
window.addEventListener('beforeprint',function(){document.querySelectorAll('details').forEach(function(d){d.open=true;});});
document.querySelectorAll('#toc a, .mlink, .seelink a').forEach(function(a){a.addEventListener('click',function(){var id=a.getAttribute('href').slice(1);setTimeout(function(){openTo(id);},0);});});
apply(false);
})();
"""

PG_OPEN = {"howto": True, "scope": True, "method": False, "sources": False, "lists": False, "toc": False, "metadata": False}
def fold_sections(page):
    tog = '<span class="tog meta"><span class="hide">طيّ ▲</span><span class="show">فتح ▼</span></span>'
    def sec(m):
        sid, title = m.group(1), m.group(2)
        extra = f' <small class="meta">v{esc(VER)} · المواصفة {esc(SPEC)} · CC BY-NC-SA 4.0</small>' if sid == "metadata" else ""
        op = " open" if PG_OPEN.get(sid, True) else ""
        tag = "footer" if sid == "metadata" else "section"
        return f'<{tag} id="{sid}"><details class="pgd" data-pg="{sid}"{op}><summary><h2>{title}{extra}{tog}</h2></summary>'
    page = re.sub(r'<(?:section|footer) id="(howto|scope|method|sources|lists|toc|metadata)"><h2>(.*?)</h2>', sec, page)
    for sid in PG_OPEN:
        tag = "footer" if sid == "metadata" else "section"
        i = page.find(f'id="{sid}"'); j = page.find(f"</{tag}>", i)
        assert i > 0 and j > 0, sid
        page = page[:j] + "</details>" + page[j:]
    return page

def build():
    c = counts(); total = len(QS); FMAX = max(q['freq'] for q in QS); cov_total = sum(len(v) for v in SUBS.values()) - B.get('coverage_stats', {}).get('uncovered', 0)
    gen = c["generated"]; total_subs = sum(len(v) for v in SUBS.values())
    ch_opts = "".join(f'<option value="{n}">الفصل {n}</option>' for n in CHAPTERS)
    ess_total = sum(1 for q in QS if q["importance"] >= 3)
    parts = [f'<!DOCTYPE html><html lang="ar" dir="rtl"><head><title>{esc(TITLE)} — v{esc(VER)}</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><script>document.documentElement.className+=" js";</script><style>{CSS}</style></head><body>',
      '<main>',
      f'<header class="cover"><h1>{esc(TITLE)}</h1><p class="sub">{esc(COURSE_LINE)}</p>'
      f'<p class="meta">الإصدار v{esc(VER)} · الفصول: {CHAPTER_LIST_AR} · {total} سؤالاً · أسئلة الامتحانات {c["exam"]} · أسئلة الكتاب {c["textbook"]} · مصادر أخرى {c["other"]} · مولَّدة {gen}</p>'
      f'<div class="scopebox"><div class="olbl">نطاق هذه المراجعة: دورة {esc(EXAM_SITTING)} فقط (امتحان {esc(EXAM_DATE)})</div><p>{esc(SCOPE_BANNER)}</p></div></header>',
      '<div class="toolbar noprint" role="toolbar" aria-label="أدوات القراءة">'
      '<div class="bar">'
      '<span class="counter" id="counter"></span><span class="fsum" id="fsum" aria-live="polite"></span>'
      '<button class="chip ftog" id="ftog" aria-expanded="true" aria-controls="filters">⚙ الفلاتر <span class="fbadge" id="fbadge" hidden></span></button>'
      f'<button class="chip jsonly" id="ess" aria-pressed="false" title="الأساسيات: الأسئلة بأهمية 3 فأكثر مع طيّ السطور الثانوية">★ الأساسيات ({ess_total})</button>'
      '<input id="search" type="search" placeholder="ابحث في الأسئلة والإجابات…" aria-label="بحث" class="jsonly">'
      '</div>'
      '<div class="filters" id="filters">'
      '<div class="grp" role="group" aria-label="نوع الأسئلة"><button class="chip on" data-mode="all">الكل</button><button class="chip" data-mode="exam">الامتحانات</button><button class="chip" data-mode="textbook">الكتاب</button><button class="chip" data-mode="other">مصادر أخرى</button><button class="chip" data-mode="generated">مولَّدة</button></div>'
      '<div class="grp sliders" aria-label="التصفية"><label class="sl">الأهمية <span id="impv">الكل</span><input id="imp" type="range" min="1" max="5" step="1" value="1" aria-label="الحد الأدنى للأهمية"></label>'
      f'<label class="sl">التكرار <span id="freqv">الكل</span><input id="freq" type="range" min="0" max="{FMAX}" step="1" value="0" aria-label="الحد الأدنى للتكرار"></label></div>'
      f'<select id="chsel" aria-label="الفصل" class="jsonly"><option value="all">كل الفصول</option>{ch_opts}</select>'
      '<div class="grp jsonly"><button class="chip" id="expand">إظهار الإجابات</button><button class="chip" id="collapse">إخفاء الإجابات</button><button class="chip" id="foldch">طيّ كل الفصول</button><button class="chip" id="opench">فتح كل الفصول</button><button class="chip" id="foldsec">طيّ الأنواع</button><button class="chip" id="opensec">فتح الأنواع</button><button class="chip" id="foldall">⊟ طيّ الكل</button><button class="chip" id="openall">⊞ فتح الكل</button><button class="chip" id="theme">◐ المظهر</button><button class="chip" id="reset">↺ إعادة ضبط التصفية</button></div>'
      '</div></div>',
      f'''<section id="howto"><h2>كيف تستخدم هذا الملف</h2>
<p>كل سؤال يحمل ثلاث علامات: <b>التكرار</b> = عدد المصادر المستقلة التي سألته ({HOWTO_FREQ})؛ <b>الأهمية ★</b> من 1 إلى 5 مبنية على عدد الدورات التي ورد فيها السؤال، زائد نقطة إن كان من أسئلة الكتاب، زائد نقطة إن كانت فقرته من مجالات تركيز المدرّس، وهي معونة للدراسة لا توقّع للامتحان؛ <b>⚠ ثقة منخفضة</b> يظهر فقط حيث يستند الجواب إلى دليل ضعيف أو نقل غير مؤكد، وغيابه يعني أن الإجابة تُحقق منها من الكتاب بالصفحة.</p>
<p>الإجابة مخفية خلف زر «إظهار الإجابة» ولا تحتاج جافاسكربت. الشريط الثابت في الأعلى يعرض العدّاد وزر «⚙ الفلاتر» وزر «★ الأساسيات» والبحث؛ وخلف زر الفلاتر: وضع القراءة (نوع واحد من الأسئلة عبر كل الفصول: الامتحانات، الكتاب، مصادر أخرى، مولَّدة)، ومنزلقان لحدّ أدنى للأهمية (1–5) وللتكرار، واختيار فصل، وإظهار الإجابات أو إخفائها، وطيّ كل الفصول أو فتحها، وطيّ أنواع الأسئلة أو فتحها، مستقلةً عن حالة الإجابات، والمظهر الفاتح أو الداكن، وزر «إعادة ضبط التصفية». اختياراتك تُحفظ وتوضع في رابط الصفحة. <b>الأساسيات</b> تعرض الأسئلة بأهمية 3 فأكثر وتطوي داخل الإجابة السطور الثانوية (المشتتات، «سُئل أيضاً»، الإجابة النموذجية الكاملة، جدول الحل) خلف زر «المزيد»؛ ضغطة ثانية تعيد العرض الكامل. على الهاتف تبدأ لوحة الفلاتر مطوية، وحين تكون مطوية وثمة تصفية فعّالة يظهر عددها على الزر وملخصها بجانب العدّاد. تنبيه: الأسئلة المولَّدة أهميتها 1 دائماً، فرفع منزلق الأهمية إلى 2 أو أكثر يخفيها كلها.</p>
<p>في الفصول الحسابية (الاهتلاك، التعادل) تبدأ كل فصل كتلة «طرق الحل» المطوية: طريقة واحدة لكل نوع مسألة بخطوات الكتاب وصفحته. في الإجابة الحسابية يظهر سطر الإجابة و«الطريق السريع» (قاعدة تقرر الجواب بلا حساب كامل حين يسمح الكتاب) والمعطيات والخطوة الأولى، وكل خطوة تالية مطوية لتقارن حلّك بها، وزر «إظهار كل الخطوات» يفتحها معاً. الأشكال (مخطط التعادل) مرسومة من أرقام السؤال نفسه: مخطط الامتحان ذو الخطوط المرقمة بلا مسميات يظهر تحت السؤال ومفتاحه (اسم كل خط ونقطة) في الإجابة، ومخطط الحل بقيمه يظهر داخل الإجابة بعد الحساب حتى لا يكشفها. الترتيب المقترح: أسئلة الامتحانات أولاً ثم أسئلة الكتاب ثم الباقي. الطباعة تُظهر كل الإجابات والخطوات وتتجاهل التصفية.</p>
<p class="meta">الأقسام التمهيدية والختامية (كيف تستخدم هذا الملف، النطاق والمصادر، المنهجية، ملفات المصدر، القوائم المرجعية، فهرس المحتويات، بيانات الملف) تُطوى وتُفتح بالنقر على عنوانها مثل الفصول، ويُحفظ ما طويته. زرّا «طيّ الكل» و«فتح الكل» في الفلاتر يطويان الفصول وأنواع الأسئلة وهذه الأقسام معاً ويُبقيان الإجابات على حالها.</p>
<p class="meta">إخفاء الإجابات معونة للمذاكرة وليس حمايةً: نص الإجابة موجود في الملف ويصل إليه البحث والنسخ وعرض المصدر، فلا يُعتمد عليه في امتحان حقيقي. نصوص الكتاب والامتحانات المقتبسة تبقى ملكاً لأصحابها.</p>
<p class="pledge">شروط رخصة هذا الملف (CC BY-NC-SA 4.0): شارك هذا الملف مجاناً مع زملائك في المادة. أبقِ الإشعار الموجود في آخر الملف حتى يجد غيرك المصدر وأحدث إصدار. لا يجوز بيعه ولا وضعه خلف اشتراك أو جدار دفع.</p></section>''',
      f'''<section id="scope"><h2>النطاق والمصادر</h2>
<p><b>{esc(SCOPE_BANNER)}</b></p>
<p>{SCOPE_TEXT.format(book=esc(BOOK_FILE), pages=BOOK_PAGES, chs=CHAPTER_LIST_AR, subs=total_subs)}</p>
<table class="tbl"><thead><tr><th>القسم</th><th>العدد</th><th>ما هو</th></tr></thead><tbody>
<tr><td>أسئلة الامتحانات</td><td>{c["exam"]}</td><td>{esc(SEC_INTRO["exam"])}</td></tr>
<tr><td>أسئلة الكتاب</td><td>{c["textbook"]}</td><td>{esc(SEC_INTRO["textbook"])}</td></tr>
<tr><td>مصادر أخرى</td><td>{c["other"]}</td><td>{esc(SEC_INTRO["other"])}</td></tr>
<tr><td>مولَّدة</td><td>{gen}</td><td>{esc(SEC_INTRO["generated"])}</td></tr></tbody></table>
<p class="meta">سؤال واحد قد يكون من الامتحانات ومن الكتاب معاً فيُحسب في القسمين ويظهر في وضعَي القراءة، لكنه يُعرض مرة واحدة (في قسم الامتحانات) مع وسم النوعين. بند الكتاب وبند الامتحان بصيغته الأصلية يبقيان بطاقتين مرتبطتين («الادعاء نفسه») بتكرار وأهمية مشتركين.</p></section>''']
    for n in CHAPTERS: parts.append(render_chapter(n))
    parts.append(methodology()); parts.append(sources_appendix()); parts.append(ref_lists()); parts.append(toc())
    parts.append(f'<footer id="metadata"><h2>بيانات الملف</h2><p>{esc(TITLE)} · ملف المراجعة الإصدار v{esc(VER)} (Review file v{esc(VER)}) · أُنشئ من المواصفة {esc(SPEC)} (Generated from prompt {esc(SPEC)}) · تاريخ الإنشاء {TODAY} · نطاق دورة {esc(EXAM_SITTING)} · ملف البنك المرافق: bank.json في مجلد العمل بالمستودع · {total} سؤالاً في {len(CHAPTERS)} فصول · {cov_total} فقرة مغطاة من {total_subs}. لا يحوي الملف بيانات شخصية. ملف HTML واحد مستقل بلا موارد خارجية.</p>'
                 f'<div class="notice"><p>أُنشئ بأداة SVU MBA Course Review Generator، المواصفة {esc(SPEC)} · ملف المراجعة v{esc(VER)}</p>'
                 f'<p>المصدر وأحدث إصدار: <a href="{REPO}" class="ltr">{REPO}</a></p>'
                 f'<p>رخصة الأداة وهذا الملف: <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ar" class="ltr">CC BY-NC-SA 4.0</a> — شارك بحرية، وانسب المصدر، ولا تبع أبداً. الرخصة تغطي محتوى المراجعة نفسها (الشروح والاختيار والترتيب)، أما نصوص الكتاب والامتحانات المقتبسة فتبقى لأصحابها وليست مشمولة.</p></div></footer>')
    parts.append('</main>')
    if SYMBOLS:
        parts.append('<div id="symsheet" hidden><div class="sh-box"><button class="sh-x" aria-label="إغلاق">✕</button><div class="sh-body"></div><div class="sh-nav"></div></div></div>')
        parts.append('<script>window.SYMS=' + json.dumps(SYMBOLS, ensure_ascii=False) + ';' + SYM_JS + '</script>')
    parts.append(f'<script>{JS.replace("__KEY__", STATE_KEY)}</script></body></html>')
    return fold_sections("\n".join(parts))

if __name__ == "__main__":
    out = build()
    dst = os.path.join(HERE, "..", "out.html")
    with open(dst, "w", encoding="utf-8", newline="\n") as f: f.write(out)
    print("written", dst, len(out.encode("utf-8"))//1024, "KB")
