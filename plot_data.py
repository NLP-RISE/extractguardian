import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("tableau-colorblind10")
from config import TAGS


def main() -> None:
    print("loading data...")
    df = pd.read_csv("data/all.csv")
    df["datetime"] = pd.to_datetime(df["date"])
    df["year"] = df["datetime"].dt.year

    print("merging `UNRELATED_TO_CLIMATE` with `SIMILAR_BUT_NOT_CLIMATE`")

    df["category"] = df["category"].apply(
        lambda x: "UNRELATED_TO_CLIMATE" if x == "SIMILAR_BUT_NOT_CLIMATE" else x
    )
    tags = [x for x in list(TAGS.keys()) if x != "SIMILAR_BUT_NOT_CLIMATE"]

    dfs = {}
    for category in tags:
        dfs[category] = (
            df[(df["use"] == True) & (df["category"] == category)]
            .groupby(["year"])["category"]
            .count()
        )

    stacked_df = pd.DataFrame(dfs)

    print("plotting...")
    stacked_df = stacked_df.fillna(0)
    fig = stacked_df.plot(
        kind="bar", stacked=True, xlabel="year", ylabel="number of articles"
    )

    chart = fig.get_figure()
    chart.savefig('barchart_label_per_year.png')

if __name__ == "__main__":
    main()
