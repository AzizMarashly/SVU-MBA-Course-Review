# -*- coding: utf-8 -*-
"""Shared helpers for the MIS question bank (record model, prompt v0.10 §5/§7).
types: exam | textbook | other | generated   (derived from sources by build_bank.py)
qtype: mcq | tf | short | essay
source codes (see SOURCES.md): BOOK S25 R44 F24 ASM OQ1 OQ2 OQ3 OQ4 OQ5 GEN
exam_sources: subset of {S25, R44, F24}
legacy_id: the v0.2 record id(s) this record replaces (e.g. "C1-01" or "C1-05+O1-03"), None for a new record.
raw: the raw source-item ids (extracted/questions/*.json "raw_id", e.g. "asem#58") the record was built from;
     "id@n" marks sub-question n of a raw item used by several records (prompt idea I-11). Optional; build_bank.py
     fails when one raw id is used by two records and lists the records that do not declare it yet.
"""
LETTERS = ["أ", "ب", "ج", "د", "هـ", "و"]

def Q(id, ch, sub, types, qtype, stem, ans, why, remember, pages,
      options=None, distractors=None, sources=(), exam_sources=(),
      reconstructed=False, original=None, variants=(), book_says=None,
      other_source=None, sci=None, low_conf=None, notes=None, subname=None,
      legacy_id=None, table=None, calc=None, ans_table=None, raw=()):
    """table / ans_table: T(...) — data table shown after the stem / inside the answer block (§7d).
    calc: C(...) — structured calculation: given values, then steps المعادلة → التعويض → الناتج (§7d)."""
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
                book_says=book_says, other_source=other_source, sci=sci, low_conf=low_conf, notes=notes, legacy_id=legacy_id, raw=list(raw),
                table=_check_table(table, id), calc=_check_calc(calc, id), ans_table=_check_table(ans_table, id))

def T(head, rows, caption=None, ltr=True):
    """A data table. head: column titles; rows: equal-length lists (numbers or short text).
    ltr=True: cells are codes/numbers rendered left-to-right (activity codes, amounts); Arabic-text tables pass ltr=False."""
    return dict(head=list(head), rows=[list(r) for r in rows], caption=caption, ltr=ltr)

def S(what, eq, sub, res, note=None):
    """One calculation step: what = the quantity found (e.g. 'SPI'), eq = the formula in symbols,
    sub = the same formula with the numbers put in (التعويض), res = the result with its unit,
    note = where a number came from when it is not obvious (optional)."""
    return dict(what=what, eq=eq, sub=sub, res=res, note=note)

def C(steps, given=(), note=None):
    """A structured calculation: given = 'symbol = value (origin)' strings, steps = [S(...)], note = one closing clause."""
    return dict(given=list(given), steps=list(steps), note=note)

def _check_table(t, id):
    if t is None: return None
    assert set(t) == {"head", "rows", "caption", "ltr"}, (id, "table must come from T()")
    n = len(t["head"]); assert n >= 2, (id, "table needs 2+ columns")
    for r in t["rows"]:
        assert len(r) == n, (id, "table row length", r)
    for r in [t["head"]] + t["rows"]:
        assert all("**" not in str(c) for c in r), (id, "no bold inside tables")
    return t

def _check_calc(c, id):
    if c is None: return None
    assert set(c) == {"given", "steps", "note"} and c["steps"], (id, "calc must come from C() with 1+ steps")
    for st in c["steps"]:
        assert set(st) == {"what", "eq", "sub", "res", "note"} and st["eq"] and st["sub"] and st["res"], (id, "step must come from S()", st)
        assert "**" not in st["eq"] + st["sub"] + st["res"], (id, "no bold inside calc cells")
    return c
