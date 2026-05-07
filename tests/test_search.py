from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Allow tests to import modules from src/ when the project isn't packaged.
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from search import SearchEngine  # noqa: E402


@pytest.fixture()
def fake_index_and_docs() -> tuple[dict[str, dict[str, object]], dict[int, dict[str, object]]]:
    documents: dict[int, dict[str, object]] = {
        0: {"url": "https://example.com/a", "title": "Doc A", "word_count": 3},
        1: {"url": "https://example.com/b", "title": "Doc B", "word_count": 2},
        2: {"url": "https://example.com/c", "title": "Doc C", "word_count": 2},
    }

    inverted_index: dict[str, dict[str, object]] = {
        "apple": {
            "df": 2,
            "postings": {
                0: {"tf": 3, "positions": [0, 1, 2]},
                1: {"tf": 1, "positions": [0]},
            },
        },
        "banana": {
            "df": 2,
            "postings": {
                0: {"tf": 1, "positions": [1]},
                2: {"tf": 2, "positions": [0, 1]},
            },
        },
        "carrot": {
            "df": 1,
            "postings": {
                2: {"tf": 5, "positions": [0, 1, 2, 3, 4]},
            },
        },
    }

    return inverted_index, documents


def test_lookup_term_existing_term_returns_postings(
    fake_index_and_docs: tuple[dict[str, dict[str, object]], dict[int, dict[str, object]]],
) -> None:
    inverted_index, documents = fake_index_and_docs
    engine = SearchEngine(inverted_index, documents)

    postings = engine.lookup_term("apple")
    assert set(postings.keys()) == {0, 1}
    assert postings[0]["tf"] == 3
    assert postings[1]["positions"] == [0]


def test_lookup_term_missing_term_returns_empty_dict(
    fake_index_and_docs: tuple[dict[str, dict[str, object]], dict[int, dict[str, object]]],
) -> None:
    inverted_index, documents = fake_index_and_docs
    engine = SearchEngine(inverted_index, documents)

    assert engine.lookup_term("missing") == {}


def test_search_single_word_returns_results_sorted_by_score_desc(
    fake_index_and_docs: tuple[dict[str, dict[str, object]], dict[int, dict[str, object]]],
) -> None:
    inverted_index, documents = fake_index_and_docs
    engine = SearchEngine(inverted_index, documents)

    results = engine.search("apple")
    assert [r["doc_id"] for r in results] == [0, 1]  # tf: 3 then 1
    assert results[0]["score"] == 3
    assert results[0]["title"] == "Doc A"
    assert results[0]["url"] == "https://example.com/a"


def test_search_multi_word_is_conjunctive_and_scores_sum_tf(
    fake_index_and_docs: tuple[dict[str, dict[str, object]], dict[int, dict[str, object]]],
) -> None:
    inverted_index, documents = fake_index_and_docs
    engine = SearchEngine(inverted_index, documents)

    results = engine.search("apple banana")
    assert len(results) == 1
    assert results[0]["doc_id"] == 0
    assert results[0]["score"] == 4  # apple tf=3 + banana tf=1


def test_search_returns_empty_list_when_any_term_missing(
    fake_index_and_docs: tuple[dict[str, dict[str, object]], dict[int, dict[str, object]]],
) -> None:
    inverted_index, documents = fake_index_and_docs
    engine = SearchEngine(inverted_index, documents)

    assert engine.search("apple missing") == []


def test_search_returns_empty_list_for_empty_query(
    fake_index_and_docs: tuple[dict[str, dict[str, object]], dict[int, dict[str, object]]],
) -> None:
    inverted_index, documents = fake_index_and_docs
    engine = SearchEngine(inverted_index, documents)

    assert engine.search("") == []
    assert engine.search("   ") == []
