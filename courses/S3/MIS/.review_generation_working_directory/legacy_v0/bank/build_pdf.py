# -*- coding: utf-8 -*-
"""Turn base.pdf into a genuinely interactive, JavaScript-free review PDF.

Design (no JavaScript anywhere):
  * answer / explanation / reference are ordinary page content  -> always readable in dumb viewers
  * an opaque cover widget sits on top of each answer            -> hidden in the file's base state
  * a green Show button and a red Hide button per question       -> hidden in the file's base state
  * /OpenAction is a standard /Hide action with /H false that reveals every cover + Show button,
    so a capable viewer opens the document already in "test mode" with the answers covered.
  * Show  : Hide(H=true)[covers, show]  -> /Next Hide(H=false)[hide]
    Hide  : Hide(H=false)[covers, show] -> /Next Hide(H=true)[hide]
"""
import json, os, zlib, io
import pymupdf, pikepdf
from pikepdf import Name, Dictionary, Array, String
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = 'مراجعه كامله لماده ال MIS'
COL_SHOW, COL_HIDE = 0x1E7A33, 0xA31D1D
COL_TXT_ANS = 0x1E7A33
PAD_X, PAD_Y = 7.0, 2.6
COVER_X0, COVER_X1 = 44.0, 568.0

# ---------------------------------------------------------------- geometry
def geometry(src):
    doc = pymupdf.open(src)
    tags = json.load(open(os.path.join(HERE, 'tags.json'), encoding='utf-8'))
    # index green heading spans per page
    green = {}
    for pno, page in enumerate(doc):
        gs = []
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for s in l['spans']:
                    if s['color'] == COL_SHOW and 10.0 < s['size'] < 11.0:
                        gs.append(pymupdf.Rect(s['bbox']))
        green[pno] = gs
    geo = {}
    for tag in sorted(tags):
        hit_s = hit_e = None
        for pno, page in enumerate(doc):
            if hit_s is None:
                r = page.search_for('AS' + tag)
                if r: hit_s = (pno, r[0])
            if hit_e is None:
                r = page.search_for('AE' + tag)
                if r: hit_e = (pno, r[0])
            if hit_s and hit_e: break
        assert hit_s and hit_e, tag
        sp, sr = hit_s; ep, er = hit_e
        yc = (sr.y0 + sr.y1) / 2.0
        band = [g for g in green[sp] if abs((g.y0 + g.y1) / 2.0 - yc) < 5.0]
        assert band, 'no green heading span for tag ' + tag
        bb = band[0]
        for g in band[1:]: bb |= g
        btn = [bb.x0 - PAD_X, bb.y0 - PAD_Y, bb.x1 + PAD_X, bb.y1 + PAD_Y]
        covers = []
        if sp == ep:
            covers.append((sp, [COVER_X0, btn[3] + 1.0, COVER_X1, er.y1 + 6.5]))
        else:
            ph = doc[sp].rect.height
            covers.append((sp, [COVER_X0, btn[3] + 1.0, COVER_X1, ph - 40.0]))
            for mid in range(sp + 1, ep):
                covers.append((mid, [COVER_X0, 40.0, COVER_X1, doc[mid].rect.height - 40.0]))
            covers.append((ep, [COVER_X0, 40.0, COVER_X1, er.y1 + 6.5]))
        geo[tag] = {'page': sp, 'btn': [round(v, 2) for v in btn],
                    'covers': [(p, [round(v, 2) for v in r]) for p, r in covers],
                    'pages': list(range(sp, ep + 1))}
    doc.close()
    return geo

# ---------------------------------------------------------------- pdf pieces
def image_xobject(pdf, path, max_px=900):
    im = Image.open(path).convert('RGB')
    if im.width > max_px:
        im = im.resize((max_px, max(1, round(im.height * max_px / im.width))), Image.LANCZOS)
    st = pikepdf.Stream(pdf, zlib.compress(im.tobytes(), 9))
    st.Type = Name.XObject; st.Subtype = Name.Image
    st.Width = im.width; st.Height = im.height
    st.ColorSpace = Name.DeviceRGB; st.BitsPerComponent = 8
    st.Filter = Name.FlateDecode
    return st

def button_ap(pdf, w, h, img, iw, ih, bg, border):
    ix, iy = (w - iw) / 2.0, (h - ih) / 2.0
    ops = ('q\n%.3f %.3f %.3f rg 0 0 %.2f %.2f re f\n'
           '%.3f %.3f %.3f RG 0.7 w 0.35 0.35 %.2f %.2f re S\n'
           'q %.2f 0 0 %.2f %.2f %.2f cm /Cap Do Q\nQ\n'
           % (bg[0], bg[1], bg[2], w, h,
              border[0], border[1], border[2], w - 0.7, h - 0.7,
              iw, ih, ix, iy))
    ap = pikepdf.Stream(pdf, ops.encode('ascii'))
    ap.Type = Name.XObject; ap.Subtype = Name.Form
    ap.BBox = Array([0, 0, w, h])
    ap.Resources = Dictionary(XObject=Dictionary(Cap=img))
    return ap

def cover_ap(pdf, w, h):
    ops = 'q 1 1 1 rg 0 0 %.2f %.2f re f Q\n' % (w, h)
    ap = pikepdf.Stream(pdf, ops.encode('ascii'))
    ap.Type = Name.XObject; ap.Subtype = Name.Form
    ap.BBox = Array([0, 0, w, h]); ap.Resources = Dictionary()
    return ap

HIDDEN_PRINT = 6          # bit2 Hidden + bit3 Print
PUSHBUTTON = 1 << 16
READONLY = 1

def widget(pdf, page, rect, name, ap, ff, action=None):
    w = pdf.make_indirect(Dictionary(
        Type=Name.Annot, Subtype=Name.Widget, FT=Name.Btn, Ff=ff,
        T=String(name), Rect=Array([rect[0], rect[1], rect[2], rect[3]]),
        F=HIDDEN_PRINT, MK=Dictionary(), AP=Dictionary(N=ap), P=page.obj))
    if action is not None:
        w.A = action
    if '/Annots' not in page.obj:
        page.obj.Annots = pdf.make_indirect(Array([]))
    page.obj.Annots.append(w)
    return w

def hide_action(pdf, targets, show):
    return pdf.make_indirect(Dictionary(
        S=Name.Hide, H=(not show), T=Array([String(t) for t in targets])))

def build():
    src = os.path.join(HERE, 'base.pdf')
    geo = geometry(src)
    pdf = pikepdf.open(src)
    pages = list(pdf.pages)
    H = pages[0].MediaBox[3] - pages[0].MediaBox[1]

    caps = json.load(open(os.path.join(HERE, 'caps.json')))
    img_s = image_xobject(pdf, os.path.join(HERE, 'cap_show.png'))
    img_h = image_xobject(pdf, os.path.join(HERE, 'cap_hide.png'))

    fields = []
    ap_cache = {}
    n_cov = n_show = n_hide = 0
    for tag in sorted(geo):
        g = geo[tag]
        bx0, by0, bx1, by1 = g['btn']
        # PDF y axis is bottom-up; pymupdf gives top-down
        bw, bh = bx1 - bx0, by1 - by0
        rect_btn = [bx0, H - by1, bx1, H - by0]
        cov_names = []
        for i, (pno, r) in enumerate(g['covers']):
            cw, ch = r[2] - r[0], r[3] - r[1]
            if ch <= 0.5: continue
            key = (round(cw, 1), round(ch, 1))
            if key not in ap_cache: ap_cache[key] = cover_ap(pdf, cw, ch)
            nm = 'cov%s_%d' % (tag, i)
            widget(pdf, pages[pno], [r[0], H - r[3], r[2], H - r[1]], nm,
                   ap_cache[key], PUSHBUTTON | READONLY)
            cov_names.append(nm); fields.append(nm); n_cov += 1
        sname, hname = 'show' + tag, 'hide' + tag
        iw_s = caps['show']['w']; ih_s = caps['show']['h']
        iw_h = caps['hide']['w']; ih_h = caps['hide']['h']
        sc = min(1.0, (bw - 4) / iw_s, (bh - 1.5) / ih_s)
        ap_show = button_ap(pdf, bw, bh, img_s, iw_s * sc, ih_s * sc,
                            (0.918, 0.961, 0.929), (0.118, 0.478, 0.200))
        sc = min(1.0, (bw - 4) / iw_h, (bh - 1.5) / ih_h)
        ap_hide = button_ap(pdf, bw, bh, img_h, iw_h * sc, ih_h * sc,
                            (0.984, 0.918, 0.918), (0.639, 0.114, 0.114))
        a_show = hide_action(pdf, cov_names + [sname], show=False)
        a_show.Next = hide_action(pdf, [hname], show=True)
        a_hide = hide_action(pdf, cov_names + [sname], show=True)
        a_hide.Next = hide_action(pdf, [hname], show=False)
        widget(pdf, pages[g['page']], rect_btn, sname, ap_show, PUSHBUTTON, a_show)
        widget(pdf, pages[g['page']], rect_btn, hname, ap_hide, PUSHBUTTON, a_hide)
        fields += [sname, hname]; n_show += 1; n_hide += 1

    # AcroForm
    all_widgets = []
    for p in pdf.pages:
        if '/Annots' in p.obj:
            for a in p.obj.Annots:
                if a.get('/Subtype') == Name.Widget: all_widgets.append(a)
    pdf.Root.AcroForm = pdf.make_indirect(Dictionary(
        Fields=Array(all_widgets), NeedAppearances=False, DA=String('/Helv 0 Tf 0 g'),
        DR=Dictionary(Font=Dictionary())))

    # document open action: reveal every cover + every Show button ("test mode")
    reveal = [n for n in fields if not n.startswith('hide')]
    pdf.Root.OpenAction = hide_action(pdf, reveal, show=True)

    with pdf.open_metadata() as m:
        m['dc:title'] = TITLE
        m['dc:creator'] = []
    for k in ('/Author', '/Creator', '/Producer', '/Company', '/SourceModified'):
        if pdf.docinfo is not None and k in pdf.docinfo:
            del pdf.docinfo[k]
    pdf.docinfo['/Title'] = TITLE

    out = os.path.join(HERE, TITLE + '.pdf')
    pdf.save(out, linearize=False)
    print('covers : %d' % n_cov)
    print('show   : %d' % n_show)
    print('hide   : %d' % n_hide)
    print('fields : %d' % len(all_widgets))
    print('openaction targets: %d' % len(reveal))
    print('saved  :', out, os.path.getsize(out), 'bytes')
    json.dump(geo, open(os.path.join(HERE, 'geo.json'), 'w'))

if __name__ == '__main__':
    build()
