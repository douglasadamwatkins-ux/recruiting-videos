from typing import List, Dict, Optional
import re


def _int_or_none(tok: str) -> Optional[int]:
    if tok is None:
        return None
    tok = tok.strip()
    if tok == "-" or tok == "":
        return None
    try:
        return int(tok)
    except ValueError:
        return None


def parse_boxscore_text(raw: str) -> Dict:
    """Parse raw OCR text into a structured representation.

    Heuristic-based table parser that handles common mobile box score layouts.
    It extracts lineup rows (name, position, AB, R, H, RBI, BB, SO), team totals,
    TB/E notes, and a simple pitching table.
    """
    # normalize and split
    lines = [re.sub(r"\s+", " ", l).strip() for l in raw.splitlines() if l.strip()]

    players: List[Dict] = []
    pitching: List[Dict] = []
    team_totals_batting: Dict = {}
    team_totals_pitching: Dict = {}
    batting_notes: Dict = {}

    section = None
    for i, line in enumerate(lines):
        low = line.lower()
        if "lineup" in low or re.match(r"^[a-z ]+\s+ab\s+r\s+h", low):
            section = "lineup"
            continue
        if low.startswith("team ") and section == "lineup":
            # parse team totals batting: numbers after TEAM
            toks = line.split()
            # expect: TEAM AB R H RBI BB SO
            if len(toks) >= 7:
                team_totals_batting = {
                    "AB": _int_or_none(toks[-6]),
                    "R": _int_or_none(toks[-5]),
                    "H": _int_or_none(toks[-4]),
                    "RBI": _int_or_none(toks[-3]),
                    "BB": _int_or_none(toks[-2]),
                    "SO": _int_or_none(toks[-1]),
                }
            section = None
            continue
        if low.startswith("tb:"):
            batting_notes["TB"] = line[len("TB:"):].strip()
            continue
        if low.startswith("e:"):
            es = line[len("E:"):].strip()
            batting_notes["E"] = [e.strip() for e in es.split(",") if e.strip()]
            continue
        if "pitching" in low:
            section = "pitching"
            continue
        if section == "lineup":
            # Heuristic: last 6 tokens are AB R H RBI BB SO (may be '-' placeholders)
            toks = line.split()
            if len(toks) >= 7:
                last6 = toks[-6:]
                name_tokens = toks[:-6]
                name = " ".join(name_tokens)
                # attempt to extract position in parentheses at end of name
                pos = None
                m = re.search(r"\(([^)]+)\)\s*$", name)
                if m:
                    pos = m.group(1)
                    name = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()

                ab = _int_or_none(last6[0])
                r = _int_or_none(last6[1])
                h = _int_or_none(last6[2])
                rbi = _int_or_none(last6[3])
                bb = _int_or_none(last6[4])
                so = _int_or_none(last6[5])

                players.append({
                    "name": name,
                    "pos": pos,
                    "AB": ab,
                    "R": r,
                    "H": h,
                    "RBI": rbi,
                    "BB": bb,
                    "SO": so,
                })
            continue
        if section == "pitching":
            toks = line.split()
            # expect: Name IP H R ER BB SO  (IP may be like 3.2)
            if len(toks) >= 6:
                last6 = toks[-6:]
                name = " ".join(toks[:-6])
                ip = last6[0]
                h = _int_or_none(last6[1])
                r = _int_or_none(last6[2])
                er = _int_or_none(last6[3])
                bb = _int_or_none(last6[4])
                so = _int_or_none(last6[5])
                pitching.append({"name": name.strip(), "IP": ip, "H": h, "R": r, "ER": er, "BB": bb, "SO": so})
                continue

    # Fallback: if no players found, attempt loose heuristic scan for lines with 6 trailing tokens
    if not players:
        for line in lines:
            toks = line.split()
            if len(toks) >= 7:
                last6 = toks[-6:]
                if all(t == "-" or re.match(r"^\d+$", t) for t in last6):
                    name = " ".join(toks[:-6])
                    ab = _int_or_none(last6[0])
                    r = _int_or_none(last6[1])
                    h = _int_or_none(last6[2])
                    rbi = _int_or_none(last6[3])
                    bb = _int_or_none(last6[4])
                    so = _int_or_none(last6[5])
                    players.append({"name": name, "pos": None, "AB": ab, "R": r, "H": h, "RBI": rbi, "BB": bb, "SO": so})

    return {
        "players": players,
        "pitching": pitching,
        "team_totals_batting": team_totals_batting,
        "team_totals_pitching": team_totals_pitching,
        "batting_notes": batting_notes,
    }
