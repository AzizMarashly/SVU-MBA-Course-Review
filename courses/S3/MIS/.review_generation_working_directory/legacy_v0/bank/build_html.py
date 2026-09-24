# -*- coding: utf-8 -*-
"""Build a single self-contained HTML review file.

The reveal mechanism is <details>/<summary> — native HTML, no JavaScript, no plugin.
It works in every browser on every device (phone, tablet, desktop), offline, from a
local file. JavaScript is used ONLY for the optional extras (search, expand-all,
chapter filter); with JS disabled every question still opens and closes normally.
"""
import html, os, re
import bank_a, bank_b, bank_c, bank_d, bank_e
from bank_a import Q, CH
from build_docx import (CHAPTERS, TITLE, QTYPE_AR, SRC_AR, GRP_LABEL, GRP_ORDER,
                        TYPE_LABEL, grp_of, sort_key)
from meta_mis import FILES, SRC_ROW, REPO, SPEC, GENERATED, RENDERED, DUPLICATES_REMOVED

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(HERE, '..', 'VERSION'), encoding='utf-8').read().strip()


def esc(t):
    return html.escape(t, quote=False)


def md(t):
    """**bold** -> <strong>, after escaping."""
    out, parts = [], re.split(r'\*\*', esc(t))
    for i, chunk in enumerate(parts):
        if not chunk:
            continue
        out.append('<strong>%s</strong>' % chunk if i % 2 else chunk)
    return ''.join(out)


CSS = """
:root{
  --bg:#f6f7f9; --card:#fff; --ink:#1a1a1a; --muted:#8a8f98; --line:#e3e6ea;
  --blue:#0b4f8a; --green:#1e7a33; --red:#a31d1d; --greenbg:#eaf6ee; --greenline:#bfe0c9;
  --shadow:0 1px 2px rgba(16,24,40,.05),0 1px 3px rgba(16,24,40,.06);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#14161a; --card:#1c1f25; --ink:#e8eaed; --muted:#8b929c; --line:#2b2f37;
  --blue:#7fb3e0; --green:#6ec98a; --red:#e88b8b; --greenbg:#1b2a20; --greenline:#2f5138;
  --shadow:none;
}}
:root[data-theme="dark"]{
  --bg:#14161a; --card:#1c1f25; --ink:#e8eaed; --muted:#8b929c; --line:#2b2f37;
  --blue:#7fb3e0; --green:#6ec98a; --red:#e88b8b; --greenbg:#1b2a20; --greenline:#2f5138;
  --shadow:none;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font-family:"Segoe UI","Noto Naskh Arabic",Tahoma,Arial,sans-serif;
 font-size:16px;line-height:1.75;direction:rtl;text-align:right;
 -webkit-text-size-adjust:100%}
.wrap{max-width:900px;margin:0 auto;padding:0 16px 80px}
header.top{background:var(--card);border-bottom:1px solid var(--line);
 position:sticky;top:0;z-index:20;box-shadow:var(--shadow)}
header.top .inner{max-width:900px;margin:0 auto;padding:10px 16px}
h1{font-size:1.25rem;margin:0 0 2px;color:var(--blue);font-weight:700}
.sub{color:var(--muted);font-size:.8rem;margin:0}
.tools{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;align-items:center}
input[type=search],select,button{font:inherit;font-size:.85rem;color:var(--ink);
 background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:7px 10px}
input[type=search]{flex:1 1 190px;min-width:0}
button{cursor:pointer}
button:hover{border-color:var(--muted)}
.hero{background:var(--card);border:1px solid var(--line);border-radius:14px;
 padding:22px;margin:22px 0;box-shadow:var(--shadow)}
.hero h2{margin:0 0 8px;font-size:1.5rem;color:var(--blue)}
.note{color:var(--muted);font-size:.85rem}
h2.ch{font-size:1.15rem;color:var(--blue);margin:34px 0 4px;
 padding-bottom:8px;border-bottom:2px solid var(--line);scroll-margin-top:120px}
.chmeta{color:var(--muted);font-size:.78rem;margin:0 0 12px}
h3.sec{font-size:.95rem;margin:26px 0 6px;padding:7px 12px;border-radius:8px;
 background:var(--card);border:1px solid var(--line);scroll-margin-top:120px}
h3.sec.s0{color:var(--red)} h3.sec.s1{color:var(--blue)}
h3.sec.s2,h3.sec.s3{color:var(--muted)}
.secnote{color:var(--muted);font-size:.8rem;margin:0 0 4px;padding:0 4px}
.q{background:var(--card);border:1px solid var(--line);border-radius:12px;
 padding:14px 16px;margin:10px 0;box-shadow:var(--shadow)}
.qhead{font-weight:600;font-size:1.02rem;margin:0}
.qhead .n{color:var(--muted);font-weight:600;margin-left:6px}
.meta{color:var(--muted);font-size:.72rem;margin:5px 0 0;letter-spacing:.1px}
ol.opts{margin:10px 0 0;padding:0 22px 0 0;list-style:arabic-indic}
ol.opts li{margin:3px 0}
ol.opts li.ltr{direction:ltr;text-align:left}
details{margin-top:12px}
summary{cursor:pointer;list-style:none;display:inline-flex;align-items:center;gap:7px;
 color:var(--green);background:var(--greenbg);border:1px solid var(--greenline);
 border-radius:8px;padding:6px 13px;font-size:.85rem;font-weight:600;
 user-select:none;-webkit-user-select:none}
summary::-webkit-details-marker{display:none}
summary::marker{content:""}
summary:hover{filter:brightness(.97)}
summary .tri{transition:transform .15s}
details[open] summary .tri{transform:rotate(-90deg)}
details[open] summary{color:var(--red);background:transparent;border-color:var(--line)}
.lbl-h{display:none}
details[open] .lbl-s{display:none}
details[open] .lbl-h{display:inline}
.ansbox{border-right:3px solid var(--greenline);padding:2px 13px;margin-top:10px}
.ans{margin:0 0 7px}.ans b{color:var(--green)}
.alt{margin:0 0 7px;color:var(--red);font-size:.9rem}
.exp{margin:0 0 7px;font-size:.94rem}.exp b.l{color:var(--blue)}
.ref{margin:0;color:var(--muted);font-size:.75rem}
.top-list{background:var(--card);border:1px solid var(--line);border-radius:12px;
 padding:14px 16px;box-shadow:var(--shadow)}
.freq{color:var(--red);font-weight:700;margin:16px 0 6px;font-size:.9rem}
.freq:first-child{margin-top:0}
.top-list p{margin:3px 0;font-size:.9rem}
.top-list .tag{color:var(--muted);font-size:.75rem;margin-left:6px}
table.meta-t{width:100%;border-collapse:collapse;font-size:.85rem;margin-top:10px}
table.meta-t td{border:1px solid var(--line);padding:7px 10px}
table.meta-t td:last-child{color:var(--muted);width:42%}
.method-box{background:var(--card);border:1px solid var(--line);border-radius:12px;
 padding:14px 16px;box-shadow:var(--shadow)}
.method-box h4{margin:16px 0 3px;font-size:.95rem}
.method-box h4:first-child{margin-top:0}
.method-box p{margin:0;font-size:.9rem;color:var(--ink)}
nav.chips{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 0}
nav.chips a{font-size:.8rem;text-decoration:none;color:var(--blue);background:var(--card);
 border:1px solid var(--line);border-radius:999px;padding:4px 11px}
nav.chips a:hover{border-color:var(--blue)}
.hidden{display:none!important}
.count{color:var(--muted);font-size:.78rem;margin:10px 0 0}
footer{color:var(--muted);font-size:.78rem;text-align:center;margin-top:40px}
.pledge{color:var(--ink);font-size:.85rem;margin:8px 0 0;padding:8px 12px;border-radius:8px;
 background:var(--greenbg);border:1px solid var(--greenline)}
.srcref{color:var(--muted);text-decoration:none;font-size:.7rem;margin-right:2px}
.srcref:hover{color:var(--blue)}
details.reflist{margin:10px 0 0}
details.reflist summary{background:var(--card);color:var(--ink);border-color:var(--line)}
details.reflist[open] summary{color:var(--ink)}
table.files{width:100%;border-collapse:collapse;font-size:.78rem;margin-top:10px}
table.files th,table.files td{border:1px solid var(--line);padding:5px 7px;vertical-align:top}
table.files th{background:var(--bg);font-weight:600}
table.files td.fn{direction:ltr;text-align:left;font-family:Consolas,monospace;font-size:.72rem;word-break:break-all}
table.files td.ltr{direction:ltr;text-align:left}
.files-wrap{overflow-x:auto}
.notice{margin-top:14px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;
 background:var(--card);text-align:right;line-height:1.6}
.notice p{margin:3px 0}
.notice a{color:var(--blue)}
.ltr{direction:ltr;unicode-bidi:embed}
mark{background:#ffe98a;color:#1a1a1a;border-radius:3px}
@media print{
  header.top,.tools,nav.chips,.hero .note{display:none}
  details{display:block}
  details>summary{display:none}
  .method-box{break-inside:avoid}
  .q{break-inside:avoid;box-shadow:none;border-color:#ccc}
  body{background:#fff;font-size:11pt}
}
"""

JS = """
(function(){
  try{
    var q=document.getElementById('q'), fc=document.getElementById('fc'),
        cnt=document.getElementById('cnt'), cards=[].slice.call(document.querySelectorAll('.q'));
    function norm(s){return (s||'').replace(/[\\u064b-\\u0652\\u0640]/g,'')
      .replace(/[\\u0623\\u0625\\u0622]/g,'\\u0627').replace(/\\u0629/g,'\\u0647')
      .replace(/\\u0649/g,'\\u064a').toLowerCase();}
    cards.forEach(function(c){c.dataset.k=norm(c.textContent);});
    function apply(){
      var t=norm(q.value.trim()), ch=fc.value, n=0;
      cards.forEach(function(c){
        var ok=(!t||c.dataset.k.indexOf(t)>-1)&&(ch==='all'||c.dataset.ch===ch);
        c.classList.toggle('hidden',!ok); if(ok)n++;
      });
      document.querySelectorAll('h2.ch,h3.sec,.secnote').forEach(function(h){
        var g=h.dataset.grp||h.dataset.ch;
        if(ch!=='all'&&h.dataset.ch&&h.dataset.ch!==ch){h.classList.add('hidden');return;}
        h.classList.remove('hidden');
      });
      document.querySelectorAll('h3.sec,.secnote').forEach(function(h){
        if(h.classList.contains('hidden'))return;
        var el=h.nextElementSibling,any=false;
        while(el&&!el.matches('h2.ch,h3.sec')){
          if(el.classList.contains('q')&&!el.classList.contains('hidden'))any=true;
          el=el.nextElementSibling;}
        h.classList.toggle('hidden',!any);});
      document.querySelectorAll('h2.ch[data-ch]').forEach(function(h){
        var el=h.nextElementSibling,any=false,meta=null;
        while(el&&!el.matches('h2.ch')){
          if(el.classList.contains('chmeta'))meta=el;
          if(el.classList.contains('q')&&!el.classList.contains('hidden'))any=true;
          el=el.nextElementSibling;}
        h.classList.toggle('hidden',!any);
        if(meta)meta.classList.toggle('hidden',!any);});
      var filtering=!!t||ch!=='all';
      ['top','topmeta','toplist'].forEach(function(id){
        var e=document.getElementById(id); if(e)e.classList.toggle('hidden',filtering);});
      cnt.textContent='المعروض الآن: '+n+' سؤال من أصل '+cards.length;
    }
    q.addEventListener('input',apply); fc.addEventListener('change',apply); apply();
    document.getElementById('ex').addEventListener('click',function(){
      document.querySelectorAll('.q:not(.hidden) details').forEach(function(d){d.open=true;});});
    document.getElementById('co').addEventListener('click',function(){
      document.querySelectorAll('details').forEach(function(d){d.open=false;});});
    var th=document.getElementById('th');
    th.addEventListener('click',function(){
      var r=document.documentElement,
          dark=r.getAttribute('data-theme')==='dark'||
               (!r.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme:dark)').matches);
      r.setAttribute('data-theme',dark?'light':'dark');});
  }catch(e){}
})();
"""


def build():
    parts = []
    A = parts.append
    A('<!doctype html>')
    A('<html lang="ar" dir="rtl"><head><meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width,initial-scale=1">')
    A('<title>%s</title>' % esc(TITLE))
    A('<style>%s</style>' % CSS)
    A('</head><body>')

    # ---------------- sticky header ----------------
    A('<header class="top"><div class="inner">')
    A('<h1>%s</h1>' % esc(TITLE))
    A('<p class="sub">نظم المعلومات الإدارية — الفصول 1، 2، 3، 5، 7، 8، 9، 10</p>')
    A('<div class="tools">')
    A('<input type="search" id="q" placeholder="ابحث في الأسئلة والإجابات…" aria-label="بحث">')
    A('<select id="fc" aria-label="تصفية حسب الفصل"><option value="all">كل الفصول</option>')
    for ch in CHAPTERS:
        A('<option value="%d">الفصل %d</option>' % (ch, ch))
    A('</select>')
    A('<button id="ex" type="button">إظهار الكل</button>')
    A('<button id="co" type="button">إخفاء الكل</button>')
    A('<button id="th" type="button">الوضع الليلي</button>')
    A('</div></div></header>')

    A('<div class="wrap">')

    # ---------------- hero / how to use ----------------
    A('<div class="hero">')
    A('<h2>مراجعة كاملة — %d سؤالاً</h2>' % len(Q))
    A('<p class="note">اضغط الزر الأخضر «إظهار الإجابة والشرح» أسفل أي سؤال لكشف إجابته، واضغطه ثانيةً لإخفائها. '
      'كل سؤال مستقل، والإجابات مخفية عند فتح الملف.</p>')
    A('<p class="note">تعمل هذه الطريقة في أي متصفح على الهاتف والحاسب دون برامج إضافية ودون اتصال بالإنترنت، '
      'ولا تحتاج إلى Adobe Acrobat ولا إلى Microsoft Word.</p>')
    A('<p class="note">للطباعة: استخدم أمر الطباعة في المتصفح، وستُطبع جميع الإجابات ظاهرة.</p>')
    A('<p class="note">ملاحظة خصوصية: الإخفاء وسيلة للمذاكرة لا حماية أمنية — نص الإجابات موجود داخل الملف '
      'ويمكن الوصول إليه بالبحث أو بعرض مصدر الصفحة.</p>')
    A('<p class="pledge">شروط رخصة هذا الملف (CC BY-NC-SA 4.0): شارك هذا الملف مجاناً مع زملائك في المادة. '
      'أبقِ الإشعار الموجود في آخر الملف حتى يجد غيرك المصدر وأحدث إصدار. '
      'لا يجوز بيعه ولا وضعه خلف اشتراك أو جدار دفع.</p>')
    A('<nav class="chips">')
    for ch in CHAPTERS:
        A('<a href="#ch%d">الفصل %d</a>' % (ch, ch))
    A('<a href="#top">الأكثر تكراراً</a><a href="#meth">المنهجية</a><a href="#sources">ملفات المصدر</a></nav>')
    A('<p class="count" id="cnt"></p>')
    A('</div>')

    # ---------------- most repeated ----------------
    A('<h2 class="ch" id="top">الأسئلة الأكثر تكراراً</h2>')
    A('<p class="chmeta" id="topmeta">وردت في ثلاثة مصادر مستقلة فأكثر. الإجابات غير معروضة هنا عمداً — راجعها في موضعها داخل الفصل.</p>')
    A('<div class="top-list" id="toplist">')
    top = sorted([x for x in Q if x['freq'] >= 3], key=lambda x: (-x['freq'], x['ch'], x['id']))
    cur = None
    for x in top:
        if x['freq'] != cur:
            cur = x['freq']
            A('<p class="freq">تكرار: %d مصادر مستقلة</p>' % cur)
        t = x['text'] if len(x['text']) <= 155 else x['text'][:152] + '…'
        A('<p><span class="tag">[ف%d · %s]</span>%s</p>' % (x['ch'], esc(x['id']), esc(t)))
    A('</div>')

    # ---------------- chapters ----------------
    qno = 0
    for ch in CHAPTERS:
        title, rng = CH[ch]
        items = sorted([x for x in Q if x['ch'] == ch], key=sort_key)
        A('<h2 class="ch" id="ch%d" data-ch="%d">%s</h2>' % (ch, ch, esc(title)))
        c = {g: sum(1 for x in items if grp_of(x) == g) for g in GRP_ORDER}
        A('<p class="chmeta" data-ch="%d">صفحات الفصل في الكتاب: %s &nbsp;|&nbsp; عدد الأسئلة: %d '
          '&nbsp;|&nbsp; دورات: %d &nbsp;·&nbsp; كتاب: %d &nbsp;·&nbsp; مصادر أخرى: %d &nbsp;·&nbsp; مولّدة: %d</p>'
          % (ch, rng, len(items), c['دورة'], c['كتاب'], c['أخرى'], c['مولّد']))

        flag = None
        for i, x in enumerate(items, 1):
            g = grp_of(x)
            if g != flag:
                flag = g
                A('<h3 class="sec s%d" id="ch%d-%d" data-ch="%d">%s</h3>'
                  % (GRP_ORDER[g], ch, GRP_ORDER[g], ch, esc(GRP_LABEL[g])))
                if g == 'أخرى':
                    A('<p class="secnote" data-ch="%d">أسئلة جُمعت من بقية ملفات المادة (ملخصات وأدلة مذاكرة '
                      'وتجميعات دورات قديمة)، وأُبقي منها ما يوجد مفهومه في كتاب المقرر الحالي، وأُعيد التحقق '
                      'من كل إجابة من نص الكتاب لا من مفاتيح تلك الملفات.</p>' % ch)
                elif g == 'مولّد':
                    A('<p class="secnote" data-ch="%d">هذه الأسئلة ليست منقولة من أي دورة أو ملف؛ صيغت خصيصاً '
                      'لتغطية أفكار واردة في كتاب المقرر لم يتناولها أي سؤال في المصادر المتاحة. كل إجابة هنا '
                      'مأخوذة من نص الكتاب مع رقم صفحة متحقَّق منه — فهي للفهم وسدّ النقص لا للتنبؤ '
                      'بالامتحان.</p>' % ch)
            qno += 1
            types_ar = ' + '.join(TYPE_LABEL.get(t, t) for t in x['types'])
            if x['freq'] == 0:
                meta = '%s · %s · لم ترد في أي مصدر — مولّد لتغطية فجوة · %s' % (
                    x['id'], QTYPE_AR[x['qtype']], types_ar)
            else:
                meta = '%s · %s · تكرار: %d من المصادر المستقلة · %s' % (
                    x['id'], QTYPE_AR[x['qtype']], x['freq'], types_ar)

            A('<article class="q" data-ch="%d">' % ch)
            A('<p class="qhead"><span class="n">س%d ·</span>%s</p>' % (i, esc(x['text'])))
            A('<p class="meta">%s</p>' % esc(meta))
            if x['opts']:
                A('<ol class="opts">')
                for o in x['opts']:
                    ltr = '' if re.search(r'[؀-ۿ]', o) else ' class="ltr"'
                    A('<li%s>%s</li>' % (ltr, esc(o)))
                A('</ol>')
            A('<details><summary><span class="tri">◂</span>'
              '<span class="lbl-s">إظهار الإجابة والشرح</span>'
              '<span class="lbl-h">إخفاء الإجابة والشرح</span></summary>')
            A('<div class="ansbox">')
            A('<p class="ans"><b>الإجابة الصحيحة:</b> <strong>%s</strong></p>' % md(x['ans']))
            if x.get('book_answer'):
                A('<p class="alt"><b>إجابة مغايرة وردت في مصدر آخر (للمقارنة فقط):</b> %s</p>'
                  % md(x['book_answer']))
            A('<p class="exp"><b class="l">الشرح:</b> %s</p>' % md(x['exp']))
            srcs = '، '.join(
                esc(SRC_AR[s]) + (' <a class="srcref" href="#src-%d" title="ملف المصدر رقم %d في ملحق ملفات المصدر">#%d</a>'
                                 % (SRC_ROW[s], SRC_ROW[s], SRC_ROW[s]) if s in SRC_ROW else '')
                for s in x['src'])
            A('<p class="ref">المرجع: الكتاب، الفصل %d، صفحة %s (الصفحة المطبوعة = صفحة PDF) · المصادر: %s</p>'
              % (x['ch'], x['page'], srcs))
            A('</div></details></article>')

    # ---------------- methodology ----------------
    A('<h2 class="ch" id="meth">المنهجية وحدود العمل</h2>')
    meth = [
        ('كيف بُنِي هذا الملف',
         'قُرئ كتاب المقرر كاملاً (507 صفحات) أولاً، ثم فُهرست حدود الفصول وتعاريفها ونماذجها وجداولها وأرقام صفحاتها. '
         'بعد ذلك استُخرجت الأسئلة من كل الملفات المرفقة، وصُنّفت، ووُحّدت المكرّرة، وتُحقّق من كل إجابة مقابل نص الكتاب.'),
        ('ترتيب الأقسام داخل كل فصل',
         'أسئلة الدورات أولاً، ثم أسئلة الكتاب، ثم أسئلة من مصادر أخرى (ملخصات وأدلة مذاكرة)، ثم الأسئلة المولّدة. '
         'ويُذكر مع كل سؤال نوعه أو أنواعه، فقد يكون السؤال «دورة» و«كتاب» معاً.'),
        ('تدقيق تغطية الأفكار',
         'قُسّم الكتاب إلى 101 فقرة فرعية ضمن الفصول الثمانية، وفُحصت كل فقرة لمعرفة ما إذا كان أي سؤال يتناولها فعلاً. '
         'كانت 69 فقرة مغطاة، و10 فقرات مذكورة في الشروح فقط، و22 فقرة لم يتناولها شيء. فصيغت 33 سؤالاً مولّداً '
         'وُضعت في قسم رابع مستقل، والتغطية الآن 101 من 101. ولم يحتج الفصل السابع إلى أي سؤال مولّد.'),
        ('عدّ التكرار',
         'عدّاد التكرار هو عدد المصادر المستقلة التي ورد فيها السؤال، لا عدد الملفات. والسؤال يُعدّ مرة واحدة في المصدر '
         'الواحد حتى لو تكرر داخله. والأسئلة المولّدة تكرارها صفر لأنها لم ترد في أي مصدر.'),
        ('المادة تتبع مقررين مختلفين',
         'أغلب ملفات الدورات المرفقة تعود إلى مقرر أقدم لنظم المعلومات الإدارية (يظهر اسم الدكتور سليمان عوض في أحد '
         'الملفات) يدور حول Solver ودرجة التقارب والجدول المحوري والمجموعة المتجانسة وإطار Hong — وهي موضوعات لا وجود '
         'لها في كتاب المقرر الحالي. فاستُبعدت إجاباتها، ولم يُؤخذ منها إلا ما يوجد مفهومه في الكتاب الحالي بعد إعادة '
         'التحقق منه.'),
        ('تعارضات مُبقاة ظاهرة',
         'حيثما اختلفت ورقة حلّ أو ملخص عن نص الكتاب، عُرضت الإجابتان معاً: إجابة الكتاب هي المعتمدة، والأخرى مذكورة '
         'بالأحمر للمقارنة. وهذا يشمل سؤال الموازنة السنوية في الفصل الثاني وسؤال ربط جداول النموذج العلائقي في الفصل الخامس.'),
        ('ما لم يُدرج',
         'لم تُدرج أسئلة الفصول 4 و6 و11 و12 لأنها خارج النطاق المطلوب، ولا الأسئلة التي تعذّر إسنادها إلى أحد الفصول '
         'الثمانية بثقة كافية، ولم تُخترع أي خيارات أو إجابات أو أرقام صفحات غير متحقَّق منها.'),
        ('إصدار المواصفة',
         'بُني بنك الأسئلة وتُحقق منه في %s قبل صدور المواصفة المرقّمة (إصدار %s)، ثم أُعيد تصيير هذا الملف في %s '
         'دون أي تغيير في الأسئلة أو الخيارات أو الإجابات أو الشروح أو أرقام الصفحات أو التكرار؛ ما أُضيف هو ملحق «ملفات المصدر» '
         'ورقم الملف عند كل سؤال في سطر المصادر، وشروط الرخصة في مقدمة الملف وإشعارها في آخره، وبيانات الإصدار. '
         'لم يُطبَّق عليه ما استُحدث في المواصفات اللاحقة (درجة الأهمية، مجالات التركيز، علامة الثقة المنخفضة).'
         % (GENERATED, VERSION, RENDERED)),
    ]
    A('<div class="method-box">')
    for h, b in meth:
        A('<h4>%s</h4><p>%s</p>' % (esc(h), esc(b)))
    A('</div>')

    # ---------------- source files appendix (§11d) ----------------
    A('<h2 class="ch" id="sources">ملفات المصدر</h2>')
    A('<p class="chmeta">كل ملف في مجلد المادة مذكور هنا، بما فيه المستبعد وغير المستخدم، ليعرف القارئ ممّ بُنيت المراجعة. '
      'رقم كل ملف هو الرقم الذي يظهر عند كل سؤال في سطر «المصادر». أسماء الملفات كما وردت؛ المادة نفسها غير منشورة مع المراجعة.</p>')
    used = sorted({n for n in SRC_ROW.values()})
    A('<p class="chmeta">%d ملفاً في المجلد · %d ملفات تحمل مصادر الأسئلة · %d نسخ مكررة أُزيلت عند حفظ المجلد في المستودع · '
      'رمز المجموعة هو رمز المصدر المستخدم في بنك الأسئلة.</p>' % (len(FILES), len(used), DUPLICATES_REMOVED))
    A('<details class="reflist"><summary><span class="tri">◂</span> جدول الملفات (%d)</summary><div class="files-wrap">' % len(FILES))
    A('<table class="files"><thead><tr><th>#</th><th>اسم الملف</th><th>النوع</th><th>الدور</th><th>مجموعة المصدر</th><th>الصفحات</th><th>ملاحظة</th></tr></thead><tbody>')
    for n, path, kind, role, grp, pages, note in FILES:
        A('<tr id="src-%d"><td>%d</td><td class="fn">%s</td><td>%s</td><td>%s</td><td class="ltr">%s</td><td>%s</td><td>%s</td></tr>'
          % (n, n, esc(path), esc(kind), esc(role), esc(grp), esc(pages), esc(note)))
    A('</tbody></table></div></details>')

    # ---------------- file metadata ----------------
    A('<h2 class="ch">بيانات الملف</h2>')
    counts = {ch: sum(1 for x in Q if x['ch'] == ch) for ch in CHAPTERS}
    rows = [('عنوان المراجعة', TITLE),
            ('المرجع الأساسي', 'كتاب مقرر نظم المعلومات الإدارية — الدكتور إياد زوكار'),
            ('الفصول المشمولة', '1, 2, 3, 5, 7, 8, 9, 10'),
            ('عدد الأسئلة الكلي', str(len(Q))),
            ('منها أسئلة مولّدة', str(sum(1 for x in Q if 'GEN' in x['src']))),
            ('عدد المصادر المستقلة', '10'),
            ('تغطية أقسام الكتاب', '101 من 101'),
            ('لغة الأسئلة', 'عربية / إنكليزية ممزوجة'),
            ('لغة الشرح', 'العربية'),
            ('إصدار ملف المراجعة', 'v%s (Review file v%s)' % (VERSION, VERSION)),
            ('المواصفة', '%s — بنك الأسئلة أُنشئ في %s، وأُعيد تصيير الملف في %s' % (SPEC, GENERATED, RENDERED)),
            ('المصدر وأحدث إصدار', REPO)]
    for ch in CHAPTERS:
        rows.append(('عدد أسئلة الفصل %d' % ch, str(counts[ch])))
    A('<table class="meta-t">')
    for k, v in rows:
        A('<tr><td>%s</td><td>%s</td></tr>' % (esc(k), esc(v)))
    A('</table>')
    A('<footer>لا يحتوي هذا الملف على أي بيانات شخصية عن جهاز المستخدم أو حسابه.'
      '<div class="notice"><p>أُنشئ بأداة SVU MBA Course Review Generator، المواصفة %s · ملف المراجعة v%s</p>'
      '<p>المصدر وأحدث إصدار: <a href="%s" class="ltr">%s</a></p>'
      '<p>رخصة الأداة وهذا الملف: <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ar" class="ltr">CC BY-NC-SA 4.0</a> '
      '— شارك بحرية، وانسب المصدر، ولا تبع أبداً. الرخصة تغطي محتوى المراجعة نفسها (الشروح والاختيار والترتيب)، '
      'أما نصوص الكتاب والامتحانات المقتبسة فتبقى لأصحابها وليست مشمولة.</p></div></footer>'
      % (esc(SPEC), esc(VERSION), REPO, REPO))
    A('</div>')
    A('<script>%s</script>' % JS)
    A('</body></html>')

    out = os.path.join(HERE, TITLE + '.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))
    print('saved:', out, os.path.getsize(out), 'bytes')
    print('questions rendered:', qno)
    return out


if __name__ == '__main__':
    build()
