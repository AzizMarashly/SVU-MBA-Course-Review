# -*- coding: utf-8 -*-
"""Render bank.json -> single self-contained RTL HTML review file (spec v0.9 rendering of a v0.4-built bank)."""
import json, os, re, html, datetime, collections
HERE = os.path.dirname(__file__)
B = json.load(open(os.path.join(HERE, "..", "bank.json"), encoding="utf-8"))
QS = B["questions"]; SUBS = {int(k): v for k, v in B["subsections"].items()}
CHAPTERS = B["chapters_in_scope"]
FOCUS = set(tuple(x) for x in B["focus_areas"])
TITLE = B["title"]; SPEC = B["spec_version"]; VER = B["file_version"]
LETTERS = ["أ", "ب", "ج", "د", "هـ", "و"]
TODAY = "2026-09-09"

CH_TITLES = {1:"طبيعة التسويق الدولي", 2:"البيئة الثقافية والاجتماعية للتسويق الدولي", 3:"البيئة السياسية والقانونية للتسويق الدولي",
 4:"البيئة الاقتصادية الدولية", 5:"إدارة المعلومات الدولية وبحوث التسويق الدولية", 6:"استراتيجيات الدخول إلى الأسواق الدولية",
 7:"استراتيجيات المنتج في الأسواق الدولية", 9:"استراتيجيات التسعير في الأسواق الدولية", 10:"استراتيجيات التوزيع في الأسواق الدولية",
 11:"الاتصالات التسويقية المتكاملة في الأسواق الدولية: الإعلان", 12:"عناصر الاتصالات التسويقية المتكاملة في الأسواق الدولية"}
CH_PAGES = {1:(10,47),2:(49,88),3:(90,128),4:(130,168),5:(169,196),6:(198,233),7:(235,263),9:(297,323),10:(325,356),11:(358,389),12:(391,422)}
OPENERS = {  # two lines each: (about, bold-terms)
 1:("يشرح الفصل دوافع انتشار الأعمال الدولية، ومراحل تطور التسويق الدولي، والتوجهات التسويقية للشركات، وإيجابيات وسلبيات الشركات عابرة القومية.",
    "**الدوافع الأساسية**، **التسويق الخارجي غير المنتظم/المنتظم**، **الموجهة بالمركز الرئيسي / تعدد المراكز / الأقاليم / العالمي**، **التبعية الاقتصادية والتكنولوجية**، **تشويه الهوية الثقافية**"),
 2:("يتناول الفصل مفهوم الثقافة وخصائصها ومكوناتها الثمانية، ومداخل دراستها (الارتباط بالسياق وهوفستد)، وأثرها على المزيج التسويقي.",
    "**مكتسبة/إلزامية/ديناميكية**، **جوهرية مقابل فرعية**، **اللغة (مرآة المجتمع)**، **الحياة المادية**، **ضعيفة/قوية الارتباط بالسياق**، **تباين النفوذ (هوفستد)**"),
 3:("يناقش الفصل سيادة الأمم والمخاطر السياسية والاقتصادية والعقوبات وهيكل الحكومة، ثم النظم القانونية والملكية الفكرية والقضايا الأخلاقية.",
    "**القانون العام مقابل المدني**، **القانون الدولي الخاص**، **نزع الملكية / المصادرة / التأميم / الأهلنة**، **التزييف / الانتهاك / القرصنة**، **الإغراق**، **السوق الرمادية**"),
 4:("يحلل الفصل حجم السوق (السكان والدخل) وطبيعة السوق (البيئة الطبيعية، النشاط الاقتصادي، البنية التحتية، التمدن).",
    "**متوسط دخل الفرد وأوجه قصوره**، **تكافؤ القوة الشرائية / Big Mac**، **طبيعة السوق مقابل حجم السوق**، **الطبوغرافيا ← التوزيع**، **وسائل الاتصال ← الترويج**"),
 5:("يشرح الفصل نظم معلومات التسويق وقواعد البيانات والبيانات الضخمة، والفرق بين بحوث التسويق الدولية والمحلية، وخطوات البحث الست.",
    "**نظام معلومات التسويق**، **تكنولوجيا المعلومات**، **البيانات الضخمة (3V) والذكاء الاصطناعي**، **تصميم البحث**، **تحديد المشكلة أولاً**، **إعداد التقرير وتقديمه**"),
 6:("يعرض الفصل الطرق الأربع لدخول الأسواق الدولية وما يرتبط بكل منها من استثمار ومخاطر وسيطرة: التصدير، الاتفاقيات التعاقدية، المشروعات المشتركة، الاستثمار المباشر.",
    "**عقود التصنيع (ميزة التسويق)**، **الترخيص والتزامات المرخَّص له**، **الامتياز (الفنادق والوجبات السريعة)**، **المشروعات المشتركة (25–75%)**، **الاستحواذ / Greenfield**"),
 7:("يتناول الفصل قرار توحيد أو تعديل المنتج وأبعاده الدولية: التغليف، اللصاقة التعريفية، الضمان، الخدمة، العلامة التجارية، وتأثير بلد المنشأ.",
    "**حجم العبوة (الدخل، عادات التسوق، حجم المتجر)**، **التشريعات الحكومية للصاقة**، **اعتبارات الضمان الأربعة**، **قيمة العلامة التجارية**، **علامة موحدة مقابل محلية**، **تأثير بلد المنشأ**"),
 9:("يشرح الفصل سياسات التسعير الدولي (التكلفة المتغيرة/الكلية، القشط/التغلغل)، والعوامل الداخلية والخارجية، وتصاعد الأسعار والإغراق والصفقات المتكافئة.",
    "**القشط (طلب غير مرن) مقابل التغلغل (طلب مرن)**، **التكلفة الحدية**، **العوامل الداخلية: أهداف/مركزية/عالمية**، **احتكار القلة والمشروع القائد**، **تصاعد الأسعار**، **الإغراق**"),
 10:("يناقش الفصل منافع قنوات التوزيع، والقنوات المباشرة وغير المباشرة، وأهداف التوزيع الستة، وكثافة التوزيع وطول القناة، وأنواع متاجر التجزئة والقنوات الرقمية.",
     "**منفعة الوقت (FedEx) والمكان (كوكاكولا)**، **6C**، **كثافة التوزيع (مكثف/انتقائي/محدود)**، **طول القناة والدخل**، **تجزئة خارج المتجر**، **تكلفة الوسطاء**"),
 11:("يعرض الفصل مفهوم الاتصالات التسويقية المتكاملة وعملية الاتصال، ومحددات البرنامج الإعلاني الستة، والقرارات الإعلانية الخمسة.",
     "**محددات البرنامج الإعلاني**، **القيود الحكومية (المنتج/الوسيلة/الرسالة)**، **اختيار وكالة الإعلان أولاً**، **وكالة دولية للسلع الصناعية**، **طرق تحديد المخصص**، **قيود تقييم الكفاءة الثلاثة**"),
 12:("يشرح الفصل العلاقات العامة والبيع الشخصي (اختيار، تدريب، تحفيز، رقابة) وتنشيط المبيعات والمعارض التجارية والتسويق المباشر.",
     "**أهداف العلاقات العامة**، **التدريب في المركز الرئيسي للمنتجات الصناعية/عالية التقنية**، **وظائف القوى البيعية الأربع**، **محددات تنشيط المبيعات القانونية**، **معارض عامة/متخصصة**، **أشكال التسويق المباشر**"),
}
SRC_NAMES = {"F17":"دورة F17","F19":"دورة F19","S24":"دورة S24","F24":"دورة F24","BOOK":"أسئلة الكتاب","EMAD":"ملخص عماد جبور (S18)","ASEM":"ملخص عاصم (حل أسئلة الكتاب)","GEN":"مولَّد لسد فجوة"}
REPO = "https://github.com/AzizMarashly/SVU-MBA-Course-Review"

# §11d — every file supplied in the course folder, in the order shown in the appendix.
# (n, relative path, kind, role, source group, pages/items, note). Page counts are PDF page counts.
FILES = [
 (1, "المنهاج الٱكاديمي/MBA-International Marketing and Trading-The Book.pdf", "كتاب المقرر", "المرجع الأساسي", "BOOK", "423 صفحة، قُرئت كلها", "لا يذكر الملف طبعة أو سنة. رقم الصفحة المطبوع = رقم صفحة PDF. خط النص بلا خريطة يونيكود فاستُخرج النص بالتعرّف الضوئي وقورن بالصورة (البند 1أ)."),
 (2, "المنهاج الٱكاديمي/_⁨أسئلة الكتاب - IMT⁩.pdf", "كتاب المقرر (مقتطف)", "نسخة تابعة للمرجع الأساسي", "BOOK", "24 صفحة", "أسئلة المراجعة من نهاية فصول #1 بترقيم مختلف؛ ليست مصدراً مستقلاً."),
 (3, "اسئلة سابقة/دورة f17 تسويق دولي.docx", "امتحان سابق", "مصدر امتحان", "F17", "27 سؤالاً", "دورة F17 منقولة من الذاكرة."),
 (4, "اسئلة سابقة/IMT_دورة f17 تسويق دولي⁩.docx", "امتحان سابق", "نسخة مكررة", "F17", "—", "مطابق لـ #3 (بصمة MD5 واحدة)."),
 (5, "اسئلة سابقة/_⁨أسئلة-تسويق-دولي_IMT(1)⁩.pdf", "امتحان سابق + ملاحظات إجابة", "نسخة تابعة", "F17", "13 صفحة، 7 صور مضمّنة فُحصت", "الأسئلة الـ27 نفسها التي في #3 مع صور لملاحظات إجابات بخط اليد ولقطتين من كتاب أقدم؛ تُعدّ مع #3 مصدراً واحداً."),
 (6, "اسئلة سابقة/دورات  F19.pdf", "امتحان سابق (مسح ضوئي بخط اليد)", "مصدر امتحان", "F19", "4 صفحات، 30 سؤالاً، قُرئت بصرياً", "دورة F19؛ النص المنسوخ في ملف العمل notes/f19_transcription.md."),
 (7, "اسئلة سابقة/أسئلة_دورات_F19_تسويق_دولي_MIS.pdf", "امتحان سابق (مسح ضوئي)", "نسخة مكررة", "F19", "—", "مطابق لـ #6 (بصمة MD5 واحدة)."),
 (8, "اسئلة سابقة/دورات.txt", "امتحانان سابقان (تصدير محادثة تيليغرام)", "مصدر امتحان", "F24 + S24", "40 سؤالاً (F24) + 32 سؤالاً (S24)", "ملف واحد يحوي جلستين مستقلتين فعُدّ مصدرين."),
 (9, "اسئلة سابقة/_⁨ملخصIMT عماد جبور كامل⁩.pdf", "ملخص بصيغة سؤال وجواب (S18)", "مصدر أسئلة أخرى", "EMAD", "58 صفحة، 469 بنداً", "أُدرج منه ما يوجد مفهومه في الكتاب الحالي فقط، وأُعيد التحقق من كل إجابة."),
 (10, "ملخصات سابقة/_⁨ملخص_عاصم_التسويق_والتجارة_الدولية_IMT⁩.pdf", "ملخص مع حل أسئلة الكتاب", "تحقق متقاطع", "ASEM", "23 صفحة، 60 عبارة صح/خطأ قورنت", "59 من 60 تطابق مفتاح الكتاب؛ لا أسئلة جديدة منه."),
 (11, "ملخصات سابقة/IMT_F19_وائل منصور.pdf", "ملخص بخط اليد (مسح ضوئي)", "مستبعد", "EXCLUDED-WAEL", "56 صفحة فُحصت كلها بصرياً", "لا يحوي أسئلة، وتقسيمه لفصول منهاج أقدم."),
 (12, "ملفات متعلقة بالمادة/photo_2024-06-05_20-58-43.jpg", "صورة بخط اليد", "دليل على مجالات التركيز فقط", "PHOTO", "صورة واحدة فُحصت", "قائمة موضوعات وردت في امتحان بترقيم فصول الكتاب؛ لا نص أسئلة."),
 (13, "اسئلة سابقة/imt exam.docx", "أسئلة مقالية من منهاج أقدم", "مستبعد", "EXCLUDED-OLD-ESSAY", "42 سؤالاً مقالياً مع إجاباته", "موضوعاته (المدخل الإدراكي، مبادئ منظمة التجارة العالمية، الحماية والليبرالية، الميزان التجاري…) غير موجودة في الكتاب الحالي (البند 2)."),
 (14, "اسئلة سابقة/imt exam(1).docx", "أسئلة مقالية من منهاج أقدم", "نسخة مكررة", "EXCLUDED-OLD-ESSAY", "—", "مطابق لـ #13."),
 (15, "اسئلة سابقة/imt-exam.docx", "أسئلة مقالية من منهاج أقدم", "نسخة مكررة", "EXCLUDED-OLD-ESSAY", "—", "مطابق لـ #13."),
 (16, "اسئلة سابقة/اسئلة.docx", "أسئلة مقالية من منهاج أقدم", "نسخة مكررة", "EXCLUDED-OLD-ESSAY", "—", "المحتوى نفسه في #13 بفروق مسافات فقط."),
 (17, "اسئلة سابقة/اسئلة(1).docx", "أسئلة مقالية من منهاج أقدم", "نسخة مكررة", "EXCLUDED-OLD-ESSAY", "—", "مطابق لـ #16."),
 (18, "اسئلة سابقة/اسئلة_IMT.docx", "أسئلة مقالية من منهاج أقدم", "نسخة مكررة", "EXCLUDED-OLD-ESSAY", "—", "مطابق لـ #16."),
 (19, "اسئلة سابقة/اسئلة_دورات_IMT.pdf", "أسئلة مقالية من منهاج أقدم", "نسخة مكررة", "EXCLUDED-OLD-ESSAY", "19 صفحة", "نسخة PDF من #13."),
 (20, "ملفات متعلقة بالمادة/الفصل الأول.pdf", "فصل من كتاب آخر", "مستبعد", "EXCLUDED-OLD-BOOK", "15 صفحة", "كتاب مختلف (مفهوم وماهية التسويق الدولي)؛ ليس المرجع الأساسي."),
 (21, "ملفات متعلقة بالمادة/الفصل الثاني.pdf", "فصل من كتاب آخر", "مستبعد", "EXCLUDED-OLD-BOOK", "24 صفحة", "كتاب مختلف (المنتج الدولي)."),
 (22, "ملفات متعلقة بالمادة/الفصل الثالث.pdf", "فصل من كتاب آخر", "مستبعد", "EXCLUDED-OLD-BOOK", "41 صفحة", "كتاب مختلف (التوزيع الدولي)."),
 (23, "ملفات متعلقة بالمادة/الفصل الخامس.pdf", "فصل من كتاب آخر", "مستبعد", "EXCLUDED-OLD-BOOK", "25 صفحة", "كتاب مختلف (الترويج الدولي)."),
 (24, "ملفات متعلقة بالمادة/شروط التجارة الدولية.ppt", "شرائح من مقرر آخر", "مستبعد", "EXCLUDED-PPT", "—", "«المحاضرة الثانية: شروط علاقات التجارة والرفاه الاقتصادي» — مقرر مختلف."),
 (25, "ملفات متعلقة بالمادة/شروط قيام التجارة والفاه الاقتصادي.ppt", "شرائح من مقرر آخر", "مستبعد", "EXCLUDED-PPT", "—", "المحتوى نفسه في #24 (بصمة مختلفة، ملف واحد)."),
 (26, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch01(Nature of International Marketing).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "19 صفحة", "لا تحوي أسئلة؛ الفصل 1 في الكتاب."),
 (27, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch02(International cultural and social environment).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "22 صفحة", "الفصل 2 في الكتاب."),
 (28, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch03 (International marketing political).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "19 صفحة", "الفصل 3 في الكتاب (مع #29)."),
 (29, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch04 (International marketing political).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "19 صفحة", "الفصل 3 في الكتاب (مع #28)."),
 (30, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch05(International Marketing Economic).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "25 صفحة", "الفصل 4 في الكتاب."),
 (31, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch06(Global Information Management and Global Marketing Research).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "26 صفحة", "الفصل 5 في الكتاب."),
 (32, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch07 (International Markets- Entry Strategies).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "19 صفحة", "الفصل 6 في الكتاب (مع #33)."),
 (33, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch08 (International Markets- Entry Strategies).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "18 صفحة", "الفصل 6 في الكتاب (مع #32)."),
 (34, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch09(Product Strategies in International Markets).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "20 صفحة", "الفصل 7 في الكتاب."),
 (35, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch10(New Products Development in International Markets).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "21 صفحة", "الفصل 8 في الكتاب — خارج النطاق."),
 (36, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch11(Pricing Strategies in International Markets).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "27 صفحة", "الفصل 9 في الكتاب."),
 (37, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch12(Distribution Strategies in International Markets).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "23 صفحة", "الفصل 10 في الكتاب."),
 (38, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch13(Integrated Marketing Communication in International Markets).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "24 صفحة", "الفصل 11 في الكتاب."),
 (39, "المنهاج الٱكاديمي/Slides/MBA-International Marketing and Trading-Ch14(Integrated Marketing Communication Elements in International Markets).pdf", "شرائح المقرر", "مرجع مساعد", "SLIDES", "24 صفحة", "الفصل 12 في الكتاب."),
]
# source code -> representative row number in FILES (the first file of the independent source)
SRC_ROW = {"BOOK":1, "F17":3, "F19":6, "F24":8, "S24":8, "EMAD":9, "ASEM":10}
FILES_SUMMARY = dict(files=len(FILES), sources=7, excluded=14, duplicates=9, images=91)
# images inspected: F19 4 pages + Wael 56 pages + photo 1 + #5 embedded 7 + book review pages 22 + #2 first page 1 = 91
SEC_NAMES = {"exam":"أسئلة الامتحانات","textbook":"أسئلة الكتاب","other":"أسئلة من مصادر أخرى","generated":"أسئلة مولَّدة لسد الفجوات"}
SEC_INTRO = {
 "exam":"أسئلة نقلها الطلاب من امتحانات سابقة (F17، F19، S24، F24). ما نُقل بصيغة حرة أُعيد بناؤه كسؤال اختيار من متعدد مع الإشارة إلى ذلك، ونصّ الطالب الأصلي مثبت تحت السؤال.",
 "textbook":"أسئلة المراجعة في نهاية كل فصل من الكتاب (صح/خطأ، خيارات متعددة، مقالية) بصيغتها الأصلية، والإجابات هي ما علّمه الكتاب نفسه (✓ والتظليل الأصفر) بعد التحقق من نص الفصل.",
 "other":"أسئلة من ملخص عماد جبور (S18) بصيغة سؤال وجواب، اختير منها ما يوجد مفهومه في الكتاب الحالي، وأُعيد التحقق من إجابته من الكتاب وصُحّح ما خالفه. أسئلة الملخص التي تخص منهاجاً أقدم (نظريات التجارة، عقود تسليم المفتاح، الأونكتاد…) لم تُدرج.",
 "generated":"أسئلة كتبتها هذه المراجعة من نص الكتاب لتغطية فقرات لم يسألها أي مصدر. هي لسد الفجوات فقط وليست توقعاً للامتحان، لذا تكرارها صفر وأهميتها 1.",
}

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
    about, terms = OPENERS[n]
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
    exam_q = [q for q in QS if "exam" in q["types"]]
    recon = sum(1 for q in QS if q["reconstructed"]); lowc = [q["id"] for q in QS if q["low_conf"]]
    gen = sum(1 for q in QS if "generated" in q["types"])
    total_subs = sum(len(v) for v in SUBS.values())
    focus_rows = [r for r in B["focus_table"] if (r["ch"], r["sub"]) in FOCUS]
    ft = "".join(f'<tr><td>{r["ch"]}</td><td>{esc(r["sub"])}</td><td>{esc(r["name"])}</td><td>{r["exam"]}</td><td>{r["textbook"]}</td><td>{r["other"]}</td><td>{r["total"]}</td></tr>' for r in sorted(focus_rows, key=lambda r:(r["ch"], -r["exam"], -r["total"])))
    ledger = """
<table class="tbl"><thead><tr><th>المعرّف</th><th>الملفات</th><th>النوع</th><th>القرار</th></tr></thead><tbody>
<tr><td>BOOK</td><td>MBA-International Marketing and Trading-The Book.pdf (423 صفحة) + أسئلة الكتاب - IMT.pdf (نسخة تابعة من فقرات المراجعة، معاد ترقيمها)</td><td>المرجع الأساسي وأسئلة نهاية الفصول</td><td>مُدرَج (المرجع الحاكم)</td></tr>
<tr><td>F17</td><td>دورة f17 تسويق دولي.docx = IMT_دورة f17 تسويق دولي.docx (MD5 متطابق) + أسئلة-تسويق-دولي_IMT(1).pdf (نفس الأسئلة الـ27 مع 7 صور مضمّنة لملاحظات إجابات مكتوبة بخط اليد ولقطتين من كتاب أقدم)</td><td>امتحان منقول من الذاكرة</td><td>مُدرَج كمصدر مستقل واحد</td></tr>
<tr><td>F19</td><td>دورات F19.pdf = أسئلة_دورات_F19_تسويق_دولي_MIS.pdf (MD5 متطابق؛ 4 صفحات ممسوحة بخط اليد، 30 سؤالاً، قُرئت بصرياً)</td><td>امتحان منقول من الذاكرة</td><td>مُدرَج</td></tr>
<tr><td>S24 و F24</td><td>دورات.txt (تصدير محادثة تيليغرام: 40 سؤالاً مع إجاباته لدورة F24، و32 سؤالاً وقوائم تذكّر لدورة S24 من طالبَين)</td><td>امتحانان منقولان من الذاكرة</td><td>مُدرَجان كمصدرين مستقلين (جلستان مختلفتان)</td></tr>
<tr><td>EMAD</td><td>ملخصIMT عماد جبور كامل.pdf (S18؛ 469 بنداً سؤال/جواب)</td><td>ملخص بصيغة أسئلة</td><td>مُدرَج جزئياً: البنود التي يوجد مفهومها في الكتاب الحالي فقط، وأُعيد التحقق منها</td></tr>
<tr><td>ASEM</td><td>ملخص_عاصم_التسويق_والتجارة_الدولية_IMT.pdf</td><td>ملخص + «حل أسئلة» الكتاب</td><td>مُدرَج كمصدر تحقق متقاطع لأسئلة الكتاب (لا أسئلة جديدة)</td></tr>
<tr><td>—</td><td>IMT_F19_وائل منصور.pdf (56 صفحة ممسوحة بخط اليد)</td><td>ملخص</td><td>فُحصت كل صفحاته بصرياً: ملخص بلا أسئلة، وبتقسيم منهاج أقدم → غير مُدرَج</td></tr>
<tr><td>—</td><td>photo_2024-06-05_20-58-43.jpg</td><td>صورة بخط اليد لقائمة موضوعات وردت في امتحان</td><td>استُخدمت كدليل على مجالات التركيز فقط (لا تحوي نص أسئلة)</td></tr>
<tr><td>—</td><td>imt exam.docx = imt exam(1).docx = imt-exam.docx؛ اسئلة.docx = اسئلة(1).docx = اسئلة_IMT.docx؛ اسئلة_دورات_IMT.pdf (كلها نسخ من ملف واحد: 42 سؤالاً مقالياً مع إجاباته)</td><td>أسئلة منهاج أقدم</td><td>مستبعدة: موضوعاتها (المدخل الإدراكي، مبادئ منظمة التجارة العالمية، الحماية والليبرالية، الحصة المزدوجة، الميزان التجاري…) غير موجودة في الكتاب الحالي</td></tr>
<tr><td>—</td><td>الفصل الأول.pdf، الفصل الثاني.pdf، الفصل الثالث.pdf، الفصل الخامس.pdf</td><td>فصول من كتاب آخر</td><td>مستبعدة: كتاب مختلف (مفهوم وماهية التسويق الدولي، المنتج الدولي، التوزيع، الترويج)</td></tr>
<tr><td>—</td><td>شروط التجارة الدولية.ppt، شروط قيام التجارة والرفاه الاقتصادي.ppt</td><td>محاضرة من مقرر آخر</td><td>مستبعدة: «المحاضرة الثانية: شروط علاقات التجارة والرفاه الاقتصادي — د. حسين الفحل» مقرر مختلف</td></tr>
<tr><td>—</td><td>الشرائح Ch01–Ch14</td><td>شرائح المقرر الحالي</td><td>لا تحوي أسئلة؛ استُخدمت مرجعاً مساعداً فقط</td></tr>
</tbody></table>"""
    chmap = """<table class="tbl"><thead><tr><th>تسمية المصدر</th><th>فصل الكتاب</th><th>الدليل</th></tr></thead><tbody>
<tr><td>الشرائح Ch01, Ch02</td><td>1, 2</td><td>العناوين متطابقة</td></tr>
<tr><td>الشرائح Ch03 + Ch04 (International marketing political)</td><td>3</td><td>الكتاب يجمع البيئة السياسية والقانونية في فصل واحد</td></tr>
<tr><td>Ch05 (Economic)</td><td>4</td><td>العنوان والمحتوى</td></tr>
<tr><td>Ch06 (Information & Research)</td><td>5</td><td>العنوان</td></tr>
<tr><td>Ch07 + Ch08 (Entry Strategies)</td><td>6</td><td>فصل واحد في الكتاب</td></tr>
<tr><td>Ch09 / Ch10 / Ch11 / Ch12 / Ch13 / Ch14</td><td>7 / 8 / 9 / 10 / 11 / 12</td><td>العناوين</td></tr>
<tr><td>صورة قائمة الموضوعات (photo_2024-06-05)</td><td>ترقيم الكتاب نفسه (1–12 دون 8)</td><td>«الفصل الخامس: تكنولوجيا المعلومات…» = فصل 5 في الكتاب</td></tr>
<tr><td>ملخص عماد (S18) وملخص وائل (F19)</td><td>تقسيم أقدم (مثلاً الثقافة = فصل 6)</td><td>رُبط كل بند بالمحتوى لا بالرقم</td></tr>
<tr><td>أرقام فصول أسئلة الامتحانات</td><td>—</td><td>لا تحمل أرقام فصول؛ أُسندت بالمحتوى إلى فقرة الكتاب</td></tr>
</tbody></table>"""
    return f"""
<section id="method"><h2>المنهجية</h2>
<h3>قراءة المرجع وتحقق أداة الاستخراج</h3>
<p>قُرئ الكتاب كاملاً (423 صفحة، 12 فصلاً). أرقام الصفحات المطبوعة تطابق أرقام صفحات PDF (تحقق آلي: 406 من 423 صفحة أظهر رقمها المطبوع مطابقاً، والباقي صفحات بلا رقم مقروء). خط النص الأساسي في PDF يحمل جدول ترميز معطوباً فيخرج الاستخراج النصي مشوّهاً (حروف ناقصة أو مبدَّلة)، لذلك <b>لم يُعتمد النص المستخرج</b> بل أُعيدت قراءة كل صفحة بالتعرّف الضوئي على الحروف (Windows OCR بالعربية) بعد تصييرها صورةً، وقورن مع الصورة، وقُرئت صفحات أسئلة المراجعة في نهاية الفصول بصرياً للتقاط علامات ✓ والتظليل الأصفر التي تحدد إجابات الكتاب. الملفات الممسوحة بخط اليد (F19، ملخص وائل) قُرئت بصرياً بالكامل.</p>
<h3>سجل المصادر</h3>{ledger}
<h3>خريطة الفصول</h3>{chmap}
<h3>التكرار والتحقق</h3>
<p>حُسبت بصمة MD5 لكل ملف قبل العدّ؛ النسخ المتطابقة والنسخ التابعة (PDF لنفس الأسئلة، ملف الأسئلة مع صور إجاباته) عُدّت مصدراً واحداً. <b>التكرار</b> = عدد المصادر المستقلة التي وردت فيها فكرة السؤال (F17، F19، S24، F24، الكتاب، ملخص عماد، ملخص عاصم) لا عدد الملفات. كل إجابة تُحقق منها من نص الكتاب بصفحته؛ حين يخالف مصدرٌ الكتاب يُعرض جواب الكتاب مع سطر «مصدر آخر» أحمر يبيّن الخلاف. حين يتعارض نص الفصل مع مفتاح مراجعته (حالة واحدة: عقود الترخيص/التصنيع ص206 و223) عُرض الاثنان مع تحذير.</p>
<p><b>التحقق المتقاطع مع ملخص عاصم:</b> يحلّ الملخص أسئلة صح/خطأ للكتاب في عشرة فصول (الفصل الثاني غير محلول فيه). قورنت 60 عبارة صح/خطأ: <b>59 من 60</b> متطابقة مع مفتاح الكتاب؛ الخلاف الوحيد في الفصل الخامس (عبارة اختلاف الأدوات والتقنيات: الكتاب «خطأ» والملخص يرى أنها «صح») وهو معروض عند السؤال. أما أسئلة الخيارات المتعددة فلا يظهر اختيار الملخص فيها في النص المستخرج فلم تُقارَن.</p>
<h3>إعادة بناء أسئلة الامتحانات</h3>
<p>الأسئلة التي نقلها الطلاب بصيغة حرة وكان واضحاً أنها اختيار من متعدد أُعيد بناؤها بخيارات من مصطلحات الفصل نفسه، مع وسم «خيارات معاد بناؤها» وإبقاء نص الطالب الأصلي أسفل السؤال. عدد الأسئلة المعاد بناؤها: <b>{recon}</b>. الأسئلة التي يخالف مفهومها الكتاب الحالي (أسئلة منهاج أقدم) أُبقيت مع سطرَي «يقول الكتاب» و«⚠ ثقة منخفضة».</p>
<h3>تدقيق التغطية والأسئلة المولَّدة</h3>
<p>قُسّمت الفصول الأحد عشر إلى <b>{total_subs}</b> فقرة فرعية وفق فهرس الكتاب (المستوى الأدنى في كل فصل). بعد التجميع والحذف أُعيد التدقيق آلياً: <b>{total_subs - gen} فقرة</b> غطّتها أسئلة حقيقية، و<b>{gen} فقرات</b> لم يسألها أي مصدر فكُتب لكل منها سؤال واحد من نص الكتاب (القسم الرابع في كل فصل). التغطية النهائية: <b>{total_subs} من {total_subs}</b>. تحقق آلي من عدم تكرار أي فكرة بين المولَّد والحقيقي (كل مولَّد يغطي فقرة لا سؤال فيها). لم تُطرح مسألة الحجم على المستخدم لأن المولَّد ({gen}) أقل من ثلث البنك ومن عدد الأسئلة الحقيقية في كل فصل.</p>
<h3>مجالات التركيز ودرجة الأهمية</h3>
<p>لكل فقرة عُدّت الأسئلة المميزة بحسب الأصل (امتحان / كتاب / أخرى) ورُتّبت الفقرات بعدد أسئلة الامتحان ثم المجموع. <b>مجال التركيز</b> في كل فصل = الفقرات التي سألها امتحانان أو أكثر، وإن قلّت عن اثنتين أُخذت أعلى فقرتين سألهما امتحان واحد على الأقل. الدرجة (1–5): الأساس من عدد مصادر الامتحان المستقلة (0 ← 1، 1 ← 2، 2 ← 3، 3 فأكثر ← 4)، زائد 1 إن كان السؤال أيضاً من أسئلة الكتاب، زائد 1 إن كانت فقرته مجال تركيز، والحد الأقصى 5؛ المولَّد يثبت على 1. الدرجة معونة للدراسة لا توقّع للامتحان.</p>
<table class="tbl"><thead><tr><th>الفصل</th><th>الفقرة</th><th>الاسم</th><th>امتحان</th><th>كتاب</th><th>أخرى</th><th>المجموع</th></tr></thead><tbody>{ft}</tbody></table>
<h3>الثقة المنخفضة</h3>
<p>أُضيف سطر «⚠ ثقة منخفضة» إلى <b>{len(lowc)}</b> سؤالاً فقط: حيث نُقل السؤال من الذاكرة بصيغة قد تعني أمرين، أو اختلفت المصادر، أو استند الجواب إلى جملة عابرة أو إلى منهاج أقدم لا إلى نص الكتاب. غياب السطر يعني تحققاً عادياً.</p>
<h3>أسئلة لم يمكن حسمها</h3>
<ul>
<li>F19 س6 وس7: محددات بورتر للميزة التنافسية للأمم ونظرية داننغ للاستثمار الأجنبي المباشر — لا تردان في الكتاب الحالي (منهاج أقدم).</li>
<li>F19 س23: «لا تعتبر من الصفقات المتكافئة» — الكتاب الحالي لا يعدّد أنواع الصفقات المتكافئة، والخيار المعلَّم غير مقروء بوضوح.</li>
<li>F17 س3: «بناء قاعة مؤتمرات شكل من أشكال؟ عقود تسليم المفتاح» — عقود تسليم المفتاح ليست ضمن الاتفاقيات التعاقدية في الكتاب الحالي.</li>
<li>F17 س20: خطأ الإسقاط في غربلة الأفكار — الفصل الثامن خارج النطاق المطلوب.</li>
</ul>
<h3>ترتيب الأولويات عند التعارض</h3>
<p>اتُّبع الترتيب: دقة المرجع ← أمانة الصياغة ← الإيجاز ← الشكل. تجاوز بعض كتل الإجابة حدَّ 80 كلمة كان مقصوداً في الأسئلة المقالية وحيث لزم سطر «يقول الكتاب» أو «مصدر آخر» أو إعادة بناء الخيارات، وفق البند 0أ من المواصفة.</p>
<h3>الخصوصية وحقوق المادة</h3>
<p>إخفاء الإجابات معونة للمذاكرة وليس حمايةً: نص الإجابات موجود داخل الملف ويمكن الوصول إليه بالبحث أو النسخ أو أدوات الوصول أو عرض المصدر، فلا يُعتمد عليه في امتحان حقيقي. لا يحوي الملف أي بيانات شخصية عن المؤلف أو الجهاز. نصوص الكتاب وأسئلة الامتحانات المقتبسة هنا تبقى ملكاً لمؤلفيها والجامعة، وعلى القارئ احترام حقوقها عند مشاركة الملف.</p>
<h3>إصدار المواصفة</h3>
<p>بُني بنك الأسئلة وتُحقق منه بالمواصفة v0.4، ثم أُعيد تصيير هذا الملف بالمواصفة v0.9 دون تغيير في الأسئلة أو الإجابات أو الدرجات؛ ما أُضيف هو ملحق «ملفات المصدر» وأرقام المصادر عند كل سؤال (البند 11د)، وإشعار الترخيص (البند 19)، وزر إعادة ضبط التصفية وملخص الفلاتر الفعّالة (البند 13أ).</p>
</section>"""

def sources_appendix():
    s = FILES_SUMMARY
    rows = "".join(f'<tr id="src-{n}"><td>{n}</td><td class="fn">{esc(path)}</td><td>{esc(kind)}</td><td>{esc(role)}</td><td class="ltr">{esc(grp)}</td><td>{esc(pages)}</td><td>{esc(note)}</td></tr>' for n, path, kind, role, grp, pages, note in FILES)
    return f"""<section id="sources"><h2>ملفات المصدر</h2>
<p>كل ملف وُجد في مجلد المادة مذكور هنا، بما فيها المستبعد والمكرر، ليعرف القارئ ممّ بُنيت المراجعة وما ينقصها. رقم كل ملف هو الرقم الذي يظهر عند كل سؤال في سطر «المصادر». أسماء الملفات كما وُردت؛ المادة نفسها غير منشورة مع المراجعة.</p>
<p class="meta">{s["files"]} ملفاً · {s["sources"]} مصادر مستقلة استُخدمت للأسئلة (الكتاب، F17، F19، S24، F24، ملخص عماد، ملخص عاصم) · {s["excluded"]} ملفاً مستبعداً · {s["duplicates"]} نسخ مكررة أو تابعة · {s["images"]} صورة فُحصت بصرياً.</p>
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
(function(){
var root=document.documentElement;
var modeBtns=document.querySelectorAll('[data-mode]'),impSl=document.getElementById('imp'),freqSl=document.getElementById('freq'),impV=document.getElementById('impv'),freqV=document.getElementById('freqv');
var chSel=document.getElementById('chsel'),search=document.getElementById('search'),counter=document.getElementById('counter');
var state={mode:'all',imp:1,freq:0,ch:'all',q:''};
function clampI(v,lo,hi){v=parseInt(v);return isNaN(v)?lo:Math.min(hi,Math.max(lo,v));}
try{var saved=JSON.parse(localStorage.getItem('imt_review_state')||'{}');if(saved.mode)state.mode=saved.mode;if(saved.imp!=null)state.imp=clampI(saved.imp,1,5);if(saved.freq!=null)state.freq=clampI(saved.freq,0,5);if(saved.ch)state.ch=saved.ch;}catch(e){}
var h=location.hash.replace('#','');if(/^mode=/.test(h)){h.split('&').forEach(function(kv){var p=kv.split('=');if(p[0]==='mode')state.mode=p[1];if(p[0]==='imp')state.imp=clampI(p[1],1,5);if(p[0]==='freq')state.freq=clampI(p[1],0,5);if(p[0]==='ch')state.ch=p[1];});}
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
 try{localStorage.setItem('imt_review_state',JSON.stringify({mode:state.mode,imp:state.imp,freq:state.freq,ch:state.ch}));}catch(e){}
 var frag='mode='+state.mode+'&imp='+state.imp+'&freq='+state.freq+'&ch='+state.ch;
 if(location.hash.replace('#','')!==frag&&!/^Q\\d\\d-\\d\\d\\d$/.test(location.hash.replace('#',''))){history.replaceState(null,'','#'+frag);}
}
var tb=document.querySelector('.toolbar'),ftog=document.getElementById('ftog'),fbadge=document.getElementById('fbadge'),fsum=document.getElementById('fsum');
modeBtns.forEach(function(b){b.addEventListener('click',function(){state.mode=b.getAttribute('data-mode');apply(true);});});
impSl.addEventListener('input',function(){state.imp=clampI(impSl.value,1,5);apply(true);});
freqSl.addEventListener('input',function(){state.freq=clampI(freqSl.value,0,5);apply(true);});
chSel.addEventListener('change',function(){state.ch=chSel.value;apply(true);});
var t;search.addEventListener('input',function(){clearTimeout(t);t=setTimeout(function(){state.q=search.value;apply(!!state.q);},150);});
document.getElementById('reset').addEventListener('click',function(){state={mode:'all',imp:1,freq:0,ch:'all',q:''};search.value='';apply(false);});
document.getElementById('expand').addEventListener('click',function(){document.querySelectorAll('article.q:not(.hidden) details.ans').forEach(function(d){d.open=true;});});
document.getElementById('collapse').addEventListener('click',function(){document.querySelectorAll('details.ans').forEach(function(d){d.open=false;});});
function setFilters(open){tb.classList.toggle('fclosed',!open);ftog.setAttribute('aria-expanded',open?'true':'false');try{localStorage.setItem('imt_filters_open',open?'1':'0');}catch(e){}}
(function(){var v=null;try{v=localStorage.getItem('imt_filters_open');}catch(e){}if(v===null)v=window.matchMedia('(max-width:760px)').matches?'0':'1';setFilters(v==='1');})();
ftog.addEventListener('click',function(){setFilters(tb.classList.contains('fclosed'));apply(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&window.matchMedia('(max-width:760px)').matches&&!tb.classList.contains('fclosed')){setFilters(false);apply(false);}});
var chOpen={};try{chOpen=JSON.parse(localStorage.getItem('imt_ch_open')||'{}');}catch(e){}
function saveCh(){try{localStorage.setItem('imt_ch_open',JSON.stringify(chOpen));}catch(e){}}
document.querySelectorAll('section.chapter').forEach(function(s){var id=s.id,d=s.querySelector('details.chd');if(chOpen[id]===false)d.open=false;
 d.addEventListener('toggle',function(){chOpen[id]=d.open;saveCh();});});
function setAll(sel,open){document.querySelectorAll(sel).forEach(function(d){d.open=open;});}
document.getElementById('foldch').addEventListener('click',function(){setAll('details.chd',false);});
document.getElementById('opench').addEventListener('click',function(){setAll('details.chd',true);});
document.getElementById('foldsec').addEventListener('click',function(){setAll('details.secd',false);});
document.getElementById('opensec').addEventListener('click',function(){setAll('details.secd',true);});
window.addEventListener('hashchange',function(){var el=document.getElementById(location.hash.slice(1));if(el){var p=el;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}el.scrollIntoView();}});
var theme=document.getElementById('theme');
function setTheme(v){if(v)root.setAttribute('data-theme',v);else root.removeAttribute('data-theme');try{localStorage.setItem('imt_theme',v||'');}catch(e){}theme.textContent=v==='dark'?'☀ فاتح':v==='light'?'🌙 داكن':'◐ المظهر';}
try{setTheme(localStorage.getItem('imt_theme')||'');}catch(e){}
theme.addEventListener('click',function(){var cur=root.getAttribute('data-theme');var dark=cur?cur==='dark':window.matchMedia('(prefers-color-scheme: dark)').matches;setTheme(dark?'light':'dark');});
window.addEventListener('beforeprint',function(){document.querySelectorAll('details').forEach(function(d){d.open=true;});});
document.querySelectorAll('#toc a').forEach(function(a){a.addEventListener('click',function(){var el=document.getElementById(a.getAttribute('href').slice(1));if(el){el.querySelectorAll('details.chd').forEach(function(d){d.open=true;});}});});
apply(false);
})();
"""

def build():
    c = counts(); total = len(QS)
    gen = c["generated"]; total_subs = sum(len(v) for v in SUBS.values())
    ch_opts = "".join(f'<option value="{n}">الفصل {n}</option>' for n in CHAPTERS)
    parts = [f'<title>{esc(TITLE)} — v{esc(VER)}</title><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><script>document.documentElement.className+=" js";</script><style>{CSS}</style>',
      '<main>',
      f'<header class="cover"><h1>{esc(TITLE)}</h1><p class="sub">التسويق والتجارة الدولية — International Marketing and Trading · ماجستير إدارة الأعمال</p>'
      f'<p class="meta">الإصدار v{esc(VER)} · الفصول: 1، 2، 3، 4، 5، 6، 7، 9، 10، 11، 12 · {total} سؤالاً · أسئلة الامتحانات {c["exam"]} · أسئلة الكتاب {c["textbook"]} · مصادر أخرى {c["other"]} · مولَّدة {gen}</p></header>',
      '<div class="toolbar noprint" role="toolbar" aria-label="أدوات القراءة">'
      '<div class="bar">'
      '<span class="counter" id="counter"></span><span class="fsum" id="fsum" aria-live="polite"></span>'
      '<button class="chip ftog" id="ftog" aria-expanded="true" aria-controls="filters">⚙ الفلاتر <span class="fbadge" id="fbadge" hidden></span></button>'
      '<input id="search" type="search" placeholder="ابحث في الأسئلة والإجابات…" aria-label="بحث" class="jsonly">'
      '</div>'
      '<div class="filters" id="filters">'
      '<div class="grp" role="group" aria-label="نوع الأسئلة"><button class="chip on" data-mode="all">الكل</button><button class="chip" data-mode="exam">الامتحانات</button><button class="chip" data-mode="textbook">الكتاب</button><button class="chip" data-mode="other">مصادر أخرى</button><button class="chip" data-mode="generated">مولَّدة</button></div>'
      '<div class="grp sliders" aria-label="التصفية"><label class="sl">الأهمية <span id="impv">الكل</span><input id="imp" type="range" min="1" max="5" step="1" value="1" aria-label="الحد الأدنى للأهمية"></label>'
      '<label class="sl">التكرار <span id="freqv">الكل</span><input id="freq" type="range" min="0" max="5" step="1" value="0" aria-label="الحد الأدنى للتكرار"></label></div>'
      f'<select id="chsel" aria-label="الفصل" class="jsonly"><option value="all">كل الفصول</option>{ch_opts}</select>'
      '<div class="grp jsonly"><button class="chip" id="expand">إظهار الإجابات</button><button class="chip" id="collapse">إخفاء الإجابات</button><button class="chip" id="foldch">طيّ كل الفصول</button><button class="chip" id="opench">فتح كل الفصول</button><button class="chip" id="foldsec">طيّ الأنواع</button><button class="chip" id="opensec">فتح الأنواع</button><button class="chip" id="theme">◐ المظهر</button><button class="chip" id="reset">↺ إعادة ضبط التصفية</button></div>'
      '</div></div>',
      f'''<section id="howto"><h2>كيف تستخدم هذا الملف</h2>
<p>كل سؤال يحمل ثلاث علامات: <b>التكرار</b> = عدد المصادر المستقلة التي سألته (امتحانات F17 وF19 وS24 وF24، الكتاب، الملخصات)؛ <b>الأهمية ★</b> من 1 إلى 5 مبنية على عدد امتحانات ورد فيها السؤال، زائد نقطة إن كان من أسئلة الكتاب، زائد نقطة إن كانت فقرته من مجالات تركيز المدرّس، وهي معونة للدراسة لا توقّع للامتحان؛ <b>⚠ ثقة منخفضة</b> يظهر فقط حيث يستند الجواب إلى دليل ضعيف أو نقل غير مؤكد، وغيابه يعني أن الإجابة تُحقق منها من الكتاب بالصفحة.</p>
<p>الإجابة مخفية خلف زر «إظهار الإجابة» ولا تحتاج جافاسكربت. الشريط الثابت في الأعلى يعرض العدّاد وزر «⚙ الفلاتر» والبحث؛ وخلف زر الفلاتر: وضع القراءة (نوع واحد من الأسئلة عبر كل الفصول: الامتحانات، الكتاب، مصادر أخرى، مولَّدة)، ومنزلقان لحدّ أدنى للأهمية (1–5) وللتكرار (0–5)، واختيار فصل، وإظهار الإجابات أو إخفائها، وطيّ كل الفصول أو فتحها، وطيّ أنواع الأسئلة أو فتحها، مستقلةً عن حالة الإجابات (ويمكن طيّ أي فصل أو نوع منفرداً بالنقر على عنوانه، ويُحفظ ما طويته)، والمظهر الفاتح أو الداكن، وزر «إعادة ضبط التصفية». اختياراتك تُحفظ وتوضع في رابط الصفحة. على الهاتف تبدأ لوحة الفلاتر مطوية، وحين تكون مطوية وثمة تصفية فعّالة يظهر عددها على الزر وملخصها بجانب العدّاد. تنبيه: الأسئلة المولَّدة أهميتها 1 دائماً، فرفع منزلق الأهمية إلى 2 أو أكثر يخفيها كلها. الترتيب المقترح: أسئلة الامتحانات أولاً ثم أسئلة الكتاب ثم الباقي. الطباعة تُظهر كل الإجابات وتتجاهل التصفية.</p>
<p class="meta">إخفاء الإجابات معونة للمذاكرة وليس حمايةً: نص الإجابة موجود في الملف ويصل إليه البحث والنسخ وعرض المصدر، فلا يُعتمد عليه في امتحان حقيقي. نصوص الكتاب والامتحانات المقتبسة تبقى ملكاً لأصحابها.</p>
<p class="pledge">شروط رخصة هذا الملف (CC BY-NC-SA 4.0): شارك هذا الملف مجاناً مع زملائك في المادة. أبقِ الإشعار الموجود في آخر الملف حتى يجد غيرك المصدر وأحدث إصدار. لا يجوز بيعه ولا وضعه خلف اشتراك أو جدار دفع.</p></section>''',
      f'''<section id="scope"><h2>النطاق والمصادر</h2>
<p>المرجع الحاكم هو كتاب المقرر (MBA-International Marketing and Trading-The Book.pdf، 423 صفحة). النطاق: الفصول 1–7 و9–12 ({total_subs} فقرة فرعية). أُدرجت أسئلة أربع دورات امتحانية منقولة من الذاكرة (F17، F19، S24، F24) وأسئلة مراجعة الكتاب في نهاية كل فصل، وأسئلة ملخص عماد جبور التي يوجد مفهومها في الكتاب، مع تحقق متقاطع من ملخص عاصم. استُبعدت الملفات التي تخص منهاجاً أقدم أو مقرراً آخر. التفاصيل في قسم المنهجية.</p>
<table class="tbl"><thead><tr><th>القسم</th><th>العدد</th><th>ما هو</th></tr></thead><tbody>
<tr><td>أسئلة الامتحانات</td><td>{c["exam"]}</td><td>{esc(SEC_INTRO["exam"])}</td></tr>
<tr><td>أسئلة الكتاب</td><td>{c["textbook"]}</td><td>{esc(SEC_INTRO["textbook"])}</td></tr>
<tr><td>مصادر أخرى</td><td>{c["other"]}</td><td>{esc(SEC_INTRO["other"])}</td></tr>
<tr><td>مولَّدة</td><td>{gen}</td><td>{esc(SEC_INTRO["generated"])}</td></tr></tbody></table>
<p class="meta">سؤال واحد قد يكون من الامتحانات ومن الكتاب معاً فيُحسب في القسمين ويظهر في وضعَي القراءة، لكنه يُعرض مرة واحدة (في قسم الامتحانات) مع وسم النوعين.</p></section>''']
    for n in CHAPTERS: parts.append(render_chapter(n))
    parts.append(methodology()); parts.append(sources_appendix()); parts.append(ref_lists()); parts.append(toc())
    parts.append(f'<footer id="metadata"><h2>بيانات الملف</h2><p>{esc(TITLE)} · ملف المراجعة الإصدار v{esc(VER)} (Review file v{esc(VER)}) · أُنشئ من المواصفة {esc(SPEC)} (Generated from prompt {esc(SPEC)}) · تاريخ الإنشاء {TODAY} · ملف البنك المرافق: {esc(TITLE)}_v{esc(VER)}_bank.json · {total} سؤالاً في 11 فصلاً · {total_subs} فقرة مغطاة من {total_subs}. لا يحوي الملف بيانات شخصية. ملف HTML واحد مستقل بلا موارد خارجية.</p>'
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
