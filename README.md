# extractguardian

Code to extract articles from The Guardian using their OpenPlatform API.
The code extracts articles based on a set of tags and filters out articles that share one or more tags.

The list of tags is found in [`config.py`](config.py).

## Setup

1. Get an access key from The Guardian [here](https://open-platform.theguardian.com/access/).
    A free developer key should be sufficient. Place your key inside the .env file. Example:

    ```bash
    ACCESS_KEY="5c32337f2-aa32-4066-ass3-25fdcebee2fc"
    ```

2. To install the dependencies, [download Poetry](https://python-poetry.org/docs/), install the dependencies, and activate the virtual environment: ```poetry install && poetry env activare```

## Run the code

To get the data through the API, run:

```bash
poetry run python3 get_data.py
```

To adjust the tags from which data is pulled, or add new tag categories, modify the [`config.py`](config.py) file as needed.

To split the data into a train, dev, and test set, run:

```bash
poetry run python3 prep_data.py --mode tags --output_dir articles --tag all
```

The script above supports pulling articles by tags and keywords. Prepping data pulled based on keywords is not fully implemented.

Use the help function if you are lost:

```bash
poetry run python3 prep_data.py --help
```

## Disclaimer

All articles extracted here are courtesy of Guardian News & Media Ltd.
Open License Terms can be found [here](https://www.theguardian.com/info/2022/nov/01/open-licence-terms)
