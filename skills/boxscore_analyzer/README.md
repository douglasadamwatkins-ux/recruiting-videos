# Boxscore Analyzer Skill

This skill extracts structured baseball statistics from photos of box scores.

Components:
- OCR: image -> raw text (using Tesseract)
- Parser: raw text -> structured box score (player rows, team totals)
- Stats: compute general and advanced metrics (AVG, OBP, SLG, OPS, wOBA, wRC+, etc.)
- CLI: process images and output CSV/JSON summaries

Quick start (local prototype):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m boxscore_analyzer.cli path/to/boxscore.jpg
```

Notes:
- For production, consider using a commercial OCR API (Google/Cloud Vision) for higher accuracy.
- Advanced calculations (WAR, Defensive metrics) require play-by-play or tracking data and are out of scope for pure box-score parsing.
