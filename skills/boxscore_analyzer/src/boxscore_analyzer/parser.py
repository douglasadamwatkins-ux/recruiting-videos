from typing import List, Dict
import re


def parse_boxscore_text(raw: str) -> Dict:
    """Parse raw OCR text into a simplified structured representation.

    This is a lightweight heuristic parser. Real box scores vary widely; you'll
    want to extend this with layout-based parsing or ML-based table extraction.
    """
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    players = []
    team = None
    for line in lines:
        # very simple heuristic: lines starting with a name-like token and numbers
        m = re.match(r"^([A-Za-z'\-\. ]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
        if m:
            name = m.group(1).strip()
            ab = int(m.group(2))
            r = int(m.group(3))
            h = int(m.group(4))
            rbi = int(m.group(5))
            players.append({"name": name, "AB": ab, "R": r, "H": h, "RBI": rbi})
    return {"players": players}
