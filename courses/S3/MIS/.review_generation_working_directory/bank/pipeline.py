# -*- coding: utf-8 -*-
"""Full build: DOCX (collapsed) + base PDF (expanded) + interactive PDF."""
import os, shutil, subprocess, sys
import win32com.client as w
HERE=os.path.dirname(os.path.abspath(__file__)); TITLE='مراجعه كامله لماده ال MIS'

def word(path, collapse, pdf=None, update=True):
    app=w.Dispatch('Word.Application'); app.Visible=False; app.DisplayAlerts=0
    doc=app.Documents.Open(path); n=0
    try:
        if update:
            doc.Fields.Update()
            for toc in doc.TablesOfContents: toc.Update()
        for p in doc.Paragraphs:
            try:
                if p.OutlineLevel==4:
                    p.CollapsedState=bool(collapse); n+=1
            except Exception: pass
        doc.Repaginate(); pages=doc.ComputeStatistics(2)
        doc.Save()
        if pdf:
            doc.ExportAsFixedFormat(OutputFileName=pdf, ExportFormat=17, OpenAfterExport=False,
                                    OptimizeFor=0, DocStructureTags=True, CreateBookmarks=1)
    finally:
        doc.Close(SaveChanges=-1); app.Quit()
    return pages, n

def main():
    subprocess.run([sys.executable,'build_docx.py'],cwd=HERE,check=True)
    src=os.path.join(HERE,TITLE+'.docx')
    tmp=os.path.join(HERE,'for_pdf.docx'); shutil.copy(src,tmp)
    pages,n = word(tmp, collapse=False, pdf=os.path.join(HERE,'base.pdf'))
    print('PDF source  : %d pages, %d answer headings expanded' % (pages,n))
    pages,n = word(src, collapse=True)
    print('DOCX final  : %d pages when collapsed, %d answer headings collapsed' % (pages,n))
    os.remove(tmp)
    subprocess.run([sys.executable,'build_pdf.py'],cwd=HERE,check=True)

main()
