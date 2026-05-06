"""
Search engine structure for the COMP3011 search engine tool.

This module provides a minimal scaffold. Ranking and CLI integration are added
in later stages.
"""

from __future__ import annotations


class SearchEngine:
    """
    Run queries against an inverted index and document store.

    Attributes:
        inverted_index: Term -> metadata (e.g. df, postings) from the indexer.
        documents: doc_id -> document metadata (e.g. url, title, word_count).
    """

    def __init__(
        self,
        inverted_index: dict[str, dict[str, object]],
        documents: dict[int, dict[str, object]],
    ) -> None:
        """
        Initialise the search engine with index and document data.

        Args:
            inverted_index: The inverted index built by ``InvertedIndexer``.
            documents: Per-document metadata keyed by document id.
        """
        self.inverted_index: dict[str, dict[str, object]] = inverted_index
        self.documents: dict[int, dict[str, object]] = documents

    def lookup_term(self, term: str) -> dict[int, dict[str, object]]:
        """
        Look up postings for a single term (placeholder).

        Args:
            term: Raw query term (normalisation not implemented yet).

        Returns:
            Mapping from doc_id to posting data for that term. Currently empty.
        """
        _ = term
        return {}

    def search(self, query: str) -> list[dict[str, object]]:
        """
        Run a full-text search for the given query (placeholder).

        Args:
            query: User search string.

        Returns:
            Ranked or unranked result list. Currently empty.
        """
        _ = query
        return []
