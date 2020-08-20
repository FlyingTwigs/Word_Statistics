import pytest
from unittest import mock
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
    

def test_score(tmp_path):
    s = score.evaluation(CONTENT)
    assert s['general'] is not None
    assert s['writing'] is not None
    assert s['lexical'] is not None
    assert s['readability'] is not None
    assert s['general']['language'] is not None
    assert s['readability']['flesch_reading_grade_consensus'] is not None
    assert s['lexical']['wordfrequency_all'] is not None
    assert s['writing']['top_8_named_entity'] is not None
