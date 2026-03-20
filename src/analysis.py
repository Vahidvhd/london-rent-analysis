import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


plt.style.use("bmh")


def build_summary():
    df = pd.read_csv("data/raw_data.csv")

    df = df.dropna(subset=["area", "rent", "beds"])
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


def save_bedroom_report_pdf(summary):
    os.makedirs("output", exist_ok=True)

    pdf_path = "output/bedroom_rent_report.pdf"

    bed_values = sorted(summary["beds"].unique())

    with PdfPages(pdf_path) as pdf:
        for bed in bed_values:
            selected = summary[summary["beds"] == bed].sort_values("avg_rent")

            fig, ax = plt.subplots(figsize=(12, 7))

            ax.barh(selected["area"], selected["avg_rent"], color="#4C78A8")
            ax.set_xlim(0, selected["avg_rent"].max() * 1.15)

            for _, row in selected.iterrows():
                ax.text(
                    row["avg_rent"] / 2,
                    row["area"],
                    f'n={row["listing_count"]} | med £{int(row["median_rent"]):,}',
                    ha="center",
                    va="center",
                    color="white"
                )

                ax.text(
                    row["avg_rent"] + 20,
                    row["area"],
                    f'£{int(row["avg_rent"]):,}',
                    ha="left",
                    va="center",
                    color="black"
                )

            bed_label = "Studio" if bed == 0 else f"{bed}-Bed"
            ax.set_title(f"{bed_label} Average Rent by Area")
            ax.set_xlabel("Average Rent (£)")
            ax.set_ylabel("")

            ax.grid(axis="x", linestyle="--", alpha=0.4)
            ax.grid(axis="y", visible=False)
            ax.set_axisbelow(True)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

    print(f"Saved PDF report to {pdf_path}")


def run_analysis():
    summary = build_summary()
    save_bedroom_report_pdf(summary)


if __name__ == "__main__":
    run_analysis()