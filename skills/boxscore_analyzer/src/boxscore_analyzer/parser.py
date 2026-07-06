from typing import List, Dict, Optional, Tuple
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


def _extract_roster_candidates(lines: List[str]) -> Dict[int, str]:
    roster: Dict[int, str] = {}
    for line in lines:
        # find candidate lines containing a full name and jersey number
        m = re.search(r"([A-Za-z][A-Za-z\.'\- ]+?)\s+#(\d+)\b", line)
        if m:
            name = m.group(1).strip()
            number = _int_or_none(m.group(2))
            if number is not None and len(name.split()) >= 2:
                roster[number] = name
    return roster


def _match_full_name(name: str, number: Optional[int], roster: Dict[int, str]) -> Tuple[str, Optional[int], Optional[str]]:
    full_name = None
    matched_number = number
    if number is not None and number in roster:
        full_name = roster[number]
    elif number is None:
        # match by last-name prefix if roster line exists
        tokens = name.split()
        if tokens:
            last = tokens[-1].lower()
            for roster_num, roster_name in roster.items():
                roster_last = roster_name.split()[-1].lower()
                if roster_last.startswith(last) or last.startswith(roster_last):
                    full_name = roster_name
                    matched_number = roster_num
                    break
    if full_name is None:
        full_name = name
    return full_name, matched_number, name


def _normalize_name_and_number(name: str) -> Tuple[str, Optional[int]]:
    number = None
    mnum = re.search(r"#(\d+)\b", name)
    if mnum:
        number = _int_or_none(mnum.group(1))
        name = re.sub(r"#\d+", "", name).strip()
    return name, number


def parse_boxscore_text(raw: str) -> Dict:
    """Parse raw OCR text into a structured representation.

    Heuristic-based table parser that handles common mobile box score layouts.
    It extracts lineup rows (name, position, AB, R, H, RBI, BB, SO), team totals,
    TB/E notes, and a simple pitching table.
    """
    # normalize and split
    lines = [re.sub(r"\s+", " ", l).strip() for l in raw.splitlines() if l.strip()]
    roster = _extract_roster_candidates(lines)

    players: List[Dict] = []
    pitching: List[Dict] = []
    team_totals_batting: Dict = {}
    team_totals_pitching: Dict = {}
    batting_notes: Dict = {}

    section = None
    for line in lines:
        low = line.lower()
        if "lineup" in low or re.match(r"^[a-z ]+\s+ab\s+r\s+h", low):
            section = "lineup"
            continue
        if low.startswith("team ") and section == "lineup":
            toks = line.split()
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
            toks = line.split()
            if len(toks) >= 7:
                last6 = toks[-6:]
                name_tokens = toks[:-6]
                name = " ".join(name_tokens)
                pos = None
                m = re.search(r"\(([^)]+)\)\s*$", name)
                if m:
                    pos = m.group(1)
                    name = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
                name, number = _normalize_name_and_number(name)

                ab = _int_or_none(last6[0])
                r = _int_or_none(last6[1])
                h = _int_or_none(last6[2])
                rbi = _int_or_none(last6[3])
                bb = _int_or_none(last6[4])
                so = _int_or_none(last6[5])
                full_name, matched_number, display_name = _match_full_name(name, number, roster)

                players.append({
                    "name": display_name,
                    "full_name": full_name,
                    "number": matched_number,
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

    if not players:
        for line in lines:
            toks = line.split()
            if len(toks) >= 7:
                last6 = toks[-6:]
                if all(t == "-" or re.match(r"^\d+$", t) for t in last6):
                    name = " ".join(toks[:-6])
                    name, number = _normalize_name_and_number(name)
                    ab = _int_or_none(last6[0])
                    r = _int_or_none(last6[1])
                    h = _int_or_none(last6[2])
                    rbi = _int_or_none(last6[3])
                    bb = _int_or_none(last6[4])
                    so = _int_or_none(last6[5])
                    full_name, matched_number, display_name = _match_full_name(name, number, roster)
                    players.append({"name": display_name, "full_name": full_name, "number": matched_number, "pos": None, "AB": ab, "R": r, "H": h, "RBI": rbi, "BB": bb, "SO": so})

    return {
        "players": players,
        "pitching": pitching,
        "team_totals_batting": team_totals_batting,
        "team_totals_pitching": team_totals_pitching,
        "batting_notes": batting_notes,
    }