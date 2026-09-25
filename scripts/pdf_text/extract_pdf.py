# -*- coding: utf-8 -*-
"""Extract an Arabic course PDF page by page (geometry-aware, fixes reversed lam-alef ligatures).
Usage:  set PYTHONUTF8=1 && python scripts/pdf_text/extract_pdf.py <book.pdf> <out_dir>
Writes out_dir/pNNN.txt (UTF-8, no BOM), out_dir/book.txt with "=== PAGE n ===" markers
(PRM extracted/FORMAT.md style) and out_dir/pages.json (method, chars, quality, needs_ocr, needs_vision).
STATUS: prototype from the 2026-09-25 evaluation, see README.md. Tested on ACM + PRM sample pages only."""
import os, sys, json, re
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import normalize_ar as N

SUSPECT = re.compile("ا[اأإآ]ل|[^\s\u0621-\u064A][أإآ]ل")   # reversed-ligature leftovers

def page_quality(txt):
    letters = len(re.findall("[\u0621-\u064A]", txt))
    words = len(txt.split())
    susp = len(SUSPECT.findall(txt))
    q = 1.0
    if letters < 80: q -= 0.5
    if words: q -= min(0.5, susp / max(words, 1) * 5)
    return round(max(q, 0), 2), letters, susp

def main(pdf, out):
    os.makedirs(out, exist_ok=True)
    doc = pymupdf.open(pdf)
    meta = []
    book = []
    for i, page in enumerate(doc, 1):
        txt = N.clean(N.mupdf_rtl(page))
        q, letters, susp = page_quality(txt)
        imgs = len(page.get_images())
        needs_ocr = letters < 80 and imgs > 0          # image page: no usable text layer
        needs_vision = needs_ocr                        # OCR engines tested were unusable; a helper reads the PNG
        if needs_ocr:
            page.get_pixmap(dpi=200).save(os.path.join(out, f"p{i:03d}.png"))
        with open(os.path.join(out, f"p{i:03d}.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        book.append(f"\n=== PAGE {i} ===\n{txt}\n")
        meta.append({"page": i, "method": "pymupdf-rawdict-rtl", "chars": len(txt), "arabic_letters": letters,
                     "suspect_patterns": susp, "images": imgs, "quality": q,
                     "needs_ocr": needs_ocr, "needs_vision": needs_vision})
    with open(os.path.join(out, "book.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.writelines(book)
    with open(os.path.join(out, "pages.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    flagged = [m["page"] for m in meta if m["needs_vision"]]
    print("pages", len(meta), "| flagged for vision/OCR:", len(flagged), flagged[:30])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
