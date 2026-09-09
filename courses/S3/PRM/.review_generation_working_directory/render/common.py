# -*- coding: utf-8 -*-
"""Shared helpers for the question bank.
types: exam | textbook | other | generated
qtype: mcq | tf | short | essay
sources codes: F17 F19 S24 F24 EMAD ASEM BOOK GEN
exam_sources: subset of F17 F19 S24 F24
"""
LETTERS = ["أ", "ب", "ج", "د", "هـ", "و"]

def Q(id, ch, sub, types, qtype, stem, ans, why, remember, pages,
      options=None, distractors=None, sources=(), exam_sources=(),
      reconstructed=False, original=None, variants=(), book_says=None,
      other_source=None, sci=None, low_conf=None, notes=None, subname=None):
    if qtype == "mcq":
        assert options and isinstance(ans, int) and 0 <= ans < len(options), id
    if qtype == "tf":
        assert ans in ("صح", "خطأ"), id
    types = list(types)
    if "generated" in types:
        assert sources == ("GEN",) or list(sources) == ["GEN"], id
    return dict(id=id, ch=ch, sub=sub, subname=subname, types=types, qtype=qtype, stem=stem.strip(),
                options=list(options) if options else None, ans=ans, why=why.strip(),
                remember=remember.strip(), distractors=(distractors or "").strip() or None,
                pages=list(pages), sources=list(sources), exam_sources=list(exam_sources),
                reconstructed=reconstructed, original=original, variants=list(variants),
                book_says=book_says, other_source=other_source, sci=sci, low_conf=low_conf, notes=notes)
