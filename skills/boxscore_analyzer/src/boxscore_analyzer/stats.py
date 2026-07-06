from typing import Dict, List, Optional
import pandas as pd


def basic_batting_stats(players: List[Dict]) -> pd.DataFrame:
    """Compute basic batting stats (AVG, SLG, OBP, OPS) for a list of player dicts.

    Expected fields per player: AB, H, 2B (optional), 3B (optional), HR (optional), BB (optional), HBP (optional), SF (optional)
    """
    df = pd.DataFrame(players).fillna(0)
    df["AVG"] = df.apply(lambda r: (r.get("H", 0) / r.get("AB", 1)) if r.get("AB", 0) > 0 else 0.0, axis=1)
    # total bases
    df["TB"] = df.get("1B", df.get("H", 0)) + df.get("2B", 0) * 2 + df.get("3B", 0) * 3 + df.get("HR", 0) * 4
    df["SLG"] = df.apply(lambda r: (r.get("TB", 0) / r.get("AB", 1)) if r.get("AB", 0) > 0 else 0.0, axis=1)
    df["OBP"] = df.apply(
        lambda r: (
            (r.get("H", 0) + r.get("BB", 0) + r.get("HBP", 0)) /
            (r.get("AB", 0) + r.get("BB", 0) + r.get("HBP", 0) + r.get("SF", 0))
        ) if (r.get("AB", 0) + r.get("BB", 0) + r.get("HBP", 0) + r.get("SF", 0)) > 0 else 0.0,
        axis=1,
    )
    df["OPS"] = df["OBP"] + df["SLG"]
    return df


def compute_woba(row: Dict, weights: Optional[Dict] = None) -> float:
    """Compute wOBA for a player's stat row. Provide weights or use defaults.

    Defaults are approximate league-average linear weights — you may replace them
    with season-specific weights for better accuracy.
    """
    if weights is None:
        weights = {"BB": 0.69, "HBP": 0.72, "1B": 0.88, "2B": 1.24, "3B": 1.56, "HR": 1.95}
    BB = row.get("BB", 0)
    HBP = row.get("HBP", 0)
    _1B = row.get("1B", row.get("H", 0) - row.get("2B", 0) - row.get("3B", 0) - row.get("HR", 0))
    _2B = row.get("2B", 0)
    _3B = row.get("3B", 0)
    HR = row.get("HR", 0)
    PA = row.get("AB", 0) + BB + HBP + row.get("SF", 0) + row.get("SH", 0)
    if PA == 0:
        return 0.0
    numerator = weights["BB"] * BB + weights["HBP"] * HBP + weights["1B"] * _1B + weights["2B"] * _2B + weights["3B"] * _3B + weights["HR"] * HR
    return numerator / PA
