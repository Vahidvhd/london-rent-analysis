import pandas as pd


def build_summary():
    df = pd.read_csv("data/raw_data.csv")

    df = df.dropna(subset=["area", "rent", "beds"])
    df["beds"] = df["beds"].replace("studio", 0)
    df["beds"] = df["beds"].astype(int)
    df = df[df["beds"] <= 4]

    listing_count = (
        df.groupby(["area", "beds"])
        .size()
        .reset_index(name="listing_count")
    )

    avg_rent = (
        df.groupby(["area", "beds"])["rent"]
        .mean()
        .reset_index(name="avg_rent")
    )

    median_rent = (
        df.groupby(["area", "beds"])["rent"]
        .median()
        .reset_index(name="median_rent")
    )

    summary = (
        listing_count
        .merge(avg_rent, on=["area", "beds"])
        .merge(median_rent, on=["area", "beds"])
        .sort_values(["beds", "avg_rent"])
    )

    return summary