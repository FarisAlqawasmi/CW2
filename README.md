# COMP3011 Coursework 2 — Search Engine Tool

## Overview

This repository contains coursework for **COMP3011 Web Services and Web Data**. The project implements a small **search engine tool** that crawls and indexes content from `https://quotes.toscrape.com/`, then supports simple term lookup and conjunctive (AND) querying via an interactive command-line interface.

## Current status

- The tool is functional end-to-end: **crawl → index → save/load → query**.
- `build` crawls `https://quotes.toscrape.com/`, builds an inverted index, and saves it to `data/index.json`.
- `load` loads the saved index from `data/index.json`.
- `print <word>` displays **df**, per-document **tf**, token **positions**, and document **URLs**.
- `find <query>` runs **conjunctive search** and prints scored results.
- Tests are implemented using `pytest`.

## Repository structure

```bash
.
├── README.md
├── requirements.txt
├── data/
│   └── index.json
├── src/
│   ├── main.py
│   ├── crawler.py
│   ├── indexer.py
│   └── search.py
└── tests/
    ├── test_crawler.py
    ├── test_indexer.py
    └── test_search.py
```

## Setup

1. Clone this repository.
2. Create and activate a Python virtual environment named `env`.
3. Install dependencies from `requirements.txt`.

### Create a virtual environment (`env`)

**macOS / Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

**Windows (Command Prompt):**

```bash
python -m venv env
env\Scripts\activate.bat
```

**Windows (PowerShell):**

```bash
python -m venv env
env\Scripts\Activate.ps1
```

### Install dependencies

With `env` activated:

```bash
pip install -r requirements.txt
```

## Run the command-line interface

```bash
python src/main.py
```

You should see a prompt like:

```text
search>
```

## Available commands

- `build`: crawl `https://quotes.toscrape.com/`, build the inverted index, and save it to `data/index.json`
- `load`: load a saved index from `data/index.json`
- `print <word>`: display index information for a single word (df, tf, positions, and URLs)
- `find <query>`: search using conjunctive (AND) matching with TF-IDF ranking
- `help`: display the available commands
- `exit`: quit the program

## Usage examples

### `build`

```text
search> build
Pages crawled: 3
Documents indexed: 3
Unique terms: 448
Index saved to: data/index.json
```

### `load`

```text
search> load
Documents loaded: 3
Unique terms loaded: 448
```

### `print <word>`

```text
search> print truth
Word: "truth"
Document frequency (df): 1
- doc_id: 0
  tf: 1
  positions: [42]
  url: https://quotes.toscrape.com/
```

### `find <query>`

```text
search> find life truth
[5.1507] Quotes to Scrape - https://quotes.toscrape.com/
```

## Testing

Run all tests:

```bash
pytest
```

Run individual test files:

```bash
pytest tests/test_crawler.py
pytest tests/test_indexer.py
pytest tests/test_search.py
```

## Dependencies

Install all dependencies with:

```bash
pip install -r requirements.txt
```

This project uses:

- `requests`
- `beautifulsoup4`
- `pytest`

## Limitations and Future Improvements

Current limitations of the system include:

- No stopword removal
- No stemming or lemmatization
- No phrase querying
- No wildcard querying
- Limited crawling scope (`max_pages=3` during demonstrations)
- Basic conjunctive (AND) retrieval only

The search engine currently uses TF-IDF scoring for ranking, but future improvements could include:

- BM25 ranking
- PageRank-style authority scoring
- Snippet generation
- Larger-scale crawling
- Better token normalization
- Query expansion and spelling correction
- Positional phrase search using stored token positions
