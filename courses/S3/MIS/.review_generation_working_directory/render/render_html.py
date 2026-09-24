# -*- coding: utf-8 -*-
"""Render bank.json -> single self-contained RTL HTML review file (MIS review, spec v0.11). Adapted from PRM; course specifics in meta_mis.py."""
import json, os, re, html, datetime, collections
HERE = os.path.dirname(__file__)
B = json.load(open(os.path.join(HERE, "..", "bank.json"), encoding="utf-8"))
QS = B["questions"]; SUBS = {int(k): v for k, v in B["subsections"].items()}
CHAPTERS = sorted(int(k) for k in B["subsections"])  # chapters actually present in the bank
OPENERS_BANK = {int(k): tuple(v) for k, v in B.get("openers", {}).items()}
FOCUS = set(tuple(x) for x in B["focus_areas"])
TITLE = B["title"]; SPEC = B["spec_version"]; VER = B["file_version"]
LETTERS = ["أ", "ب", "ج", "د", "هـ", "و"]
from meta_mis import GENERATED_DATE
TODAY = GENERATED_DATE
try:
    QA = json.load(open(os.path.join(HERE, "..", "qa", "summary.json"), encoding="utf-8"))
except FileNotFoundError:
    QA = {}

from meta_mis import *  # MIS-specific tables: CH_TITLES, CH_PAGES, OPENERS, SRC_NAMES, REPO, FILES, SRC_ROW, FILES_SUMMARY, SEC_NAMES, SEC_INTRO, COURSE_LINE, CHAPTER_LIST_AR
CHAPTERS = sorted(int(k) for k in B["subsections"])  # override meta: chapters present in the bank

def esc(s): return html.escape(s or "", quote=True)
def md(s):
    s = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
def stars(n): return "★"*n + "☆"*(5-n)

def render_table(t, cls):
    """Data table of a question (§7d): header row; numeric/code cells left-to-right, Arabic cells right-to-left."""
    if not t: return ""
    cell = (lambda c: f'<td class="ltr">{esc(str(c))}</td>') if t["ltr"] else (lambda c: f'<td>{esc(str(c))}</td>')
    cap = f'<caption>{esc(t["caption"])}</caption>' if t["caption"] else ""
    head = "".join(f'<th>{abbr(esc(str(h)))}</th>' for h in t["head"])
    body = "".join("<tr>" + "".join(cell(c) for c in r) + "</tr>" for r in t["rows"])
    return f'<div class="tw"><table class="{cls}">{cap}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

SYMBOLS = globals().get("SYMBOLS", {})
_SYM_RE = re.compile(r"(?<![A-Za-z])([A-Z][A-Za-z]{0,4})(?![A-Za-z])")
def symbols_used(q):
    """Symbols (from the course SYMBOLS glossary) that this record's tables and calculation actually use, first-appearance order."""
    texts = []
    for t in (q.get("table"), q.get("ans_table")):
        if t: texts.append(" ".join(str(h) for h in t["head"]))
    c = q.get("calc")
    if c:
        texts += c["given"] + [st["what"] + " " + st["eq"] for st in c["steps"]]
    texts.append(q["stem"])
    seen, out = set(), []
    for tok in _SYM_RE.findall(" ".join(texts)):
        if tok in SYMBOLS and tok not in seen:
            seen.add(tok); out.append(tok)
    return out

def sym_lines(k):
    d = SYMBOLS[k]
    return [d["ar"] + " (" + d["en"] + ")"] + ([d["f"]] if d["f"] else []) + [d["note"]]

def abbr(text):
    """Wrap every glossary symbol in already-escaped text with <abbr> whose tooltip has one line per field (each line keeps its own direction)."""
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
                     f'<span class="p-en ltr">{esc(d["en"])}</span>{f}<span class="p-n">{esc(d["note"])}</span></span></span>')
    return f'<div class="{cls}"><span class="slbl">الرموز:</span> {"".join(chips)} <span class="shint">اضغط على أي رمز للشرح الكامل</span></div>'

SYM_JS = r"""(function(){
var sheet=document.getElementById('symsheet');if(!sheet)return;
var body=sheet.querySelector('.sh-body'),nav=sheet.querySelector('.sh-nav');
function esc(t){return t.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function show(k,q){var d=window.SYMS[k];if(!d)return;
 body.innerHTML='<span class="p-ar"><b class="ltr">'+esc(k)+'</b> = '+esc(d.ar)+'</span><span class="p-en ltr">'+esc(d.en)+'</span>'+(d.f?'<span class="p-f">'+esc(d.f)+'</span>':'')+'<span class="p-n">'+esc(d.note)+'</span>';
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

def render_calc(c):
    """Calculation block (§7d): given values, then one row per step — المعادلة → التعويض → الناتج."""
    if not c: return ""
    out = ['<div class="calc"><p class="a-calc"><span class="lbl">الحساب:</span></p>']
    if c["given"]:
        out.append('<ul class="given">' + "".join(f'<li>{abbr(md(g))}</li>' for g in c["given"]) + "</ul>")
    rows = []
    for i, st in enumerate(c["steps"], 1):
        note = f'<div class="cnote">{md(st["note"])}</div>' if st["note"] else ""
        rows.append(f'<tr><td class="cwhat" data-l="المطلوب">{i}. {abbr(md(st["what"]))}</td>'
                    f'<td class="ltr ceq" data-l="المعادلة"><span>{abbr(esc(st["eq"]))}</span></td>'
                    f'<td class="ltr csub" data-l="التعويض"><span>{esc(st["sub"])}</span></td>'
                    f'<td class="cres" data-l="الناتج"><b>{esc(st["res"])}</b>{note}</td></tr>')
    out.append('<div class="tw"><table class="ctbl"><thead><tr><th>المطلوب</th><th>المعادلة</th><th>التعويض</th><th>الناتج</th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>')
    if c["note"]: out.append(f'<p class="cfinal">{md(c["note"])}</p>')
    out.append("</div>")
    return "".join(out)

def render_q(q, num, sec):
    types = q["types"]
    tags = " ".join(f'<span class="tag t-{t}">{SEC_NAMES[t] if t!="generated" else "مولَّد"}</span>' for t in types)
    data_sec = " ".join(types)
    if "generated" in types:
        srcs = 'المصدر: مولَّد لسد فجوة (البند 9 من المواصفة)'
    else:
        srcs = "المصادر: " + "، ".join(f'{esc(SRC_NAMES.get(s, s))} <a class="srcref" href="#src-{SRC_ROW[s]}" title="ملف المصدر رقم {SRC_ROW[s]} في ملحق ملفات المصدر">#{SRC_ROW[s]}</a>' for s in q["sources"])
    qt = {"mcq":"اختيار من متعدد","tf":"صح / خطأ","short":"سؤال قصير","essay":"مقالي"}[q["qtype"]]
    recon = ' <span class="tag recon">خيارات معاد بناؤها</span>' if q["reconstructed"] else ""
    lowc = ' <span class="tag lowc">⚠</span>' if q["low_conf"] else ""
    meta1 = f'<div class="meta"><span class="qid">{esc(q["id"])}</span> · <span>{qt}</span> · {tags}{recon}{lowc}</div>'
    freq_txt = "مولَّد — التكرار: 0" if "generated" in types else f'التكرار: {q["freq"]} {"مصدر مستقل" if q["freq"]==1 else "مصادر مستقلة"}'
    meta2 = f'<div class="meta"><span>{freq_txt}</span> · <span class="imp" title="الأهمية {q["importance"]}/5">{stars(q["importance"])} <small>{q["importance"]}/5</small></span> · <span>الفقرة {esc(q["sub"])}: {esc(q["subname"])}</span></div>'
    stem = f'<p class="stem"><span class="num">{num}.</span> {esc(q["stem"])}</p>' + render_table(q.get("table"), "qtbl")
    if q.get("table") or q.get("calc") or q.get("ans_table"):
        stem += render_symbols(q, "syms")
    opts = ""
    if q["qtype"] == "mcq":
        opts = '<ol class="opts">' + "".join(f'<li><span class="let">{LETTERS[i]})</span> {esc(o)}</li>' for i, o in enumerate(q["options"])) + "</ol>"
    elif q["qtype"] == "tf":
        opts = '<p class="opts tf">( صح / خطأ )</p>'
    orig = f'<p class="orig">نص الطالب الأصلي: {esc(q["original"])}</p>' if q["original"] else ""
    # answer block
    if q["qtype"] == "mcq":
        ans_line = f'{LETTERS[q["ans"]]} — {esc(q["options"][q["ans"]])}'
    else:
        ans_line = esc(q["ans"])
    lines = [f'<p class="a-ans"><span class="lbl">✔ الإجابة:</span> {ans_line}</p>',
             render_table(q.get("ans_table"), "qtbl atbl") + render_calc(q.get("calc")),
             f'<p class="a-why"><span class="lbl">لماذا:</span> {md(q["why"])}</p>',
             f'<p class="a-rem"><span class="lbl">تذكّر:</span> {md(q["remember"])}</p>']
    if q["distractors"]:
        lines.append(f'<p class="a-dis"><span class="lbl">المشتتات:</span> {md(q["distractors"])}</p>')
    runs = []   # consecutive pages as ranges, in the record's order (MIS: printed page = PDF page)
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
    vars_html = ""
    if q["variants"]:
        vars_html = '<details class="vars"><summary>صيغ أخرى في المصادر</summary><ul>' + "".join(f"<li>{esc(v)}</li>" for v in q["variants"]) + "</ul></details>"
    srcline = f'<p class="meta src">{srcs}</p>'
    return (f'<article class="q" id="{esc(q["id"])}" data-section="{data_sec}" data-chapter="{q["ch"]}" '
            f'data-importance="{q["importance"]}" data-freq="{q["freq"]}" data-sec="{sec}">'
            f'{meta1}{stem}{opts}{orig}{meta2}'
            f'<details class="ans"><summary><span class="show">إظهار الإجابة</span><span class="hide">إخفاء الإجابة</span></summary>'
            f'<div class="ablock">{"".join(lines)}{srcline}{vars_html}</div></details></article>')

def order_key(q):
    return (-q["importance"], -q["freq"], 0 if q["qtype"]=="mcq" else 1, q["id"])

def render_chapter(n):
    qs = [q for q in QS if q["ch"]==n]
    about, terms = OPENERS_BANK.get(n) or OPENERS[n]
    parts = [f'<section class="chapter" id="ch{n}" data-chapter="{n}"><details class="chd" open><summary><h2>الفصل {n}: {esc(CH_TITLES[n])} <small class="meta">الكتاب ص {CH_PAGES[n][0]}–{CH_PAGES[n][1]} · <span class="cnt" data-total="{len(qs)}">{len(qs)} سؤالاً</span></small><span class="tog meta"><span class="hide">طيّ ▲</span><span class="show">فتح ▼</span></span></h2></summary>',
             f'<div class="opener"><div class="olbl">في هذا الفصل</div><p>{esc(about)}</p><p>{md(terms)}</p></div>']
    num = 0; done = set()
    for sec in ["exam","textbook","other","generated"]:
        sq = sorted([q for q in qs if sec in q["types"] and q["id"] not in done], key=order_key)
        done.update(q["id"] for q in sq)
        if not sq:
            if sec == "generated":
                parts.append(f'<div class="secnote meta">هذا الفصل لم يحتج إلى أسئلة مولَّدة: جميع فقراته مغطاة بأسئلة حقيقية.</div>')
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
    cs = B.get("coverage_stats", {}); real_cov = cs.get("direct", total_subs - gen); gen_cov = cs.get("generated_only", 0); unc = cs.get("uncovered", 0); ment = cs.get("mentioned_only", 0)
    focus_rows = [r for r in B["focus_table"] if (r["ch"], r["sub"]) in FOCUS]
    ft = "".join(f'<tr><td>{r["ch"]}</td><td>{esc(r["sub"])}</td><td>{esc(r["name"])}</td><td>{r["exam"]}</td><td>{r["textbook"]}</td><td>{r["other"]}</td><td>{r["total"]}</td></tr>' for r in sorted(focus_rows, key=lambda r:(r["ch"], -r["exam"], -r["total"])))
    led = "".join(f'<tr><td class="ltr">{esc(e["id"])}</td><td>{esc("؛ ".join(e["files"]))}</td><td>{esc(e["type"])}</td><td>{esc(e["decision"])}</td></tr>' for e in B["source_ledger"])
    ledger = f'<table class="tbl"><thead><tr><th>المعرّف</th><th>الملفات</th><th>النوع</th><th>القرار</th></tr></thead><tbody>{led}</tbody></table>'
    cm = "".join(f'<tr><td>{esc(r["source"])}</td><td>{esc(str(r["book_chapter"]))}</td><td>{esc(r["evidence"])}</td></tr>' for r in B["chapter_map"])
    chmap = f'<table class="tbl"><thead><tr><th>تسمية المصدر</th><th>فصل الكتاب</th><th>الدليل</th></tr></thead><tbody>{cm}</tbody></table>'
    unres = "".join(f"<li>{esc(u)}</li>" for u in QA.get("unresolved", []))
    asem = QA.get("asem", "")
    return f"""
<section id="method"><h2>المنهجية</h2>
<h3>قراءة المرجع وتحقق أداة الاستخراج</h3>
<p>{METHOD_EXTRACTION.format(pages=BOOK_PAGES, images=QA.get("images", "—"))}</p>
<h3>منهاجان في المجلد</h3>
<p>{METHOD_CURRICULA}</p>
<h3>سجل المصادر</h3>{ledger}
<h3>خريطة الفصول</h3>{chmap}
<h3>التكرار والتحقق</h3>
<p>{METHOD_DUP}</p>
<p><b>التحقق المتقاطع مع ملخص عاصم:</b> {esc(asem)}</p>
<h3>إعادة بناء أسئلة الامتحانات</h3>
<p>الأسئلة التي نقلها الطلاب بصيغة حرة («تعريف X»، جملة ناقصة مع الجواب) وكان واضحاً أنها اختيار من متعدد أُعيد بناؤها بخيارات من مصطلحات الفصل نفسه، مع وسم «خيارات معاد بناؤها» وإبقاء نص الطالب الأصلي أسفل السؤال. عدد الأسئلة المعاد بناؤها: <b>{recon}</b>. أسئلة الكتاب والمصادر الأخرى بقيت بصيغتها الأصلية.</p>
<h3>تدقيق التغطية والأسئلة المولَّدة</h3>
<p>قُسّمت الفصول الثمانية إلى <b>{total_subs}</b> فقرة وفق فهرس الكتاب (أدقّ مستوى في الفهرس: العناوين «N-M-K»، وحيث لا تفريع للفقرة عنوان القسم «N-M» نفسه؛ اختير هذا المستوى لأن مستوى الأقسام وحده لا يعطي إلا 30 فقرة للفصول الثمانية). <b>{real_cov}</b> فقرة غطّتها أسئلة حقيقية، و<b>{gen_cov}</b> فقرة كُتب لها أسئلة من نص الكتاب (القسم الرابع في كل فصل: <b>{gen}</b> سؤالاً مولَّداً)، و<b>{unc}</b> فقرة بقيت بلا سؤال ({ment} منها مذكورة داخل الشروح فقط). التغطية النهائية: <b>{total_subs - unc} من {total_subs}</b>. تحقق آلي من أن كل مولَّد يغطي فقرة لا سؤال حقيقي فيها. وضع التشغيل كان DECIDE فطُبّقت قاعدته: توليد سؤال للفقرات غير المغطاة التي هي مجال تركيز، مع حدّ ثلاثة أسئلة جديدة في الفصل للفقرات الأخرى؛ الأسئلة المولَّدة في الإصدار v0.2 التي ما زالت تغطي فقرة بلا سؤال حقيقي أُبقيت بعد إعادة التحقق منها. لم يتجاوز المولَّد ثلث البنك ولا عدد الأسئلة الحقيقية في أي فصل.</p>
<h3>مجالات التركيز ودرجة الأهمية</h3>
<p>لكل فقرة عُدّت الأسئلة المميزة بحسب الأصل (امتحان / كتاب / أخرى) ورُتّبت الفقرات بعدد أسئلة الامتحان ثم المجموع. <b>مجال التركيز</b> في كل فصل = الفقرات التي سألتها دورتان أو أكثر، وإن قلّت عن اثنتين أُخذت أعلى فقرتين سألتهما دورة واحدة على الأقل. الدرجة (1–5): الأساس من عدد الدورات المستقلة التي ورد فيها السؤال (0 ← 1، 1 ← 2، 2 ← 3، 3 فأكثر ← 4)، زائد 1 إن كان السؤال أيضاً من أسئلة الكتاب، زائد 1 إن كانت فقرته مجال تركيز، والحد الأقصى 5؛ المولَّد يثبت على 1. الدرجة معونة للدراسة لا توقّع للامتحان.</p>
<table class="tbl"><thead><tr><th>الفصل</th><th>الفقرة</th><th>الاسم</th><th>امتحان</th><th>كتاب</th><th>أخرى</th><th>المجموع</th></tr></thead><tbody>{ft}</tbody></table>
<h3>الثقة المنخفضة</h3>
<p>أُضيف سطر «⚠ ثقة منخفضة» إلى <b>{len(lowc)}</b> سؤالاً فقط: حيث نُقل السؤال من الذاكرة بصيغة قد تعني أمرين، أو اختلفت المصادر ولم يحسمها الكتاب، أو استند الجواب إلى جملة عابرة أو إلى منهاج أقدم. غياب السطر يعني تحققاً عادياً.</p>
<h3>أسئلة خارج النطاق أو لم يمكن حسمها</h3>
<ul>{unres}</ul>
<h3>ترتيب الأولويات عند التعارض</h3>
<p>اتُّبع الترتيب: دقة المرجع ← أمانة الصياغة ← الإيجاز ← الشكل. تجاوز بعض كتل الإجابة حدَّ 80 كلمة كان مقصوداً في الأسئلة المقالية والتعاريف الطويلة وحيث لزم سطر «يقول الكتاب» أو «مصدر آخر» أو إعادة بناء الخيارات، وفق البند 0أ من المواصفة.</p>
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
<p class="meta">{s["files"]} ملفاً · {s["sources"]} مصادر مستقلة استُخدمت للأسئلة (الكتاب، ثلاث دورات امتحانية، ملخص عاصم، خمس مجموعات من المنهاج الأقدم) · {s["excluded"]} ملفاً مستبعداً · {s["duplicates"]} نسخ مكررة أو تابعة · {s["images"]} صورة فُحصت بصرياً.</p>
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
:root{--bg:#fbfaf7;--fg:#1f2328;--muted:#6b7280;--line:#e5e2da;--card:#ffffff;--ans:#166534;--ansbg:#f0fdf4;--why:#1e3a8a;--red:#b91c1c;--amber:#b45309;--tint:#eef2ff;--accent:#2563eb;--chip:#f3f4f6;--chipon:#1f2328;--chipontext:#fff}
:root[data-theme="dark"]{--bg:#111418;--fg:#e6e6e6;--muted:#9aa0a6;--line:#2a2f36;--card:#181c22;--ans:#4ade80;--ansbg:#0f2419;--why:#93c5fd;--red:#f87171;--amber:#fbbf24;--tint:#1a2033;--accent:#60a5fa;--chip:#232a33;--chipon:#e6e6e6;--chipontext:#111}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#111418;--fg:#e6e6e6;--muted:#9aa0a6;--line:#2a2f36;--card:#181c22;--ans:#4ade80;--ansbg:#0f2419;--why:#93c5fd;--red:#f87171;--amber:#fbbf24;--tint:#1a2033;--accent:#60a5fa;--chip:#232a33;--chipon:#e6e6e6;--chipontext:#111}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font-family:"Segoe UI","Noto Naskh Arabic","Tahoma","Arial",sans-serif;font-size:17px;line-height:1.75;direction:rtl;text-align:right}
main{max-width:960px;margin:0 auto;padding:16px 20px 80px}
h1,h2,h3{line-height:1.3}
h2{margin-top:56px;border-bottom:2px solid var(--line);padding-bottom:6px}
h3.sech{margin-top:36px;color:var(--fg)}
details.chd > summary,details.secd > summary{cursor:pointer;list-style:none}
details.chd > summary::-webkit-details-marker,details.secd > summary::-webkit-details-marker{display:none}
details.chd > summary h2,details.secd > summary h3{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.tog{margin-inline-start:auto;font-size:.75em;font-weight:normal;white-space:nowrap}
details.chd > summary .tog .hide,details.secd > summary .tog .hide{display:none}
details.chd[open] > summary .tog .hide,details.secd[open] > summary .tog .hide{display:inline}
details.chd[open] > summary .tog .show,details.secd[open] > summary .tog .show{display:none}
details.chd:not([open]) > summary h2{margin-bottom:0}
p{margin:.4em 0}
a{color:var(--accent)}
.meta{color:var(--muted);font-size:.82em}
.cover{padding:48px 0 12px}
.cover h1{font-size:2em;margin:0 0 8px}
.cover .sub{color:var(--muted);font-size:1.05em}
.toolbar{position:sticky;top:0;z-index:20;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0}
.toolbar .bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.toolbar .grp{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.chip{border:1px solid var(--line);background:var(--chip);color:var(--fg);border-radius:999px;padding:3px 12px;cursor:pointer;font:inherit;font-size:.85em}
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
 .filters .chip,.filters select,.filters .sl{min-height:44px}
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
.opener{background:var(--tint);border-radius:12px;padding:12px 16px;margin:14px 0 22px}
.opener .olbl{font-size:.8em;color:var(--muted);margin-bottom:2px}
.opener p{margin:.2em 0}
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
.tag.recon{color:var(--amber);border-color:var(--amber)}
.tag.lowc{color:var(--amber);border-color:var(--amber)}
.imp{letter-spacing:1px}
details.ans{margin-top:8px}
details.ans > summary{cursor:pointer;list-style:none;display:inline-block;border:1px solid var(--line);border-radius:8px;padding:3px 12px;font-size:.9em;color:var(--fg);background:var(--chip)}
details.ans > summary::-webkit-details-marker{display:none}
details.ans > summary .hide{display:none}
details.ans[open] > summary .hide{display:inline}
details.ans[open] > summary .show{display:none}
.ablock{margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}
.ablock p{margin:.35em 0}
.lbl{font-weight:600;margin-inline-end:4px}
.a-ans{color:var(--ans);background:var(--ansbg);border-radius:8px;padding:4px 10px}
.a-why,.a-rem,.a-dis{color:var(--fg)}
.a-why .lbl,.a-rem .lbl,.a-dis .lbl{color:var(--why)}
.a-ref{color:var(--muted);font-size:.9em}
.a-red{color:var(--red)}
.a-amber{color:var(--amber)}
.a-sci{color:var(--red)}
.src{margin-top:6px}
details.vars{font-size:.85em;color:var(--muted);margin-top:6px}
details.vars summary{cursor:pointer}
.tw{overflow-x:auto;margin:8px 0}
.qtbl,.ctbl{border-collapse:collapse;font-size:.92em}
.qtbl th,.qtbl td,.ctbl th,.ctbl td{border:1px solid var(--line);padding:3px 10px;text-align:center;vertical-align:top;white-space:nowrap}
.qtbl th,.ctbl th{background:var(--chip);font-weight:600}
.qtbl caption{caption-side:top;text-align:start;color:var(--muted);font-size:.9em;padding:2px 0}
.qtbl.atbl{font-size:.88em}
.syms{font-size:.85em;margin:4px 0 8px;display:flex;flex-wrap:wrap;gap:4px 6px;align-items:center;line-height:1.5}
.syms .slbl{color:var(--why);font-weight:600}
.syms .chip{display:inline-block;position:relative;border:1px solid var(--line);background:var(--chip);border-radius:999px;padding:1px 10px;cursor:help;color:var(--fg)}
.syms .chip:hover,.syms .chip:focus{border-color:var(--why);outline:none}
.syms .pop{display:none;position:absolute;top:calc(100% + 4px);inset-inline-start:0;z-index:20;width:max-content;min-width:16em;max-width:min(26em,85vw);background:var(--card);color:var(--fg);border:1px solid var(--why);border-radius:10px;padding:8px 12px;box-shadow:0 6px 18px rgba(0,0,0,.25);font-size:1em;line-height:1.6;white-space:normal;text-align:start;cursor:auto}
@media (hover:hover){.syms .chip:hover .pop{display:block}}
#symsheet{position:fixed;inset:0;z-index:1000;background:rgba(0,0,0,.45);display:flex;align-items:flex-end;justify-content:center}
#symsheet[hidden]{display:none}
#symsheet .sh-box{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:16px 16px 0 0;width:100%;max-width:34em;padding:12px 16px calc(16px + env(safe-area-inset-bottom));box-shadow:0 -6px 24px rgba(0,0,0,.3);line-height:1.7;max-height:70vh;overflow:auto}
#symsheet .sh-x{float:left;border:1px solid var(--line);background:var(--chip);color:var(--fg);border-radius:999px;width:2em;height:2em;font-size:1em;cursor:pointer}
#symsheet .sh-body > span{display:block}
#symsheet .p-ar{font-weight:600;font-size:1.05em}
#symsheet .p-en{color:var(--muted);font-size:.92em}
#symsheet .p-f{font-family:Consolas,"Courier New",monospace;background:var(--chip);border-radius:6px;padding:2px 10px;margin:4px 0;display:inline-block;direction:ltr;unicode-bidi:isolate}
#symsheet .p-n{margin-top:4px}
#symsheet .sh-nav{margin-top:8px;display:flex;flex-wrap:wrap;gap:4px 6px;font-size:.85em}
#symsheet .sh-nav .chip{cursor:pointer;display:inline-block;border:1px solid var(--line);background:var(--chip);border-radius:999px;padding:1px 10px;direction:ltr}
#symsheet .sh-nav .chip.open{border-color:var(--why);color:var(--why);font-weight:600}
#symsheet .sh-nav .slbl{color:var(--why);font-weight:600}
@media (min-width:601px){#symsheet .sh-box{border-radius:16px;margin-bottom:6vh}}
.syms .pop > span{display:block}
.syms .pop .p-ar{font-weight:600}
.syms .pop .p-en{color:var(--muted);font-size:.9em}
.syms .pop .p-f{font-family:Consolas,"Courier New",monospace;background:var(--chip);border-radius:6px;padding:1px 8px;margin:3px 0;display:inline-block}
.syms .pop .p-n{margin-top:2px}
.syms .chip b{color:var(--why);margin-inline-end:4px}
.syms .shint{color:var(--muted);flex-basis:100%;font-size:.9em}
abbr[title]{text-decoration:underline dotted;text-underline-offset:3px;cursor:help;color:inherit}
.qtbl th abbr,.ctbl abbr{text-decoration-color:var(--why)}
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
footer{margin-top:60px;color:var(--muted);font-size:.85em;border-top:1px solid var(--line);padding-top:12px}
[dir="ltr"],.ltr{direction:ltr;text-align:left;unicode-bidi:isolate}
@media (max-width:600px){.ctbl thead{display:none}.ctbl,.ctbl tbody,.ctbl tr,.ctbl td{display:block;width:100%;box-sizing:border-box}.ctbl tr{border:1px solid var(--line);border-radius:8px;margin:6px 0;padding:4px 8px}.ctbl td{border:0;padding:2px 0;text-align:start;white-space:normal!important}.ctbl td.ltr{direction:rtl;text-align:start}.ctbl td.ltr::after{content:none}.ctbl td::before{content:attr(data-l) ": ";color:var(--muted);font-size:.85em}.ctbl td.ceq span,.ctbl td.csub span{direction:ltr;unicode-bidi:isolate}body{font-size:16px}main{padding:10px 12px 60px}.q{padding:12px}.toolbar input{min-width:120px}}
@media print{.toolbar,.noprint{display:none!important}.tbl.files{display:table}details.ans,details.reflist,details.vars,details.chd,details.secd,details.pgd{display:block}.tog{display:none}details.ans > summary{display:none}details > *:not(summary){display:block}.q{break-inside:avoid;border-color:#bbb}.hidden{display:block!important}body{background:#fff;color:#000}a{color:#000;text-decoration:none}}
"""

JS = """
(function(){var KEY="__KEY__";var FMAX=parseInt(document.getElementById("freq").max)||5;
var root=document.documentElement;
var modeBtns=document.querySelectorAll('[data-mode]'),impSl=document.getElementById('imp'),freqSl=document.getElementById('freq'),impV=document.getElementById('impv'),freqV=document.getElementById('freqv');
var chSel=document.getElementById('chsel'),search=document.getElementById('search'),counter=document.getElementById('counter');
var state={mode:'all',imp:1,freq:0,ch:'all',q:''};
function clampI(v,lo,hi){v=parseInt(v);return isNaN(v)?lo:Math.min(hi,Math.max(lo,v));}
try{var saved=JSON.parse(localStorage.getItem(KEY+'_review_state')||'{}');if(saved.mode)state.mode=saved.mode;if(saved.imp!=null)state.imp=clampI(saved.imp,1,5);if(saved.freq!=null)state.freq=clampI(saved.freq,0,FMAX);if(saved.ch)state.ch=saved.ch;}catch(e){}
var h=location.hash.replace('#','');if(/^mode=/.test(h)){h.split('&').forEach(function(kv){var p=kv.split('=');if(p[0]==='mode')state.mode=p[1];if(p[0]==='imp')state.imp=clampI(p[1],1,5);if(p[0]==='freq')state.freq=clampI(p[1],0,FMAX);if(p[0]==='ch')state.ch=p[1];});}
function norm(s){return (s||'').toLowerCase().replace(/[\\u064B-\\u0652\\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي');}
var MODE_NAMES={all:'الكل',exam:'الامتحانات',textbook:'الكتاب',other:'مصادر أخرى',generated:'مولَّدة'};
function cntText(el,vis){var tot=parseInt(el.getAttribute('data-total'));var paren=el.textContent.charAt(0)==='(';
 var s=vis===tot?tot+' سؤالاً':vis+' من '+tot;el.textContent=paren?'('+(vis===tot?tot:vis+'/'+tot)+')':s;}
function apply(reveal){
 var qs=document.querySelectorAll('article.q'),shown=0,total=qs.length,nq=norm(state.q);
 qs.forEach(function(a){
  var ok=true;
  if(state.mode!=='all'&&a.getAttribute('data-section').split(' ').indexOf(state.mode)<0)ok=false;
  if(parseInt(a.getAttribute('data-importance'))<state.imp)ok=false;
  if(parseInt(a.getAttribute('data-freq'))<state.freq)ok=false;
  if(state.ch!=='all'&&a.getAttribute('data-chapter')!==state.ch)ok=false;
  if(nq&&norm(a.textContent).indexOf(nq)<0)ok=false;
  a.classList.toggle('hidden',!ok);if(ok)shown++;
 });
 document.querySelectorAll('section.chapter').forEach(function(s){var n=s.querySelectorAll('article.q:not(.hidden)').length;s.classList.toggle('hidden',n===0);
  var c=s.querySelector('details.chd > summary .cnt');if(c)cntText(c,n);
  if(reveal&&n>0){s.querySelector('details.chd').open=true;}
  s.querySelectorAll('details.secd').forEach(function(d){var m=d.querySelectorAll('article.q:not(.hidden)').length;d.classList.toggle('hidden',m===0);
   var sc=d.querySelector('summary .cnt');if(sc)cntText(sc,m);if(reveal&&m>0)d.open=true;});
 });
 counter.textContent=shown+' من '+total+' سؤالاً';
 var parts=[];if(state.mode!=='all')parts.push(MODE_NAMES[state.mode]);if(state.imp>1)parts.push('★'+state.imp+'+');if(state.freq>0)parts.push('تكرار '+state.freq+'+');if(state.ch!=='all')parts.push('الفصل '+state.ch);if(state.q)parts.push('بحث: «'+state.q+'»');
 var nf=parts.length;fbadge.textContent=nf;fbadge.hidden=nf===0;ftog.classList.toggle('on',nf>0);
 fsum.textContent=(nf>0&&tb.classList.contains('fclosed'))?parts.join(' · '):'';
 modeBtns.forEach(function(b){b.classList.toggle('on',b.getAttribute('data-mode')===state.mode);});
 impSl.value=state.imp;freqSl.value=state.freq;
 impV.textContent=state.imp<=1?'الكل':state.imp+'+';freqV.textContent=state.freq<=0?'الكل':state.freq+'+';
 impSl.parentElement.classList.toggle('on',state.imp>1);freqSl.parentElement.classList.toggle('on',state.freq>0);
 chSel.value=state.ch;if(search.value!==state.q)search.value=state.q;
 try{localStorage.setItem(KEY+'_review_state',JSON.stringify({mode:state.mode,imp:state.imp,freq:state.freq,ch:state.ch}));}catch(e){}
 var frag='mode='+state.mode+'&imp='+state.imp+'&freq='+state.freq+'&ch='+state.ch;
 if(location.hash.replace('#','')!==frag&&!/^Q\\d\\d-\\d\\d\\d$/.test(location.hash.replace('#',''))){history.replaceState(null,'','#'+frag);}
}
var tb=document.querySelector('.toolbar'),ftog=document.getElementById('ftog'),fbadge=document.getElementById('fbadge'),fsum=document.getElementById('fsum');
modeBtns.forEach(function(b){b.addEventListener('click',function(){state.mode=b.getAttribute('data-mode');apply(true);});});
impSl.addEventListener('input',function(){state.imp=clampI(impSl.value,1,5);apply(true);});
freqSl.addEventListener('input',function(){state.freq=clampI(freqSl.value,0,FMAX);apply(true);});
chSel.addEventListener('change',function(){state.ch=chSel.value;apply(true);});
var t;search.addEventListener('input',function(){clearTimeout(t);t=setTimeout(function(){state.q=search.value;apply(!!state.q);},150);});
document.getElementById('reset').addEventListener('click',function(){state={mode:'all',imp:1,freq:0,ch:'all',q:''};search.value='';apply(false);});
document.getElementById('expand').addEventListener('click',function(){document.querySelectorAll('article.q:not(.hidden) details.ans').forEach(function(d){d.open=true;});});
document.getElementById('collapse').addEventListener('click',function(){document.querySelectorAll('details.ans').forEach(function(d){d.open=false;});});
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
window.addEventListener('hashchange',function(){var el=document.getElementById(location.hash.slice(1));if(el){var p=el;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}el.scrollIntoView();}});
var theme=document.getElementById('theme');
function setTheme(v){if(v)root.setAttribute('data-theme',v);else root.removeAttribute('data-theme');try{localStorage.setItem(KEY+'_theme',v||'');}catch(e){}theme.textContent=v==='dark'?'☀ فاتح':v==='light'?'🌙 داكن':'◐ المظهر';}
try{setTheme(localStorage.getItem(KEY+'_theme')||'');}catch(e){}
theme.addEventListener('click',function(){var cur=root.getAttribute('data-theme');var dark=cur?cur==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;setTheme(dark?'light':'dark');});
window.addEventListener('beforeprint',function(){document.querySelectorAll('details').forEach(function(d){d.open=true;});});
document.querySelectorAll('#toc a').forEach(function(a){a.addEventListener('click',function(){var el=document.getElementById(a.getAttribute('href').slice(1));if(el){el.querySelectorAll('details.chd').forEach(function(d){d.open=true;});}});});
apply(false);
})();
"""


# ---- §13a (v0.10): collapsible page sections, applied to the assembled page so IMT and PRM stay identical ----
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
    parts = [f'<title>{esc(TITLE)} — v{esc(VER)}</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><script>document.documentElement.className+=" js";</script><style>{CSS}</style>',
      '<main>',
      f'<header class="cover"><h1>{esc(TITLE)}</h1><p class="sub">{esc(COURSE_LINE)}</p>'
      f'<p class="meta">الإصدار v{esc(VER)} · الفصول: {CHAPTER_LIST_AR} · {total} سؤالاً · أسئلة الامتحانات {c["exam"]} · أسئلة الكتاب {c["textbook"]} · مصادر أخرى {c["other"]} · مولَّدة {gen}</p></header>',
      '<div class="toolbar noprint" role="toolbar" aria-label="أدوات القراءة">'
      '<div class="bar">'
      '<span class="counter" id="counter"></span><span class="fsum" id="fsum" aria-live="polite"></span>'
      '<button class="chip ftog" id="ftog" aria-expanded="true" aria-controls="filters">⚙ الفلاتر <span class="fbadge" id="fbadge" hidden></span></button>'
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
<p>كل سؤال يحمل ثلاث علامات: <b>التكرار</b> = عدد المصادر المستقلة التي سألته ({HOWTO_FREQ})؛ <b>الأهمية ★</b> من 1 إلى 5 مبنية على عدد امتحانات ورد فيها السؤال، زائد نقطة إن كان من أسئلة الكتاب، زائد نقطة إن كانت فقرته من مجالات تركيز المدرّس، وهي معونة للدراسة لا توقّع للامتحان؛ <b>⚠ ثقة منخفضة</b> يظهر فقط حيث يستند الجواب إلى دليل ضعيف أو نقل غير مؤكد، وغيابه يعني أن الإجابة تُحقق منها من الكتاب بالصفحة.</p>
<p>الإجابة مخفية خلف زر «إظهار الإجابة» ولا تحتاج جافاسكربت. الشريط الثابت في الأعلى يعرض العدّاد وزر «⚙ الفلاتر» والبحث؛ وخلف زر الفلاتر: وضع القراءة (نوع واحد من الأسئلة عبر كل الفصول: الامتحانات، الكتاب، مصادر أخرى، مولَّدة)، ومنزلقان لحدّ أدنى للأهمية (1–5) وللتكرار، واختيار فصل، وإظهار الإجابات أو إخفائها، وطيّ كل الفصول أو فتحها، وطيّ أنواع الأسئلة أو فتحها، مستقلةً عن حالة الإجابات (ويمكن طيّ أي فصل أو نوع منفرداً بالنقر على عنوانه، ويُحفظ ما طويته)، والمظهر الفاتح أو الداكن، وزر «إعادة ضبط التصفية». اختياراتك تُحفظ وتوضع في رابط الصفحة. على الهاتف تبدأ لوحة الفلاتر مطوية، وحين تكون مطوية وثمة تصفية فعّالة يظهر عددها على الزر وملخصها بجانب العدّاد. تنبيه: الأسئلة المولَّدة أهميتها 1 دائماً، فرفع منزلق الأهمية إلى 2 أو أكثر يخفيها كلها. الترتيب المقترح: أسئلة الامتحانات أولاً ثم أسئلة الكتاب ثم الباقي. الطباعة تُظهر كل الإجابات وتتجاهل التصفية.</p>
<p class="meta">الأقسام التمهيدية والختامية (كيف تستخدم هذا الملف، النطاق والمصادر، المنهجية، ملفات المصدر، القوائم المرجعية، فهرس المحتويات، بيانات الملف) تُطوى وتُفتح بالنقر على عنوانها مثل الفصول، ويُحفظ ما طويته. زرّا «طيّ الكل» و«فتح الكل» في الفلاتر يطويان الفصول وأنواع الأسئلة وهذه الأقسام معاً ويُبقيان الإجابات على حالها؛ الصفحة المطوية كلها قائمة عناوين قصيرة.</p>
<p class="meta">إخفاء الإجابات معونة للمذاكرة وليس حمايةً: نص الإجابة موجود في الملف ويصل إليه البحث والنسخ وعرض المصدر، فلا يُعتمد عليه في امتحان حقيقي. نصوص الكتاب والامتحانات المقتبسة تبقى ملكاً لأصحابها.</p>
<p class="pledge">شروط رخصة هذا الملف (CC BY-NC-SA 4.0): شارك هذا الملف مجاناً مع زملائك في المادة. أبقِ الإشعار الموجود في آخر الملف حتى يجد غيرك المصدر وأحدث إصدار. لا يجوز بيعه ولا وضعه خلف اشتراك أو جدار دفع.</p></section>''',
      f'''<section id="scope"><h2>النطاق والمصادر</h2>
<p>{SCOPE_TEXT.format(book=esc(BOOK_FILE), pages=BOOK_PAGES, chs=CHAPTER_LIST_AR, subs=total_subs)}</p>
<table class="tbl"><thead><tr><th>القسم</th><th>العدد</th><th>ما هو</th></tr></thead><tbody>
<tr><td>أسئلة الامتحانات</td><td>{c["exam"]}</td><td>{esc(SEC_INTRO["exam"])}</td></tr>
<tr><td>أسئلة الكتاب</td><td>{c["textbook"]}</td><td>{esc(SEC_INTRO["textbook"])}</td></tr>
<tr><td>مصادر أخرى</td><td>{c["other"]}</td><td>{esc(SEC_INTRO["other"])}</td></tr>
<tr><td>مولَّدة</td><td>{gen}</td><td>{esc(SEC_INTRO["generated"])}</td></tr></tbody></table>
<p class="meta">سؤال واحد قد يكون من الامتحانات ومن الكتاب معاً فيُحسب في القسمين ويظهر في وضعَي القراءة، لكنه يُعرض مرة واحدة (في قسم الامتحانات) مع وسم النوعين.</p></section>''']
    for n in CHAPTERS: parts.append(render_chapter(n))
    parts.append(methodology()); parts.append(sources_appendix()); parts.append(ref_lists()); parts.append(toc())
    parts.append(f'<footer id="metadata"><h2>بيانات الملف</h2><p>{esc(TITLE)} · ملف المراجعة الإصدار v{esc(VER)} (Review file v{esc(VER)}) · أُنشئ من المواصفة {esc(SPEC)} (Generated from prompt {esc(SPEC)}) · تاريخ الإنشاء {TODAY} · ملف البنك المرافق: bank.json في مجلد العمل بالمستودع · {total} سؤالاً في {len(CHAPTERS)} فصول · {cov_total} فقرة مغطاة من {total_subs}. لا يحوي الملف بيانات شخصية. ملف HTML واحد مستقل بلا موارد خارجية.</p>'
                 f'<div class="notice"><p>أُنشئ بأداة SVU MBA Course Review Generator، المواصفة {esc(SPEC)} · ملف المراجعة v{esc(VER)}</p>'
                 f'<p>المصدر وأحدث إصدار: <a href="{REPO}" class="ltr">{REPO}</a></p>'
                 f'<p>رخصة الأداة وهذا الملف: <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ar" class="ltr">CC BY-NC-SA 4.0</a> — شارك بحرية، وانسب المصدر، ولا تبع أبداً. الرخصة تغطي محتوى المراجعة نفسها (الشروح والاختيار والترتيب)، أما نصوص الكتاب والامتحانات المقتبسة فتبقى لأصحابها وليست مشمولة.</p></div></footer>')
    parts.append('</main>')
    if SYMBOLS:   # §7d symbol sheet only when the course has a glossary (MIS v1.0 has none)
        parts.append('<div id="symsheet" hidden><div class="sh-box"><button class="sh-x" aria-label="إغلاق">✕</button><div class="sh-body"></div><div class="sh-nav"></div></div></div>')
        parts.append('<script>window.SYMS=' + json.dumps(SYMBOLS, ensure_ascii=False) + ';' + SYM_JS + '</script>')
    parts.append(f'<script>{JS.replace("__KEY__", STATE_KEY)}</script>')
    return fold_sections("\n".join(parts))

if __name__ == "__main__":
    out = build()
    dst = os.path.join(HERE, "..", "out.html")
    with open(dst, "w", encoding="utf-8", newline="\n") as f: f.write(out)
    print("written", dst, len(out.encode("utf-8"))//1024, "KB")
