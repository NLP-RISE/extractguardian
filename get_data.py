import argparse
import json
import os
import time

import requests
from pathlib import Path 
from config import KEY, TAGS, KEYWORDS

# Define the Guardian API key and base URL
API_KEY = KEY
BASE_URL = "https://content.guardianapis.com/search"

# Define the date range for the search
start_date = "1900-01-01"
end_date = "2024-12-31"


# Function to fetch articles by keyword or tag
def fetch_articles(search_term=None, tag=None, page=1):
    params = {
        "api-key": API_KEY,
        "from-date": start_date,
        "to-date": end_date,
        "page": page,
        "page-size": 200,
        "show-fields": "all",
        "show-tags": "all",
        "order-by": "newest",
    }

    if search_term:
        params["q"] = search_term
    elif tag:
        params["tag"] = tag

    response = requests.get(BASE_URL, params=params)
    # (response.url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.url)
        return None


# Function to collect articles based on keywords
def collect_data(terms, output_dir, is_keyword=True, start_date="", end_date=""):
    """
    Collect articles based on keywords or tags.

    Parameters:
    - terms: List of keywords or tags.
    - output_dir: Directory to save the output files.
    - is_keyword: Boolean indicating if the terms are keywords (True) or tags (False).
    - start_date: Start date for filename.
    - end_date: End date for filename.
    """
    term_type = "keyword" if is_keyword else "tag"
    all_data = {}

    for term in terms:
        all_articles = []
        print(f"Fetching articles for {term_type}: {term}")
        current_page = 1
        max_pages = 10 if is_keyword else 15

        while current_page <= max_pages:
            data = fetch_articles(
                search_term=term if is_keyword else None,
                tag=term if not is_keyword else None,
                page=current_page,
            )
            if data:
                articles = data["response"]["results"]
                all_articles.extend(articles)
                total_pages = data["response"].get("pages")
                if max_pages == 2:
                    max_pages = total_pages
                print(
                    f"Fetched page {current_page} of {total_pages} for {term_type} '{term}'"
                )
                current_page += 1
                time.sleep(1)
            else:
                break
        backslash_char = '"'
        filename = os.path.join(
            output_dir,
            f"{term_type}-{term.replace(' ', '_').replace('/', '_').replace(backslash_char, '')}_articles_{start_date}_to_{end_date}.json",
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=4)
        all_data[term] = all_articles

    print(f"{term_type.capitalize()}-based data collection completed.")


# Main function with argparse for command-line interface
def main(TAGS=TAGS):
    parser = argparse.ArgumentParser(
        description="Fetch articles from The Guardian API based on keywords or tags."
    )
    parser.add_argument(
        "--mode",
        choices=["keywords", "tags"],
        required=True,
        help="Choose whether to search by keywords or tags.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="jsons",
        help="Directory to save output JSON files.",
    )

    tag_choices = list(TAGS.keys()).copy()
    tag_choices.append("all")
    parser.add_argument(
        "--tag",
        type=str,
        choices=tag_choices,
        required=False,
        help="Which tag category to use for crawling.",
        default="",
    )

    args = parser.parse_args()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True) 
        
    if args.mode == "keywords":
        os.makedirs(args.output_dir, exist_ok=True)
        collect_data(
            KEYWORDS,
            output_dir=args.output_dir,
            is_keyword=True,
            start_date=start_date,
            end_date=end_date,
        )
    elif args.mode == "tags" and args.tag == "all":
        for t in TAGS.keys():
            os.makedirs(f"{args.output_dir}/{t}", exist_ok=True)
            collect_data(
                TAGS[t],
                output_dir=f"{args.output_dir}/{t}",
                is_keyword=False,
                start_date=start_date,
                end_date=end_date,
            )
    elif args.mode == "tags" and args.tag not in ["", "all"]:
        os.makedirs(f"{args.output_dir}/{args.tag}", exist_ok=True)
        collect_data(
            TAGS[args.tag],
            output_dir=f"{args.output_dir}/{args.tag}",
            is_keyword=False,
            start_date=start_date,
            end_date=end_date,
        )


# Entry point for the script
if __name__ == "__main__":
    main()
