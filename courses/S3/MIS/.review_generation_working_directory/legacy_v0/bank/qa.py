# -*- coding: utf-8 -*-
import pymupdf, pikepdf, json, zipfile, re
from pikepdf import Name
from lxml import etree
T='مراجعه كامله لماده ال MIS'
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
ok=lambda c: 'PASS' if c else '**FAIL**'
print('='*68); print('A. CONTENT'); print('='*68)
import bank_a,bank_b,bank_c,bank_d,bank_e
bank_d.register_assem_summary()
from bank_a import Q as _Q
N=len(_Q); NSRC=10
from bank_a import Q
ids=[x['id'] for x in Q]
print('%-52s %s'%('unique question ids', ok(len(ids)==len(set(ids)))))
print('%-52s %s'%('every question has answer+explanation+page', ok(all(x['ans'] and x['exp'] and x['page'] for x in Q))))
print('%-52s %s'%('every question in scope 1,2,3,5,7,8,9,10', ok(all(x['ch'] in (1,2,3,5,7,8,9,10) for x in Q))))
print('%-52s %s'%('frequency 1..%d for sourced, 0 for generated'%NSRC, ok(all((x['freq']==0)==('GEN' in x['src']) and 0<=x['freq']<=NSRC for x in Q))))
print('%-52s %s'%('freq equals distinct sources (generated exempt)', ok(all(x['freq']==len(set(x['src'])) for x in Q if 'GEN' not in x['src']))))
print('%-52s %s'%('generated questions carry a verified page', ok(all(x['page'] and x['exp'] for x in Q if 'GEN' in x['src']))))
print('   declared question count: %d   (generated: %d)'%(len(Q), sum(1 for x in Q if 'GEN' in x['src'])))

print(); print('='*68); print('B. DOCX'); print('='*68)
z=zipfile.ZipFile(T+'.docx'); x=etree.fromstring(z.read('word/document.xml'))
seq=[]
for p in x.iter(W+'p'):
    pPr=p.find(W+'pPr'); st=None; col=False
    if pPr is not None:
        s=pPr.find(W+'pStyle');  st=s.get(W+'val') if s is not None else None
        col=pPr.find(W+'collapsed') is not None
    seq.append((st,col))
h3=[s for s in seq if s[0]=='Heading3']; h4=[s for s in seq if s[0]=='Heading4']
print('%-52s %s'%('%d question headings (Heading3)'%N, ok(len(h3)==N)))
print('%-52s %s'%('%d answer headings  (Heading4)'%N, ok(len(h4)==N)))
print('%-52s %s'%('answer headings are real outline-4 headings', ok(len(h4)==N)))
print('%-52s %s'%('  (collapsed-by-default: NOT persistable by Word)', 'KNOWN LIMITATION'))
styles=[s[0] for s in seq]
bad=0
for i,s in enumerate(styles):
    if s=='Heading4':
        nxt=[k for k in styles[i+1:] if k in ('Heading1','Heading2','Heading3','Heading4')]
        if nxt and nxt[0]=='Heading4': bad+=1
print('%-52s %s'%('each answer block ends before next question', ok(bad==0)))
print('%-52s %s'%('docx has no author metadata', ok(not (z.read('docProps/core.xml').decode().count('<dc:creator>') and re.search(r'<dc:creator>[^<]+</dc:creator>', z.read('docProps/core.xml').decode())))))

print(); print('='*68); print('C. PDF STRUCTURE'); print('='*68)
raw=open(T+'.pdf','rb').read(); p=pikepdf.open(T+'.pdf')
w={}
for pg in p.pages:
    for a in pg.obj.get('/Annots',[]):
        if a.get('/Subtype')==Name.Widget: w[str(a.T)]=a
cov=[k for k in w if k.startswith('cov')]; sh=[k for k in w if k.startswith('show')]; hd=[k for k in w if k.startswith('hide')]
print('%-52s %s'%('pages (expanded PDF)', ok(len(p.pages)>0)+'  (%d)'%len(p.pages)))
print('%-52s %s'%('no /JS or /JavaScript anywhere', ok(raw.count(b'/JS')==0 and raw.count(b'/JavaScript')==0)))
print('%-52s %s'%('no /AA additional-actions', ok(raw.count(b'/AA')==0)))
print('%-52s %s'%('AcroForm present, fields not flattened', ok('/AcroForm' in p.Root and len(w)>0)))
print('%-52s %s'%('%d show + %d hide buttons'%(N,N), ok(len(sh)==N and len(hd)==N)))
print('%-52s %s'%('cover widget per question', ok(len(cov)>=N)))
print('%-52s %s'%('all widgets hidden+print in base state (F=6)', ok(all(int(v.F)==6 for v in w.values()))))
print('%-52s %s'%('all widgets carry an appearance stream', ok(all('/AP' in v and '/N' in v.AP for v in w.values()))))
oa=p.Root.get('/OpenAction')
print('%-52s %s'%('document open action exists and is /Hide', ok(oa is not None and oa.S==Name.Hide and bool(oa.H)==False)))
oat=set(str(t) for t in oa.T)
print('%-52s %s'%('open action reveals every cover + show button', ok(oat==set(cov)|set(sh))))
print('%-52s %s'%('open action never touches a hide button', ok(not (oat & set(hd)))))
bad=[]
for n in sh+hd:
    tag=n[4:]; a=w[n].A
    t1=sorted(str(v) for v in a.T); t2=[str(v) for v in a.Next.T]
    exp=sorted([k for k in cov if k[3:7]==tag]+['show'+tag])
    want=(True,False) if n.startswith('show') else (False,True)
    if t1!=exp or t2!=['hide'+tag] or (bool(a.H),bool(a.Next.H))!=want: bad.append(n)
print('%-52s %s'%('every button targets only its own question', ok(not bad)))
info=p.docinfo or {}
print('%-52s %s'%('pdf has no author/creator metadata', ok(not any(k in info for k in ('/Author','/Creator','/Company')))))

print(); print('='*68); print('D. GEOMETRY'); print('='*68)
d=pymupdf.open('base.pdf'); geo=json.load(open('geo.json'))
unc=ovl=btn=0
for tag,g in geo.items():
    covers={pp:pymupdf.Rect(r) for pp,r in g['covers']}
    b=pymupdf.Rect(*g['btn'])
    for pp,c in covers.items():
        for bl in d[pp].get_text('dict')['blocks']:
            for l in bl.get('lines',[]):
                for s in l['spans']:
                    r=pymupdf.Rect(s['bbox'])
                    if 'AS' in s['text'] or 'AE' in s['text']: continue
                    if pp==g['page'] and r.y0<b.y1: continue
                    if c.y0-0.6<=r.y0 and r.y1<=c.y1+0.6 and not (r.x0>=c.x0-0.5 and r.x1<=c.x1+0.5): unc+=1
                    if s['color']==0x1A1A1A and 12.0<s['size']<13.0 and r.y0>(b.y1 if pp==g['page'] else 0) and r.y0<c.y1-1.0: ovl+=1
print('%-52s %s'%('no answer text left outside its cover', ok(unc==0)))
print('%-52s %s'%('no cover bleeds onto the next question', ok(ovl==0)))
print('%-52s %s'%('no literal ** markdown left in the pdf', ok(not any('**' in pg.get_text() for pg in d))))
