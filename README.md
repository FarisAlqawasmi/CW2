# COMP3011 Coursework 2 — Search Engine Tool

This project implements core components of a search engine, including web crawling, indexing, and query processing, as covered in the module lectures.

## Overview

This repository contains coursework for **COMP3011 Web Services and Web Data** (University of Leeds). The project is a **search engine tool** that will crawl, index, and query content from **[quotes.toscrape.com](https://quotes.toscrape.com/)**. The planned command-line interface will support **`build`**, **`load`**, **`print`**, and **`find`** operations.

## Current status

The repository structure is in place, but the implementation is not yet complete. The crawler and other components will be developed in later stages.

## Repository structure

```
.
├── README.md
├── requirements.txt
├── data/              # Crawled data and index storage (placeholder)
├── src/
│   ├── main.py        # Entry point
│   ├── crawler.py
│   ├── indexer.py
│   └── search.py
└── tests/
    ├── test_crawler.py
    ├── test_indexer.py
    └── test_search.py
```

## Setup

1. Clone this repository (or extract the project folder).
2. Create and activate a Python virtual environment named **`env`** (see below).
3. Install dependencies from `requirements.txt`.

### Virtual environment (`env`)

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

### Run (placeholder)

```bash
python src/main.py
```

> **Note:** The search engine implementation is still in progress; behaviour may be incomplete until development is finished.

## Planned commands

The tool will support the following commands:

- `build` — crawl the website and build the index  
- `load` — load a previously saved index  
- `print` — display indexed information for a word  
- `find` — search for documents matching a query  