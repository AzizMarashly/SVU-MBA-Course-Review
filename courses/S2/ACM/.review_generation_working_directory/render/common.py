# -*- coding: utf-8 -*-
"""Shared helpers for the ACM question bank (record model, prompt v0.12 §5/§7).
types: exam | textbook | other | generated   (derived from sources by build_bank.py)
qtype: mcq | tf | short | essay
source codes (see SOURCES.md): BOOK S23 F23 S24 F24 S25 OLD SUM SOL345 GEN
exam_sources: subset of the exam sittings in ledger.json (S23 F23 S24 F24 S25 OLD)
raw: raw source-item ids (extracted/questions/*.json "raw_id", e.g. "exams#58"); "id@n" marks sub-question n of a raw item used by
     several records; a leading "~" marks a number-less credit (§5c) that may sit on several records. build_bank.py fails when one raw
     id is used by two records.

v0.12 additions:
  model_answer  full model answer for essay / list / process questions (§7b): 100–200 words, bold keywords, page of each point
                inline as «(ص N)». Rendered collapsed under the answer line. Required when qtype is "essay".
  fast          «Fast route» (§7e): a rule-based deduction in one or two sentences with the page it follows from; add «(مستنتج)» when the
                book does not state it in those words. Only where a rule of the book decides the item without the full calculation.
  see           ids of cross-linked cards of the same claim (§5a step 2: a book review item and a verbatim exam item keep their own
                cards, share frequency and importance). build_bank.py unions their sources for freq/importance.
  fig           F("cvp", ...) — a figure drawn by the build from the record's data (Appendix A.6). build_bank.py recomputes the
                break-even quantity from the data and fails when it differs from the record's `be_q`.
  unsolved      True for a book exercise the book leaves unsolved and this review solved (§7e): rendered with the label
                «حل مولَّد — ليس حلّ الكتاب»; frequency 1 (BOOK).
  method        on C(...): the key of the chapter's METHODS entry the steps follow (e.g. "M2"); every Step label links to it.
"""
LETTERS = ["أ", "ب", "ج", "د", "هـ", "و"]

def Q(id, ch, sub, types, qtype, stem, ans, why, remember, pages,
      options=None, distractors=None, sources=(), exam_sources=(),
      reconstructed=False, original=None, variants=(), book_says=None,
      other_source=None, sci=None, low_conf=None, notes=None, subname=None,
      table=None, calc=None, ans_table=None, raw=(), claim=None,
      model_answer=None, fast=None, see=(), fig=None, unsolved=False, also=()):
    """table / ans_table: T(...) — data table shown after the stem / inside the answer block (§7d).
    calc: C(...) — structured calculation: given values, then steps المعادلة → التعويض → الناتج (§7d).
    claim: one line — the book fact whose knowledge decides the answer (§5). Required on every record.
    also: «also asked as» lines (§5a): tuples (form, wording, key, sources) for folded forms."""
    if qtype == "mcq":
        assert options and isinstance(ans, int) and 0 <= ans < len(options), id
    if qtype == "tf":
        assert ans in ("صح", "خطأ"), id
    if qtype == "essay":
        assert model_answer, (id, "essay needs a full model answer (§7b)")
    types = list(types)
    if "generated" in types:
        assert sources == ("GEN",) or list(sources) == ["GEN"], id
    assert claim and len(claim) > 8, (id, "claim line required (§5)")
    return dict(id=id, ch=ch, sub=sub, subname=subname, types=types, qtype=qtype, stem=stem.strip(),
                options=list(options) if options else None, ans=ans, why=why.strip(),
                remember=remember.strip(), distractors=(distractors or "").strip() or None,
                pages=list(pages), sources=list(sources), exam_sources=list(exam_sources),
                reconstructed=reconstructed, original=original, variants=list(variants),
                book_says=book_says, other_source=other_source, sci=sci, low_conf=low_conf, notes=notes, raw=list(raw),
                claim=claim.strip(), model_answer=(model_answer or "").strip() or None, fast=(fast or "").strip() or None,
                see=list(see), fig=_check_fig(fig, id), unsolved=bool(unsolved),
                also=[dict(form=a[0], wording=a[1], key=a[2], sources=list(a[3])) for a in also],
                table=_check_table(table, id), calc=_check_calc(calc, id), ans_table=_check_table(ans_table, id))

def T(head, rows, caption=None, ltr=True):
    """A data table. head: column titles; rows: equal-length lists (numbers or short text).
    ltr=True: cells are codes/numbers rendered left-to-right (amounts); Arabic-text tables pass ltr=False."""
    return dict(head=list(head), rows=[list(r) for r in rows], caption=caption, ltr=ltr)

def S(what, eq, sub, res, note=None):
    """One calculation step: what = the quantity found (Arabic + symbol), eq = the formula in symbols only,
    sub = the same formula with the numbers put in (التعويض), res = the result with its unit, note = origin of a number (optional)."""
    return dict(what=what, eq=eq, sub=sub, res=res, note=note)

def C(steps, given=(), note=None, method=None):
    """A structured calculation: given = 'symbol = value (origin)' strings, steps = [S(...)], note = one closing clause,
    method = key of the chapter's METHODS entry these steps follow (§7e)."""
    return dict(given=list(given), steps=list(steps), note=note, method=method)

def F(kind, **data):
    """A figure drawn by the build from data (A.6). kind "cvp": price, var (variable cost per unit), fixed, be_q (the record's
    break-even quantity), optional cash_fixed (fixed costs without depreciation → shutdown point), qmax (x-axis range),
    highlight ("be" | "shutdown" | "safety" | "lines"), sales_q (actual sales for the margin of safety), alt (text alternative)."""
    d = dict(kind=kind); d.update(data); return d

def M(key, name, recognise, steps, page, fast=None):
    """One Methods-block entry (§7e): key "M1", name, how to recognise the type, ordered steps [(what, output)], book page, optional
    fast-route rule in words."""
    return dict(key=key, name=name, recognise=recognise, steps=[list(s) for s in steps], page=page, fast=fast)

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
    assert set(c) == {"given", "steps", "note", "method"} and c["steps"], (id, "calc must come from C() with 1+ steps")
    for st in c["steps"]:
        assert set(st) == {"what", "eq", "sub", "res", "note"} and st["eq"] and st["sub"] and st["res"], (id, "step must come from S()", st)
        assert "**" not in st["eq"] + st["sub"] + st["res"], (id, "no bold inside calc cells")
    return c

def _check_fig(f, id):
    if f is None: return None
    assert f.get("kind") == "cvp", (id, "only the cvp figure exists")
    for k in ("price", "var", "fixed", "be_q"):
        assert k in f, (id, "cvp figure needs", k)
    assert f["price"] > f["var"] > 0 and f["fixed"] > 0, (id, "cvp data")
    return f
