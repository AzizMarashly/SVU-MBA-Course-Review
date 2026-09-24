# -*- coding: utf-8 -*-
"""Build the interactive DOCX review file."""
import re, os
import bank_a, bank_b, bank_c, bank_d, bank_e
from bank_a import Q, CH

N_ASM = bank_d.register_assem_summary()
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

AR_FONT = 'Arial'
LRM = '‎'; RLM = '‏'
GRAY = RGBColor(0x7F, 0x7F, 0x7F)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
GREEN = RGBColor(0x1E, 0x7A, 0x33)
BLUE = RGBColor(0x0B, 0x4F, 0x8A)
RED = RGBColor(0xA3, 0x1D, 0x1D)

CHAPTERS = [1, 2, 3, 5, 7, 8, 9, 10]
TITLE = 'مراجعه كامله لماده ال MIS'
# PLAIN=1 -> a flat, printable document: answers simply printed, no reveal control,
# no collapsible heading, no invisible anchors, no interactivity wording anywhere.
PLAIN = os.environ.get('MIS_PLAIN') == '1'

def is_rtl(t):
    return len(re.findall(r'[؀-ۿ]', t)) > 0

_PPR_SUCC = ('w:adjustRightInd', 'w:snapToGrid', 'w:spacing', 'w:ind', 'w:contextualSpacing',
             'w:mirrorIndents', 'w:suppressOverlap', 'w:jc', 'w:textDirection', 'w:textAlignment',
             'w:textboxTightWrap', 'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr',
             'w:sectPr', 'w:pPrChange')

def set_rtl(p, rtl=True):
    """w:bidi must precede w:jc/w:spacing/w:ind in the schema.
    In a bidi paragraph w:jc is LOGICAL: 'left' == start == visually right.
    Leaving w:jc unset gives start alignment, which is what we want for Arabic."""
    pPr = p._p.get_or_add_pPr()
    b = pPr.find(qn('w:bidi'))
    if b is None:
        b = OxmlElement('w:bidi')
        pPr.insert_element_before(b, *_PPR_SUCC)
    b.set(qn('w:val'), '1' if rtl else '0')
    p.alignment = None if rtl else WD_ALIGN_PARAGRAPH.LEFT

def set_collapsed(p):
    pPr = p._p.get_or_add_pPr()
    c = OxmlElement('w:collapsed'); c.set(qn('w:val'), 'true'); pPr.append(c)

def fmt(run, size=11, color=DARK, bold=False, italic=False, font=AR_FONT, rtl=None):
    """rtl=None -> auto: mark the run as complex-script/RTL when it contains Arabic.
    Without <w:rtl/> Word lays Arabic glyphs out left-to-right (reversed)."""
    run.font.size = Pt(size); run.font.color.rgb = color
    run.bold = bold; run.italic = italic; run.font.name = font
    rPr = run._r.get_or_add_rPr()
    rf = rPr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rPr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rf.set(qn(a), font)
    szcs = OxmlElement('w:szCs'); szcs.set(qn('w:val'), str(int(size * 2))); rPr.append(szcs)
    if bold:
        bcs = OxmlElement('w:bCs'); bcs.set(qn('w:val'), 'true'); rPr.append(bcs)
    if italic:
        ics = OxmlElement('w:iCs'); ics.set(qn('w:val'), 'true'); rPr.append(ics)
    if rtl is None:
        rtl = bool(re.search(r'[؀-ۿ]', run.text or ''))
    if rtl:
        e = OxmlElement('w:rtl'); e.set(qn('w:val'), 'true'); rPr.append(e)
    return run

def md_parts(text, base=None):
    """Split '**bold**' spans into separate runs (Word has no markdown)."""
    base = dict(base or {})
    out = []
    for i, chunk in enumerate(re.split(r'\*\*', text)):
        if not chunk:
            continue
        k = dict(base)
        if i % 2 == 1:
            k['bold'] = True
        out.append((chunk, k))
    return out or [(text, base)]

def para(doc, text='', style=None, size=11, color=DARK, bold=False, italic=False,
         rtl=None, space_before=0, space_after=4, indent=0, keep_next=False):
    p = doc.add_paragraph(style=style)
    if rtl is None: rtl = is_rtl(text) if text else True
    set_rtl(p, rtl)
    pf = p.paragraph_format
    pf.space_before = Pt(space_before); pf.space_after = Pt(space_after)
    pf.line_spacing = 1.18
    if indent:
        pf.left_indent = Cm(indent)   # logical 'start' side: right for RTL, left for LTR
    if keep_next: pf.keep_with_next = True
    if text:
        fmt(p.add_run(text), size, color, bold, italic)
    return p

def rich(doc, parts, rtl=True, size=11, space_before=0, space_after=4, indent=0, keep_next=False):
    """parts = [(text, dict-of-fmt-kwargs), ...]"""
    p = doc.add_paragraph()
    set_rtl(p, rtl)
    pf = p.paragraph_format
    pf.space_before = Pt(space_before); pf.space_after = Pt(space_after); pf.line_spacing = 1.18
    if indent:
        pf.left_indent = Cm(indent)   # logical 'start' side: right for RTL, left for LTR
    if keep_next: pf.keep_with_next = True
    for t, kw in parts:
        k = dict(size=size); k.update(kw)
        fmt(p.add_run(t), **k)
    return p

def heading(doc, text, level, size, color, bold=True, rtl=True, collapsed=False,
            space_before=10, space_after=6, keep_next=True):
    p = doc.add_paragraph(style='Heading %d' % level)
    set_rtl(p, rtl)
    pf = p.paragraph_format
    pf.space_before = Pt(space_before); pf.space_after = Pt(space_after)
    pf.keep_with_next = keep_next; pf.line_spacing = 1.15
    fmt(p.add_run(text), size, color, bold)
    if collapsed: set_collapsed(p)
    return p

def hr(doc):
    p = doc.add_paragraph(); set_rtl(p, True)
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(6)
    pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '4')
    b.set(qn('w:space'), '1'); b.set(qn('w:color'), 'D9D9D9')
    pbdr.append(b); pPr.append(pbdr)

AR_NUM = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
QTYPE_AR = {'MCQ': 'اختيار من متعدد', 'TF': 'صح / خطأ', 'ESSAY': 'سؤال مقالي', 'DEF': 'تعريف / سؤال مباشر'}
SRC_AR = {'BKQ': 'أسئلة الكتاب', 'S25': 'دورة S25', 'HD': 'مجموعة «حل دورات»',
          'F24': 'دورة F24', 'R44': 'دورة الـ44 سؤالاً', 'ASM': 'ملخص عاصم 2022',
          'OQ1': 'مجموعة أسئلة الدورات المجمعة', 'OQ2': 'ملف أسئلة مقرر نظم المعلومات وحلّه',
          'OQ3': 'تجميع MIS Q', 'OQ4': 'مفتاح إجابات دورة مصوّرة',
          'OQ5': 'ملاحظات المقرر وأسئلة امتحان 2019', 'GEN': 'سؤال مولّد لتغطية فجوة'}
GRP_ORDER = {'دورة': 0, 'كتاب': 1, 'أخرى': 2, 'مولّد': 3}
GRP_LABEL = {'دورة': 'أولاً: أسئلة الدورات', 'كتاب': 'ثانياً: أسئلة الكتاب',
             'أخرى': 'ثالثاً: أسئلة من مصادر أخرى (ملخصات وأدلة مذاكرة)',
             'مولّد': 'رابعاً: أسئلة مولّدة لتغطية أفكار لم تتناولها المصادر'}
GRP_COLOR = {'دورة': RED, 'كتاب': BLUE, 'أخرى': GRAY, 'مولّد': GRAY}
TYPE_LABEL = {'دورة': 'سؤال دورة', 'كتاب': 'سؤال كتاب', 'أخرى': 'سؤال من مصدر آخر',
              'مولّد': 'سؤال مولّد'}

def grp_of(x):
    for t in ('دورة', 'كتاب', 'أخرى'):
        if t in x['types']:
            return t
    return 'مولّد'

def sort_key(x):
    return (GRP_ORDER[grp_of(x)], -x['freq'],
            {'MCQ': 0, 'TF': 1, 'DEF': 2, 'ESSAY': 3}[x['qtype']], x['id'])

def build():
    doc = Document()
    st = doc.styles['Normal']
    st.font.name = AR_FONT; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn('w:cs'), AR_FONT)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.0)
        s.top_margin = Cm(1.8); s.bottom_margin = Cm(1.8)

    # ---------------- COVER (kept deliberately simple) ----------------
    for _ in range(5): para(doc, '', space_after=0)
    rich(doc, [(TITLE, dict(size=30, bold=True, color=BLUE))], space_after=10)
    rich(doc, [('نظم المعلومات الإدارية — Management Information Systems', dict(size=14, color=DARK))], space_after=6)
    rich(doc, [('الفصول المشمولة: ', dict(size=12, color=GRAY)),
               (LRM + '1, 2, 3, 5, 7, 8, 9, 10' + LRM, dict(size=12, color=DARK, bold=True))], space_after=4)
    rich(doc, [('المرجع الأساسي: كتاب المقرر للدكتور إياد زوكار', dict(size=12, color=GRAY))], space_after=30)
    if PLAIN:
        rich(doc, [('نسخة للقراءة والطباعة — الإجابة والشرح مطبوعان أسفل كل سؤال', dict(size=11, color=GRAY, italic=True))])
    else:
        rich(doc, [('ملف مراجعة تفاعلي — اضغط «إظهار الإجابة والشرح» لكشف كل إجابة على حدة', dict(size=11, color=GRAY, italic=True))])
    doc.add_page_break()

    # ---------------- HOW TO USE ----------------
    heading(doc, 'كيف تستخدم هذا الملف', 1, 17, BLUE, space_before=0)
    if PLAIN:
        para(doc, 'هذه نسخة مرتّبة للقراءة والطباعة. كل سؤال مستقل بذاته، وتحته مباشرةً إجابته الصحيحة ثم شرحها ثم مرجعها في كتاب المقرر.', size=11)
        para(doc, 'يُذكر مع كل سؤال رقمه ونوعه وعدد المصادر المستقلة التي ورد فيها، وذلك بخط رمادي خفيف حتى يبقى التركيز على نص السؤال.', size=11)
        para(doc, 'ترتيب كل فصل: أسئلة الدورات أولاً، ثم أسئلة الكتاب، ثم أسئلة من مصادر أخرى، ثم الأسئلة المولّدة لتغطية ما لم تتناوله المصادر.', size=11)
        para(doc, 'ويوجد في نهاية الملف فهرس للمحتويات وجدول ببيانات الملف وإحصاءاته.', size=11)
    else:
        para(doc, 'كل سؤال في هذا الملف مستقل بذاته، ويوجد أسفله عنوان أخضر بعنوان «إظهار الإجابة والشرح».', size=11)
    if not PLAIN:
        para(doc, 'في نسخة Word لسطح المكتب: مرّر المؤشر على العنوان الأخضر فيظهر مثلث صغير بجانبه — اضغطه لطيّ الإجابة أو إظهارها. وطيّ إجابة واحدة لا يؤثر إطلاقاً على السؤال التالي.', size=11)
    if not PLAIN:
        para(doc, 'ولإخفاء كل الإجابات دفعةً واحدة: انقر بالزر الأيمن على أي عنوان أخضر ثم اختر «توسيع/طي» ثم «طي كل العناوين».', size=11)
    if not PLAIN:
        para(doc, 'في نسخة PDF التفاعلية: اضغط الزر الأخضر «إظهار الإجابة والشرح» لكشف الإجابة، ثم الزر الأحمر «إخفاء الإجابة والشرح» لإخفائها من جديد.', size=11)
    if not PLAIN:
        para(doc, 'ملاحظة توافقية مهمة: لا يحفظ Microsoft Word حالة الطيّ داخل ملف DOCX — فهي حالة عرض مؤقتة تخص الجلسة الحالية فقط. لذلك يُفتح الملف والإجابات ظاهرة في كل مرة، وتحتاج إلى طيّها مرة واحدة بالأمر المذكور أعلاه. أما نسخة PDF التفاعلية فتُفتح والإجابات مخفية تلقائياً دون أي إجراء منك.', size=10, color=GRAY)
    if not PLAIN:
        para(doc, 'كما أن خاصية الطيّ والتوسيع مصممة لبرنامج Microsoft Word لسطح المكتب، وقد تختلف أو لا تعمل في Word للويب أو في برامج معالجة نصوص أخرى (مثل Google Docs أو LibreOffice). وفي هذه الحالة تظهر الإجابات مكشوفة، ويبقى الملف قابلاً للقراءة والتحرير بالكامل.', size=10, color=GRAY)
    if not PLAIN:
        para(doc, 'ملاحظة خصوصية: إخفاء الإجابات هو وسيلة للمذاكرة فقط وليس حماية أمنية. نص الإجابات موجود داخل الملف، ويمكن الوصول إليه عن طريق البحث أو النسخ أو أدوات إتاحة الوصول أو فحص بنية الملف. لا تعتمد عليه في تسليم امتحان حقيقي.', size=10, color=GRAY)

    # ---------------- SCOPE ----------------
    heading(doc, 'نطاق المراجعة ومصادرها', 1, 17, BLUE)
    para(doc, 'يغطي هذا الملف الفصول 1 و2 و3 و5 و7 و8 و9 و10 فقط، وقد استُبعدت الفصول 4 و6 و11 و12 من نطاق المراجعة.', size=11)
    para(doc, 'وقد جرى تدقيق التغطية: قُسّم كتاب المقرر إلى 101 فقرة فرعية ضمن الفصول الثمانية، وفُحص لكل فقرة ما إذا كان أي سؤال في المصادر يتناولها فعلاً. تبيّن أن 32 فقرة لم يتناولها أي سؤال، فصيغت لها أسئلة مولّدة وُضعت في قسم رابع منفصل ومميّز داخل كل فصل.', size=11)
    para(doc, 'المرجع المعتمد في التحقق من كل إجابة هو كتاب المقرر نفسه. وفي هذا الكتاب رقم الصفحة المطبوعة يطابق رقم صفحة ملف PDF، لذلك يُذكر رقم واحد في المراجع.', size=11)

    stats = [
        ('عدد الأسئلة النهائية بعد التوحيد', str(len(Q))),
        ('عدد المصادر المستقلة داخل النطاق', '10'),
        ('عدد الملفات المستبعدة كنسخ مكررة', '6'),
        ('عدد ملفات المادة التي فُحصت', '45'),
        ('عدد الصور التي فُحصت بصرياً', '12 (7 فريدة)'),
        ('أقسام كتاب المقرر التي دُقّقت تغطيتها', '101'),
        ('عدد الأسئلة المولّدة لسدّ الفجوات', '33'),
    ]
    t = doc.add_table(rows=0, cols=2); t.style = 'Light Grid Accent 1'
    for k, v in stats:
        row = t.add_row().cells
        p0 = row[0].paragraphs[0]; set_rtl(p0, True); fmt(p0.add_run(k), 10.5)
        p1 = row[1].paragraphs[0]; set_rtl(p1, True); fmt(p1.add_run(LRM + v + LRM), 10.5, DARK, True)
    para(doc, '', space_after=6)

    para(doc, 'المصادر المستقلة المعتمدة داخل النطاق:', size=11.5, bold=True, space_before=6)
    srcdesc = [
        ('أسئلة الكتاب', 'أسئلة نهاية الفصول الواردة في كتاب المقرر (صح/خطأ، اختيار من متعدد، أسئلة للمناقشة).'),
        ('دورة S25', 'أسئلة دورة استُذكرت فصلاً بعد فصل.'),
        ('مجموعة «حل دورات»', 'مجموعة موحّدة من أسئلة دورات سابقة مع إجاباتها.'),
        ('دورة F24', 'دورة الفصل F24 — مركز خارجي، ستون سؤالاً.'),
        ('دورة الـ44 سؤالاً', 'استذكار لدورة جاءت بأربعة وأربعين سؤالاً.'),
        ('ملخص عاصم 2022', 'ملخص للمقرر يعيد إيراد أسئلة نهاية الفصول كاملةً مع إجاباتها المحلولة، فصلاً بفصل. استُخدم كمصدر مستقل للتحقق من إجابات أسئلة الكتاب.'),
        ('مجموعة أسئلة الدورات المجمعة', 'تجميعات دورات سابقة تعود لمقرر أقدم؛ لم يُؤخذ منها إلا ما يوجد مفهومه في الكتاب الحالي، بعد إعادة التحقق من الكتاب.'),
        ('ملف أسئلة مقرر نظم المعلومات وحلّه', 'ملف أسئلة مع ملف حلّ مرافق له؛ عومل الاثنان كمصدر واحد لأن الحلّ تابع للأسئلة.'),
        ('تجميع MIS Q', 'تجميع أسئلة سابق؛ استُخدم بالشروط نفسها.'),
        ('مفتاح إجابات دورة مصوّرة', 'مفتاح إجابات مكوّن من خمسين بنداً، متوفّر كملف PDF وكصور فوتوغرافية لنفس الأوراق؛ عومل كمصدر واحد.'),
        ('ملاحظات المقرر وأسئلة امتحان 2019', 'ملاحظات وتعاريف وأسئلة امتحان؛ استُخدمت بالشروط نفسها.'),
    ]
    for n, d in srcdesc:
        rich(doc, [('• ', dict(size=11, color=GRAY)), (n + ': ', dict(size=11, bold=True)),
                   (d, dict(size=11))], indent=0.4, space_after=2)

    # ---------------- MOST REPEATED ----------------
    doc.add_page_break()
    heading(doc, 'الأسئلة الأكثر تكراراً', 1, 17, BLUE, space_before=0)
    para(doc, 'الأسئلة التي وردت في ثلاثة مصادر مستقلة فأكثر، مرتّبة تنازلياً حسب عدد المصادر ثم حسب رقم الفصل. الإجابات غير معروضة هنا عمداً — راجعها في موضعها داخل الفصل.', size=10.5, color=GRAY)
    top = sorted([x for x in Q if x['freq'] >= 3], key=lambda x: (-x['freq'], x['ch'], x['id']))
    cur = None
    for x in top:
        if x['freq'] != cur:
            cur = x['freq']
            rich(doc, [('تكرار: ', dict(size=12, bold=True, color=RED)),
                       (LRM + str(cur) + LRM, dict(size=12, bold=True, color=RED)),
                       (' مصادر مستقلة', dict(size=12, bold=True, color=RED))],
                 space_before=10, space_after=4)
        txt = x['text'] if len(x['text']) <= 155 else x['text'][:152] + '…'
        rich(doc, [('[' + LRM + 'ف' + str(x['ch']) + ' · ' + x['id'] + LRM + '] ', dict(size=9.5, color=GRAY)),
                   (txt, dict(size=10.5))], indent=0.4, space_after=3)

    # ---------------- CHAPTERS ----------------
    qno_global = 0
    for ch in CHAPTERS:
        doc.add_page_break()
        title, rng = CH[ch]
        heading(doc, title, 1, 16, BLUE, space_before=0)
        items = sorted([x for x in Q if x['ch'] == ch], key=sort_key)
        nd = sum(1 for x in items if grp_of(x) == 'دورة')
        nb = sum(1 for x in items if grp_of(x) == 'كتاب')
        no = sum(1 for x in items if grp_of(x) == 'أخرى')
        ng = sum(1 for x in items if grp_of(x) == 'مولّد')
        rich(doc, [('صفحات الفصل في الكتاب: ', dict(size=10, color=GRAY)),
                   (LRM + rng + LRM, dict(size=10, color=GRAY)),
                   ('   |   عدد الأسئلة: ', dict(size=10, color=GRAY)),
                   (LRM + str(len(items)) + LRM, dict(size=10, color=GRAY)),
                   ('   |   منها أسئلة دورات: ', dict(size=10, color=GRAY)),
                   (LRM + str(nd) + LRM, dict(size=10, color=GRAY)),
                   ('   وأسئلة كتاب: ', dict(size=10, color=GRAY)),
                   (LRM + str(nb) + LRM, dict(size=10, color=GRAY)),
                   ('   ومن مصادر أخرى: ', dict(size=10, color=GRAY)),
                   (LRM + str(no) + LRM, dict(size=10, color=GRAY)),
                   ('   ومولّدة: ', dict(size=10, color=GRAY)),
                   (LRM + str(ng) + LRM, dict(size=10, color=GRAY))], space_after=10)

        section_flag = None
        for i, x in enumerate(items, 1):
            grp = grp_of(x)
            if grp != section_flag:
                section_flag = grp
                heading(doc, GRP_LABEL[grp], 2, 13, GRP_COLOR[grp], space_before=12, space_after=6)
                if grp == 'مولّد':
                    para(doc, 'هذه الأسئلة ليست منقولة من أي دورة أو ملف؛ صيغت خصيصاً لتغطية أفكار واردة في '
                              'كتاب المقرر لم يتناولها أي سؤال في المصادر المتاحة. كل إجابة هنا مأخوذة من نص '
                              'الكتاب مع رقم صفحة متحقَّق منه، ولا يُتوقع ورودها في الدورات — فهي للفهم '
                              'وسدّ النقص لا للتنبؤ بالامتحان.',
                         size=9.5, color=GRAY, indent=0.35, space_after=6)
                if grp == 'أخرى':
                    para(doc, 'أسئلة جُمعت من بقية ملفات المادة (ملخصات، أدلة مذاكرة، تجميعات دورات قديمة)، '
                              'وأُبقي منها ما يوجد مفهومه فعلاً في كتاب المقرر الحالي، وأُعيد التحقق من كل إجابة '
                              'من نص الكتاب لا من مفاتيح تلك الملفات.',
                         size=9.5, color=GRAY, indent=0.35, space_after=6)
            qno_global += 1
            tag = '%04d' % qno_global
            x['_tag'] = tag
            # --- question heading (Heading 3) ---
            qh = doc.add_paragraph(style='Heading 3')
            set_rtl(qh, True)
            pf = qh.paragraph_format
            pf.space_before = Pt(11); pf.space_after = Pt(2)
            pf.keep_with_next = True; pf.line_spacing = 1.2
            fmt(qh.add_run(LRM + 'س' + str(i) + LRM + ' · '), 12, GRAY, True)
            fmt(qh.add_run(x['text']), 12.5, DARK, True)
            # --- faded metadata line ---
            types_ar = ' + '.join(TYPE_LABEL.get(t, t) for t in x['types'])
            if x['freq'] == 0:
                meta = ('%s · %s · لم ترد في أي مصدر — مولّد لتغطية فجوة · %s'
                        % (x['id'], QTYPE_AR[x['qtype']], types_ar))
            else:
                meta = ('%s · %s · تكرار: %s من المصادر المستقلة · %s'
                        % (x['id'], QTYPE_AR[x['qtype']], LRM + str(x['freq']) + LRM, types_ar))
            mp = rich(doc, [(meta, dict(size=8.5, color=GRAY))], indent=0.35, space_after=3)
            mp.paragraph_format.keep_with_next = True
            # --- options ---
            if x['opts']:
                for j, o in enumerate(x['opts']):
                    lab = 'أ ب ت ث ج ح'.split()[j]
                    o_rtl = is_rtl(o)
                    if o_rtl:
                        op = rich(doc, [(lab + ') ', dict(size=10.5, color=GRAY, bold=True)),
                                        (o, dict(size=11))], rtl=True, indent=0.7, space_after=1)
                    else:
                        op = rich(doc, [(lab + ') ' + o, dict(size=11))], rtl=False, indent=0.7, space_after=1)
                    op.paragraph_format.keep_with_next = True
            if not PLAIN:
                # collapsible answer heading (Heading 4, collapsed) + START anchor
                ah = heading(doc, '  ▸  إظهار الإجابة والشرح', 4, 10.5, GREEN, collapsed=True,
                             space_before=5, space_after=3, keep_next=True)
                fmt(ah.add_run(' AS' + tag), 1, RGBColor(0xFF, 0xFF, 0xFF))
            # --- answer body ---
            p1 = rich(doc, [('الإجابة الصحيحة: ', dict(size=11, bold=True, color=GREEN))]
                      + md_parts(x['ans'], dict(size=11, bold=True)), indent=0.35, space_after=3,
                      space_before=6 if PLAIN else 0)
            p1.paragraph_format.keep_with_next = True
            if x.get('book_answer'):
                pb = rich(doc, [('إجابة مغايرة وردت في مصدر آخر (للمقارنة فقط): ', dict(size=10.5, bold=True, color=RED))]
                          + md_parts(x['book_answer'], dict(size=10.5, color=RED)), indent=0.35, space_after=3)
                pb.paragraph_format.keep_with_next = True
            p2 = rich(doc, [('الشرح: ', dict(size=10.5, bold=True, color=BLUE))]
                      + md_parts(x['exp'], dict(size=10.5)), indent=0.35, space_after=3)
            p2.paragraph_format.keep_with_next = True
            srcs = '، '.join(SRC_AR[s] for s in x['src'])
            p3 = rich(doc, [('المرجع: الكتاب، الفصل ', dict(size=9, color=GRAY)),
                            (LRM + str(x['ch']) + LRM, dict(size=9, color=GRAY)),
                            ('، صفحة ', dict(size=9, color=GRAY)),
                            (LRM + str(x['page']) + LRM, dict(size=9, color=GRAY)),
                            (' (الصفحة المطبوعة = صفحة PDF)  ·  المصادر: ', dict(size=9, color=GRAY)),
                            (srcs, dict(size=9, color=GRAY))], indent=0.35, space_after=2)
            if not PLAIN:
                fmt(p3.add_run(' AE' + tag), 1, RGBColor(0xFF, 0xFF, 0xFF))
            hr(doc)

    # ---------------- METHODOLOGY ----------------
    doc.add_page_break()
    heading(doc, 'المنهجية وحدود العمل', 1, 17, BLUE, space_before=0)
    meth = [
        ('كيف بُنِي هذا الملف',
         'قُرئ كتاب المقرر كاملاً (507 صفحات) أولاً، ثم فُهرست حدود الفصول وعناوينها وتعاريفها ونماذجها وجداولها وأرقام صفحاتها. بعد ذلك استُخرجت الأسئلة من كل الملفات المرفقة، وصُنّفت، ووُحّدت المكرّرة، وتُحقّق من كل إجابة مقابل نص الكتاب.'),
        ('فحص الصور والمسح الضوئي',
         'فُحصت جميع صور المجلدات المرفقة بصرياً صورةً صورة، ولم يُكتفَ باستخراج النص. وعدد الصور اثنتا عشرة صورة، تبيّن بعد المطابقة بالبصمة الرقمية أن سبعاً منها فقط فريدة والباقي نسخ مكررة. وست من الصور الفريدة أوراق فوتوغرافية لمفتاح إجابات واحد مؤلَّف من خمسين بنداً، والسابعة صورة صفحة من كتاب أقدم عن التنقيب في البيانات. وقُرئت هذه الأوراق بالكامل بالفحص البصري، وأُخذ منها ما يوجد مفهومه في كتاب المقرر الحالي إلى قسم «أسئلة من مصادر أخرى»، بعد إعادة التحقق من كل إجابة من نص الكتاب.'),
        ('تدقيق تغطية الأفكار والقسم الرابع',
         'لم يكن كافياً جمع الأسئلة وتوحيدها، إذ قد تترك المصادر مجتمعةً أفكاراً في الكتاب دون أي سؤال. لذلك قُسّم كتاب المقرر إلى مئة وفقرة فرعية ضمن الفصول الثمانية المشمولة، وفُحصت كل فقرة آلياً ويدوياً لمعرفة ما إذا كان نص أي سؤال أو خياراته أو إجابته يتناولها. وكانت النتيجة أن تسعاً وستين فقرة مغطاة بأسئلة فعلية، وأن عشر فقرات ورد ذكرها في الشروح فقط دون أن يُسأل عنها، وأن اثنتين وعشرين فقرة لم يتناولها شيء إطلاقاً. وقد صيغت لهذه الفجوات ثلاثة وثلاثون سؤالاً وُضعت في قسم رابع منفصل في كل فصل بعنوان «أسئلة مولّدة»، بحيث تبقى مميّزة تماماً عن أسئلة الدورات والكتاب فلا تختلط بها. وكل إجابة فيها مأخوذة من نص الكتاب مع رقم صفحة متحقَّق منه، ولم يُدرج سؤال مولّد لفكرة يغطيها سؤال قائم، ولا فكرة مكررة بين سؤالين مولّدين.'),
        ('لماذا وُجد قسم ثالث في كل فصل',
         'رُتّبت أسئلة كل فصل في ثلاثة أقسام: أسئلة الدورات أولاً، ثم أسئلة الكتاب، ثم أسئلة جُمعت من بقية مواد المذاكرة (الملخصات وأدلة المذاكرة وتجميعات الدورات القديمة). ويخضع القسم الثالث لشرطين: أن يكون مفهوم السؤال موجوداً فعلاً في أحد الفصول الثمانية من كتاب المقرر الحالي، وأن تكون إجابته قابلة للتحقق من نص الكتاب مع رقم صفحة متحقَّق منه. وما لم يستوفِ الشرطين بقي مستبعَداً.'),
        ('ملخص عاصم كمصدر مستقل للتحقق',
         'يعيد «ملخص عاصم 2022» إيراد أسئلة نهاية الفصول الواردة في الكتاب مع إجاباتها المحلولة. وقد قوبلت إجاباته بإجابات هذا الملف سؤالاً بسؤال لأسئلة الصح والخطأ في الفصول الثمانية: تطابقت أربع وستون إجابة من خمس وستين، واختلفت إجابة واحدة فقط (سؤال ربط جداول النموذج العلائقي في الفصل الخامس) وقد عُرضت الإجابتان معاً في موضع السؤال.'),
        ('كشف الملفات المكررة',
         'حُسبت بصمة رقمية (MD5) لكل ملف قبل عدّ التكرار. تبيّن أن ملف «حل أسئلة MIS» موجود ثلاث مرات بأسماء ومسارات مختلفة وبمحتوى متطابق بايت ببايت، وأن ملف «MIS Q» موجود نسختين، وأن خمساً من صور المجلد مكررة مزدوجة. عُوملت كل مجموعة متطابقة على أنها مصدر واحد فقط، ولم يُرفع عدّاد التكرار بسبب رفع الملف نفسه أكثر من مرة أو بسبب تحويله إلى صيغة أخرى.'),
        ('حدود مهمة: المادة تتبع مقررين مختلفين',
         'أغلب ملفات الدورات المرفقة لا تعود إلى كتاب الدكتور إياد زوكار، بل إلى مقرر أقدم لنظم المعلومات الإدارية (يظهر اسم الدكتور سليمان عوض في أحد الملفات). ذلك المقرر يدور حول أداة Solver في Excel، والتصفية التلقائية، والجدول المحوري، ودرجة التقارب، وشجرة القرار، والشبكات العصبية، وتحليل المجموعة المتجانسة، ونظم معلومات التنفيذيين، وإطار Hong لتصنيف النظم بين المنظمات — وهي موضوعات لا وجود لها إطلاقاً في كتاب المقرر الحالي، وأرقام صفحاتها لا تطابقه. لذلك استُبعدت هذه المصادر بالكامل من بنك الأسئلة، لأن التحقق من إجاباتها مقابل الكتاب المعتمد غير ممكن، ولأن إدراجها كان سيضلّل المراجعة.'),
        ('الملفات المستبعدة لهذا السبب',
         'اسئلة_دورات_مجمعة_MIS · أسئلة_من_مقرر_نظم_المعلومات_الإدارية · تجميعة اسئلة دورات_MIS_2 · MIS Q · MIS_محدد عليه اسئلة الدورات · تعريفات_مادة_نظم_المعلومات · ملاحظات_مقرر_MIS · اسئلة MIS_امتحان_2019 · حل أسئلة MIS · دورات.pdf · MIS_F19_Anan · ومجلد الصور MISS بكامله.'),
        ('مصدر لم يُقرأ آلياً',
         'ملف «أسئلة الكتاب - MIS» مكتوب بخط عربي لا يحمل جدول ترميز Unicode، فخرج نصه العربي مشوّهاً تماماً عند الاستخراج. غير أن محتواه هو نفسه أسئلة نهاية الفصول الموجودة في كتاب المقرر، وقد أُخذت هذه الأسئلة من الكتاب نفسه بنصّها الصحيح، فلم تضع أي معلومة.'),
        ('عدّ التكرار',
         'عدّاد التكرار المذكور مع كل سؤال هو عدد المصادر المستقلة التي ورد فيها السؤال، لا عدد الملفات. والسؤال يُعدّ مرة واحدة فقط في المصدر الواحد حتى لو تكرر داخله عدة مرات — وقد تكرر داخل ملف «دورات» قسم كامل مرتين، فلم يُحتسب إلا مرة واحدة.'),
        ('تعارض بين ورقة حل وكتاب المقرر',
         'في سؤال «الموازنة السنوية Budgeting planning تنتمي إلى أي نظام؟» وردت في إحدى ورقات الحل إجابة ESS، بينما ينص جدول الكتاب صراحةً على أن مثال نظام MIS هو «الموازنة السنوية» وأن مستواه التنظيمي هو المستوى الإداري. وقد أُبقيت الإجابتان ظاهرتين معاً في موضع السؤال: إجابة الكتاب هي المعتمدة، وإجابة ورقة الحل مذكورة للمقارنة.'),
        ('سؤال لا يمكن تأكيده من متن الكتاب',
         'عبارة «تستخدم العديد من الأنظمة التقليدية القديمة الكبيرة DBMS الهرمية» واردة ضمن أسئلة نهاية الفصل الخامس، لكن متن الفصل لا يتناول قواعد البيانات الهرمية إطلاقاً. أُعطيت الإجابة وفق المرجع الأصلي الذي ينقل عنه الكتاب (Laudon & Laudon, MIS 16th ed.) مع تنبيه واضح في موضع السؤال.'),
        ('ما استُبعد رغم وروده في مواد المذاكرة',
         'استُبعدت من القسم الثالث الموضوعات التي لا وجود لها في كتاب المقرر الحالي ولا يمكن التحقق من إجاباتها منه: أداة Solver ودرجة التقارب، والتصفية التلقائية والجدول المحوري ودوال التلخيص في Excel، وتحليل المجموعة المتجانسة، وسلاسل ماركوف، ونظم معلومات التنفيذيين ولوحة القيادة بتصنيفها الثلاثي، وإطار Hong للنظم بين المنظمات، والتحريات الوظيفية، وتصنيف النظم المفتوحة والمغلقة ونظام الساعة، ومفهوم «نظام العمل». وقد فُضّل استبعادها على إدراجها بإجابات غير متحقَّق منها.'),
        ('ما لم يُدرج',
         'لم تُدرج أسئلة الفصول 4 و6 و11 و12 لأنها خارج النطاق المطلوب. ولم تُدرج الأسئلة التي تعذّر إسنادها إلى أحد الفصول الثمانية بثقة كافية، ولم تُخترع أي خيارات أو إجابات أو أرقام صفحات غير متحقَّق منها.'),
    ]
    for h, b in meth:
        para(doc, h, size=12, bold=True, color=DARK, space_before=8, space_after=2, keep_next=True)
        para(doc, b, size=10.5, indent=0.35)

    # ---------------- TOC + METADATA (at the end, as requested) ----------------
    doc.add_page_break()
    heading(doc, 'فهرس المحتويات', 1, 17, BLUE, space_before=0)
    para(doc, 'إن ظهر الفهرس فارغاً في Word، اضغط بداخله ثم اضغط F9 لتحديثه.', size=9.5, color=GRAY)
    p = doc.add_paragraph(); set_rtl(p, True)
    r = p.add_run(); fmt(r, 11)
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve')
    it.text = r' TOC \o "1-2" \h \z \u '
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'separate')
    f3 = OxmlElement('w:fldChar'); f3.set(qn('w:fldCharType'), 'end')
    r._r.append(f1); r._r.append(it); r._r.append(f2); r._r.append(f3)

    doc.add_page_break()
    heading(doc, 'بيانات الملف', 1, 17, BLUE, space_before=0)
    counts = {ch: sum(1 for x in Q if x['ch'] == ch) for ch in CHAPTERS}
    md = [('عنوان المراجعة', TITLE),
          ('المرجع الأساسي', 'كتاب مقرر نظم المعلومات الإدارية — الدكتور إياد زوكار'),
          ('الفصول المشمولة', LRM + '1, 2, 3, 5, 7, 8, 9, 10' + LRM),
          ('عدد الأسئلة الكلي', LRM + str(len(Q)) + LRM),
          ('لغة الأسئلة', 'عربية / إنكليزية ممزوجة'),
          ('لغة الشرح', 'العربية')]
    for ch in CHAPTERS:
        md.append(('عدد أسئلة الفصل ' + LRM + str(ch) + LRM, LRM + str(counts[ch]) + LRM))
    t = doc.add_table(rows=0, cols=2); t.style = 'Light Grid Accent 1'
    for k, v in md:
        row = t.add_row().cells
        p0 = row[0].paragraphs[0]; set_rtl(p0, True); fmt(p0.add_run(k), 10)
        p1 = row[1].paragraphs[0]; set_rtl(p1, True); fmt(p1.add_run(v), 10, DARK, True)
    para(doc, '', space_after=8)
    para(doc, 'لا يحتوي هذا الملف على أي بيانات شخصية عن جهاز المستخدم أو حسابه.', size=9.5, color=GRAY)

    # ---------------- BUTTON CAPTION ASSETS (last page; stripped from the PDF) --------
    if os.environ.get('MIS_ASSETS') == '1':
        doc.add_page_break()
        p = doc.add_paragraph(); set_rtl(p, True)
        p.paragraph_format.space_after = Pt(30)
        fmt(p.add_run('ZZSHOW '), 9, RGBColor(0xFF, 0xFF, 0xFF), rtl=False)
        fmt(p.add_run('▸  إظهار الإجابة والشرح'), 10.5, GREEN, True)
        p = doc.add_paragraph(); set_rtl(p, True)
        p.paragraph_format.space_after = Pt(30)
        fmt(p.add_run('ZZHIDE '), 9, RGBColor(0xFF, 0xFF, 0xFF), rtl=False)
        fmt(p.add_run('▾  إخفاء الإجابة والشرح'), 10.5, RED, True)

    doc.core_properties.title = TITLE
    doc.core_properties.author = ''
    doc.core_properties.last_modified_by = ''
    doc.core_properties.comments = ''
    doc.core_properties.category = ''
    doc.core_properties.subject = 'MIS review'
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, ('plain_' if PLAIN else '') + TITLE + '.docx')
    doc.save(out)
    import json
    json.dump({x['_tag']: {'id': x['id'], 'ch': x['ch'], 'freq': x['freq'], 'qtype': x['qtype']}
               for x in Q if '_tag' in x},
              open(os.path.join(here, 'tags.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('saved:', out)
    print('questions rendered:', qno_global)
    return out

if __name__ == '__main__':
    build()
