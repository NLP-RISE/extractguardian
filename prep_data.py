from config import TAGS
import os
import argparse
import json
import pandas as pd
from typing import Union
from sklearn.model_selection import train_test_split
from pathlib import Path


def filter_by_tags(tags: list[str], category: str) -> bool:
    """Returns False if `tags` contains any tags it shares with other categories. Else, returns True"""
    filter_tags = []
    for k in TAGS.keys():
        if k != category:
            for tag in TAGS[k]:
                filter_tags.append(tag)

    for t in tags:
        if t in filter_tags:
            return False
    return True


def split_data(df, label_col: str = "category"):
    X_train, X_tmp, y_train, y_tmp = train_test_split(
        df, df[[label_col]], test_size=0.20, stratify=None, shuffle=True
    )
    X_dev, X_test, y_dev, y_test = train_test_split(
        X_tmp, y_tmp, test_size=0.50, stratify=None, shuffle=False
    )
    return X_train, X_dev, X_test, y_train, y_dev, y_test


def main():
    parser = argparse.ArgumentParser(
        description="Filter out articles with tags shared across categories"
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        default="articles",
        help="A directory with first level dirs as categories, containing JSON files (Crawling output from The Guardian).",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default="data",
        help="A directory for the data to land (split into train, dev, test)",
    )

    parser.add_argument(
        "--filter_by_tags",
        type=str,
        default="Y",
        choices=["Y", "N"],
        help="Whether or not to filter by tags. Case sensitive.",
    )
    args = parser.parse_args()

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    extracted_data: list[dict[str, Union[str, list]]] = []
    for d in os.listdir(args.data_dir):
        files = os.listdir(f"{args.data_dir}/{d}")
        for f in files:
            print(args.data_dir, d, f)
            file = json.load(open(f"{args.data_dir}/{d}/{f}", "r"))
            if file:
                for article in file:
                    id = article["id"]
                    title = article["webTitle"]
                    body = article["fields"]["bodyText"]
                    tags = [x["id"] for x in article["tags"]]
                    extracted_from_tag = (
                        f.replace("tag-", "").split("_articles")[0].replace("_", "/")
                    )
                    if body:
                        if len(body.split()) < 1000 and len(body.split()) >= 50:
                            extracted_data.append(
                                {
                                    "id": id,
                                    "title": title,
                                    "body": body,
                                    "tags": tags,
                                    "extracted_from_tag": extracted_from_tag,
                                    "category": d,
                                    "date": article["webPublicationDate"],
                                }
                            )
    df = pd.DataFrame(extracted_data)

    # merge "UNRELATED_TO_CLIMATE and SIMILAR_BUT_NOT_CLIMATE"
    df["category"] = df["category"].apply(
        lambda x: "UNRELATED_TO_CLIMATE" if x == "SIMILAR_BUT_NOT_CLIMATE" else x
    )

    if args.filter_by_tags == "Y":

        df["use"] = df.apply(
            lambda row: filter_by_tags(row["tags"], row["category"]), axis=1
        )
    elif args.filter_by_tags == "N":
        df["use"] = True

    print(f"Total rows: {len(df.index)}")
    print(f"Used rows: {len(df[df['use'] == True])}")

    df.to_csv(f"{args.output_dir}/all.csv", index=False)
    X_train, X_dev, X_test, y_train, y_dev, y_test = split_data(df[df["use"] == True])
    train, dev, test = pd.DataFrame(X_train), pd.DataFrame(X_dev), pd.DataFrame(X_test)
    train["label"], dev["label"], test["label"] = y_train, y_dev, y_test

    train.to_csv(f"{args.output_dir}/train.csv", index=False)
    dev.to_csv(f"{args.output_dir}/dev.csv", index=False)
    test.to_csv(f"{args.output_dir}/test.csv", index=False)


if __name__ == "__main__":
    main()
