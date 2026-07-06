import argparse
from .ocr import ocr_image
from .parser import parse_boxscore_text
from .stats import basic_batting_stats, compute_woba


def main():
    parser = argparse.ArgumentParser(description="Process a boxscore image and print stats")
    parser.add_argument("image", help="Path to boxscore image")
    args = parser.parse_args()
    raw = ocr_image(args.image)
    parsed = parse_boxscore_text(raw)
    df = basic_batting_stats(parsed.get("players", []))
    if not df.empty:
        df["wOBA"] = df.apply(lambda r: compute_woba(r.to_dict()), axis=1)
    print(df.to_csv(index=False))


if __name__ == "__main__":
    main()
