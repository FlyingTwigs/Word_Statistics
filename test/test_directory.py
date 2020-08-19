import pytest
import os
from lib.score import Score

CONTENT = "hello hello hello. test."
score = Score()

def test_text(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "testing.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert len(p.read_text().split()) == 4
    

""" 
def test_score(tmp_path):
    s = score.evaluation(p)
    assert s['general'] is not None
"""
    