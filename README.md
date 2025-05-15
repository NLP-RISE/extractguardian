# ExtractGuardian

Code to extract articles from The Guardian using their [OpenPlatform API](https://open-platform.theguardian.com/access/).
The code extracts articles based on a set of tags and filters out articles that share one or more tags.

The list of tags is found in [`config.py`](config.py).

## Docs

### Setup

1. Get an access key from [the Guardian OpenPlatform](https://open-platform.theguardian.com/access/).
    A free developer key should be sufficient. Place your key inside the .env file. Example:

    ```bash
    ACCESS_KEY="5c32337f2-aa32-4066-ass3-25fdcebee2fc"
    ```

2. To install the dependencies, [download Poetry](https://python-poetry.org/docs/), install the dependencies, and activate the virtual environment:

    ```bash
    poetry install
    poetry env activate
    ```

### Run the code

To get the data through the API, run:

```bash
poetry run python3 get_data.py --mode tags --output_dir articles --tag all
```

To adjust the tags from which data is pulled, or add new tag categories, modify the [`config.py`](config.py) file as needed.

To split the data into a train, dev, and test set, run:

```bash
poetry run python3 prep_data.py --data_dir articles --output_dir dataset --filter_by_tags Y
```

To split the data **without filtering out articles that share tags across categories**, change the "filter by tags" flag:

```bash
poetry run python3 prep_data.py --data_dir articles --output_dir dataset --filter_by_tags N
```

The script above supports pulling articles by tags and keywords. Prepping data pulled based on keywords is not fully implemented.

> [!WARNING]  
> Keep in mind:
> In [`prep_data.py`](prep_data.py), the `UNRELATED_TO_CLIMATE` and `SIMILAR_BUT_NOT_CLIMATE` categories are merged.

### Plot the distribution of labels per year

```bash
poetry run python3 plot_data.py --data_dir dataset --data_split all
```

### Get help

Use the help function if you are lost:

```bash
poetry run python3 get_data.py --help
poetry run python3 prep_data.py --help
```

Otherwise, you are welcome to start a new issue on github.

## The Guardian Climate News Corpus

Are you looking for [The Guardian Climate News Corpus](https://huggingface.co/datasets/NLP-RISE/guardian_climate_news_corpus), as part of the [ClimateEval](https://github.com/MurathanKurfali/ClimateEval-Yaml) pipeline?

The Guardian Climate News Corpus was created using this same script, but the results are not deterministic. So, if you are looking to replicate the ClimateEval evaluation results [described in our paper](https://openreview.net/forum?id=183GtY94tB), use [the dataset provided on HuggingFace](https://huggingface.co/datasets/NLP-RISE/guardian_climate_news_corpus).

**This script is intended for creating similar datasets and extending the existing one.** To evaluate your model on your newly created dataset using the LM Evaluation Harness as part of ClimateEval, you need to first upload the dataset to HuggingFace. You can follow [this format](https://huggingface.co/datasets/NLP-RISE/guardian_climate_news_corpus/tree/main). Once your new dataset has been uploaded, manipulate [the LM harness YAML configs found here](https://github.com/MurathanKurfali/ClimateEval-Yaml/tree/main/guardian_climate_news) to refer to your newly created dataset instead.

## Citation

```bibtex
@inproceedings{
    kurfali2025climateeval,
    title={ClimateEval: A Comprehensive Benchmark for {NLP} Tasks Related to Climate Change},
    author={Murathan Kurfali and Shorouq Zahra and Joakim Nivre and Gabriele Messori},
    booktitle={The 2nd Workshop of Natural Language Processing meets Climate Change},
    year={2025},
    url={https://openreview.net/forum?id=183GtY94tB}
}
```

## Disclaimer

All articles extracted here are courtesy of Guardian News & Media Ltd.
Open License Terms can be found [here](https://www.theguardian.com/info/2022/nov/01/open-licence-terms)
