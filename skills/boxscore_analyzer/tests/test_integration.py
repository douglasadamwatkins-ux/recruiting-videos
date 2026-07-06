import pytest
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
