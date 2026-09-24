# -*- coding: utf-8 -*-
"""Shared helpers for the question bank.
types: exam | textbook | other | generated
qtype: mcq | tf | short | essay
sources codes: F17 F19 S24 F24 F25 EMAD ASEM BOOK GEN
exam_sources: subset of F17 F19 S24 F24 F25
table / ans_table / calc: prompt v0.11 §7d (ported from the PRM tooling in IMT v1.6)
"""
LETTERS = ["أ", "ب", "ج", "د", "هـ", "و"]

def Q(id, ch, sub, types, qtype, stem, ans, why, remember, pages,
      options=None, distractors=None, sources=(), exam_sources=(),
      reconstructed=False, original=None, variants=(), book_says=None,
      other_source=None, sci=None, low_conf=None, notes=None, subname=None,
      table=None, calc=None, ans_table=None):
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
                book_says=book_says, other_source=other_source, sci=sci, low_conf=low_conf, notes=notes,
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
