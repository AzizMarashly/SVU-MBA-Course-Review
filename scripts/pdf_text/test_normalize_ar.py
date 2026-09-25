# -*- coding: utf-8 -*-
"""Unit tests for the plain-text parts of normalize_ar (run: set PYTHONUTF8=1 && python -m pytest scripts/pdf_text)."""
import normalize_ar as N

def test_prm_fix_only_handles_article_case():
    assert N.prm_fix("اإلجابات") == "الإجابات"
    assert N.prm_fix("األول") == "الأول"
    assert N.prm_fix("مالحظة") == "مالحظة"      # the PRM fix cannot repair this (ambiguous with genuine ال)

def test_clean_digits_and_nfkc():
    assert N.clean("٢٠٢٠") == "2020"
    assert N.clean("\ufefbم") == "لام"          # presentation-form lam-alef
    assert N.clean("حصـــر") == "حصر"

def test_naive_fix_inside_word():
    assert N.naive_fix("بأل") == "بلأ"
