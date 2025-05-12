import pandas as pd
import matplotlib.pyplot as plt
import argparse
from time import time 

plt.style.use("tableau-colorblind10")
from config import TAGS

def main() -> None: 
    parser = argparse.ArgumentParser(
        description="Plot data split",
    )

    parser.add_argument(
        "--data_dir",
        type=str,
        default="dataset",
        help="Directory containing dataset (split as `dev`, `test`, `train` and `all`)",
    )

    parser.add_argument(
        "--data_split",
        type=str,
        default="all",
        help="Select the data split",
        choices=["dev", "test", "train", "all"]
    )
    
    args = parser.parse_args()

    print("loading data...")
    df = pd.read_csv(f"{args.data_dir}/{args.data_split}.csv")
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
    output_filename = f"barchart_label_per_year_{time()}.png"
    print(f"storing .png at {output_filename}")
    chart = fig.get_figure()
    chart.savefig(output_filename)

if __name__ == "__main__":
    main()
