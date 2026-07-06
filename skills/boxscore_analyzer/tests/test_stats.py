from boxscore_analyzer.stats import basic_batting_stats, compute_woba


def test_basic_stats():
    players = [{"name": "A", "AB": 4, "H": 2, "2B": 1, "BB": 1, "SF": 0}]
    df = basic_batting_stats(players)
    assert df.iloc[0]["AVG"] == 0.5


def test_woba():
    row = {"AB": 4, "H": 2, "2B": 1, "BB": 1, "HBP": 0, "3B": 0, "HR": 0, "SF": 0, "SH": 0}
    w = compute_woba(row)
    assert w >= 0.0
