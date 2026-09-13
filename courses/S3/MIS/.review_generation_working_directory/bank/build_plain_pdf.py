# -*- coding: utf-8 -*-
"""Build the clean, non-interactive PDF: answers simply printed, no form fields at all."""
import os, subprocess, sys
os.environ['MIS_PLAIN'] = '1'
import win32com.client as w
import pikepdf

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = 'مراجعه كامله لماده ال MIS'


def main():
    env = dict(os.environ, MIS_PLAIN='1', PYTHONIOENCODING='utf-8')
    subprocess.run([sys.executable, 'build_docx.py'], cwd=HERE, check=True, env=env)
    src = os.path.join(HERE, 'plain_' + TITLE + '.docx')
    raw = os.path.join(HERE, 'plain_raw.pdf')

    app = w.DispatchEx('Word.Application'); app.Visible = False; app.DisplayAlerts = 0
    doc = app.Documents.Open(src)
    try:
        doc.Fields.Update()
        for toc in doc.TablesOfContents:
            toc.Update()
        doc.Repaginate()
        pages = doc.ComputeStatistics(2)
        doc.Save()
        doc.ExportAsFixedFormat(OutputFileName=raw, ExportFormat=17, OpenAfterExport=False,
                                OptimizeFor=0, DocStructureTags=True, CreateBookmarks=1)
    finally:
        doc.Close(SaveChanges=0); app.Quit()

    # strip every trace of interactivity + all personal metadata
    pdf = pikepdf.open(raw)
    for k in ('/AcroForm', '/OpenAction', '/Names', '/JavaScript'):
        if k in pdf.Root:
            del pdf.Root[k]
    n_annots = 0
    for page in pdf.pages:
        if '/Annots' in page.obj:
            keep = [a for a in page.obj.Annots
                    if a.get('/Subtype') not in (pikepdf.Name.Widget,)]
            n_annots += len(page.obj.Annots) - len(keep)
            if keep:
                page.obj.Annots = pdf.make_indirect(pikepdf.Array(keep))
            else:
                del page.obj['/Annots']
        if '/AA' in page.obj:
            del page.obj['/AA']
    with pdf.open_metadata() as m:
        m['dc:title'] = TITLE
        m['dc:creator'] = []
    for k in ('/Author', '/Creator', '/Producer', '/Company', '/SourceModified',
              '/LastModifiedBy', '/Manager'):
        if pdf.docinfo is not None and k in pdf.docinfo:
            del pdf.docinfo[k]
    pdf.docinfo['/Title'] = TITLE
    out = os.path.join(HERE, TITLE + '.pdf')
    pdf.save(out, linearize=True)
    pdf.close()
    os.remove(raw)
    print('pages          :', pages)
    print('widgets removed:', n_annots)
    print('saved          :', out, os.path.getsize(out), 'bytes')


main()
