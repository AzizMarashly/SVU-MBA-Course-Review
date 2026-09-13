# -*- coding: utf-8 -*-
"""DOCX -> base.pdf via Word, updating the TOC and forcing Heading-4 collapse state."""
import os, sys, win32com.client as w
HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = 'مراجعه كامله لماده ال MIS'

def run(docx_name=None, pdf_name='base.pdf', collapse=True):
    src = os.path.join(HERE, docx_name or (TITLE + '.docx'))
    dst = os.path.join(HERE, pdf_name)
    app = w.Dispatch('Word.Application'); app.Visible = False; app.DisplayAlerts = 0
    doc = app.Documents.Open(src)
    try:
        doc.Fields.Update()
        for toc in doc.TablesOfContents:
            toc.Update()
        n_col = 0
        if collapse:
            for p in doc.Paragraphs:
                try:
                    if p.OutlineLevel == 4:          # wdOutlineLevel4 -> our answer headings
                        p.CollapsedState = True
                        n_col += 1
                except Exception:
                    pass
        doc.Repaginate()
        pages = doc.ComputeStatistics(2)
        doc.SaveAs2(src)
        doc.ExportAsFixedFormat(OutputFileName=dst, ExportFormat=17, OpenAfterExport=False,
                                OptimizeFor=0, DocStructureTags=True, CreateBookmarks=1)
    finally:
        doc.Close(SaveChanges=0); app.Quit()
    print('pages: %d   collapsed headings set: %d   -> %s' % (pages, n_col, pdf_name))
    return pages

if __name__ == '__main__':
    run(*(sys.argv[1:3] or []))
