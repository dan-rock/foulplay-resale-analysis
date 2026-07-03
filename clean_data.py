"""
Clean and structure the Foulplay Grailed sold listings dataset.

The raw scrape is already in good shape (no dupes, prices clean, dates present).
This script does the light, honest cleaning and the useful structuring:

  1. Confirms no duplicate listings.
  2. Parses dates into real datetimes + adds year/month helpers.
  3. Splits the 'type.value' encoded fields (category, size) into clean columns.
  4. Normalizes condition labels into readable names + an ordered quality rank.
  5. Treats currency as USD (Grailed is USD-only; blanks are unstamped USD).
  6. Adds ask_vs_sold fields. NOTE: 'original_price' is the seller's LISTING
     price, not brand retail. So this measures negotiation, not resale premium.

Output: foulplay_clean.csv (for analysis. . .)
"""

import pandas as pd

RAW = "foulplay_sold.csv"
OUT = "foulplay_clean.csv"

# Readable names + a sensible quality ordering (higher = better condition)
CONDITION_MAP = {
    "is_new":            ("New",            5),
    "is_gently_used":    ("Gently used",    4),
    "is_used":           ("Used",           3),
    "is_worn":           ("Worn",           2),
    "is_not_specified":  ("Not specified",  1),
}


def main():
    df = pd.read_csv(RAW)
    start = len(df)

    # 1. de-dupe defensively (we expect zero)
    df = df.drop_duplicates(subset="id").reset_index(drop=True)
    print(f"Rows: {start} -> {len(df)} after de-dup ({start - len(df)} removed)")

    # 2. dates
    for col in ["sold_at", "created_at"]:
        df[col] = pd.to_datetime(df[col], utc=True, errors="coerce")
    df["sold_year"] = df["sold_at"].dt.year
    df["sold_month"] = df["sold_at"].dt.to_period("M").astype(str)
    # how long the piece sat listed before selling (days)
    df["days_to_sell"] = (df["sold_at"] - df["created_at"]).dt.days

    # 3. split 'type.value' encoded fields
    # category like 'tops.short_sleeve_shirts' -> garment_type='tops',
    #   item_type='short_sleeve_shirts'
    cat = df["category"].astype(str).str.split(".", n=1, expand=True)
    df["garment_type"] = cat[0]
    df["item_type"] = cat[1]

    # size like 'tops.l' -> size_value='l'  (the prefix repeats garment_type)
    sz = df["size"].astype(str).str.split(".", n=1, expand=True)
    df["size_value"] = sz[1].fillna(sz[0])

    # 4. condition
    df["condition_label"] = df["condition"].map(lambda c: CONDITION_MAP.get(c, (c, 0))[0])
    df["condition_rank"] = df["condition"].map(lambda c: CONDITION_MAP.get(c, (c, 0))[1])

    # 5. currency: all USD
    df["currency"] = "USD"

    # 6. ask vs sold (NEGOTIATION, not retail premium) 
    # original_price here = seller's listing/ask price, NOT brand retail.
    df["ask_price"] = df["original_price"]
    df["sold_vs_ask"] = df["sold_price"] - df["ask_price"]            # $ above/below ask
    df["sold_vs_ask_pct"] = (df["sold_vs_ask"] / df["ask_price"] * 100).round(1)

    # tidy column order for the analysis file 
    keep = [
        "id", "title", "designer",
        "garment_type", "item_type", "size_value",
        "condition_label", "condition_rank", "color",
        "ask_price", "sold_price", "sold_vs_ask", "sold_vs_ask_pct", "currency",
        "sold_at", "created_at", "days_to_sell",
        "sold_year", "sold_month", "url",
    ]
    df = df[keep]

    df.to_csv(OUT, index=False)
    print(f"Saved {len(df)} clean rows -> {OUT}")
    print("\nNew/derived columns added:")
    for c in ["garment_type", "item_type", "size_value", "condition_label",
              "condition_rank", "days_to_sell", "sold_vs_ask", "sold_vs_ask_pct",
              "sold_year", "sold_month"]:
        print(f"  - {c}")


if __name__ == "__main__":
    main()

