import os
import pytest
from pathlib import Path
from PIL import Image

from boxscore_analyzer import ocr, parser, stats


SAMPLE_TEXT = """GBG COLORADO 2029
LINEUP AB R H RBI BB SO
J Bradle #14 (CF) 3 0 0 0 0 0
J Farmer #17 (LF) 3 0 1 0 0 0
R Enochs #3 (SS) 3 0 2 0 0 0
E West #30 (3B) 3 0 0 0 0 0
C Davies #1 (1B) 2 0 0 0 0 0
J Holder #4 (RF) 2 0 1 0 0 0
P Martin #5 (C) 2 0 1 0 0 1
G Watkins #21 (DH) 2 0 2 0 0 0
C Carter #27 (LF) 1 0 0 0 0 1
L LaForest #15 1 0 0 0 0 1
B Gainey #11 (P) - - - - - -
C Sherp #22 (2B) 2 0 0 0 0 0
TEAM 24 0 7 0 0 3
TB: G Watkins 2, R Enochs 2, J Farmer 1, J Holder 1, P Martin 1
E: C Sherpa, E West, J Farmer
"""


def test_parser_on_sample_text():
    parsed = parser.parse_boxscore_text(SAMPLE_TEXT)
    assert isinstance(parsed, dict)
    assert "players" in parsed
    assert len(parsed["players"]) >= 5

    # Ensure roster matching preserves the number and full name when present.
    first_player = parsed["players"][0]
    assert first_player["number"] == 14
    assert first_player["full_name"] == "J Bradle"


def test_parser_full_name_matching():
    # Simulate a full roster line plus the shortened lineup reference.
    raw = """GBG COLORADO 2029
LINEUP AB R H RBI BB SO
J Bradle #14 (CF) 3 0 0 0 0 0
John Bradley #14 CF
"""
    parsed = parser.parse_boxscore_text(raw)
    assert parsed["players"][0]["number"] == 14
    assert parsed["players"][0]["full_name"] == "John Bradley"


def test_sample_text_fixture_parser():
    sample_path = Path(__file__).resolve().parents[1] / "samples" / "boxscore_sample_text.txt"
    assert sample_path.exists(), "Sample boxscore text fixture must exist"

    raw = sample_path.read_text()
    parsed = parser.parse_boxscore_text(raw)
    assert "players" in parsed
    assert parsed["players"][0]["full_name"] == "J Bradle"
    assert parsed["players"][0]["number"] == 14
    assert parsed["players"][1]["full_name"] == "Joseph Farmer"


def test_ocr_parser_integration(monkeypatch, tmp_path):
    # create a small blank image file to pass to ocr_image
    img_path = tmp_path / "sample.png"
    Image.new("RGB", (800, 600), color=(255, 255, 255)).save(img_path)

    # monkeypatch pytesseract to return our SAMPLE_TEXT regardless of image
    import pytesseract

    monkeypatch.setattr(pytesseract, "image_to_string", lambda img: SAMPLE_TEXT)

    raw = ocr.ocr_image(str(img_path))
    assert SAMPLE_TEXT in raw
    parsed = parser.parse_boxscore_text(raw)
    df = stats.basic_batting_stats(parsed.get("players", []))
    assert not df.empty
