from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Allow tests to import modules from src/ when the project isn't packaged.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from indexer import InvertedIndexer  # noqa: E402


def test_tokenize_lowercases_keeps_numbers_removes_punctuation() -> None:
    indexer = InvertedIndexer()
    text = "Hello, WORLD!! 123 apples. B2B... can't? 42"
    tokens = indexer.tokenize(text)

    assert "hello" in tokens
    assert "world" in tokens
    assert "123" in tokens
    assert "42" in tokens
    assert "b2b" in tokens

    # punctuation should not appear as tokens
    assert "," not in tokens
    assert "world!!" not in tokens
    assert "apples." not in tokens


def test_add_document_stores_metadata_tf_positions_and_df() -> None:
    indexer = InvertedIndexer()

    indexer.add_document(
        doc_id=0,
        url="https://example.com/a",
        title="Doc A",
        text="Apple banana apple.",
    )
    indexer.add_document(
        doc_id=1,
        url="https://example.com/b",
        title="Doc B",
        text="banana apple",
    )

    # document metadata
    assert indexer.documents[0]["url"] == "https://example.com/a"
    assert indexer.documents[0]["title"] == "Doc A"
    assert indexer.documents[0]["word_count"] == 3

    # postings: term frequencies and positions
    apple_entry = indexer.inverted_index["apple"]
    assert apple_entry["df"] == 2
    assert apple_entry["postings"][0]["tf"] == 2
    assert apple_entry["postings"][0]["positions"] == [0, 2]
    assert apple_entry["postings"][1]["tf"] == 1
    assert apple_entry["postings"][1]["positions"] == [1]

    banana_entry = indexer.inverted_index["banana"]
    assert banana_entry["df"] == 2
    assert banana_entry["postings"][0]["tf"] == 1
    assert banana_entry["postings"][0]["positions"] == [1]
    assert banana_entry["postings"][1]["tf"] == 1
    assert banana_entry["postings"][1]["positions"] == [0]


def test_build_index_builds_from_crawler_style_pages() -> None:
    pages: dict[int, dict[str, object]] = {
        0: {
            "url": "https://example.com/a",
            "title": "A",
            "text": "cat dog cat",
            "links": [],
        },
        1: {
            "url": "https://example.com/b",
            "title": "B",
            "text": "dog",
            "links": [],
        },
    }

    indexer = InvertedIndexer()
    indexer.build_index(pages)

    assert len(indexer.documents) == 2
    assert indexer.documents[0]["url"] == "https://example.com/a"
    assert indexer.documents[1]["title"] == "B"

    assert indexer.inverted_index["cat"]["df"] == 1
    assert indexer.inverted_index["cat"]["postings"][0]["tf"] == 2
    assert indexer.inverted_index["cat"]["postings"][0]["positions"] == [0, 2]

    assert indexer.inverted_index["dog"]["df"] == 2
    assert indexer.inverted_index["dog"]["postings"][0]["tf"] == 1
    assert indexer.inverted_index["dog"]["postings"][1]["tf"] == 1


def test_save_and_load_restores_documents_and_postings(tmp_path: Path) -> None:
    indexer = InvertedIndexer()
    indexer.add_document(
        doc_id=0,
        url="https://example.com/a",
        title="A",
        text="alpha beta alpha",
    )

    out_file = tmp_path / "index.json"
    indexer.save_to_file(str(out_file))

    loaded = InvertedIndexer()
    loaded.load_from_file(str(out_file))

    assert loaded.documents[0]["url"] == "https://example.com/a"
    assert loaded.documents[0]["title"] == "A"
    assert loaded.documents[0]["word_count"] == 3

    alpha = loaded.inverted_index["alpha"]
    assert alpha["df"] == 1
    assert 0 in alpha["postings"]
    assert alpha["postings"][0]["tf"] == 2
    assert alpha["postings"][0]["positions"] == [0, 2]
