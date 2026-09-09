# -*- coding: utf-8 -*-
"""Render bank.json -> single self-contained RTL HTML review file (PRM review, spec v0.9)."""
import json, os, re, html, datetime, collections
HERE = os.path.dirname(__file__)
B = json.load(open(os.path.join(HERE, "..", "bank.json"), encoding="utf-8"))
QS = B["questions"]; SUBS = {int(k): v for k, v in B["subsections"].items()}
CHAPTERS = sorted(int(k) for k in B["subsections"])  # chapters actually present in the bank
OPENERS_BANK = {int(k): tuple(v) for k, v in B.get("openers", {}).items()}
FOCUS = set(tuple(x) for x in B["focus_areas"])
TITLE = B["title"]; SPEC = B["spec_version"]; VER = B["file_version"]
LETTERS = ["أ", "ب", "ج", "د", "هـ", "و"]
from meta_prm import GENERATED_DATE
TODAY = GENERATED_DATE
try:
    QA = json.load(open(os.path.join(HERE, "..", "qa", "summary.json"), encoding="utf-8"))
except FileNotFoundError:
    QA = {}

from meta_prm import *  # PRM-specific tables: CH_TITLES, CH_PAGES, OPENERS, SRC_NAMES, REPO, FILES, SRC_ROW, FILES_SUMMARY, SEC_NAMES, SEC_INTRO, COURSE_LINE, CHAPTER_LIST_AR
CHAPTERS = sorted(int(k) for k in B["subsections"])  # override meta: chapters present in the bank

def esc(s): return html.escape(s or "", quote=True)
def md(s):
    s = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
def stars(n): return "★"*n + "☆"*(5-n)

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
    stem = f'<p class="stem"><span class="num">{num}.</span> {esc(q["stem"])}</p>'
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
             f'<p class="a-why"><span class="lbl">لماذا:</span> {md(q["why"])}</p>',
             f'<p class="a-rem"><span class="lbl">تذكّر:</span> {md(q["remember"])}</p>']
    if q["distractors"]:
        lines.append(f'<p class="a-dis"><span class="lbl">المشتتات:</span> {md(q["distractors"])}</p>')
    pages = q["pages"]
    pg = f'ص {pages[0]}' if len(pages)==1 else f'ص {pages[0]}–{pages[-1]}' if len(pages)>3 else "ص " + "، ".join(str(p) for p in pages)
    lines.append(f'<p class="a-ref"><span class="lbl">المرجع:</span> الفصل {q["ch"]} · {pg} (PDF {pages[0] if len(pages)==1 else str(pages[0])+"–"+str(pages[-1])})</p>')
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
    real_cov = QA.get("subs_covered_real", total_subs - gen)
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
<p>قُرئ الكتاب كاملاً ({BOOK_PAGES} صفحة، 14 فصلاً). أرقام الصفحات المطبوعة تطابق أرقام صفحات PDF (تحقق آلي لكل صفحة: لا اختلاف). استُخرج النص بـ PyMuPDF وقورن بصورة الصفحة: الخط يُخرج حرفَي «لا» بترتيب معكوس («األول» بدل «الأول») فصُحّح ذلك على مستوى الحرف قبل أي استخدام. إجابات أسئلة المراجعة في نهاية الفصول يعلّمها الكتاب بتظليل أصفر لا بمفتاح مطبوع، فاستُخرج التظليل من الصورة وعُومل كإجابة الكتاب ثم تُحقق منه من نص الفصل. الملفات الممسوحة وبخط اليد والصور المضمّنة قُرئت بصرياً ({QA.get("images", "—")} صورة/صفحة).</p>
<h3>سجل المصادر</h3>{ledger}
<h3>خريطة الفصول</h3>{chmap}
<h3>التكرار والتحقق</h3>
<p>حُسبت بصمة MD5 لكل ملف قبل العدّ (حُذفت قبل التشغيل ست نسخ مكررة بطلب صاحب المجلد). النسخ التابعة (قائمة الأسئلة نفسها بخط اليد، أو منسوخة داخل ملف طالب آخر) عُدّت مصدراً واحداً. <b>التكرار</b> = عدد المصادر المستقلة التي وردت فيها فكرة السؤال (الدورات الست، الكتاب، ملخص عماد، مجموعة المراجعة، ملخص عاصم) لا عدد الملفات. كل إجابة تُحقق منها من نص الكتاب بصفحته؛ حين يخالف مصدرٌ الكتاب يُعرض جواب الكتاب مع سطر «مصدر آخر» أحمر. حين يخالف نص الفصل تظليل الكتاب نفسه عُرض الاثنان مع سطر «يقول الكتاب».</p>
<p><b>التحقق المتقاطع مع ملخص عاصم:</b> {esc(asem)}</p>
<h3>إعادة بناء أسئلة الامتحانات</h3>
<p>الأسئلة التي نقلها الطلاب بصيغة حرة وكان واضحاً أنها اختيار من متعدد أُعيد بناؤها بخيارات من مصطلحات الفصل نفسه، مع وسم «خيارات معاد بناؤها» وإبقاء نص الطالب الأصلي أسفل السؤال. عدد الأسئلة المعاد بناؤها: <b>{recon}</b>. المسائل الحسابية المنقولة (الشبكات، جداول القيمة المكتسبة، تسوية الموارد، التقدير بثلاث نقاط) حُلّت بطريقة الكتاب وذُكرت خطوات الحل باختصار في سطر «لماذا».</p>
<h3>تدقيق التغطية والأسئلة المولَّدة</h3>
<p>قُسّمت الفصول الأربعة عشر إلى <b>{total_subs}</b> فقرة وفق فهرس الكتاب (عناوين المستوى الثاني «N-M»؛ عناوين المستوى الثالث عُدّت موضوعات داخل فقرتها لأن الكتاب يفرّع بعض الفقرات إلى عشرين بنداً). <b>{real_cov}</b> فقرة غطّتها أسئلة حقيقية، والباقي كُتب له أسئلة من نص الكتاب (القسم الرابع في كل فصل): <b>{gen}</b> سؤالاً مولَّداً. التغطية النهائية: <b>{QA.get("subs_covered_total", total_subs)} من {total_subs}</b>. تحقق آلي من أن كل مولَّد يغطي فقرة لا سؤال حقيقي فيها. وضع التشغيل كان DECIDE فطُبّقت قاعدته: توليد سؤال للفقرات غير المغطاة مع حدّ ثلاثة للفقرات التي ليست مجال تركيز، ولم يتجاوز المولَّد ثلث البنك ولا عدد الأسئلة الحقيقية في أي فصل.</p>
<h3>مجالات التركيز ودرجة الأهمية</h3>
<p>لكل فقرة عُدّت الأسئلة المميزة بحسب الأصل (امتحان / كتاب / أخرى) ورُتّبت الفقرات بعدد أسئلة الامتحان ثم المجموع. <b>مجال التركيز</b> في كل فصل = الفقرات التي سألتها دورتان أو أكثر، وإن قلّت عن اثنتين أُخذت أعلى فقرتين سألتهما دورة واحدة على الأقل. الدرجة (1–5): الأساس من عدد الدورات المستقلة التي ورد فيها السؤال (0 ← 1، 1 ← 2، 2 ← 3، 3 فأكثر ← 4)، زائد 1 إن كان السؤال أيضاً من أسئلة الكتاب، زائد 1 إن كانت فقرته مجال تركيز، والحد الأقصى 5؛ المولَّد يثبت على 1. الدرجة معونة للدراسة لا توقّع للامتحان.</p>
<table class="tbl"><thead><tr><th>الفصل</th><th>الفقرة</th><th>الاسم</th><th>امتحان</th><th>كتاب</th><th>أخرى</th><th>المجموع</th></tr></thead><tbody>{ft}</tbody></table>
<h3>الثقة المنخفضة</h3>
<p>أُضيف سطر «⚠ ثقة منخفضة» إلى <b>{len(lowc)}</b> سؤالاً فقط: حيث نُقل السؤال من الذاكرة بصيغة قد تعني أمرين، أو اختلفت المصادر ولم يحسمها الكتاب، أو استند الجواب إلى جملة عابرة أو إلى منهاج أقدم. غياب السطر يعني تحققاً عادياً.</p>
<h3>أسئلة خارج النطاق أو لم يمكن حسمها</h3>
<ul>{unres}</ul>
<h3>ترتيب الأولويات عند التعارض</h3>
<p>اتُّبع الترتيب: دقة المرجع ← أمانة الصياغة ← الإيجاز ← الشكل. تجاوز بعض كتل الإجابة حدَّ 80 كلمة كان مقصوداً في الأسئلة المقالية والمسائل الحسابية وحيث لزم سطر «يقول الكتاب» أو «مصدر آخر» أو إعادة بناء الخيارات، وفق البند 0أ من المواصفة.</p>
<h3>الخصوصية وحقوق المادة</h3>
<p>إخفاء الإجابات معونة للمذاكرة وليس حمايةً: نص الإجابات موجود داخل الملف ويمكن الوصول إليه بالبحث أو النسخ أو أدوات الوصول أو عرض المصدر، فلا يُعتمد عليه في امتحان حقيقي. لا يحوي الملف أي بيانات شخصية عن المؤلف أو الجهاز. نصوص الكتاب وأسئلة الامتحانات المقتبسة هنا تبقى ملكاً لمؤلفيها والجامعة، وعلى القارئ احترام حقوقها عند مشاركة الملف.</p>
<h3>إصدار المواصفة ووضع التشغيل</h3>
<p>بُني هذا الملف بالمواصفة {esc(SPEC)} في وضع DECIDE (بلا توقف لأخذ رأي المستخدم): لا فصل تجريبي، والأسئلة المولَّدة وفق القاعدة أعلاه، وHTML هو الصيغة الوحيدة المنتَجة. نسخة PDF أو DOCX تُنتج عند الطلب من البنك نفسه.</p>
</section>"""

def sources_appendix():
    s = FILES_SUMMARY
    rows = "".join(f'<tr id="src-{n}"><td>{n}</td><td class="fn">{esc(path)}</td><td>{esc(kind)}</td><td>{esc(role)}</td><td class="ltr">{esc(grp)}</td><td>{esc(pages)}</td><td>{esc(note)}</td></tr>' for n, path, kind, role, grp, pages, note in FILES)
    return f"""<section id="sources"><h2>ملفات المصدر</h2>
<p>كل ملف وُجد في مجلد المادة مذكور هنا، بما فيها المستبعد والمكرر، ليعرف القارئ ممّ بُنيت المراجعة وما ينقصها. رقم كل ملف هو الرقم الذي يظهر عند كل سؤال في سطر «المصادر». أسماء الملفات كما وُردت؛ المادة نفسها غير منشورة مع المراجعة.</p>
<p class="meta">{s["files"]} ملفاً · {s["sources"]} مصادر مستقلة استُخدمت للأسئلة (الكتاب، ست دورات امتحانية، ملخص عماد، مجموعة المراجعة، ملخص عاصم) · {s["excluded"]} ملفاً مستبعداً · {s["duplicates"]} نسخ مكررة أو تابعة · {s["images"]} صورة فُحصت بصرياً.</p>
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
.tbl{border-collapse:collapse;width:100%;font-size:.88em;margin:10px 0;display:block;overflow-x:auto}
.tbl th,.tbl td{border:1px solid var(--line);padding:4px 8px;text-align:right;vertical-align:top}
.tbl th{background:var(--chip)}
.tbl.files .fn{direction:ltr;text-align:left;unicode-bidi:plaintext;word-break:break-all;font-size:.92em}
.tbl.files td:target,tr:target td{background:var(--ansbg)}
.srcref{text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:0 4px;direction:ltr;unicode-bidi:isolate}
.notice{margin-top:10px;padding:8px 12px;border:1px dashed var(--line);border-radius:8px}
.notice p{margin:.2em 0}
.pledge{border-inline-start:3px solid var(--line);padding-inline-start:10px;color:var(--muted);font-size:.92em}
details.reflist{margin:10px 0}
details.reflist summary{cursor:pointer;font-weight:600}
.hidden{display:none!important}
.chapter.hidden{display:none!important}
footer{margin-top:60px;color:var(--muted);font-size:.85em;border-top:1px solid var(--line);padding-top:12px}
[dir="ltr"],.ltr{direction:ltr;text-align:left;unicode-bidi:isolate}
@media (max-width:600px){body{font-size:16px}main{padding:10px 12px 60px}.q{padding:12px}.toolbar input{min-width:120px}}
@media print{.toolbar,.noprint{display:none!important}.tbl.files{display:table}details.ans,details.reflist,details.vars,details.chd,details.secd{display:block}.tog{display:none}details.ans > summary{display:none}details > *:not(summary){display:block}.q{break-inside:avoid;border-color:#bbb}.hidden{display:block!important}body{background:#fff;color:#000}a{color:#000;text-decoration:none}}
"""

JS = """
(function(){var FMAX=parseInt(document.getElementById("freq").max)||5;
var root=document.documentElement;
var modeBtns=document.querySelectorAll('[data-mode]'),impSl=document.getElementById('imp'),freqSl=document.getElementById('freq'),impV=document.getElementById('impv'),freqV=document.getElementById('freqv');
var chSel=document.getElementById('chsel'),search=document.getElementById('search'),counter=document.getElementById('counter');
var state={mode:'all',imp:1,freq:0,ch:'all',q:''};
function clampI(v,lo,hi){v=parseInt(v);return isNaN(v)?lo:Math.min(hi,Math.max(lo,v));}
try{var saved=JSON.parse(localStorage.getItem('prm_review_state')||'{}');if(saved.mode)state.mode=saved.mode;if(saved.imp!=null)state.imp=clampI(saved.imp,1,5);if(saved.freq!=null)state.freq=clampI(saved.freq,0,FMAX);if(saved.ch)state.ch=saved.ch;}catch(e){}
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
 try{localStorage.setItem('prm_review_state',JSON.stringify({mode:state.mode,imp:state.imp,freq:state.freq,ch:state.ch}));}catch(e){}
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
function setFilters(open){tb.classList.toggle('fclosed',!open);ftog.setAttribute('aria-expanded',open?'true':'false');try{localStorage.setItem('prm_filters_open',open?'1':'0');}catch(e){}}
(function(){var v=null;try{v=localStorage.getItem('prm_filters_open');}catch(e){}if(v===null)v=window.matchMedia('(max-width:760px)').matches?'0':'1';setFilters(v==='1');})();
ftog.addEventListener('click',function(){setFilters(tb.classList.contains('fclosed'));apply(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&window.matchMedia('(max-width:760px)').matches&&!tb.classList.contains('fclosed')){setFilters(false);apply(false);}});
var chOpen={};try{chOpen=JSON.parse(localStorage.getItem('prm_ch_open')||'{}');}catch(e){}
function saveCh(){try{localStorage.setItem('prm_ch_open',JSON.stringify(chOpen));}catch(e){}}
document.querySelectorAll('section.chapter').forEach(function(s){var id=s.id,d=s.querySelector('details.chd');if(chOpen[id]===false)d.open=false;
 d.addEventListener('toggle',function(){chOpen[id]=d.open;saveCh();});});
function setAll(sel,open){document.querySelectorAll(sel).forEach(function(d){d.open=open;});}
document.getElementById('foldch').addEventListener('click',function(){setAll('details.chd',false);});
document.getElementById('opench').addEventListener('click',function(){setAll('details.chd',true);});
document.getElementById('foldsec').addEventListener('click',function(){setAll('details.secd',false);});
document.getElementById('opensec').addEventListener('click',function(){setAll('details.secd',true);});
window.addEventListener('hashchange',function(){var el=document.getElementById(location.hash.slice(1));if(el){var p=el;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}el.scrollIntoView();}});
var theme=document.getElementById('theme');
function setTheme(v){if(v)root.setAttribute('data-theme',v);else root.removeAttribute('data-theme');try{localStorage.setItem('prm_theme',v||'');}catch(e){}theme.textContent=v==='dark'?'☀ فاتح':v==='light'?'🌙 داكن':'◐ المظهر';}
try{setTheme(localStorage.getItem('prm_theme')||'');}catch(e){}
theme.addEventListener('click',function(){var cur=root.getAttribute('data-theme');var dark=cur?cur==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;setTheme(dark?'light':'dark');});
window.addEventListener('beforeprint',function(){document.querySelectorAll('details').forEach(function(d){d.open=true;});});
document.querySelectorAll('#toc a').forEach(function(a){a.addEventListener('click',function(){var el=document.getElementById(a.getAttribute('href').slice(1));if(el){el.querySelectorAll('details.chd').forEach(function(d){d.open=true;});}});});
apply(false);
})();
"""

def build():
    c = counts(); total = len(QS); FMAX = max(q['freq'] for q in QS); cov_total = QA.get('subs_covered_total', sum(len(v) for v in SUBS.values()))
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
      '<div class="grp jsonly"><button class="chip" id="expand">إظهار الإجابات</button><button class="chip" id="collapse">إخفاء الإجابات</button><button class="chip" id="foldch">طيّ كل الفصول</button><button class="chip" id="opench">فتح كل الفصول</button><button class="chip" id="foldsec">طيّ الأنواع</button><button class="chip" id="opensec">فتح الأنواع</button><button class="chip" id="theme">◐ المظهر</button><button class="chip" id="reset">↺ إعادة ضبط التصفية</button></div>'
      '</div></div>',
      f'''<section id="howto"><h2>كيف تستخدم هذا الملف</h2>
<p>كل سؤال يحمل ثلاث علامات: <b>التكرار</b> = عدد المصادر المستقلة التي سألته (ست دورات امتحانية منقولة من الذاكرة: نحو 2015 والدورة التالية لها و2016 وS19 وF24 ومجموعة أسئلة الفحص المتداولة، ثم الكتاب والملخصات)؛ <b>الأهمية ★</b> من 1 إلى 5 مبنية على عدد امتحانات ورد فيها السؤال، زائد نقطة إن كان من أسئلة الكتاب، زائد نقطة إن كانت فقرته من مجالات تركيز المدرّس، وهي معونة للدراسة لا توقّع للامتحان؛ <b>⚠ ثقة منخفضة</b> يظهر فقط حيث يستند الجواب إلى دليل ضعيف أو نقل غير مؤكد، وغيابه يعني أن الإجابة تُحقق منها من الكتاب بالصفحة.</p>
<p>الإجابة مخفية خلف زر «إظهار الإجابة» ولا تحتاج جافاسكربت. الشريط الثابت في الأعلى يعرض العدّاد وزر «⚙ الفلاتر» والبحث؛ وخلف زر الفلاتر: وضع القراءة (نوع واحد من الأسئلة عبر كل الفصول: الامتحانات، الكتاب، مصادر أخرى، مولَّدة)، ومنزلقان لحدّ أدنى للأهمية (1–5) وللتكرار، واختيار فصل، وإظهار الإجابات أو إخفائها، وطيّ كل الفصول أو فتحها، وطيّ أنواع الأسئلة أو فتحها، مستقلةً عن حالة الإجابات (ويمكن طيّ أي فصل أو نوع منفرداً بالنقر على عنوانه، ويُحفظ ما طويته)، والمظهر الفاتح أو الداكن، وزر «إعادة ضبط التصفية». اختياراتك تُحفظ وتوضع في رابط الصفحة. على الهاتف تبدأ لوحة الفلاتر مطوية، وحين تكون مطوية وثمة تصفية فعّالة يظهر عددها على الزر وملخصها بجانب العدّاد. تنبيه: الأسئلة المولَّدة أهميتها 1 دائماً، فرفع منزلق الأهمية إلى 2 أو أكثر يخفيها كلها. الترتيب المقترح: أسئلة الامتحانات أولاً ثم أسئلة الكتاب ثم الباقي. الطباعة تُظهر كل الإجابات وتتجاهل التصفية.</p>
<p class="meta">إخفاء الإجابات معونة للمذاكرة وليس حمايةً: نص الإجابة موجود في الملف ويصل إليه البحث والنسخ وعرض المصدر، فلا يُعتمد عليه في امتحان حقيقي. نصوص الكتاب والامتحانات المقتبسة تبقى ملكاً لأصحابها.</p>
<p class="pledge">شروط رخصة هذا الملف (CC BY-NC-SA 4.0): شارك هذا الملف مجاناً مع زملائك في المادة. أبقِ الإشعار الموجود في آخر الملف حتى يجد غيرك المصدر وأحدث إصدار. لا يجوز بيعه ولا وضعه خلف اشتراك أو جدار دفع.</p></section>''',
      f'''<section id="scope"><h2>النطاق والمصادر</h2>
<p>المرجع الحاكم هو كتاب المقرر ({esc(BOOK_FILE)}، {BOOK_PAGES} صفحة، 14 فصلاً). النطاق: الفصول {CHAPTER_LIST_AR} ({total_subs} فقرة). أُدرجت أسئلة ست دورات امتحانية منقولة من الذاكرة (دورة نحو 2015 والدورة التالية لها، ودورة 2016، ودورة S19 بتاريخ 2020-02-04، ودورة F24، ومجموعة «الأسئلة التي تأتي في الفحص»)، وأسئلة مراجعة الكتاب في نهاية كل فصل بإجاباته المظلَّلة، وأسئلة ملخص عماد جبور ومجموعة أسئلة المراجعة التي يوجد مفهومها في الكتاب، مع تحقق متقاطع من ملخص عاصم. استُبعدت الملفات التي لا تحوي أسئلة أو تخص مقرراً آخر. التفاصيل في قسم المنهجية.</p>
<table class="tbl"><thead><tr><th>القسم</th><th>العدد</th><th>ما هو</th></tr></thead><tbody>
<tr><td>أسئلة الامتحانات</td><td>{c["exam"]}</td><td>{esc(SEC_INTRO["exam"])}</td></tr>
<tr><td>أسئلة الكتاب</td><td>{c["textbook"]}</td><td>{esc(SEC_INTRO["textbook"])}</td></tr>
<tr><td>مصادر أخرى</td><td>{c["other"]}</td><td>{esc(SEC_INTRO["other"])}</td></tr>
<tr><td>مولَّدة</td><td>{gen}</td><td>{esc(SEC_INTRO["generated"])}</td></tr></tbody></table>
<p class="meta">سؤال واحد قد يكون من الامتحانات ومن الكتاب معاً فيُحسب في القسمين ويظهر في وضعَي القراءة، لكنه يُعرض مرة واحدة (في قسم الامتحانات) مع وسم النوعين.</p></section>''']
    for n in CHAPTERS: parts.append(render_chapter(n))
    parts.append(methodology()); parts.append(sources_appendix()); parts.append(ref_lists()); parts.append(toc())
    parts.append(f'<footer id="metadata"><h2>بيانات الملف</h2><p>{esc(TITLE)} · ملف المراجعة الإصدار v{esc(VER)} (Review file v{esc(VER)}) · أُنشئ من المواصفة {esc(SPEC)} (Generated from prompt {esc(SPEC)}) · تاريخ الإنشاء {TODAY} · ملف البنك المرافق: bank.json في مجلد العمل بالمستودع · {total} سؤالاً في 14 فصلاً · {cov_total} فقرة مغطاة من {total_subs}. لا يحوي الملف بيانات شخصية. ملف HTML واحد مستقل بلا موارد خارجية.</p>'
                 f'<div class="notice"><p>أُنشئ بأداة SVU MBA Course Review Generator، المواصفة {esc(SPEC)} · ملف المراجعة v{esc(VER)}</p>'
                 f'<p>المصدر وأحدث إصدار: <a href="{REPO}" class="ltr">{REPO}</a></p>'
                 f'<p>رخصة الأداة وهذا الملف: <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ar" class="ltr">CC BY-NC-SA 4.0</a> — شارك بحرية، وانسب المصدر، ولا تبع أبداً. الرخصة تغطي محتوى المراجعة نفسها (الشروح والاختيار والترتيب)، أما نصوص الكتاب والامتحانات المقتبسة فتبقى لأصحابها وليست مشمولة.</p></div></footer>')
    parts.append('</main>'); parts.append(f'<script>{JS}</script>')
    return "\n".join(parts)

if __name__ == "__main__":
    out = build()
    dst = os.path.join(HERE, "..", "out.html")
    with open(dst, "w", encoding="utf-8", newline="\n") as f: f.write(out)
    print("written", dst, len(out.encode("utf-8"))//1024, "KB")
